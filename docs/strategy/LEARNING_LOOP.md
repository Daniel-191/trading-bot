# Learning from our trades without fooling ourselves

The bot can improve over time, and Claude can do much of that work. It can't do it by looking at recent trades and adjusting the strategy, though. The daily trend strategy recommended in [`STRATEGY_OPTIONS.md`](STRATEGY_OPTIONS.md) opens only **2–5 positions a year**. That is far too little feedback to learn *when to be in the market*.

We tested this directly. On BTC data from 2016 to May 2025, we tried **15 ways for a trend bot to learn from its own results**, walk-forward, against simply running fixed rules. **None was reliably better. Twelve did worse.** The ones that learned hardest did worst, and an ML filter was the worst of all. Even a genuine improvement of the size we saw would need **13–20 years** of live trading to confirm.

What the bot *can* learn quickly are the parts with dense feedback: **costs and execution, volatility estimates, and operational mistakes**, each with hundreds of observations a year. In the same test, a better volatility estimator proved itself statistically within **two years** of data.

So we propose keeping the strategy fixed from day to day and wrapping it in three learning loops that run at different speeds:

1. **Daily, in code:** record every decision, run alternative strategies in shadow, and calibrate the models that get dense feedback.
2. **Weekly, Claude as reviewer:** read the journal, check that the bot did what the backtest says it should, and flag problems.
3. **Quarterly, Claude as researcher with both of us as gatekeepers:** turn observations into pre-registered hypotheses and test them on history. Survivors run in shadow, and a change reaches the live bot only through a pull request we both approve.

Claude stays out of the order path. An LLM's trading decisions can't be backtested honestly, because the model remembers the market history it would be tested on. Published LLM trading agents lose half or more of their backtested performance once tested after their training cutoff.

This doesn't replace the strategy choice. Option A (long-or-flat daily trend, volatility-targeted) stays the strategy. This document is about how that strategy, and the people and Claude sessions running it, get better without overfitting.

*How this was put together: a literature search on LLM trading agents, look-ahead bias and adaptive model combination, plus our own walk-forward experiment on Coin Metrics daily BTC data. The experiment used no data after 31 May 2025, leaving the last year as an untouched holdout. Its method, caveats and full output are in [`research/learning-experiments.md`](research/learning-experiments.md), and the script is [`research/learning_experiments.py`](research/learning_experiments.py). As in the earlier research, several sources could only be read through abstracts and search summaries, so spot-check key numbers before relying on them.*

## "Learning from trades" is mostly a data problem

A daily trend bot generates a lot of data about some things and almost none about others. What it can learn, and how fast, depends on which kind of data it is.

| What we would learn about | Observations a year, live | Time to detect a real improvement | Learnable from our own trading? |
|---|---|---|---|
| **When to be long** (the signal) | 2–5 entries; 365 daily returns | 13–20+ years for a +0.2 Sharpe gain (table below) | **No.** Only from history, then a long forward shadow run |
| **Per-trade statistics** (win rate, payoff) | 2–5 closed trades | About 100 trades, i.e. 20–40 years, to pin a win rate down to ±10 points | **No** |
| **Volatility estimate** (position size) | 365 forecasts scored daily | About 2 years (our test reached t ≈ −2.5 after two years) | **Yes, slowly** |
| **Execution** (slippage, fees, order type, timing) | Every order (about 36 small rebalances a year), plus order-book snapshots we record each minute | Months | **Yes** |
| **Operations** (missed candles, rejected orders, reconnects, replay mismatches) | Continuous | Immediately | **Yes.** Early losses are most likely to come from here |

The signal row is the one people mean by "learning from trades", and it is hopeless at our scale. The arithmetic is simple. Suppose the current strategy (the champion) and a candidate replacement (the challenger) run side by side on the same daily data, with similar volatility and correlation ρ. The years needed before the challenger's Sharpe advantage reaches a t-statistic of 2 are about **8(1 − ρ) ÷ ΔSharpe²**:

| Sharpe gain | ρ = 0.80 | ρ = 0.90 | ρ = 0.95 | ρ = 0.99 |
|---|---|---|---|---|
| +0.1 | 160 years | 80 | 40 | 8 |
| +0.2 | 40 | 20 | 10 | 2 |
| +0.3 | 18 | 9 | 4 | 1 |
| +0.5 | 6 | 3 | 2 | 0.3 |

This is a trap in both directions. A challenger that differs a lot from the champion (low ρ) is drowned in noise. One that differs only slightly (high ρ) can only offer a tiny Sharpe gain. Live P&L is therefore the slowest teacher we have. This is why the validation research already warns against re-tuning on live results ([Arnott, Harvey & Markowitz](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/)), and why Quantopian found that the more a strategy was backtested, the worse it did live ([Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)).

## Our test: 15 ways to learn from results, none reliably better

We built 14 long-or-flat sub-signals from the literature, called "arms" below: momentum over 30–365 days, Donchian breakouts over 10–160 days, and price above a 20–200-day average. The baseline averages all 14 with fixed equal weights. Each learning scheme combines the same arms but adapts to past results. All schemes use identical sizing (40% volatility target), costs (0.15% per side) and rebalance band, so differences come only from the learning. Each scheme sees only information available at the time.

| Scheme (2016 to May 2025) | What it learns from | CAGR | Sharpe | Max DD | Round trips/yr | P(no better than fixed) |
|---|---|---|---|---|---|---|
| **Fixed equal-weight ensemble** | Nothing | 54.9% | **1.62** | −38.8% | 3.4 | — |
| Option A blend (fixed) | Nothing | 54.5% | 1.63 | −36.7% | 3.3 | 0.37 |
| Pick best arm, trailing 180/365/730 days | Each arm's recent Sharpe | 48–53% | 1.39–1.45 | −41% to −58% | 6.0–8.2 | 0.86–0.95 |
| Top-3 arms, trailing 365 days | Same | 51.6% | 1.55 | −34.8% | 5.2 | 0.74 |
| Sharpe-weighted arms | Same | 52.2% | 1.56 | −39.1% | 3.9 | 0.89 |
| Hedge (exponential weights), η = 0.5 / 2 / 8 | Each arm's cumulative return | 47–55% | 1.64 / 1.53 / 1.41 | −43% to −50% | 5.0–11.3 | 0.37 / 0.82 / 0.94 |
| Drop an arm after losing trades (last 3 / 5) | Each arm's own closed trades | 34% / 41% | 1.61 / 1.58 | −18.8% / −34.5% | 1.6–2.0 | 0.55 / 0.68 |
| Equity-curve filter, 50 / 100 days | The strategy's own equity curve | 59% / 53% | **1.84** / 1.64 | −23.1% / −29.3% | 4.4–4.7 | **0.05** / 0.38 |
| ML meta-label filter (walk-forward logistic) | Whether past signals like today's paid off | 31.4% | 1.28 | −45.2% | 4.9 | 0.91 |
| Turning points, learned state weights | Which market states paid in the past | 61.4% | 1.38 | −60.1% | 5.4 | 0.94 |
| *Buy and hold, 40% vol target* | — | 58.7% | 1.27 | −65.1% | 1.6 | 0.97 |

*P(no better than fixed) is the share of 2,000 paired block-bootstrap resamples in which the scheme's Sharpe did not beat the fixed ensemble's. It is a rough one-sided p-value with no correction for the number of schemes tried.*

Five findings stand out.

First, **chasing recent winners hurts.** Picking the arm with the best recent Sharpe cost 0.16–0.22 of Sharpe, about doubled turnover and deepened the worst drawdown. Softer versions (top-3, Sharpe-weighting) did less damage but were still worse than the fixed weights. This is the "forecast combination puzzle": simple averages keep beating estimated weights because the estimation error outweighs the gain ([Smith & Wallis](https://econpapers.repec.org/RePEc:bla:obuest:v:71:y:2009:i:3:p:331-355)). DeMiguel, Garlappi and Uppal found the same for portfolios: none of 14 optimised models consistently beat 1/N out of sample ([IDEAS/RePEc](https://ideas.repec.org/a/inm/ormnsc/v55y2009i5p798-812.html)).

Second, **online learning converges on doing nothing.** The textbook online-learning algorithm (Hedge) matched the fixed ensemble only at its gentlest setting (correlation 0.99). Each faster learning rate did worse. This matches the online portfolio selection literature, where strategies lose much of their reported performance once trading costs are modelled ([Li & Hoi survey](https://arxiv.org/pdf/1212.2129); [Ha & Zhang](https://strathprints.strath.ac.uk/id/eprint/63911)).

Third, **"learning" from losing trades is just holding less.** Benching an arm after a run of losing trades left Sharpe unchanged. It cut exposure from 41% to 23–30% and CAGR from 55% to 34–41%. The smaller drawdowns are what you would get from a smaller position.

Fourth, **learning from history which regimes pay backfired when it mattered.** One scheme learned, for each of four market states, whether being long had paid in that state so far. It had the best 2023–25 numbers of any scheme (Sharpe 1.94). It also lost **49% in 2022**, against 27% for the fixed ensemble, because 2019–21 had taught it that buying corrections pays. The walk-forward ML filter was the worst scheme overall, losing 0.34 of Sharpe.

Fifth, **one idea looked better: the equity-curve filter.** It runs the ensemble only while the ensemble's own equity is above its 50-day average, which can be read as "stop trading when the strategy itself is in a slump".
- It raised Sharpe to 1.84 and cut the worst drawdown from −39% to −23%.
- Every look-back from 20 to 200 days scored between 1.60 and 1.84, with drawdowns of −20% to −29%. The Sharpe gain came mostly from 20–50 days.
- It helped in 2018, 2019–21 and 2022, and gave up some return in 2023–25.
- Its bootstrap p of 0.05 does not survive a correction for the roughly 24 variants we tried.
- It is a second trend filter applied to the strategy's own P&L, so it learns nothing about the market. Practitioner sources agree it only helps when returns come in streaks ([LuxAlgo](https://www.luxalgo.com/library/concept/equity-curve-based-throttling/)), and trend-following returns do.
- Confirming its +0.22 Sharpe live would take about **13 years**. We found no peer-reviewed test of the idea.

It is worth pre-registering as **one shadow challenger**, not adopting.

## Where learning pays: dense feedback

Volatility is the clearest example. Each day the bot predicts the next month's volatility, and a month later it can score the prediction. We compared the 30-day rolling estimate that Option A currently uses with longer and exponentially weighted ones:

| Volatility estimator | Forecast loss (QLIKE, lower is better) | t vs 30-day, full period | …after 1 year | …after 2 years | Avg yearly miss vs the 40% target | Option A Sharpe / Max DD |
|---|---|---|---|---|---|---|
| 30-day rolling (current) | 0.680 | — | — | — | 3.9 pts | 1.63 / −36.7% |
| 90-day rolling | 0.469 | −2.8 | −0.4 | −1.3 | 2.8 pts | 1.62 / −32.5% |
| EWMA, λ = 0.94 | 0.559 | −3.9 | −1.4 | −2.4 | 2.4 pts | 1.54 / −35.5% |
| **EWMA, λ = 0.97** | **0.430** | **−3.9** | −1.5 | **−2.5** | **2.4 pts** | 1.63 / **−33.2%** |

The improvement shows up in **two years of daily scoring, not twenty**. It buys **risk control, not return**. The 30-day estimate reacts late and let realised volatility overshoot the 40% target, reaching 47–50% in 2017, 2019 and 2020. EWMA 0.97 kept the yearly miss to 2.4 points and trimmed the worst drawdown, with the same Sharpe. The general rule: **choose risk models by forecast accuracy scored every day, not by which one gave the best backtest P&L.**

Execution works the same way, and we can only measure it live. For each order, the bot should record the price when the decision was made, the price it actually got, and the fees. The gap is the *implementation shortfall* (Perold, 1988; [history](https://www.quantitativebrokers.com/blog/a-brief-history-of-implementation-shortfall)). After a few dozen orders, plus order-book snapshots recorded every minute, we can choose between market and limit orders, pick the time of day to rebalance, and correct the backtester's 0.15%-per-side cost assumption. All of these have short feedback cycles.

Operations matter most early on. Every day, the bot's live decision should match what the backtester produces on the same candle, exactly. Any mismatch is a bug, and it shows up the same day.

## Why Claude should not make the trading decisions

It is tempting to let Claude look at the market each day and decide, or to have it rewrite the strategy after each trade. The evidence against both is strong.

- **LLM decisions can't be backtested honestly.** Models memorise market history: asked whether the market rose on a given date, GPT-4o-class models answer correctly over 85% of the time. Published LLM trading agents lose roughly half or more of their backtested performance when re-tested after their training cutoff ([Profit Mirage](https://arxiv.org/abs/2510.07920); also [Glasserman & Lin](https://arxiv.org/abs/2309.17322); [Gao, Jiang & Yan](https://arxiv.org/pdf/2512.23847v1)). Claude has read about Bitcoin's history, so any backtest of "what Claude would have done" in 2018 or 2022 is contaminated. The only clean test would be years of live trading, and the earlier table shows how long that takes.
- **Reported LLM alpha doesn't survive scrutiny.** A 2026 review argues that the returns reported by FinMem, TradingAgents, FinAgent and similar agents can't be separated from contamination, unmodelled costs and short-window noise. Gross returns often turned into net losses once costs were applied ([The Alpha Illusion](https://www.alphaxiv.org/abs/2605.16895)). FinMem overtraded and showed negative alpha in every scenario of a longer test ([arXiv 2505.07078](https://arxiv.org/pdf/2505.07078)).
- **Live contests went badly.** In Alpha Arena's first season, most LLM traders lost money in 17 days. Claude Sonnet 4.5 reportedly lost about 31%, and the two early winners gave back much of their gains ([Protos](https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto/); [RootData](https://www.rootdata.com/news/412456)). These are secondary sources over a very short window.
- **Even LLM-*discovered* strategies rarely survive honest accounting.** The closest study to what we would do is Gencay (2026). It let an LLM agent search for strategies through look-ahead-proof tools. **No discovered strategy passed certification against the agent's own count of trials**, including some that were profitable out of sample ([arXiv 2608.27734](https://arxiv.org/pdf/2608.27734)). It also showed that a deliberately leaky strategy with a Sharpe of 35 passes the usual overfitting statistics (deflated Sharpe, PBO). Look-ahead has to be made impossible by the tooling; statistics alone won't catch it.
- **Practical reasons.** An LLM in the order path makes decisions non-deterministic, so the daily replay check above becomes impossible. It also adds an outage dependency and a per-decision cost.

Claude's ideas carry a subtler bias: they come from what it has read, which overlaps with the history we test on. A hypothesis Claude suggests is partly in-sample before we run a single backtest. That is fine, as long as **forward shadow results count for more than research-set backtests** when judging Claude's ideas.

What Claude is good at here:
- reading a week of decisions and fills and spotting what doesn't fit;
- explaining anomalies;
- writing and checking analysis code;
- keeping the research ledger honest;
- turning observations into precise, testable hypotheses;
- writing up results so the other developer, and the next Claude session, can build on them.

## The design: one fixed strategy, three learning loops

```
 LOOP 1 · every day at 00:00 UTC · code only, no LLM
   daily candle ─┬─▶ champion ─▶ risk checks ─▶ broker ─▶ fills
                 └─▶ challengers (shadow: same candle, no orders)
   decision journal ◀── decisions, fills, costs, replay check, health metrics
   dense-feedback calibration: score vol forecasts, update the backtester's cost model
        │
        ▼
 LOOP 2 · weekly · Claude reviews the journal (read-only)
   replay matched? costs vs model? data gaps or rejects? inside the expected range?
   ─▶ review stored + Telegram summary, anomalies flagged to us, candidate hypotheses
        │
        ▼
 LOOP 3 · quarterly · Claude researches, both of us decide
   hypothesis issue (pre-registered) ─▶ check LESSONS.md and the research ledger
   ─▶ research-set backtest (logged, N + 1) ─▶ shadow run ─▶ PR with both approvals
   ─▶ LESSONS.md entry, pass or fail
        │
        └──▶ a promoted change becomes the next strategy version in loop 1
```

### The daily strategy (the champion)

The champion is Option A from [`STRATEGY_OPTIONS.md`](STRATEGY_OPTIONS.md), specified exactly in [`STRATEGY_SPEC.md`](STRATEGY_SPEC.md). Once a day, at the 00:00 UTC close, the bot:

1. Closes and validates the daily candle (no gaps, no duplicate timestamps).
2. Computes the ten sub-signals (momentum over 30/60/90/180/365 days, Donchian over 10/20/40/80/160 days) and averages them into a signal between 0 and 1.
3. Forecasts volatility and sets the target weight = signal × min(1, 40% ÷ forecast vol).
4. Trades only if the target is at least 10 points away from the current weight, or the position is opening or closing.
5. Sends the order and records the fill.
6. Writes a **decision record**, even on the ~360 days a year with no trade.
7. Runs each **shadow challenger** on the same candle and records what it would have done. Challengers place no orders.

We propose two changes when Option A is pre-registered, both chosen on the research set only:
- **Use EWMA (λ = 0.97) volatility instead of the 30-day rolling estimate.** It was chosen on forecast accuracy, the right criterion for a risk model, not on P&L.
- **Run the equity-curve filter (50-day) as the first shadow challenger.** It stays in shadow until it meets the promotion criteria below.

### Loop 1: daily, in code (no LLM)

- **Decision journal.** One record per day, plus records for orders, fills and round-trip trades (schema below). This is the raw material for every other loop.
- **Shadow challengers.** The engine runs any number of strategies on the same candles. Only the champion's orders reach the broker. Running challengers on daily bars costs nothing.
- **Replay check.** The backtester replays the day's candle. Its target weight must equal the live one exactly; a mismatch raises an alert.
- **Dense-feedback calibration.**
  - Score yesterday's volatility forecast once the outcome is known.
  - Record the decision price against the fill price and fees for every order.
  - Log a top-of-book and depth snapshot every minute; it costs nothing and builds a slippage dataset.
  - These updates feed the backtester's cost model and the reports. **They never change the live trading rules automatically.**
- **Health metrics.**
  - Equity in USDT and in BTC.
  - Where cumulative P&L sits in the backtest's Monte Carlo range.
  - A CUSUM drift statistic.
  - Drawdown against its pre-registered limit.

  Breaches go out as events to Telegram, as in [`../PLAN.md`](../PLAN.md).

### Loop 2: weekly, Claude reviews the journal

A scheduled job on the VPS sends Claude the week's records once a week. Its inputs are the decision and fill records, the health metrics, the previous four reviews and `LESSONS.md`. Claude returns a structured review (JSON plus a short markdown summary), which is stored in the database, shown on the dashboard and summarised to Telegram. Each review answers the same questions:

1. Did every live decision match the replay? List any that didn't.
2. What did execution cost compared with the model (bps per order, fees)?
3. Were there data gaps, late candles, rejects, reconnects or reconciliation differences?
4. Is cumulative performance inside the expected range? Has any retirement trigger moved closer?
5. Did anything happen that the rules didn't anticipate, such as an exchange outage, a wick or a halted market?
6. Are there observations worth a hypothesis? These are written as candidates only.

The review is **not allowed to recommend changing the strategy because of recent P&L**. The prompt says so, and so does the output schema, which has no field for it.

Claude's access is limited:
- It gets a read-only export.
- It never sees exchange keys or `.env`.
- It has no GitHub token on the VPS. We open issues from the review ourselves.

A single API call with structured output is enough; no agent framework is needed. At today's list prices for Claude Opus 5.5 ($4 per million input tokens, $20 per million output tokens), a review of about 40k tokens in and 4k out costs roughly **$0.25, about $1 a month**. The bot keeps trading if the API is down.

### Loop 3: quarterly, Claude researches and we decide

Each quarter, one of us runs a Claude Code research session over the hypothesis backlog:

1. **Pre-register.** Each hypothesis becomes a GitHub issue with:
   - the exact rule;
   - where it came from (paper, review, Claude's suggestion);
   - the variants we are allowed to try, decided in advance;
   - what result would accept or reject it.
2. **Check memory.** Search `LESSONS.md` and the research ledger. If the idea, or an equivalent, has already been tested, don't test it again unless there is new data.
3. **Test on the research set only.** The backtester appends every run to the research ledger automatically; logging isn't left to anyone's discipline. Evaluate against the champion:
   - paired bootstrap;
   - deflated Sharpe using the ledger's total N;
   - a parameter plateau rather than a single best value;
   - no regime (2018, 2019–21, 2022, ETF era) materially worse than the champion.
4. **Shadow.** Survivors run as challengers on live data for at least two quarters. The point is to confirm that they behave as backtested: signals match the replay, turnover and costs are as expected. Two quarters can't prove an edge (the earlier table says why).
5. **Promote by pull request.** Promotion changes the versioned strategy config. The PR carries a "Risk to live trading" section and needs both approvals. The old champion keeps running in shadow so we can roll back.
6. **Record the result either way.** Write a `LESSONS.md` entry for every hypothesis, accepted or rejected. A rejected idea recorded is as valuable as an accepted one, because it stops the next session from re-testing it and inflating N.

Promotion rules:
- At most one change is promoted per quarter, so each change can be attributed.
- Changes that reduce risk or complexity need less evidence than changes that add exposure.

Retirement rules are pre-registered as in [`research/validation-sizing-and-risk.md`](research/validation-sizing-and-risk.md): halt for review if live drawdown exceeds the Monte Carlo 95th–99th percentile, if cumulative P&L sits below the 5th percentile for three months or more, or if execution costs wipe out the expected edge. A fix is a new hypothesis, not a live tweak.

The holdout (data from 1 June 2025) is used **once**, for the first pre-registered champion and its first challenger together. After that, honest out-of-sample evidence comes only from time passing: each quarter of new data is out of sample for every hypothesis registered before it. That is slow, but it is real learning.

### How Claude remembers

Claude doesn't learn from our trades in the sense of updating its model. Each session starts fresh. Whatever we want it to have learned must be written down where the next session will read it:

| Memory | What it holds | Written by |
|---|---|---|
| Decision journal (database) | Every daily decision, order, fill, trade and health metric | The bot (loop 1) |
| Weekly reviews (database) | What happened and what looked wrong | Claude (loop 2) |
| Research ledger (`research_runs` table or CSV) | Every backtest ever run: rule, parameters, dates, result. Gives the N for deflated Sharpe | The backtester, automatically |
| `docs/strategy/LESSONS.md` | Short, curated conclusions with links to evidence. Status: open, rejected, shadow or adopted | Claude drafts, we approve via PR |
| `CLAUDE.md` | A pointer: "read `LESSONS.md` before any strategy work" | Us |

Seed lessons from the research so far:
- Averaging lookbacks beats picking one.
- Picking recent winners hurts.
- Fixed weights beat learned weights.
- Daily RSI(2) mean reversion fails.
- The MVRV > 3 exit never fired in the 2023–26 cycle.
- Costs barely matter at daily turnover.
- The ML meta-label filter hurt.
- Learned regime weights failed in 2022.
- EWMA volatility forecasts beat the 30-day estimate.
- The equity-curve filter is promising but unproven.

## What to record

These tables extend the storage plan in [`../PLAN.md`](../PLAN.md) (candles, orders, fills, positions, equity snapshots, events):

| Record | When | Key fields |
|---|---|---|
| `decision` | Every candle close, trade or not | Candle timestamp and source; strategy version (git SHA + config hash); each sub-signal value; blended signal; vol forecast and estimator; target, drifted and final weight; band decision and reason; risk-check results; intended order; best bid/ask and mid at decision time |
| `order` / `fill` | Every order | Sent, acknowledged and filled timestamps; limit and fill price; quantity; fee and fee asset; slippage vs decision mid in bps; partial fills; rejects and reasons |
| `trade` | Each closed round trip (derived) | Entry and exit decision IDs; days held; gross and net return; worst and best move during the trade; P&L split into BTC move, sizing and costs |
| `shadow_decision` | Every candle close, per challenger | Challenger ID and version; target weight; paper equity |
| `health` | Daily | Equity in USDT and BTC; replay match; cone percentile; CUSUM; drawdown vs limit; vol forecast error once known; data issues |
| `book_snapshot` | Every minute | Top N levels of bid and ask; for slippage modelling |
| `research_run` | Every backtest | Hypothesis issue; rule and parameters; data window; metrics; whether the holdout was touched |

## Guardrails

- **No LLM in the order path.** The champion's daily decision is deterministic code that the backtester can replay.
- **Claude never changes live strategy parameters, risk limits or `TRADING_MODE`.** Every change is a PR with a "Risk to live trading" section and both approvals, as `CLAUDE.md` already requires.
- **No change in response to recent P&L.** "We lost money this month" is not a hypothesis.
- **Every backtest counts.** The ledger is append-only and written by the backtester, and its N goes into the deflated Sharpe.
- **The holdout is used once,** for the first pre-registered strategy.
- **The weekly reviewer is read-only.** It gets no exchange keys, no `.env` and no GitHub write access. It reads only our own data, not web pages, so outside text can't inject instructions.

## How this fits the build plan

| Phase ([`../PLAN.md`](../PLAN.md)) | Addition for the learning loop |
|---|---|
| 2. Market data & storage | `decision`, `shadow_decision`, `health`, `book_snapshot` and `research_run` tables; minute order-book snapshots |
| 3. Engine core | `Signal` carries its sub-signal components, not just a target; the engine runs N shadow strategies and routes only the champion's orders; strategy versions are recorded |
| 6. Backtesting | Deterministic replay of a live day; automatic research ledger; paired bootstrap and deflated Sharpe in the standard report |
| 7. Deploy & monitoring | Health metrics and alerts; weekly Claude review job; dashboard review panel |

**Interface impact:** the `Signal` change and the new tables touch the Phase 2 and 3 interfaces that both of us build on. We should agree them in the Phase 3 issue before anyone implements them. The same goes for any new dashboard panels, which must follow [`../design/DESIGN_SYSTEM.md`](../design/DESIGN_SYSTEM.md).

## Decisions we need to make

1. **Claude's role.** Agree that Claude is reviewer and researcher only, never in the order path.
2. **Freeze the holdout** at 1 June 2025 onwards. This work used no data after 31 May 2025.
3. **Pre-registration choices:** adopt EWMA 0.97 volatility for Option A, and register the equity-curve filter as the first shadow challenger.
4. **Interfaces.** Approve the decision-journal tables and the `Signal` change as additions to Phases 2–3.
5. **Memory conventions.** Create `docs/strategy/LESSONS.md`, the research ledger and the `CLAUDE.md` pointer, all in one small docs PR.
6. **Weekly review delivery:** stored in the database and summarised to Telegram, with no GitHub token on the VPS.

## Sources
- Li et al., "Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents" (2025): https://arxiv.org/abs/2510.07920
- Glasserman & Lin, "Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis" (2023): https://arxiv.org/abs/2309.17322
- Gao, Jiang & Yan, "A Test of Lookahead Bias in LLM Forecasts": https://arxiv.org/pdf/2512.23847v1
- "The Alpha Illusion: Reported Alpha from LLM Trading Agents Should Not Be Treated as Deployment Evidence" (2026): https://www.alphaxiv.org/abs/2605.16895
- "Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?": https://arxiv.org/pdf/2505.07078
- Gencay, "What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery" (2026): https://arxiv.org/pdf/2608.27734
- Alpha Arena season 1 results (secondary): https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto/, https://www.rootdata.com/news/412456
- Smith & Wallis, "A Simple Explanation of the Forecast Combination Puzzle" (2009): https://econpapers.repec.org/RePEc:bla:obuest:v:71:y:2009:i:3:p:331-355
- DeMiguel, Garlappi & Uppal, "Optimal Versus Naive Diversification" (2009): https://ideas.repec.org/a/inm/ormnsc/v55y2009i5p798-812.html
- Li & Hoi, "Online Portfolio Selection: A Survey": https://arxiv.org/pdf/1212.2129; Ha & Zhang on market-impact costs: https://strathprints.strath.ac.uk/id/eprint/63911
- Garg, Goulding, Harvey & Mazzoleni, "Momentum Turning Points", *Journal of Financial Economics* (2023): https://scholars.duke.edu/publication/1586630
- Equity-curve throttling (practitioner): https://www.luxalgo.com/library/concept/equity-curve-based-throttling/
- Perold, "The Implementation Shortfall: Paper versus Reality", *Journal of Portfolio Management* 14(3), 1988 (summary): https://www.quantitativebrokers.com/blog/a-brief-history-of-implementation-shortfall
- Arnott, Harvey & Markowitz backtesting protocol (summary): https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/
- Quantopian in-sample vs out-of-sample study (summary): https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/
