#!/usr/bin/env bash
# Runs the emulator steps of android-ci.yml for one flavor. Usage: ci_emulator_tests.sh <Fdroid|Play>
#
# android-emulator-runner runs every line of its `script` input in a separate shell, so exit codes
# and background processes cannot be shared between lines. Keeping the steps in one script file
# makes the exit codes and the memory sampler reliable.
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: ci_emulator_tests.sh <Fdroid|Play>" >&2
    exit 2
fi
flavor="$1"
case "$flavor" in
    Fdroid|Play) ;;
    *)
        echo "unsupported flavor '$flavor' (expected Fdroid or Play)" >&2
        echo "usage: ci_emulator_tests.sh <Fdroid|Play>" >&2
        exit 2
        ;;
esac

(while true; do echo "$(date +%T) $(free -m | awk '/Mem:/{print "used=" $3 "MB"}')"; sleep 5; done) > mem-emulator.log 2>&1 &
sampler=$!
trap 'kill "$sampler" 2>/dev/null || true' EXIT

# run_logged <log> <gradle task>: writes the Gradle output and its exit code to <log>, then fails
# the script with that exit code when Gradle failed.
run_logged() {
    local log="$1"
    shift
    local rc=0
    ./gradlew --no-daemon "$@" > "$log" 2>&1 || rc=$?
    echo "gradle exit code: $rc" >> "$log"
    if (( rc != 0 )); then
        echo "::group::Gradle failure details ($log)"
        tail -n 100 "$log"
        echo "::endgroup::"
        python3 - "$log" <<'PY'
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

log = Path(sys.argv[1])
lines = log.read_text(errors="replace").splitlines()
pattern = re.compile(r"FAILED|FAILURE:|What went wrong|Execution failed|Caused by:|Exception|Error:|AssertionError|Tests run:", re.I)
selected = [line for line in lines if pattern.search(line)][-20:]
if not selected:
    selected = lines[-20:]
for line in selected:
    escaped = line[:2000].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::error title=Connected Gradle test failure::{escaped}")

results = Path("app/build/outputs/androidTest-results/connected")
if results.exists():
    for report in sorted(results.rglob("TEST-*.xml")):
        try:
            root = ElementTree.parse(report).getroot()
        except ElementTree.ParseError as error:
            print(f"::error title=Malformed Android test report::{report}: {error}")
            continue
        for case in root.iter("testcase"):
            for kind in ("failure", "error"):
                failure = case.find(kind)
                if failure is not None:
                    message = " ".join((failure.get("message", ""), failure.text or "")).strip()
                    summary = f"{case.get('classname', '')}.{case.get('name', '')}: {message}"
                    escaped = summary[:4000].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                    print(f"::error title=Android instrumentation {kind}::{escaped}")
PY
    fi
    return "$rc"
}

run_logged gradle-install.log :security-test-client:installDebug
run_logged gradle-connected.log ":app:connected${flavor}DebugAndroidTest"
