# How we work

We both build with Claude Code. Claude follows `CLAUDE.md` (shared rules) and
`.claude/settings.json` (enforced permissions + hooks). This page is for us humans.

## Setup
1. Install [uv](https://docs.astral.sh/uv/) and the [GitHub CLI](https://cli.github.com/) (`gh auth login`).
2. `git clone https://github.com/Daniel-191/trading-bot.git && cd trading-bot`
3. `uv sync`
4. `cp .env.example .env` and fill in **your own** exchange keys (trading only, never withdrawals).

## The loop
1. **Create or pick an issue** and assign yourself — this is how we avoid building the same thing.
   Fill in "Scope" so we know which files you'll touch.
2. Tell Claude: *"implement issue #N"*. It will branch, build, test, and open a PR.
3. **The other person reviews.** Run `/code-review <PR#>` in Claude Code, read the summary,
   and approve or comment. Changes marked "Risk to live trading" need a careful human look.
4. **Squash and merge.** Branch is deleted automatically.
5. Pull `main` before starting the next thing.

## Working on the same area
- Agree on the interface first (write it in the issue), merge a small skeleton PR, then split the work.
- If you need someone's unmerged work, branch off their branch.
- Keep PRs small. Big long-lived branches = big conflicts.

## Rules
- Nothing goes to `main` without a PR + approval.
- `.env` is never committed and Claude is blocked from reading it.
- Default mode is `paper`. Going live is a deliberate decision we make together.
- Personal Claude preferences go in `CLAUDE.local.md` (gitignored), not `CLAUDE.md`.
