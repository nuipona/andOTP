"""Guard the automated gates and manual review workflow the repository documents."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"


class ContinuousIntegrationWorkflowTest(unittest.TestCase):
    def test_android_ci_runs_all_documented_gate_categories(self):
        source = (WORKFLOWS / "android-ci.yml").read_text()
        for marker in (
            "  push:",
            "  pull_request:",
            "  workflow_dispatch:",
            "  source-checks:",
            "  android-build:",
            "  reproducibility:",
            "  instrumentation:",
            "python3 -m unittest discover -s scripts/tests -v",
            "scripts/check_build_inputs.py",
            "--no-daemon --stacktrace",
            ":app:test${{ matrix.flavor }}DebugUnitTest",
            ":app:lint${{ matrix.flavor }}Release",
            "scripts/verify_reproducible_build.sh",
            "scripts/ci_emulator_tests.sh",
            "scripts/check_manifest.py",
            "max-parallel: 2",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)
        for api in (28, 36):
            self.assertIn(f"api-level: {api}", source)
        self.assertIn("flavor: [Fdroid, Play]", source)
        self.assertIn(":app:test${{ matrix.flavor }}DebugUnitTest", source)
        self.assertIn(":app:lint${{ matrix.flavor }}Release", source)

    def test_dependency_baseline_is_manual_read_only_and_reviewable(self):
        source = (WORKFLOWS / "dependency-baseline.yml").read_text()
        self.assertIn("on:\n  workflow_dispatch:", source)
        self.assertIn("permissions:\n  contents: read", source)
        self.assertIn("--write-verification-metadata sha256", source)
        self.assertIn("build/reports/dependency-inventory.txt", source)
        self.assertIn("actions/upload-artifact@", source)
        self.assertNotIn("--write-locks", source)
        self.assertNotIn("git push", source)

    def test_emulator_diagnostics_are_not_accidentally_committed(self):
        ignore = (ROOT / ".gitignore").read_text()
        for filename in ("/gradle-install.log", "/gradle-connected.log", "/mem-emulator.log"):
            self.assertIn(filename, ignore)

    def test_emulator_script_rejects_bad_or_missing_flavors_before_work(self):
        script = ROOT / "scripts/ci_emulator_tests.sh"
        for arguments in ([], ["Tasker"], ["Fdroid", "Play"]):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    ["bash", str(script), *arguments],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()
