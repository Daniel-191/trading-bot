# Price/volume-based (technical and systematic) strategies for Bitcoin: what the evidence says after costs

> Method note for the report writer: every full-text fetch failed with a DNS error during this session. That covered quantpedia.com, concretumgroup.com, arxiv.org, ideas.repec.org, cxoadvisory.com, man.com, monash.edu and abarbon.com. All findings below therefore come from search-engine summaries of abstracts, author write-ups and secondary summaries, not from reading the full PDFs. Many exact Sharpe, CAGR and turnover tables could not be verified; they are listed under Gaps. Fee arithmetic in the Inferences is my own, based on the fee levels in the brief (spot 0.10% per side; perp 0.02% maker / 0.05% taker).

## 1. Trend following / time-series momentum on BTC (MA crossovers, price-vs-MA, Donchian breakouts, TSMOM, multi-lookback blends): does it work, at which timeframes, and has it decayed?

### Takeaway
Trend following is the best-supported price-based family for BTC. Daily-bar rules (price above an MA, Donchian breakouts, ensembles of lookbacks) have repeatedly delivered better Sharpe ratios and much smaller drawdowns than buy-and-hold, at low turnover that survives retail fees. Evidence that they beat buy-and-hold on raw return is weak, and the strictest out-of-sample test (Hudson & Urquhart) found no BTC predictability out-of-sample. I found no rigorous BTC-only study that isolates performance after the January 2024 ETF launch.

### Cited Findings
**Academic: daily trend / MA rules**
- Detzel, Liu, Strauss, Zhou & Zhu, "Learning and predictability via technical analysis: Evidence from bitcoin and stocks with hard-to-value fundamentals", *Financial Management* 50(1), 2021, pp. 107–137. Ratios of price to moving average forecast daily Bitcoin returns both in-sample and out-of-sample. Trading on these ratios "generate[s] an economically significant alpha and Sharpe ratio gains relative to a buy-and-hold position." — [IDEAS/RePEc](https://ideas.repec.org/a/bla/finmgt/v50y2021i1p107-137.html)
- The Detzel et al. strategy holds BTC when price is above a 5-, 10-, 20-, 50- or 100-day SMA and holds T-bills otherwise; the working-paper version is dated January 2018. — [CXO Advisory summary](https://www.cxoadvisory.com/currency-trading/timing-bitcoin-with-smas/)
- Hudson & Urquhart, "Technical trading and cryptocurrencies", *Annals of Operations Research* 297 (2021), pp. 191–220. They test about 15,000 rules in five classes on two BTC markets and three other coins. They find significant predictability and profitability, use data-snooping corrections, and report breakeven costs well above typical crypto costs. However, **Bitcoin showed no predictability in the out-of-sample period**, while the other coins still did. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1); [IDEAS/RePEc](https://ideas.repec.org/a/spr/annopr/v297y2021i1d10.1007_s10479-019-03357-1.html)
- A search snippet from the crypto technical-trading literature reported the mean Sharpe of rule portfolios falling from 0.66 in-sample to 0.06 out-of-sample, with returns not surviving "modest transaction costs" out-of-sample and no BTC predictability out-of-sample. This appears to be the Hudson & Urquhart out-of-sample analysis, but I could not confirm the attribution because the full text was unavailable. — [Hull repository (Hudson)](https://hull-repository.worktribe.com/output/2328042)
- Corbet, Eraslan, Lucey & Sensoy, *Finance Research Letters* 31 (2019). On high-frequency BTC data they test MA-oscillator and trading-range-breakout rules and find significant support for MA rules. The variable-length MA rule performs best, and **buy signals earn more than sell signals**. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html); [DCU repository](https://doras.dcu.ie/25053)
- Grobys, Ahmed & Sapkota (2020) use daily data on 11 cryptocurrencies, 2016–2018. **Excluding Bitcoin**, a simple MA rule earned an excess return of 8.76% per year after controlling for the average market return. — [Osuva PDF](https://osuva.uwasa.fi/bitstream/10024/11192/2/Osuva_%20Grobys_Ahmed_Sapkota_2020.pdf)
- Deprez & Frömmel, "Are simple technical trading rules profitable in bitcoin markets?", *International Review of Economics & Finance* 93B (2024), pp. 858–874. It tests MA crossovers, filter rules and momentum rules on BTC; the abstract text was not retrievable. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/reveco/v93y2024ipbp858-874.html)
- A blog summary of related Deprez & Frömmel work says that under much stricter conditions, selected rule portfolios still beat BTC buy-and-hold out-of-sample, **mainly on a risk-return basis**, and contrasts this with Hudson & Urquhart. This is a secondary source. — [Harbourfront Quant (Substack)](https://harbourfrontquant.substack.com/p/can-hypothesis-testing-reduce-data)
- Svogun & Bazán-Palomino test 69 MA and breakout rules on daily and 1-minute data, 2016–2021, with and without costs. Bubble periods raise the odds that the best rules beat buy-and-hold for ETH, XRP and LTC, **but not for BTC or BCH**. They also report that costs *raise* that likelihood for BTC and ETH, a counter-intuitive result I could not check in the full text. — [Universidad del Pacífico](https://ciup.up.edu.pe/publicaciones/technical-analysis-in-cryptocurrency-markets-do-transaction-costs-and-bubbles-matter/)
- A 2020 *Finance Research Letters* paper found the trading-range-breakout rule outperformed in strongly trending BTC markets. — [Utrecht research portal](https://research-portal.uu.nl/en/publications/the-profitability-of-technical-trading-rules-in-the-bitcoin-marke/)
- A 2022 study of four Bitcoin exchange rates found MA rules predict returns and stay profitable after accounting for time-varying risk premiums. — [Journal of Capital Markets Studies (Emerald)](https://emerald.com/insight/content/doi/10.1108/JCMS-10-2021-0030)

**Academic: TSMOM**
- Liu & Tsyvinski, "Risks and Returns of Cryptocurrency" (NBER WP 24877, 2018; later *Review of Financial Studies*). Crypto returns are predicted by crypto-specific factors, mainly **time-series momentum and investor attention**, and have little exposure to stock, macro, currency or commodity factors. — [NBER PDF](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)
- Liu & Tsyvinski's own write-up: for Bitcoin weekly returns, a one-standard-deviation rise in the current week's return goes with a **3.16% higher return the following week**, and a one-SD rise in Google searches with 1.84% higher next-week returns. — [WEF article by the authors](https://www.weforum.org/stories/2018/09/what-are-the-risks-and-returns-associated-with-cryptocurrencies/)
- AIER's summary of the same paper cites a different horizon: a 0.33% higher next-day return. The two summaries disagree on which horizon is headline, and I could not check the paper's tables. — [AIER](https://aier.org/?p=28457)
- Rozario, Holt, West & Ng, "A Decade of Evidence of Trend Following Investing in Cryptocurrencies" (arXiv 2009.12155, September 2020). This is industry-affiliated (Globe Research) with public code. It reports 255% walk-forward annualised returns in bitcoin's early years, and says crypto trend has commodity-like risk-adjusted returns and strong bear-market diversification against equities. — [arXiv](https://arxiv.org/abs/2009.12155v1)

**Practitioner and recent (2025–2026)**
- Zarattini, Pagani & Barbon, "Catching Crypto Trends: A Tactical Approach for Bitcoin and Altcoins" (Swiss Finance Institute RP 25-80, SSRN, revised October 2025; the authors run Concretum Group). It combines an **ensemble of Donchian-channel trend models with different lookbacks into one signal, plus volatility-based position sizing**, to reduce parameter sensitivity. — [Concretum](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/); [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html)
  - **BTC long-only result, from January 2015:** net-of-fee CAGR of 30%, Sharpe 1.56, maximum drawdown 19%, at a 25% annualised volatility target, against "drawdowns exceeding 80% under passive exposure." The fee model is not stated in the summaries. — [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
  - **Altcoin extension:** a trend-managed portfolio of the top 20 most liquid coins reports a net-of-fee Sharpe above 1.5 and annualised alpha of 10.8% versus Bitcoin. Another summary gives a net-of-fee CAGR of 18% with a maximum drawdown of 11%. Summaries are ambiguous about whether the Sharpe above 1.5 and the 10.8% alpha refer to the BTC test or the altcoin test. — [Concretum](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/); [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
  - I found no independent replication. A GitHub issue planning one tests simpler SMA rules and says its author has not read the paper. — [GitHub issue](https://github.com/cuauhtemocbe/btc-predictor/issues/181)
- Padyšák & Vojtko (Quantpedia, 2022), "Seasonality, Trend-following, and Mean reversion in Bitcoin". When BTC is at a **local maximum (10- to 50-day lookback)** it tends to keep rising, and shorter lookbacks work better within that range. Combining the trend (buy at maxima) and mean-reversion (buy at minima) legs gives a return-to-volatility ratio above 2. Cost treatment is not stated in the snippets. — [Quantpedia](https://quantpedia.com/trend-following-and-mean-reversion-in-bitcoin/)
- Nguyen (Talyxion Research), "Systematic Trend-Following with Adaptive Portfolio Construction" (arXiv 2602.11708, 2026; preprint, industry). Out-of-sample over 2022–2024 on 150+ crypto pairs, with a 4 bp taker fee, slippage and funding modelled, it reports Sharpe 2.41, maximum drawdown −12.7% and Calmar 3.18. It claims to beat TSMOM and equal-weight buy-and-hold. A search summary also reported a vol-scaled TSMOM Sharpe of 1.83 and a BTC buy-and-hold Sharpe of 0.17 from its tables, but noted column labels "look inconsistent", and a second summary could not confirm the 1.83. This is multi-coin, so not directly applicable. — [arXiv](https://arxiv.org/abs/2602.11708v1)

**Intraday / sub-daily trend**
- Shen, Urquhart & Wang, "Bitcoin intraday time-series momentum", *Financial Review* 57(2), 2022. Using trading volume as a market clock, the **first half-hour return positively predicts the last half-hour return**, both in- and out-of-sample. The effect is strongest in the highest-volume or highest-volatility sessions, gives "substantial economic gains… especially in periods of a market downturn", and is driven by liquidity provision. Its net-of-cost numbers were not retrievable. — [Birmingham research portal](https://research.birmingham.ac.uk/en/publications/bitcoin-intraday-time-series-momentum/); [Reading accepted version](https://centaur.reading.ac.uk/100181/3/21Sep2021Bitcoin%20Intraday%20Time-Series%20Momentum.R2.pdf)
- Concretum's intraday follow-up: an ensemble of high-frequency trend models, **long-short**, volatility-scaled to 20%, has a **gross-of-fees** Sharpe of about 1.6 over 2018–2025. A volatility-targeted long-only BTC portfolio at the same 20% target has a Sharpe just below 0.8. No net-of-fee Sharpe was found. — [Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)
- Quantpedia (November 2025): a plain **MACD crossover on hourly BTC** made 2,262 trades for 4.6% annual return, Sharpe 0.33, Calmar 0.19 and maximum drawdown −23.9%. Quantpedia then adds a daily-trend filter in the Elder triple-screen style (only take H1 longs when D1 is up); the filtered results were not in the snippets. — [Quantpedia](https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/)

**Decay and efficiency**
- A 2018 Erasmus master's thesis on 5-minute BTC/USD, 2013–2017, found many rules profitable even after data-snooping corrections and costs, but profitability was "highly unstable and declines over time." This is a student thesis. — [Erasmus thesis](https://thesis.eur.nl/pub/41546/)
- Islas Anguiano & García-Medina (arXiv 2511.00665, November 2025; preprint) train on 2021-01-10 to 2024-01-09 and **test from the spot-ETF approval onward**. An LSTM earned about 65.23% cumulative in under a year and beat LightGBM, an EMA crossover, MACD+ADX and buy-and-hold. The snippets do not say how the EMA and MACD+ADX rules did against buy-and-hold. — [arXiv](https://arxiv.org/abs/2511.00665v1)

**Cross-sectional momentum (does not apply to a single-pair bot)**
- Liu, Tsyvinski & Wu (NBER 25882, 2019) find crypto market, size and momentum factors explain the cross-section. These are multi-coin long-short factors. — [NBER](https://www.nber.org/papers/w25882.pdf)
- Man Group finds peak risk-adjusted returns in a crypto trend portfolio at around 10–15 coins, beyond which costs and liquidity outweigh diversification. This is a multi-coin result, irrelevant to a single-pair bot except as evidence that trend works in crypto generally. — [Man Group, "In Crypto We Trend"](https://www.man.com/insights/in-crypto-we-trend)

### Inferences
- The consistent pattern across Detzel, Concretum, Quantpedia and the blog backtests in section 6 is that **daily-bar trend rules on BTC mainly reduce drawdown and raise Sharpe; they rarely beat buy-and-hold on CAGR.** The Concretum BTC result shows this: 30% CAGR at a 25% vol target, while passive BTC from 2015 compounded far faster with drawdowns above 80%.
- **Timeframe:** daily-bar systems (lookbacks of roughly 10–100 days) have the most and best-quality evidence, at turnover of tens of round trips a year. Hourly and intraday trend has an academic effect (Shen et al.) and a gross Sharpe of about 1.6 (Concretum), but no verified net-of-fee result. A naive hourly MACD was poor even before costs (Sharpe 0.33 over 2,262 trades). I found no rigorous 4h-specific BTC study; 4h is untested middle ground.
- **Cost sensitivity, my arithmetic:** a spot round trip costs about 0.20% at 0.10% per side, or 0.15% with BNB. A daily trend system with 10–30 round trips a year pays roughly 2–6% a year at spot taker fees, which is survivable. The hourly MACD's 2,262 trades at 0.20% each would cost about 450 percentage points cumulatively (if "trades" are round trips), which is fatal.
- **Ensembles of lookbacks** (Concretum's Donchian ensemble; Padyšák & Vojtko's finding that 10–50-day lookbacks all work, shorter better) are the main published defence against overfitting a single parameter. They are also easy to implement in an `on_candle` loop.
- **Decay:** the one strict multi-hypothesis out-of-sample test (Hudson & Urquhart) is negative for BTC, while later practitioner work through 2025 (Concretum) remains positive. The likely reconciliation is that trend rules on BTC capture a large, rare-event component: avoiding the 2018 and 2022 −75% to −80% bear markets. That makes results lumpy and statistically weak over short windows, which argues for judging the strategy on drawdown control, not on monthly alpha.
- **Implementation difficulty:** low. The rules need daily OHLC, an MA or rolling max/min, and a realized-volatility estimate for sizing. They fit a candle-driven bot on a cheap VPS and are insensitive to 50–500 ms latency.

### Gaps
- No full-text tables were obtained for Detzel et al. (Sharpe, alpha, sample end), Liu & Tsyvinski (weekly vs daily TSMOM horizons), Deprez & Frömmel 2024 (abstract and results), Shen et al. (net-of-cost results) or Catching Crypto Trends (exact lookbacks, fee model, turnover, trade count, win rate, per-year and post-2024 returns).
- I found **no rigorous BTC-only trend study isolating January 2024 onwards (the ETF era)**. The only post-ETF test found (Islas Anguiano & García-Medina) is a non-peer-reviewed preprint whose snippets do not report the TA rules against buy-and-hold.
- I found no source reporting win rate, average holding period or trade count for daily BTC trend systems. These need an in-house backtest.
- A snippet claimed an earlier crypto momentum study stayed significantly profitable after a 0.2% fee per trade at lower frequencies but not at 5-minute frequency. I could not attribute it to a specific paper.
- Could not access the Monash paper (Le & Ruthbah, "Trend-following Strategies for Crypto Investors") because of a DNS failure: [Monash](https://www.monash.edu/business/monash-centre-for-financial-studies/our-research/all-projects/investment-strategy/trend-following-strategies-for-crypto-investors).

## 2. Mean reversion on BTC (RSI/Bollinger/z-score, short-horizon reversal, buying large drops, "buy the weekend dip")

### Takeaway
BTC shows short-horizon (1–4 hour, and weakly 1-day) negative autocorrelation, and reversion after sharp *drops* is stronger than after rises. However, published BTC mean-reversion strategies are either gross of costs, from theses or blogs, or lose badly to buy-and-hold in bull markets. Over multi-week horizons BTC trends rather than reverts. Unconditional RSI or Bollinger reversal is not evidence-backed for BTC. Mean-reversion entries conditioned on an uptrend are plausible but untested in the literature I could reach.

### Cited Findings
- De Nicola, "On the Intraday Behavior of Bitcoin", *Ledger* (2021). Finds significant **negative first-order autocorrelation at 1-, 2- and 4-hour horizons**. Bigger moves are followed by bigger reversals, which the paper links to overreaction and leverage-driven liquidations. — [Ledger PDF](https://ledger.pitt.edu/ojs/ledger/article/download/213/212/1232)
- Corbet & Katsiampa (2018), nonlinear ANAR models on minutely-to-weekly data, 2010–2018. Reversion is asymmetric: **negative returns revert more strongly than positive ones**, and positive returns show some positive serial correlation (momentum). — [Sheffield Hallam repository](https://shura.shu.ac.uk/23470/)
- A blog estimate puts BTC daily lag-1 autocorrelation at about −0.08, with a significant positive lag-4 value (July 2022; not peer-reviewed). — [CryptoDataDownload](https://www.cryptodatadownload.com/blog/posts/determining-autocorrelation-in-bitcoin-timeseries/)
- Padyšák & Vojtko (Quantpedia, 2022) find that local minima are linked to "abnormal price action" after which BTC tends to bounce. Buying at minima is mutually exclusive with buying at maxima, and the combination gives a return-to-volatility ratio above 2. Cost treatment is unknown. — [Quantpedia](https://quantpedia.com/trend-following-and-mean-reversion-in-bitcoin/)
- A Finnish bachelor's/master's thesis on BTC, 2020–2025, finds BTC mean-reverting on **hourly** data, and a Bollinger strategy beat momentum and buy-and-hold on return and risk-adjusted measures. Results depend heavily on hourly vs daily data, and fee and slippage modelling is unknown. — [Theseus](https://www.theseus.fi/handle/10024/902903)
- A plain RSI 30/70 strategy on BTC over 2019–2021 returned about 60% against about 1,200% for buy-and-hold, because it sold into what were only temporary tops. — [BGeometrics](https://bgeometrics.com/blog/2022-01-rsi-vs-hodl-bitcoin)
- Buying after a large crash: MarketVector analysed 2,286 entry points (2013–2023) after 50% BTC crashes. The title finding is that "buying bitcoin after a 50% crash rarely works". It reports a "Sharpe-like" ratio (median return / standard deviation) of 0.42 for lump-sum entry vs 0.19 for DCA. — [MarketVector](https://marketvector.com/insights/mvis-onehundred/buying-bitcoin-after-a-50percent-crash-rarely-works)
- On "buy the weekend dip", an Ecoinometrics analysis found **no weekend drop in median or average daily BTC returns**. — [Ecoinometrics](https://ecoinometrics.substack.com/p/ecoinometrics-is-there-a-weekend)

### Inferences
- The evidence points to a **horizon split**: hours to about one day show reversion (De Nicola; daily ACF about −0.08), while weeks show momentum (Liu & Tsyvinski; Padyšák & Vojtko 10–50 days). Mean-reversion edges sit on the timeframes where fees bite hardest relative to the expected move.
- Reversion is stronger after drops (Corbet & Katsiampa) and plausibly driven by liquidation cascades (De Nicola). This argues for a **long-only "buy the flush" entry** rather than symmetric fading. Shorting rallies fights the positive serial correlation of up-moves.
- Unconditional oscillator rules (RSI 30/70) underperform massively in bull regimes because they exit trends early. Mean-reversion logic is more useful as an **entry-timing overlay inside a trend filter** than as a standalone strategy (see section 5).
- Cost sensitivity: hourly reversion with frequent trades needs maker execution. At 0.20% per round trip on spot taker, an average gross edge per trade below about 0.2–0.3% is uneconomic. I found no source quantifying the average per-trade edge of BTC hourly reversion.

### Gaps
- No peer-reviewed BTC RSI, Bollinger or z-score study with explicit transaction costs and out-of-sample tests was found.
- No study found on "buy the weekend dip" as a trading rule, as opposed to weekend return statistics.
- A Turatti et al. paper (*Journal of Empirical Finance*), cited in search results as finding BTC "mean-averting" (i.e. trending) across horizons over 2010–2019, could not be tied to a verifiable URL. It conflicts with the short-horizon reversion findings and is worth checking.
- No regime-conditional (high vs low volatility, bull vs bear) study of BTC daily return autocorrelation was found.

## 3. Volatility-based approaches (vol targeting a long BTC position, Larry Williams / opening-range volatility breakout, ATR channels)

### Takeaway
Volatility targeting is widely used in the best BTC trend studies (Concretum targets 20–25%, and Man Group calls it effective at controlling risk). It clearly controls risk, but I found **no rigorous BTC-only study that isolates vol-scaling of a long position against unscaled buy-and-hold** with Sharpe and drawdown numbers. The one cross-sectional crypto study found vol management raised Sharpe through higher returns, not crash avoidance. Larry Williams-style volatility breakout on BTC is popular in Korean retail and TradingView circles but has **no academic or rigorous practitioner evidence** that I could find.

### Cited Findings
- Concretum: a **volatility-targeted long-only BTC portfolio at 20% target volatility** has a Sharpe "just below 0.8" over 2018–2025. In the same write-up, the gross intraday long-short trend ensemble has a Sharpe of about 1.6. — [Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)
- Catching Crypto Trends sizes positions by volatility to a **25% annualised volatility target**, reaching a 19% maximum drawdown against more than 80% for passive BTC. Vol targeting and trend timing are combined, so their contributions are not separated in the summaries. — [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
- Man Group's "An Investor's Guide to Crypto" finds volatility-targeting methods effective at controlling risk, and says trend-following strategies have performed well. — [Man Group](https://www.man.com/insights/investor-guide-to-crypto)
- Applying Barroso/Santa-Clara risk-managed momentum to crypto (cross-sectional, *Finance Research Letters*, 2025) raises average weekly returns from 3.18% to 3.47% and annualised Sharpe from **1.12 to 1.42**. The gains come mainly from higher returns, not from avoiding extreme losses, and crypto lacks the long momentum crashes seen in equities. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1544612325011377)
- The equity benchmark for the idea, Moreira & Muir, "Volatility-Managed Portfolios" (*Journal of Finance*, 2017): taking less risk when volatility is high raises the market factor's Sharpe ratio by about 25%. — [Moreira & Muir PDF](https://amoreira2.github.io/alan-moreira.github.io/VolPortfolios_published.pdf)
- Larry Williams volatility breakout as described by a trading-platform vendor: take the previous day's high-low range, multiply it by 0.25, and add it to (or subtract it from) today's open. Go long when price breaks above the upper level. — [WH SelfInvest](https://whselfinvest.com/en-be/trading-platform/free-trading-strategies/tradingsystem/56-volatility-break-out-larry-williams-free)
- TradingView BTC versions of the rule add filters, such as skipping entries when the prior day's open-to-close volatility exceeds a threshold. These are unvetted scripts with author-claimed performance only. — [TradingView TVExtBot script](https://my.tradingview.com/script/cGIaJaSy)
- The trading-range-breakout rule (a channel breakout) outperformed in strongly trending BTC markets (*Finance Research Letters*, 2020). — [Utrecht research portal](https://research-portal.uu.nl/en/publications/the-profitability-of-technical-trading-rules-in-the-bitcoin-marke/)

### Inferences
- For a single-pair bot, **vol targeting is a sizing layer, not a signal**. Its main documented effect in the BTC studies is cutting maximum drawdown from more than 80% to roughly 20%, while proportionally cutting CAGR, because BTC's realized volatility is usually well above a 20–25% target. Whether it *raises* Sharpe for BTC specifically is not established by any source I could reach. The cross-sectional crypto result (Sharpe 1.12 to 1.42) is suggestive but from a different strategy.
- At a 20–25% vol target on spot without leverage, the bot will usually hold *less* than 100% BTC. Vol targeting only needs leverage (perps) when realized volatility falls below target, which is rare for BTC.
- Rebalancing a vol-scaled position daily creates small trades. A rebalance band (e.g. only trade if target exposure changes by more than 10–20%) is a standard way to keep fees down; no source quantifies this for BTC.
- Daily volatility breakout (one trade a day, entered intraday and exited the next day) implies about 250–365 round trips a year. At 0.20% spot taker cost that is a 50–73% annual fee drag. The strategy is only plausible on perps with maker fills or on a much lower trade frequency.
- Implementation difficulty: vol targeting is easy (rolling standard deviation or ATR of daily returns). Volatility breakout needs intraday stop or trigger orders and is sensitive to fill quality.

### Gaps
- No BTC-only study of vol-targeted long BTC vs unscaled buy-and-hold with Sharpe, CAGR and maximum drawdown over the same window was found.
- No academic or rigorous backtest of Larry Williams volatility breakout, opening-range breakout or ATR-channel systems on BTC with costs was found. Searches surfaced only TradingView scripts and vendor pages.
- The Concretum page's breakdown of the vol-targeted long-only BTC portfolio (CAGR, maximum drawdown) was not retrievable.

## 4. Calendar, seasonality and intraday effects (time of day, US vs Asia sessions, 00:00 UTC / funding timestamps, day of week / weekend, month of year, halving cycle)

### Takeaway
Most BTC calendar effects are fragile. The large multi-exchange study (Baur et al.) found no consistent or persistent time-of-day, day-of-week or month-of-year patterns. Day-of-week findings conflict across studies, and halving-cycle "effects" rest on four events with overlapping windows. The most-cited tradable intraday anomaly (long 21:00–23:00 UTC) reports roughly 33–41% annualised **apparently gross**. At about 365 round trips a year, fees would eat most or all of it at retail spot rates. Session-level return patterns appear to have shifted around 2021 and the 2024 ETFs, but the evidence conflicts.

### Cited Findings
- Baur, Cahill, Godfrey & Liu, "Bitcoin Time-of-Day, Day-of-Week and Month-of-Year Effects in Returns and Trading Volume" (SSRN 3088472, 2017). Uses more than 15 million observations from 7 exchanges and finds time-varying effects but **no consistent or persistent patterns**, consistent with an efficient market. — [UWA repository](https://research-repository.uwa.edu.au/en/publications/bitcoin-time-of-day-day-of-week-and-month-of-year-effects-in-retu/)
- Caporale & Plastun (CESifo WP 6716, 2018): Bitcoin was the only crypto tested with a day-of-week anomaly, with **Monday returns significantly higher**. A trading simulation suggested exploitable profits. — [CESifo PDF](https://cesifo.org/DocDL/cesifo1_wp6716.pdf)
- Aharon & Qadan (*Finance Research Letters*, 2019), using daily data 2010–2017, find a day-of-week effect in both returns and volatility that is robust across subsamples and methods. — [University of Haifa](https://cris.haifa.ac.il/en/publications/bitcoin-and-the-day-of-the-week-effect/)
- Contradicting these: Ecoinometrics finds no weekend drop in returns ([Substack](https://ecoinometrics.substack.com/p/ecoinometrics-is-there-a-weekend)), and a UCD paper finds no classical day-of-week effect in returns, only lower weekend risk ([UCD repository](https://researchrepository.ucd.ie/server/api/core/bitstreams/3fe12e0f-f1c4-4226-937e-b7fc034dfcd9/content)).
- Padyšák & Vojtko / Quantpedia, intraday seasonality, Gemini hourly data. The rule is **buy at 21:00 UTC and sell at 23:00 UTC**, a window when major traditional exchanges are closed. It reports about **33% annualised return, 20.93% volatility and −22.45% maximum drawdown**. — [Quantpedia](https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/)
- Quantpedia's later update with an extended sample reports **40.64% annualised and Calmar 1.79**, with a maximum drawdown of −22.7% against more than −70% for BTC. The strategy had "a rough period in 2022 and 2023". Quantpedia notes the long-only version does poorly in bear markets. Cost treatment is not stated in the snippets. — [Quantpedia, "The Seasonality of Bitcoin"](https://quantpedia.com/the-seasonality-of-bitcoin/)
- Quantpedia, Gemini hourly data 2015–2022: the BTC return during NYSE hours ("intraday") is stronger and more stable than the "overnight" return. — [Quantpedia](https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/)
- On the effect of ETFs on session returns, an Aalto University thesis finds the US spot ETF launch was associated with a **larger US-region overnight premium**, while the Asian overnight premium became statistically insignificant. — [Aalto](https://aaltodoc.aalto.fi/items/e4962f5a-045a-4131-b329-cc27926f6c4f)
- Contradicting this, a CryptoSlate analysis finds the shift toward US-hours volatility **predates the ETFs (change point November 2021)**, with no comparable break at January 2024, and results that depend on the window chosen. — [CryptoSlate](https://cryptoslate.com/crypto-never-closes-but-bitcoin-ethereum-xrp-and-solana-now-move-on-wall-street-time/)
- Session returns in 2026 swing with the window. Velo data over about 3 months gave APAC about +13%, US about +11.5% and Europe about +6.5% ([Bitget](https://www.bitget.com/news/detail/12560605399596)). A later 13-session window (21 September to 7 October) gave −3.24% during US hours and +6.07% outside them ([TokenPost](https://www.tokenpost.com/news/investing/28079)).
- Halving cycle:
  - A 2025 *JRFM* paper uses only **four halvings** (2012, 2016, 2020, 2024) and finds abnormal returns and volatility shifts that are declining as the market matures. — [IDEAS/RePEc](https://ideas.repec.org/a/gam/jjrfmx/v18y2025i5p242-d1647669.html)
  - A 2025 synthetic-control study finds a positive effect three months after the 2024 halving, but **no statistically significant and robust effect for 2020**. — [arXiv 2511.05512](https://arxiv.org/pdf/2511.05512)
  - An older analysis finds BTC and LTC return distributions around halvings statistically the same as the rest of the sample. — [CryptoSlate](https://cryptoslate.com/the-myth-of-cryptocurrency-halving-events-a-deeper-analysis/)
  - A 2026 preprint argues that standard tests over-reject for persistent signals with overlapping returns, with Newey-West empirical rejection rates of 0.33 and 0.17 against a nominal 0.05. — [arXiv 2607.26188](https://arxiv.org/pdf/2607.26188)

### Inferences
- **Robust vs data-mined:** none of the BTC calendar effects meets a high bar. Day-of-week results flip between studies. Month-of-year was not found significant in the largest study. Halving timing has n = 4 events with overlapping windows. The 21:00–23:00 UTC effect is the most specific and best-documented, but it comes from one research shop, had a weak 2022–2023, and appears to be gross of costs.
- **Fee arithmetic for 21:00–23:00 UTC (mine):** one round trip a day is about 365 a year. At spot taker 0.10% per side that is about 73% a year in fees; at 0.075% with BNB about 55%; at perp taker 0.05% about 36.5%; at perp maker 0.02% about 14.6%. Against a 33–41% gross annual return, the strategy is **negative or near-zero after retail spot fees**. It is only conceivable with maker-only fills on perps (where non-fills become a risk), or as a *timing tilt* for a position the bot already holds.
- Session effects (US vs Asia) appear to drift with market structure (Nov 2021 change point; possible ETF effects). Any hard-coded session rule should be expected to decay and must be re-validated on recent data.
- I found no evidence on returns around 00:00 UTC or around perpetual funding timestamps (00:00, 08:00, 16:00 UTC). This was a gap in what I found, not a finding of no effect.
- Implementation is trivial (time-based `on_candle` logic), which is why these strategies are popular in community bots. The risk is in costs and overfitting, not engineering.

### Gaps
- Could not verify whether Quantpedia's 21:00–23:00 UTC results include fees, nor obtain per-year returns or trade statistics.
- No source found on BTC returns or volatility around funding timestamps or 00:00 UTC.
- No post-2024 replication of day-of-week or month-of-year effects was found.

## 5. Combinations and filters (trend filter + mean-reversion entry, regime filters such as volatility regimes or ADX, long-only vs long/short)

### Takeaway
The best-supported combinations are trend timing plus volatility sizing (Concretum) and trend plus buying local minima (Quantpedia, return-to-volatility ratio above 2). A higher-timeframe trend filter on a lower-timeframe signal is a common practitioner fix. On direction, evidence favours **long-only or long-biased** BTC rules on daily bars: buy signals beat sell signals, and the leading daily BTC trend paper is long-only. The only clear long-short success is an intraday ensemble reported **gross** of fees. I found no rigorous test of "RSI dip above the 200-day MA" or ADX filters on BTC.

### Cited Findings
- Trend + mean-reversion combined: buying at 10–50-day maxima (trend) and at minima (reversion) are mutually exclusive signals, and combining them yields a return-to-volatility ratio above 2. — [Quantpedia](https://quantpedia.com/trend-following-and-mean-reversion-in-bitcoin/)
- Multi-timeframe filter: Quantpedia starts from a weak hourly MACD (2,262 trades, Sharpe 0.33, maximum drawdown −23.9%) and adds a daily-trend filter, taking H1 longs only when D1 is up. The filtered results were not retrievable. — [Quantpedia](https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/)
- Trend + vol sizing: Catching Crypto Trends (BTC long-only, Donchian ensemble, 25% vol target) reports Sharpe 1.56, CAGR 30% and maximum drawdown 19% net of fees from 2015. — [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
- Long vs short:
  - For BTC MA rules, **buy signals produce higher returns than sell signals**. — [Corbet et al. 2019, IDEAS/RePEc](https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html)
  - The multi-day Catching Crypto Trends BTC test is **long-only**. — [Concretum](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/)
  - The intraday **long-short** ensemble reaches a Sharpe of about 1.6 **gross**, against just below 0.8 for vol-targeted long-only BTC (2018–2025). — [Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)
  - A Finnish thesis on BTC technical strategies found that when both long-only and short-only versions are profitable, the combined long and short version earns much more. — [LUT University](https://lutpub.lut.fi/handle/10024/159052)
  - Asymmetric reversion: negative returns revert more strongly, while positive returns show positive serial correlation. — [Corbet & Katsiampa, SHU](https://shura.shu.ac.uk/23470/)
- Regime behaviour:
  - BTC intraday momentum has its largest economic value in market downturns. — [Shen, Urquhart & Wang](https://research.birmingham.ac.uk/en/publications/bitcoin-intraday-time-series-momentum/)
  - A summary of a BTC trend study notes a DEMA strategy is relatively stable in Sharpe, especially in bear markets. — [Harbourfront Quant](https://harbourfrontquant.substack.com/p/bitcoin-trend-following-strategies)
  - The 21:00–23:00 UTC long-only rule does poorly in bear markets. — [Quantpedia](https://quantpedia.com/the-seasonality-of-bitcoin/)
- RSI and 200-day filter: the nearest backtest found gates RSI-oversold entries with a short-SMA-above-long-SMA condition, not price above the 200-day MA, and its results were not visible. — [Substack, "I Backtested a Powerful Strategy on Bitcoin"](https://abouttrading.substack.com/p/i-backtested-a-powerful-strategy)

### Inferences
- A defensible single-pair design implied by the evidence is: **(a)** a long-only daily trend signal (an ensemble of lookbacks), **(b)** volatility-targeted sizing, **(c)** optionally, mean-reversion *entries* (buy local minima or sharp drops) only while (a) is on or only for small adds. Every component has at least practitioner-grade BTC evidence. The specific combination has not been tested out-of-sample with costs in any source I found.
- **Shorting BTC:** daily-bar evidence for the short side is weak (buy signals beat sell signals, up-moves are positively autocorrelated, BTC has strong long-run drift). For a spot bot, "flat" is the natural bearish state. A short leg via perps adds funding exposure. In positive-funding regimes shorts *receive* funding, which partly offsets this, but funding flips negative in crashes. That funding point is general market mechanics, not from a cited study here. Shorts also add liquidation risk. Long-short appears to pay mainly at intraday horizons, where fee drag is highest.
- Regime filters: trend systems lose to whipsaw in choppy, range-bound markets and win by stepping aside in sustained bear markets. Mean-reversion does the opposite. That is the rationale for the combination, but I found **no BTC-specific test of ADX or volatility-regime filters**.

### Gaps
- No BTC study found testing ADX filters, volatility-regime switches or "RSI < 30 while price > 200-day SMA" with costs and out-of-sample validation.
- No head-to-head long-only vs long-short decomposition for daily BTC trend rules (net of fees and funding) was found.
- The results of the Rozario et al. (2020) long/short analysis could not be retrieved.

## 6. Benchmarks: how these compare with buy-and-hold and DCA (return, Sharpe, max drawdown, Calmar)

### Takeaway
Reported BTC buy-and-hold over long windows has a Sharpe of roughly 0.8–1.0 and maximum drawdowns of about 77–83%. Trend and timing strategies typically cut maximum drawdown to about 20–60% and often, but not always, raise Sharpe. They frequently lag on CAGR, especially when volatility-targeted. A plain 200-day SMA filter has been reported to *lower* Sharpe versus holding. DCA reduces drawdown relative to lump sum but loses on return most of the time. Most benchmark figures come from blogs or vendors with unclear windows and fees.

### Cited Findings
- **Buy-and-hold reference points:**
  - Passive BTC drawdowns "exceeding 80%" (2015 onwards). — [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
  - One replication-planning table shows BTC buy-and-hold with CAGR 48.9%, Sharpe 0.96 and maximum drawdown −77% (period unspecified; unofficial). — [GitHub issue](https://github.com/cuauhtemocbe/btc-predictor/issues/181)
  - A vol-targeted (20%) long-only BTC portfolio has a Sharpe just below 0.8 (2018–2025). — [Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)
- **200-day SMA vs hold (CryptoQuant):** the 200-day SMA trend strategy had a **Sharpe of about 0.91 vs 1.01 for buy-and-hold**, and a worse Calmar ratio, i.e. risk-adjusted returns were *worse*. Buy-and-hold maximum drawdown was about 80%; a different minute-frequency variant cut this to about 30%. — [CryptoQuant](https://cryptoquant.dev/resources/blog/improve-buy-and-hold-btc)
- **Monthly momentum timing vs hold (Substack):** CAGR 68.6% vs 59.8%, maximum drawdown −58.2% vs −83.4%, Sharpe 1.30 vs 1.04 (period and fees not given in the snippet). — [Systematic Strategies](https://systematicstrategies.substack.com/p/can-you-keep-bitcoins-upside-without)
- **MACD vs hold (vendor):** CAGR 77.24% vs 61.28%, maximum drawdown −61.97% vs −83.40%, invested about half the time (period and fee treatment unverified). — [QuantifiedStrategies](https://www.quantifiedstrategies.com/bitcoin-macd-trading-strategy-performance-backtest/)
- **Donchian ensemble vs hold:** 30% CAGR, Sharpe 1.56 and 19% maximum drawdown, against more than 80% passive drawdown (from 2015, net of fees, 25% vol target). — [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
- **21:00–23:00 UTC seasonality vs hold:** −22.7% maximum drawdown vs more than −70% for BTC; Calmar 1.79 (costs unclear). — [Quantpedia](https://quantpedia.com/the-seasonality-of-bitcoin/)
- **DCA vs lump sum:**
  - AMDAX (10-year backtest): lump-sum portfolios fell about 20% more peak-to-trough than DCA on average; weekly DCA was least risky (measured with Calmar). — [AMDAX (Medium)](https://medium.com/amdax-asset-management/lump-sum-or-dollar-cost-averaging-42c8f5bb9938)
  - Analyst "Nobrainflip", about 400,000 scenarios with a 5% cash yield: lump sum beat DCA in 58–72% of scenarios, but DCA won when starting in BTC's 20–70% drawdown zone. — [CoinTurk News](https://en.coin-turk.com/study-finds-dca-beats-lump-sum-in-20-70-btc-drawdowns/)
  - MarketVector (2,286 entries after 50% crashes, 2013–2023): DCA delivered roughly half the median return of lump sum at less than a quarter of the volatility, with a "Sharpe-like" ratio of 0.42 for lump sum vs 0.19 for DCA. — [MarketVector](https://marketvector.com/insights/mvis-onehundred/buying-bitcoin-after-a-50percent-crash-rarely-works)

### Inferences
- **"Beats buy-and-hold only on drawdown"** is the norm. Typical reported maximum-drawdown improvements are from about −80% to −20% (vol-targeted trend), −22% (seasonality) or −58% to −62% (unscaled timing). Sharpe improvements range from negative (200-day SMA: 0.91 vs 1.01) to large (Donchian ensemble: 1.56 vs roughly 0.8–1.0 for holding). CAGR is usually *lower* for vol-targeted systems and sometimes higher for unscaled timing systems in blog backtests.
- The developers should benchmark any candidate against **(1) buy-and-hold BTC, (2) vol-targeted buy-and-hold at the same target volatility, and (3) weekly DCA**, over the same window and with the same fees. Benchmark (2) separates the value of the timing signal from the value of simply holding less BTC. Concretum's numbers suggest vol-targeted holding alone gives a Sharpe of about 0.8, so a trend system must clearly beat that.
- Calmar is the most informative single ratio for BTC given its −77% to −83% drawdowns. Sharpe is distorted by BTC's fat right tail.

### Gaps
- No single rigorous source gives buy-and-hold, DCA and trend strategies on identical windows with fees and post-2024 sub-periods.
- A search summary cited a CoinDesk Indices cycle-aware strategy (June 2026) with Sharpe 1.22 vs 0.82 for buy-and-hold over 15 years and maximum drawdown −44% vs −80%. I could not tie this to a verifiable URL, so it is excluded from the cited findings.
- The windows and fee assumptions of the Substack, QuantifiedStrategies and CryptoQuant backtests were not visible in the snippets.

## 7. What serious practitioner sources report, and separating rigorous sources from marketing

### Takeaway
The most rigorous practitioner BTC work found is Concretum/Zarattini–Pagani–Barbon (SSRN/SFI paper, ensembles, vol targeting, stated as net of fees but with an unverified fee model) and Quantpedia (Padyšák & Vojtko; explicit rules, but cost treatment unclear). Man Group's commentary supports crypto trend and vol targeting without single-BTC numbers. AQR's trend evidence is non-crypto. TradingView scripts, vendor sites (QuantifiedStrategies), single-author Substacks and exchange "knowledge hubs" are low-evidence or marketing. Freqtrade community backtests did not surface in searches.

### Cited Findings
- **Concretum Group (Zarattini, Pagani, Barbon):**
  - SFI working paper; Donchian ensemble, vol sizing, net-of-fee claims; BTC Sharpe 1.56 and maximum drawdown 19% from 2015. — [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html); [Concretum Substack](https://concretumgroup.substack.com/p/catching-crypto-trends)
  - Intraday long-short Sharpe of about 1.6 **gross**. — [Concretum](https://concretumgroup.com/seasonality-in-bitcoin-intraday-trend-trading/)
- **Quantpedia:**
  - BTC trend and mean-reversion (Padyšák & Vojtko). — [Quantpedia](https://quantpedia.com/trend-following-and-mean-reversion-in-bitcoin/)
  - 21:00–23:00 UTC seasonality (33% then 40.64% annualised; weak 2022–2023). — [Quantpedia](https://quantpedia.com/the-seasonality-of-bitcoin/)
  - Multi-timeframe MACD (baseline Sharpe 0.33). — [Quantpedia](https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/)
  - Calendar-effects review. — [Quantpedia](https://quantpedia.com/are-there-any-simple-calendar-effects-in-bitcoin-market/)
- **Man Group:**
  - Crypto suits trend following because of liquidity, volatility and the lack of fundamental valuation anchors; optimal around 10–15 coins after costs. — [Man Group, "In Crypto We Trend"](https://www.man.com/insights/in-crypto-we-trend)
  - Vol-targeting "effective at controlling risk", and trend has "performed well". — [Man Group, "An Investor's Guide to Crypto"](https://www.man.com/insights/investor-guide-to-crypto)
  - BTC returns were negative 79% of the time during equity drawdowns since 2010, so BTC is not a reliable crisis hedge. — [Man Group, "Bitcoin's Place in Multi-Asset Portfolios"](https://www.man.com/insights/bitcoins-place-in-multi-asset-portfolios)
- **AQR**, "A Century of Evidence on Trend-Following Investing": TSMOM profitable consistently over about 110 years in traditional markets. No crypto-specific AQR note was found. — [AQR](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing)
- **Industry preprints:**
  - Talyxion AdaptiveTrend (Sharpe 2.41, out-of-sample 2022–2024, multi-coin, fees, slippage and funding modelled; not peer-reviewed; table inconsistencies flagged). — [arXiv](https://arxiv.org/abs/2602.11708v1)
  - Globe Research (2020; code public). — [arXiv](https://arxiv.org/abs/2009.12155v1)
- **Low-evidence / marketing examples:**
  - TradingView BTC "volatility breakout" scripts with author-claimed results ("the best strategy for Bitcoin"); protected code. — [TradingView](https://www.tradingview.com/script/8gF0O6eF/)
  - Vendor MACD backtest. — [QuantifiedStrategies](https://www.quantifiedstrategies.com/bitcoin-macd-trading-strategy-performance-backtest/)
  - Exchange educational content on mean reversion with no empirical tests. — [BIT Knowledge Hub](https://www.bit.com/knowledge-hub/mean-reversion)

### Inferences
- Rigour ranking for BTC price-based evidence:
  1. Peer-reviewed papers with out-of-sample tests and data-snooping control (Hudson & Urquhart: negative for BTC out-of-sample; Detzel et al.: positive out-of-sample for price/MA ratios).
  2. Practitioner working papers with ensembles and stated net-of-fee results (Concretum).
  3. Research-shop blogs with explicit rules but unclear costs (Quantpedia).
  4. Blogs and vendors.
  5. TradingView and exchange marketing.
- Common red flags: gross-only results on high-turnover rules (Concretum intraday, Quantpedia seasonality), single-parameter optimisation, short windows dominated by one bull run, and multi-coin results presented as if they applied to BTC alone (Talyxion, Man's 10–15-coin result).
- For a retail BTC bot, the strongest evidence points to a **daily-bar, long-only (or long/flat), multi-lookback trend system with volatility-targeted sizing**. It has low turnover (cost-robust at 0.10% spot fees) and is judged mainly on drawdown and Calmar improvement over buy-and-hold rather than higher CAGR. Intraday and seasonal strategies need maker execution and fresh out-of-sample validation before they are credible.

### Gaps
- Robot Wealth, Alpha Architect, Newfound Research, QuantConnect and Freqtrade community BTC backtests did not surface with BTC-specific numbers in my searches. Coverage of these sources is missing.
- I found no CTA or CME report quantifying how BTC futures contributed to managed-futures trend returns (e.g. in 2020–2021 or 2024).
- Man Group pages could not be fetched (DNS failure), so their numeric results (Sharpe, drawdowns, cost assumptions) are missing.
