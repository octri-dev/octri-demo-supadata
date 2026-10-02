"""Run every included SDK's checks; only local mocks contact HTTP endpoints."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ["baseline", "apiroad"] if ROOT.name.endswith("scrapeninja") else ["generated"]
ENV = os.environ.copy()
ENV["VIRTUAL_ENV"] = sys.prefix
RESULTS = []


def run(label, command, cwd):
    result = subprocess.run(command, cwd=cwd, env=ENV, text=True, capture_output=True)
    print(f"{label}: {'PASS' if result.returncode == 0 else 'FAIL'}", flush=True)
    if result.returncode:
        print(result.stdout + result.stderr)
    RESULTS.append({"check": label, "exit_code": result.returncode})
    return result.returncode == 0


with tempfile.TemporaryDirectory(prefix="octri-demo-validation-") as package_dir:
    for variant in VARIANTS:
        for language in ["python", "typescript"]:
            cwd = ROOT / "sdks" / variant / language
            prefix = variant + "/" + language
            if language == "python":
                commands = [
                    ("tests", ["sh", "scripts/test"]),
                    ("lint", [sys.executable, "-m", "ruff", "check", "src", "tests"]),
                    ("format", [sys.executable, "-m", "ruff", "format", "--check", "src", "tests"]),
                    ("types", [sys.executable, "-m", "mypy", "src"]),
                    ("package", [sys.executable, "-m", "build", "--wheel", "--outdir", package_dir]),
                ]
            else:
                if not run(prefix + "/install", ["npm", "ci", "--ignore-scripts"], cwd):
                    continue
                commands = [
                    ("tests", ["sh", "scripts/test"]),
                    ("lint", ["npm", "run", "lint"]),
                    ("format", ["npm", "run", "format"]),
                    ("types", ["npm", "run", "typecheck"]),
                    ("package", ["npm", "pack", "--dry-run"]),
                ]
            for label, command in commands:
                run(prefix + "/" + label, command, cwd)
    run("root/install", ["npm", "ci", "--ignore-scripts"], ROOT)
    run("demo/python", [sys.executable, "demos/check-python.py"], ROOT)
    run("demo/typescript", ["npm", "run", "check:typescript"], ROOT)
print(json.dumps(RESULTS, indent=2))
raise SystemExit(1 if any(result["exit_code"] for result in RESULTS) else 0)
