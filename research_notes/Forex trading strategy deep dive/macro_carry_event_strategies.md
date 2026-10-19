# Macro, risk-premia, event-driven and flow-based FX strategies (carry, value, dollar, multi-factor, central-bank events, positioning, seasonals) — evidence and survival after retail costs

*Method note: in this session WebFetch could not resolve any domain (DNS failure on every site tried, including bis.org, nber.org, federalreserve.gov and oanda.com). Every figure below therefore comes from search-engine summaries of abstracts, working papers, fact sheets and news pages, not from full-text reading. Spot-check load-bearing numbers against the PDFs before relying on them. Labels used: **[gross]** = before transaction costs/financing; **[net-BA]** = net of interbank bid-ask only; **[net-fees]** = net of fund fees; **[unclear]** = cost treatment not stated. No published academic carry figure found here is net of retail broker financing markups. Rates are as of mid-October 2026.*

---

## 1. Carry trade: theory and academic evidence

### Takeaway
Currency carry (long high-rate, short low-rate currencies) earns a real but modest premium: Sharpe about 0.5 in post-1980 samples before retail costs, and only 0.2–0.4 over 1900–2012. That premium is mostly pay for crash, volatility and liquidity risk, with negative skew, not a free lunch. The academic case is strongest for the *dollar* part of carry. The dollar-neutral cross-currency part is weak once crash risk is hedged.

### Cited Findings
**Factor structure (Lustig, Roussanov & Verdelhan 2011, RFS)**
- HML_FX (long high-rate, short low-rate currency portfolios) has an annualised Sharpe of **0.54** in an earlier draft whose sample ends 2008. HML_FX explains about **60%** of the variation in average currency-portfolio excess returns — [MIT draft](https://web.mit.edu/adrienv/www/commonriskfactors.pdf); [NBER w14082](https://www.nber.org/system/files/working_papers/w14082/revisions/w14082.rev0.pdf)
- A later draft reports Sharpe **0.50 after bid-ask spreads [net-BA]**. In that draft an unconditional sort gives Sharpe 0.23 against 0.70 for the conditional sort. The authors argue currency Sharpe ratios are "comparable to the ones measured in equity markets, even after controlling for bid-ask spreads" — [Notre Dame copy of RFS 2011](https://www3.nd.edu/~nmark/GradMacroFinance/LustigRoussanovVerdelhan_RFS_2011.pdf); [UPenn repository](https://repository.upenn.edu/server/api/core/bitstreams/31f4f35e-2339-4f9d-bffc-3fa4a6606957/content)

**Peso problem (Burnside, Eichenbaum, Kleshchelski & Rebelo 2011, RFS 24(3):853–891)**
- A carry trade hedged with currency options against large adverse moves has average payoffs "statistically indistinguishable" from the unhedged trade. The authors conclude that peso events (rare large crashes) are not a major driver of carry payoffs. They model the peso event as a state with a very high stochastic discount factor rather than a huge loss — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v24y2011i3p853-891.html); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1596287)
- A later Burnside survey still lists peso events as "a candidate explanation" — [NBER w17278](https://www.nber.org/system/files/working_papers/w17278/w17278.pdf)

**Crash risk (Brunnermeier, Nagel & Pedersen 2008, NBER Macro Annual 23)**
- Exchange-rate moves between high- and low-rate currencies are **negatively skewed**. The skew comes from sudden unwinding of carry positions "in periods in which risk appetite and funding liquidity decrease". Funding-liquidity measures forecast FX moves. Carry losses *reduce* future crash risk but *increase* the price of crash risk — [NBER w14473](https://www.nber.org/system/files/working_papers/w14473/w14473.pdf); [U. Chicago Press](https://www.journals.uchicago.edu/doi/10.1086/593088)
- In weeks when the VIX rises, carry tends to lose money, and risk-reversal prices and carry activity fall — [BNP, U. Chicago Press](https://www.journals.uchicago.edu/doi/10.1086/593088) (attribution from the search summary)

**Volatility risk (Menkhoff, Sarno, Schmeling & Schrimpf 2012, JF 67(2):681–718)**
- Innovations in global FX volatility explain **more than 90%** of the cross-section of excess returns across five carry portfolios. High-rate currencies fall when global FX volatility jumps, and low-rate currencies hedge. Liquidity risk also matters, but less — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01728.x); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1342968)

**Dollar vs dollar-neutral carry (Daniel, Hodrick & Lu 2017, Critical Finance Review 6:211–262)**
- Dollar-neutral carry trades show **insignificant abnormal returns**. The dollar-exposure component earns significant abnormal returns "with little skewness". It is the **dollar-neutral part that carries the downside risk** — [Columbia PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/6378/Daniel.Hodrick.Lu.Carry%20Trade.Critical%20Finance%20Review.2017.pdf); [NBER w20433](https://www.nber.org/papers/w20433)
- The equal-weighted carry Sharpe depends on the base currency: **0.78** (SE 0.19) USD-based and **0.36** JPY-based. A spread-weighted, risk-rebalanced version reaches **1.02** **[unclear]** — [Columbia PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/6378/Daniel.Hodrick.Lu.Carry%20Trade.Critical%20Finance%20Review.2017.pdf)

**Carry everywhere (Koijen, Moskowitz, Pedersen & Vrugt 2018, JFE 127(2):197–225)**
- Carry predicts returns cross-sectionally and in time series across asset classes. A diversified global carry factor has Sharpe about **1.1–1.2** (by draft), against about **0.74–0.8** for the average single-asset-class carry strategy. Carry drawdowns cluster in global recessions and in liquidity and volatility shocks — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X17302908); [CBS accepted manuscript](https://research-api.cbs.dk/ws/portalfiles/portal/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf); [Wharton draft](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2014/06/Carry.pdf)
- A slower "carry1-12" signal (12-month average carry) has a diversified Sharpe of **0.93** against **1.41** for current carry in one draft (multi-asset, not FX only) — [FMG draft](https://www.fmg.ac.uk/sites/default/files/2020-08/Ralph-Koijen-paper.pdf)
- Koijen and Pedersen host updated carry factor data — [Pedersen data page](https://www.lhpedersen.com/data)

**Crash-neutral carry (Jurek 2014, JFE 113(3):325–347)**
- Crash-risk premia explain **30–40%** of carry excess returns. In the working-paper version, carry that is dollar-neutral *and* crash-hedged has excess returns "statistically indistinguishable from zero" — [IDEAS](https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html); [NBER conf. WP](http://users.nber.org/~confer/2008/apf08/jurek.pdf)

**Very long samples**
- Doskov & Swinkels (1900–2012, 20 currencies) find carry Sharpe of only **0.2–0.4**, "markedly lower than the Sharpe ratios above 0.6 reported for recent sample periods". Large losses do not always coincide with equity losses — [Quantpedia summary](https://vvv.quantpedia.com/?p=571)
- A 200+ year study finds FX carry, momentum and value all still produce positive returns over the full span — [Quantpedia](https://quantpedia.com/fx-carry-value-momentum-strategies-over-their-200-year-history/)

### Inferences
- **Mechanism matters for a bot.** The premium pays for losses in global risk-off episodes such as 2008 and August 2024. Any carry bot will therefore lose money at the same time as BTC and equities. It is not a diversifier in a crash.
- The DHL and Jurek results suggest that **most of the reliably priced premium sits in the dollar leg** (see §7). The cross-sectional ranking among non-USD currencies adds crash risk without much reward.
- The gap between the long-sample Sharpe (0.2–0.4) and the post-1980 Sharpe (about 0.5) is a warning in itself. A realistic *ex ante* gross Sharpe for G10 carry is about 0.2–0.5, before financing markups (§5).

### Gaps
- No FX-only Sharpe from Koijen et al. could be extracted; only the multi-asset figures surfaced.
- Exact sample periods for each LRV draft were not visible in the summaries.

---

## 2. Carry trade: track record 2008–2026, including the August 2024 unwind and the 2022–2026 revival

### Takeaway
G10 carry was close to dead from 2008 to about 2021. The ETF tracking it lost 28% in 2008, then went nowhere and closed in 2023, and one rebuild of that ETF's index shows Sharpe 0.07 over about 19.5 years. Carry came back strongly as rates normalised from 2022. EM carry had its best year since 2009 in 2025 and a strong 2026. The August 2024 yen unwind and a smaller July–September 2026 yen squeeze show that the crash risk is still live.

### Cited Findings
**2008 and the following decade**
- Invesco DB G10 Currency Harvest (DBV; long the top 3 and short the bottom 3 G10 yielders) returned **−28.40% in 2008** and **+21.28% in 2009** **[net-fees]** — [Yahoo Finance](https://nz.finance.yahoo.com/quote/DBV/performance/). Investing.com lists it as out of business from **10 March 2023** — [Investing.com](https://www.investing.com/etfs/powershares-db-g10-curr.-harvest-profile)
- An independent rebuild of the DBV-style G10 basket from free data (lagged rates, quarterly rebalance, USD ranked but never traded) returned **0.74%/yr on 9.8% volatility, Sharpe 0.07, over about 19.5 years** **[gross of the ETF's 0.78% fee]**. In the calmest fifth of months it earned **+4.8%/yr**; in the most stressed fifth it lost **−15.6%/yr**. The stressed regime could be flagged in advance only with *implied equity volatility*, not the basket's own realised volatility. The USD leg was skipped in 65.4% of months — [Alpha in Academia, "Carry's Zero"](https://www.alphainacademia.com/p/carrys-zero)
- Quantpedia's indicative FX carry figures (Deutsche Bank Currency Carry USD index, 1989–2009) are **7.27%/yr, 9.6% vol, Sharpe 0.29, max drawdown about −37%** **[unclear]** — [Quantpedia screener](https://quantpedia.com/Screener/Details/5); [Quantpedia strategy page](https://quantpedia.com/strategies/fx-carry-trade). DB's own 2009 factsheet shows a **−37.07%** max drawdown for the carry component — [DB Currency Returns brochure](https://quantpedia.com/www/DBCR_Brochure.pdf)
- In 2008 the currencies that fell most during the equity-volatility spike had offered the highest yields in the previous six months. The VIX rose from **19 on 22 Aug 2008 to 80 on 27 Oct 2008** — [BIS Quarterly Review Dec 2009](https://www.bis.org/publ/qtrpdf/r_qt0912i.pdf)
- Unverified secondary claims: a carry index fell about 30% peak to trough in 2008, and AUD fell about 40% from above parity to near 0.60 — [Halleytech Substack](https://halleytech.substack.com/p/carry-crashes-picking-up-pennies-in-front-of-a-steamroller)
- Fan, Paseka, Qi & Zhang (JIMF 2022) find carry performance "declined sharply after the global financial crisis". They attribute the decline mainly to the *disappearance of downside-risk compensation*, not to under-diversification or lower crash risk — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1042443121001670)
- Standard Chartered's G10 FX Carry Index (SCINFXC) was discontinued at end-December 2024 — [Bloomberg quote page](https://www.bloomberg.com/quote/SCINFXC:IND)

**2022–2026 revival**
- Goldman Sachs (via Tickmill) says that in early 2026 carry explained "a historic majority" of total returns on major USD pairs, comparable to 2023, "a strong carry year". It also says the usual gap between EM and G10 carry is "narrower than usual" — [Tickmill summary of GS](https://www.tickmill.com/blog/institutional-insights-goldman-sachs-g10-fx-carry-comeback)
- A Bloomberg EM carry measure returned **about 17% in 2025, its biggest gain since 2009** — [Bloomberg, 14 Dec 2025](https://www.bloomberg.com/news/articles/2025-12-14/carry-trade-revival-that-electrified-em-spurs-optimism-for-2026)
- In 2026 one carry gauge was up **about 12% by April**, the strongest start since 2023 — [FXBrokerTrust](https://www.fxbrokertrust.com/insights/emerging-market-currencies-lead-2026-forex-as-carry-trades-hit-threeyear-best-start). A euro-funded BRL/COP/TRY basket was up **about 19% YTD in early August 2026** — [Swissinfo/Bloomberg](https://www.swissinfo.ch/eng/carry-trade-is-powering-on-as-investors-sidestep-yens-gains/91850324); [Japan Times](https://www.japantimes.co.jp/business/2026/08/06/markets/emerging-market-yen-carry-trade/). A post cites about +18% for an EM carry basket against about **+8% for a G10 carry strategy** (date unclear, low-quality source) — [Kobeissi Letter on X](https://x.com/KobeissiLetter/status/2081088764453998928)
- USD returns from carry year to mid-October 2026 per one research firm: COP about 30%, BRL about 20%, ARS 19.3% (single source) — [Rio Times / Delphos](https://www.riotimesonline.com/argentina-carry-trade-dollar-gain-2026/)
- Counterpoint: the JPM GBI-EM Global Diversified (EM local-currency *bonds*) returned **−0.94% in Q3 2026** in USD. Carry was outweighed by higher local yields and a late-quarter USD rebound — [SSGA](https://www.ssga.com/us/en/institutional/insights/emerging-market-debt-commentary-q3-2026)

**August 2024 yen carry unwind**
- BIS Bulletin No 90 (27 Aug 2024): leveraged strategies were forced to unwind, and yen-funded currency carry trades were "the hardest hit". The peak was **5 Aug, when TOPIX lost 12% in one day**. Fragility showed from the first half of July, when the yen's depreciation trend reversed amid rumoured BoJ intervention, with signs of unwinding in the 24 July equity sell-off. The VIX spike "far exceeded" what S&P 500 returns implied — [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.pdf); [BIS alt. URL](https://www.bis.org/publications/bulletin-90-market-turbulence-and-carry-trade-unwind-august-2024.pdf)
- On 5 Aug 2024 the **VIX hit 65 intraday** (from about 23 the previous Friday), the **Nikkei fell about 12%** (12.4% per other reports), and the yen rose 2.6% on the day to 142.79/USD — [CNBC](https://www.cnbc.com/2024/08/04/stock-market-today-live-updates.html)
- Size of the yen move by window: **+14% vs USD from 10 July to 5 Aug** per [Schwab](https://schwabassetmanagement.com/story/carry-trade-unwind-is-it-really-over); "roughly 6% within days" per [WisdomTree](https://www.wisdomtree.com/ch/de/insights/blog/positioning-for-a-stronger-yen). These are different windows, not a contradiction.
- Seven yen crosses fell **9.9% to 18.7%** from their highs in the 2024 unwind; **MXN/JPY fell 18.7%** — [TickerLayer](https://tickerlayer.com/learn/yen-carry-trade)
- Aggregate figures such as "$250–500bn of carry unwound" come only from low-quality sites and are not confirmed by BIS or major news sources — [5quadrants](https://5quadrants.com/risk/yen-carry-trade-unwind/)

**2026 yen episode**
- USD/JPY peaked at **163.87 on 23 Jul 2026** (about 164, its weakest yen since 1986). After a **joint US–Japan intervention** it fell 6.3% to 153.53 by 11 Sep, then rebounded to 158.10 on 15 Oct. Seven yen crosses fell only **4.0–6.3%** from their highs between 1 Jul and 15 Sep 2026, against 9.9–18.7% in 2024 — [TickerLayer, 16 Oct 2026](https://tickerlayer.com/learn/yen-carry-trade); [CNBC, 20 Aug 2026](https://www.cnbc.com/2026/08/20/us-japan-yen-intervention-bank-of-japan-carry-trade.html)
- CFTC: leveraged funds held **178,742 short vs 76,752 long** CME yen futures contracts as of 28 Jul 2026 — [TickerLayer](https://tickerlayer.com/learn/yen-carry-trade)
- EM carry trades "showing resilience even after a joint U.S.-Japan currency intervention" — [Japan Times](https://www.japantimes.co.jp/business/2026/08/06/markets/emerging-market-yen-carry-trade/)

### Inferences
- **By period** (rough synthesis, mostly gross):
  - **2008–2014:** a large 2008 crash (DBV −28%), a 2009 rebound, then flat to negative as G10 rates converged near zero.
  - **2015–2021:** weak. G10 rate spreads were tiny, and the 2018–2020 style-premia slump hit carry too.
  - **2022–2026:** the best G10 conditions since 2007, because rate dispersion returned, and EM carry is very strong (2025 best since 2009). The cost was sharp, short unwinds in Aug 2024 and Jul–Sep 2026.
- The "Carry's Zero" regime split (+4.8% calm, −15.6% stressed) is the clearest numeric case for a **risk-off filter on implied volatility** (§4). Without one, a G10 carry bot's long-run edge rounds to zero.
- The 2026 rally coincides with a global hiking cycle (§3). Rate *dispersion* is high, which historically favours carry, but so is policy-surprise risk (interventions, hikes in low-yielders such as the BoJ).

### Gaps
- No verified year-by-year G10 carry index returns for 2015–2025 (Bloomberg FX Carry Trade indices, BFXCAR-type tickers, were not retrievable).
- No reliable figure for the 2008 peak-to-trough of a G10 carry index from a primary source.
- No verified total size of the yen carry trade.

---

## 3. Carry: live trades and rate differentials as of October 2026

### Takeaway
Mid-October 2026 sits in a global *hiking* cycle driven by oil and inflation shocks. In G10 the high yielders are AUD (4.60%), NOK (4.50%), USD (3.75–4.00%) and GBP (3.75%); the funders are CHF (0%), JPY (1.25%) and SEK (1.75%). Policy-rate differentials for the classic G10 crosses are about 2.6–4.6 percentage points (pp). EM offers far more: TRY 37%, BRL 13.75%, ZAR 7.25%, MXN 6.5%, with conflicting reports on MXN and BRL.

### Cited Findings
**G10 policy rates (latest decision, mid-Oct 2026)**

| Currency | Policy rate | Last move | Source |
|---|---|---|---|
| USD | 3.75–4.00% | +25bp, 16 Sep 2026 (12–0; first hike since 2023; IORB 3.90%) | [Fed statement](https://www.federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf); [CNBC](https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html) |
| EUR | 2.50% deposit (MRO 2.65%) | +25bp effective 16 Sep 2026 | [ECB account](https://www.ecb.europa.eu/press/accounts/2026/html/ecb.mg261008~a10153d090.en.html); [DNB](https://www.dnb.nl/en/the-euro-and-europe/the-ecb-s-monetary-policy/ecb-interest-rates/) |
| JPY | 1.25% | +25bp, 18 Sep 2026 (7–2), highest since 1995 | [CNBC](https://www.cnbc.com/2026/09/18/japan-raises-rates-30-year-high-yen-jgb.html); [MTS Insights](https://www.mtsinsights.com/summaries/11002/) |
| GBP | 3.75% | Held 17 Sep 2026 (6–3, three votes to hike) | [MTS Insights](https://www.mtsinsights.com/summaries/10990/); [Kael Tripton](https://www.kaeltripton.com/bank-rate-held-mpc-vote-split-three-for-rise/) |
| CHF | 0.00% | Held 24 Sep 2026 | [Admiral Markets](https://admiralmarkets.com/analytics/traders-blog/snb-rate-decision-september-2026); [Central Banking](https://www.centralbanking.com/central-banks/monetary-policy/monetary-policy-decisions/7977033/switzerland-sweden-and-hungary-hold-rates-norway-hikes) |
| AUD | 4.60% | +25bp, 29 Sep 2026 (fourth hike of 2026) | [ABC News](https://www.abc.net.au/news/2026-09-29/asx-markets-business-news-live-updates-tuesday-29-september/107206212); [Azura](https://azurafinancial.com.au/azura-financial-market-update-october-2026/) |
| NZD | 2.75% (moderate confidence) | Hikes in Jul and Aug 2026; 28 Oct decision "completely open" | [investingLive](https://investinglive.com/central-banks/rbnz-s-conway-says-october-rate-decision-completely-open-ocr-more-likely-to-rise/); conflicting older 2.25% at [RNZ](https://www.rnz.co.nz/news/business/591776/reserve-bank-holds-official-cash-rate-at-2-point-25-percent) |
| CAD | 2.25% (moderate confidence) | Held since Oct 2025; cut possible 28 Oct after −68k jobs | [Rio Times](https://www.riotimesonline.com/bank-of-canada-october-28-rate-decision-jobs-drop-2026) |
| NOK | 4.50% | +25bp, 23 Sep 2026 (second hike of 2026) | [Norges Bank](https://www.norges-bank.no/en/topics/monetary-policy/Monetary-policy-meetings/2026/september-2026/) |
| SEK | 1.75% | Held, Sep 2026 | [Riksbank](https://www.riksbank.se/en-gb/monetary-policy/monetary-policy-report/2026/monetary-policy-decision-september-2026/) |

**EM rates**
- **TRY 37%** one-week repo, held 10 Sep (fifth straight hold), October cut possible — [Central Banking](https://www.centralbanking.com/central-banks/monetary-policy/monetary-policy-decisions/7976881/turkey-holds-rates-for-fifth-consecutive-meeting); [Bloomberg](https://www.bloomberg.com/news/articles/2026-09-10/turkey-holds-rates-steady-in-face-of-oil-price-inflation-risks)
- **BRL 13.75%** after a 25bp September cut, with a real rate near 9.5% — [Swissinfo/Bloomberg](https://www.swissinfo.ch/eng/a-higher-rate-world-is-in-store-as-central-banks-approach-2027/92200921); [Rio Times](https://www.riotimesonline.com/brazil-economy-2026-state-of/). Contradicted by [Finobird](https://finobird.com/central-banks/global-rate-cycle-2026-ecb-and-rbnz-hike-as-fed-boc-and-boe-ease-2026-09-15/) (14.0%).
- **MXN 6.50%**, held for a third straight meeting in September — [Swissinfo/Bloomberg](https://www.swissinfo.ch/eng/a-higher-rate-world-is-in-store-as-central-banks-approach-2027/92200921). Contradicted by Finobird's 9.5% (likely stale or wrong).
- **ZAR 7.25%** after a 25bp hike on 23 Sep — [Trading Economics](https://tradingeconomics.com/south-africa/interest-rate/news/586122)
- The USD/JPY carry was **2.625pp on 15 Oct 2026, down from 5.475pp in Jan 2024**. Carry-to-risk was **0.57 for MXN/JPY** against **0.33 for USD/JPY** — [TickerLayer](https://tickerlayer.com/learn/yen-carry-trade)
- Typical 2026 structure: fund in JPY or CHF (or EUR), buy BRL, MXN and ZAR — [FXBrokerTrust](https://www.fxbrokertrust.com/insights/emerging-market-currencies-lead-2026-forex-as-carry-trades-hit-threeyear-best-start)

### Inferences
- **Policy-rate differentials** (my arithmetic from the table; USD at the 3.875% midpoint). The rates a broker actually pays track tom-next and forward points, not policy rates.

  | Pair | Differential |
  |---|---|
  | AUD/CHF | 4.60pp |
  | NOK/CHF | 4.50pp |
  | USD/CHF | 3.875pp |
  | AUD/JPY | 3.35pp |
  | NOK/JPY | 3.25pp |
  | USD/JPY | 2.625pp (matches TickerLayer's figure) |
  | GBP/JPY | 2.50pp |
  | AUD/SEK | 2.85pp |
  | MXN/JPY | 5.25pp |
  | ZAR/JPY | 6.0pp |
  | BRL/JPY | 12.5pp |
  | TRY/JPY | about 35.75pp |

- **G10 "3×3" carry portfolio today:** long AUD, NOK, USD; short CHF, JPY, SEK. The average gross spread is about (4.60 + 4.50 + 3.875)/3 − (0 + 1.25 + 1.75)/3 ≈ **3.3pp**. That is the best G10 dispersion in years.
- **Funding-side risks are unusually high.** The BoJ is hiking (1.25% and rising), the Japanese and US authorities intervened jointly in 2026, and speculators were still heavily short yen in July. JPY funding is therefore the most crowded leg. CHF funding (SNB at 0%) is cleaner on carry, but CHF is the classic risk-off haven.
- TRY and BRL carry is huge on paper. For a retail bot, though, broker availability, wide spreads, high CFD margin requirements, extra swap markups on exotic pairs (§5) and devaluation risk make them hard to harvest. MXN and ZAR are the most practical EM legs.

### Gaps
- No primary-source confirmation for the RBNZ, BoC, Banxico, BCB or SARB levels (I relied on news and secondary sites, and the MXN and BRL figures conflict).
- Market tom-next, forward-implied differentials and actual broker swap tables for October 2026 were not retrievable.

---

## 4. Carry: crash-protection overlays (volatility filters, VIX filter, momentum)

### Takeaway
There is good evidence that carry losses cluster when implied volatility rises. Volatility-scaling raises factor Sharpe ratios in general, and a trend or momentum overlay on carry improves Sharpe and drawdown. Buying option protection costs about what it saves. None of these overlays has a published, net-of-retail-cost, out-of-sample FX test.

### Cited Findings
- Carry loses in weeks when the VIX rises; risk reversals and carry activity fall at the same time — [BNP 2008](https://www.journals.uchicago.edu/doi/10.1086/593088)
- Of the regime signals tested in the G10 carry rebuild, only *implied equity volatility* flagged the stressed regime (−15.6%/yr) ahead of time. The basket's own realised volatility did not — [Alpha in Academia](https://www.alphainacademia.com/p/carrys-zero)
- Volatility-managed portfolios: scaling exposure by inverse recent variance raises Sharpe ratios across factors, *including currency carry*, because volatility changes are not matched by changes in expected return — [Moreira & Muir NBER w22208](https://www.nber.org/system/files/working_papers/w22208/w22208.pdf)
- Global FX volatility innovations are the priced risk in carry (more than 90% of the cross-section) — [Menkhoff et al. 2012](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01728.x)
- Option hedging: hedged carry payoffs are statistically indistinguishable from unhedged — [Burnside et al. 2011](https://ideas.repec.org/a/oup/rfinst/v24y2011i3p853-891.html). Crash-hedged, dollar-neutral carry returns about zero — [Jurek WP](http://users.nber.org/~confer/2008/apf08/jurek.pdf)
- Trend overlay: Quantpedia's research summary says adding a trend-following filter to FX carry gives a higher Sharpe and a smaller max drawdown than carry alone — [Quantpedia](https://quantpedia.com/new-research-paper-shows-how-to-easily-improve-5-fx-carry-trade/); [Swedroe, ETF.com](https://www.etf.com/node/94260.md). Quantpedia also maintains a list of carry risk-mitigation papers — [Quantpedia](https://quantpedia.com/fx-carry-risk-mitigation-papers/)
- Carry plus momentum (Burnside, Eichenbaum & Rebelo 2011):
  - The average individual carry trade has Sharpe **0.42**, about half that of the equal-weighted carry portfolio.
  - Equal-weighted momentum has a **7.3%** standard deviation and Sharpe **0.62**.
  - The paper also studies a **50/50 carry–momentum** portfolio **[gross]** — [Kellogg PDF](https://www.kellogg.northwestern.edu/faculty/rebelo/htm/carry.pdf)
  - In a related Burnside paper, transaction costs cut the equal-weighted carry Sharpe from about **0.306 to 0.234** **[net-BA]** — [NBER Reporter summary](https://www.nber.org/reporter/2012number3/understanding-profitability-currency-trading-strategies) (attribution from the search summary is uncertain)
- Macrosynergy: valuation-adjusted carry strategies outperformed simple real carry (figures not visible) — [Macrosynergy](https://macrosynergy.com/research/advanced-fx-carry-strategies-with-valuation-adjustment/)

### Inferences
- **Codeable overlay set, in order of evidence strength:**
  1. **Vol-scaling:** target portfolio volatility of 5–8% using 1–3 month realised volatility of each pair.
  2. **Implied-vol risk-off switch:** go flat or halve carry when the VIX is above its trailing 1-year 80th percentile, or when the VIX rises more than about 30% over 5 days.
  3. **Trend agreement:** hold a carry pair only if its 3–12 month spot return is not strongly against the carry direction.

  The thresholds are illustrative, not from a paper. Choose them *before* backtesting and test robustness across a range, as the BTC study did for SMA lengths.
- The VIX is free and daily, so the filter adds no data cost. It does add turnover: each risk-off flip costs spread twice. At monthly or weekly evaluation that cost is small in G10.
- A filter reacting on a daily close would have cut exposure only partway through the 24 Jul to 5 Aug 2024 move. Expect overlays to *reduce*, not avoid, crash losses.

### Gaps
- No peer-reviewed out-of-sample test of a simple VIX threshold on FX carry was found.
- The exact net-of-cost combined carry–momentum Sharpe from Burnside, Eichenbaum & Rebelo was not visible.

---

## 5. Carry: how retail broker financing (swap/rollover) is priced, and whether the markup erases the carry

### Takeaway
Every retail broker found prices overnight financing as the interbank tom-next or benchmark rate differential plus a markup. Published markups range from about ±0.35–0.75%/yr (Saxo's tom-next tiers) to "up to 3%" (Pepperstone UK). IG's admin fee is 0.3–1.5% by region and version, IBKR forex CFDs about 1.0%, and the long-run AUD/JPY study assumes 1.5%. The markup applies to the *full notional*, and the realised G10 carry excess return has historically been only about 0–3%/yr. A 1–2% markup therefore erases most or all of the historical G10 carry edge, especially with leverage. It leaves a meaningful but smaller share of today's unusually wide 3–5pp differentials.

### Cited Findings

| Broker | Formula / markup found | Source |
|---|---|---|
| OANDA | Daily charge = position value × funding rate × days/365 × FX conversion. FX funding rate = market rate (liquidity providers' tom-next) + instrument-specific admin fee, with separate long and short rates. Worked example uses illustrative −3.00% long / +1.60% short EUR/USD. A shown EUR/USD long of −2.68% "including 1% admin fee" may refer to the metals fee. The per-pair FX admin-fee table could not be read. | [OANDA AU help](https://help.oanda.com/au/en/faqs/financing-costs-au.htm); [OANDA SG help](https://help.oanda.com/sg/en/faqs/financing-costs.htm); [OANDA UK](https://www.oanda.com/uk-en/trading/financing-costs) |
| IG | Tom-next rate ± admin fee (long rate raised, short rate lowered by the fee). Admin fee quoted as "not exceeding 0.3% (0.8% for mini)" on a UK page, **0.5%/yr** (US), **0.8%** (Singapore), **1%** (Switzerland) and **1.5%** (older UK/AU version). Triple charge on Wednesday positions. | [IG UK](https://www.ig.com/uk/help-and-support/spread-betting-and-cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-); [IG intl](https://www.ig.com/en/help-and-support/articles/618798-why-is-overnight-funding-charged-and-how-is-it-calculated); [IG SG](https://www.ig.com/sg/help-and-support/articles/720366-why-is-overnight-funding-charged-and-how-is-it-calculated); [IG CH](https://www.ig.com/en-ch/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-); [IG AU](https://www.ig.com/au/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-) (could not map each figure to each regional page with certainty) |
| IBKR (forex CFD) | Client rate = pair benchmark − spread for longs, + spread for shorts. Major-pair spread "starts at **1.0%**", down to **0.5%** for large balances; higher on volatile pairs. A third-party page says an **extra 1%** has applied to MiFID retail clients since Aug 2018 (not confirmed as current). | [IBKR FAQ](https://www.ibkrguides.com/kb/en-us/article-2707.htm); [IBKR UK forex CFDs](https://www.interactivebrokers.co.uk/en/trading/ibkr-forex-cfds.php); [Lynx](https://www.lynxbroker.com/info/ibkr-rates-cfds/) |
| IBKR (spot FX via cash and margin) | IBKR Pro pays benchmark **−0.5%** on cash and charges benchmark **+1.5%** on margin loans (lower at higher tiers; JPY and CHF fall to BM+0.5% at the top tier). Lite: BM−1.5% / BM+2.5%. Benchmarks on 14 Oct 2026: **JPY 0.989%, CHF −0.251%**. | [IBKR margin rates](https://www.interactivebrokers.com/en/trading/margin-rates.php); [IBKR HK tiers](https://www.clientam.com.hk/en/trading/margin-rates.php); [Lynx benchmarks](https://www.lynxbroker.com/info/ibkr-margin-rates/) |
| Saxo | Rollover = tom-next swap points from Tier-1 banks + client-specific markup, plus financing of unrealised P&L. Tom-next markups by tier: **±0.75/0.50/0.35%** (MENA), **±0.60/0.50/0.45%** (HK), **±0.65/0.55/0.45%** (CH). An older UK page adds ±2.0–2.5% on P&L financing and **+0.30% extra on MXN, RUB, TRY and ZAR crosses** (possibly superseded). | [Saxo MENA](https://www.home.saxo/en-mena/rates-and-conditions/forex/financing); [Saxo rollovers](https://www.help.saxo/hc/en-ch/articles/360001263583-What-are-Forex-Rollovers); [Saxo HK](https://www.home.saxo/en-hk/rates-and-conditions/forex/spreads-and-commissions); [Saxo CH](https://www.home.saxo/en-ch/rates-and-conditions/forex/spreads-and-commissions) |
| Pepperstone | Funding = tom-next "annualised in points, marked-up by **up to 3%**". A 2.5% admin-fee footnote sits in the index section. Worked EUR/USD 1-lot example: long swap −11.49, short +7.02. | [Pepperstone UK costs PDF](https://eu-assets.contentstack.com/v3/assets/bltd74737b907a31bbb/bltc19314db598b7ab0/UK_Legal_Costs_and_Charges.pdf); [Pepperstone swaps guide](https://pepperstone.com/en-eu/education/what-are-swaps-how-to-calculate-swaps) |

**Empirical size of the haircut**
- Forexop's AUD/JPY study (1 lot long from 2 Jan 2004 at 81.09) models broker swaps as "interbank rate gap minus **1.5 points a year**". By end-2019, interest at interbank rates was about **A$57,615** against about **A$33,606** at broker swaps, so the retail trader kept about **58%** of the carry (my arithmetic). Broker swap tables imply a carry "spread" (long-short swap average) of about **−1.00%/yr at Tickmill** and **−1.53% at FXTM** — [Forexop primer](https://forexop.com/carry-trading-primer/)
- Forexop's swap snapshot for 2 Sep 2020 shows a **negative long AUD/JPY carry of −0.501%** (and −1.542% short). When the differential is small, the markup flips the sign, so a long "carry" trade *pays* — [Forexop AUDJPY swaps](https://forexop.com/swaps/AUDJPY/)

### Inferences
- **Worked example: long AUD/JPY at today's ~3.35pp policy differential.** These are illustrations; real tom-next-implied rates differ.

  | Broker / markup | Net carry |
  |---|---|
  | Saxo top tier (±0.35%) | about 3.0% |
  | IG 0.5–1.5% / IBKR CFD 1.0% | about 1.9–2.9% |
  | IBKR spot (borrow JPY at BM+1.5%, earn AUD at BM−0.5%; about 2pp total) | about 1.35% |
  | Pepperstone at the full 3% | about 0.35% |

- **Leverage multiplies the markup.** At 3× notional on a $10k account, a 1% markup costs about $300/yr (3% of equity), against gross carry of about $1,000.
- **Against the realised edge:**
  - The long-run G10 basket earned **0.74%/yr** gross ([Alpha in Academia](https://www.alphainacademia.com/p/carrys-zero)), and a long-run carry factor about 3.4%/yr ([Fan 2025](https://onlinelibrary.wiley.com/doi/10.1111/fire.70000)).
  - A 1–1.5% markup on each pair therefore removes **30% to more than 100%** of the historical net-of-spot edge.
  - The markup hits the interest component; spot depreciation then takes a further bite on top.
  - **Verdict: in normal (narrow-spread) G10 regimes, retail markup erases most of the carry. In today's wide-dispersion regime (3–5pp), roughly 50–90% of the gross carry survives at a low-markup broker.**
- **Practical rules for a bot:**
  - (a) Rank on the broker's *actual net swap* for the side being held (the carry actually earned), not on central-bank rates.
  - (b) Require net swap ≥ a threshold such as 1.5%/yr before holding.
  - (c) Avoid exotic crosses, which often carry extra markups (Saxo +0.30% on MXN, TRY and ZAR).
  - (d) Account for the Wednesday triple-roll.
  - (e) Keep leverage low.
- Broker choice is the single largest controllable cost in a retail carry strategy. It matters more than spread for a monthly-rebalanced book.

### Gaps
- OANDA's per-pair FX admin-fee table and live IG and Pepperstone swap tables for October 2026 could not be loaded.
- No independent survey compares effective retail swap markups across brokers with a primary-data methodology.
- Whether IBKR's extra 1% for MiFID retail still applies was not confirmed.

---

## 6. Value / PPP (and BEER/FEER)

### Takeaway
Currency value (buy currencies cheap against PPP or fundamentals, sell expensive ones) has weak and slow evidence. Raw PPP signals barely work and have decayed: Quantpedia reports negative out-of-sample results, and PPP value baskets have been almost flat since 2017. Mean reversion has a half-life of 3–5 years. Value is useful only as a slow diversifier inside a multi-factor book, not as a standalone retail strategy.

### Cited Findings
- Menkhoff, Sarno, Schmeling & Schrimpf, "Currency Value" (RFS 2017, 30(2):416–441): raw real exchange rates predict returns but largely capture persistent cross-country risk-premium differences. Adjusting for productivity, export quality, net foreign assets and output gaps "better isolates information related to the currency risk premium" and is consistent with reversion to fundamentals — [City Research Online](https://openaccess.city.ac.uk/id/eprint/14851/13/FXVALUE_Rev3_cepr.pdf); [SSRN](http://ssrn.com/abstract=2492082); [City news summary](https://www.citystgeorges.ac.uk/news-and-events/news/2016/09/adjusting-exchange-rates-affects-currency-value)
- Asness, Moskowitz & Pedersen (JF 2013): value and momentum are negatively correlated in every asset class, including currencies. A 50/50 value–momentum combination across all asset classes has Sharpe **1.42–1.45** (by version) **[gross]**. Currency value is measured with PPP-type comparisons. FX-only Sharpe figures were not extracted — [NYU PDF](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf)
- Quantpedia currency-value (PPP) strategy: OECD PPP fair value against USD, long the 3 most undervalued and short the 3 most overvalued, rebalanced quarterly or monthly. **7.82%/yr, 9.33% vol, Sharpe 0.36, max drawdown −26.4% (1989–2009, DB Currency Valuation USD index) [unclear]**. Out-of-sample results were "slightly negative" and alpha "appears to be deteriorating" — [Quantpedia](https://test.quantpedia.com/strategies/currency-value-factor-ppp-strategy/); [Quantpedia screener](https://quantpedia.com/screener?FilterMarkets=currencies&screener_tab=screener-classic)
- DB's 2009 factsheet: max drawdown of the valuation component **−26.40%** — [DBCR brochure](https://quantpedia.com/www/DBCR_Brochure.pdf)
- PPP-based FX value baskets "almost flat since 2017", with correlation about **0.45** to FX carry — [Resonanz Capital](https://resonanzcapital.com/insights/style-premia-are-they-still-relevant)
- PPP half-life consensus is **3–5 years** (Rogoff 1996, JEL), "far too long" for nominal-rigidity models that predict 1–2 years — [Rogoff](https://web.williams.edu/Economics/macro/rogoff.pdf). Confidence intervals are very wide (lower bound about 1 year, upper bound infinite). Panel studies give 2–2.5 years; Murray & Papell argue that, once corrected, the evidence supports Rogoff — [Murray & Papell](https://www.uh.edu/~dpapell/mp4.pdf)
- Alternative fair-value models: PPP "has good predictive power but offers little economic insight" — [Quantpedia](https://quantpedia.com/alternative-fair-value-models-for-currency-value-strategy/). Macrosynergy studies FX strategies based on real exchange rates — [Macrosynergy](https://macrosynergy.com/research/fx-strategies-based-on-real-exchange-rates/)
- The OECD and Eurostat price about 2,500–3,000 goods for PPPs (the free data source) — [OECD statistics blog](https://oecdstatistics.blog/2017/07/10/purchasing-power-parities-not-only-about-big-macs/)

### Inferences
- **Codeable rule:**
  - Universe: G10.
  - Signal: log(OECD PPP / spot), or the negative of the 5-year change in the real exchange rate, using CPI.
  - Positions: long the cheapest 3, short the richest 3, rebalanced quarterly, inverse-vol sizing.
  - Turnover is very low (positions change perhaps 1–3 times a year), so spread cost is negligible. Financing is not: a value book is often *short* high-yielders, because expensive currencies tend to be high-yielders, so it pays negative carry plus the markup.
- **Practicality:** with a 3–5 year half-life, a retail account could sit through multi-year drawdowns, and the published out-of-sample evidence is negative. **Verdict: not standalone. At most a 1/3 sleeve in a combination (§8).**
- BEER and FEER models (behavioural and fundamental equilibrium exchange rates) need current-account and NFA data. They are mostly produced by the IMF or banks and add model risk; I found nothing showing they beat PPP net of cost.

### Gaps
- No FX-only value Sharpe for 2015–2026 was found from a primary source.
- No net-of-cost BEER/FEER trading evidence was found.
- The specific FX value Sharpe from AMP was not extracted.

---

## 7. The dollar factor and "dollar carry" (Lustig, Roussanov & Verdelhan 2014)

### Takeaway
Dollar carry is a single, simple, monthly switch: long a basket of foreign currencies against USD when US short rates are below the foreign average, short the basket otherwise. In the working paper it has Sharpe above 0.5, is uncorrelated with standard carry, and carries little skew. It is the most retail-friendly risk-premium signal found. In October 2026 its G10 version says **long USD**, since the US rate of about 3.875% is above the G10 ex-US average of about 2.6%.

### Cited Findings
- Rule: go long a basket of foreign currencies and short USD when the basket's average forward discount is positive, and the reverse when it is negative — [LRV, SSRN](https://ssrn.com/abstract=1541230); [Quantpedia](https://quantpedia.com/strategies/dollar-carry-trade)
- Published in JFE 111(3):527–553 (2014). The working paper reports Sharpe ratios "in excess of 0.50", higher than HML carry or US equities, and returns "uncorrelated with the returns on well-known carry trade strategies" **[gross / net-BA not clear]** — [NBER w16427](https://www.nber.org/system/files/working_papers/w16427/revisions/w16427.rev0.pdf); [Wharton copy](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2014/06/05.12.Roussanov.pdf)
- The average forward discount and US industrial production growth forecast **up to 25%** of dollar-return variation at a one-year horizon. The premium is countercyclical, which the authors link to the volatility of the US pricing kernel — [NBER w16427](https://www.nber.org/system/files/working_papers/w16427/revisions/w16427.rev0.pdf)
- DHL (2017): the dollar component of carry earns most of carry's abnormal return, with little skew — [Columbia PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/6378/Daniel.Hodrick.Lu.Carry%20Trade.Critical%20Finance%20Review.2017.pdf)
- Mueller, Tahbaz-Salehi & Vedolin (2017): shorting USD against foreign currencies earns more on FOMC days (see §9) — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12499)
- Recent dollar path:
  - **2025 full year:** DXY −9.4% vs G10 per [Funds Society](https://www.fundssociety.com/en/news/markets/if-the-historical-trend-continues-the-dollar-could-decline-by-8-in-2026/); "over 9%", the weakest since 2017, per [NPR](https://www.npr.org/2026/01/04/nx-s1-5662540/why-the-dollar-fell-over-9-in-2025-and-what-to-expect-in-2026); about −7.4% on the broad index per [Eco3min](https://eco3min.fr/en/us-dollar-worst-first-halves-1973-2025/).
  - **H1 2025:** about −11%, the steepest first-half fall since 1973 on DXY — [Financer](https://financer.com/invest/dxy-index/)
- 2026: the Fed hiked to 3.75–4.00% in September, with a median dot for one more 2026 hike — [Chase](https://www.chase.com/personal/investments/learning-and-insights/article/federal-reserve-raises-rates-officials-signal-one-more-hike-in-2026). There was a "late-quarter rebound in the US dollar" in Q3 2026 — [SSGA](https://www.ssga.com/us/en/institutional/insights/emerging-market-debt-commentary-q3-2026)

### Inferences
- **Codeable rule:**
  - Monthly: compute the average 1-month (or 3-month) rate of the G9 ex-US currencies (or their forward discounts) minus the US rate.
  - If positive, hold an equal-weight long basket of EUR, JPY, GBP, CHF, AUD, NZD, CAD, NOK and SEK against USD (9 USD pairs); if negative, short that basket.
  - Vol-target the basket. Optionally add LRV's US industrial-production signal (free, FRED).
  - Implementation is about 9 liquid USD pairs, about 12 rebalances a year, and rare sign flips. Spread cost is trivial.
- **October 2026 reading (my arithmetic, policy rates from §3):** G9 average = (2.50 + 1.25 + 3.75 + 0 + 4.60 + 2.75 + 2.25 + 4.50 + 1.75)/9 ≈ **2.59%**, against US ≈ 3.875%. The signal is **long USD, short basket**.
  - The short-basket position *earns* carry against low-yielders (CHF, JPY, SEK, EUR) but *pays* against AUD and NOK. Net basket carry is only about 1.3pp gross, so a 1% retail markup would take most of it.
  - Including EM in the basket (as LRV's broader sample does) would likely flip the signal to short USD.
- **Overfitting angle:** a single binary switch with no free parameters is about the most overfitting-resistant FX premium available. The cost is that it can sit on one side for years; it was long USD for much of 2015–2019 by the same logic.

### Gaps
- No post-2014 out-of-sample performance of LRV dollar carry was found.
- The published JFE Sharpe figures were not extracted.
- No backtest of the G10-only version for 2015–2026 was found.

---

## 8. Multi-factor currency portfolios (carry + momentum + value)

### Takeaway
Combining carry, momentum and value is the best-documented way to harvest FX premia with tolerable drawdowns. DB's Currency Returns index had a max drawdown of about −9% against −24% to −37% for its components, and FX styles raised the out-of-sample Sharpe of a global portfolio from 0.64 to 1.05 after costs. Post-2015 performance was weak to middling (2018–2020 slump; value flat since 2017) and has recovered with carry since 2022. Long-run factor Sharpe is about 0.6 for carry and 0.67–0.96 for momentum (gross).

### Cited Findings
- **Deutsche Bank Currency Returns (DBCR):**
  - Construction: equal weights to carry, momentum and valuation, reassessed quarterly. The carry leg buys the top 3 and sells the bottom 3 by 3-month yield — [DB 2007 paper](https://my.liuc.it/MatSup/2006/F86032/DeutscheBank_CurrencyReturnsIndex_070329.pdf); [DB guide to FX indices](http://cbs.db.com/new/docs/DBGuideToFXIndices.pdf)
  - Performance by document: 4% excess return since 1980 with Sharpe **0.77**; later, Sharpe **0.80** with an 11% max drawdown; the 2009 factsheet shows Sharpe **0.65**, max drawdown **−8.91%** against −37.07% (carry), −23.89% (momentum) and −26.40% (valuation) **[gross, partly simulated pre-launch]** — [DB March 2009](http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf); [DBCR brochure](https://quantpedia.com/www/DBCR_Brochure.pdf)
  - Pre-inception history is simulated; DBCR+ launched in Feb 2008 — [SEC filing](https://sec.gov/Archives/edgar/data/1159508/000095010310002326/dp18772_fwp-dbcrplus.htm)
- **Kroencke, Schindler & Schrimpf (Review of Finance 2014, 18(5):1847–1883):** adding a composite of FX carry, momentum and value to global stocks and bonds raises the **out-of-sample Sharpe from 0.64 to 1.05**. Results hold "after transaction costs" in a real-time out-of-sample experiment **[net-BA]** — [IDEAS](https://ideas.repec.org/a/oup/revfin/v18y2014i5p1847-1883..html); [ZEW DP 11-028](https://www.zew.de/fileadmin/FTP/dp/dp11028.pdf)
- **Fan (Financial Review 2025):** equal-weighted FX momentum earns **4.78%/yr, Sharpe 0.963** (max drawdown about 15%); carry earns **3.42%, Sharpe 0.614** (max drawdown about 9%). Sample not visible **[gross]** — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/fire.70000)
- **Resonanz Capital (2005 to Mar 2025):** G10 time-series FX momentum **+5.6%, Sharpe 0.67**; FX carry **+4.9%, Sharpe 0.60**; FX value and size "have lost relevance recently" **[gross]** — [Resonanz](https://resonanzcapital.com/insights/style-premia-are-they-still-relevant). Its 2018–2020 slump note covers losses for value, momentum and carry, with carry hurt by low DM rates and volatility spikes (mainly an equities piece) — [Resonanz](https://resonanzcapital.com/insights/what-caused-the-style-premia-slump-in-2018-2020-a-cautionary-tale)
- **Burnside, Eichenbaum & Rebelo (2011):** carry and momentum combined 50/50 (momentum Sharpe 0.62) — [Kellogg](https://www.kellogg.northwestern.edu/faculty/rebelo/htm/carry.pdf)
- **Record plc (currency manager):** multi-strategy returned **0.86% p.a.** (7.68% cumulative), scaled to a 4% volatility target in USD, per a 2021 presentation. FY-25 AUM **$100.9bn**, with revenue down 8% on lower performance fees; a new $3bn FX Alpha mandate — [Record 2021 presentation](https://recordfg.com/wp-content/uploads/2025/06/2021-Full-Year-Presentation-Record-plc.pdf); [Record FY-25 results](https://www.investormeetcompany.com/companies/record-plc/rns/4209705/view); [DirectorsTalk](https://www.directorstalkinterviews.com/record-currency-management-wins-3bn-fx-alpha-mandate-as-frontier-strategy-expands/4121264400)
- **Long-run:** carry, momentum and value each have positive returns over 200+ years — [Quantpedia](https://quantpedia.com/fx-carry-value-momentum-strategies-over-their-200-year-history/)

### Inferences
- **Codeable rule (DBCR-style, G10):**
  - Monthly or quarterly rebalance.
  - **Carry:** rank on the broker's net swap (or 1–3 month rates); long top 3, short bottom 3.
  - **Momentum:** rank on 3- or 12-month spot return excluding the last month; long top 3, short bottom 3. Cross-sectional momentum belongs to the other researcher; it is noted here only as a combination input.
  - **Value:** as in §6.
  - Equal risk weight per sleeve, net the positions per currency, vol-target the total at 6–8%.
  - The result is about 6–9 pairs. Netting reduces the number of financing markups paid.
- **Performance over time (synthesis):**
  - 2008: the composite held up far better than carry alone (DB's −8.9% max drawdown versus −37% for carry).
  - 2015–2021: mediocre. Value was flat after 2017, and momentum and carry slumped in 2018–2020.
  - 2022–2026: carry-led recovery, while value likely detracted, as it is often short the high-yielders (inference).
  - Record's 0.86% p.a. at 4% volatility is about Sharpe 0.2, a sobering live institutional datapoint.
- **Retail fit:** minimum practical size. With micro-lot or unit sizing, 6–9 positions are feasible at about $5k–$10k or more. Below that, position-size granularity distorts weights (assumption: depends on broker minimums).

### Gaps
- No primary source for AQR's FX-specific style-premia returns for 2015–2026.
- No Millennium Global or Pictet overlay results.
- No year-by-year multi-factor FX returns for 2022–2026.

---

## 9. Central-bank and macro announcement strategies (FOMC, pre-announcement drift, NFP/CPI, surprise indices)

### Takeaway
The only announcement effect with solid peer-reviewed support that works at daily horizons is the FOMC-day premium for being short USD (Mueller, Tahbaz-Salehi & Vedolin 2017). Evidence for an FX pre-FOMC drift conflicts. Price discovery on NFP and CPI happens in seconds to minutes, while retail spreads widen 5–10× around those releases. A retail bot with seconds of latency cannot capture release-time moves. At most it can hold a pre-positioned, low-frequency FOMC-day trade.

### Cited Findings
- **FOMC-day premium (MTV 2017, JF 72(3)):** a short-USD, long-foreign strategy earns higher returns on scheduled FOMC days. The excess return is (i) larger for currencies with higher rate differentials against the US, (ii) larger when monetary-policy uncertainty is higher, and (iii) larger still under Fed easing. The authors interpret it as compensation for policy uncertainty borne by constrained intermediaries **[gross]** — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12499); [Kellogg PDF](https://www.kellogg.northwestern.edu/faculty/alirezat/FXAnnouncements.pdf); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2705818)
- **Pre-FOMC drift:**
  - Lucca & Moench find the drift in equities but **no significant EUR/USD or USD/JPY excess returns on FOMC days since 1994** (daily data) — [NY Fed/Stern](https://web-docs.stern.nyu.edu/old_web/finance/docs/pdfs/Seminars/113w-moench.pdf); [NBER conf.](https://conference.nber.org/confer/2012/APf12/Lucca_Moench.pdf)
  - Contradicted by Lee & Wang (high-frequency data): a positive pre-FOMC drift in currencies, with about **65%** cancelled by low post-FOMC returns realised **12–24 hours** after the announcement — [SSRN 4386170](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4386170)
  - A 2017 AEA paper finds a predictable pre-FOMC dollar return unrelated to the announcement surprise — [AEA](https://topcat.aeaweb.org/conference/2017/preliminary/paper/RAK7GsSa)
- **Speed of price discovery:**
  - Andersen, Bollerslev, Diebold & Vega (AER 2003, 93(1):38–62): using six years of real-time quotes for USD against DEM, GBP, JPY, CHF and EUR, surprises cause **conditional-mean jumps**, so high-frequency FX dynamics are tied to fundamentals, with sign and timing asymmetries — [AEA](https://www.aeaweb.org/articles?id=10.1257%2F000282803321455151); [Duke PDF](https://public.econ.duke.edu/~boller/Published_Papers/aer_03.pdf)
  - Fed IFDP work on one-minute EBS data documents announcement effects on EUR/USD and USD/JPY prices and volume — [IFDP 903](https://www.federalreserve.gov/pubs/ifdp/2007/903/ifdp903.pdf); [IFDP 823](https://www.federalreserve.gov/pubs/ifdp/2004/823/ifdp823.htm)
- **Retail execution around releases** (broker and education sources, low quality):
  - EUR/USD spreads widen from about 1 pip to **5–10+ pips** around NFP and normalise within **2–5 minutes**. Slippage is about 1–3 pips, and EUR/USD can move 3–5 pips within 150–300ms of a release — [AlphaTradeCircle](https://alphatradecircle.com/blog/forex-spread-widening-news-events); [FXNX](https://fxnx.com/en/blog/spread-widening-scheduled-news-peaks-recovery-times); [Trade That Swing](https://tradethatswing.com/how-to-day-trade-non-farm-payrolls-nfp-eurusd-gbpusd/)
- **Macro surprise indices:**
  - A positive change in the US surprise index appreciates USD (Fed IFDP 1093) — [Fed](https://www.federalreserve.gov/pubs/ifdp/2013/1093/ifdp1093.pdf)
  - Macrosynergy: relative economic surprises are "valid predictors of FX forward returns", but the signals are short-lived and need frequent rebalancing — [Macrosynergy](https://macrosynergy.com/research/economic-surprises-and-global-asset-class-returns/)
  - Fulcrum has a paper on US rate surprises and currency returns (details not retrieved) — [Fulcrum PDF](https://fulcrumasset.com/wp-content/uploads/2024/07/us-interest-rate-surprises-and-currency-returns.pdf)
- **Upcoming events:** FOMC 28 Oct 2026 — [CentralBank.watch](https://centralbank.watch/tools/calendar/); ECB 29 Oct — [Euribor-rates.info](https://euribor-rates.info/en/ecb-interest-rates/); BoC and RBNZ 28 Oct — [FinanceCalendar](https://www.financecalendar.com/bank-of-canada-rate-decisions/); RBA 3 Nov, BoE 5 Nov, Norges Bank 5 Nov (sources in §3)

### Inferences
- **Codeable FOMC-day rule (MTV-style):**
  - On each of the 8 scheduled FOMC days, buy an equal-weight basket of the highest-differential G10 currencies (e.g., AUD, NOK, GBP) against USD at the prior day's close.
  - Exit at the close of the announcement day, or the next morning to sidestep Lee & Wang's reversal.
  - Turnover: about 16 basket round trips a year. On 3 pairs at about 1–2 pips each way, roughly 0.5–1.5%/yr of notional in spread (my estimate; retail spreads vary).
  - The per-event premium is small and noisy. Validate on post-2017 data only, after the paper's publication.
  - It is the only event idea that tolerates seconds of latency, because it is positioned *before* the release.
- **NFP, CPI and rate-decision "news trading": no.** The price jumps within seconds (ABDV, EBS studies), spreads are widest exactly then, and retail fills are last in the queue. Post-release drift strategies would need a minute-level, net-of-spread backtest; none was found.
- **Surprise-index tilts** are a possible slow signal (weekly or monthly relative surprises), but the evidence is practitioner-only and the free data is thin (Citi's index is proprietary).

### Gaps
- MTV's per-event magnitude (bp per FOMC day) and its post-2015 performance were not extracted.
- No net-of-retail-cost test of any announcement strategy was found.
- No peer-reviewed evidence on post-release FX drift at retail-feasible horizons.

---

## 10. Positioning and sentiment (CFTC COT, retail broker sentiment, risk reversals)

### Takeaway
Speculator positioning in COT data tends to *follow* or confirm trends rather than mark reversals. The simple contrarian reading is not supported, and some results vanish after multiple-testing correction. Retail traders are contrarian to past moves and largely uninformed, but there is no rigorous evidence that fading them is profitable after costs, and free broker-sentiment feeds are shrinking. Risk reversals relate to crash risk, but the data is not free. Use positioning as a crowding or risk filter at most.

### Cited Findings
- **COT, speculators vs hedgers:** speculative positions usually forecast **continuations**, while hedging positions forecast **reversals** — [UMBC WP](https://economics.umbc.edu/wp-content/uploads/sites/243/2014/09/wp_09_116.pdf)
- **COT peaks and troughs:** peaks and troughs in commercial and non-commercial net positions are "generally useful predictors" of spot changes (Tornell & Yuan 2012, as summarised) — [AEA 2019 paper](https://www.aeaweb.org/conference/2019/preliminary/paper/KkfN9BAN)
- **Klitgaard & Weir:** speculators' net positions line up with the correct direction of spot moves about **75%** of the time (secondhand summary) — [ResearchGate](https://www.researchgate.net/publication/5050511_Exchange_rate_changes_and_net_positions_of_speculators_in_the_futures_market)
- **EUR futures:** evidence that speculators lead EUR/USD "largely collapses if we account for multiple testing" — [Finance Research Letters 2016](https://www.sciencedirect.com/science/article/abs/pii/S1544612316300563)
- **Hedging pressure:** hedging-pressure portfolios earn positive, significant excess returns in currency futures, as in commodities and equities (Fernandez-Perez et al.). Bessembinder (1992) finds currency futures returns vary with hedgers' net holdings — [AUT/AFP paper](https://acfr.aut.ac.nz/__data/assets/pdf_file/0007/188161/AFP-Hedging-pressure-everywhere_Adrian-Fernandez-Perez_2018-DMC.pdf)
- **2026 positioning example:** leveraged funds were net short about 102k CME yen contracts (178,742 short vs 76,752 long) on 28 Jul 2026, just before the yen squeeze — [TickerLayer](https://tickerlayer.com/learn/yen-carry-trade)
- **Retail FX flow:** minute-level aggregate retail EUR/USD positions trade *contrarian to lagged returns*. The behaviour is driven by past prices, not macro news, so retail FX investors "appear largely uninformed". Order flow does respond positively to news sentiment — [JIFMIM 2025](https://www.sciencedirect.com/science/article/abs/pii/S1042443125000368)
- **Retail contrarianism in equities** provides liquidity and may *reduce* short-term reversals; this is not evidence that fading retail pays — [Feedback-trading review](https://dspace.stir.ac.uk/retrieve/e3cad0c2-aa70-415d-a7ae-ec68abd82e68/Economou%20et%20al%202022.pdf)
- **OANDA sentiment data:** OANDA reportedly stopped serving its OrderBook and PositionBook endpoints through the v20 API (2024) — [Dekalog blog](https://dekalogblog.blogspot.com/2024/09/discontinuation-of-oandas-orderbook-and.html). OANDA Japan's labs docs list position-ratio and order-book endpoints (token required) — [OANDA developer JP](https://developer.oanda.com/docs/jp/v1/forex-labs/)
- **Risk reversals and options:**
  - After controlling for rate differentials, the relationship between risk reversals and *future* skewness is **negative** — [BNP NBER w14473](https://www.nber.org/system/files/working_papers/w14473/w14473.pdf)
  - Risk-neutral and realised skewness move in opposite directions after currency returns — [Jurek 2014](https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html)
- **Free COT data:** weekly currency COT data is aggregated by third parties from CFTC releases — [COTData](https://www.cotdata.net/cot/fx)

### Inferences
- **Codeable use as a filter:**
  - Weekly: compute non-commercial (or leveraged-fund) net position ÷ open interest for each currency future, z-scored over 3 years.
  - Do not *add* carry exposure in a pair whose funding currency is in an extreme speculative short (z < −2). Halve exposure if already held.
  - This is a crowding/crash-risk heuristic consistent with BNP's unwind mechanism, **not** a validated alpha source.
  - COT reflects Tuesday positions released later in the week; the CFTC schedule was not re-verified in this session.
- **Retail-sentiment fading:** no peer-reviewed evidence that it pays net of cost. Data access is broker-specific and unstable. Not recommended.
- **Risk reversals:** in principle a crash-risk gauge, but needs paid options data (Bloomberg or Refinitiv). The free VIX substitute (§4) is better supported for retail.

### Gaps
- No primary-source figures on IG Client Sentiment data availability or on any backtest of it.
- Klitgaard & Weir's 75% figure may describe contemporaneous co-movement rather than prediction; the summary was ambiguous and I could not verify it.
- No net-of-cost COT strategy backtests from peer-reviewed sources.

---

## 11. Seasonal and flow effects (month-end and quarter-end rebalancing, turn-of-month, gotobi, Japanese fiscal year-end, holidays, day-of-week)

### Takeaway
Flow seasonals have plausible mechanisms but weak, unstable or short-sample evidence:
- **Month-end equity-rebalancing models:** sell-side only, with significance that comes and goes.
- **Gotobi USD/JPY:** an intraday Tokyo-fix effect, documented mainly on 2018–2020 data.
- **Japanese fiscal year-end:** no consistent March pattern.
- **Turn-of-month and day-of-week:** non-stationary and fading.

None has evidence of surviving retail spreads at the turnover required.

### Cited Findings
- **Month-end rebalancing (sell-side):**
  - UBS models last-5-day FX returns on relative equity returns. Using full-month equity returns *overstates* explanatory power, so the cut-off must be days before month-end.
  - Significance was "low from 2014 to 2018", "more robust post-2019", dipped mid-2021 and in Q3 2024, and has been "declining over consecutive months" in 2026 — [Macrostream summary, May 2026](https://www.macrostream.ai/articles/6a165eefea096911e186e101); [Macrostream, Aug 2026](https://www.macrostream.ai/articles/6a905f39e4dfa51c83d66ddb)
  - Central-bank intervention can override the signal (yen example) — [same](https://www.macrostream.ai/articles/6a165eefea096911e186e101)
  - BNY iFlow publishes month-end rebalancing estimates — [BNY](https://www.bny.com/corporate/global/en/solutions/platforms/execution-services/iflow/fx-g10-em/month-end-rebalancing-usd-likely-to-struggle-cad-to-find-relief.html)
  - The claim that a DXY move above 2% in the month makes the hedge rebalance dominate comes from a single unvetted guide — [TradingFuse](https://tradingfuse.com/research/plain-english-guide-to-month-end-fx-rebalancing-flows)
- **Gotobi** (Japanese settlement days falling on the 5th, 10th, 15th and so on, when importers buy USD at the Tokyo fix):
  - Long USD/JPY from 3:00 to 9:55 JST on gotobi days showed "steadily increasing earnings", and adding a short from 9:55 to 12:00 gave the most stable profits **[unclear costs]** — [Bessho, Sugimoto & Suzuki, arXiv 2301.13204](https://arxiv.org/pdf/2301.13204)
  - Mechanism: before the Tokyo fixing, order imbalances are often large and predictable in direction, as importers' USD buying exceeds exporters' selling — [Ito & Yamada, NBER w22820](https://www.nber.org/system/files/working_papers/w22820/w22820.pdf)
  - Critique: the Bessho sample covers only **2018–2020**, and some design choices were made on the test data — [ForexDetox Substack](https://forexdetox.substack.com/p/the-tokyo-fix-reversal-anomaly-on); see also [Alpha in Academia](https://www.alphainacademia.com/p/can-you-beat-the-market-by-trading)
  - Commercial expert-advisor claims of 65–89% win rates are unverifiable — [MQL5](https://www.mql5.com/en/market/product/162603)
- **Japanese fiscal year-end (March):**
  - Over about 10 years, the yen rose against USD in only **5 of 10 Marches**, giving "no seasonal trading pattern" (dated article) — [MoneyShow](https://www.moneyshow.com/articles/tradingidea-19132/)
  - A seasonal-statistics site claims USD/JPY averages −0.8% in March (42% win rate) and +1.1% in April (62%), with no stated sample — [SeasOptima](https://www.seasoptima.com/en/blog/usdjpy-seasonal-patterns)
- **Turn-of-month and day-of-week:**
  - Kumar (J. Econ. & Business 2016, 1985–2014): FX turn-of-month returns are negative and significantly lower than other days. Monday–Wednesday returns are positive and Thursday–Friday negative. Effects are stronger in EM currencies and **diminish over time** — [IDEAS](https://ideas.repec.org/a/eee/jebusi/v86y2016icp16-32.html)
  - Liano & Kelly (1995): turn-of-month effects in currency futures, positive for JPY and opposite for GBP — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/104402839590008X)
  - In a 29-currency study, day-of-week patterns are "not stationary but dynamic" and tied to microstructure — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0275531904000054)
- **Interaction with the London 4pm fix:** month-end rebalancing flows are executed largely at the WM/R 4pm fix. Fix mechanics belong to the other researcher; the UBS and BNY notes above describe month-end flows, not fix microstructure.

### Inferences
- **Month-end:** a codeable rule exists (e.g., 3 days before month-end, sell the currency whose equity market most outperformed USD equities that month), but evidence is sell-side, regime-dependent and decaying. At 12 round trips a year and a few pips each, costs are small; the problem is the edge, not the cost. **Verdict: research curiosity, not a core strategy.**
- **Gotobi:** an intraday effect (hours) on about 6–8 days a month, needing JST-timed execution. It fits a bot technically (low latency need), but the evidence is a 3-year in-sample result, and every trade pays the USD/JPY spread. **Verdict: paper-trade only, if at all.**
- **Japanese fiscal year-end, turn-of-month, day-of-week:** no reliable edge. Kumar's finding that effects diminish over time is consistent with arbitrage.

### Gaps
- No peer-reviewed study of month-end FX rebalancing returns net of cost.
- No study of FX holiday effects (Christmas, Golden Week, US Thanksgiving) was found.
- No out-of-sample gotobi test after 2020 from a credible source.
- No primary quarter-end-specific FX evidence beyond sell-side notes.

---

## 12. Overall: which family has the best evidence of surviving retail costs and financing at $1k–$50k?

### Takeaway
Only the slow, monthly risk-premium strategies have both academic support and turnover low enough to survive retail spreads: dollar carry, G10 carry with a volatility/VIX and trend filter, and a carry + momentum + value composite. For carry the binding cost is the broker's swap markup, not the spread. With today's 3–5pp G10 differentials and a broker charging about 0.5% or less, a filtered G10 carry or multi-factor book is defensible. With a 1.5–3% markup it is not. Event, positioning and seasonal strategies lack net-of-cost evidence or need speed a retail bot does not have.

### Cited Findings
- Published carry and multi-factor Sharpe ratios are about 0.3–1.0, **gross or net of interbank bid-ask only**:
  - LRV 0.50 net-BA — [LRV](https://www3.nd.edu/~nmark/GradMacroFinance/LustigRoussanovVerdelhan_RFS_2011.pdf)
  - DBCR 0.65–0.80 — [DB](http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf)
  - KSS out-of-sample, after costs — [IDEAS](https://ideas.repec.org/a/oup/revfin/v18y2014i5p1847-1883..html)
  - Long-sample carry 0.2–0.4 — [Quantpedia](https://vvv.quantpedia.com/?p=571)
- **Live or near-live evidence is far weaker:** DBV lost 28% in 2008 and closed in 2023 ([Yahoo](https://nz.finance.yahoo.com/quote/DBV/performance/); [Investing.com](https://www.investing.com/etfs/powershares-db-g10-curr.-harvest-profile)); the G10 rebuild has Sharpe 0.07 over about 19.5 years ([Alpha in Academia](https://www.alphainacademia.com/p/carrys-zero)); Record's multi-strategy made 0.86% p.a. at 4% volatility ([Record](https://recordfg.com/wp-content/uploads/2025/06/2021-Full-Year-Presentation-Record-plc.pdf)).
- **Retail swap markups:** about 0.35% to 3%/yr — [Saxo](https://www.home.saxo/en-mena/rates-and-conditions/forex/financing); [IG](https://www.ig.com/uk/help-and-support/spread-betting-and-cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-); [IBKR](https://www.ibkrguides.com/kb/en-us/article-2707.htm); [Pepperstone](https://eu-assets.contentstack.com/v3/assets/bltd74737b907a31bbb/bltc19314db598b7ab0/UK_Legal_Costs_and_Charges.pdf). Over 2004–2019 they left about 58% of AUD/JPY interbank carry — [Forexop](https://forexop.com/carry-trading-primer/)
- **Today's opportunity set:** the widest G10 dispersion in years (AUD 4.60% / NOK 4.50% vs CHF 0% / JPY 1.25%) and strong EM carry in 2025–26 — sources in §2–§3

### Inferences
**Ranking for a small retail bot (best first):**

1. **Dollar carry (LRV) on 9 G10 USD pairs, monthly, vol-targeted.** No free parameters, about 12 rebalances a year, and the academic premium is concentrated in the dollar leg (DHL). Currently long USD vs G10, where net carry is small, so financing markups bite. Expected live Sharpe is perhaps 0.2–0.5 (judgement).
2. **G10 carry, 3×3 or pair-based, ranked on the *broker's net swap*, with VIX risk-off, trend-agreement and vol-scaling overlays; monthly.** Best economics *right now* (gross spread about 3.3pp). Fails in narrow-spread regimes and loses in global risk-off episodes, the same days BTC falls. Needs a broker markup of about 0.5% or less, leverage of 2× or less, and a net-swap ≥ 1.5% filter. MXN or ZAR legs are optional if offered without extra markups.
3. **Carry + momentum + value composite (DBCR-style), quarterly or monthly.** Best drawdown record and the best overfitting protection through diversification, but more pairs (more markups) and a weak value leg. Needs about $5k–$10k or more for weight granularity (assumption).
4. **FOMC-day short-USD basket (MTV).** Peer-reviewed, latency-tolerant, about 8 events a year. A small, noisy add-on to test after (1)–(2).
5. **Not recommended:** standalone value (too slow, out-of-sample negative); COT or retail-sentiment trading (filter at most); NFP/CPI news trading (seconds-scale, spreads 5–10× wider); month-end, gotobi, fiscal-year-end, turn-of-month and day-of-week seasonals (unstable, short samples, decaying).

**Overfitting guardrails, consistent with the BTC study's standard:**
- Fix the rules from the literature before backtesting (top/bottom 3, monthly, 12-1 momentum, PPP value).
- Report results by regime: 2008–14, 2015–21, 2022–26.
- Charge realistic swap markups (test at 0.5%, 1.0% and 1.5%) and Wednesday triple-rolls.
- Treat post-publication data (post-2011 for carry, post-2014 for dollar carry and KSS, post-2017 for MTV) as the only true out-of-sample period.

**Interaction with the existing BTC bot:** FX carry is short volatility and loses in the same risk-off episodes in which BTC trend-following goes flat. It adds return in calm regimes but little crash diversification. A trend or momentum overlay (the other researcher's domain) is the natural complement.

### Gaps
- No published FX carry or multi-factor backtest uses *retail* swap markups. The other researcher's backtest should model this explicitly.
- Free daily or monthly short-rate and forward-point data was not verified in this session. Likely candidates are central-bank sites, FRED/OECD 3-month interbank rates and the BIS policy-rate dataset; broker swap histories are usually not downloadable.
- Retail CFD availability and margin rules for EM pairs (MXN, ZAR, BRL, TRY) vary by jurisdiction and belong to the broker/regulation researcher.
