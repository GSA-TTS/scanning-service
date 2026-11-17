"""Guard repository scope conversion and the reviewed App token profiles."""

from pathlib import Path
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).parents[1]


class TokenScopeTests(unittest.TestCase):
    def convert(self, value):
        return subprocess.run(
            ["bash", str(ROOT / ".github/actions/repo-list/token-repositories.sh"), "GSA-TTS"],
            input=json.dumps(value), text=True, capture_output=True, check=False)

    def test_valid_names_are_deduplicated_and_owner_is_removed(self):
        result = self.convert(["GSA-TTS/pic-team", "gsa-tts/scanning-service", "GSA-TTS/pic-team"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "pic-team,scanning-service")

    def test_invalid_scope_fails_instead_of_requesting_installation_wide_token(self):
        for value in ([], {}, [None], ["other/repo"], ["GSA-TTS/repo,another"],
                      ["GSA-TTS/repo/extra"], ["repo"], ["GSA-TTS/repo\n"]):
            with self.subTest(value=value):
                self.assertNotEqual(self.convert(value).returncode, 0)

    def test_workflow_requests_match_reviewed_permission_profiles(self):
        expected = {
            "gitleaks-audit": [{"contents": "read", "issues": "write"}],
            "monitoring": [{"contents": "read", "pull-requests": "read"}, {"contents": "read"}],
            "vulnerability-sla": [{"contents": "read", "vulnerability-alerts": "read", "issues": "write"}],
            "zizmor-sast": [{"contents": "write", "workflows": "write", "pull-requests": "write", "issues": "write"}],
            "oscal-update-consumers": [{"contents": "write", "pull-requests": "write"}],
            "renovate": [{"contents": "write", "workflows": "write", "issues": "write",
                          "pull-requests": "write", "statuses": "write",
                          "vulnerability-alerts": "read"}],
        }
        for workflow, profiles in expected.items():
            text = (ROOT / f".github/workflows/{workflow}.yml").read_text()
            requests = re.findall(
                r"      - name: Generate GitHub App token\n(.*?)(?=\n      - name:|\Z)", text, re.S)
            with self.subTest(workflow=workflow):
                self.assertEqual(len(requests), len(profiles))
                for request, profile in zip(requests, profiles):
                    actual = dict(re.findall(r"          permission-([\w-]+): (read|write)", request))
                    self.assertEqual(actual, profile)
                    scope = "matrix.consumer" if workflow == "oscal-update-consumers" else (
                        "steps.repos.outputs.token-repositories" if workflow == "renovate"
                        else "steps.repo-list.outputs.token-repositories")
                    self.assertIn("repositories: ${{ " + scope + " }}", request)
        matrix = (ROOT / ".github/workflows/oscal-update-consumers.yml").read_text()
        self.assertIn("- pic-blm-cxworks", matrix)
        self.assertNotIn("- GSA-TTS/pic-blm-cxworks", matrix)

    def test_metrics_count_configured_app_across_all_pages(self):
        text = (ROOT / ".github/workflows/monitoring.yml").read_text()
        self.assertIn("RENOVATE_APP_SLUG: ${{ steps.app-token.outputs.app-slug }}", text)
        match = re.search(r"\| jq --arg author .*?\n\s+'([^']+)'", text)
        self.assertIsNotNone(match)
        fixture = [[{"user": {"login": "custom-scanner[bot]"}, "head": {"ref": "renovate/one"}}],
                   [{"user": {"login": "renovate[bot]"}, "head": {"ref": "renovate/two"}},
                    {"user": {"login": "custom-scanner[bot]"}, "head": {"ref": "renovate/three"}},
                    {"user": {"login": "custom-scanner[bot]"}, "head": {"ref": "zizmor/fixes"}}]]
        result = subprocess.run(["jq", "--arg", "author", "custom-scanner[bot]", match[1]],
                                input=json.dumps(fixture), text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout.strip(), "2")


if __name__ == "__main__":
    unittest.main()
