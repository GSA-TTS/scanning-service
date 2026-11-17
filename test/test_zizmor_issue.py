"""Current-report, semantic comparison, and retry notification regressions."""
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("issue", Path(__file__).parents[1] / ".github/scripts/zizmor_issue.py")
issue = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(issue)
ITEM = {"rule": "github-app", "path": ".github/workflows/test.yml", "line": 10,
        "severity": "Low", "fixes": ["unsafe"]}
REPO = "example/repo"


class IssueTests(unittest.TestCase):
    def body(self, current):
        return issue.report(REPO, "abc", "1.32.0", "https://example.invalid/run", current, [])

    def test_line_changes_do_not_notify_but_additions_escalations_removals_do(self):
        self.assertFalse(any(issue.changes({"a": ITEM}, {"a": dict(ITEM, line=99)}).values()))
        self.assertEqual(issue.changes({}, {"a": ITEM})["New findings"], [ITEM])
        self.assertEqual(len(issue.changes({"a": ITEM}, {"a": dict(ITEM, severity="High")})["Severity increased"]), 1)
        self.assertEqual(issue.changes({"a": ITEM}, {})["No longer reported"], [ITEM])
        self.assertEqual(issue.changes(None, {"a": ITEM}), {})

    def test_managed_body_preserves_human_context_and_legacy_text(self):
        current = self.body({"a": ITEM})
        self.assertEqual(issue.state(current), {"a": ITEM})
        replaced = issue.replace_report("human prefix\n" + current + "\nhuman suffix", self.body({}))
        self.assertTrue(replaced.startswith("human prefix"))
        self.assertTrue(replaced.endswith("human suffix"))
        self.assertIn("human legacy", issue.replace_report("human legacy", current))
        with self.assertRaises(ValueError):
            issue.replace_report(issue.START, current)

    def test_named_step_identity_survives_index_and_line_movement(self):
        def raw(index, row):
            route = [{"Key": "jobs"}, {"Key": "test"}, {"Key": "steps"}, {"Index": index}]
            return [{"ignored": False, "ident": "github-app", "determinations": {"severity": "Low"},
                     "fixes": [{"disposition": "unsafe"}], "locations": [
                         {"symbolic": {"kind": "Hidden", "route": {"route": route}},
                          "concrete": {"feature": "run: echo test\n        name: Token\n        id: token\n          id: shell-content\n",
                                       "location": {"start_point": {"column": 8}}}},
                         {"symbolic": {"kind": "Primary", "route": {"route": route + [{"Key": "with"}]},
                                       "key": {"Local": {"verbatim_path": "/tmp/repo/.github/workflows/test.yml"}},
                                       "feature_kind": "Normal"},
                          "concrete": {"location": {"start_point": {"row": row}}}}]}]
        self.assertEqual(set(issue.findings(raw(0, 10), Path("/tmp/repo"))),
                         set(issue.findings(raw(4, 50), Path("/tmp/repo"))))
        self.assertEqual(len(issue.findings(raw(0, 10) * 2, Path("/tmp/repo"))), 2)

    @patch.object(issue, "gh")
    @patch.object(issue, "pages")
    def test_existing_legacy_issue_gets_quiet_baseline(self, pages, gh):
        pages.side_effect = [[{"number": 32, "title": issue.TITLE, "state": "open",
                               "labels": [{"name": "actions-security"}], "updated_at": "today",
                               "body": "legacy"}], []]
        issue.publish(REPO, "abc", "1.32.0", "run", {"a": ITEM})
        self.assertEqual(gh.call_args.args[1], "edit")
        self.assertEqual(gh.call_count, 1)

    @patch.object(issue, "gh")
    @patch.object(issue, "pages")
    def test_notification_precedes_edit_and_failure_preserves_baseline(self, pages, gh):
        canonical = {"number": 32, "title": issue.TITLE, "state": "open",
                     "labels": [{"name": "actions-security"}], "updated_at": "today", "body": self.body({})}
        pages.side_effect = [[canonical], [], []]
        gh.side_effect = subprocess.CalledProcessError(1, "gh")
        with self.assertRaises(subprocess.CalledProcessError):
            issue.publish(REPO, "abc", "1.32.0", "run", {"a": ITEM})
        self.assertEqual(gh.call_args.args[1], "comment")
        gh.reset_mock(); gh.side_effect = None
        pages.side_effect = [[canonical], [], []]
        issue.publish(REPO, "abc", "1.32.0", "run", {"a": ITEM})
        self.assertEqual([call.args[1] for call in gh.call_args_list], ["comment", "edit"])
        comment = gh.call_args_list[0].args[-1]
        gh.reset_mock()
        pages.side_effect = [[canonical], [], [{"body": comment}]]
        issue.publish(REPO, "different-commit", "1.33.0", "different-run", {"a": dict(ITEM, line=99)})
        self.assertEqual([call.args[1] for call in gh.call_args_list], ["edit"])

    @patch.object(issue, "gh")
    @patch.object(issue, "pages")
    def test_clean_closes_and_returning_findings_reopen(self, pages, gh):
        canonical = {"number": 32, "title": issue.TITLE, "state": "open",
                     "labels": [{"name": "actions-security"}], "updated_at": "today", "body": self.body({"a": ITEM})}
        pages.side_effect = [[canonical], [], [], []]
        issue.publish(REPO, "abc", "1.32.0", "run", {})
        self.assertEqual([call.args[1] for call in gh.call_args_list], ["comment", "edit", "close"])
        gh.reset_mock()
        canonical.update(state="closed", body=self.body({}))
        pages.side_effect = [[canonical], [], []]
        issue.publish(REPO, "abc", "1.32.0", "run", {"a": ITEM})
        self.assertEqual([call.args[1] for call in gh.call_args_list], ["comment", "edit", "reopen"])

    @patch.object(issue, "gh")
    @patch.object(issue, "pages")
    def test_state_change_failure_reuses_published_notification(self, pages, gh):
        for closing in (True, False):
            canonical = {"number": 32, "title": issue.TITLE,
                         "state": "open" if closing else "closed",
                         "closed_at": "2026-11-01T00:00:00Z" if not closing else None,
                         "labels": [{"name": "actions-security"}], "updated_at": "today",
                         "body": self.body({"a": ITEM} if closing else {})}
            current = {} if closing else {"a": ITEM}
            pages.side_effect = [[canonical], [], [], []] if closing else [[canonical], [], []]
            gh.side_effect = ["", "", subprocess.CalledProcessError(1, "gh")]
            with self.assertRaises(subprocess.CalledProcessError):
                issue.publish(REPO, "abc", "1.32.0", "run", current)
            comment = gh.call_args_list[-3].args[-1]
            canonical["body"] = gh.call_args_list[-2].args[-1]
            gh.reset_mock(); gh.side_effect = None
            pages.side_effect = ([[canonical], [], [], [{"body": comment}]] if closing
                                 else [[canonical], [], [{"body": comment}]])
            retry = {} if closing else {"a": dict(ITEM, line=99)}
            issue.publish(REPO, "abc", "1.32.0", "retry", retry)
            self.assertNotIn("comment", [call.args[1] for call in gh.call_args_list])
            gh.reset_mock()
            if not closing:
                canonical["body"] = issue.report(REPO, "abc", "1.32.0", "retry", retry, [],
                                                   issue.state(canonical["body"]) and "old-marker",
                                                   canonical["closed_at"])
                canonical["closed_at"] = "2026-11-02T00:00:00Z"
                pages.side_effect = [[canonical], [], [{"body": comment}]]
                issue.publish(REPO, "abc", "1.32.0", "new-close", retry)
                self.assertIn("comment", [call.args[1] for call in gh.call_args_list])
                gh.reset_mock()


if __name__ == "__main__":
    unittest.main()
