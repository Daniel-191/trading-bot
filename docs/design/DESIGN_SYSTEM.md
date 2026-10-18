# Dashboard design system: "Obsidian & Champagne"

Every dashboard screen follows this file. It goes with:
- `docs/design/theme.css`: the tokens (colours, type, spacing) and base component classes.
  **Use them. Don't hardcode hex values or invent new classes for things listed here.**
- `docs/design/dashboard/`: the reference mockups. When unsure how something looks, copy the
  nearest existing screen. (The mockups predate `theme.css` and use some older class names;
  `theme.css` wins where they differ.)

If something you need isn't covered, add it to `theme.css` and this file in the same PR,
rather than styling it one-off on a page.

---

## 1. Principles

1. **Calm, dark, premium.** Near-black ground, one warm accent (champagne gold), lots of space.
   Colour is used for meaning, not decoration.
2. **Numbers first.** This is a tool for watching money. Figures are large, monospaced and aligned.
3. **Always know the mode.** The `PAPER` / `TESTNET` / `LIVE` badge is visible on every screen.
4. **Dangerous actions are hard to do by accident.** Danger styling plus a confirmation step.
5. **Nothing is shown by colour alone.** P&L has a sign, buy/sell has a label or a triangle, status has an icon or text.

---

## 2. Colour

Use the CSS variables. Hex values are listed for reference only.

| Role | Variable | Hex | Use for |
|---|---|---|---|
| Page | `--bg` | `#0A0C0F` | Page background, sidebar |
| Card | `--surface` | `#111418` | All cards and panels |
| Control | `--surface-raised` | `#151920` | Buttons |
| Sunken | `--surface-sunken` | `#0D1013` | Inputs, segmented controls, chart tooltips |
| Border | `--line` | `#1E232B` | Card borders, table header rule |
| Text | `--text` | `#ECE9E2` | Primary text, values |
| Secondary | `--text-muted` | `#8A919B` | Labels, captions |
| Faint | `--text-faint` | `#7D848E` | Axis labels, table headers. **The lightest grey allowed for text.** |
| Accent | `--accent` / `--accent-text` | `#B5873A` / `#D4AE6C` | Brand, our equity line, links, active nav, mode badge |
| Benchmark | `--series-2` | `#4F82E8` | Comparison lines (BTC hold), take-profit lines |
| Up | `--up` / `--up-text` | `#2FA77C` / `#4CC495` | Gains, buys, long, healthy |
| Down | `--down` / `--down-text` | `#E0604C` / `#EE7B68` | Losses, sells, stops, errors |
| Warning | `--warn` | `#D9A441` | Reconnects, nearing a limit |

Rules:
- **One accent.** Gold is the only brand colour. Don't add purples, teals or gradients.
- **`--up`/`--down` are for marks** (candles, bars, triangles). For text, use `.up`/`.down`
  (the lighter `-text` variants), and **always** add a sign: `+$18.24`, `−$4.12`, `▲ +1.84%`.
- **Status colours are reserved.** Never use green, red or amber as a plain series colour.
- **Neutral by default.** Risk meters are grey until ≥ 80% of a limit (`.meter--warn`), and red at the limit (`.meter--over`).
- **No new colours** without checking contrast (text ≥ 4.5:1 on `--surface`) and, for chart
  series, running the dataviz palette validator against `#111418`.

---

## 3. Typography

| Role | Font | Size | Notes |
|---|---|---|---|
| Page title | Instrument Serif | 48px (36px phone) | One per screen, `.serif` |
| Big statement | Instrument Serif | 28–40px | Rare: strategy signal ("Hold"), confirmation title |
| Card title | Geist 600 | 16px (15px phone) | `<h2>` |
| Body / table | Geist 400 | 13px | |
| Caption | Geist 400 | 12px | `.muted` |
| Eyebrow label | Geist 500 | 11px, uppercase, 0.14em tracking | `.eyebrow`, for KPI labels and section labels |
| **Every number** | Geist Mono | as context | `.num`: tabular figures so columns line up |

Never use Inter, Roboto or Arial. No font sizes outside this table.

### Number formatting
- Money: `$10,482.16` (2 dp, thousands separators). Signed P&L: `+$18.24` / `−$4.12`.
- Use the real minus sign `−` (U+2212), not a hyphen.
- Percentages: 2 dp for returns (`+0.65%`), 1 dp for limits and rates (`28.1%`).
- Prices: the exchange's tick precision (`67,412.50`, `154.32`). Quantities: the market's step size (`0.0120`).
- Times: 24-hour, UTC, `19:32:41` in tables and `19:32` in feeds. Dates: `18 Oct`, or `Today` / `Yesterday`.
- Values come from `Decimal` on the backend. Format them as strings server-side or with
  a fixed-precision formatter. Never do float arithmetic in the UI.

---

## 4. Layout and spacing

- **Desktop shell:** sidebar (232px) plus content (`.shell`). The content has 36px top padding and
  `clamp(16px, 3vw, 44px)` side padding. The sidebar stacks above the content on narrow screens.
- **Page structure, top to bottom:** header (eyebrow · serif title · mode badge · status and actions on the
  right) → KPI tiles (`.tiles`) → card rows (`.card-row` with `.wide` 2/3 + `.narrow` 1/3).
- **Spacing:** 14px between tiles, 18px between cards, 24px between sections, 22px card padding (16px on phone).
- **Radius:** 16px cards (18px phone), 10px controls, 6px chips.
- **Phone (≤ 480px):** single column, a 390-wide design, bottom tab bar (`.tab-item`) instead of the sidebar,
  wide tables become stacked row cards, 2-column KPI grid. No fake status bar.
- Wide tables always sit inside `.table-scroll`.
- The only decorative effect is `.page-glow` on `<main>`. No other gradients, glows or textures.

---

## 5. Components

Use these classes from `theme.css`.

| Component | Class | Rules |
|---|---|---|
| Card | `.card` | Every panel. Optional `.card--feature` (gold border) on **one** card per page. |
| Button | `.btn` | Default action. Min 44px tall. Use `.btn--sm` only for row actions in desktop tables. |
| Danger button | `.btn--danger` | Flatten, Kill, Cancel all. **Must open a confirmation.** |
| Confirm button | `.btn--danger-solid` | Only inside a confirmation dialog or sheet. |
| Segmented control | `.seg` | Time ranges, timeframes, pair switchers, tabs. Mark the active one with `aria-pressed`/`aria-selected`. |
| Switch | `.switch` | On/off settings (pause entries). `role="switch"` + `aria-checked`. |
| Chip | `.chip--buy` / `.chip--sell` | `BUY`, `SELL`, `LONG`, `SHORT`. Uppercase text. |
| Mode badge | `.chip--mode` | `PAPER` / `TESTNET` / `LIVE`. On every screen: header and sidebar. |
| Status dot | `.status-dot` (+ `--live`, `--warn`, `--down`) | Always next to a text label ("Running", "Streaming"). |
| Table | `table.t` | Header in `.eyebrow` style, numbers right-aligned (`.r`) and `.num`, hover row highlight. |
| Meter | `.meter` | Risk usage. Show `used / limit` as text next to it. |
| Field | `.field` | A `<label for>` plus an input/select. Never a placeholder used as the label. |
| Nav | `.nav-item` / `.tab-item` | Mark the current page with `aria-current="page"`. |
| KPI tile | `.card` + `.eyebrow` + `.num` value (30px) + a caption line | Max 5 per row. Each must answer a question you'd actually ask. |
| Event row | icon (16px stroke) · title · muted detail · time | Icons: tick = ok, triangle = warning, shield = risk, person = control action, circle-i = info. |

### Icons
Inline stroke SVGs, 1.6px stroke (2px at 16px and below), `currentColor`, `aria-hidden="true"`.
No emoji, and no icon fonts. An icon-only button needs an `aria-label`.

### Dangerous actions
1. The button uses `.btn--danger`, with a label ending in `…` ("Flatten all…").
2. Clicking it opens a confirmation (inline `role="alertdialog"` on desktop, bottom sheet on phone) that states **exactly** what will happen
   ("Cancels 2 open orders and closes 3 positions at market").
3. The confirm button uses `.btn--danger-solid` and has a verb label ("Flatten now"). The Cancel button sits beside it.
4. The action goes through the `Control` interface and is written to the audit log.

---

## 6. Charts

| Rule | Detail |
|---|---|
| Series colours | Our bot = `--accent`, benchmark = `--series-2`. Add a third series only after running the palette validator. |
| Lines | 2px for the main series, 1.5px for the benchmark, round joins. Area fill at most 8% opacity of the line colour. |
| Candles | Up = hollow with an `--up` outline, down = solid `--down`. (The fill difference helps colour-blind readers.) |
| Our trades | Buy = `--up` triangle pointing up, below the candle. Sell = `--down` triangle pointing down, above it. 2px `--surface` ring. |
| Price lines | Dashed 5/4: entry = accent, take-profit = `--series-2`, stop = `--down`. Each gets a tag on the right axis. Last price = solid faint line with a light tag. |
| Bars | Rounded 3–4px on the end away from zero, a 2px gap between bars. Diverging around a visible zero line. |
| Axes and grid | Gridlines `--grid`, baseline `--baseline`, labels `--text-faint` 11px mono. Keep 5–6 gridlines at most. |
| Legend | Above the chart, left, as a short line plus label. Required for 2+ series. |
| Hover | Every chart gets a crosshair and tooltip (`--surface-sunken`, 10px radius, values in mono). |
| Never | Dual y-axes, pie charts for P&L, 3D, rainbow palettes, a value label on every point. |

---

## 7. Copy and tone

- Short, plain and specific: "Pause new entries", not "Toggle trading state".
- Sentence case everywhere except eyebrow labels and chips.
- Say what an action does and what it keeps: "Stops opening positions. Open positions keep working."
- No exclamation marks, emoji or marketing language.
- Empty states say what will appear and when: "No open positions. New entries appear here when the strategy signals."

---

## 8. Accessibility (non-negotiable)

- Use real `<button>`, `<a href>`, `<input>` + `<label>` elements. Never a clickable `<div>`.
- Touch targets ≥ 44px (the exception is `.btn--sm` in desktop tables).
- Text contrast ≥ 4.5:1. Nothing lighter than `--text-faint` for text.
- Visible focus ring (already set in `theme.css`). Don't remove outlines.
- Charts get `role="img"` and an `aria-label` that states the takeaway, plus a table view where the data matters.

---

## 9. Checklist for a new screen or component

- [ ] Uses `theme.css` variables and classes, with no new hex values or one-off styles
- [ ] Mode badge visible
- [ ] Serif page title, `.eyebrow` labels, `.num` on every number
- [ ] P&L signed and coloured with `.up`/`.down`, never colour alone
- [ ] Dangerous actions have danger styling and a confirmation
- [ ] Works at phone width (stacks, tables scroll or become cards)
- [ ] Touch targets ≥ 44px, real form and button elements, focus visible
- [ ] Charts follow section 6: legend, hover, no dual axis
- [ ] Anything new was added to `theme.css` and this file in the same PR
