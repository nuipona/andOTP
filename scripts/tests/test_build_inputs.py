import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_build_inputs", ROOT / "scripts/check_build_inputs.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
WORKFLOW_DIR = ROOT / ".github/workflows"
WORKFLOWS = sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))


class BuildInputsTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in [*checker.HASHES, "gradle/wrapper/gradle-wrapper.properties"]:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / name).read_bytes())
        for source in WORKFLOWS:
            destination = self.root / ".github/workflows" / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())

    def test_official_wrapper_and_every_workflow_pass(self):
        self.assertTrue(WORKFLOWS, "The build-input gate must cover at least one workflow")
        self.assertEqual({item.name for item in WORKFLOWS},
                         {item.name for item in (self.root / ".github/workflows").iterdir()})
        self.assertEqual([], checker.check(self.root))

    def test_workflow_checkouts_do_not_persist_credentials(self):
        for workflow in (self.root / ".github/workflows").iterdir():
            lines = workflow.read_text().splitlines()
            checkout_lines = [index for index, line in enumerate(lines) if "uses: actions/checkout@" in line]
            for index in checkout_lines:
                with self.subTest(workflow=workflow.name, line=index):
                    self.assertIn("persist-credentials: false", "\\n".join(lines[index:index + 4]))

    def test_modified_wrapper_is_rejected(self):
        path = self.root / "gradle/wrapper/gradle-wrapper.jar"
        path.write_bytes(path.read_bytes() + b"tampered")
        self.assertTrue(any("provenance" in error for error in checker.check(self.root)))

    def test_missing_or_duplicate_distribution_checksum_is_rejected(self):
        path = self.root / "gradle/wrapper/gradle-wrapper.properties"
        original = path.read_text()
        path.write_text("\n".join(line for line in original.splitlines() if not line.startswith("distributionSha256Sum=")))
        self.assertTrue(checker.check(self.root))
        path.write_text(original + "distributionSha256Sum=" + checker.DISTRIBUTION_HASH + "\n")
        self.assertTrue(any("Duplicate" in error for error in checker.check(self.root)))

    def test_changed_distribution_url_is_rejected(self):
        path = self.root / "gradle/wrapper/gradle-wrapper.properties"
        path.write_text(path.read_text().replace("gradle-8.13-all.zip", "gradle-8.14-all.zip"))
        self.assertTrue(checker.check(self.root))

    def test_mutable_action_tag_is_rejected_in_any_workflow(self):
        path = self.root / ".github/workflows/build-fdroid-debug-apk.yml"
        original = path.read_text()
        self.assertIn("actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683", original)
        path.write_text(original.replace(
            "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
            "actions/checkout@v4", 1))
        self.assertTrue(any("Unpinned" in error and path.name in error for error in checker.check(self.root)))

    def test_missing_wrapper_properties_and_workflows_are_reported(self):
        (self.root / "gradle/wrapper/gradle-wrapper.properties").unlink()
        workflows = self.root / ".github/workflows"
        for path in workflows.iterdir():
            path.unlink()
        errors = checker.check(self.root)
        self.assertTrue(any("Cannot inspect gradle/wrapper/gradle-wrapper.properties" in error for error in errors))
        self.assertTrue(any("No GitHub Actions workflows found" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
