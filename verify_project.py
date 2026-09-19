"""Save real validation output; stop when a required check fails."""

import json
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
import requests
from EmotionDetection.emotion_detection import emotion_detector, URL, HEADERS

EVIDENCE = Path("evidence")
EVIDENCE.mkdir(exist_ok=True)


def record_prediction(filename, text, expected):
    result = emotion_detector(text)
    assert result["dominant_emotion"] == expected, result
    report = f"Input: {text}\n" + json.dumps(result, indent=2) + "\n"
    (EVIDENCE / filename).write_text(report, encoding="utf-8")
    print(filename, "PASS", result["dominant_emotion"])


def run_check(filename, arguments):
    result = subprocess.run([sys.executable, *arguments], capture_output=True, text=True, check=False)
    report = "$ python3 " + " ".join(arguments) + "\n" + result.stdout + result.stderr
    (EVIDENCE / filename).write_text(report, encoding="utf-8")
    print(filename, "PASS" if result.returncode == 0 else "FAIL")
    print((result.stdout + result.stderr)[-900:])
    if result.returncode:
        raise SystemExit(result.returncode)


record_prediction("3b_formatted_output_test.txt", "I am so happy I am doing this.", "joy")
record_prediction("4b_packaging_test.txt", "I hate working long hours.", "anger")
blank_response = requests.post(URL, json={"raw_document": {"text": ""}}, headers=HEADERS, timeout=30)
blank_result = emotion_detector("")
assert blank_response.status_code == 400, blank_response.status_code
assert all(value is None for value in blank_result.values()), blank_result
(EVIDENCE / "7d_blank_input_service_test.txt").write_text(
    f"Watson HTTP status: {blank_response.status_code}\n" + json.dumps(blank_result, indent=2),
    encoding="utf-8",
)
print("Live blank-input check PASS (Watson HTTP 400)")
run_check("5b_unit_testing_result.txt", ["-m", "unittest", "test_emotion_detection", "-v"])
run_check("error_handling_tests.txt", ["-m", "unittest", "test_error_handling", "-v"])
run_check("8b_static_code_analysis.txt", ["-m", "pylint", "server.py"])
versions = {name: version(name) for name in ("requests", "Flask", "pylint")}
(EVIDENCE / "environment.json").write_text(json.dumps(versions, indent=2), encoding="utf-8")
print("ALL VALIDATION CHECKS PASSED")
