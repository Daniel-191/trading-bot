"""PostToolUse hook: auto-format and lint-fix any Python file Claude edits.

Keeps formatting identical across both developers so it never causes merge conflicts.
"""

import json
import subprocess
import sys

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
if path.endswith(".py"):
    subprocess.run([sys.executable, "-m", "ruff", "format", "--quiet", path])
    subprocess.run([sys.executable, "-m", "ruff", "check", "--fix", "--quiet", path])
