"""PreToolUse hook: block commits/pushes to main and plain force-pushes.

Exit code 2 blocks the tool call and shows stderr to Claude.
"""

import json
import re
import subprocess
import sys

PROTECTED = {"main", "master"}


def current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
    )
    return result.stdout.strip()


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\b", command):
        return

    if re.search(r"git\s+push\b.*\s(--force|-f)(\s|$)", command):
        block("Plain force-push is blocked. Use `git push --force-with-lease` on your own branch.")

    if re.search(r"git\s+push\b.*[\s:](main|master)(\s|$)", command):
        block("Pushing to main is blocked. Push your feature branch and open a PR.")

    creates_branch = re.search(r"git\s+(checkout\s+-b|switch\s+-c)\s", command)
    commits = re.search(r"git\s+(commit|push)\b", command)
    if commits and not creates_branch and current_branch() in PROTECTED:
        block(
            "You are on main. Create a branch first, e.g. `git checkout -b feat/<name>`, "
            "then commit there and open a PR."
        )


if __name__ == "__main__":
    main()
