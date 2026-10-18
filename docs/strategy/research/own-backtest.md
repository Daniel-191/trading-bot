# Own sanity-check backtest of candidate BTC strategies (daily bars, 2015 to May 2026)

These notes come from our own analysis, not from published research. The research tracks could only see search summaries of published results, and none of them tested the candidates side by side on the same data with our costs. This backtest does that, so we have one consistent comparison of the shortlisted rules.

## Method
- **Data:** Coin Metrics Community Data, `csv/btc.csv` (daily `PriceUSD`, a cross-exchange reference rate at 00:00 UTC, plus `CapMVRVCur`). It runs to 2026-05-23. Source: https://github.com/coinmetrics/data. SHA-256 of the file used: `06495ff8e643432e6948b7b4686ce44fc106217287dabdc1b38351d9ddec46c3`. Binance and other exchange hosts were blocked from this environment, so the backtest could not use data.binance.vision. The bot's real backtester should use Binance klines.
- **Script:** `btc_backtest.py` in this folder. Run it with `uv run --no-project --with pandas --with numpy python -I btc_backtest.py btc.csv`. It is research scratch code, not part of the bot.
- **Execution:** the target weight is decided on the close of day t and earns the return from t to t+1. BTC trades 24/7, so the close of t is the open of t+1. A variant with one extra day of lag is also reported.
- **Positions:** long or flat only, spot, no leverage (0 ≤ w ≤ 1). Idle USDT earns 0%.
- **Costs:** 0.15% per side, made up of the 0.10% taker fee plus 0.05% slippage. Sensitivity runs at 0.05% and 0.30% per side.
- **Rebalance band:** volatility-scaled positions only trade when the target moves by at least 10 percentage points from the drifted weight.
- **Parameters:** chosen in advance from the literature, not optimised. Each ensemble is an equal-weight average of 0/1 sub-signals:
  - MA ensemble: price above its 20/50/100/200-day SMAs (Detzel et al. style).
  - TSMOM ensemble: positive 30/60/90/180/365-day return.
  - Donchian ensemble: lookbacks 10/20/40/80/160 days. Enter on a new closing high over the lookback; exit on a new closing low over half the lookback (Concretum/Turtle style).
  - Vol target: weight = signal × min(1, target ÷ 30-day realised vol).
  - RSI(2) rule: Connors' version, buying when RSI(2) < 10 above the 200-day SMA and exiting above the 5-day SMA.
  - MVRV overlay: hold, but go flat while MVRV > 3.
- **Variants:** about 12 strategy variants plus two parameter sweeps (SMA lengths and Donchian lookbacks). Count these toward N when deflating any Sharpe ratio.
- **Bootstrap:** block bootstrap (30-day blocks, 2,000 resamples). P(Sharpe ≤ benchmark) is the share of resamples in which the strategy's Sharpe did not beat the benchmark's. It is a rough one-sided p-value, not adjusted for multiple testing.

## Caveats
- **In-sample:** most of these rules were published using pre-2021 BTC data, so only 2022 onwards, and especially 2024 onwards, is out-of-sample relative to the literature.
- **Data:** daily closes only, so there is no intrabar stop simulation and no wick risk. Coin Metrics prices are a reference rate, not Binance BTC/USDT fills.
- **Not modelled:** taxes, and interest on idle USDT. Idle cash earning yield would help the strategies with low exposure.

## Key results
- **Full period, 2015-01-01 to 2026-05-23:**
  - Buy-and-hold: Sharpe 1.06, max drawdown −83.8%, CAGR 61.9%.
  - Trend ensembles: Sharpe 1.31–1.58, max drawdown −24% to −63%, CAGR 32–67%.
  - Turnover: about 3–9 round trips a year.
- **ETF era, 2024-01-11 onwards:**
  - Buy-and-hold: Sharpe 0.68, max drawdown −49%.
  - Trend ensembles: Sharpe 0.61–0.89, max drawdown −16% to −29%.
  - The Sharpe advantage has mostly gone; the drawdown reduction remains.
- **TSMOM ensemble at a 40% vol target** was the best performer in the ETF era: Sharpe 0.89, max drawdown −21%, CAGR 23.4% against 23.5% for buy-and-hold.
- **Costs barely matter at this turnover.** Moving from 0.05% to 0.30% per side changes the full-period Sharpe by 0.10 at most.
- **Bootstrap against the volatility-targeted buy-and-hold benchmark** (holding BTC sized to the same volatility target, which separates the value of timing from simply holding less BTC):
  - Donchian ensemble at a 40% vol target: p ≈ 0.03.
  - Other ensembles: p ≈ 0.10–0.19.
  - None clears a t ≈ 3 bar once the number of variants tried is accounted for.
- **Robustness to lookback:** single-SMA Sharpe is 1.23–1.40 for every length from 30 to 150 days. The 200-day SMA is among the weakest at 1.16. Single Donchian lookbacks of 20–80 days score 1.20–1.40. There is a broad plateau, so no single value has to be picked precisely.
- **Mean reversion on daily bars fails:** the RSI(2) dip-buy above the 200-day SMA has a full-period Sharpe of 0.28 and a CAGR of 3.9%.
- **The MVRV > 3 exit hurt returns:** CAGR 47.8% against 61.9% for buy-and-hold. It exited the 2021 bull run too early. MVRV peaked at only 2.78 (2024-03-11) in the 2023–2026 cycle, so the rule never fired, consistent with Grobys (2026).
- **Bear markets:**
  - 2018: buy-and-hold −72.7%; Donchian ensemble at a 40% vol target −11.5%.
  - 2022: buy-and-hold −65.3%; trend ensembles −14% to −32%; the 200-day SMA rule was flat all year (0%).
- **Median realised BTC volatility (30-day, annualised)** has fallen from mostly 0.55–0.9 (2015–2022, apart from 0.40 in 2016) to about 0.40–0.50 (2023–2026). A 40% vol target therefore now holds close to a full position whenever the signal is on.

## Full output
```
Data: 2013-01-01 to 2026-05-23  cost/side=0.15% band=0.1

=== FULL 2015-01-01 to end ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                             61.9%  67.1%   1.06  -83.8%   0.74   100%    0.0     243.0x
Buy & hold, vol-target 40%             45.8%  43.4%   1.09  -65.1%   0.70    72%    1.6      73.7x
200d SMA filter                        60.3%  52.1%   1.16  -68.0%   0.89    61%    3.1     216.5x
MA ensemble (20/50/100/200)            65.9%  45.0%   1.35  -56.5%   1.17    57%    9.2     320.7x
TSMOM ensemble (30-365d)               67.1%  48.0%   1.31  -63.2%   1.06    62%    5.9     347.6x
Donchian ensemble (10-160d)            58.8%  38.5%   1.39  -47.7%   1.23    45%    5.6     194.5x
Donchian ensemble, vol-target 40%      43.5%  26.2%   1.51  -33.4%   1.30    33%    4.3      61.6x
Donchian ensemble, vol-target 25%      31.6%  18.5%   1.58  -23.6%   1.34    23%    2.8      22.9x
TSMOM ensemble, vol-target 40%         44.3%  31.2%   1.33  -41.0%   1.08    45%    4.9      65.5x
RSI(2) dip-buy above 200d SMA           3.9%  25.9%   0.28  -37.1%   0.10     9%    8.8       1.5x
Buy & hold, flat when MVRV>3           47.8%  63.7%   0.94  -78.7%   0.61    95%    1.4      86.1x
Donchian ens. + RSI2 dips (max)        62.4%  45.2%   1.30  -57.7%   1.08    51%    9.2     252.3x

=== Binance era 2017-08-17 to end ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                             38.8%  66.9%   0.83  -83.8%   0.46   100%    0.1      17.8x
Buy & hold, vol-target 40%             31.0%  43.1%   0.84  -65.1%   0.48    71%    1.5      10.7x
200d SMA filter                        36.2%  50.1%   0.87  -68.0%   0.53    56%    3.8      15.0x
MA ensemble (20/50/100/200)            49.8%  43.4%   1.15  -56.5%   0.88    54%    9.7      34.6x
TSMOM ensemble (30-365d)               48.2%  46.3%   1.08  -63.2%   0.76    59%    6.5      31.6x
Donchian ensemble (10-160d)            43.7%  37.0%   1.16  -47.7%   0.92    42%    5.9      24.1x
Donchian ensemble, vol-target 40%      31.1%  24.3%   1.23  -33.4%   0.93    30%    4.5      10.7x
Donchian ensemble, vol-target 25%      21.5%  16.8%   1.24  -23.6%   0.91    20%    2.8       5.5x
TSMOM ensemble, vol-target 40%         30.7%  29.3%   1.06  -41.0%   0.75    43%    5.2      10.5x
RSI(2) dip-buy above 200d SMA           1.5%  24.9%   0.19  -37.1%   0.04     9%    8.8       1.1x
Buy & hold, flat when MVRV>3           25.2%  63.3%   0.68  -78.7%   0.32    95%    1.1       7.2x
Donchian ens. + RSI2 dips (max)        43.8%  43.5%   1.05  -57.7%   0.76    48%    9.5      24.2x

=== 2018 bear (2018-01-01..2018-12-31) ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                            -72.7%  82.9%  -1.14  -81.4%  -0.89   100%    0.5       0.3x
Buy & hold, vol-target 40%            -48.9%  40.8%  -1.44  -55.2%  -0.89    57%    1.3       0.5x
200d SMA filter                       -53.4%  52.4%  -1.19  -63.3%  -0.84    19%    3.0       0.5x
MA ensemble (20/50/100/200)           -35.4%  31.4%  -1.23  -46.2%  -0.76    23%    8.8       0.6x
TSMOM ensemble (30-365d)              -43.6%  43.8%  -1.08  -55.5%  -0.78    40%    9.1       0.6x
Donchian ensemble (10-160d)           -24.6%  19.7%  -1.33  -32.3%  -0.76    13%    4.2       0.8x
Donchian ensemble, vol-target 40%     -11.5%   9.0%  -1.32  -14.2%  -0.81     7%    2.1       0.9x
Donchian ensemble, vol-target 25%      -8.0%   5.5%  -1.49   -9.8%  -0.82     4%    1.3       0.9x
TSMOM ensemble, vol-target 40%        -27.2%  18.4%  -1.64  -32.2%  -0.85    22%    6.1       0.7x
RSI(2) dip-buy above 200d SMA         -13.4%  34.0%  -0.25  -31.8%  -0.42     6%    4.0       0.9x
Buy & hold, flat when MVRV>3          -69.0%  82.4%  -1.00  -78.7%  -0.88    99%    1.5       0.3x
Donchian ens. + RSI2 dips (max)       -31.0%  38.8%  -0.76  -39.4%  -0.79    18%    7.1       0.7x

=== 2019-2021 (incl. Covid crash, bull) ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                            129.7%  74.4%   1.50  -61.4%   2.11   100%    0.2      12.2x
Buy & hold, vol-target 40%             83.4%  46.3%   1.54  -43.4%   1.92    63%    1.9       6.2x
200d SMA filter                        53.6%  57.9%   1.03  -62.2%   0.86    67%    4.3       3.6x
MA ensemble (20/50/100/200)           107.1%  52.7%   1.64  -37.5%   2.85    63%    9.5       8.9x
TSMOM ensemble (30-365d)              100.5%  54.7%   1.55  -48.5%   2.07    68%    5.8       8.1x
Donchian ensemble (10-160d)            95.4%  45.4%   1.70  -29.1%   3.28    49%    5.6       7.5x
Donchian ensemble, vol-target 40%      64.2%  29.2%   1.84  -16.4%   3.92    31%    3.9       4.4x
Donchian ensemble, vol-target 25%      48.5%  20.7%   2.02  -11.2%   4.33    21%    2.1       3.3x
TSMOM ensemble, vol-target 40%         57.9%  33.9%   1.51  -33.4%   1.73    43%    4.2       3.9x
RSI(2) dip-buy above 200d SMA          -0.6%  26.3%   0.11  -35.1%  -0.02    10%    9.3       1.0x
Buy & hold, flat when MVRV>3           90.0%  69.8%   1.28  -61.4%   1.46    91%    0.8       6.9x
Donchian ens. + RSI2 dips (max)        88.4%  51.4%   1.49  -45.0%   1.97    56%    9.9       6.7x

=== 2022 bear ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                            -65.3%  63.7%  -1.34  -66.8%  -0.98   100%    0.5       0.3x
Buy & hold, vol-target 40%            -55.6%  43.0%  -1.67  -55.8%  -1.00    68%    2.1       0.4x
200d SMA filter                         0.0%   0.0%    nan    0.0%    nan     0%    0.0       1.0x
MA ensemble (20/50/100/200)           -31.1%  16.4%  -2.18  -32.7%  -0.95    16%    8.3       0.7x
TSMOM ensemble (30-365d)              -32.0%  12.8%  -2.94  -31.9%  -1.00    15%    7.4       0.7x
Donchian ensemble (10-160d)           -30.5%  16.1%  -2.19  -30.8%  -0.99    20%    5.8       0.7x
Donchian ensemble, vol-target 40%     -22.7%  11.0%  -2.27  -22.7%  -1.00    13%    3.9       0.8x
Donchian ensemble, vol-target 25%     -14.4%   7.8%  -1.95  -14.7%  -0.98     9%    2.2       0.9x
TSMOM ensemble, vol-target 40%        -27.4%   9.7%  -3.26  -27.4%  -1.00    11%    5.5       0.7x
RSI(2) dip-buy above 200d SMA           0.0%   0.0%    nan    0.0%    nan     0%    0.0       1.0x
Buy & hold, flat when MVRV>3          -65.3%  63.7%  -1.34  -66.8%  -0.98   100%    0.5       0.3x
Donchian ens. + RSI2 dips (max)       -30.5%  16.1%  -2.19  -30.8%  -0.99    20%    5.8       0.7x

=== 2023-01-01 to end ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                             56.8%  46.9%   1.19  -49.1%   1.16   100%    0.1       4.6x
Buy & hold, vol-target 40%             52.1%  39.9%   1.25  -46.0%   1.13    87%    1.2       4.2x
200d SMA filter                        36.0%  38.6%   0.99  -32.0%   1.12    69%    5.0       2.8x
MA ensemble (20/50/100/200)            37.1%  32.9%   1.12  -29.4%   1.26    62%   11.2       2.9x
TSMOM ensemble (30-365d)               42.5%  33.7%   1.22  -25.7%   1.65    66%    6.7       3.3x
Donchian ensemble (10-160d)            26.6%  27.0%   1.01  -25.0%   1.07    46%    6.6       2.2x
Donchian ensemble, vol-target 40%      24.7%  23.1%   1.07  -18.5%   1.34    40%    5.9       2.1x
Donchian ensemble, vol-target 25%      16.0%  16.0%   1.01  -16.0%   1.00    28%    4.0       1.7x
TSMOM ensemble, vol-target 40%         38.3%  28.9%   1.27  -21.2%   1.80    58%    6.2       3.0x
RSI(2) dip-buy above 200d SMA          12.3%  18.7%   0.72  -23.0%   0.54    12%   12.1       1.5x
Buy & hold, flat when MVRV>3           56.8%  46.9%   1.19  -49.1%   1.16   100%    0.1       4.6x
Donchian ens. + RSI2 dips (max)        36.1%  32.0%   1.12  -28.3%   1.28    54%   11.2       2.8x

=== ETF era 2024-01-11 to end ===
strategy                                CAGR    Vol Sharpe   MaxDD Calmar   Expo  RT/yr       Mult
Buy & hold                             23.5%  47.9%   0.68  -49.1%   0.48   100%    0.2       1.6x
Buy & hold, vol-target 40%             22.9%  39.6%   0.72  -46.0%   0.50    84%    1.2       1.6x
200d SMA filter                        12.6%  37.1%   0.51  -32.0%   0.39    64%    6.3       1.3x
MA ensemble (20/50/100/200)            17.2%  31.1%   0.66  -29.4%   0.58    57%   11.9       1.5x
TSMOM ensemble (30-365d)               24.2%  33.4%   0.81  -25.7%   0.94    63%    7.4       1.7x
Donchian ensemble (10-160d)            13.0%  25.3%   0.61  -25.0%   0.52    41%    6.6       1.3x
Donchian ensemble, vol-target 40%      14.4%  21.5%   0.73  -18.3%   0.78    36%    5.8       1.4x
Donchian ensemble, vol-target 25%       8.7%  15.2%   0.63  -16.0%   0.55    25%    4.0       1.2x
TSMOM ensemble, vol-target 40%         23.4%  28.1%   0.89  -21.2%   1.10    55%    6.5       1.6x
RSI(2) dip-buy above 200d SMA          10.3%  19.3%   0.60  -23.0%   0.45    11%   11.4       1.3x
Buy & hold, flat when MVRV>3           23.5%  47.9%   0.68  -49.1%   0.48   100%    0.2       1.6x
Donchian ens. + RSI2 dips (max)        20.6%  31.0%   0.76  -28.3%   0.73    48%   11.3       1.6x

=== Robustness on FULL period ===
200d SMA filter                      +1d lag Sharpe 1.19 | cost 0.05%/side 1.18 | 0.30%/side 1.15 | P(Sharpe<=B&H) 0.39 | P(Sharpe<=VT B&H) 0.47
MA ensemble (20/50/100/200)          +1d lag Sharpe 1.35 | cost 0.05%/side 1.39 | 0.30%/side 1.29 | P(Sharpe<=B&H) 0.08 | P(Sharpe<=VT B&H) 0.16
TSMOM ensemble (30-365d)             +1d lag Sharpe 1.28 | cost 0.05%/side 1.33 | 0.30%/side 1.27 | P(Sharpe<=B&H) 0.06 | P(Sharpe<=VT B&H) 0.19
Donchian ensemble (10-160d)          +1d lag Sharpe 1.31 | cost 0.05%/side 1.42 | 0.30%/side 1.35 | P(Sharpe<=B&H) 0.06 | P(Sharpe<=VT B&H) 0.13
Donchian ensemble, vol-target 40%    +1d lag Sharpe 1.36 | cost 0.05%/side 1.54 | 0.30%/side 1.46 | P(Sharpe<=B&H) 0.03 | P(Sharpe<=VT B&H) 0.03
TSMOM ensemble, vol-target 40%       +1d lag Sharpe 1.32 | cost 0.05%/side 1.36 | 0.30%/side 1.29 | P(Sharpe<=B&H) 0.10 | P(Sharpe<=VT B&H) 0.10
RSI(2) dip-buy above 200d SMA        +1d lag Sharpe 0.17 | cost 0.05%/side 0.35 | 0.30%/side 0.18 | P(Sharpe<=B&H) 0.99 | P(Sharpe<=VT B&H) 0.99

=== Parameter plateau, FULL period: single SMA filter length ===
SMA  20:   54.7%  45.6%   1.18  -65.0%   0.84    55%   19.2     144.7x
SMA  30:   60.9%  46.6%   1.25  -61.2%   1.00    56%   14.5     226.7x
SMA  50:   70.6%  47.9%   1.35  -63.2%   1.12    57%    9.0     442.3x
SMA  75:   62.2%  49.1%   1.23  -58.3%   1.07    57%    7.3     247.4x
SMA 100:   64.6%  50.4%   1.24  -63.9%   1.01    58%    6.3     293.8x
SMA 125:   78.8%  50.8%   1.40  -62.4%   1.26    59%    3.6     754.5x
SMA 150:   72.3%  51.1%   1.32  -62.6%   1.15    60%    3.5     493.7x
SMA 200:   60.3%  52.1%   1.16  -68.0%   0.89    61%    3.1     216.5x
SMA 250:   60.1%  53.8%   1.14  -65.1%   0.92    65%    3.4     213.1x
SMA 300:   60.6%  54.8%   1.14  -71.2%   0.85    67%    3.0     221.5x

=== Parameter plateau, FULL period: single Donchian lookback (exit = lb/2) ===
Donchian  10:   43.9%  40.7%   1.10  -62.8%   0.70    42%   15.3      63.4x
Donchian  20:   59.5%  41.7%   1.33  -61.2%   0.97    43%    7.2     204.3x
Donchian  30:   65.6%  42.4%   1.40  -55.6%   1.18    43%    4.6     313.9x
Donchian  40:   63.7%  43.7%   1.34  -47.5%   1.34    44%    3.6     275.3x
Donchian  60:   55.1%  44.4%   1.21  -58.6%   0.94    43%    2.5     148.6x
Donchian  80:   55.3%  45.1%   1.20  -48.8%   1.13    43%    2.0     150.9x
Donchian 120:   56.8%  49.3%   1.16  -68.6%   0.83    48%    1.1     168.1x
Donchian 160:   53.7%  48.5%   1.13  -65.2%   0.82    51%    0.9     134.5x
Donchian 250:   46.9%  50.6%   1.01  -75.4%   0.62    55%    0.6      80.1x

=== MVRV context ===
MVRV 2017-01-01..2018-12-31: max 4.72 on 2017-12-07, min 0.69
MVRV 2020-01-01..2022-12-31: max 3.96 on 2021-02-21, min 0.75
MVRV 2023-01-01..end: max 2.78 on 2024-03-11, min 0.84

=== Realised BTC vol (30d, annualised) by year: median ===
time
2015    0.58
2016    0.40
2017    0.89
2018    0.73
2019    0.65
2020    0.55
2021    0.72
2022    0.62
2023    0.42
2024    0.50
2025    0.40
2026    0.42
```
