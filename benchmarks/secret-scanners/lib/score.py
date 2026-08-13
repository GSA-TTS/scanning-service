#!/usr/bin/env python3
"""Score normalized scanner output against the synthetic corpus.

Reads:
  --corpus DIR     corpus dir (files prefixed pos_/neg_ = ground truth). Optional;
                   omit for --target mode (unscored: findings + speed only).
  --results DIR    dir containing <scanner>.norm.json files
  --timing FILE    TSV: <scanner>\t<seconds> (one line per run)
  --meta FILE      TSV: <scanner>\t<validation>\t<config_interop>
  --out DIR        where to write latest.md / latest.json

Redaction: only file basenames, rule ids, and aggregate counts are ever read or
emitted. Secret values never reach this script.
"""
import argparse, json, os, glob, statistics, sys


def load_norm(path):
    try:
        with open(path) as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="")
    ap.add_argument("--results", required=True)
    ap.add_argument("--timing", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--target", default="")
    args = ap.parse_args()

    positives, negatives = set(), set()
    scored = bool(args.corpus)
    if scored:
        for name in os.listdir(args.corpus):
            if name.startswith("pos_"):
                positives.add(name)
            elif name.startswith("neg_"):
                negatives.add(name)

    timings = {}
    if os.path.exists(args.timing):
        for line in open(args.timing):
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2:
                timings.setdefault(parts[0], []).append(float(parts[1]))

    meta = {}
    if os.path.exists(args.meta):
        for line in open(args.meta):
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3:
                meta[parts[0]] = {"validation": parts[1], "config": parts[2]}

    rows = []
    for norm_path in sorted(glob.glob(os.path.join(args.results, "*.norm.json"))):
        scanner = os.path.basename(norm_path)[: -len(".norm.json")]
        findings = load_norm(norm_path)
        flagged = {f.get("file") for f in findings if f.get("file")}
        row = {
            "scanner": scanner,
            "raw_findings": len(findings),
            "median_seconds": round(statistics.median(timings.get(scanner, [0])), 3),
            "runs": len(timings.get(scanner, [])),
            "validation": meta.get(scanner, {}).get("validation", "?"),
            "config_interop": meta.get(scanner, {}).get("config", "?"),
        }
        if scored:
            tp = len(positives & flagged)
            fn = len(positives - flagged)
            fp = len(negatives & flagged)
            recall = tp / (tp + fn) if (tp + fn) else 0.0
            precision = tp / (tp + fp) if (tp + fp) else 1.0
            f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
            row.update(
                tp=tp, fn=fn, fp=fp,
                recall=round(recall, 3),
                precision=round(precision, 3),
                f1=round(f1, 3),
            )
        rows.append(row)

    os.makedirs(args.out, exist_ok=True)
    report = {
        "mode": "corpus" if scored else "target",
        "target": args.target or (args.corpus if scored else ""),
        "corpus": {"positives": len(positives), "negatives": len(negatives)} if scored else None,
        "scanners": rows,
    }
    with open(os.path.join(args.out, "latest.json"), "w") as fh:
        json.dump(report, fh, indent=2)

    # ── markdown ──
    md = ["# Secret Scanner Benchmark", ""]
    if scored:
        md.append(f"Corpus: **{len(positives)}** positives / **{len(negatives)}** negatives "
                  "(synthetic, redacted). Higher recall/precision/F1 is better; lower time is better.")
        md.append("")
        md.append("| Scanner | Recall | Precision | F1 | TP | FN | FP | Findings | Median s | Validation | Config interop |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rows, key=lambda x: (-x.get("f1", 0), x["median_seconds"])):
            md.append("| {scanner} | {recall} | {precision} | {f1} | {tp} | {fn} | {fp} | "
                      "{raw_findings} | {median_seconds} | {validation} | {config_interop} |".format(**r))
    else:
        md.append(f"Target: `{args.target}` (unscored — findings + speed only).")
        md.append("")
        md.append("| Scanner | Findings | Median s | Validation | Config interop |")
        md.append("|---|---|---|---|---|")
        for r in sorted(rows, key=lambda x: x["median_seconds"]):
            md.append("| {scanner} | {raw_findings} | {median_seconds} | "
                      "{validation} | {config_interop} |".format(**r))
    md += ["", "_Values are redacted: only file names, rule ids, and counts are recorded._", ""]
    md_text = "\n".join(md)
    with open(os.path.join(args.out, "latest.md"), "w") as fh:
        fh.write(md_text)
    print(md_text)


if __name__ == "__main__":
    sys.exit(main())
