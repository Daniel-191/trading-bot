# Own walk-forward test: can a daily BTC trend bot improve by learning from its results?

These notes come from our own analysis. They back the findings in [`../LEARNING_LOOP.md`](../LEARNING_LOOP.md). The question is narrow: given the trend core recommended in [`../STRATEGY_OPTIONS.md`](../STRATEGY_OPTIONS.md), does any scheme that adapts to the strategy's own past results beat simply running the fixed rules?

## Method
- **Data:** Coin Metrics Community Data, `csv/btc.csv`, daily `PriceUSD` (the same file as [`own-backtest.md`](own-backtest.md), SHA-256 `06495ff8e643432e6948b7b4686ce44fc106217287dabdc1b38351d9ddec46c3`). Binance hosts were still blocked from this environment.
- **Holdout respected:** the script reads no prices after **2025-05-31**. Everything from 2025-06-01 onwards is left unseen, as the proposed holdout for the one-time test of the pre-registered strategy. (The earlier `own-backtest.md` run did look at data to May 2026, so the holdout is only clean with respect to this work and any later work.)
- **Script:** `learning_experiments.py` in this folder. Run it with `uv run --no-project --with pandas --with numpy python -I learning_experiments.py btc.csv` (pandas 3.0.5, numpy 2.5.3). It is research scratch code, not part of the bot.
- **Evaluation window:** 2016-01-01 to 2025-05-31 (9.4 years), so that learners with two-year look-backs have history to learn from. Sub-periods: 2016–17 bull, 2018 bear, 2019–21, 2022 bear, 2023 to May 2025.
- **Execution, costs and sizing:** identical to `btc_backtest.py`: the weight decided on the close of day t earns the t to t+1 return; 0.15% per side; 10-point rebalance band; long or flat spot. **Every scheme is sized the same way**, signal × min(1, 40% ÷ 30-day realised vol), so differences come only from how the signal is learned.
- **Arms:** 14 long/flat sub-signals from the literature: time-series momentum 30/60/90/180/365 days, Donchian 10/20/40/80/160 days (exit on a half-lookback low), and price above its 20/50/100/200-day SMA.
- **Baselines (no learning):** the equal-weight average of all 14 arms ("fixed ensemble"), and Option A's blend (the average of the momentum and Donchian ensembles).
- **Information discipline:** the return an arm earns from t to t+1 is only known at t+1, so every learner uses yesterday's information. Trades count as closed only after their exit close. The ML filter's labels (10-day forward return) enter training only once they are known, plus a one-day embargo.

### Learning schemes tested (15 variants)
| Family | What it learns from | Variants |
|---|---|---|
| Pick the best arm | Each arm's trailing Sharpe; re-chosen monthly | look-back 180, 365, 730 days |
| Top-3 arms | Same, equal weight on the best three | 365 days |
| Sharpe-weighted | Weights ∝ max(0, trailing Sharpe), monthly | 365 days |
| Hedge (exponential weights) | Each arm's cumulative log return; daily | η = 0.5, 2, 8 |
| Drop an arm after losing trades | The arm's own last k closed trades, net of costs | k = 3, 5 |
| Equity-curve filter | The ensemble's own equity vs its n-day average | n = 50, 100 |
| Meta-label filter (ML) | Walk-forward logistic regression on 6 features, refit quarterly: "will the next 10 days be up when we are long?" | 1 |
| Turning-point states | Slow (365d) and fast (30d) momentum agree or disagree (after Garg et al.) | static weights; weights learned from each state's history |

Follow-ups, run after seeing the first results and counted as extra variants:
- an equity-curve filter plateau sweep (n = 20, 30, 75, 150, 200; five new variants);
- Option A sized with four alternative volatility estimators (four new variants).

**Variant ledger:** this work adds **24 strategy variants** on BTC, on top of the roughly 14 variants and two sweeps in `own-backtest.md`. Count them all in any deflated Sharpe or multiple-testing correction.

### Volatility forecasting test
- **Target:** realised volatility over the next 30 days.
- **Estimators:** 30-day rolling (the current Option A choice), 90-day rolling, EWMA with λ = 0.94 (RiskMetrics) and 0.97, and an average of 30-day, 90-day and EWMA 0.97.
- **Loss:** QLIKE on variance (robust to noise in the volatility proxy). Differences against the 30-day estimator are tested with a Newey–West t-statistic (30 lags, because the targets overlap). We report the t-statistic over the full window and over its first one and two years, to show how quickly the evidence builds.
- **Tracking:** realised volatility, by year, of buy-and-hold sized to 40% with each estimator.

## Caveats
- **One asset, one path.** The 2016–2025 window has two bear markets. Every regime-level conclusion rests on very few episodes.
- **The arm menu is in-sample.** The 14 arms come from papers written with pre-2021 BTC data, and `own-backtest.md` already examined them. The test isolates the learning layer; it doesn't validate the arms.
- **Learners were not tuned.** Each family got a few reasonable settings. A determined search would find a better-looking learner, and that is exactly the overfitting this work warns about.
- **Daily closes only:** no intrabar stops or wicks, and Coin Metrics prices are a reference rate, not Binance fills.

## Key results
- **No learning scheme reliably beat the fixed ensemble** (Sharpe 1.62, CAGR 54.9%, max drawdown −38.8%, 3.4 round trips a year over 2016 to May 2025). Of 15 learning variants, 12 had a lower Sharpe. The three higher ones were +0.02, +0.02 and +0.22.
- **Chasing recent winners hurt.** Picking the best arm by trailing Sharpe lost 0.16–0.22 of Sharpe, roughly doubled turnover (6–8 round trips a year) and deepened the worst drawdown to between −41% and −58%. Paired-bootstrap P(Sharpe ≤ fixed) was 0.86–0.95. Weighting by trailing Sharpe (−0.05) and top-3 selection (−0.07) did less harm, but still did harm.
- **Online learning converges on doing nothing.** Hedge with a gentle learning rate (η = 0.5) matched the fixed ensemble (+0.02 Sharpe, correlation 0.99). Faster learning rates got worse as they learned harder (η = 2: −0.09; η = 8: −0.21).
- **Learning from each arm's own trades is de-risking, not learning.** Dropping arms after losing trades kept Sharpe the same (1.58–1.61) but cut exposure from 41% to 23–30% and CAGR from 55% to 34–41%. It shrank drawdowns (−18.8% for k = 3) in the way that simply holding less would.
- **The ML filter was the worst learner.** The walk-forward logistic meta-label filter lost 0.34 of Sharpe and cut CAGR to 31%.
- **Learning regime weights from history backfired in the regime that mattered.** Turning-point weights learned from each state's past returns earned the best 2023–25 numbers (Sharpe 1.94). But in 2022 they lost 49%, against 27% for the fixed ensemble. Their full-period drawdown was −60%: the scheme had learned in 2019–21 that "corrections" pay.
- **One scheme looked better: the equity-curve filter.** It trades the ensemble only while the ensemble's own equity is above its n-day average.
  - At n = 50 it scored Sharpe 1.84 (+0.22), CAGR 59.3% and a −23.1% max drawdown, with paired-bootstrap P ≈ 0.05.
  - The plateau is real but uneven. Every look-back from 20 to 200 days scored 1.60–1.84 and cut the worst drawdown to between −20% and −29%. The short look-backs (20–50 days) carried most of the Sharpe gain.
  - It helped in 2018, 2019–21 and 2022. In 2016–17 and 2023–25 its Sharpe was about the same and its CAGR lower (47.7% against 53.5% in 2023–25).
  - With about 24 variants tried here, a one-sided p of 0.05 does not survive a multiple-testing correction.
  - Mechanically it is a second, slower trend filter applied to the strategy's own P&L. It learns nothing about the market.
- **Volatility forecasting is where learning shows up quickly.**
  - EWMA 0.97 beat the 30-day estimator with a Newey–West t of −3.9 over the full window. The t-statistic already reached −2.5 after the first two years.
  - It cut the gap between realised and target volatility from 3.9 to 2.4 points a year. The 30-day estimator overshot 40% in 2017, 2019 and 2020 (47–50% realised).
  - Better risk estimates did not change Option A's Sharpe (1.63 for both). Max drawdown improved from −36.7% to −33.2%.
- **Telling a better variant apart in live trading takes years.** For daily returns, the live years needed for a Sharpe gain to reach t = 2 is about 8(1 − ρ) ÷ ΔSharpe², where ρ is the correlation between the champion's and the challenger's returns. A +0.2 Sharpe gain at ρ = 0.9 needs about 20 years. The equity-curve filter's +0.22 at ρ = 0.92 needs about 13.
- **Trades are scarce.** Option A's blend made 23 flat-to-long entries in 9.4 years (2.4 a year). The individual arms made 0.8–19 a year.

## Full output
```
Data 2013-01-01..2025-05-31 (research set; holdout starts after 2025-05-31)  cost/side=0.15% band=0.1 vol target=40%
Learning variants tested in this script: 15 (+2 fixed baselines)

=== EVALUATION 2016-01-01..2025-05-31 ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble            54.9%   1.62  -38.8%   41%    3.4
FIXED: Option A blend (TSMOM + Donchian)       54.5%   1.63  -36.7%   40%    3.3
Pick best arm, trailing 180d Sharpe            49.6%   1.40  -41.4%   39%    6.4
Pick best arm, trailing 365d Sharpe            52.7%   1.45  -45.2%   40%    6.0
Pick best arm, trailing 730d Sharpe            48.2%   1.39  -58.0%   41%    8.2
Top-3 arms, trailing 365d Sharpe               51.6%   1.55  -34.8%   39%    5.2
Sharpe-weighted arms, trailing 365d            52.2%   1.56  -39.1%   40%    3.9
Hedge (exp. weights), eta=0.5                  54.5%   1.64  -42.5%   39%    5.0
Hedge (exp. weights), eta=2                    49.3%   1.53  -46.2%   37%    8.4
Hedge (exp. weights), eta=8                    46.5%   1.41  -50.1%   38%   11.3
Drop arm after losing trades, last 3           34.1%   1.61  -18.8%   23%    1.6
Drop arm after losing trades, last 5           41.0%   1.58  -34.5%   30%    2.0
Equity-curve filter on ensemble, 50d           59.3%   1.84  -23.1%   29%    4.4
Equity-curve filter on ensemble, 100d          52.9%   1.64  -29.3%   31%    4.7
Meta-label logistic filter (walk-forward)      31.4%   1.28  -45.2%   32%    4.9
Turning points, static (4 states)              57.8%   1.56  -43.2%   48%    6.0
Turning points, learned state weights          61.4%   1.38  -60.1%   60%    5.4
Buy & hold                                     79.0%   1.19  -83.8%  100%    0.1
Buy & hold, vol-target 40%                     58.7%   1.27  -65.1%   70%    1.6

=== 2016-2017 bull ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble           174.9%   2.81  -20.7%   55%    3.1
FIXED: Option A blend (TSMOM + Donchian)      173.8%   2.81  -20.0%   54%    3.0
Pick best arm, trailing 180d Sharpe           131.5%   2.38  -32.4%   49%    7.8
Pick best arm, trailing 365d Sharpe           151.4%   2.74  -21.6%   42%    7.9
Pick best arm, trailing 730d Sharpe           132.5%   2.75  -17.8%   37%    9.4
Top-3 arms, trailing 365d Sharpe              169.1%   2.86  -19.9%   51%    6.3
Sharpe-weighted arms, trailing 365d           176.0%   2.85  -19.9%   54%    3.3
Hedge (exp. weights), eta=0.5                 171.8%   2.93  -19.2%   51%    4.2
Hedge (exp. weights), eta=2                   151.1%   2.92  -17.3%   44%    7.3
Hedge (exp. weights), eta=8                   135.4%   2.79  -17.6%   37%    9.1
Drop arm after losing trades, last 3          122.6%   2.84  -15.7%   40%    2.3
Drop arm after losing trades, last 5          155.3%   2.90  -18.5%   48%    2.7
Equity-curve filter on ensemble, 50d          154.3%   2.77  -20.0%   45%    5.1
Equity-curve filter on ensemble, 100d         146.0%   2.56  -22.6%   45%    3.8
Meta-label logistic filter (walk-forward)      93.1%   2.79  -14.0%   34%    7.4
Turning points, static (4 states)             190.3%   2.88  -21.6%   61%    4.4
Turning points, learned state weights         192.7%   2.73  -21.6%   61%    6.2
Buy & hold                                    464.7%   2.68  -35.8%  100%    0.2
Buy & hold, vol-target 40%                    212.6%   2.78  -25.6%   68%    1.9

=== 2018 bear ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble           -21.3%  -1.77  -23.9%   14%    2.4
FIXED: Option A blend (TSMOM + Donchian)      -17.1%  -1.36  -19.8%   15%    2.5
Pick best arm, trailing 180d Sharpe            -3.0%  -0.09  -10.1%   16%    7.7
Pick best arm, trailing 365d Sharpe           -10.2%  -0.50  -16.2%   19%    9.5
Pick best arm, trailing 730d Sharpe           -13.5%  -0.71  -16.2%   19%    9.6
Top-3 arms, trailing 365d Sharpe              -18.5%  -1.41  -19.8%   13%    5.3
Sharpe-weighted arms, trailing 365d           -23.3%  -1.79  -25.8%   15%    3.3
Hedge (exp. weights), eta=0.5                 -18.2%  -1.48  -20.4%   14%    4.1
Hedge (exp. weights), eta=2                   -19.1%  -1.34  -20.4%   17%    6.8
Hedge (exp. weights), eta=8                    -9.4%  -0.44  -15.8%   21%    9.0
Drop arm after losing trades, last 3          -12.5%  -1.49  -14.8%    9%    0.7
Drop arm after losing trades, last 5          -14.8%  -1.39  -17.5%   12%    0.7
Equity-curve filter on ensemble, 50d          -11.5%  -1.25  -14.4%    5%    1.7
Equity-curve filter on ensemble, 100d         -18.8%  -2.05  -21.4%    4%    2.6
Meta-label logistic filter (walk-forward)      -5.5%  -0.98   -8.6%    3%    1.1
Turning points, static (4 states)             -35.5%  -1.71  -38.4%   31%    6.6
Turning points, learned state weights         -32.0%  -0.98  -35.0%   47%    3.2
Buy & hold                                    -75.0%  -1.27  -81.4%  100%    0.5
Buy & hold, vol-target 40%                    -50.2%  -1.50  -55.2%   57%    1.3

=== 2019-2021 ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble            70.1%   1.83  -23.9%   40%    2.8
FIXED: Option A blend (TSMOM + Donchian)       63.3%   1.74  -25.6%   38%    2.7
Pick best arm, trailing 180d Sharpe            64.4%   1.58  -24.2%   36%    6.2
Pick best arm, trailing 365d Sharpe            67.8%   1.59  -27.2%   39%    4.7
Pick best arm, trailing 730d Sharpe            81.5%   1.90  -24.4%   37%    6.9
Top-3 arms, trailing 365d Sharpe               56.9%   1.61  -24.5%   34%    4.5
Sharpe-weighted arms, trailing 365d            60.5%   1.69  -24.0%   35%    3.5
Hedge (exp. weights), eta=0.5                  68.2%   1.82  -21.3%   37%    4.3
Hedge (exp. weights), eta=2                    66.7%   1.75  -19.8%   36%    8.9
Hedge (exp. weights), eta=8                    63.5%   1.60  -28.8%   39%   13.6
Drop arm after losing trades, last 3           33.3%   1.63  -18.1%   21%    1.4
Drop arm after losing trades, last 5           42.0%   1.55  -20.2%   30%    1.7
Equity-curve filter on ensemble, 50d           79.0%   2.11  -14.1%   29%    3.8
Equity-curve filter on ensemble, 100d          61.6%   1.74  -17.9%   32%    5.3
Meta-label logistic filter (walk-forward)      29.9%   1.14  -22.4%   32%    3.7
Turning points, static (4 states)              67.8%   1.65  -34.1%   45%    6.0
Turning points, learned state weights          76.6%   1.48  -43.4%   57%    4.2
Buy & hold                                    128.1%   1.49  -61.4%  100%    0.2
Buy & hold, vol-target 40%                     82.8%   1.54  -43.4%   63%    1.9

=== 2022 bear ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble           -26.7%  -2.91  -26.7%   12%    3.9
FIXED: Option A blend (TSMOM + Donchian)      -23.9%  -2.69  -23.9%   13%    3.5
Pick best arm, trailing 180d Sharpe           -16.2%  -1.67  -16.2%    5%    1.4
Pick best arm, trailing 365d Sharpe           -27.1%  -1.72  -27.9%   10%    4.2
Pick best arm, trailing 730d Sharpe           -28.7%  -1.70  -34.4%   19%    9.4
Top-3 arms, trailing 365d Sharpe              -24.5%  -1.99  -25.9%   12%    4.8
Sharpe-weighted arms, trailing 365d           -27.5%  -2.51  -27.5%   14%    5.2
Hedge (exp. weights), eta=0.5                 -30.7%  -2.57  -30.8%   16%    5.4
Hedge (exp. weights), eta=2                   -36.7%  -2.48  -38.1%   19%    8.5
Hedge (exp. weights), eta=8                   -37.9%  -2.27  -40.3%   21%   11.5
Drop arm after losing trades, last 3           -4.9%  -1.77   -5.0%    2%    0.6
Drop arm after losing trades, last 5          -10.0%  -2.39  -10.0%    4%    1.0
Equity-curve filter on ensemble, 50d           -7.1%  -1.97   -7.5%    3%    2.0
Equity-curve filter on ensemble, 100d          -0.9%  -1.06   -0.9%    1%    0.6
Meta-label logistic filter (walk-forward)     -20.8%  -2.80  -20.8%    9%    2.8
Turning points, static (4 states)             -24.2%  -2.15  -24.3%   16%    7.3
Turning points, learned state weights         -49.2%  -2.27  -49.3%   38%   14.5
Buy & hold                                    -65.1%  -1.33  -66.8%  100%    0.5
Buy & hold, vol-target 40%                    -55.4%  -1.66  -55.8%   68%    2.1

=== 2023..2025-05-31 ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
FIXED: equal-weight 14-arm ensemble            53.5%   1.63  -19.8%   54%    4.8
FIXED: Option A blend (TSMOM + Donchian)       54.2%   1.66  -16.9%   53%    4.4
Pick best arm, trailing 180d Sharpe            39.9%   1.15  -24.5%   60%    7.2
Pick best arm, trailing 365d Sharpe            50.5%   1.36  -34.7%   63%    5.4
Pick best arm, trailing 730d Sharpe            32.7%   0.97  -31.4%   66%    8.1
Top-3 arms, trailing 365d Sharpe               54.8%   1.59  -25.3%   57%    5.3
Sharpe-weighted arms, trailing 365d            53.9%   1.60  -20.2%   56%    4.7
Hedge (exp. weights), eta=0.5                  58.5%   1.75  -18.0%   52%    6.7
Hedge (exp. weights), eta=2                    55.1%   1.67  -22.8%   50%    9.3
Hedge (exp. weights), eta=8                    47.9%   1.44  -29.8%   53%   11.2
Drop arm after losing trades, last 3           20.9%   1.27  -11.9%   28%    1.9
Drop arm after losing trades, last 5           26.2%   1.32  -13.1%   33%    2.7
Equity-curve filter on ensemble, 50d           47.7%   1.61  -17.4%   38%    6.8
Equity-curve filter on ensemble, 100d          48.3%   1.58  -16.7%   40%    7.2
Meta-label logistic filter (walk-forward)      36.9%   1.27  -19.8%   51%    6.7
Turning points, static (4 states)              70.8%   1.85  -23.8%   61%    6.7
Turning points, learned state weights         100.9%   1.94  -23.2%   80%    3.6
Buy & hold                                    113.8%   1.80  -28.0%  100%    0.2
Buy & hold, vol-target 40%                    102.3%   1.92  -23.2%   86%    1.4

=== Each scheme vs the fixed ensemble, 2016-01-01..2025-05-31 ===
P(<=fixed): paired block bootstrap, share of resamples where the scheme's Sharpe
does not beat the fixed ensemble's. Years: live years for a Sharpe gain this size to
reach t = 2 at this correlation, 8(1 - rho) / dSharpe^2 (see the next table).
scheme                                       dSharpe     TE  corr P(<=fixed)  years
FIXED: Option A blend (TSMOM + Donchian)       +0.01   3.4%  0.99       0.37    445
Pick best arm, trailing 180d Sharpe            -0.22  15.0%  0.89       0.95  never
Pick best arm, trailing 365d Sharpe            -0.16  15.5%  0.88       0.86  never
Pick best arm, trailing 730d Sharpe            -0.22  17.4%  0.84       0.90  never
Top-3 arms, trailing 365d Sharpe               -0.07  10.0%  0.94       0.74  never
Sharpe-weighted arms, trailing 365d            -0.05   4.5%  0.99       0.89  never
Hedge (exp. weights), eta=0.5                  +0.02   4.8%  0.99       0.37    233
Hedge (exp. weights), eta=2                    -0.09  10.6%  0.94       0.82  never
Hedge (exp. weights), eta=8                    -0.21  14.7%  0.88       0.94  never
Drop arm after losing trades, last 3           -0.01  12.9%  0.95       0.55  never
Drop arm after losing trades, last 5           -0.04   9.6%  0.96       0.68  never
Equity-curve filter on ensemble, 50d           +0.22  11.5%  0.92       0.05     13
Equity-curve filter on ensemble, 100d          +0.02   9.1%  0.95       0.38    666
Meta-label logistic filter (walk-forward)      -0.34  18.4%  0.79       0.91  never
Turning points, static (4 states)              -0.06  11.0%  0.94       0.72  never
Turning points, learned state weights          -0.24  19.9%  0.89       0.94  never
Buy & hold                                     -0.42  48.1%  0.81       0.98  never
Buy & hold, vol-target 40%                     -0.34  23.7%  0.86       0.97  never

=== Plateau check on the one scheme that looked better: equity-curve filter ===
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
Equity-curve filter, 20d                       51.9%   1.73  -23.7%   27%    9.4
Equity-curve filter, 30d                       56.6%   1.80  -20.5%   28%    6.3
Equity-curve filter, 50d                       59.3%   1.84  -23.1%   29%    4.4
Equity-curve filter, 75d                       54.2%   1.68  -23.6%   30%    4.4
Equity-curve filter, 100d                      52.9%   1.64  -29.3%   31%    4.7
Equity-curve filter, 150d                      53.9%   1.66  -26.3%   32%    3.3
Equity-curve filter, 200d                      51.4%   1.60  -24.9%   34%    3.3

=== How fast does live trading reveal a better variant? ===
Years of daily returns for the difference to reach t = 2, given the Sharpe gain
and the correlation between champion and challenger (equal volatility assumed).
 dSharpe   rho=0.8   rho=0.9  rho=0.95  rho=0.99
     0.1     160.0      80.0      40.0       8.0
     0.2      40.0      20.0      10.0       2.0
     0.3      17.8       8.9       4.4       0.9
     0.5       6.4       3.2       1.6       0.3

=== Trade counts: what 'learning from trades' has to work with ===
tsmom30     128 entries in 9.4 years (13.6/yr)
tsmom60      78 entries in 9.4 years (8.3/yr)
tsmom90      64 entries in 9.4 years (6.8/yr)
tsmom180     24 entries in 9.4 years (2.5/yr)
tsmom365     10 entries in 9.4 years (1.1/yr)
don10       144 entries in 9.4 years (15.3/yr)
don20        69 entries in 9.4 years (7.3/yr)
don40        32 entries in 9.4 years (3.4/yr)
don80        18 entries in 9.4 years (1.9/yr)
don160        8 entries in 9.4 years (0.8/yr)
sma20       181 entries in 9.4 years (19.2/yr)
sma50        82 entries in 9.4 years (8.7/yr)
sma100       59 entries in 9.4 years (6.3/yr)
sma200       29 entries in 9.4 years (3.1/yr)
Option A blend: 23 flat-to-long entries (2.4/yr)

=== Volatility forecasting: learning where feedback is dense ===
Target: realised vol over the next 30 days. Loss: QLIKE on variance (lower is better).
t-stat: Newey-West (30 lags) on the loss difference vs the 30d rolling estimator;
negative = better than 30d rolling.
estimator                    QLIKE  t (all) t (1st 1y) t (1st 2y)
30d rolling (Option A)       0.680        -          -          -
90d rolling                  0.469    -2.77      -0.39      -1.34
EWMA 0.94                    0.559    -3.90      -1.39      -2.41
EWMA 0.97                    0.430    -3.89      -1.50      -2.48
Blend 30d+90d+EWMA0.97       0.469    -3.78      -1.31      -2.32

Vol-target tracking: realised vol of buy & hold sized to 40% with each estimator
estimator                    2016   2017   2018   2019   2020   2021   2022   2023   2024   2025    MAE
30d rolling (Option A)        38%    50%    41%    47%    49%    42%    43%    40%    43%    41%   3.9%
90d rolling                   38%    49%    41%    42%    47%    42%    40%    39%    43%    41%   2.8%
EWMA 0.94                     36%    44%    38%    43%    46%    41%    40%    38%    41%    40%   2.4%
EWMA 0.97                     36%    46%    38%    41%    46%    41%    39%    39%    42%    40%   2.4%
Blend 30d+90d+EWMA0.97        36%    49%    39%    43%    47%    42%    40%    39%    42%    41%   3.0%

Option A blend sized with each estimator (does better vol tracking change results?)
scheme                                          CAGR Sharpe   MaxDD  Expo  RT/yr
Option A, 30d rolling (Option A)               54.5%   1.63  -36.7%   40%    3.3
Option A, 90d rolling                          53.9%   1.62  -32.5%   38%    2.3
Option A, EWMA 0.94                            47.2%   1.54  -35.5%   39%    3.1
Option A, EWMA 0.97                            51.0%   1.63  -33.2%   38%    2.6
Option A, Blend 30d+90d+EWMA0.97               54.0%   1.65  -33.5%   39%    2.7
```
