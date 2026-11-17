"""Maintain a current zizmor report and notify only semantic finding changes."""
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

TITLE = "zizmor: Actions security findings"
START = "<!-- scanning-service:zizmor-report:start -->"
END = "<!-- scanning-service:zizmor-report:end -->"
STATE = "<!-- scanning-service:zizmor-state:"
RANK = {"Informational": 0, "Low": 1, "Medium": 2, "High": 3}


def gh(*args):
    return subprocess.run(["gh", *args], check=True, text=True,
                          capture_output=True, timeout=180).stdout


def pages(endpoint):
    return [item for page in json.loads(gh("api", "--paginate", "--slurp", endpoint))
            for item in page]


def findings(raw, root):
    result = {}
    occurrences = {}
    for finding in raw:
        if finding["ignored"]:
            continue
        primary = next(location for location in finding["locations"]
                       if location["symbolic"]["kind"] == "Primary")
        symbolic = primary["symbolic"]
        path = Path(symbolic["key"]["Local"]["verbatim_path"])
        relative = path.relative_to(root).as_posix() if path.is_absolute() else path.as_posix()
        if not relative.startswith(".github/") or ".." in Path(relative).parts:
            raise ValueError("Unexpected finding path")
        route = symbolic["route"]["route"]
        # Anchor step indices by id/name, so inserting unrelated steps does not
        # notify again. Unnamed steps conservatively retain symbolic indices.
        hidden = [loc for loc in finding["locations"] if loc["symbolic"]["kind"] == "Hidden"]
        for anchor in hidden:
            anchor_route = anchor["symbolic"]["route"]["route"]
            if route[:len(anchor_route)] == anchor_route and anchor_route and "Index" in anchor_route[-1]:
                feature = anchor["concrete"]["feature"]
                # Only fields at the concrete step's indentation, never fields
                # embedded in run blocks or nested with/env mappings.
                lines = [line for line in feature.splitlines() if line.strip()]
                indentation = anchor["concrete"]["location"]["start_point"]["column"]
                fields = "\n".join([lines[0].lstrip()] + [line[indentation:] for line in lines[1:]
                                   if len(line) - len(line.lstrip()) == indentation])
                name = re.search(r"^(?:-\s*)?id:\s*(.+)$", fields, re.M)
                name = name or re.search(r"^(?:-\s*)?name:\s*(.+)$", fields, re.M)
                if name:
                    route = route[:len(anchor_route)-1] + [{"Step": name[1].strip()}] + route[len(anchor_route):]
        kind = symbolic["feature_kind"]
        fragment = kind.get("Subfeature", {}).get("fragment") if isinstance(kind, dict) else None
        identity = json.dumps([finding["ident"], relative, route, fragment], sort_keys=True)
        # Distinguish repeated expressions at the same symbolic construct by
        # occurrence order rather than character offsets or line numbers.
        occurrence = occurrences.get(identity, 0)
        occurrences[identity] = occurrence + 1
        key = hashlib.sha256(f"{identity}:{occurrence}".encode()).hexdigest()
        severity = finding["determinations"]["severity"]
        if severity not in RANK:
            raise ValueError("Unknown finding severity")
        result[key] = {"rule": finding["ident"], "path": relative, "severity": severity,
                       "line": primary["concrete"]["location"]["start_point"]["row"] + 1,
                       "fixes": sorted({fix["disposition"] for fix in finding["fixes"]})}
    return result


def state(body):
    match = re.search(re.escape(STATE) + r"([A-Za-z0-9+/=]+) -->", body)
    if not match:
        return None
    value = json.loads(base64.b64decode(match[1], validate=True))
    if value["version"] != 1:
        raise ValueError("Unsupported report state version")
    return value["findings"]


def changes(previous, current):
    if previous is None:
        return {}
    return {
        "New findings": [current[key] for key in sorted(current.keys() - previous.keys())],
        "Severity increased": [current[key] for key in sorted(current.keys() & previous.keys())
                               if RANK[current[key]["severity"]] > RANK[previous[key]["severity"]]],
        "No longer reported": [previous[key] for key in sorted(previous.keys() - current.keys())],
    }


def entry(repo, commit, finding):
    return (f"- **{finding['severity']} — {finding['rule']}**: "
            f"[{finding['path']}:{finding['line']}]"
            f"(https://github.com/{repo}/blob/{commit}/{finding['path']}#L{finding['line']})")


def footer(timestamp):
    return ("*Updated by [GSA-TTS scanning service](https://github.com/GSA-TTS/scanning-service) "
            f"at {timestamp:%Y-%m-%d %H:%M UTC}. Runs weekly on Wednesdays.*")


def report(repo, commit, version, run_url, current, prs, notification_marker=None, closed_at=None, reopened_event=None):
    timestamp = dt.datetime.now(dt.timezone.utc)
    counts = ", ".join(f"{sum(item['severity'] == severity for item in current.values())} "
                       f"{severity.lower()}" for severity in reversed(RANK))
    lines = [START, f"# Actions Security Status — {timestamp.date()}", "",
             f"**Summary:** {len(current)} {'finding' if len(current) == 1 else 'findings'} — {counts}.", "",
             f"Audited commit: `{commit}` · zizmor {version} · [Scan run]({run_url})", ""]
    if any(item["severity"] == "High" for item in current.values()):
        lines += ["> [!WARNING]", "> **Action required:** High-severity findings require review.", ""]
    lines += ["### Findings", ""]
    for key in sorted(current):
        item = current[key]
        disposition = ("Safe autofix available" if "safe" in item["fixes"] else
                       "Unsafe autofix requires manual review" if "unsafe" in item["fixes"] else
                       "No autofix available")
        lines.append(entry(repo, commit, item) + f" — {disposition}.")
    if not current:
        lines.append("No findings reported by this successful scan.")
    if prs:
        lines += ["", "### Open automated remediation PRs"]
        lines += [f"- [#{pr['number']}](https://github.com/{repo}/pull/{pr['number']})" for pr in prs]
    lines += ["", "Unsafe fixes are not applied automatically. Findings no longer reported may reflect "
              "code, suppression, configuration, or scanner changes—not necessarily a fix.", "",
              "Subscribe to this issue to be notified of new findings, severity escalations, "
              "and findings no longer reported. Use sub-issues to discuss remediations, "
              "record risk decisions, and link to relevant PRs.", "", "---", "", footer(timestamp), ""]
    encoded = base64.b64encode(json.dumps({"version": 1, "findings": current,
                                          "commit": commit, "run": run_url,
                                          "notification": notification_marker,
                                          "closed_at": closed_at,
                                          "reopened_event": reopened_event}, sort_keys=True).encode()).decode()
    return "\n".join(lines + [STATE + encoded + " -->", END])


def replace_report(body, section):
    if START in body or END in body:
        if body.count(START) != 1 or body.count(END) != 1 or body.index(END) < body.index(START):
            raise ValueError("Malformed managed section; refusing to overwrite")
        start, end = body.index(START), body.index(END) + len(END)
        return body[:start] + section + body[end:]
    # Legacy body remains outside the managed section until a human removes it.
    return section + ("\n\n<details><summary>Previous issue context</summary>\n\n"
                      + body + "\n</details>" if body else "")


def publish(repo, commit, version, run_url, current):
    issues = [issue for issue in pages(f"/repos/{repo}/issues?state=all&per_page=100")
              if "pull_request" not in issue and issue["title"] == TITLE
              and (any(label["name"] == "actions-security" for label in issue["labels"])
                   or (issue.get("user", {}).get("type") == "Bot"
                       and "Generated by the [zizmor SAST workflow]" in (issue.get("body") or "")))]
    open_issues = [issue for issue in issues if issue["state"] == "open"]
    canonical = max(open_issues or issues, key=lambda issue: (issue["updated_at"], issue["number"])) if issues else None
    prs = [pr for pr in pages(f"/repos/{repo}/pulls?state=open&per_page=100")
           if pr["title"] == "fix: zizmor auto-fix Actions security findings"]
    section = report(repo, commit, version, run_url, current, prs)
    if canonical is None:
        if current:
            gh("label", "create", "actions-security", "-R", repo, "--color", "e11d48", "--force")
            gh("issue", "create", "-R", repo, "--title", TITLE, "--label", "actions-security", "--body", section)
        return
    number = str(canonical["number"])
    body = canonical.get("body") or ""
    previous = state(body)
    delta = changes(previous, current)
    reopening = canonical["state"] == "closed" and bool(current)
    closing = canonical["state"] == "open" and not current
    reopened_event = None
    if closing:
        events = pages(f"/repos/{repo}/issues/{number}/events?per_page=100")
        reopened_event = max((event["id"] for event in events if event["event"] == "reopened"), default=0)
    notification_marker = None
    lines = []
    if reopening:
        lines += ["## Findings reported again", ""]
    if closing:
        lines += ["## No findings reported", "", "The latest successful audit reports no findings.", ""]
    for heading, items in delta.items():
        if items:
            lines += [f"### {heading}", ""] + [entry(repo, commit, item) for item in items] + [""]
    if reopening and not any(delta.values()):
        lines += [entry(repo, commit, item) for item in current.values()]
    if lines:
        # Retry identity excludes line movement and scan timestamp/version.
        transition = [hashlib.sha256(body.encode()).hexdigest(),
                      {key: {k: v for k, v in item.items() if k != "line"}
                                 for key, item in current.items()}, closing, reopening]
        marker = "<!-- scanning-service:zizmor-notification:" + hashlib.sha256(
            json.dumps(transition, sort_keys=True).encode()).hexdigest() + " -->"
        semantic = lambda items: {key: {k: v for k, v in item.items() if k != "line"}
                                  for key, item in items.items()}
        if previous is not None and semantic(previous) == semantic(current) and (closing or reopening):
            saved = re.search(re.escape(STATE) + r"([A-Za-z0-9+/=]+) -->", body)
            if saved:
                metadata = json.loads(base64.b64decode(saved[1]))
                if ((closing and metadata.get("reopened_event") == reopened_event)
                        or (reopening and metadata.get("closed_at") == canonical.get("closed_at"))):
                    marker = metadata.get("notification") or marker
        notification_marker = marker
        comments = pages(f"/repos/{repo}/issues/{number}/comments?per_page=100")
        if not any(marker in (comment.get("body") or "") for comment in comments):
            gh("issue", "comment", number, "-R", repo, "--body",
               "\n".join(lines) + "\n---\n\n" + footer(dt.datetime.now(dt.timezone.utc)) + "\n\n" + marker)
    section = report(repo, commit, version, run_url, current, prs, notification_marker,
                     canonical.get("closed_at") if reopening else None, reopened_event)
    gh("issue", "edit", number, "-R", repo, "--body", replace_report(body, section))
    if reopening:
        gh("issue", "reopen", number, "-R", repo)
    if closing:
        gh("issue", "close", number, "-R", repo, "--reason", "completed")


if __name__ == "__main__":
    try:
        raw_file, root, repo, commit, version, run_url = sys.argv[1:]
        publish(repo, commit, version, run_url, findings(json.loads(Path(raw_file).read_text()), Path(root)))
    except (ValueError, KeyError, StopIteration, subprocess.SubprocessError, OSError):
        print("zizmor issue update failed; prior report must not be treated as current", file=sys.stderr)
        sys.exit(1)
