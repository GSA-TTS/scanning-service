"""Validate self-repository references without rewriting them for an old linter."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]


class SelfRepositoryTests(unittest.TestCase):
    def test_all_self_action_targets_exist_and_no_workspace_references_remain(self):
        references = []
        for path in (ROOT / ".github").rglob("*.yml"):
            for target in re.findall(r"^\s*uses: ([^\s]+)", path.read_text(), re.M):
                self.assertFalse(target.startswith("./"), f"{path}: {target}")
                if target.startswith("$/"):
                    self.assertNotIn("@", target)
                    relative = target[2:]
                    self.assertNotIn("..", Path(relative).parts)
                    destination = ROOT / relative
                    self.assertTrue(destination.is_file() or (destination / "action.yml").is_file(), target)
                    references.append(target)
        self.assertGreater(len(references), 10)

    def test_reusable_secret_scan_retains_caller_history_not_toolkit_checkout(self):
        text = (ROOT / ".github/workflows/secret-scan.yml").read_text()
        self.assertIn("fetch-depth: 0", text)
        self.assertIn("uses: $/.github/actions/secret-scan", text)
        self.assertNotIn("path: .scanning-service", text)

    def test_consumer_and_fixture_workspace_are_retained(self):
        oscal = (ROOT / ".github/workflows/oscal-update-consumers.yml").read_text()
        self.assertIn("repository: ${{ github.repository_owner }}/${{ matrix.consumer }}", oscal)
        self.assertNotIn("path: _scanning-service", oscal)
        fixture = (ROOT / ".github/workflows/secret-scan-test.yml").read_text()
        self.assertIn("path: .test-toolkit", fixture)
        self.assertIn('"$GITHUB_WORKSPACE" "$FIXTURE_KIND"', fixture)
        dependency = (ROOT / ".github/actions/dependency-check/action.yml").read_text()
        self.assertIn("uses: $/.github/actions/install-zizmor", dependency)
        self.assertNotIn("../install-zizmor", dependency)


if __name__ == "__main__":
    unittest.main()
