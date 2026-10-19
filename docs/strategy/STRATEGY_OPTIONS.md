# Ride Bitcoin's trends, size by volatility

The best-supported strategy for our single-pair BTC bot is **long-or-flat trend following on daily candles**. It averages several lookback periods and sizes the position to a volatility target. Everything else we researched either loses to retail fees at our scale or works only as a filter on top of it.

Published work and our own backtest agree on what this edge looks like. Trend rules cut Bitcoin's −84% buy-and-hold drawdown to between **−24% and −63%** (−33% for the best volatility-targeted version) and raise Sharpe from **about 1.06 to 1.3–1.6** over 2015 to May 2026. Most of that comes from stepping aside in 2018 and 2022. They trade only **3–9 round trips a year**, so fees cost around 1–3% annually.

The edge has thinned since US spot ETFs launched in January 2024. Since then buy-and-hold's Sharpe is **0.68**, and the trend ensembles score **0.61–0.89** with half the drawdown.

The other families fare worse. Mean reversion, intraday timing, grid bots, market making, order-flow trading and arbitrage lose to fees or faster players. Funding-rate carry has collapsed from about **11% a year in 2024 to about 2% in 2026**. On-chain, sentiment and machine-learning signals are at best slow filters.

Expectations matter more than the choice of strategy. With about nine years of Binance data, even a true Sharpe of 1 barely clears a strict significance test, and published edges shrink by **26–58%** once they are out of sample or published. A live Sharpe of 0.5–1.0 with much smaller drawdowns than holding BTC would be a good result. We recommend building Option A (trend core) first, and adding filters and carry later, each validated separately.

*How this was put together: three parallel research tracks (price-based strategies; derivatives and alternative data; validation, sizing and risk), whose notes are in [`research/`](research/). The research tools could not load full-text pages, so most published figures come from abstracts and author summaries; spot-check key numbers before relying on them. We added our own daily backtest of the shortlisted rules on Coin Metrics community data. Its method, caveats and full output are in [`research/own-backtest.md`](research/own-backtest.md), and the script is [`research/btc_backtest.py`](research/btc_backtest.py).*

## Daily trend rules are the one family whose evidence survives retail fees

The strongest academic support comes from Detzel, Liu, Strauss, Zhou and Zhu in *Financial Management* (2021). They find that the ratio of price to its moving average predicts daily Bitcoin returns **both in and out of sample**, and that trading on it delivers "economically significant alpha and Sharpe ratio gains relative to a buy-and-hold position" ([IDEAS/RePEc](https://ideas.repec.org/a/bla/finmgt/v50y2021i1p107-137.html)). Liu and Tsyvinski reach a similar result: crypto returns are driven mainly by **time-series momentum and investor attention**, not by stock or macro factors ([NBER](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)). Corbet and co-authors add that for BTC moving-average rules, **buy signals earn more than sell signals** ([IDEAS/RePEc](https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html)). That supports going long or flat rather than shorting.

The most relevant practitioner result is Zarattini, Pagani and Barbon's "Catching Crypto Trends" (2025). It averages Donchian channel breakouts over several lookbacks and sizes positions to a **25% volatility target**. Long-only on BTC since 2015, it reports **30% CAGR, Sharpe 1.56 and a 19% maximum drawdown net of fees**, against passive drawdowns above 80% ([Concretum](https://concretumgroup.substack.com/p/catching-crypto-trends)). The fee model is not stated, and we found no independent replication.

The strongest counter-evidence is serious. Hudson and Urquhart tested about **15,000 rules with corrections for data mining** and found **no out-of-sample predictability for Bitcoin**, although other coins still showed some ([Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)). The likely reconciliation is that BTC trend profits are lumpy. They come from avoiding a few 75–80% bear markets, so the edge looks weak in any short window and strong over full cycles.

Timeframe matters as much as the rule. Daily candles have the best evidence. Quantpedia's plain **hourly MACD** made 2,262 trades for a Sharpe of **0.33** ([Quantpedia](https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/)). Concretum's intraday long-short trend portfolio reaches a Sharpe of about 1.6, but only **before fees** ([Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)).

The fee arithmetic explains why. A spot round trip costs **0.20%** at Binance's 0.10% taker rate. That is **2.4% a year at 12 round trips, 10% at 50 and 50% at 250**, before slippage. Perp maker fills (0.04% per round trip) only change the picture for strategies already near break-even. A daily trend system's fee bill is a rounding error. An hourly or daily-rebalanced system needs a large gross edge just to break even.

## Our 11-year backtest: trend halves drawdowns, but the ETF era thinned the edge

The published numbers come from different periods, cost models and rule definitions, so we ran the shortlisted rules ourselves.

The setup was: daily Coin Metrics BTC prices; signals on each day's close, earning the next day's return; **0.15% per side** for fee plus slippage; long or flat on spot; no leverage. Parameters were taken from the literature, not optimised. Pre-ETF numbers are in-sample relative to most of the papers above. Only 2024 onward is genuinely new data.

| Strategy (daily, long/flat) | Sharpe 2015–26 | CAGR 2015–26 | Max DD 2015–26 | Sharpe ETF era | Max DD ETF era | Round trips/yr |
|---|---|---|---|---|---|---|
| Buy and hold | 1.06 | 61.9% | −83.8% | 0.68 | −49.1% | 0 |
| Buy and hold, 40% vol target | 1.09 | 45.8% | −65.1% | 0.72 | −46.0% | 1.6 |
| 200-day SMA filter | 1.16 | 60.3% | −68.0% | 0.51 | −32.0% | 3.1 |
| MA ensemble (20/50/100/200d) | 1.35 | 65.9% | −56.5% | 0.66 | −29.4% | 9.2 |
| Momentum ensemble (30–365d returns) | 1.31 | 67.1% | −63.2% | 0.81 | −25.7% | 5.9 |
| Donchian ensemble (10–160d) | 1.39 | 58.8% | −47.7% | 0.61 | −25.0% | 5.6 |
| **Donchian ensemble, 40% vol target** | **1.51** | 43.5% | **−33.4%** | 0.73 | −18.3% | 4.3 |
| **Momentum ensemble, 40% vol target** | 1.33 | 44.3% | −41.0% | **0.89** | −21.2% | 4.9 |
| RSI(2) dip-buy above 200d SMA | 0.28 | 3.9% | −37.1% | 0.60 | −23.0% | 8.8 |
| Hold, flat when MVRV > 3 | 0.94 | 47.8% | −78.7% | 0.68 | −49.1% | 1.4 |

*ETF era = 11 Jan 2024 to 23 May 2026. Sharpe uses daily returns annualised with √365. Idle USDT earns 0% here.*

Four findings stand out.

First, **the edge is mostly drawdown control**. In 2018 buy-and-hold lost **72.7%** and the volatility-targeted Donchian ensemble lost **11.5%**. In 2022 buy-and-hold lost **65.3%** and the trend ensembles lost **14–32%**. In bull years they trailed holding.

Second, **the results don't depend on choosing an exact parameter**. Every single-SMA length from 30 to 150 days scored a Sharpe of 1.23–1.40, and Donchian lookbacks of 20 to 80 days scored 1.20–1.40. The popular 200-day SMA was among the weakest, at 1.16. Averaging several lookbacks therefore avoids picking a lucky one.

Third, **costs are close to irrelevant at this turnover**. Moving from 0.05% to 0.30% per side changed full-period Sharpe by at most 0.10. An extra day of signal delay barely mattered either.

Fourth, **the post-ETF picture is much weaker**. Since January 2024, buy-and-hold BTC's own Sharpe has fallen to 0.68. Of the trend ensembles, only momentum (0.81–0.89) and the volatility-targeted Donchian ensemble (0.73) beat it. All still roughly **halved the drawdown**, from −49% to between −18% and −29%.

The statistical case is real but not conclusive. In a block bootstrap, only the volatility-targeted Donchian ensemble beat volatility-matched buy-and-hold in more than 95% of resamples (**p ≈ 0.03**). The other ensembles sat between p ≈ 0.10 and 0.19, and none would survive a correction for the roughly 14 variants we tried.

BTC's realised volatility has also fallen, from a typical 0.55–0.9 a year before 2023 to about **0.40–0.50 since**. A 40% volatility target now means a near-full position whenever the trend signal is on. Concretum's 25% target would leave the bot mostly in cash: it made only 8.7% CAGR in the ETF era in our test.

Two popular ideas failed outright. Connors-style RSI dip-buying in an uptrend made **3.9% a year**. The "exit when MVRV exceeds 3" rule left the 2021 bull market early and never triggered in the 2023–2026 cycle, where MVRV peaked at **2.78**.

## Mean reversion, calendar timing, grids and order flow lose to fees or faster players

Bitcoin does mean-revert at short horizons. De Nicola documents significant **negative autocorrelation at 1-, 2- and 4-hour horizons**, with larger reversals after larger moves ([Ledger](https://ledger.pitt.edu/ojs/ledger/article/download/213/212/1232)). But those are the horizons where fees are largest relative to the move, and over weeks BTC trends instead.

Oscillator rules show the cost of fighting that trend. A plain RSI 30/70 strategy returned about **60% against roughly 1,200% for buy-and-hold** over 2019–2021, because it kept selling into rallies that were not tops ([BGeometrics](https://bgeometrics.com/blog/2022-01-rsi-vs-hodl-bitcoin)). Our RSI(2) test confirms the pattern. We found no peer-reviewed BTC RSI or Bollinger study that included costs.

Calendar effects are the least reliable. The largest study, more than 15 million observations across seven exchanges, found **no consistent or persistent time-of-day, day-of-week or month-of-year pattern** ([UWA](https://research-repository.uwa.edu.au/en/publications/bitcoin-time-of-day-day-of-week-and-month-of-year-effects-in-retu/)). Halving-cycle studies rest on **four events** ([IDEAS/RePEc](https://ideas.repec.org/a/gam/jjrfmx/v18y2025i5p242-d1647669.html)).

The most cited intraday rule is Quantpedia's: buy at 21:00 UTC and sell at 23:00 UTC. It reports **33–41% a year**, apparently before costs, and had a rough 2022–2023 ([Quantpedia](https://quantpedia.com/the-seasonality-of-bitcoin/)). One round trip a day at spot taker fees costs about **73% a year**, so the rule is unusable on spot. Even with maker-only perp fills it would cost about 15%.

Grid bots are mainly a bet that price stays in a range. An academic analysis finds a plain grid has **roughly zero expected value before fees**, so it loses money after them ([arXiv](https://arxiv.org/pdf/2506.11921)). One four-year backtest of popular Binance grid settings returned **+7% against +127% for buy-and-hold in 2024**, and **−35% against −65% in 2022** ([DEV Community](https://dev.to/aduenasdev/i-backtested-the-most-popular-binance-grid-bots-on-4-years-of-real-data-1gnb)).

Market making is out of reach at our scale and latency. Crypto spreads carry significant adverse-selection costs ([Tiniç & Sensoy](https://nottingham-repository.worktribe.com/OutputFile/40584797)), and the maker-rebate VIP tiers that make it pay need millions in monthly futures volume ([Binance](https://www.binance.com/uz-UZ/support/articles/360033544231)).

Order-book imbalance signals live at **1–10 second horizons** and are unstable. In one 2025–26 study the BTC/USDT result **reversed when the sample grew from 7 to 9 days** ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7227998)). Cross-exchange arbitrage spreads have narrowed to about 0.1–2%, against a 0.2% fee break-even, according to a vendor source ([Opportuna](https://opportuna.io/blog/is-arbitrage-profitable)).

Copy trading fares no better. On Bybit, followers of "reputable" leaders **lost money cumulatively**, and gold-tier portfolios started losing for copiers **within 10 days** ([ACM CHI 2024](https://dl.acm.org/doi/10.1145/3613904.3642715)).

## Carry, on-chain, sentiment and ML work as switches, not engines

Funding-rate carry means holding spot BTC long and a short perpetual against it, so the position is market-neutral and collects funding payments. It is the easiest strategy here to build and the most tempting. BIS research finds crypto carry averaged **over 10% a year and at times 40–60%**. It also finds that **with 10x leverage the futures leg would have been liquidated in over half the months studied**, and that **high carry predicts crashes** ([BIS](https://www.bis.org/publ/work1087.pdf)).

The yield has since collapsed. BTC perp funding averaged **11% in 2024, 4.9% in 2025 and 2.2% in 2026 to August** ([CryptoSlate](https://cryptoslate.com/ethena-is-targeting-the-120-trillion-wall-street-stocks-market-to-hunt-yields-5x-higher-than-bitcoin/)). CME basis traded around 2–3%, below Treasury yields ([BigGo Finance](https://finance.biggo.com/news/9c11c1e7-4988-4ad7-998f-7d4f8a51f6ad)), and hedge funds on CME flipped from structural shorts to net long in August 2026 ([CoinDesk](https://www.coindesk.com/markets/2026/08/10/a-rare-cme-shift-hedge-funds-abandon-structural-shorts-to-bet-on-a-bitcoin-rally)).

The tail risk is concrete. On 10 October 2025, **$19 billion** of positions were liquidated. Auto-deleveraging closed the profitable hedge shorts that market-neutral traders depended on, and some users could not reduce risk for nearly two hours ([Forbes](https://www.forbes.com/sites/boazsobrado/2025/10/21/locked-out-and-liquidated-traders-blame-binance-for-19-billion-crash/)).

Capital has to be split between the spot leg and the perp margin, and opening and closing both legs costs 0.24–0.30% of notional. Net of both, BTC-only carry in 2026 yields roughly **1–3% on capital**. That suits a module that switches on when funding is unusually high, not a strategy to run all the time.

Funding, open interest and liquidation data work as risk gauges, not entry signals. Regressing 8-hour BTC returns on funding gives an **R² of 0.003** ([Fulgur Ventures](https://medium.com/@fulgur.ventures/bitcoin-funding-rates-and-price-predictability-27ce95535af1)). The BIS crash link holds over about a month, which supports cutting exposure when leverage looks crowded.

On-chain valuation has the same problem as calendar rules: too few cycles. Grobys (2026) raised Sharpe from **0.45 to 1.28** with MVRV-Z, but **none of the exit thresholds triggered in 2022–2025** ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0275531926002138)). Our MVRV test lost 14 points of CAGR. BTC exchange net inflows **generally lack predictive power** for returns ([arXiv](https://arxiv.org/pdf/2411.06327)).

On data access, Glassnode's $49 tier gives only 14 days of history over its API, which is useless for backtesting ([costbench](https://costbench.com/software/onchain-analytics/glassnode/)). BGeometrics' free tier is enough for a daily poll ([bitcoin-data.com](https://bitcoin-data.com/bguser/free-features.html)). CoinMarketCap, our one aggregator, does not appear to offer on-chain metrics, but its free Basic plan includes its **own Fear & Greed index** ([CoinMarketCap](https://coinmarketcap.com/academy/article/best-free-crypto-api-in-2026-free-tier-comparison)).

Sentiment and machine learning follow the same pattern. A BTC Fear & Greed contrarian rule returned **1,145% against 1,046% for buy-and-hold**, before fees and taxes ([Bitcoin Magazine](https://bitcoinmagazine.com/markets/how-a-bitcoin-fear-and-greed-index-trading-strategy-beats-buy-and-hold-investing)). In a test of 141 BTC predictors, only about **4 beat a random walk at every horizon** ([ResearchGate](https://www.researchgate.net/publication/396908181_A_Comprehensive_Look_at_Bitcoin_Return_Predictability)). The apparent effect of ETF flows on returns falls from **4.89 to 1.67 points per $1B** once timestamps are aligned, and price predicts flows at least as strongly as flows predict price ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7545019)).

The best recent ML study used hourly BTC data from 2018 to 2026 and a 27-fold walk-forward test. Naive models **fail after 10 basis points of costs**. A filter that only trades when the predicted move exceeds costs rescued some XGBoost setups, but the result was **not statistically better than buy-and-hold** ([arXiv](https://arxiv.org/abs/2606.00060)). Another audit found a model with an **AUC near 0.89 that still lost 44%** ([arXiv](https://arxiv.org/abs/2607.19453)). In the 17-day Alpha Arena contest, **four of six LLM traders lost money** ([Forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/)).

## Nine years of data can only prove a strong, simple strategy

The validation research is the most consequential part of this report, because it limits what any backtest can prove. Bailey, Borwein, López de Prado and Zhu show that with five years of data, **about 45 independent tries are enough to "find" a Sharpe of 1 by luck** ([CORE](https://core.ac.uk/display/24055290)). Harvey, Liu and Zhu argue that after decades of data mining a new finding needs a **t-statistic above 3, not 2** ([SSRN](https://papers.ssrn.com/abstract=2513152)).

As a rule of thumb, the t-statistic is about Sharpe × √years. A true Sharpe of 1 therefore needs about **nine years to reach t = 3**, which is all the Binance BTC/USDT history there is, and only if almost nothing else was tried.

Track records show how backtests decay. Across 888 Quantopian algorithms, backtest Sharpe explained **under 2.5% of the variation in live Sharpe**, while volatility and drawdown did predict live results. The more a strategy was backtested, the worse it did live ([Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)). Published anomalies earn about **26% less out of sample and 58% less after publication** ([McLean & Pontiff](https://www.gwern.net/doc/economics/2016-mclean.pdf)). After 200 tests, a 0.75 Sharpe deflates to **0.32** ([Advisor Perspectives](https://www.advisorperspectives.com/articles/2016/04/28/special-edition-can-you-trust-investment-research)).

Retail base rates are harsh. **Fewer than 1%** of Taiwanese day traders were reliably profitable after fees ([IDEAS/RePEc](https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html)), and about **97%** of persistent Brazilian futures day traders lost money ([EconPapers](https://econpapers.repec.org/RePEc:fgv:eesptd:525)). That is why a **live Sharpe of 0.5–1.0** is a realistic target, and why a single-asset backtest above 2 should be treated as a bug to find.

These findings point to a protocol for testing strategies:

- **Holdout:** set aside the most recent 12–18 months of data now, unseen, and use it once.
- **Selection:** choose on the earlier data with walk-forward testing. Log every variant tried, and report the deflated Sharpe ratio and the probability of backtest overfitting.
- **Robustness:** accept only broad parameter plateaus. Report results by regime (2018, 2019–21, 2022, ETF era), run the unchanged rules on ETH as a check, and Monte Carlo-resample trades to set drawdown limits.

Paper trading and testnet then test the **plumbing, not the edge**. After three months, a Sharpe estimate has a standard error of about 2.

On sizing, volatility targeting has the strongest evidence. Across 60+ assets it **raised Sharpe for risk assets and consistently reduced extreme returns** ([Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/)), extending Moreira and Muir's volatility-managed portfolios ([NBER](https://www.nber.org/papers/22208)). Kelly sizing should only set an upper limit: half Kelly lost half its wealth **1% of the time against 8.4% for full Kelly** in one simulation ([Ziemba](https://www.mathnet.ru/PresentFiles/7097/7097.pdf)).

Kaminski and Lo prove that stop-losses **always reduce expected return under a random walk** and add value only when prices trend ([MIT](https://dspace.mit.edu/entities/publication/bb69ca4b-0cdc-487f-831d-63b2e84fafee)). So trend exits and a wide exchange-side disaster stop suit Option A, and tight stops do not.

The backtester should follow Freqtrade's and NautilusTrader's rules. It should fill orders at the next bar, assume the stop triggers first when a stop and target fall within the same candle, and run Freqtrade-style lookahead and recursive-indicator tests ([Freqtrade](https://github.com/freqtrade/freqtrade/blob/develop/docs/lookahead-analysis.md)). It should also handle Binance's switch to **microsecond kline timestamps from January 2025** ([binance-public-data](https://github.com/binance/binance-public-data)).

## Four options for the bot, from conservative core to research bets

| | **A. Trend core** *(recommended start)* | **B. Trend core + risk filters** | **C. Trend core + opportunistic carry** | **D. Faster or long-short trend on perps** |
|---|---|---|---|---|
| **What it does** | BTC/USDT spot, long or flat. Daily signal at the 00:00 UTC close, averaging momentum (30–365d) and Donchian (10–160d) signals. Position = signal × min(1, 40% ÷ 30-day realised vol), with a 10-point rebalance band. Wide exchange-side disaster stop. | Option A, plus slow overlays that cut exposure: funding or basis crowding (BIS crash link), extreme Fear & Greed (CMC Basic). Each overlay is a separately tested variant. | Option A, plus a perp leg: when funding stays well above baseline (e.g. 7-day average above about 10%), idle USDT runs spot-long/perp-short carry. Off otherwise. | Option A's logic on 4h or 1h candles with maker-only entries, and/or a short side when the trend is down. |
| **Evidence** | Strongest of any family: Detzel; Concretum; our backtest (Sharpe 1.33–1.51 since 2015, 0.73–0.89 in the ETF era). | Weak to moderate. Filters are cheap, but each adds a variant and none is proven out of sample. | Strong that carry existed; weak that it pays now (about 2% in 2026). | Gross-only intraday results. Buy signals beat sell signals on daily bars. |
| **Expected profile** | Drawdowns roughly half of buy-and-hold. Trails in bull runs. Live Sharpe maybe 0.5–1.0. | Similar to A with slightly smaller tail losses, if the filters hold up. | Adds about 1–3% a year on idle capital at 2026 funding, more if funding rebounds. | Unknown. More trades, funding costs, liquidation risk. |
| **Turnover / fees** | About 4–6 round trips a year, about 1–2% a year in fees and slippage. | About the same as A. | 0.24–0.30% per carry round trip. | Tens to hundreds of round trips a year. Fee-bound. |
| **Build effort / new risks** | Low. Fits the planned `on_candle` → RiskManager → Broker path. Spot only, no liquidation risk. | Low. Funding data comes free from the exchange via CCXT. | Medium. Perp account, margin monitoring, auto-deleveraging, exchange counterparty risk. Needs a "Risk to live trading" section. | Medium to high. Liquidation risk, mark-price modelling, funding cash flows. Needs a "Risk to live trading" section. |
| **Verdict** | **Build first.** | Add after A passes its holdout. | Park until funding regimes improve. | Research track only. |

Option A is the only choice backed by both published evidence and our own numbers, and it is also the simplest to build, test and explain.

Its specific settings are reasoned defaults, not tuned values:

- **Blend:** the momentum and Donchian ensembles averaged together. This is untested; it should be the single pre-registered candidate and tested once.
- **Volatility target:** 40%, so that at today's lower volatility the bot can hold a full position.
- **Rebalance band:** 10 points, to keep the volatility scaling from churning fees.

It should be benchmarked against:

- buy-and-hold;
- buy-and-hold at the same volatility target (the fairest comparison);
- a 200-day SMA filter;
- weekly DCA;

with results reported in USDT and in BTC.

Options B and C improve on A without replacing it. Both reuse its execution path. Their extra risk sits in the filter logic and the perp account, which can be switched off separately.

We recommend against building the following:

- RSI or Bollinger mean reversion on its own;
- intraday seasonality on spot;
- grid bots;
- market making;
- order-flow trading;
- arbitrage;
- standalone ML or LLM trading;
- copy trading;
- MVRV threshold exits.

## Conclusion

For a single BTC pair, choosing a strategy is mostly choosing an objective. Trend following does not reliably beat holding Bitcoin on return. In the ETF era it behaves like **BTC exposure with roughly half the drawdown**, earning roughly the same return in the best variants and somewhat less in others. If we judge the bot on beating buy-and-hold in a bull market, we will judge it a failure. If we judge it on reaching a 2022-style bear market with a 15–30% loss instead of 65%, it already works on paper. We should agree which objective we are using before writing any code, because it decides the volatility target, the benchmark and when we would retire the strategy.

The second takeaway is about process. With one asset and nine years of data, the bot's real advantage comes from limiting what we try: few variants, set aside a holdout, and record every backtest. That matters more than any indicator.

Next steps:

1. Agree the objective. We also need to decide whether perps are allowed at all, since they determine whether Options C and D exist.
2. Freeze the holdout window.
3. Reproduce the Option A table on Binance BTC/USDT data in our own backtester, once it exists (Phase 6).
4. Open a GitHub issue that pre-registers Option A's rules before we tune anything. The proposed rules are written out in [`STRATEGY_SPEC.md`](STRATEGY_SPEC.md).
5. Decide how the bot learns from its own trades without overfitting. The proposal, and a walk-forward test of 15 learning schemes, is in [`LEARNING_LOOP.md`](LEARNING_LOOP.md).
