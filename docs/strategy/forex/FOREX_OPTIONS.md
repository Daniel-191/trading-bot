# Forex edges barely survive retail financing costs

Forex has only two strategy families with real academic support: **multi-month trend following** and **carry**. In our own test, neither clears retail costs convincingly. We backtested the nine G10 currencies against the US dollar over 2000 to October 2026:

- The best rule, an equal-risk blend of trend and carry, earned a **net Sharpe of 0.20** (bootstrap p ≈ 0.15).
- Trend alone earned **0.04**.
- Carry alone earned **0.13–0.14**.
- No candidate has earned a Sharpe above 0.1 in either 2015–2021 or 2022–2026.

The cost that decides this is not the spread but the broker's overnight financing markup. OANDA US adds **1% a year to every open position** on most pairs. A forex book run at 10% volatility holds 1.6–3.3 times its equity in positions, so that markup costs **1.6–3.3% of equity a year**. With the markup removed, the blend's Sharpe rises to **0.44**.

Every faster or cleverer idea lost to costs or has no evidence that survives them. That covers mean reversion, London breakouts, news trading, fading retail sentiment, seasonal patterns and machine learning.

Our Bitcoin trend core does far better: Sharpe 1.33–1.51 since 2015 and 0.73–0.89 since the US spot ETFs launched (2024–26). Forex is also more work to run:

- It needs a new broker connection, because CCXT supports no forex broker.
- It needs about nine instruments at once.
- It needs margin and financing bookkeeping.
- It reverses the repo's Bitcoin-only decision.

We recommend keeping BTC Option A as the bot's core and treating forex as a research track at most. If both developers want to pursue it, the one candidate worth pre-registering is the G10 trend-plus-carry blend, run at whichever broker or venue charges the least financing.

*How this was put together: three parallel research tracks, whose notes are in [`research/`](research/):*

- *price-based strategies: [`price-based-strategies.md`](research/price-based-strategies.md);*
- *carry, macro, event and flow strategies: [`macro-carry-and-event-strategies.md`](research/macro-carry-and-event-strategies.md);*
- *brokers, costs, regulation and our own backtest: [`implementation-and-backtest.md`](research/implementation-and-backtest.md).*

*The web page tool failed for every site in this session. Published figures therefore come from abstracts, author summaries and search extracts, not full texts; spot-check key numbers before relying on them.*

*The backtest script is [`research/fx_backtest.py`](research/fx_backtest.py). It runs on the Federal Reserve's daily H.10 exchange rates and the OECD's 3-month interest rates, both mirrored on GitHub. The downloaded data is gitignored; the notes list each file's URL and SHA-256 so the run can be reproduced.*

*We checked several current facts against a second source:*

- *OANDA's 1% financing fee;*
- *the September 2026 Fed hike;*
- *the July 2026 US–Japan yen intervention;*
- *FTMO's purchase of OANDA;*
- *the CME micro FX contract list.*

*Two terms used throughout:*

- *A **pip** is the standard price step in a currency pair: 0.0001, or 0.01 for yen pairs.*
- *A **leg** is one currency position against the US dollar. A carry book long AUD and short CHF holds two legs.*

## Only trend and carry have published evidence that survives costs

Trend following has the deepest record, but currencies are one of its weaker markets. AQR's "Demystifying Managed Futures" exhibit shows a gross Sharpe of **0.87 for the currency sleeve against 1.79 for the diversified portfolio**. The sample period is probably 1985–2012 but not confirmed ([AQR](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Demystifying-Managed-Futures.pdf)).

Hurst, Ooi and Pedersen's century study (67 markets, including 12 currency pairs, 1880–2016) found net returns **positive in every decade**. CXO summarises it as a Sharpe of about **0.4 after 2-and-20 fees** ([CXO Advisory](https://www.cxoadvisory.com/momentum-investing/trend-following-with-intrinsic-momentum-over-the-very-long-run)).

FX trend is weaker for a structural reason: seven to ten dollar pairs share one dollar factor, so they offer perhaps three to five independent bets.

Speed matters too. Kurth, Eisler, Rej and Bouchaud (July 2026) find that short-term trends **stopped delivering reliable returns around 2009** in markets whose price increments are small relative to their volatility ([arXiv](https://arxiv.org/abs/2607.01550)). A secondary summary says currencies are in that group ([alphaxiv](https://www.alphaxiv.org/overview/2607.01550)).

The only FX-only out-of-sample test we found is a non-peer-reviewed walk-forward on seven majors over 2003–2025. It got a Sharpe of **0.43**, and only USDJPY and EURUSD individually cleared 0.5 ([QuantInsti](https://www.quantinsti.com/articles/trend-following-strategies-major-currency-markets-epat-project/)). Volatility targeting does not raise the Sharpe ratio in currencies, but it does cut extreme outcomes ([Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/)).

Classic chart rules are a subset of trend, and their stand-alone edge is gone. Filter and moving-average profits on dollar exchange rates were genuine in the 1970s–80s and **had disappeared by the early 1990s** ([Neely, Weller & Ulrich](https://econpapers.repec.org/paper/fipfedlwp/2006-046.htm)).

Studies that correct for testing thousands of rules disagree:

- Hsu, Taylor and Wang tested over 21,000 rules on 30 currencies and still found profits, mostly in emerging markets ([SSRN](https://papers.ssrn.com/abstract=2765673)).
- Kuang, Schröder and Wang found that almost all the profits from 25,988 rules on 10 emerging-market currencies **vanish once data snooping is accounted for** ([IDEAS/RePEc](https://ideas.repec.org/p/bir/birmec/13-09.html)).

Real retail accounts point the same way. In 428 currency-trader accounts over 2005–2009, using technical indicators was **associated with worse returns** ([Abbey & Doukas](https://www.efmaefm.org/0DOUKAS/publications/pdf/IsTechnicalAnalysisProfitable_12-14-2011.pdf)). Moving-average crossovers and Donchian channels therefore belong inside a trend ensemble as extra lookbacks, never as separately tuned strategies.

The carry premium is real but modest, and it is pay for crash risk:

- Lustig, Roussanov and Verdelhan report a Sharpe of **0.50 after interbank bid-ask costs** ([LRV 2011](https://www3.nd.edu/~nmark/GradMacroFinance/LustigRoussanovVerdelhan_RFS_2011.pdf)).
- Over 1900–2012 the Sharpe was only **0.2–0.4** ([Quantpedia on Doskov & Swinkels](https://vvv.quantpedia.com/?p=571)).
- Carry returns are negatively skewed, because positions unwind together when risk appetite and funding liquidity dry up ([Brunnermeier, Nagel & Pedersen](https://www.nber.org/system/files/working_papers/w14473/w14473.pdf)).
- Shocks to global FX volatility explain **more than 90%** of the differences in returns across carry portfolios ([Menkhoff et al. 2012](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01728.x)).

The reliable part sits in the dollar leg. Carry that is neutral to the dollar shows insignificant abnormal returns ([Daniel, Hodrick & Lu](https://business.columbia.edu/sites/default/files-efs/pubfiles/6378/Daniel.Hodrick.Lu.Carry%20Trade.Critical%20Finance%20Review.2017.pdf)). Carry that is both dollar-neutral and hedged against crashes earns roughly zero ([Jurek](http://users.nber.org/~confer/2008/apf08/jurek.pdf)).

The live record is sobering. Invesco's G10 carry ETF (DBV) lost **28.4% in 2008** ([Yahoo Finance](https://nz.finance.yahoo.com/quote/DBV/performance/)) and closed in March 2023 ([Investing.com](https://www.investing.com/etfs/powershares-db-g10-curr.-harvest-profile)). An independent rebuild of its basket earned **0.74% a year, a Sharpe of 0.07 over about 19.5 years**. It made 4.8% a year in calm months and lost 15.6% a year in stressed ones ([Alpha in Academia](https://www.alphainacademia.com/p/carrys-zero)).

Diversified versions of these premia look better on paper:

- **Dollar carry** is a single monthly switch: long a basket of foreign currencies when foreign short rates are above US rates on average, short it otherwise. It has a Sharpe above 0.5 and is uncorrelated with ordinary carry ([Lustig, Roussanov & Verdelhan 2014](https://www.nber.org/system/files/working_papers/w16427/revisions/w16427.rev0.pdf)).
- **Deutsche Bank's Currency Returns index** blends carry, momentum and value. It had a **−8.9% maximum drawdown against −37.1% for carry alone**, partly on simulated history ([DB brochure](https://quantpedia.com/www/DBCR_Brochure.pdf)).
- Adding these currency styles to a stock-and-bond portfolio raised its out-of-sample Sharpe from 0.64 to 1.05 after costs ([Kroencke, Schindler & Schrimpf](https://ideas.repec.org/a/oup/revfin/v18y2014i5p1847-1883..html)).

Live institutional results are thinner. Record plc's multi-strategy currency programme made **0.86% a year at 4% volatility**, a Sharpe of about 0.2 ([Record](https://recordfg.com/wp-content/uploads/2025/06/2021-Full-Year-Presentation-Record-plc.pdf)). Value on its own is too slow and has faded: purchasing-power deviations take **3–5 years to halve** ([Rogoff](https://web.williams.edu/Economics/macro/rogoff.pdf)), and value baskets have been almost flat since 2017 ([Resonanz Capital](https://resonanzcapital.com/insights/style-premia-are-they-still-relevant)).

## Faster and cleverer forex strategies lose to costs or lack evidence

**Cross-sectional momentum** means buying the currencies that rose most recently and shorting those that fell. Over 1976–2010 it earned up to 10% a year gross, but "very effective limits to arbitrage" stood in the way ([BIS WP 366](https://www.bis.org/publ/work366.pdf)). Most of the profit came from less liquid emerging-market currencies, and about a third was lost to costs ([Cass Knowledge](https://www.cass.city.ac.uk/faculties-and-research/research/cass-knowledge/inbusiness/2013/swept-along-by-currencies)). The only post-2010 test we found, a bachelor's thesis, found no significant returns ([Aalto](https://aaltodoc.aalto.fi/items/0db57fa9-e5c6-4b7d-9dd8-1ae15a8940c6)).

**Mean reversion** has no out-of-sample evidence that survives costs. Bollinger-band rules fail after costs ([IDEAS/RePEc](https://ideas.repec.org/a/taf/raflxx/v3y2007i4p263-267.html)). The January 2015 removal of the EUR/CHF floor shows the hidden risk. A pair held in a band by a central bank looks like the ideal mean-reversion trade until the band breaks. When it broke, **FXCM's clients ran up $225m of negative balances** ([Finance Magnates](https://www.financemagnates.com/forex/brokers/fxcm-publishes-data-of-snb-mishandling-of-the-swiss-franc/)).

**Time-of-day and fixing effects** are statistically real:

- Currencies tend to weaken during their home market's business hours ([Ranaldo 2009](https://ideas.repec.org/a/eee/jbfina/v33y2009i12p2199-2206.html)).
- The dollar traces a W-shaped daily path around the Tokyo, ECB and London fixings ([Krohn, Mueller & Whelan](https://www.bankofcanada.ca/2021/10/staff-working-paper-2021-48/)).

The authors say these are exploitable only by investors with **lower-than-average transaction costs** ([draft](https://acfr.aut.ac.nz/__data/assets/pdf_file/0007/190753/Krohn_Mueller_Whelan_Jun2018_FXPremiaAroundTheClock.pdf)). Our own arithmetic shows why. At 1.5 basis points per round trip, a strategy holding for three hours needs a **gross Sharpe of about 1.3 just to break even**, and one holding for an hour about 2.3. The one systematic London-breakout backtest we found, a vendor's on GBPUSD over 2016–2026, lost **60%** ([Backtrex](https://backtrex.com/en/backtests/london-breakout-gbp-usd)). The useful lesson is about execution: never trade around the 5pm New York rollover, often the least liquid hour of the FX day ([CME Group](https://www.cmegroup.com/articles/2026/when-fx-futures-pause.html)), and keep away from the fixings.

**News trading** is out of reach. Data surprises move prices within seconds to minutes ([Andersen et al. 2003](https://www.aeaweb.org/articles?id=10.1257%2F000282803321455151)), while retail EURUSD spreads widen to 5–10 pips or more around payrolls, according to broker education sources ([FXNX](https://fxnx.com/en/blog/spread-widening-scheduled-news-peaks-recovery-times)).

The one event effect that tolerates retail latency is positioned before the release: short-dollar baskets earn more on scheduled FOMC days ([Mueller, Tahbaz-Salehi & Vedolin](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12499)). Daily-data evidence for a pre-FOMC drift in EURUSD and USDJPY is weak ([Lucca & Moench](https://conference.nber.org/confer/2012/APf12/Lucca_Moench.pdf)).

**Positioning** data mostly confirms trends rather than calling reversals:

- Speculators' futures positions forecast continuations ([UMBC](https://economics.umbc.edu/wp-content/uploads/sites/243/2014/09/wp_09_116.pdf)).
- One EUR result largely collapses after correcting for multiple tests ([Finance Research Letters](https://www.sciencedirect.com/science/article/abs/pii/S1544612316300563)).
- Retail FX flow is contrarian but uninformed ([JIFMIM 2025](https://www.sciencedirect.com/science/article/abs/pii/S1042443125000368)).
- OANDA reportedly stopped serving its order-book data feed in 2024 ([Dekalog](https://dekalogblog.blogspot.com/2024/09/discontinuation-of-oandas-orderbook-and.html)).

**Seasonal patterns** are unstable. The main study of "gotobi" days, the Japanese settlement dates that drive dollar buying in USDJPY, rests on 2018–2020 data and made design choices on its own sample ([Bessho et al.](https://arxiv.org/pdf/2301.13204); [critique](https://forexdetox.substack.com/p/the-tokyo-fix-reversal-anomaly-on)). Turn-of-month and day-of-week effects **diminish over time** ([Kumar 2016](https://ideas.repec.org/a/eee/jebusi/v86y2016icp16-32.html)).

**Machine learning** follows the BTC pattern. The most careful exchange-rate study finds a regularised linear model beats the random walk monthly, and "nonlinearities do not appear substantial" ([Filippou, Rapach, Taylor & Zhou](https://repec.cepr.org/repec/cpr/ceprdp/DP15305.pdf)). Deep-learning trend models lose their edge once costs pass about **2–3 basis points** ([Lim, Zohren & Roberts](https://arxiv.org/abs/1904.04912)).

## Our 27-year G10 backtest: the best blend nets a Sharpe of 0.20

**Data:**
- Daily H.10 noon New York exchange rates for nine currencies against USD, 3 January 2000 to 9 October 2026 ([H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv)).
- Monthly OECD 3-month interest rates for all ten countries.

**Execution and costs:**
- Positions are decided on each day's fixing and earn the next day's move.
- Round-trip spread plus slippage of 1.0–2.0 pips on majors and 50 pips on SEK and NOK.
- Each position earns the interest-rate differential and pays a **1%-a-year financing markup**.

**Sizing:**
- Each pair is weighted inversely to its own volatility.
- The whole book targets **10% annual volatility**.

**Parameters** came from the literature and were not tuned. In total we ran nine variants plus two benchmarks.

| Strategy (G10 vs USD) | Net Sharpe 2000–26 | 2000–07 | 2008–14 | 2015–21 | 2022–26 | Max DD | Frictionless Sharpe | Turnover (× equity/yr) |
|---|---|---|---|---|---|---|---|---|
| Trend: momentum ensemble (1/3/6/12-month) | 0.04 | 0.51 | 0.24 | −0.23 | −0.66 | −47% | 0.29 | 39 |
| Trend: Donchian ensemble (20/55/100/200-day) | 0.04 | 0.68 | 0.27 | −0.49 | −0.63 | −56% | 0.23 | 16 |
| Cross-sectional momentum, 12-month | −0.33 | −0.17 | −0.21 | −0.57 | −0.46 | −72% | −0.08 | 8 |
| G10 carry, long 3 / short 3, unscaled | 0.14 | 0.96 | −0.27 | −0.13 | 0.04 | −40% | 0.36 | 0.6 |
| G10 carry, long 3 / short 3, 10% vol target | 0.13 | 1.05 | −0.51 | −0.25 | 0.06 | −61% | 0.39 | 2 |
| **50/50 trend + carry, 10% vol** | **0.20** | **1.10** | −0.12 | −0.21 | −0.28 | −47% | **0.52** | 33 |
| EURUSD 5-day reversal | −0.22 | −0.13 | −0.42 | −0.03 | −0.33 | −53% | −0.04 | 63 |
| EURUSD RSI(2) fade | −0.42 | −0.63 | −0.55 | −0.40 | 0.08 | −58% | −0.29 | 34 |
| Benchmark: long USD basket | −0.18 | −0.69 | −0.13 | 0.05 | 0.22 | −58% | −0.06 | 0 |

*2022–26 runs to 9 Oct 2026. "Frictionless" means the spot move plus the interest differential, with no spread or markup, which is comparable to academic gross figures. Turnover is total weight traded ÷ 2 per year, in multiples of equity, so it is not comparable with the BTC table's count of round trips. Full output, tail windows and calendar years are in [`research/implementation-and-backtest.md`](research/implementation-and-backtest.md) §9.*

Four findings stand out.

First, **the edge has decayed exactly where it matters**. Before 2008 the textbook result held: carry made about 1.0, trend 0.5–0.7 and the blend **1.10**. The only stretch out of sample for most of the literature that supplied our parameters is roughly 2016 onward, and every strategy did worst there. Recent years show it clearly:

| Strategy | 2022 | 2024 | 2025 | 2026 YTD |
|---|---|---|---|---|
| Momentum ensemble | +8.6% | −18.5% | −10.6% | −5.2% |
| Unscaled carry | — | +4.7% | −3.2% | +6.7% |

Trend did well in 2022 as the dollar rallied, then lost in each year since. Multi-asset trend funds were up about 15.7% year to date in October 2026 ([Top Traders Unplugged](https://www.toptradersunplugged.com/trend-following-week-in-review-october-2-2026/)), so currencies have not been the sleeve driving their gains.

Second, **trend and carry hedge each other**. Their daily correlation is −0.02 to −0.05, which is why the blend beats both. In September to December 2008, trend made **+11.6%** while unscaled carry lost **23.4%**.

Third, **a single-pair forex bot modelled on our BTC design has nothing to trade**. Both EURUSD mean-reversion rules lost money in almost every sub-period. The rules with any edge are nine-pair portfolios.

Fourth, **having more data does not rescue the case**. Unlike BTC, the history here is long enough: 27 years. The blend's t-statistic is still only about **1.0**, and its uncorrected p ≈ 0.15 is far from the roughly 0.006 that nine variants would require.

The caveats cut both ways:

- **Prices:** H.10 is one noon reference rate, not a bid/ask series, and has no intraday data, so flash crashes and stop-outs are invisible.
- **Rates:** 3-month interbank rates are not the overnight rates retail financing follows.
- **Costs:** spread costs are held constant since 2000, which flatters the early years.
- **Turnover:** trend turnover is inflated by daily volatility rescaling with no rebalance band. Halving spread costs lifts trend to 0.09, roughly what a band might recover.

## Financing markups, not spreads, decide whether forex pays

Retail brokers price overnight financing as the interbank rate differential plus a markup on every position. The rate is reported as either the "tom-next" swap rate (the cost of rolling a position from tomorrow to the next day) or a benchmark rate:

| Broker | Markup a year | Source |
|---|---|---|
| OANDA US | 1% admin fee on most pairs; 2% on ZAR, HUF and others; 4% on TRY | [OANDA](https://www.oanda.com/us-en/trading/financing-fees/) |
| IG | 0.3–1.5% by region and contract size | [IG](https://www.ig.com/uk/help-and-support/spread-betting-and-cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-) |
| Saxo | ±0.35–0.75% by account tier | [Saxo](https://www.home.saxo/en-mena/rates-and-conditions/forex/financing) |
| IBKR | borrowed currency at benchmark + 1.5%; cash earns benchmark − 0.5% | [IBKR](https://www.interactivebrokers.com/en/trading/margin-rates.php) |
| Pepperstone | up to 3% | [Pepperstone](https://eu-assets.contentstack.com/v3/assets/bltd74737b907a31bbb/bltc19314db598b7ab0/UK_Legal_Costs_and_Charges.pdf) |

A long-run AUD/JPY example shows the effect. At a 1.5% markup, a retail trader holding the position over 2004–2019 kept only about **58% of the interbank carry** ([Forexop](https://forexop.com/carry-trading-primer/)).

The markup charges on the size of each position, not on each trade. That is why it dominates. At a 10% volatility target our books held **1.6–3.3 times equity** in positions on average, so a 1% markup costs 1.6–3.3% of equity a year. That is more than the frictionless edge of any rule we tested. Changing the inputs shows which one matters:

| Change | Trend | Carry | Blend |
|---|---|---|---|
| Base case (1% markup) | 0.04 | 0.14 | 0.20 |
| No markup | 0.20 | 0.36 | 0.44 |
| 2% markup | negative | negative | negative |
| Spreads doubled | — | — | 0.12 |

Doubling spreads costs the blend only 0.08 of Sharpe; the markup costs far more. This is the reverse of the BTC result, where costs barely mattered because the gross edge was large and the position never exceeded 1× equity.

Where to trade therefore matters more than which strategy. Three ways to cut the markup:

1. **Trade cross pairs directly.** Hold long AUD/CHF instead of long AUD/USD plus short USD/CHF. That roughly halves the positions paying the markup; our estimate is that the carry book's markup would fall from 1.8% to about 0.9% of equity a year.
2. **Use a large account at a low-markup broker,** such as Saxo's top tier.
3. **Use CME micro FX futures.** Futures prices build in the interest differential at market rates, so there is no broker financing markup (our inference; untested). They are exchange-cleared and fall outside the retail-forex rules.

Micro futures have limits. They exist for only six currencies: EUR, GBP, AUD, CAD, CHF and JPY, at **€12,500, £6,250, A$10,000, C$10,000, CHF 12,500 and ¥1.25m** per contract ([CME](https://www.cmegroup.com/activetrader/MicroFX); [CME 2026](https://www.cmegroup.com/articles/2026/fx-futures-are-not-only-for-big-players.html)). That is about $6,000–15,000 of exposure each. A 10%-volatility book under about $50k would hold one contract or none per currency, so position sizes would be very coarse. Quarterly roll costs were not tested.

Carry's current setup is the best in years, which makes it tempting. As of mid-October 2026, in G10:

- **High yielders:** AUD at 4.60% and NOK at 4.50%, alongside USD at 3.75–4.00% after a September hike ([Fed](https://www.federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf)).
- **Low yielders used as funding:** CHF at 0%, JPY at 1.25% ([CNBC](https://www.cnbc.com/2026/09/18/japan-raises-rates-30-year-high-yen-jgb.html)) and SEK at 1.75%.

The full table is in the macro notes. Our own 3-month rate data corroborates these levels. A long-three, short-three G10 carry book now earns about 3.1–3.3 percentage points before markup, and our unscaled carry is up **6.7%** in 2026.

The crash risk is live too:

- **August 2024:** the vol-targeted carry book lost **14.6%** in four weeks, more than double the unscaled book's 6.4%. Volatility targeting raises leverage in calm markets, just before carry crashes.
- **July–September 2026:** USDJPY peaked at **163.87 on 23 July**, the US and Japan intervened jointly, and yen crosses fell 4–6% ([TickerLayer](https://tickerlayer.com/learn/yen-carry-trade); [CNBC](https://www.cnbc.com/2026/08/20/us-japan-yen-intervention-bank-of-japan-carry-trade.html)).

Carry also loses in the same risk-off weeks in which the BTC bot sits in cash, so it adds little crash protection.

## Running forex means a new broker layer and a multi-instrument bot

CCXT's documentation lists **no forex broker** ([CCXT README](https://raw.githubusercontent.com/ccxt/ccxt/master/README.md)), so the planned exchange layer cannot be reused. The candidate brokers:

- **OANDA's v20 REST API is the closest fit.** It is plain HTTP plus streaming, has a free practice account that maps onto our planned `TestnetBroker`, and serves the US, UK, EU and Australia. The prop-trading firm FTMO completed its purchase of OANDA on 1 December 2025 ([Finance Magnates](https://www.financemagnates.com/forex/prop-firm-ftmo-closes-oanda-acquisition-deal-after-ten-months/)).
- **Interactive Brokers** works through the maintained, asyncio-based `ib_async`. Its main forex venue (IdealPro) requires orders of at least $25,000. Smaller orders get "odd-lot" fills **1–2 basis points worse** ([IBKR](https://ibkb.interactivebrokers.com/tag/forex?page=2)) and pay a $2 minimum commission ([IBKR](https://interactivebrokers.ie/en/pricing/commissions-spot-currencies.php)). IBKR also needs its Gateway program running alongside the bot.
- **MetaTrader 5's Python package ships Windows wheels only** ([PyPI](https://pypi.org/project/MetaTrader5/)).
- **FXCM is being broken up:** AvaTrade agreed on 12 October 2026 to buy most of the business ([Bernama](https://www.bernama.com/en/press/news.php?id=2618885)), and Trade Nation is taking its UK client book ([Finance Magnates](https://www.financemagnates.com/forex/exclusive-trade-nation-acquires-fxcms-uk-client-book/)).

Regulation depends on where the account sits:

- **US:** retail forex requires minimum deposits of 2% of position size on majors and 5% on other pairs, i.e. 50:1 and 20:1 leverage ([Morgan Lewis](https://www.morganlewis.com/pubs/2010/09/cftc-issues-final-retail-forex-rules)). Positions in a pair must be closed oldest-first, and hedged long and short positions in the same pair are banned ([OANDA](https://www.oanda.com/us-en/skills-and-insights/education/trading-asset-classes/forex/nfa-fifo-rule-challenges-expert-advisors/)). Customer forex funds **may not be segregated** if the dealer fails ([CFTC](https://WWW.cftc.gov/idc/groups/public/@cpfraudawarenessandprotection/documents/file/forex_advretailcustomers2007.pdf)).
- **UK:** the FCA caps majors at 30:1, closes positions out when margin falls to 50%, and protects retail clients against negative balances. These rules also cover spread bets and rolling spot forex ([FCA PS19/18](https://www.fca.org.uk/publications/policy-statements/ps19-18-restricting-contract-difference-products)).
- **EU and Australia:** the same limits apply ([ESMA](https://www.esma.europa.eu/press-news/esma-news/esma-adopts-final-product-intervention-measures-cfds-and-binary-options); [ASIC](https://asic.gov.au/about-asic/news-centre/find-a-media-release/2022-releases/22-082mr-asic-s-cfd-product-intervention-order-extended-for-five-years/)).

None of these leverage caps binds a 10%-volatility book.

The base rates are harsh. ESMA found **74–89% of retail CFD accounts lose money** ([ESMA](https://www.esma.europa.eu/node/84933)). The UK average across 14 FCA-regulated brokers was **69.9%** in April 2026 ([The Investors Centre](https://www.theinvestorscentre.co.uk/trading/statistics/cfd-trading/)). A study of about 100,000 retail FX traders found **no improvement with experience** ([Hayley & Marsh](https://openaccess.city.ac.uk/15691)).

The tail risks are concrete:

- **The 2015 Swiss franc shock** left FXCM needing a **$300m rescue** and made Alpari UK insolvent ([Finance Magnates](https://www.financemagnates.com/forex/brokers/alpari-uk-first-major-casualty-chf-lcg-group-facing-2-5-mln-losses/)).
- **The October 2016 sterling flash crash:** sterling fell about 9% in Asian trading ([BIS](https://www.bis.org/publ/mktc09.htm)), yet our daily data shows only −1.7% that day.
- **The January 2019 yen flash rally:** the yen rose about 3% in roughly 30 seconds ([RBA](https://www.rba.gov.au/publications/smp/2019/feb/pdf/box-b-the-recent-japanese-yen-flash-event.pdf)), yet our data shows about 1%.

Stress tests therefore have to be written explicitly, because daily backtests cannot show these moves.

Most of the planned engine carries over unchanged: the `Strategy` protocol, event bus, Control and Telegram, dashboard, storage, the backtest harness and the `TRADING_MODE` gating. Forex needs several new pieces:

- an `OandaBroker` or `IbkrBroker` behind the existing `Broker` interface;
- per-instrument metadata (pip size, units, margin rates);
- profit and loss in several currencies, converted into the account currency with `Decimal`;
- a daily financing ledger;
- a trading calendar: Sunday 17:00 to Friday 17:00 New York, daily bars cut at 17:00 New York, and no orders around the rollover;
- risk limits on total exposure per currency across pairs;
- a list of instruments in place of the single `TRADING_PAIR`.

Two interface changes affect the other developer. The `Broker` interface would gain financing and margin concepts, and `PaperBroker` would have to simulate bid/ask prices and financing. Both decisions-log entries in `CLAUDE.md` would also have to change: Bitcoin-only, and CoinMarketCap as the only market-data source, since the forex data would come from the broker's own candles. Both developers need to agree to that.

## Five specific forex strategies, ranked

| | **FX-1. Trend + carry blend** *(only candidate worth pre-registering)* | **FX-2. Filtered G10 carry** | **FX-3. Dollar-carry switch** | **FX-4. Trend ensemble alone** | **FX-5. FOMC-day short-USD add-on** |
|---|---|---|---|---|---|
| **Rules** | Equal-risk 50/50 of FX-4 and carry. Carry: monthly, long the 3 highest and short the 3 lowest G10 rates (ranked on the broker's actual net financing). Book scaled to 10% vol, capped at 4×, with a rebalance band. | Carry as in FX-1, unscaled or vol-capped (never scaled up). Hold only pairs earning ≥ 1.5% a year after the broker's markup. Halve exposure on a risk-off VIX signal and when trend disagrees. Filters are illustrative and must be fixed before testing. | Monthly. If the average G9 short rate is above the US rate, go long an equal-weight basket of the 9 currencies vs USD; otherwise short it. Vol-targeted. No free parameters. | Average sign of 21/63/126/252-day returns per G10 pair, long/short, sized inversely to each pair's volatility, book at 10% vol, daily signal after the 17:00 NY roll, banded rebalance. | Before each of the 8 scheduled FOMC days, buy an equal-weight basket of the highest-yielding G10 currencies vs USD at the prior close; exit at the close or the next morning. |
| **Evidence** | Both legs documented; near-zero correlation; DB's blend had a quarter of carry's drawdown. | Real premium paid for crash risk; filters have no out-of-sample test. | LRV 2014: Sharpe > 0.5; post-2014 untested. | Strongest long-run record; weak since 2015; short-term trend gone since about 2009. | Peer-reviewed (MTV 2017); small and noisy per event. |
| **Our backtest** | Net Sharpe 0.20 (0.44 with no markup); 1.10 before 2008, negative in each period since. | 0.14 unscaled; +6.7% in 2026 YTD; −23% in late 2008. | Not tested. Signal today: **long USD**, with only about 1.3 points of gross carry. | 0.04 net, 0.29 frictionless; +11.6% in late 2008. | Not tested (needs event-day data). |
| **Expected live profile** | Sharpe roughly 0–0.3; 30–50% drawdowns at 10% vol. | Pays in calm regimes like now; loses in the same crashes as BTC. | Long spells on one side (long USD through much of 2016–2019). | A crisis diversifier with long flat stretches. | Unknown; the premium per event is small and noisy. |
| **Costs** | Markup about 2.6% of equity a year at 1%; spread about 0.8%. | Markup about 1.8% a year; trading under 1× equity a year. | Markup about 1% of equity a year (positions ≈ 1× equity). | Spread about 1% a year before banding; markup 1.6%. | About 16 basket round trips a year. |
| **Build effort** | High: new broker, 9 instruments, financing, margin, plus "Risk to live trading" sign-off. | High, as FX-1. | Medium: 9 pairs, one monthly decision. | High, as FX-1. | Low once FX-1 exists. |
| **Verdict** | Pre-register and test once on post-2015 data, at the cheapest-financing venue. | Only at a markup of 0.5% or less. | Cheapest next test. | Not on its own. | Research only. |

We recommend against building the following, on the evidence above:

- single-pair EURUSD mean reversion (RSI or 5-day reversal), which lost in our own test;
- cross-sectional momentum;
- London-open or Asian-range breakouts;
- trading payrolls, CPI or rate-decision releases;
- gotobi, month-end and day-of-week seasonals;
- trading on COT positioning or broker sentiment;
- value on its own;
- machine-learning forecasters;
- any fade of a pegged or floored pair.

## Conclusion

Forex turns out to be a cost problem more than a signal problem. The signals that work are slow, well known and must be spread across many pairs, and they already have to clear interbank costs in the academic record. The real question is whether a retail account can hold two to three times its equity in positions without paying 1–3% a year for the privilege. At most retail brokers it cannot, and that is why our backtest's frictionless Sharpe of 0.52 shrinks to 0.20.

The premium that remains is mostly carry, which is short volatility. It pays in calm years like 2026 and loses in the same risk-off weeks in which our BTC bot is already flat. The one sleeve that made money in a crisis, FX trend, has lost money since 2015. Forex is therefore not a substitute for the BTC core. At best it is a modest, uncorrelated add-on, and only if a cheap venue exists for our jurisdiction.

Next steps:

1. Decide whether forex is in scope at all. It reverses the Bitcoin-only and single-pair decisions in `CLAUDE.md`, so both developers have to agree.
2. If it is, measure the daily correlation between FX-1 and BTC Option A. No research track measured it, and it is the one number that could change this verdict: a 0.2–0.3 Sharpe sleeve with near-zero correlation would still improve the combined bot.
3. Choose the jurisdiction and venue before writing any code. Compare OANDA's 1% markup, a low-markup broker and CME micro futures on financing cost and contract size for our account size.
4. Pre-register FX-1 and FX-3 in a GitHub issue, test them once on 2015 onward, and log every variant, following the same protocol as the BTC strategy.
