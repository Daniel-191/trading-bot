# Validating, Sizing and Risk-Managing a Single-Asset Systematic BTC Strategy (Retail, Non-HFT)

Research notes, October 2026. Some primary sites (freqtrade.io, binance.com, man.com, cxoadvisory.com, ams.org, davidhbailey.com, monash.edu, and the Binance REST API) could not be reached from this research environment. Where a claim rests on a search-result summary of a page rather than the page itself, it is marked "(summary)". Statements marked "(background, unverified here)" come from general domain knowledge and should be checked before they are relied on.

## 1. Backtest overfitting and data snooping: what the literature says, how much BTC data is needed, and how to count variants

### Takeaway
The literature agrees that trying many variants on one historical path all but guarantees an impressive in-sample Sharpe with zero true edge. With about 5 years of data, roughly 45 independent tries are enough to "find" an annualised Sharpe of 1 by luck. Binance BTC/USDT history is only about 9 years, so even a true Sharpe-1 strategy barely clears the t > 3 multiple-testing bar. The team must log every variant tried and deflate results accordingly.

### Cited Findings
- **Minimum Backtest Length (MinBTL).** Bailey, Borwein, López de Prado & Zhu, "Pseudo-Mathematics and Financial Charlatanism" (Notices of the AMS, 2014): "with five years of data, no more than forty-five independent model configurations should be tried", or strategies with an in-sample annualised Sharpe of 1 and an expected out-of-sample Sharpe of 0 are almost guaranteed. The authors call the 45 figure conservative because it assumes independent trials. — [CORE record of the paper](https://core.ac.uk/display/24055290); [ScienceDaily release](https://sciencedaily.com/releases/2014/04/140410103005.htm)
- Same research line: after trying only **7 strategy configurations**, a researcher should expect at least one **2-year** backtest with an annualised Sharpe above 1 even when the true out-of-sample Sharpe is 0. — [IAQF talk abstract](https://iaqf.org/event-813217)
- Analysts rarely report how many configurations they tried, so investors cannot judge how overfit a backtest is. — [CORE record](https://core.ac.uk/display/24055290)
- More configurations raise the probability of overfitting, and more complex strategies produce more configurations. For return series with memory (autocorrelation), further in-sample optimisation can make out-of-sample performance *worse*, not just less good (summary). — [CXO Advisory on iterative backtests](https://www.cxoadvisory.com/big-ideas/insidiousness-of-overfitting-investment-strategies-via-iterative-backtests); [CXO Advisory](https://www.cxoadvisory.com/?p=23736)
- **Probability of Backtest Overfitting (PBO).** Bailey, Borwein, López de Prado & Zhu propose estimating PBO with Combinatorially Symmetric Cross-Validation (CSCV). Published in the Journal of Computational Finance, 20(4), 2017. — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253); [eScholarship PDF](https://escholarship.org/content/qt4w1110bb/qt4w1110bb.pdf)
- **Deflated Sharpe Ratio (DSR).** Bailey & López de Prado correct the Sharpe ratio for selection bias under multiple testing and for non-normal returns (skew and kurtosis). — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551)
- **Harvey, Liu & Zhu, "…and the Cross-Section of Expected Returns"** (RFS 29(1):5–68, 2016; NBER WP 20592): at least 316 factors have been tested. Given that much data mining, a new factor needs a **t-ratio above 3.0** rather than the usual 2.0, and "most claimed research findings in financial economics are likely false." — [SSRN 2513152](https://papers.ssrn.com/abstract=2513152); [NBER w20592](https://www.nber.org/papers/w20592)
- **Harvey & Liu, "Backtesting"** (JPM 41(1), 2015): applying the industry rule-of-thumb **50% Sharpe haircut** mechanically is "a serious mistake". The correct haircut is **nonlinear**: high Sharpe ratios are penalised moderately and marginal ones heavily. — [Harvey & Liu PDF (Duke)](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)
  - Worked example from the paper as reported: a Sharpe of 0.75 after accounting for 200 tests adjusts to 0.32, about a **60% haircut**. — [Advisor Perspectives](https://www.advisorperspectives.com/articles/2016/04/28/special-edition-can-you-trust-investment-research)
  - A secondary summary reports that for annualised Sharpe < 0.4 the haircut is almost always above 50%, and for Sharpe > 1.0 it is at most about 25% (summary, not checked against the paper). — [CXO Advisory, "Navigating the data-snooping icebergs"](https://www.cxoadvisory.com/big-ideas/navigating-the-data-snooping-icebergs/)
- **White's Reality Check / Hansen's SPA.** Both build a null distribution with a stationary bootstrap over the *entire* set of rules tried, so choosing the best rule doesn't inflate significance. SPA is generally the more powerful test. — [MetricGate docs (vendor explanation)](https://metricgate.com/docs/reality-check-superior-predictive-ability/)
  - Applied to technical rules on US futures (1985–2004), the best rules were significantly profitable for only **2 of 17** contracts after correcting for data snooping. — [AgEcon Search record 19039](https://ageconsearch.umn.edu/record/19039)
  - Applied to equity indices, simple rules were significant in "young" markets (NASDAQ Composite, Russell 2000) but not in "mature" ones (DJIA, S&P 500). — [Re-examining technical analysis with White's RC and Hansen's SPA (PDF)](https://c.mql5.com/forextsd/forum/211/Re-Examining%20the%20Profitability%20of%20Technical%20Analysis%20with%20Whitets%20Reality%20Check%20and%20Hansen9s%20SPA%20Tes.pdf)
- **Arnott, Harvey & Markowitz, "A Backtesting Protocol in the Era of Machine Learning"** (JFDS 1(1):64–74, 2019). Themes as summarised by Alpha Architect (summary):
  - avoid cherry-picking samples and ad hoc data cleaning;
  - there is effectively no true out-of-sample period other than live trading and fresh data;
  - don't tweak a model in response to live results;
  - doubt whether you have enough data to justify extra complexity ("Probably not");
  - reward good research process rather than good results.
  — [SSRN 3275654](https://papers.ssrn.com/abstract=3275654); [Alpha Architect summary](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/); [Research Affiliates listing](https://www.researchaffiliates.com/insights/journal-papers/702-a-backtesting-protocol-in-the-era-of-machine-learning)
- **Quantopian, "All that Glitters Is Not Gold"** (Wiecki, Campbell, Lent & Stauth, 2016): studied 888 algorithms with at least 6 months of out-of-sample trading.
  - Backtest Sharpe had almost no power to predict out-of-sample Sharpe (**R² < 0.025**).
  - The more backtests a quant ran on a strategy, the bigger the gap between backtest and out-of-sample results.
  - Volatility and max drawdown *did* have significant predictive value.
  - A non-linear classifier reached R² = 0.17 on hold-out data.
  — [Quantpedia summary](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)
- Andrew Lo, "The Statistics of Sharpe Ratios" (2002): serial correlation in monthly returns can overstate annualised Sharpe by up to **65%**. — [Lo (2002) PDF](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf)
- Rob Carver (via a review of *Smart Portfolios*):
  - Sharpe estimates are so uncertain that they are "effectively worthless". The 95% confidence range for the relative Sharpe of US stocks vs bonds is about 0.5 Sharpe units.
  - Volatility estimates are far more precise than Sharpe estimates.
  — [Harriman House review](https://harriman.house/?p=1770071)

### Inferences
- **Years of data needed (arithmetic, using Lo's IID approximation SE(annual SR) ≈ 1/√years).** The t-stat is roughly annual Sharpe × √years.

  | True annual Sharpe | Years for t = 2 | Years for t = 3 (HLZ bar) |
  |---|---|---|
  | 1.0 | 4 | 9 |
  | 0.5 | 16 | 36 |

  Binance BTC/USDT spot history starts around August 2017 (see Gaps), giving about **9 years** by October 2026. So **only a strategy with a true Sharpe of about 1 or more can clear t ≈ 3, and only if essentially no variants were tried.** Fat tails, which are typical of BTC, widen the error further; DSR handles that.
- **How many variants can you afford?** For N roughly independent zero-edge variants, the expected best in-sample Sharpe is about SE × √(2 ln N) (background, unverified here; this is the logic behind MinBTL). With 5 years (SE ≈ 0.45):
  - N = 45 gives a best Sharpe of about 1, which matches Bailey et al.
  - N = 1,000 gives about 1.7.
  - Hyperopt-style searches over thousands of parameter combinations can therefore produce Sharpe 1.5–2 backtests on noise.
- **Trades needed (arithmetic).** Per-trade t-stat = (mean trade return ÷ std of trade returns) × √N_trades.
  - A trend system with a per-trade mean/sd of about 0.1 needs about 400 trades for t = 2 and about 900 for t = 3.
  - At mean/sd ≈ 0.2 it needs about 100 trades for t = 2 and 225 for t = 3.
  - Daily-bar BTC trend systems often trade only 10–40 times a year, so 9 years gives roughly 90–360 trades, which is borderline. Hourly systems generate more trades but pay far more in fees (section 4).
- **Counting variants (practical rule).** Log every backtest run in an append-only research journal: strategy family, parameters, timeframe, filters, date range, and result. Count every:
  - parameter combination evaluated (including each hyperopt epoch);
  - indicator or filter swapped in or out;
  - timeframe tried;
  - "small tweak after looking at results".

  Use the total (or the number of clusters of highly correlated variants) as N in DSR and Harvey-Liu haircuts. Quantopian's finding that more backtesting leads to a bigger live gap is the empirical reason to do this.
- **Reporting:** report DSR (or the Harvey-Liu-adjusted Sharpe) alongside the raw Sharpe, and treat a raw Sharpe below about 0.5 as noise for a single-asset strategy (consistent with the large haircuts for low Sharpe ratios).

### Gaps
- I could not open the AMS/SSRN PDFs to quote the exact MinBTL and DSR formulas. The formulas above come from background knowledge and need checking against [SSRN 2460551](https://papers.ssrn.com/abstract=2460551) and the Notices paper.
- I could not confirm the original Sullivan-Timmermann-White (1999) Reality Check results on technical rules. Only later studies were found.
- I found no BTC-specific published estimate of "trades required". The figures above are arithmetic illustrations.

## 2. Validation methods: walk-forward, purged/embargoed CV and CPCV, holdout, parameter stability, Monte Carlo, cross-asset and regime tests, and which suit a small team

### Takeaway
Use a layered protocol:
- a locked final holdout;
- walk-forward (or, more rigorously, CPCV/CSCV) for model selection, with PBO and DSR computed;
- parameter-plateau checks;
- regime-split and ETH robustness checks;
- a Monte Carlo trade-reshuffle for drawdown distributions.

All are feasible for a two-person team on a single asset. CPCV is the most rigorous but the most work; walk-forward plus a holdout plus DSR is the pragmatic minimum.

### Cited Findings
- **Walk-forward** produces a single historical path, and a lucky or unlucky path looks identical to a robust one.
- **CPCV** splits the data into contiguous groups and tests every combination of held-out groups. This gives many out-of-sample paths, from which you can estimate a *distribution* of out-of-sample Sharpe and the PBO.
- Example: N = 6 groups with k = 2 test groups gives C(6,2) = 15 train/test splits. Sources differ on how many distinct paths that yields.

— [Wikipedia: Purged cross-validation](https://en.wikipedia.org/wiki/Purged_cross-validation); [dev.to walk-forward vs López de Prado](https://dev.to/shaktitiwari/walk-forward-testing-for-trading-models-the-honest-method-lopez-de-prado-165j)
- **Purging and embargo.** Purging drops training rows whose labels overlap the test window. An embargo adds a gap after the test window because purging alone does not remove serial correlation. A cited rule of thumb is an embargo of about **1% of the bars in the test set** (secondary course material). — [Wikipedia](https://en.wikipedia.org/wiki/Purged_cross-validation); [TradingInterview course](https://www.tradinginterview.com/courses/machine-learning/lessons/cross-validation-for-financial-data-purging-and-embargoing/)
- An applied CPCV example: 10 training folds and 8 test folds give 36 backtest paths and 45 training combinations, with a 21-day purge/embargo. — [arXiv 2407.17645](https://arxiv.org/pdf/2407.17645)
- CPCV is attributed to López de Prado, *Advances in Financial Machine Learning* (2018), ch. 7. Some sources date it to 2017. — [Wikipedia](https://en.wikipedia.org/wiki/Purged_cross-validation)
- PBO via CSCV (section 1) is designed to estimate the probability that the in-sample-best configuration underperforms the median configuration out of sample. — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253)
- Arnott-Harvey-Markowitz: the only true out-of-sample test is live trading or new data, and models should not be tweaked in response to live results (summary). — [Alpha Architect](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/)
- Mature-vs-young-market evidence: technical rules showed significance in "young" markets but not "mature" ones, so the edge may decay as a market matures. That argues for **regime and sub-period testing** of BTC, which has matured since 2017. — [Hsu-Kuan-style SPA study (PDF)](https://c.mql5.com/forextsd/forum/211/Re-Examining%20the%20Profitability%20of%20Technical%20Analysis%20with%20Whitets%20Reality%20Check%20and%20Hansen9s%20SPA%20Tes.pdf)
- BTC behaviour depends on time scale: one thesis (2020–2025) found mean reversion in **hourly** BTC data while momentum performed only moderately there. Results can flip with bar size, so test each timeframe as a separate hypothesis (and count it as a variant). — [Theseus thesis](https://www.theseus.fi/handle/10024/902903)
- Zarattini, Pagani & Barbon ("Catching Crypto Trends", SFI Research Paper):
  - They developed a trend model on Bitcoin, then extended it to all coins traded since 2015 using a survivorship-bias-free dataset.
  - On a top-20 rotational portfolio it reports Sharpe > 1.5 and 10.8% annual alpha vs BTC, net of fees.
  - That is a cross-asset generalisation test in practice.
  — [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html); [author page](https://abarbon.com/papers/catching-crypto-trends)

### Inferences
- **Recommended pipeline for this team** (an inference, combining the above):
  1. **Freeze a final holdout now**, e.g. the most recent 12–18 months of BTC/USDT. Nobody looks at it until one pre-registered candidate is chosen. Use it once.
  2. On the remaining data (about Aug 2017 to mid-2025), do model selection with **anchored or rolling walk-forward**, e.g. 3-year train and 6-month test, stepping 6 months. If ML or label-based features are used, use **CPCV with purge and embargo**. Record N (all variants) and compute **PBO (CSCV)** and **DSR** on the selection set.
  3. **Plateau, not peak.** Plot performance over a grid of each parameter, e.g. MA lengths ±50%. Accept only if a broad neighbourhood is profitable. Pick the centre of the plateau, not the best cell. Reject if Sharpe collapses with ±20% parameter moves. (Practitioner convention; I found no primary citation in this session.)
  4. **Regime splits.** Report metrics separately for:
     - 2017-08 to 2018-12 (bubble and bust);
     - 2019 to 2020-Q1 (including the March 2020 crash);
     - 2020-Q2 to 2021 (bull);
     - 2022 (bear, plus LUNA and FTX);
     - 2023 to 2026 (ETF era, including the Oct 10–11, 2025 liquidation cascade).

     A strategy that makes all its money in one regime is a regime bet, not an edge.
  5. **Cross-asset robustness.** Run the *unchanged* BTC strategy on ETH/USDT (and optionally on BTC on another exchange or quote currency). This isn't for trading, just to check the logic isn't fitted to BTC's single path. Expect weaker but same-sign results.
  6. **Monte Carlo.** Reshuffle or bootstrap the trade sequence (or use a block bootstrap of daily returns to keep autocorrelation) for 1,000+ runs. Use the 95th-percentile max drawdown and the 5th-percentile CAGR for sizing and kill-switch thresholds, not the single historical max DD.
- The most practical rigorous combination for two developers is walk-forward + DSR + PBO + plateau + regime + ETH + Monte Carlo. CPCV is worth adding only if the strategy has many fitted parameters or ML components.

### Gaps
- I found no primary, citable source in this session for the "plateau not peak" heuristic or for Monte Carlo trade reshuffling (both are widespread practitioner conventions, e.g. Robert Pardo or Robot Wealth). I also found none for a published comparison of walk-forward vs CPCV on crypto.
- I could not retrieve Bitcoin-only numbers (Sharpe, max DD, fees) from the Zarattini et al. full paper.

## 3. Backtest bias checklist specific to crypto candles

### Takeaway
The biggest candle-level traps are:
- trading at the close of the bar that generated the signal (look-ahead);
- optimistic intrabar stop/target ordering on OHLC data;
- "recursive" indicators that differ with history length;
- timestamp-unit and alignment errors in Binance archive files (spot timestamps switched to **microseconds from 2025-01-01**);
- unmodelled perp funding and mark-price liquidations;
- extreme wick events such as Oct 10–11, 2025.

Mature frameworks (Freqtrade, NautilusTrader) encode explicit conservative assumptions you can copy.

### Cited Findings
- **Freqtrade backtesting assumptions** (documented):
  - "Entries happen at open-price" (of the next candle) unless custom pricing is set.
  - "Exit-signal exits happen at open-price of the consecutive candle."
  - "Stoploss exits happen exactly at stoploss price, even if low was lower."
  - Within a candle, "Low happens before high for stoploss, protecting capital first."
  - Evaluation order is exit-signal, then stoploss, then ROI, then trailing stop.
  - Backtesting "can't capture intra-candle price movement", so results are biased.
  - Stoploss exits can appear **more often in backtests** than in dry-run or live.
  - Exchange limits and precision use *current* rules because historical ones aren't available.

  — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)
- **Freqtrade `--timeframe-detail`** re-evaluates candles that have active signals or open trades on a lower timeframe (e.g. 5m) to simulate intra-candle movement. The docs suggest using it late in development "to check whether the strategy exploits backtesting assumptions". — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)
- **Freqtrade `lookahead-analysis`** chains backtests: one full baseline, then re-runs for each entry and exit on sliced data. It "compare[s] both dataframes (baseline and sliced) for any difference in columns' value and report[s] the bias". It checks 20 signals by default. Caveat: "Signals that are not triggered will not have been verified" (possible false negatives). — [Freqtrade docs: lookahead-analysis.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/lookahead-analysis.md)
- **Freqtrade `recursive-analysis`** detects indicators whose values depend on how much history is loaded (e.g. EMA or RSI seeds). It recomputes them with different `startup_candle_count` values and compares the last-row values against a benchmark built from at least about 5,000 candles. Live bots see less history than backtests, so such indicators can diverge. Zero variance is "not necessarily" the goal; enough startup candles that signals don't change is. — [Freqtrade docs: recursive-analysis.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/recursive-analysis.md)
- **NautilusTrader bar execution:**
  - Bars don't record whether the high came before the low, so the engine simulates a path, by default **Open → High → Low → Close**.
  - With `bar_adaptive_high_low_ordering`, it visits the extreme nearer the open first.
  - Orders submitted from `on_bar` arrive only *after* all four points of that bar have been processed.
  - `ts_init` must represent the bar **close**, "which prevents the complete bar from becoming visible before it formed".

  — [NautilusTrader docs: bar-based execution](https://nautilustrader.io/docs/latest/concepts/backtesting/bar-execution/)
- **Same-bar stop and target ambiguity** is a general problem:
  - On Wealth-Lab, users found stop vs limit outcomes varied between runs, and recommended worst-case (stop first) unless finer data is available.
  - NinjaTrader recommends adding a finer data series, e.g. 1-tick.

  — [Wealth-Lab forum](https://wealth-lab.com/Discussion/Stop-loss-or-take-profit-on-same-bar-6510); [NinjaTrader forum](https://forum.ninjatrader.com/forum/ninjatrader-8/strategy-development/1262218-handling-of-stop-loss-and-take-profit-levels-in-backtesting?p=1262277)
- **Binance public data (data.binance.vision) pitfalls:**
  - Spot kline timestamps are in **microseconds** from January 1, 2025 (example open time 1735689600000000). Futures examples remain in milliseconds.
  - Every zip has a `.CHECKSUM` (SHA-256) file.
  - Archived files "may be updated at a later date as a result of recently discovered issues". There was a 2022-08-08 kline fix ("Fixed inconsistent data").
  - Daily files appear the next day, and monthly files on the first Monday of the month.
  - Spot intervals run from `1s` to `1mo` (`1mo` is used instead of `1M`).
  - The README does not mention mark-price klines or funding-rate files.

  — [binance/binance-public-data README](https://github.com/binance/binance-public-data)
- **Extreme wick and outage example, Oct 10–11, 2025** (secondary crypto press; dates differ by source between Oct 10 and 11 UTC):
  - about $19B of leveraged positions liquidated across about 1.6M accounts;
  - BTC down about 14.5% within six hours after a US tariff announcement;
  - USDe briefly at about $0.66 on Binance;
  - Binance reimbursed about $283M for collateral mispricing that caused erroneous liquidations;
  - Binance says about 75% of liquidations happened before any internal system degradation, which critics dispute.

  — [Cointelegraph](https://cointelegraph.com/news/19b-crypto-market-crash-leverage-china-tariffs); [CoinGecko explainer](https://www.coingecko.com/learn/october-10-crypto-crash-explained); [The Defiant autopsy](https://thedefiant.io/newsletter/defi-daily/the-ultimate-10-10-crash-autopsy)
- **Perp funding and mark price:**
  - A third-party script citing Binance's FAQ says funding occurs every 8 hours, with a default interest component of 0.01% per interval (0.03% per day).
  - On BitMEX, the mark price already includes the upcoming funding, and liquidations occur on mark price. These are exchange-specific mechanics.

  — [TradingView script citing Binance FAQ](https://kr.tradingview.com/script/BKa9AHJx-Binance-Funding-Rates-vichtoreb); [BitMEX support](https://support.bitmex.com/hc/en-gb/articles/7160140704669-Can-a-Funding-Payment-Trigger-Liquidation)
- Kaiko reported Binance BTC liquidity "plummeted" during the October 2023 ETF-rumour volatility. Depth is not constant and vanishes in fast markets. — [FXStreet on Kaiko data](https://www.fxstreet.com/amp/cryptocurrencies/news/bitcoin-liquidity-on-binance-plummeted-during-the-etf-rumor-induced-market-rollercoaster-kaiko-202310170704)

### Inferences
Bias checklist for our backtester (derived from the above):

1. **Signal timing.** Compute signals on bar *t*'s close and fill at bar *t+1*'s open (plus slippage). Never fill at bar *t*'s close in the same step that observed it. Enforce this in code: the strategy receives only closed bars, and the broker fills on the next event (as Nautilus does).
2. **Intrabar ordering.** If stop and target are both inside one bar, assume the **stop hit first**. Fill stops at min(stop, open) when the bar gaps through the stop, not at the stop price; this is more conservative than Freqtrade's "exactly at stoploss price". Re-run on 1m data, Freqtrade's `timeframe-detail` idea, as a final check.
3. **Look-ahead and recursive tests.** Port Freqtrade's two tests:
   - (a) recompute indicators on truncated data and assert that historical values are unchanged;
   - (b) vary warm-up length and assert that signals are stable.

   Run both in CI (pytest).
4. **Timestamps.** Normalise all data.binance.vision timestamps (ms vs µs from 2025-01-01) to UTC. Align on candle *open* time. Assert continuity: no missing or duplicate bars; gaps are flagged, not forward-filled silently. Verify CHECKSUMs and re-download months that Binance has revised.
5. **Data gaps and outages.** Treat missing bars as "no trading possible" (orders can't fill). Treat exchange maintenance windows as periods when stops don't work.
6. **Wicks.** Don't assume a stop fills at its level during flash moves. Model gap-through fills. Stress-test with injected −15% to −20% intraday moves (Oct 2025 scale).
7. **Perps.** Use the **mark price** series for liquidation and margin checks and the last price for fills. Add **funding cash flows every 8h** using historical funding rates. Neither is in the kline archive per the README, so source them separately.
8. **Survivorship** is not a concern for BTC/USDT itself. Quote-asset risk (USDT) and venue risk (e.g. FTX 2022) are the BTC analogues and should be noted.
9. **Precision.** Apply historical lot and tick sizes, or conservative ones. Freqtrade uses current limits only, which is a known simplification.

### Gaps
- I could not confirm the earliest BTC/USDT kline date on data.binance.vision. The Binance API was blocked from this environment. August 2017 is widely cited (background, unverified here).
- I could not confirm from Binance's own docs where historical mark-price and funding-rate archives live, or the exact Binance liquidation formula.
- I did not verify how backtesting.py and vectorbt resolve same-bar stop/target conflicts.

## 4. Transaction costs and slippage for $1k–$50k BTC/USDT orders

### Takeaway
At retail size, **fees, not market impact, dominate costs** on Binance and Bybit BTC/USDT:
- spot taker round trip is about 0.20% (0.15% with BNB);
- perp taker round trip is about 0.10–0.11%;
- perp maker round trip is about 0.04%.

Order books near the top level are many orders of magnitude larger than $50k in calm markets, though depth vanishes in fast markets. Turnover is the edge-killer: a strategy trading daily on spot taker fees needs roughly 50% a year of gross edge just to break even.

### Cited Findings
- **Binance spot.** The regular tier is 0.10% maker and 0.10% taker. Paying fees in BNB cuts this to 0.075% (secondary sources; "policy could change"). USDC pairs have a slightly lower taker fee (0.095%). Top VIP tiers are about 0.011%/0.023% (VIP 9, requiring ≥ $4B 30-day volume); secondary sources conflict on the exact figures. — [Finhay 2026 guide](https://www.finhay.com.vn/en/phi-giao-dich-binance); [Coinspot guide](https://coinspot.io/en/analysis/binance-fees-2025-the-ultimate-guide/); [Binance support article](https://www.binance.com/es/support/articles/360033544231)
- **Binance USDT-M perps:** 0.02% maker / 0.05% taker at the base tier. — [CoinPerps comparison (2026)](https://www.coinperps.com/zh/learn/bybit-vs-binance-perpetual-futures-fees)
- **Bybit** (review citing the schedule updated **2 Sept 2026**):
  - Spot VIP 0: 0.10% maker / 0.10% taker.
  - USDT perps: 0.02% maker / **0.055%** taker.
  - VIP 5: spot 0.04%/0.05%, futures 0.01%/0.032%.
  - VIP 5 qualification: about $2M in assets, $50M 30-day spot volume, or $250M derivatives volume.

  — [Analytics Insight](https://www.analyticsinsight.net/cryptocurrency-analytics-insight/okx-vs-bybit-fees-features-crypto-trading-options-compared); [Bitsgap](https://bitsgap.com/blog/bybit-trading-fees-explained-what-it-costs)
- Bybit halved **VIP** taker fees on **USDC**-quoted spot and futures pairs from 23 March 2026; non-USDC pairs were unchanged. — [Bybit press release via AAP](https://aap.com.au/aapreleases/cision20260323ae16461)
- **Depth.** Kaiko defines market depth as buy and sell offers within 1% or 2% of mid. In October 2023, Binance BTC/USDT had about **$30M** of liquidity within 1% of mid. — [Watcher.Guru on Kaiko data](https://watcher.guru/news/bitcoin-usdt-dominates-binance-liquidity-despite-tusd-rise); [Kaiko docs](https://docs.kaiko.com/getting-started/kaiko-examples/compare-price-slippage-between-exchanges)
- Kaiko research: a **$100k** BTC sell order cost about **0.1%** slippage on the most liquid USD and USDT pairs in early March of the period studied (the context suggests 2023; the year is not explicit). — [Kaiko Research](https://research.kaiko.com/insights/the-state-of-liquidity-in-crypto-markets)
- Liquidity can collapse during volatility (Binance BTC, October 2023). — [FXStreet on Kaiko](https://www.fxstreet.com/amp/cryptocurrencies/news/bitcoin-liquidity-on-binance-plummeted-during-the-etf-rumor-induced-market-rollercoaster-kaiko-202310170704)
- Crypto trend research finds that **shorter lookbacks give higher gross Sharpe, but transaction costs from frequent rebalancing eat the profits** (Monash Centre for Financial Studies, summary). — [Monash CFS project page](https://www.monash.edu/business/mcfs/our-research/all-projects/investment-strategy/trend-following-strategies-for-crypto-investors)
- Man Group: in crypto trend following, costs cap the gains from diversification. The optimum is about 10–15 coins (summary). That is evidence that costs bind even for institutions. — [Man Group, "In Crypto We Trend"](https://www.man.com/insights/in-crypto-we-trend)
- Freqtrade applies fees on both entry and exit using the exchange default fee via CCXT. `--fee` overrides it, e.g. 0.001 = 0.1%. — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)

### Inferences
- **Break-even arithmetic** (round-trip cost × round trips per year = annual drag):

  | Venue / order type | Round-trip fee | 12 RT/yr | 50 RT/yr | 250 RT/yr |
  |---|---|---|---|---|
  | Spot taker (0.10% × 2) | 0.20% | 2.4% | 10% | 50% |
  | Spot taker with BNB (0.075% × 2) | 0.15% | 1.8% | 7.5% | 37.5% |
  | Perp taker, Binance (0.05% × 2) | 0.10% | 1.2% | 5% | 25% |
  | Perp maker (0.02% × 2) | 0.04% | 0.5% | 2% | 10% |

  Add slippage. A conservative backtest assumption for $1k–$50k market orders in normal conditions is about 0.01–0.05% per side, and 0.1–0.5%+ per side on stop orders in fast markets. These are my modelling suggestions, supported only by the Kaiko $100k ≈ 0.1% data point and its depth figures.
- **Break-even test.** For a strategy with average gross return per trade *g* and round-trip cost *c*, net edge = *g* − *c*. Report the "cost to break even" (the *c* at which net Sharpe hits 0) as a headline robustness metric. Prefer strategies whose break-even cost is at least 3× the expected real cost.
- **Size vs depth.** $50k is under 0.2% of the 2023 1%-depth figure, so impact is negligible in calm markets. The real slippage risk is **stops during cascades** (Oct 2025), when depth evaporates.
- **Maker-only trade-offs** (background, unverified here). Post-only limit orders save about 0.06–0.08% per side on perps and get a lower rate on some spot tiers. The costs:
  - adverse selection: you get filled when price moves through you, and miss fills when it runs away;
  - missed breakout entries, which are exactly the profitable trades for trend systems.

  The backtester should model maker fills only when price trades *through* the limit, not merely touches it, and count missed fills.
- At $1k–$50k with low turnover, VIP tiers are unreachable (Bybit VIP 5 needs $50M of monthly spot volume), so budget for base-tier fees.

### Gaps
- I found no 2025–2026 Kaiko figure for Binance or Bybit BTC/USDT 1% depth or typical bid-ask spread. The 2023 figures are the latest found.
- I could not open Binance's official fee page to confirm 2026 base and BNB-discount rates. They match the team's stated assumptions, but treat them as unverified.
- I found no published study of maker-only fill rates and adverse selection for retail BTC bots.

## 5. Position sizing: fixed fractional, volatility targeting, Kelly and fractional Kelly, caps, and leverage

### Takeaway
Volatility targeting (size = target vol ÷ forecast vol, capped) has the strongest evidence for risk assets. It tends to raise Sharpe and thin the left tail, and volatility is far easier to forecast than returns. Full Kelly is dangerous because it needs a precise estimate of edge, which backtests can't provide; use at most about ¼–½ Kelly as a ceiling, not a target. On spot, unlevered long-only sizing is naturally capped at 100% of equity. Perps add liquidation risk that should be avoided or kept at ≤ 1–2× notional.

### Cited Findings
- **Moreira & Muir**, "Volatility-Managed Portfolios" (JF 72(4):1611–1644, 2017): scaling exposure by the inverse of the prior month's realised variance produces large alphas, higher Sharpe ratios and utility gains across market, value, momentum, profitability, ROE, investment, BAB and FX carry factors. — [NBER w22208](https://www.nber.org/papers/22208)
- **Harvey, Hoyle, Korgaonkar, Rattray, Sargaison & Van Hemert**, "The Impact of Volatility Targeting" (JPM 45(1), 2018), covering 60+ assets with data from 1926 to 2017:
  - vol targeting improves Sharpe for **risk assets** (equities, credit), with negligible effect for bonds, FX and commodities;
  - it "consistently reduces the likelihood of extreme returns (and the volatility of volatility)" across all assets;
  - left-tail events are less severe because they tend to happen when vol is high, when a vol-targeted portfolio holds less.

  — [Alpha Architect summary](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/); [Quantpedia](https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies)
- Crypto application: Zarattini, Pagani & Barbon combine Donchian trend signals with **volatility-based position sizing** in their crypto trend model. — [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html)
- **Volatility is more estimable than mean return.** Carver argues Sharpe estimates are near-useless while vol estimates are precise, which justifies risk-weighting. Hentschel (2026) makes the same point: expected returns are learned slowly in calendar time, volatility quickly. — [Harriman House review of Carver](https://harriman.house/?p=1770071); [Hentschel 2026 WP](https://www.ludgerhentschel.com/PDFs/Hentschel%20'26d.pdf)
- **Kelly:**
  - MacLean, Thorp & Ziemba document "good and bad properties" of Kelly and fractional Kelly. A related study finds a consistent growth-vs-security trade-off and that "the short term performance of Kelly and high fractional Kelly strategies is very risky".
  - In one Ziemba simulation, half Kelly loses half of wealth only **1%** of the time vs **8.4%** for full Kelly (presentation slides; verify).
  - Practitioner summaries state half Kelly keeps about **¾ of the optimal growth rate** with much lower volatility and drawdowns.

  — [MacLean-Thorp-Ziemba chapter (IDEAS)](https://ideas.repec.org/h/wsi/wschap/9789814293501_0038.html); [MacLean-Thorp-Zhao-Ziemba (EFMA 2011)](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2011-Braga/papers/0103.pdf); [Ziemba presentation](https://www.mathnet.ru/PresentFiles/7097/7097.pdf); [LuxAlgo Kelly overview (secondary)](https://www.luxalgo.com/library/concept/kelly-criterion.md)
- **Crypto volatility scale:** the HFR Cryptocurrency Index had **59.5%** annualised volatility over the 5 years to February 2025. That is a fund index, not BTC itself. — [HFR market commentary, March 2025](https://www.hfr.com/?p=38140)
- **Leverage and liquidation:** in the Oct 10–11, 2025 cascade, about $19B in leveraged positions were liquidated as BTC fell about 14.5% within 6 hours. — [Cointelegraph](https://cointelegraph.com/news/19b-crypto-market-crash-leverage-china-tariffs)

### Inferences
- **Recommended default: volatility-targeted, capped sizing.**
  - Notional fraction w = min(cap, σ_target ÷ σ̂_BTC), where σ̂ is an EWMA or 20–60-day realised vol, annualised.
  - Example: σ_target = 30% and σ̂ = 60% gives w = 50% of equity in BTC. If σ̂ falls to 30%, w = 100% (the spot cap).
  - On **spot long-only**, w can't usefully exceed 1.0, so the target mostly *reduces* exposure in high-vol periods. That fits the Moreira-Muir and Harvey et al. evidence that cutting exposure when vol is high trims tails.
  - A 20–40% annualised vol target is reasonable for a BTC sleeve. It means typically holding about 35–70% of equity in BTC when long, if BTC vol is about 55–60% (assumption; measure BTC's own vol from data).
- **Per-trade risk sizing (ATR / fixed fractional)** as an alternative: risk *r*% of equity per trade (e.g. 0.5–1%), with quantity = (r × equity) ÷ (k × ATR). Cap notional at 100% on spot. Use `Decimal` throughout, per CLAUDE.md.
- **Kelly as a ceiling only.** The Kelly fraction ≈ μ/σ² depends on μ, the least reliable quantity, and a backtest μ is inflated by selection (sections 1 and 8). If you compute it, use the **DSR- or haircut-adjusted** Sharpe and apply ≤ ½, preferably ¼. Example: a haircut Sharpe of 0.5 with σ = 60% gives μ ≈ 30%, so Kelly ≈ 0.30 ÷ 0.36 ≈ 0.83 and half Kelly ≈ 0.4. Vol targeting usually gives a similar or smaller number with less estimation risk.
- **Hard caps independent of the model:**
  - max notional (e.g. 100% of equity on spot; ≤ 1–2× on perps);
  - max order size (e.g. a fixed USDT limit from config);
  - max position change per bar, to avoid fat-finger or bug-driven orders.
- **Leverage.** For perps, an isolated-margin long at leverage L is liquidated after roughly a 1/L adverse move, less maintenance margin (background, unverified here; check the exchange formula). At 5× that is about −18% to −20%, which the Oct 2025 move nearly reached intraday. Keep effective leverage ≤ 2× and model liquidation with mark price. Better still, stay spot-only until the spot strategy has a live track record. Any leverage change must be flagged under "Risk to live trading" per CLAUDE.md.

### Gaps
- I found no BTC-specific study of vol-targeting benefits. The evidence comes from traditional assets (Moreira-Muir, Harvey et al.) plus its use in crypto trend papers.
- I could not verify Carver's specific half-Kelly guidance or his recommended vol targets from primary sources (blog qoppac.blogspot.com and *Systematic Trading*).
- I found no sourced current figure for BTC's own realised volatility (2023–2026).

## 6. Risk management: stop-loss evidence, trailing and time stops, loss limits, drawdown breakers, kill switches, downtime and liquidation risk

### Takeaway
Stop-losses aren't free insurance. Kaminski & Lo prove they **reduce** expected return under a random walk and can only add value when returns have momentum. They therefore suit trend-following systems and generally hurt mean-reversion systems. Backtests also tend to show more, and cleaner, stop exits than live trading. Portfolio-level controls are engineering necessities and should be pre-registered:
- volatility-scaled exposure;
- daily loss limits;
- drawdown circuit breakers;
- kill switches;
- stale-data and exchange-down handling.

### Cited Findings
- **Kaminski & Lo**, "When Do Stop-Loss Rules Stop Losses?" (J. Financial Markets, 2014; working paper from 2007):
  - "under the Random Walk Hypothesis, simple 0/1 stop-loss rules always decrease a strategy's expected return, but in the presence of momentum, stop-loss rules can add value";
  - empirically (US equities, switching to long-term bonds when stopped out), some rules added **50–100 bps per month** during stop-out periods;
  - at lower sampling frequencies, certain stop policies raised expected return while substantially reducing volatility.

  — [MIT DSpace record](https://dspace.mit.edu/entities/publication/bb69ca4b-0cdc-487f-831d-63b2e84fafee)
- Freqtrade warns that stoploss exits "can appear more often in backtests than in dry-run or live". Its backtester fills stops at the stop price even when the low was lower, an optimistic assumption on gaps. — [Freqtrade docs: backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)
- BTC dynamics depend on time scale (hourly mean reversion in one 2020–2025 study). Whether stops help therefore depends on the strategy's horizon. — [Theseus thesis](https://www.theseus.fi/handle/10024/902903)
- **Venue failure is real:** in Oct 2025, Binance reimbursed about $283M for collateral mispricing that caused erroneous liquidations (secondary press). — [CoinGecko explainer](https://www.coingecko.com/learn/october-10-crypto-crash-explained); [The Defiant](https://thedefiant.io/newsletter/defi-daily/the-ultimate-10-10-crash-autopsy)
- On perps, mark price drives liquidation and can already include upcoming funding, so liquidations can occur from unrealised losses before funding settles (BitMEX mechanics). — [BitMEX support](https://support.bitmex.com/hc/en-gb/articles/7160140704669-Can-a-Funding-Payment-Trigger-Liquidation)
- Arnott-Harvey-Markowitz: don't tweak models in response to live results (summary). Risk rules should be set in advance, not changed after a loss. — [Alpha Architect](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/)

### Inferences
- **Stops by strategy type:**
  - **Trend and breakout:** wide ATR-based initial stops (e.g. 2–4× ATR) and trailing or channel exits (e.g. an opposite Donchian channel) are consistent with Kaminski-Lo's momentum case.
  - **Mean reversion:** tight stops tend to cut trades just before they revert, so use **time stops** (exit after N bars) plus a wide disaster stop.
  - Test any stop rule as a variant (it counts toward N) and on 1m detail data.
- **Disaster stop on the exchange.** Even when the strategy uses candle-close exits, place an exchange-side stop-market order (reduce-only on perps) far from price, e.g. a 3–4× ATR or 15–20% move. Positions are then protected if the VPS or bot dies. Accept that it may fill badly in cascades.
- **Pre-registered portfolio controls** (suggested defaults to calibrate with Monte Carlo from section 2):
  - **Daily loss limit:** halt new entries for the day if equity falls by more than about 2–3× the expected daily σ of the sized strategy.
  - **Drawdown circuit breaker:** if live drawdown exceeds about 1.0–1.5× the backtest's Monte Carlo 95th-percentile max drawdown, flatten and halt for manual review.
  - **Kill switch:** a one-command, idempotent "cancel all orders and flatten" path, tested on testnet. It is triggered automatically by:
    - stale market data (no new closed candle within 2× the bar interval);
    - order rejections or repeated API errors;
    - position mismatch between the bot's state and the exchange's state;
    - clock drift.
  - **Exposure limits:** max notional, max leverage (≤ 1× spot, ≤ 2× perps), max open orders, and max order size enforced in the broker layer, not the strategy.
  - **Downtime handling:** on restart, reconcile with the exchange (balances, positions, open orders) before acting. Never assume the last known state. During exchange maintenance, suspend signals.
  - **Perps:** use isolated margin. Monitor the distance to liquidation using mark price, and auto-reduce if it falls below, for example, 3× daily σ.
- All of the above touches order placement and risk limits, so each change needs a "Risk to live trading" section per CLAUDE.md.

### Gaps
- I found no crypto-specific empirical study of stop-loss efficacy for BTC trend vs mean-reversion systems. The Levine & Pedersen and Clare et al. figures quoted on TradingView pages could not be verified and are excluded.
- I found no authoritative source for specific daily-loss-limit or circuit-breaker thresholds for retail algos. The numbers above are suggested defaults, not cited facts.

## 7. Strategy-level risk metrics to report and benchmarks (buy-and-hold, DCA)

### Takeaway
Report risk-shape metrics (volatility, max drawdown and its duration, tails), not just Sharpe. Quantopian found backtest Sharpe nearly useless for predicting live Sharpe, while volatility and max drawdown did carry predictive information. Always benchmark against BTC buy-and-hold and DCA over identical periods, on a risk-adjusted basis (e.g. buy-and-hold scaled to the strategy's volatility).

### Cited Findings
- Quantopian (888 algos): backtest Sharpe had R² < 0.025 for out-of-sample Sharpe, while **volatility and max drawdown** "show significant predictive value". — [Quantpedia summary](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)
- Serial correlation can overstate annualised Sharpe by up to 65% (Lo 2002). Compute Sharpe from returns sampled at the strategy's natural frequency and check autocorrelation. — [Lo (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf)
- DSR adjusts the Sharpe for skew, kurtosis and the number of trials. — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551)
- **DCA is not a risk-free benchmark.** The BIS simulated retail users buying $100 of BTC per month from their first exchange-app download. By December 2022 the median investor had lost about **$431 of $900** invested, and about three-quarters of new users downloaded apps when BTC was above $20k. Covers 200+ exchange apps in 95 countries, 2015–2022. — [BIS Bulletin No. 69](https://www.bis.org/publ/bisbull69.htm)
- Crypto return series are extremely volatile (HFR Crypto Index: 59.5% annualised vol over 5 years to February 2025; −16.8% in February 2025 alone). — [HFR commentary, March 2025](https://www.hfr.com/?p=38140)

### Inferences
- **Standard report** (per backtest, per walk-forward fold, per regime, and live):
  - **Return and risk:** CAGR, annualised volatility, Sharpe (with its standard error and DSR), Sortino, Calmar (CAGR ÷ max drawdown), max drawdown, and max drawdown duration (days underwater).
  - **Tails:** worst day, worst week, 5% CVaR (expected shortfall), skew, kurtosis.
  - **Activity:** exposure % (time in market), turnover (round trips per year), average holding time, number of trades.
  - **Trade quality:** win rate, payoff ratio (average win ÷ average loss), profit factor, expectancy per trade in bps net of costs.
  - **Cost sensitivity:** cost-to-break-even (section 4).
  - **Robustness:** PBO, and the Monte Carlo 5th–95th percentile range for CAGR and max drawdown.
- **Benchmarks on identical dates and costs:**
  - (a) BTC buy-and-hold;
  - (b) BTC buy-and-hold **scaled to the strategy's volatility** (a fair risk-matched comparison for a strategy that is in the market only part of the time);
  - (c) monthly DCA;
  - (d) a simple 200-day moving-average filter, as a "dumb trend" baseline the strategy must beat to justify its complexity.

  A strategy that loses to (b) or (d) after costs isn't worth running.
- Measure all metrics in USDT terms *and* in BTC terms. A strategy that sits in USDT during bear markets can look good in USDT while underperforming simply holding BTC over full cycles.

### Gaps
- I found no source giving BTC buy-and-hold Sharpe and max drawdown for 2017–2026 from a primary data provider. The team should compute this directly from data.binance.vision.

## 8. Realistic expectations: retail algo success rates, professional crypto fund returns, backtest-to-live decay, and a plausible single-asset BTC Sharpe

### Takeaway
The base rates are sobering:
- under 1% of Taiwan day traders were predictably profitable net of fees;
- about 97% of persistent Brazilian futures day traders lost money;
- most crypto-app retail users lost money on BTC.

Published anomalies lose about 26% of their return out of sample and about 58% after publication, and backtest Sharpe barely predicts live Sharpe. Professional crypto fund indices show huge, BTC-beta-driven swings rather than steady alpha. For a single-asset BTC strategy, a *live* Sharpe of about 0.5–1.0 would be a good outcome. Backtests above about 1.5–2 should be treated as overfit until proven otherwise.

### Cited Findings
- **Barber, Lee, Liu & Odean** (J. Financial Markets 18, 2014), Taiwan, 1992–2006:
  - "less than 1% of the day trader population is able to predictably and reliably earn positive abnormal returns net of fees";
  - the top 500 ranked by prior performance earned 37.9 bps per day after fees.
  — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html)
- Barber, Lee, Liu, Odean & Zhang (Review of Asset Pricing Studies 10(1), 2020): about **97%** of day traders are likely to lose money in future day trading. — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rasset/v10y2020i1p61-93..html)
- **Chague, De-Losso & Giovannetti**, "Day trading for a living?" (FGV WP 525, 2020), Brazilian equity futures:
  - among individuals who started in 2013–2015 and day traded for at least 300 days, about **97% lost money**;
  - only about 0.4% earned more than a bank teller (abstract; a secondary source says 1.1%, so cite the abstract);
  - no evidence of learning.
  — [EconPapers](https://econpapers.repec.org/RePEc:fgv:eesptd:525); [Quantpedia summary](https://quantpedia.com/?p=4771)
- **BIS Bulletin 69** (2023): in nearly all economies, most crypto-app users ended with losses on their bitcoin holdings. Large holders sold into the 2022 shocks while small holders bought. — [BIS](https://www.bis.org/publ/bisbull69.htm)
- **McLean & Pontiff** (JF 2016), covering 97 published predictors:
  - returns are about **26% lower out of sample** (an upper bound on data mining) and about **58% lower after publication**;
  - an earlier draft using 82 characteristics reported about 35% post-publication decay.
  — [Published version (PDF)](https://www.gwern.net/doc/economics/2016-mclean.pdf); [Earlier draft (Ivey PDF)](https://ivey.uwo.ca/media/3775549/pontiff.pdf)
- **Quantopian:** backtest Sharpe gave R² < 0.025 for out-of-sample Sharpe across 888 algorithms. — [Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)
- **Harvey & Liu:** a reported Sharpe of 0.75 adjusted for 200 tests becomes 0.32 (about a 60% haircut). — [Advisor Perspectives](https://www.advisorperspectives.com/articles/2016/04/28/special-edition-can-you-trust-investment-research)
- **HFR Cryptocurrency Index:**
  - 2020: +193%; 2021: +215% (as reported by HFR via trade press).
  - 5-year annualised return +51.4% with 59.5% volatility (to February 2025).
  - February 2025: −16.8%; May 2025: +12.7%.
  - About +10% year-to-date through November 2025 after a −8% November (summary).
  - HFRI Systematic Directional (not crypto-specific) was −1.9% year-to-date through November 2025.
  — [HFR commentary, March 2025](https://www.hfr.com/?p=38140); [HFR May 2025 release](https://www.hfr.com/?p=39720); [WealthBriefing](https://www.wealthbriefing.com/html/article.php?id=193376); [HedgeCo](https://www.hedgeco.net/news/?p=91935)
- **AIMA/PwC 7th Global Crypto Hedge Fund Report (2025):**
  - 55% of hedge funds have crypto exposure (up from 47%), mostly under 2% of AUM;
  - 122 managers and investors surveyed, overseeing about $982B.
  - The public coverage found gave no return figures.
  — [Cayman Finance](https://caymanfinance.ky/2025/11/13/majority-of-hedge-funds-now-invest-in-crypto-report-finds/); [Reuters via WHBL](https://whbl.com/?p=887392)
- **Academic crypto trend results:**
  - Zarattini et al.: Sharpe > 1.5 and 10.8% alpha vs BTC net of fees, for a **top-20 rotational** portfolio, not BTC alone.
  - Monash: short-lookback BTC trend gives a high Sharpe before costs, but costs erode it.
  - Man Group: costs cap diversification benefits at about 10–15 coins.
  — [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html); [Monash CFS](https://www.monash.edu/business/mcfs/our-research/all-projects/investment-strategy/trend-following-strategies-for-crypto-investors); [Man Group](https://www.man.com/insights/in-crypto-we-trend)
- A study of trend following on hourly Bitcoin (2011–2019) optimised parameters for Sharpe (working paper; its cost treatment was not confirmed). — [arXiv 2009.12155](https://ar5iv.labs.arxiv.org/html/2009.12155)

### Inferences
- **Expected decay from backtest to live.** Combining the sources:
  - expect a selected backtest's Sharpe to fall by **30–60%+** live (McLean-Pontiff's 26% out-of-sample to 58% post-publication; Harvey-Liu haircuts of about 25–60%+);
  - the decay will be larger the more variants were tried (Quantopian).
- **Plausible single-asset BTC Sharpe:**
  - A disciplined long-only, vol-targeted daily trend system on BTC might plausibly deliver a **live Sharpe of about 0.5–1.0** over a full cycle.
  - Its main value is often **lower drawdowns than buy-and-hold** rather than higher returns.
  - A backtest Sharpe of 1.2–1.5 after realistic costs is consistent with that. A backtest Sharpe above 2 on a single asset with candle data should trigger an overfitting and look-ahead audit, not excitement.
  - This is an inference; I found no audited dataset of single-asset BTC strategy live Sharpe ratios.
- **Retail returns.** Base rates say most retail traders lose money after costs. A low-turnover, vol-targeted BTC strategy that roughly matches buy-and-hold's return with materially smaller drawdowns would be a *good* outcome. Absolute returns will be dominated by BTC's own trend (beta) in any regime where the strategy is long.
- **Professional comparison.** Crypto fund indices swing with BTC (+193%/+215% in 2020–21, −16.8% in a single month in 2025), suggesting most of their return is beta. Sophisticated systematic shops with diversified multi-coin trend still report cost constraints.

### Gaps
- I could not find the AIMA/PwC 2025 report's performance figures, Eurekahedge crypto index 2025 results, or a full-year 2025 HFR Crypto Index number.
- I found no audited study of retail *crypto algo bot* performance (e.g. from Freqtrade, 3Commas or Pionex users). The evidence is from day traders and crypto-app users generally.
- Crypto-specific CTA research on adding BTC to trend portfolios (e.g. Man, AQR, Campbell) was not retrieved beyond Man's summary snippet.

## 9. Process: paper and testnet duration, live-vs-backtest comparison, decay detection, retirement, and lessons from open-source frameworks

### Takeaway
Paper and testnet trading can't validate an edge statistically: weeks of data have a Sharpe standard error of several units. Its job is to validate **plumbing and execution**, i.e. that live fills, slippage, fees, signal timing and state handling match the backtester trade-for-trade. Statistical validation must come from the pre-registered out-of-sample and holdout work.

Go live small, compare live fills against simulated fills continuously, and pre-register retirement rules based on Monte Carlo drawdown bands rather than eyeballing rolling Sharpe.

### Cited Findings
- Freqtrade: backtesting "will never replace dry-run testing". Stop exits are over-represented in backtests. Indicators can diverge between backtest and live because of how much history is loaded (the recursive problem). — [Freqtrade backtesting.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md); [recursive-analysis.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/recursive-analysis.md)
- Freqtrade's two automated bias detectors, look-ahead (baseline vs sliced dataframes) and recursive (startup-candle variance), plus `--timeframe-detail` intrabar re-simulation, are concrete, copyable tests. — [lookahead-analysis.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/lookahead-analysis.md); [recursive-analysis.md](https://github.com/freqtrade/freqtrade/blob/develop/docs/recursive-analysis.md)
- NautilusTrader's design choices are copyable: `ts_init` set to bar close, orders from `on_bar` fill only after the bar is processed, and configurable intrabar ordering. For many strategies, "bar data (e.g., 1-minute) can be sufficient for backtesting and strategy development". — [NautilusTrader bar execution](https://nautilustrader.io/docs/latest/concepts/backtesting/bar-execution/)
- Arnott-Harvey-Markowitz: live trading is the only true out-of-sample, and models shouldn't be tweaked on live results. — [Alpha Architect](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/)
- Quantopian: the size of the backtest-to-live gap grows with the amount of backtesting. — [Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)

### Inferences
- **Why weeks can't prove edge.** The Sharpe standard error is about 1/√years, so:
  - 3 months of live trading gives SE ≈ 2.0;
  - 1 year gives SE ≈ 1.0.

  A true Sharpe-1 strategy can easily show a negative Sharpe over 6–12 months. Hence:
  - **Paper (local paper broker on live data): 2–4 weeks.** Goal: signals generated live match signals the backtester produces on the same candles, *exactly* (a deterministic replay check).
  - **Testnet: 4–8 weeks**, or until at least about 20–30 round trips have occurred, whichever is later. Goals: order lifecycle, partial fills, rejections, precision and lot sizes, reconnects, restarts and reconciliation, kill-switch drills.

    Testnet order books and liquidity are not representative (background, unverified here), so **don't** judge slippage or P&L there.
  - **Live, small:** start with the minimum notional, e.g. $500–$1,000. Scale up stepwise, e.g. ×2 per month, only while the execution metrics below stay in tolerance.
- **What to compare live vs backtest, per trade:**
  - signal time;
  - intended vs actual fill price (implementation shortfall in bps);
  - fee paid vs fee modelled;
  - latency from candle close to order acknowledgement;
  - missed and partial fills;
  - funding paid (perps).

  Re-run the backtester over the live period with the actual candles and compare equity curves. A persistent gap above about 10–20% of expected per-trade edge means the cost model is wrong.
- **Decay detection** (suggested methods, not sourced in this session):
  - (a) compare cumulative live P&L against the Monte Carlo cone of the backtest (5th–95th percentile);
  - (b) run a one-sided **CUSUM** on per-trade standardised returns vs the backtest mean to detect a downward shift;
  - (c) track a rolling 6–12-month Sharpe *with its standard error*, never as a bare number;
  - (d) watch for regime changes in turnover, win rate or holding time relative to the backtest.
- **Retirement rules (pre-registered):**
  - retire, or halt for review, if live drawdown exceeds the Monte Carlo 95th–99th percentile max drawdown;
  - or if cumulative P&L falls below the 5th-percentile cone for a sustained period (e.g. 3+ months);
  - or if the execution gap makes the net expected edge negative.

  Don't re-optimise parameters on live data to "fix" it (Arnott et al.). A fix is a new strategy and goes back through the full pipeline with N incremented.

### Gaps
- I found no published, evidence-based standard for minimum paper or testnet duration. The durations above are reasoned from statistics, not cited.
- I did not retrieve Freqtrade's hyperopt documentation (loss functions, overfitting warnings), Jesse's docs, or vectorbt/backtesting.py docs on overfitting safeguards. I found no source documenting CUSUM use for live strategy-decay monitoring.
- I could not verify how realistic Binance and Bybit testnet liquidity and fills are.

## 10. Practical tooling: research backtest libraries and BTC historical data sources

### Takeaway
For fast research, use a vectorised pandas/NumPy (or vectorbt) layer to sweep ideas, but count every sweep as a variant. Then confirm candidates in the team's own event-driven backtester, which shares strategy, risk and paper-broker code with live and follows Nautilus/Freqtrade-style conservative fill rules. data.binance.vision is the primary free source for BTC/USDT klines and trades, with checksums. Watch the 2025 microsecond timestamp change and later file revisions.

### Cited Findings
- **data.binance.vision** (binance-public-data):
  - **Spot:** aggTrades, klines and trades.
  - **Futures (USD-M and COIN-M):** aggTrades, klines and trades.
  - Spot kline intervals run from `1s` to `1mo`.
  - Daily files are available the next day; monthly files on the first Monday of the month.
  - Each zip has a `.CHECKSUM` (SHA-256).
  - Spot timestamps are in **microseconds from 2025-01-01**.
  - Files may be revised later; a kline fix was logged on 2022-08-08.
  - The README does not list mark-price klines or funding rates.

  — [binance-public-data README](https://github.com/binance/binance-public-data)
- NautilusTrader supports bar-based execution with explicit intrabar path assumptions and L1 order-book simulation from bars. It ranks data fidelity as order book > trades/quotes > bars. — [NautilusTrader docs](https://nautilustrader.io/docs/latest/concepts/backtesting/bar-execution/)
- Freqtrade provides `lookahead-analysis`, `recursive-analysis` and `--timeframe-detail`, and fee modelling via CCXT exchange defaults or `--fee`. — [Freqtrade docs](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)
- Kaiko offers order-book snapshots via its API only over a rolling 1-month window, so historical depth requires a paid request or your own recording. — [Kaiko docs (summary)](https://docs.kaiko.com/getting-started/kaiko-examples/compare-price-slippage-between-exchanges)

### Inferences
- **Recommended stack:**
  - (1) data.binance.vision spot BTC/USDT 1m + 1h + 1d klines, stored as Parquet with a validated, gap-checked UTC index. Keep 1m data for intrabar re-checks.
  - (2) ETH/USDT for robustness.
  - (3) for perps, USD-M klines plus separately sourced funding-rate and mark-price history. CCXT `fetch_funding_rate_history` and exchange REST endpoints are options (background, unverified here).
  - (4) record your own live order-book snapshots (top N levels each minute) from day one of paper trading. That builds a slippage-model dataset for free.
- vectorbt for parameter sweeps and backtesting.py for quick single-strategy prototypes are reasonable research tools. Final numbers should come only from the shared event-driven engine, so research shortcuts (e.g. close-to-close fills) don't leak into decisions.
- Bybit historical data (public trading-history dumps) can serve as a cross-venue check on Binance candles, e.g. to spot exchange-specific wicks (background, unverified here).

### Gaps
- I could not confirm the earliest BTC/USDT candle on data.binance.vision or Bybit's public history start date (network access to Binance and Bybit was blocked). Verify by listing `data/spot/monthly/klines/BTCUSDT/1d/`.
- I did not retrieve vectorbt, backtesting.py or Jesse docs in this session. Their features and default fill assumptions (e.g. backtesting.py's `trade_on_close` and same-bar SL/TP handling) are unverified here.
- Robot Wealth, Ernie Chan and Quantpedia practitioner guidance on these topics was not retrieved beyond the Quantpedia summaries cited above.
