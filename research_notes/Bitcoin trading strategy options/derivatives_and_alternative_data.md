# Bitcoin strategies using derivatives, market structure, order flow, alternative data and ML: evidence and feasibility for a small retail BTC-only bot

_How these notes were made (October 2026): the page-fetch tool could not reach any host (DNS failure), so every figure below comes from search-engine extracts of abstracts, snippets and articles, not from full papers I read myself. Where a number matters for a decision, check it against the primary source. The team's own assumptions are used in the inferences: spot fees about 0.10% maker/taker, perp fees about 0.02% maker / 0.05% taker, capital $1k–$50k, 50–500 ms latency._

---

## 1. Funding-rate carry and cash-and-carry basis (long spot BTC + short BTC perp, and dated-futures basis)

### Takeaway
The BTC carry trade earned double-digit yields in 2021–2024. Since then it has collapsed. BTC perp funding averaged about 11% in 2024, about 4.9% in 2025 and about 2.2% in 2026 up to 11 August. CME 3-month basis was about 2–4% in 2026, below US Treasury yields, and USDe supply shrank by about two-thirds. Once you account for the capital split between spot and margin, four-leg fees, rebalancing and exchange risk, a retail bot running BTC-only carry in 2026 would net roughly cash-like returns or less. It is technically the easiest strategy to build, but the yield is low right now and the risk does not show up most of the time and then arrives all at once.

### Cited Findings
**Academic evidence on carry size and risk**
- BIS Working Paper 1087 "Crypto carry" (Schmeling, Schrimpf, Todorov; first published April 2023, revised October 2025; also CEPR DP20719) defines crypto carry as the return on long spot plus short futures. The paper finds it averages above 10% a year and sometimes exceeds 40% a year. That is much larger than carry in equities, fixed income, FX or commodities. — [BIS WP 1087 landing page](https://bis.org/publ/work1087.htm); [CEPR DP20719](https://cepr.org/publications/dp20719)
- Another version of the paper describes carry as reaching "up to 60% p.a.". It also reports that **with 10x leverage the futures leg would have been liquidated in over half of the months in the sample**, and it names the lack of cross-margining between spot and futures accounts as central to that risk. — [BIS WP 1087 PDF](https://www.bis.org/publ/work1087.pdf) (via search extract)
- According to BIS, high carry comes from demand by smaller, trend-chasing investors who want leveraged upside, combined with limited arbitrage capital. Arbitrage is limited because margins and liquidations spike during drawdowns. **High carry predicts future price crashes**, and a 10% rise in standardised carry predicts a 22% rise in short-futures liquidations (as a share of open interest) over the next month. — [BIS WP 1087 PDF](https://www.bis.org/publ/work1087.pdf); [SSRN version](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4268371)
- BIS: the CME basis ranged from below −50% during the FTX collapse (November 2022) to above 45% just before the spot ETF launch (January 2024). — [BIS WP 1087 PDF](https://www.bis.org/publ/work1087.pdf) (via search extract)
- A ResearchGate listing says the paper was published in *Management Science* in 2026 (DOI 10.1287/mnsc.2024.05069). — [ResearchGate](https://www.researchgate.net/publication/404601341_Crypto_Carry)
- He, Manela, Ross and von Wachter, "Fundamentals of Perpetual Futures" (arXiv 2212.06888; v6 August 2024): crypto perp deviations from no-arbitrage prices are much larger than in traditional FX and **shrink as markets mature**. — [arXiv abstract](https://arxiv.org/abs/2212.06888v6)
- In one version, their random-maturity arbitrage on BTC reaches a **Sharpe of 3.35 under high retail-level trading costs** and 11.65 for fee-free market makers, falling to 3.27 and 10.46 after effective spreads. A secondary article cites different figures, BTC Sharpe 3.53 with zero fees and 1.80 with high retail costs. The two sets probably come from different paper versions, so they conflict. — [arXiv PDF](https://arxiv.org/pdf/2212.06888); [ResearchGate](https://www.researchgate.net/publication/366287738_Fundamentals_of_Perpetual_Futures)

**Funding-arbitrage studies that include costs**
- Werapun et al. (2025) studied BTC, ETH, XRP, BNB and SOL on Binance, BitMEX, ApolloX and Drift. They report funding arbitrage returns "up to 115.9% over six months" with a maximum loss of 1.92%. The study is multi-coin, and the extract does not say whether the figures are net of fees. — [ResearchGate](https://www.researchgate.net/publication/394323707_Exploring_Risk_and_Return_Profiles_of_Funding_Rate_Arbitrage_on_CEX_and_DEX)
- "The Two-Tiered Structure of Cryptocurrency Funding Rate Markets" (MDPI *Mathematics* 2026) covered an 8-day window in November 2025 across 26 venues (11 CEX, 15 DEX). **Only 40% of top opportunities were profitable after transaction costs and spread reversals**, and forced exits happened in 95% of opportunities. — [MDPI](https://www.mdpi.com/2227-7390/14/2/346)
- A Springer paper (2026) on CEX–DEX funding arbitrage as a basis trade used Binance data for 2021–2024 plus dYdX v4. Net annualised returns come mainly from funding carry but are "highly assumption-sensitive and should not be interpreted as frictionless arbitrage profits". Residual risks come from basis moves, index-composition differences and mark-price methods. — [Springer, Digital Finance](https://link.springer.com/article/10.1007/s42521-026-00213-3)

**Recent yields, 2024–2026**
- BTC perp funding averaged **11% in 2024, 4.9% in 2025 and 2.2% in 2026 through 11 August**. — [CryptoSlate](https://cryptoslate.com/ethena-is-targeting-the-120-trillion-wall-street-stocks-market-to-hunt-yields-5x-higher-than-bitcoin/)
- On 16 October 2026 a snapshot showed BTC funding at 0.0100% per 8 hours, about 10.9% annualised. That is the default baseline rate, a single-day reading and not a trend. — [TokenPost](https://tokenpost.com/news/investing/33874)
- The BTC basis reportedly peaked at 20–25% annualised in 2024 and fell to about 10% by mid-2025. — [bit.com](https://www.bit.com/insights/knowledge-hub/basis-trade)
- Amberdata's reconstruction shows the 30-day annualised basis peaking at 15.3% in January 2025 (seen only via a Substack summary). — [MEXC Learn Substack](https://mexclearn.substack.com/p/bitcoin-futures-basis-guide-contango)
- In 2026 the 3-month BTC futures basis was reported at about 3%, below Treasury yields, and at about 2.08% on 8 August 2026, down from 3.8% in February 2026. These are secondary sources. — [BigGo Finance](https://finance.biggo.com/news/9c11c1e7-4988-4ad7-998f-7d4f8a51f6ad)
- In August 2026, hedge funds on CME flipped from structural net shorts (the basis-trade hedge) to net long for the first time in years. — [CoinDesk, 10 Aug 2026](https://www.coindesk.com/markets/2026/08/10/a-rare-cme-shift-hedge-funds-abandon-structural-shorts-to-bet-on-a-bitcoin-rally); [The Coin Republic](https://www.thecoinrepublic.com/2026/08/10/cme-hedge-funds-flip-net-long-on-bitcoin-futures-for-the-first-time-in-years/)

**Ethena / USDe, the largest public carry vehicle**
- USDe supply reached nearly $15B in late 2025 and fell sharply after the October 2025 crash, when funding turned negative. — [bit.com](https://www.bit.com/insights/knowledge-hub/basis-trade)
- One source puts USDe supply below $5B in 2026 and says Ethena is moving towards equity perpetuals, where funding has averaged 13.9% against 3.9% for BTC. A Q1-2026 report gives $5.92B. — [Zipp](https://zippfeed.com/a/ethena-pivots-usde-basis-trade-into-equity-perpetuals); [Stablecoin Insider Q1 2026](https://stablecoininsider.org/ethena-usde-q1-2026-report/)
- sUSDe yields averaged about 18% APY in 2024 and 4–15% in 2025. One guide says 4–30% across 2024–25, mostly 8–18%. In late September 2026 the yield was about 4.76–5.0%. Sources disagree on the all-time low and high. — [eco.com](https://eco.com/support/en/articles/15254002-ethena-usde-and-susde-2026-delta-neutral-yield); [Stablecoin Insider review](https://stablecoininsider.org/ethenas-staked-usde-stablecoin/); [EarnPark](https://earnpark.com/en/posts/ethena-fees-apy-interest-rates-explained-2026/)
- When funding turns negative, sUSDe yield drops to zero first and a reserve fund covers the shortfall. That fund was about $62M in April 2026. — [Stablecoin Insider review](https://stablecoininsider.org/ethenas-staked-usde-stablecoin/)
- A 2024-era analysis citing Ethena data said only one quarter in the previous three years had negative average funding, and that quarter was distorted by the ETH PoW fork arbitrage. — [Chorus One](https://chorus.one/articles/ethena-delving-into-the-mechanics-and-risks-of-usde)

**How often funding is negative**
- In January 2025 BTC funding turned negative for the first time that year (about −0.001%), and only a few times since November 2024. On 10 March 2025 the daily rate reached −0.006%, about −2% annualised. — [CoinDesk, Jan 2025](https://www.coindesk.com/markets/2025/01/10/bitcoin-funding-rates-briefly-went-negative-usually-marks-a-local-bottom-van-straten); [CoinDesk, Mar 2025](https://www.coindesk.com/markets/2025/03/10/no-bottom-in-sight-as-bitcoin-funding-rate-swings)
- In early 2026 there was a multi-week negative stretch. As of 19 March 2026 it had lasted nearly three weeks, the longest since April 2025 (Gate, secondary). In April 2026 funding was the most negative since 2023, with heavy short positioning even as price rose. — [Gate](https://www.gate.com/blog/btc-negative-funding-rate-historical-bottom-market-signals-analysis); [CoinDesk, 16 Apr 2026](https://www.coindesk.com/markets/2026/04/16/bitcoin-funding-rates-hit-most-negative-since-2023-history-suggests-bottom-is-in)
- A CoinDesk piece (27 April 2026) reportedly gives the 30-day average funding at −5%. The extract was truncated, so treat it as unverified. — [CoinDesk, 27 Apr 2026](https://www.coindesk.com/markets/2026/04/27/as-the-bitcoin-price-rises-futures-may-look-bearish-but-they-re-not-analyst-says)
- A CoinCub headline reports funding at the 0.01% baseline for 78% of a quarter. The exchange, period and contracts were not visible in the extract. — [CoinCub](https://coincub.com/blog/perpetual-futures-funding-rates-78-of-a-quarter-at-0-01/)

**Mechanics on Binance and Bybit (third-party descriptions; official pages not retrieved)**
- Binance USDT-M default: an 8-hour interval settling at 00:00, 08:00 and 16:00 UTC. Funding = premium index (impact bid/ask against the index, time-averaged) + clamp(interest − premium), with a default interest of 0.01% per interval. Funding is paid between traders and Binance takes no fee. — [Coinvado 2026 guide](https://coinvado.com/en/posts/binance-futures-funding-rate-guide-2026/); [proofoftalk](https://proofoftalk.io/blog/perpetual-futures-funding-rates/)
- **Sources conflict on the funding cap for BTCUSDT**: ±0.3% (one 2026 guide); 0.75 × maintenance-margin ratio for about 34 major contracts and ±2% for others (another analysis); a generic ±0.05% (others). — [Coinvado](https://coinvado.com/en/posts/binance-futures-funding-rate-guide-2026/); [CoinCub](https://coincub.com/blog/perpetual-futures-funding-rates-78-of-a-quarter-at-0-01/)
- Binance, Bybit and OKX reportedly shorten the settlement interval (8h to 1h) when funding hits its cap (secondary claim). — [CoinCub](https://coincub.com/?p=14476)
- Bybit uses the same premium-index structure. For BTCUSDT the impact-margin notional is $200 ÷ initial margin rate at maximum leverage, for example $25,000 at 125x / 0.8%. The interest component is 0.03% a day (0.01% per 8 hours). — [Coinglass learn](https://www.coinglass.com/ru/learn/funding-rates-1); [bybt.com learn](https://bybt.com/learn/funding-rates-1)

**Tail and counterparty risk: the 10 October 2025 crash**
- More than $19B of leveraged positions were liquidated within hours. Sources link the trigger to the US 100% tariff announcement on China. — [CoinGecko](https://www.coingecko.com/learn/october-10-crypto-crash-explained); [FTI Consulting](https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)
- **Auto-deleveraging (ADL) forcibly closed profitable positions, including the winning shorts that delta-neutral traders hold as hedges.** Some firms could not place risk-reducing orders for nearly two hours. — [Forbes](https://www.forbes.com/sites/boazsobrado/2025/10/21/locked-out-and-liquidated-traders-blame-binance-for-19-billion-crash/); [edgeX](https://pro.edgex.exchange/en-US/news/article/crypto-auto-deleveraging-risks); [insights4vc](https://insights4vc.substack.com/p/inside-the-19b-flash-crash)
- Binance reportedly used about $188M from its insurance fund and compensated some users. Reports of the refund amount differ (about $280M in one account). There are unconfirmed allegations that Ethena's hedges were shielded from ADL. — [CCN](https://www.ccn.com/education/crypto/oct-10-crypto-flash-crash-exchanges-whales-traders-who-lost/); [edgeX](https://pro.edgex.exchange/en-US/news/article/crypto-auto-deleveraging-risks)
- On Hyperliquid, more than 1,000 wallets were fully liquidated and about $1.23B of trader capital was lost. — [CoinDesk](https://www.coindesk.com/markets/2025/10/11/largest-ever-crypto-liquidation-event-wipes-out-6-300-wallets-on-hyperliquid)

### Inferences
- **Baseline arithmetic.** 0.01% per 8 hours × 3 × 365 = 10.95% a year. When funding sits at the default, the gross carry is about 11% on the hedged notional. The 2025–2026 averages (4.9%, 2.2%) mean funding often sat below that baseline or turned negative.
- **Capital split.** Hedging notional N needs N in spot plus margin of N/L for the short perp. Yield on total capital = funding × L/(L+1). At 1x that is funding/2; at 2x, 2/3 of funding; at 3x, 3/4. Higher L moves the short's liquidation price closer, and BIS shows liquidation of the futures leg was common at 10x. At 2x a short is liquidated only on a rise of roughly 45–50%, but long BTC bull runs reach that.
- **Gross yield on capital at 2x:** about 7.3% (2024 average), about 3.3% (2025), about 1.5% (2026 year-to-date).
- **Four-leg fees with the team's assumptions:** buy spot 0.10% + short perp 0.02–0.05%, then sell spot 0.10% + cover perp 0.02–0.05%, which is **about 0.24–0.30% of notional per round trip**. That is small if the position is held a full year. If the bot exits whenever funding turns negative and re-enters later (in 2025–26 that could mean several round trips), fees can take a large share of the 2–5% gross. Rebalancing margin as BTC rises (moving spot gains into perp collateral) adds more fees or transfers.
- **Negative funding** means the short pays. In 2025–2026 there were multi-week negative stretches, so a static hedge pays out during those periods.
- **Feasibility verdict: technically feasible, economically weak in 2025–2026, and the risk only shows up in crashes.** It is simple to build with CCXT (spot buy + perp short, monitor margin) and needs no fast infrastructure. But BTC-only carry in 2026 yields about 1–3% on capital after the split and fees, below the reported basis-trade yields that already sit under Treasuries. Ethena's move away from BTC towards equity perps shows the large carry players reached the same conclusion. The risks are exchange counterparty risk (both legs usually sit on one CEX), ADL removing the hedge, account lockouts during crashes, and liquidation of the perp leg when spot and perp margin are separate. Reasonable as an opportunistic module that turns on only when funding is well above baseline. Not something to run all the time.
- **Dated-futures basis** (for example Binance/Bybit quarterly contracts or CME) fixes the yield at entry and removes the risk of funding flipping, but 2026 basis levels (about 2–4%) are just as unattractive. CME needs a regulated futures broker and a contract size well above this team's capital (not verified here).
- "Reverse" carry (long perp, short spot when funding is negative) needs margin-borrowing of BTC, which adds borrow cost and complexity. The He et al. Sharpe ratios assume both directions can be traded and should not be used for a long-spot/short-perp-only setup.

### Gaps
- BIS sample period and net-of-cost strategy returns or Sharpe were not visible in the extracts. A commentary notes the paper does not compute a tradable net strategy.
- The official Binance and Bybit BTCUSDT funding cap and floor, and whether the interval changes at the cap, are unresolved because sources conflict. Check the exchange funding-rate history and contract specification pages or the API (e.g. `fapi/v1/fundingInfo`).
- I did not find a clean "percentage of 8-hour periods with negative BTC funding" for 2024–2026. The team can compute it from CCXT `fetchFundingRateHistory`.
- Whether Bybit's Unified Trading Account or Binance Portfolio Margin lets spot BTC collateralise a USDT-M short at retail size (which would improve capital efficiency) was not researched.
- Coinglass and Laevitas historical funding pages could not be fetched.

---

## 2. Funding rate, open interest, long/short ratio and liquidations as directional signals

### Takeaway
There is little rigorous evidence that these metrics predict short-horizon BTC direction. The best academic result (BIS) is that **high carry predicts crashes and short liquidations at roughly a monthly horizon**. One simple regression of 8-hour returns on funding found R² of 0.003. "Extreme negative funding marks bottoms" claims rest on a handful of episodes. Liquidation early-warning signals differ from one cascade to the next. Useful as a risk filter (cut exposure when leverage looks crowded). Not proven as a standalone entry signal.

### Cited Findings
- BIS: high crypto carry predicts future price crashes, and a rise in carry goes together with a higher price of crash-risk insurance. A 10% rise in standardised carry predicts a 22%-of-open-interest rise in short-futures liquidations over the next month. — [BIS WP 1087 PDF](https://www.bis.org/publ/work1087.pdf)
- Fulgur Ventures regressed 8-hour BTC returns on BitMEX funding and found a slight negative relationship with **R² = 0.003**, which explains almost none of the variance. — [Fulgur Ventures (Medium)](https://medium.com/@fulgur.ventures/bitcoin-funding-rates-and-price-predictability-27ce95535af1)
- A practitioner backtest of funding-based signals over 6.7 years of BTC reported results "opposite of what we expected". The statistics were not visible. — [tradingstrategies.work](https://tradingstrategies.work/blog/funding-rate-signal-btc-backtest)
- Anecdotal claims: CoinDesk (January 2025) says negative funding "usually marks a local bottom". Another piece lists six episodes in 2022–2025 where negative lows came before rebounds. These are small samples with no significance tests. — [CoinDesk](https://www.coindesk.com/markets/2025/01/10/bitcoin-funding-rates-briefly-went-negative-usually-marks-a-local-bottom-van-straten); [CryptoRank](https://cryptorank.io/news/feed/fab7b-bitcoin-negative-funding-rate-rebound)
- Counter-example: in April 2026 funding was the most negative since 2023 *while price trended higher* (heavy short positioning). 10x Research argued that the bearish-looking futures data was misleading. — [CoinDesk, 16 Apr 2026](https://www.coindesk.com/markets/2026/04/16/bitcoin-funding-rates-hit-most-negative-since-2023-history-suggests-bottom-is-in); [CoinDesk, 27 Apr 2026](https://www.coindesk.com/markets/2026/04/27/as-the-bitcoin-price-rises-futures-may-look-bearish-but-they-re-not-analyst-says)
- A 2026 arXiv preprint studied seven crypto-perp liquidation cascades using Binance BTCUSDT data. **Early-warning signals (variance, lag-1 autocorrelation) are "event-heterogeneous"**, meaning they differ across episodes. Intraday open interest fell 24.6% across one cascade. The paper notes Binance has stopped publishing per-event `liquidationSnapshot` dumps, and that 8-hour funding is "far too coarse" for intraday early warning. — [arXiv 2607.27070](https://arxiv.org/html/2607.27070v1)
- Industry commentary says open interest and funding showed leverage building before the October 2025 trigger, but the trigger itself could not be predicted (opinion, not a test). — [XT.com (Medium)](https://medium.com/@XT_com/bitcoin-futures-market-microstructure-liquidation-cascades-funding-regimes-and-open-interest-978b107b4889)
- An SEC comment letter (August 2026) cites a Binance study where short-perp/long-spot earned high realised returns, and a BitMEX liquidation study. I saw these only through the letter. — [SEC comment letter](https://www.sec.gov/comments/S7-2026-21/s7202621-1011079-3235289.pdf)

### Inferences
- The robust signal is about *risk*, not direction: when funding or basis is very high, crash and liquidation risk goes up over weeks. A bot could cut long exposure or leverage when funding stays far above the 0.01% baseline. Back this rule out of sample before relying on it.
- Fading extreme funding at the 8-hour horizon looks close to zero edge (R² 0.003). Once taker fees and slippage are paid, it is unlikely to survive.
- Liquidation data is hard to get historically for free (Binance dumps discontinued). A bot would need to record liquidation streams itself, so backtesting this kind of signal needs months of self-collected data.
- **Feasibility verdict:** easy and free to collect (funding and open-interest history via CCXT; long/short ratio via exchange endpoints). **Use as a regime or risk filter, not as a primary alpha source.** Treat any strategy built mainly on these signals as unproven until walk-forward tested.

### Gaps
- I found no peer-reviewed study of the **long/short ratio** (Binance top-trader or global accounts) as a BTC return predictor.
- I found no rigorous test of "liquidation cascade then reversal" entry rules with costs.
- The full results of the tradingstrategies.work backtest were not visible.

---

## 3. Grid trading and passive market making on BTC/USDT

### Takeaway
A grid bot is in effect short volatility and mean-reverting. It profits while BTC stays inside a range and falls behind or loses badly when price trends out of it. An academic analysis concludes a plain grid has **roughly zero expected value before fees and therefore negative after fees**, unless it has some view on trend. Passive market making by a non-colocated retail bot faces documented adverse selection and picking-off risk, and the maker-rebate VIP tiers need volume far beyond this team's capital. Neither is a good fit.

### Cited Findings
- "Dynamic Grid Trading Strategy: From Zero Expectation to Market Outperformance" (arXiv 2506.11921): without trend information, **plain grid trading has effectively zero expected value**, so "investors face a high risk of losing money after taking transaction fees into consideration". The authors' own dynamic variant beat buy-and-hold and standard grids in backtests from 2021 to July 2024. This is the authors' proposal and has not been independently replicated. — [arXiv 2506.11921](https://arxiv.org/pdf/2506.11921)
- An individual backtest of popular Binance grid configurations over 4 years found the grid returned **−35% (max drawdown −39%) in the 2022 crash against −65% buy-and-hold**, and **+7% in the 2024 bull run against +127% buy-and-hold**. This is one person's work and not peer-reviewed. — [DEV Community](https://dev.to/aduenasdev/i-backtested-the-most-popular-binance-grid-bots-on-4-years-of-real-data-1gnb)
- A vendor reports that for a BTC grid with a ±15% range, price left the range in 23% of 30-day periods in 2020–2025, and warns that "too many [grids] and fees consume your profits". This is commercial material. — [Freya Finance](https://www.freyafinance.com/academy/strategy-guides/grid-bot-profitability-real-market-analysis)
- A Stevens Institute student project with Quantm Capital, using Bybit data, found ML integration did not beat traditional grid methods, while a hedged grid did better than holding BTC. Not peer-reviewed. — [Stevens FSC](https://fsc.stevens.edu/cryptocurrency-market-making-improving-grid-trading-strategies-in-bitcoin/)
- A Bollinger-band "range" backtest lost 12.70% over six months with 0.1% fees, mostly in the directional moves of early 2026. Not a true grid. — [CoinQuant](https://www.coinquant.ai/blog/grid-trading-strategy-explained-how-to-set-it-up-and-backtest-it)
- **Adverse selection in crypto:** a study of Bitfinex order and trade data finds statistically significant adverse-selection costs in the spreads of major cryptocurrencies. — [Tiniç & Sensoy, "Adverse Selection in Cryptocurrency Markets"](https://nottingham-repository.worktribe.com/OutputFile/40584797)
- In abrupt crashes, makers' stale bids get "aggressively lifted, leading to significant losses before they can adjust quotes". A tested market-making strategy suffered catastrophic losses in a flash crash. — [arXiv 2602.00776](https://arxiv.org/html/2602.00776v1)
- General theory: limit orders that rely on imbalance predictions face latency and adverse-selection risk. Imbalance-based predictions typically do not beat spread plus fees. — [arXiv 1610.00261](https://arxiv.org/pdf/1610.00261)
- Binance futures fees depend on VIP level. **The futures VIP volume requirement is 5× the spot one**, and paying fees in BNB gives a 10% discount on USDⓈ-M. — [Binance support](https://www.binance.com/uz-UZ/support/articles/360033544231)
- Third parties disagree on the base and tier thresholds. Base is about 0.02% maker / 0.05% taker (one source; another lists a 0.04% maker fee). VIP1 is variously given as 5 BNB plus $5M of 30-day futures volume, or a $15M futures gate. — [Analytics Insight](https://www.analyticsinsight.net/cryptocurrency-analytics-insight/crypto-exchange-vip-programs-and-fee-tiers-compared-2026); [Traders Union](https://tradersunion.com/brokers/crypto/view/binance/futures-fees/); [DEV fee JSON](https://dev.to/jacktrader/i-open-sourced-every-binance-and-okx-2026-fee-tier-as-json-a-calculator-fnj)

### Inferences
- **Grid payoff:** each completed buy-low/sell-high cycle earns the grid spacing minus two fees. On spot at 0.10% per side, spacing must be well above 0.2% to earn anything. Tighter grids trade more and pay more fees. When price breaks out upward the grid ends up holding mostly USDT and misses the rally. When it breaks out downward it ends up holding mostly BTC bought on the way down. That matches the documented +7% vs +127% (2024) and −35% vs −65% (2022) profile.
- **Why exchanges promote grids** (my reading, no source found): grids create steady trading volume and fees for the venue, and the payoff looks good in ranging markets (many small wins), which retail users find attractive.
- **Market-making feasibility:** at $1k–$50k, reaching even a $5–15M/month futures VIP1 tier means turning over capital about 100–15,000 times a month. Maker rebates are out of reach. Without rebates, a quote at the touch earns at most the BTC/USDT spread (usually a single tick on major venues, not verified here) and pays maker fees. At 50–500 ms latency the bot cannot cancel quickly enough to avoid being picked off by faster participants.
- **Feasibility verdict: grid = feasible to build, poor expected value.** It is mainly a bet that BTC stays in a range, with fees working against it. Only consider it as an explicit volatility-harvesting sleeve with a hard range exit, and backtest it on 2024–2026 data with real fees. **Passive market making = not feasible** for this setup: no colocation, no rebates, documented adverse selection, and crash picking-off risk.

### Gaps
- I found no peer-reviewed, cost-inclusive study of exchange-native grid bots (Binance, Bybit, Pionex) on BTC, and no audited aggregate performance data from any exchange for its grid users.
- Current official Binance and Bybit VIP thresholds and any retail-accessible maker-rebate programmes were not confirmed from primary pages.

---

## 4. Order-book and order-flow signals (order book imbalance, trade flow imbalance, CVD)

### Takeaway
Order-book imbalance carries statistically detectable information about BTC price moves over **seconds to a few minutes**. But the effects are tiny (R² often below 1–2%), unstable across samples and sensitive to the fee regime. The literature repeatedly finds they do not cover spread plus fees. At 50–500 ms latency with 0.05% perp taker fees, a retail bot is very unlikely to monetise them. CVD and trade-flow imbalance have even weaker evidence.

### Cited Findings
- Schmalz (SSRN, 2025–26) tested order-flow imbalance (OFI) on BTC/USDT at 1–10 second horizons. **Out of sample, the result reversed as the sample grew.** On about 7 days OFI had significant positive R² of 0.17–1.00%. On about 9 days the pooled result was null or negative at every horizon. **Trade-flow imbalance was never significant**, and a simple AR(1) matched or beat OFI at every horizon except 10 seconds. — [SSRN 7227998](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7227998)
- When Binance moved BTC/USDT from zero to commission-based fees (March 2023), **OFI's explanatory power for price changes rose from about 5% to 21.55% R²**. The authors suggest zero fees diluted the information in order flow. This is a *contemporaneous* explanatory R², not a forecast. — [Springer chapter, "Fee Structure and Order Flow Informativeness"](https://link.springer.com/chapter/10.1007/978-3-032-18109-1_13)
- A Charles University thesis on Binance futures data finds bid-ask imbalance measures have statistically significant effects on short-interval returns. It acknowledges that transaction costs, latency and adversarial algorithms limit profitability. — [Charles University thesis](https://dspace.cuni.cz/bitstream/handle/20.500.11956/200516/120505902.pdf?sequence=1)
- In general limit-order-book markets, "the expected value of buying and selling back using accurate predictions based on sizes at first limits does not beat transaction costs (bid-ask spread and fees)". — [arXiv 1610.00261](https://arxiv.org/pdf/1610.00261)
- A 2026 gradient-boosting and SHAP study across five cryptos finds OFI has a largely monotone effect, concave at extremes, and that wider spreads go with less predictability. — [arXiv 2602.00776](https://arxiv.org/html/2602.00776v1)
- A 2026 SSRN methods paper stresses separating true predictability from the mechanical same-interval effect of trades on price, and requires realistic costs and data-snooping controls. — [SSRN 6938742 (Vafin)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6938742)
- Fragmentation and cross-impact matter for BTC price formation across venues. — [arXiv 2108.09750](https://arxiv.org/pdf/2108.09750)

### Inferences
- The horizons where the signal exists (1–10 seconds) are the ones where 50–500 ms latency plus a VPS round trip use up a large share of the window. Any edge has to beat a 0.10% round-trip taker cost on perps (0.20% on spot), which is far larger than typical expected moves at these horizons.
- Coarser versions such as 1–5 minute CVD or imbalance may still help as **execution aids** (for example, delaying a planned entry when the book is heavily one-sided). They are not a standalone strategy.
- **Feasibility verdict: not feasible as an alpha source** for this setup. At most a minor execution-timing input. Collecting L2 data via websockets is free, but storing and replaying it is non-trivial.

### Gaps
- I found no study that measures BTC order-flow edge specifically under 50–500 ms retail latency with realistic queue position.
- I found no rigorous evidence on CVD specifically (it appears mainly in practitioner content).

---

## 5. Arbitrage (cross-exchange spot, triangular, spot–perp)

### Takeaway
For a retail bot in 2026 the answer is largely **no**. Cross-exchange BTC spreads on major venues are thin, fees on both venues plus withdrawal or transfer friction remove most of the profit, and the space is bot-dominated. Triangular arbitrage needs several currency pairs and is dominated by professional bots. "Spot–perp arbitrage" is the carry trade from section 1.

### Cited Findings
- On-chain arbitrage (mostly DEX) over the year to late August 2026: about 139M trades and about $95.8M of profit after fees once filtered (about $0.69 per trade), against about $762M counted naively. **Ethereum's annual arbitrage take fell about 94% from its 2021 peak.** — [Bitquery](https://bitquery.io/investigations/crypto-arbitrage-69-cents)
- Typical cross-exchange spreads on major venues are now about 0.1–2%, down from the double-digit gaps of 2021–2023. With 0.1% taker fees, a gap of at least 0.2% is needed just to break even. This is a vendor or affiliate-type source. — [Opportuna](https://opportuna.io/blog/is-arbitrage-profitable)
- Withdrawal limits and delays and bot competition compress margins until "small accounts struggle to profit meaningfully after costs". — [EarnPark](https://earnpark.com/en/posts/xrp-arbitrage-can-you-still-profit-in-2026/); [Ventureburn (partly sponsored)](https://ventureburn.com/what-is-crypto-arbitrage/)

### Inferences
- BTC/USDT is the most heavily arbitraged pair in crypto. Spreads between Binance and Bybit for BTC are likely to sit below the combined ≥0.2% taker cost most of the time. Capturing the rare dislocations (for example during the October 2025 crash) means holding inventory on both venues, which doubles counterparty exposure, and those are exactly the moments when exchanges lock users out.
- Triangular arbitrage (for example BTC/USDT, BTC/USDC, USDC/USDT) technically keeps BTC as the only risky asset, but it is a sub-millisecond, colocated game.
- **Feasibility verdict: not feasible.** Spot–perp is covered by the carry analysis in section 1.

### Gaps
- I found no academic study of retail CEX–CEX BTC arbitrage profitability for 2024–2026. Kaiko and Paradigm 2025 reports were mentioned but not retrieved.

---

## 6. On-chain signals (MVRV / MVRV-Z, SOPR, NUPL, exchange net flows, miner flows, hash ribbons, Puell, stablecoin supply): predictive power, data access and cost

### Takeaway
On-chain valuation metrics (MVRV-Z, NUPL) have mainly **in-sample, multi-year cycle-timing** evidence, from a handful of cycles. The best peer-reviewed test reports Sharpe improving from 0.45 to 1.28, yet **none of its exit thresholds triggered in the 2022–2025 cycle**. Exchange net flows have weak predictive power for BTC returns intraday. Hash ribbons and Puell rest on originator claims from about 9–20 signals. These are slow, low-frequency regime indicators, not trading signals, and the main daily metrics are available free or cheaply (BGeometrics free tier, CryptoQuant from about $29–$109/month). I found no evidence that CoinMarketCap provides any of these on-chain metrics.

### Cited Findings
**Evidence**
- Grobys (peer-reviewed, ScienceDirect 2026) tests NUPL, MVRV-Z and CVDD as rule-based strategies over three BTC cycles. **Sharpe rose from 0.45 (buy-and-hold) to 1.28 with MVRV-Z.** This is a cycle-based backtest. **In the latest cycle (2022–2025) none of the strategies reached their exit thresholds.** — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0275531926002138); [PDF](https://iris.unito.it/retrieve/8e104076-d79e-4df7-a1fe-1f86d7630c41/1-s2.0-S0275531926002138-main.pdf)
- Chi, Chu and Hao (arXiv 2411.06327): **BTC exchange net inflows "generally lack predictive power for BTC returns (except at 4 hours)"** but are negatively associated with volatility at all intraday intervals. ETH net inflows predict ETH returns strongly. — [arXiv 2411.06327](https://arxiv.org/pdf/2411.06327)
- A 2026 arXiv review notes that on-chain signal selection is regime-specific and that exchange-level order-flow signals remain untested under proper multi-regime evaluation (attribution taken from the search summary). — [arXiv 2606.00071](https://arxiv.org/pdf/2606.00071)
- Hash ribbons (Charles Edwards / Capriole, 2019): the originator reports 9 historic buy signals with an average gain to the next cycle peak above 5,000% and an average maximum drawdown of 11% per entry. It also says most drawdowns are removed by waiting for the 10-day SMA to cross above the 20-day SMA (a price filter). The author's own disclaimer says backtests use hindsight. — [Capriole](https://capriole.com/hash-ribbons-bitcoin-bottoms)
- Hit-rate claims for hash ribbons conflict: about 85% of about 20 signals since 2011 marked local bottoms (one guide) versus about 64% profitable since 2013 (another). After a signal, drawdowns of 3–42% have occurred. Some argue miner selling matters less now that ETFs and corporate holders are large. I found no out-of-sample test of hash ribbons or the Puell multiple. — [Spark glossary](https://www.spark.money/glossary/hash-ribbon); [Axel Adler Jr](https://axeladlerjr.com/bitcoin-hash-ribbons-capitulation-signals-buy-triggers/); [Cointelegraph](https://cointelegraph.com/news/bitcoin-hash-ribbons-flash-buy-signal-90k-will-btc-price-rebound?rand=6792)
- **Stablecoin supply:** no consensus on causality. Griffin and Shams linked Tether issuance to price support, while Wei found no causal effect of Tether issuance on BTC returns. Some studies argue issuance *responds* to demand in bull markets (reverse causality). A stress-period study finds crypto returns Granger-cause USDC depegs, not the reverse. — [arXiv stablecoin survey 2507.13883](https://arxiv.org/pdf/2507.13883); [MDPI stress-period study](https://www.mdpi.com/2674-1032/5/3/68)
- A VAR preprint finds USDT and USDC *peg deviations* Granger-cause BTC returns (not supply growth). — [ResearchGate](https://www.researchgate.net/publication/399220796_The_Impact_of_Stablecoins_on_Bitcoin_Returns_An_Empirical_Analysis_Based_on_VAR_Model)

**Data availability and cost**
- **BGeometrics / bitcoin-data.com free plan:** no token needed; 8 requests/hour, 15/day; **4 years of history**; endpoints include `/v1/mvrv`, `/v1/mvrv-zscore`, `/v1/sopr`, `/v1/sth-sopr`, `/v1/lth-sopr`, `/v1/asopr`; 248+ metrics. A paid tier gives 200/hour, 400/day and full history (one source lists $8/month). BGeometrics charts are free with no registration. — [bitcoin-data.com free plan](https://bitcoin-data.com/bguser/free-features.html); [bitcoin-data.com](https://bitcoin-data.com/); [BGeometrics](https://bgeometrics.com/)
- **Glassnode:** there is no free API (the free Standard tier is web-only, with delayed data). **Studio Advanced costs $49/month billed yearly or $99/month monthly, with a throttled "API Light" of 50 calls/day, 14 days of history and daily resolution.** The full API starts at Professional (about $999/month billed yearly, with the API as an add-on or through sales). These are third-party figures. — [costbench](https://costbench.com/software/onchain-analytics/glassnode/); [cryptint](https://cryptint.io/compare/glassnode); [comparedge](https://comparedge.com/tools/glassnode/pricing)
- **CryptoQuant:** Advanced about $29–39/month; **Professional about $99/month yearly or $109/month monthly, including on-chain API access and minute-level data**; Premium $799/month. The API is moving to a prepaid credit model. These are third-party figures. — [costbench](https://costbench.com/software/onchain-analytics/cryptoquant/); [thegodfunded](https://thegodfunded.com/en/tools/cryptoquant/); [CryptoBriefing](https://cryptobriefing.com/cryptoquant-api-upgrade-rate-limits/); [CryptoQuant docs FAQ](https://docs.cryptoquant.com/guides/faq)
- Other free or cheap options that turned up: checkonchain charts, the Bitcoin Research Kit (BRK) API at bitview.space, and Newhedge (preview only; full history paid). Glassnode metrics are also resold through an Apify wrapper from $5 per 1,000 data points. — [checkonchain](https://charts.checkonchain.com/); [BRK API](https://bitview.space/api); [Newhedge](https://newhedge.io/bitcoin/mvrv); [Apify](https://apify.com/nabeelbaghoor/onchain-crypto-metrics-api)
- **CoinMarketCap:** the Basic (free) plan gives 15,000 call credits a month and 50 requests a minute (one source says 30 a minute). It includes CMC's proprietary indices, including **CMC's own Fear & Greed** (latest and historical). A derivatives section (open interest, funding, basis) exists, but which plans include it is unclear. — [CMC academy, free tiers](https://coinmarketcap.com/academy/article/best-free-crypto-api-in-2026-free-tier-comparison); [CMC API FAQ](https://coinmarketcap.com/api/faq/); [altFINS CMC API review](https://altfins.com/knowledge-base/coinmarketcap-api/)

### Inferences
- MVRV-Z and NUPL thresholds change only every few months. Each signal has 3–4 data points per decade, and the latest cycle never reached the classic "overheated" thresholds (Grobys). That suggests the thresholds are drifting as BTC matures and becomes ETF-held. These metrics suit **slow position sizing or regime tilts** (for example, scale exposure down when MVRV-Z is very high) rather than trade timing.
- For a bot, the daily MVRV, SOPR and NUPL values from the free BGeometrics tier (15 calls/day) are enough if the bot polls once a day and caches. Glassnode's $49 tier (14 days of history over the API) is useless for backtesting, so build history from BGeometrics or a one-off CryptoQuant month instead.
- CoinMarketCap does not appear to supply on-chain metrics, so on-chain data would be a second, free data source rather than a second paid aggregator. The team should confirm that this fits its "one aggregator" decision, since BGeometrics and CryptoQuant are on-chain analytics providers rather than price aggregators.
- **Feasibility verdict: feasible and cheap as a slow regime overlay. Not a standalone trading strategy.** Expect it to change little over a 1–2 year bot lifetime.

### Gaps
- I found no out-of-sample academic test of SOPR, Puell, hash ribbons, or miner-flow signals.
- Coin Metrics Community API terms and limits and Blockchain.com chart API coverage were not found in my searches.
- I found no confirmation that CoinMarketCap's Basic plan includes derivatives (open interest and funding) endpoints. Check the CMC endpoint docs.
- Whether BGeometrics' $8/month tier includes on-chain or only price data is ambiguous in the extract.

---

## 7. Sentiment and flow signals (Fear & Greed, Google Trends, social sentiment, spot ETF flows, stablecoin flows)

### Takeaway
The evidence is mixed and mostly weak. Fear & Greed contrarian rules show only small edges before costs in BTC-specific tests (one test: 1,145% against 1,046% buy-and-hold, ignoring fees and taxes). Social-media sentiment predicts returns only at very short horizons and mainly around the 2017 bubble. Most of a 141-predictor "zoo" fails out of sample. ETF-flow studies find **returns predicting flows** at least as strongly as the reverse, and the flow-to-return coefficient shrinks about threefold once timestamps are aligned correctly. These work as context or filters at most.

### Cited Findings
**Fear & Greed**
- The Alternative.me index components and weights are volatility 25%, momentum/volume 25%, social media 15%, surveys 15% (**currently paused**), BTC dominance 10% and Google Trends 10%. Sources disagree on whether there are five or six components. — [StealthEX](https://stealthex.io/blog/crypto-fear-and-greed-index/); [DEXTools](https://www.dextools.io/tutorials/what-is-fear-and-greed-index-crypto-guide-2026)
- A Springer chapter (20 largest non-stablecoin cryptos, February 2018 to December 2021) found contrarian Fear & Greed strategies "may generate significantly better results" than passive holding. It is not BTC-only. — [IDEAS/RePEc](https://ideas.repec.org/h/spr/eurchp/978-3-031-36286-6_16.html)
- BTC test from February 2018: buy 1% of capital when the index is ≤20 and sell 1% when ≥80. It returned **about 1,145% against about 1,046% buy-and-hold, excluding fees and taxes**, and needed careful scaling in and out. — [Bitcoin Magazine](https://bitcoinmagazine.com/markets/how-a-bitcoin-fear-and-greed-index-trading-strategy-beats-buy-and-hold-investing)
- The most consistent BTC gains came during "Neutral" sentiment rather than extreme fear, which challenges a simple contrarian reading. — [CCN](https://www.ccn.com/analysis/business/warren-buffetts-fear-and-greed-strategy-in-crypto/)

**Social and search predictors**
- "A Comprehensive Look at Bitcoin Return Predictability" (daily data, September 2014 to April 2025) tests 141 technical, fundamental, macro and sentiment predictors, including Google Trends and Twitter. **67 are useful in-sample, 29 give significant out-of-sample gains at one or more horizons, and only 4 beat the random walk at all horizons.** A second search could not confirm the "4" figure from the full text. — [ResearchGate](https://www.researchgate.net/publication/396908181_A_Comprehensive_Look_at_Bitcoin_Return_Predictability)
- StockTwits (about 1M messages): sentiment predicts BTC returns significantly at frequencies **up to 15 minutes only**. The relation disappears at lower frequencies and is concentrated around the 2017 bubble. — [ScienceDirect, Finance Research Letters](https://www.sciencedirect.com/science/article/abs/pii/S1544612319314199)
- Cheah et al. (33 predictors): volatility-scaled time-series momentum and uncertainty measures (EPU, financial uncertainty) performed best. — [NTU repository](https://irep.ntu.ac.uk/id/eprint/41292/1/1374791_Cheah.pdf)
- Google search interest in Bitcoin has not returned to its 2020–2021 levels (descriptive only). — [Bitcoin.com News](https://news.bitcoin.com/google-trends-data-shows-bitcoin-quietly-holding-its-place-as-the-year-comes-to-a-close/)

**Spot ETF flows**
- Fabus et al. (SSRN): pairing day-t flows with the day-t UTC return gives **4.89 percentage points per $1B of net inflow**. Aligning the return window to the 24 hours *after* the ETF session close **cuts this to 1.67**. The reverse channel (prior BTC returns predicting same-day flows) is the stronger one. — [SSRN 7545019](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7545019)
- Lim (SSRN, April 2026): causality runs both ways. Flows explain 21% of daily return variation, and there is no reversal in post-flow cumulative returns at horizons of 1–20 days. — [SSRN 6592830](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6592830)
- FalconX (early ETF period): Granger-significant but modest, with correlation 0.30. — [FalconX](https://www.falconx.io/newsroom/what-can-spot-etf-flows-tell-us-about-the-trajectory-of-bitcoin-prices-a-preliminary-statistical-investigation)
- Cointegration between ETF assets and BTC price is significant only at 10% (short sample of about one year). — [ResearchGate](https://www.researchgate.net/publication/398763174_From_Flows_to_Value_Cointegration_Between_Bitcoin_Spot_ETF_Assets_and_Bitcoin_Price)

**Stablecoin flows:** see section 6. There is no consensus that supply growth leads BTC returns, and reverse causality is plausible. — [arXiv 2507.13883](https://arxiv.org/pdf/2507.13883)

### Inferences
- Fear & Greed is free (Alternative.me API, and CMC's own index on the Basic plan). A slow contrarian tilt (scale in during extreme fear, trim in extreme greed) is cheap to add. But BTC-specific evidence shows only about a 10-percentage-point edge over about 7 years *before* costs, which makes it a weak signal.
- ETF flow data (e.g. Farside) is published after the US session. Fabus et al. show that the tradable, correctly aligned effect is about one-third of the naive one, and much of the relationship runs from price to flows. A next-day flow-momentum signal might carry some information, but it is not established.
- **Feasibility verdict:** Fear & Greed and ETF flows are **feasible as cheap, slow filters**. Social-sentiment NLP is **not worth building** (short-horizon only, faded after 2017, needs paid data or APIs). None should be a primary strategy.

### Gaps
- I found no BTC-only, cost-inclusive, out-of-sample Fear & Greed study covering 2022–2026.
- I found no subsample test of whether Google Trends or Twitter predictability declined after 2020.
- I found no study using Farside data specifically, and no tested rule for trading on ETF-flow announcements.

---

## 8. Machine learning for BTC prediction (2019–2026), and LLM trading agents

### Takeaway
The best recent evidence is consistent. ML models (XGBoost, LSTM, transformers) can show positive *gross* out-of-sample results on BTC, but **naive signal-following strategies fail once realistic costs (about 10–30 bps) are applied**. A cost-aware trade filter can restore positive net results in some configurations, **but not with statistical significance against buy-and-hold**. High classification metrics (AUC about 0.9) can coexist with heavy trading losses. LLM agents in the Alpha Arena live competition mostly lost money over a 17-day window. ML is a tool for filtering and sizing, not a reliable source of edge.

### Cited Findings
- **Bysik & Ślepaczuk (arXiv 2606.00060, May 2026):** about 70,000 hourly BTC/USDT observations (2018–2026), XGBoost, LSTM and iTransformer, a 27-fold walk-forward (12 months train, 3 validate, 3 test), 10 bps per trade. **Naive sign-based strategies fail after costs.** A cost-aware threshold cut turnover by more than 10× and restored positive net performance in *selected* XGBoost setups. The best was an XGBoost long-only strategy with annualised return above 65% and Sharpe above 1. However, **bootstrap Sharpe comparisons against the passive benchmark do not reject the null**, and performance is uneven across regimes. XGBoost was descriptively better than the neural nets, but not significantly. — [arXiv 2606.00060](https://arxiv.org/abs/2606.00060)
- **Jadouli (arXiv 2607.19453, July 2026):** an audit of candle-based Binance spot timing models. An OHLCV model reached **ROC-AUC 0.874–0.896 but average precision only about 0.12–0.13, and lost 44.30% over seven cycles**. A frozen ten-pair daily selector lost 6.72% over 19 July cycles at a 31 bps cost (3 wins, 16 losses), "conditional on extensive predecessor search". Gross advantages of 11–12 bps were below a 21 bps stress cost. Key message: **"event-ranking skill does not imply policy value"**. Simulation-only and multi-pair. — [arXiv 2607.19453](https://arxiv.org/abs/2607.19453)
- A KIT study of short-term BTC prediction (LSTM, GRU, random forest, gradient boosting) found trading results **turn negative with 30 bps round-trip costs** because holding periods are short, consistent with market efficiency. — [KIT](https://publikationen.bibliothek.kit.edu/1000150665/149388567)
- An MDPI 2025 study: random forest with ROC-AUC about 0.61 earned a 35.97% gross out-of-sample return that became **negligible after transaction costs**. — [MDPI Forecasting](https://www.mdpi.com/2571-9394/8/3/40)
- Across 3,703 cryptos, out-of-sample R² was 4.855%, "primarily achieved through the strong one-day reversal effect". That is a known anomaly, not model skill, and it is a multi-coin result. — [ScienceDirect RIBAF 2023](https://www.sciencedirect.com/science/article/abs/pii/S0275531923000314)
- Contrasting claim: a 2022 paper reports an **out-of-sample Sharpe of about 3.2 after costs** for LSTM and GRU ensembles, assuming 15 bps half-turn costs and **no short-selling costs**. It is older and more optimistic than 2026 work. — [ScienceDirect 2022](https://www.sciencedirect.com/science/article/pii/S2405918822000174)
- **Alpha Arena (nof1) Season 1** (ended 3 November 2025; $10,000 each; crypto perps on Hyperliquid; same prompts and data for every model; about 17 days): Qwen3 Max **+22.3%** ($12,231); DeepSeek V3.1 **+4.89%**; **four of six models lost**. Sources disagree on the exact losses: Claude Sonnet 4.5 −30.8% or −42.0%; Gemini 2.5 Pro −56.7% or −45.6%; Grok 4 −45.3% or −57.9%; GPT-5 −62.7% or −58.7%. Analysts stress that 17 days is too short to draw conclusions and that the winner may simply have had the risk settings that suited that particular market. — [Forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/); [iWeaver](https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/); [Buildix](https://www.buildix.trade/blog/nof1-alpha-arena-lessons-ai-trading-byok-strategy-advisor-2026)
- Season 1.5 (US equities, ended 3 December 2025) was won by an unnamed "mystery model" at +12.11% over two weeks. One outlet's headline says all eight major models posted losses through overtrading, but it is unclear which season or leaderboard that refers to. — [Forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/); [BigGo Finance](https://finance.biggo.com/news/5BSX_Z0BaoGGrU-ID27J)

### Inferences
- **Pitfalls these studies point to:** cost blindness (the biggest killer); judging by AUC or accuracy instead of net P&L; multiple testing ("extensive predecessor search"); regime dependence; and a "model" edge that is really a known anomaly (one-day reversal). Leakage (for example, normalising on the full sample, overlapping labels, look-ahead in features) is standard advice but was not explicitly covered in what I retrieved.
- What has held up best: **simple, low-turnover models with a cost-aware "only trade when the expected move exceeds costs" filter**, evaluated walk-forward. Even then the net benefit over buy-and-hold is not statistically significant.
- LLM agents: the public evidence is a short, high-variance competition with leveraged perps and mostly losses. No audited long-horizon evidence of LLM trading skill turned up.
- **Feasibility verdict:** it is feasible to *use* ML (XGBoost on hourly or daily features, walk-forward, cost-aware thresholds) as a filter or sizing layer on top of a simpler strategy. **It is not feasible to expect ML on its own to supply reliable edge.** LLM-driven trading decisions are **not recommended** beyond research or assistant use.

### Gaps
- I found no systematic review that explicitly quantifies leakage or overfitting in the BTC ML literature for 2019–2026.
- Per-model Sharpe figures for LSTM and iTransformer in Bysik & Ślepaczuk were not visible.
- Official nof1 final numbers were not retrieved, and the secondary sources conflict.

---

## 9. Copy-trading, signal services and "AI bots" marketed to retail

### Takeaway
I found no independently audited evidence that retail copy-trading or "AI bot" products deliver positive net returns. Peer-reviewed work on Bybit shows that leader rankings mislead and that copiers of "reputable" portfolios lose money in aggregate.

### Cited Findings
- "Stranger Danger?" (ACM CHI 2024; Bybit and TraderWagon): copiers following supposedly reputable, higher-level portfolios **cumulatively lose significant amounts**. **Gold-level portfolios' performance degrades within 10 days and starts to lose money for copiers.** Bybit's leaderboard ranks by aggregate PnL across followers. — [ACM DL](https://dl.acm.org/doi/10.1145/3613904.3642715)
- A 90-day multi-exchange dataset (Binance, Bybit, MEXC; 100,236 copier outcomes; not peer-reviewed or audited): **48.48% of copiers finished profitable**. 97.04% of leaders were profitable on their own PnL, but **only 43.61% produced positive follower PnL**. — [YieldFund](https://www.yieldfund.com/news/is-copy-trading-profitable-a-90-day-multi-exchange-study); [KuCoin blog](https://www.kucoin.com/blog/is-crypto-copytrading-profitable-in-2026)
- Bybit says follower results can differ from the leader's because of slippage and execution limits during volatility. — [Coin Bureau review](https://coinbureau.com/review/bybit-copy-trading-review)

### Inferences
- The gap between leader PnL (97% green) and follower PnL (44% positive) points to entry timing, slippage and survivorship and selection bias in leaderboards.
- **Verdict:** not a strategy for this team. If anything, these products are competing retail flow.

### Gaps
- I found no audited performance disclosure for any exchange-marketed "AI bot" or grid-bot product.

---

## 10. Overall feasibility ranking for a small BTC-only retail bot (CCXT, cheap VPS, 50–500 ms, $1k–$50k)

### Takeaway
None of the derivatives, market-structure or alternative-data families gives a well-documented, cost-surviving edge at retail scale in 2025–2026. The most defensible uses are: (1) **opportunistic funding or basis carry**, switched on only when funding is well above baseline, with strict exchange-risk limits; and (2) **slow, free regime filters** (high funding or carry as a crash-risk warning, MVRV-Z, Fear & Greed, ETF flows) layered on a core strategy researched elsewhere. Order-flow alpha, market making and arbitrage are out of reach. Grid bots and ML-only prediction have poor or unproven net expected value.

### Cited Findings
- Carry yields: 11% in 2024, 4.9% in 2025, 2.2% in 2026 to August — [CryptoSlate](https://cryptoslate.com/ethena-is-targeting-the-120-trillion-wall-street-stocks-market-to-hunt-yields-5x-higher-than-bitcoin/). Basis below Treasuries in 2026 — [BigGo Finance](https://finance.biggo.com/news/9c11c1e7-4988-4ad7-998f-7d4f8a51f6ad). Liquidation and ADL risk — [BIS WP 1087](https://www.bis.org/publ/work1087.pdf), [Forbes](https://www.forbes.com/sites/boazsobrado/2025/10/21/locked-out-and-liquidated-traders-blame-binance-for-19-billion-crash/)
- Funding as a crash-risk signal (monthly) — [BIS WP 1087](https://www.bis.org/publ/work1087.pdf). As a short-horizon signal R² = 0.003 — [Fulgur Ventures](https://medium.com/@fulgur.ventures/bitcoin-funding-rates-and-price-predictability-27ce95535af1)
- Grid has zero expected value before fees — [arXiv 2506.11921](https://arxiv.org/pdf/2506.11921). Order-flow imbalance is unstable out of sample — [SSRN 7227998](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7227998). Adverse selection in crypto — [Tiniç & Sensoy](https://nottingham-repository.worktribe.com/OutputFile/40584797)
- ML fails after costs unless filtered, and is still not significant against buy-and-hold — [arXiv 2606.00060](https://arxiv.org/abs/2606.00060); [arXiv 2607.19453](https://arxiv.org/abs/2607.19453)
- On-chain valuation thresholds were not reached in 2022–2025 — [Grobys, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0275531926002138)

### Inferences
Feasibility ranking (my judgement from the evidence above):

| Strategy family | Fit for this team | Main reason |
|---|---|---|
| Funding/basis carry (spot long + perp short) | **Conditional yes, as an opportunistic module** | Simple to build, but 2025–26 BTC yields are about 1–3% on capital after the capital split; tail risk from ADL, lockouts and exchange failure |
| Funding, OI and liquidations as risk filter | **Yes (filter)** | Free via CCXT; BIS supports crash prediction at monthly horizons |
| Same, as directional entry signal | No / unproven | R² ≈ 0; anecdotal evidence only |
| On-chain valuation (MVRV-Z, NUPL, SOPR) | **Yes (slow overlay)** | Free daily data; in-sample cycle evidence only; thresholds drifting |
| Fear & Greed, ETF flows | **Yes (cheap filter)** | Small, cost-sensitive edges; reverse causality for ETF flows |
| Grid trading | Weak | Zero expected value before fees; large opportunity cost in trends |
| Passive market making | No | Latency, no rebates at this scale, adverse selection |
| Order-book / order-flow alpha | No | Edge at seconds horizon, unstable, below fees and latency |
| Arbitrage (cross-exchange, triangular) | No | Thin spreads, bot competition, transfer friction |
| ML return prediction | Only as filter or sizing with cost-aware thresholds | Not significant against buy-and-hold after costs |
| LLM agents, copy-trading, "AI bots" | No | Short-window losses; copiers lose; no audited evidence |

- Some families would be multi-coin and are excluded by the BTC-only decision: cross-sectional funding arbitrage across many perps (Werapun et al.; the MDPI two-tiered study), multi-pair ML selectors (Jadouli), and Ethena-style diversification into equity perps.

### Gaps
- Most numbers come from search extracts. Primary PDFs (BIS, He et al., Bysik & Ślepaczuk, Grobys) could not be fetched in this session and should be spot-checked.
- The team can fill several gaps cheaply with its own data: compute the share of negative-funding periods and the net carry after four-leg fees from CCXT funding history for 2024–2026 on Binance and Bybit, and backtest a "carry on only when 7-day average funding exceeds X" rule.
