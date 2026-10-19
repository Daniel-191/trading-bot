# Proposed v1 strategy: BTC daily trend ensemble

This is the concrete strategy we propose the bot trades first. It is Option A from [`STRATEGY_OPTIONS.md`](STRATEGY_OPTIONS.md), written down precisely enough to code, test and pre-register. It includes the one change the learning-loop research supports, a better volatility estimate (see [`LEARNING_LOOP.md`](LEARNING_LOOP.md)).

The rules work like this. Once a day, ten trend rules each vote on whether Bitcoin is in an uptrend. The share of "yes" votes sets how much BTC the bot wants to hold. That amount is then scaled down when Bitcoin is unusually volatile, and the bot only trades when the change is worth it. It holds BTC or USDT, never borrows and never bets on prices falling.

On our research data (2016 to May 2025), the rules returned **51% a year with a worst drawdown of −33%**. Buy-and-hold returned **79% a year** but fell **−84%** at its worst. The strategy lost **22% in 2022 and 16% in 2018**, when Bitcoin lost **65% and 72%**. In return, it typically captured only **35–65% of Bitcoin's gain in up years**.

That trade-off is the whole strategy. It gives up part of the rallies to avoid most of the crashes. If our goal is to beat holding Bitcoin in a bull market, this strategy will disappoint. If our goal is to own Bitcoin's upside without its 65–85% crashes, it does that.

*Numbers come from [`research/spec_check.py`](research/spec_check.py), run on Coin Metrics daily data from 1 January 2016 to 31 May 2025. Later data is held out for a single pre-registered test. These numbers are in-sample relative to most of the published research behind them, so expect live results to be meaningfully worse (see "What to expect").*

## Part 1: the technical spec

### Parameters

| Setting | Value | Why |
|---|---|---|
| Market | `TRADING_PAIR` (BTC/USDT spot) | Bitcoin only (`CLAUDE.md`). Spot means no liquidation risk |
| Positions | Long or flat, 0 ≤ weight ≤ 1 of strategy capital | Buy signals beat sell signals on BTC; no leverage |
| Decision time | Once a day, on the 00:00 UTC daily close | Daily bars have the best evidence; fees stay negligible |
| Momentum votes | 5 votes: close today > close *L* days ago, for *L* = 30, 60, 90, 180, 365 | Time-series momentum (Liu & Tsyvinski; Detzel et al.) |
| Breakout votes | 5 votes, each a Donchian channel with *L* = 10, 20, 40, 80, 160: on when the close ≥ the highest close of the previous *L* days; off when the close ≤ the lowest close of the previous *L*/2 days; otherwise unchanged | Turtle/Concretum-style breakouts with a built-in exit |
| Signal | *s* = ½ × (share of momentum votes on) + ½ × (share of breakout votes on), in steps of 0.1 | Averaging lookbacks avoids picking a lucky one (all single lookbacks from 30–150 days scored similarly) |
| Volatility forecast | σ̂ = √(365 × EWMA of squared daily log returns), λ = 0.97 (half-life about 23 days) | Forecast BTC volatility better than the 30-day window (t ≈ −3.9) |
| Target weight | *w*\* = *s* × min(1, 40% ÷ σ̂) | Volatility targeting; at 2023–25 volatility (43–51%) a full signal means 78–93% in BTC |
| Rebalance band | Trade only if *w*\* = 0 or the position is 0, or \|*w*\* − *w*\| ≥ 0.10 | Stops volatility noise from churning fees |
| Warm-up | 365 daily closes before the first decision | Longest lookback |
| Cost assumption (backtest) | 0.15% per side (0.10% taker fee + 0.05% slippage) | Binance base tier; to be replaced by measured costs |

*w* is the current, drifted weight: BTC value ÷ (BTC value + USDT) in the strategy's account.

### The daily decision, as code

```python
# Runs once per day after the 00:00 UTC candle is final. Use Decimal for money in the real code.
def decide(closes, current_weight, donchian_state):
    mom = [closes[-1] > closes[-1 - L] for L in (30, 60, 90, 180, 365)]
    brk = []
    for L in (10, 20, 40, 80, 160):
        prev = closes[-1 - L : -1]  # previous L closes, excluding today
        prev_exit = closes[-1 - max(L // 2, 2) : -1]
        on = donchian_state[L]
        if not on and closes[-1] >= max(prev):
            on = True
        elif on and closes[-1] <= min(prev_exit):
            on = False
        donchian_state[L] = on
        brk.append(on)
    signal = 0.5 * mean(mom) + 0.5 * mean(brk)
    vol = ewma_annualised_vol(closes, lam=0.97)
    target = signal * min(1, 0.40 / vol)
    if target == 0 or current_weight == 0 or abs(target - current_weight) >= 0.10:
        return target  # rebalance to this weight
    return current_weight  # inside the band: do nothing
```

The Donchian votes carry state from one day to the next. The engine must persist that state, and rebuild it on restart by replaying history, so that a restart can never change a decision.

### Orders and execution

1. Wait until the exchange marks the daily candle final. Fetch it over REST and check for gaps or duplicates against the stored candles. If anything is wrong, skip the day and alert; never trade on a bad candle.
2. Convert the weight change into a BTC quantity. Round it to the exchange's step size, and skip it if it is below the minimum notional.
3. Place a post-only limit order at the best bid (buys) or best ask (sells), re-pegging each minute for up to 15 minutes.
4. If part is still unfilled after that, send the remainder as a limit order that crosses the spread, capped at 0.2% from the decision-time mid price. If it still doesn't fill, cancel it and alert.
5. Record the decision price, fill price and fees for every order (the implementation shortfall). This is the first thing the learning loop calibrates.

The research set implies about **36 small rebalances a year** (a median of 13% of the account each). Turnover adds up to about **2.6 full round trips a year**, and the bot is completely out of BTC on only about 5% of days.

### Safety rails and pre-registered limits

| Rail | Rule | Note |
|---|---|---|
| Disaster stop | An exchange-side stop order sells the whole position if BTC trades **30% below the latest daily close**. It is re-placed after each daily close. After it fires, the next daily decision applies the normal rules | Covers outages and flash crashes between decisions. Untested: daily closes can't show intraday moves. Check against Binance 1-minute data in Phase 6 |
| No leverage, no shorts | Weight is capped at 1 and floored at 0, enforced in the risk manager as well as the strategy | |
| Bad data | No decision on a missing, late or inconsistent candle | |
| Replay check | The live decision must equal the backtester's replay on the same candle | Any mismatch is a bug: alert and pause new buys |
| Review trigger (yellow) | Drawdown beyond **−30%** | About the 95th-percentile one-year drawdown in a block bootstrap of the research-set returns |
| Halt for review (red) | Drawdown beyond **−45%**; or cumulative return below the 5th percentile of the expected range for 3+ months; or measured costs above 0.5% per side over 20 orders | −45% is about the 99th-percentile three-year drawdown in the same bootstrap. Halting pauses new buys; it doesn't sell |

The worst drawdown on the research set was −33.2%. The bootstrap ranges come from that same optimistic sample, so the thresholds lean generous rather than strict.

### What to expect

Research set, 1 January 2016 to 31 May 2025, 0.15% per side. Each row is one continuous run, and the regime rows are slices of it, as the live bot would experience them:

| | CAGR | Sharpe | Max drawdown | Time-avg BTC weight | Round trips/yr |
|---|---|---|---|---|---|
| **v1 strategy** | **51.0%** | **1.63** | **−33.2%** | 38% | 2.6 |
| Buy and hold | 78.9% | 1.19 | −83.8% | 100% | 0.1 |
| Buy and hold, 40% vol target | 53.5% | 1.25 | −60.7% | 65% | 0.9 |
| 200-day SMA filter | 70.9% | 1.24 | −68.0% | 65% | 3.1 |

By regime:

| Period | v1 CAGR | v1 Sharpe | v1 Max DD | Buy and hold CAGR | Buy and hold Max DD |
|---|---|---|---|---|---|
| 2016–17 bull | 154% | 2.77 | −20% | 455% | −36% |
| 2018 bear | −16.5% | −1.29 | −22% | −72% | −81% |
| 2019–21 | 63% | 1.84 | −19% | 132% | −61% |
| 2022 bear | −22% | −2.67 | −22% | −65% | −67% |
| 2023 to May 2025 | 50% | 1.60 | −20% | 114% | −28% |

Calendar years, v1 against buy-and-hold:

| | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 to May |
|---|---|---|---|---|---|---|---|---|---|---|
| v1 | +104% | +217% | −16% | +56% | +125% | +23% | −22% | +59% | +63% | +3% |
| Buy and hold | +129% | +1,250% | −72% | +88% | +310% | +62% | −65% | +165% | +114% | +11% |

Four points matter more than the headline numbers.

- **These numbers are optimistic.** The rules come from papers that used much of this data, and published edges shrink by roughly 26–58% out of sample. The earlier research expects a **live Sharpe of about 0.5–1.0**, not 1.6.
- **The recent edge is protection, not outperformance.** From 2023 to May 2025, buy-and-hold beat v1 on both return (114% against 50% a year) and Sharpe (1.81 against 1.60). v1's only advantage was a smaller drawdown (−20% against −28%). [`STRATEGY_OPTIONS.md`](STRATEGY_OPTIONS.md) found the same for the ETF era.
- **It trails in every strong up year.** It typically captured 35–65% of BTC's gain, and only 17% in 2017's mania. It never sells the top: on 13 April 2021, the highest close of the spring 2021 rally, it held 58% (example below).
- **Daily losses still happen.** The worst single day on the research set was −9.4% of the account, and a typical year's worst drawdown in the bootstrap is about −17%.

### Worked examples

| Date | BTC close | Momentum votes (30/60/90/180/365) | Breakout votes (10/20/40/80/160) | Signal | Vol forecast | Target weight |
|---|---|---|---|---|---|---|
| 13 Apr 2021 (spring 2021 peak close) | $63,446 | 5 of 5 | 5 of 5 | 1.0 | 69% | **58%** |
| 22 Jun 2021 (after the May crash) | $32,395 | 2 of 5 (180, 365) | 0 of 5 | 0.2 | 96% | **8%** |
| 18 Jun 2022 (June 2022 crash low) | $19,014 | 0 of 5 | 0 of 5 | 0.0 | 93% | **0%** |
| 11 Mar 2024 (ETF rally) | $72,198 | 5 of 5 | 5 of 5 | 1.0 | 58% | **69%** |

## Part 2: the same strategy in plain English

**Ten judges vote every midnight.** Once a day, at midnight UTC, the bot asks ten simple questions about Bitcoin's price. Each answer is a yes or no:
- **Five "is it higher than before?" questions.** Is today's price higher than 1 month ago? 2 months? 3 months? 6 months? 1 year?
- **Five "did it just break out?" questions.** Has the price just climbed above its recent range, for ranges of 10, 20, 40, 80 and 160 days? Once a breakout question says yes, it keeps saying yes until the price falls through the bottom of a shorter range.

**The votes work a dimmer, not an on/off switch.** If all ten say yes, the bot wants to be fully in Bitcoin. If six say yes, it wants a bit over half. If none do, it holds only dollars (USDT). Because the judges look at different time spans, the votes change gradually. The bot usually holds *some* Bitcoin and turns the amount up or down as the trend strengthens or fades. It's completely out only about 5% of the time.

**It slows down in a storm.** When Bitcoin is swinging around more than usual, the bot holds less of it, like driving slower in bad weather. The aim is for the account to swing by about the same amount (40% a year) whatever the market is doing. When Bitcoin is calm, the bot can hold the full amount the votes ask for. When Bitcoin is wild, it holds less.

**It doesn't fidget.** If the new target is within 10% of what it already holds, it does nothing. In practice it trades about three times a month, usually a small adjustment.

**It never borrows and never bets on a fall.** The worst case is Bitcoin falling while the bot holds some. There is no leverage and no liquidation. When trends are down, it sits in dollars.

**An emergency brake covers the gaps.** If Bitcoin crashes 30% between two midnights, a standing order on the exchange sells automatically, even if the bot itself is down.

**The trade-off.** It is like holding Bitcoin with a seatbelt. The seatbelt kept it to about −22% in 2022, when Bitcoin fell 65%, and about −16% in 2018, when Bitcoin fell 72%. The price of the seatbelt is that it only catches part of the big rallies: about half of 2024's gain and a sixth of 2017's. It will never sell at the very top or buy at the very bottom. It gets out after a trend breaks and back in after a new one starts.

**The four example days, in words:**
- **13 April 2021, the peak of the spring 2021 rally.** All ten judges said "uptrend", but Bitcoin was very volatile, so the bot held 58% rather than 100%. It did not see the top coming; no trend rule can.
- **22 June 2021, after Bitcoin halved.** Only the two slowest judges (6 months and 1 year) still said yes. The market was extremely jumpy, so the bot held 8%.
- **18 June 2022, the June crash low.** Every judge said no, and the bot held nothing. Bitcoin fell further, to about $15,800 in November, and the bot held little through the rest of 2022 (11% on average over the year). It only bought back in properly once a new uptrend started.
- **11 March 2024, the ETF rally.** All ten said yes, Bitcoin was calmer than in 2021, and the bot held 69%.

**Why this and not something cleverer?** We tested cleverer versions: picking whichever rule had worked lately, machine-learning filters, and learning from past trades. They did worse on the same data (see [`LEARNING_LOOP.md`](LEARNING_LOOP.md)). Simple, averaged and slow is what held up. Published research on Bitcoin points the same way.

**How it gets better over time.** The rules don't change on their own. The bot writes down every decision and trade. Claude reviews that log weekly for mistakes, costs and anything odd. New ideas are tested on history first, then run in parallel on paper, and adopted only if both of us approve. The first idea in that queue is a pause that kicks in when the strategy's own results are in a slump.

## What v1 deliberately leaves out

| Not in v1 | Why |
|---|---|
| Shorting, leverage, perps | Weak evidence for the short side on daily bars; adds liquidation and funding risk (Options C/D) |
| Faster timeframes (hourly, intraday) | Fees eat the edge (Option D) |
| Funding, Fear & Greed or on-chain filters | Unproven; each is a separate variant to test later (Option B) |
| Profit targets or tight stop-losses | Stops reduce returns unless prices trend, and the trend exits already do that job (Kaminski & Lo) |
| ML or Claude making the decisions | Worse in our test; LLM decisions can't be backtested honestly ([`LEARNING_LOOP.md`](LEARNING_LOOP.md)) |
| Equity-curve pause | Promising but unproven: the first shadow challenger, not part of v1 |

## Next steps

1. **Agree the objective.** "BTC exposure with much smaller crashes" is what this delivers. "Beat holding BTC" is not.
2. **Pre-register these rules** in a GitHub issue, unchanged. Register the equity-curve pause as the one challenger, then freeze both.
3. **Re-run the tables on Binance BTC/USDT data** in our own backtester (Phase 6). The numbers here come from Coin Metrics reference prices. This includes checking the disaster stop against 1-minute data.
4. **Run the holdout once** (1 June 2025 onwards), for the champion and the challenger together, and record the result whatever it is.
5. **Paper, then testnet, then live with the minimum notional**, following the durations in [`research/validation-sizing-and-risk.md`](research/validation-sizing-and-risk.md). Going live needs its own issue and both of us agreeing (`docs/PLAN.md`).

## Sources
Evidence for the rule family, the volatility target and the fee arithmetic is cited in [`STRATEGY_OPTIONS.md`](STRATEGY_OPTIONS.md) and [`research/`](research/). The main ones:
- Detzel et al., *Financial Management* 2021: https://ideas.repec.org/a/bla/finmgt/v50y2021i1p107-137.html
- Liu & Tsyvinski, "Risks and Returns of Cryptocurrency": https://www.nber.org/system/files/working_papers/w24877/w24877.pdf
- Corbet et al., buy vs sell signals on BTC: https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html
- Zarattini, Pagani & Barbon, "Catching Crypto Trends": https://concretumgroup.substack.com/p/catching-crypto-trends
- Moreira & Muir, volatility-managed portfolios: https://www.nber.org/papers/22208
- Kaminski & Lo, "When Do Stop-Loss Rules Stop Losses?": https://dspace.mit.edu/entities/publication/bb69ca4b-0cdc-487f-831d-63b2e84fafee
- McLean & Pontiff, out-of-sample decay: https://www.gwern.net/doc/economics/2016-mclean.pdf
