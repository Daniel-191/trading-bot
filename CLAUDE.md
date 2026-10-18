# Trading Bot — Shared Claude Instructions

Two people work on this repo, each using Claude Code. You (Claude) are not the only one
making changes. This file is the shared source of truth — follow it exactly.

## Git workflow (mandatory)
- NEVER commit or push to `main`. A hook will block you if you try.
- Before starting work: `git checkout main && git pull`, then create a branch:
  `feat/<short-name>`, `fix/<short-name>`, `refactor/<short-name>`, `chore/<short-name>`, `docs/<short-name>`.
- Work should map to a GitHub issue. If the user references an issue, read it first
  (`gh issue view <n>`) and stay within its scope. Put `Closes #<n>` in the PR body.
- Keep PRs small and focused — one concern per PR. If scope grows, stop and suggest splitting.
- Before pushing: `git fetch origin && git rebase origin/main`, then run the checks below.
- After rebasing an already-pushed branch use `git push --force-with-lease` (plain `--force` is blocked).
- Open PRs with `gh pr create`, filling in the PR template. Never merge PRs yourself
  unless the user explicitly asks.
- When resolving merge conflicts, explain to the user what each side did and what you kept.
  The other side is the other developer's work — don't silently discard it.

## Checks (must pass before every push)
```
uv run ruff format .
uv run ruff check --fix .
uv run pytest
```
CI runs the same checks on every PR.

## Code conventions
- Python 3.13, dependencies managed with `uv` (`uv add <pkg>`, `uv add --dev <pkg>`).
  Never use pip directly. Commit `uv.lock` changes.
- Source in `src/trading_bot/`, tests in `tests/` mirroring the source layout.
- Every behavior change comes with tests. Tests must never hit real exchanges or need real keys —
  mock the exchange or use recorded data.
- Type hints on all public functions. Use `decimal.Decimal` (not float) for prices, quantities and money.
- Prefer extending existing modules/interfaces over creating parallel ones. If you think an
  interface needs changing, say so and explain the impact — the other developer depends on it.

## Safety rules (non-negotiable)
- Never read, print, or edit `.env`. Config comes from environment variables; `.env.example` documents them.
- Never hardcode API keys, secrets, or account IDs anywhere.
- `TRADING_MODE` defaults to `paper`. Never change a default to `live`, and never run anything in live mode.
- Any change touching order placement, position sizing, or risk limits must be called out
  explicitly in the PR description under "Risk to live trading".

## Dashboard design system (mandatory for any UI work)
- Before building or changing any dashboard screen or component, read
  `docs/design/DESIGN_SYSTEM.md` and follow it.
- Style with the variables and classes in `docs/design/theme.css`. Don't hardcode colours,
  fonts or spacing, or restyle an existing component one-off.
- Match the reference mockups in `docs/design/dashboard/` (desktop and mobile).
- If you need something the design system doesn't cover, add it to `theme.css` and
  `DESIGN_SYSTEM.md` in the same PR and mention it in the PR description.
- Run the checklist at the end of `DESIGN_SYSTEM.md` before opening a UI PR.

## Architecture
_(Not built yet. As modules and interfaces are decided, document them here in the same PR
that introduces them, so the other developer's Claude knows about them.)_

## Decisions log
_(Record important design decisions here with a one-line rationale.)_
