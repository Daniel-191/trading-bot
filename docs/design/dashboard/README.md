# Dashboard design

Design mockups for the dashboard (roadmap phase 5, `docs/PLAN.md` §5).
Live canvas: https://claude.ai/artifact/Uh6z5kddKs8C37rjgWk1jD (private until shared).

These files are the canvas source (`.dc.html` design components plus `canvas.json`).
They load a `support.js` runtime that only exists inside the canvas, so they won't render
when opened directly. Treat them as a reference for layout, content and styling, not as
code to ship. **All numbers in them are sample data.**

## Screens

| File | Screen |
|---|---|
| `Main.dc.html` | Overview: status, headline numbers, equity curve vs BTC hold, live trades, positions/orders, risk limits, daily P&L, events |
| `Trades.dc.html` | Live trading: candles with our fills, entry/TP/stop lines, order book, open orders, strategy signal, today's fills |
| `History.dc.html` | Trade history: filters, CSV export, summary stats, paginated closed-trade table |
| `Risk.dc.html` | Risk & system: pause/flatten/kill with confirmation, risk limits, system health, event & audit log |
| `Mobile-*.dc.html` | Phone versions (390×844) of the same four areas, with a bottom tab bar |

The rules for building new screens are in `../DESIGN_SYSTEM.md`, and the tokens are in
`../theme.css`. Those files are authoritative; the table below is a summary.

## Design tokens ("Obsidian & Champagne")

| Token | Value | Use |
|---|---|---|
| Background | `#0A0C0F` | Page |
| Surface | `#111418` | Cards |
| Border | `#1E232B` | Card and table lines |
| Text | `#ECE9E2` / `#8A919B` | Primary / secondary |
| Accent | `#B5873A` (text `#D4AE6C`) | Brand, equity line, mode badge |
| Benchmark | `#4F82E8` | BTC buy & hold line, take-profit |
| Up / down marks | `#2FA77C` / `#E0604C` | Candles, bars, buy/sell markers |
| Up / down text | `#4CC495` / `#EE7B68` | P&L figures (always with a +/− sign) |
| Warning | `#D9A441` | Reconnects and other warnings |

Fonts (Google Fonts): Instrument Serif for page titles, Geist for UI, Geist Mono with
tabular figures for every number.

The chart palette was checked with a colour-vision validator against the dark surface.
Gold/blue pass every check. Up/down green/red is borderline for deuteranopia, so P&L is
never shown by colour alone: signs, arrows and up/down triangles carry it too.

## Notes for building it

- The mode badge (paper/testnet/live) is visible on every screen.
- Controls go through the same `Control` interface as Telegram and are written to the audit log.
  Flatten and Kill need a confirmation step.
- Risk limits are read-only in the UI. The design shows three env vars not yet in `PLAN.md`:
  `RISK_MAX_DRAWDOWN_PCT`, `RISK_MAX_EXPOSURE_PCT`, `RISK_MAX_ORDERS_PER_MIN`.
- The dashboard cannot change trading mode or API keys.
