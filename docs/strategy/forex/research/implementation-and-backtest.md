# Running a small retail FX bot in Python: brokers, costs, regulation, data, outcomes, tail risk, and our own G10 backtest

*Research method note (applies to every section).* The web-fetch tool could not load any page in this environment: every fetch failed with a DNS error (oanda.com, ig.com, wikipedia.org and others), and curl to most hosts was blocked. So every web figure below comes from **search-result summaries and quoted snippets**, not from reading the full page. Spot-check key numbers on the vendor's own page before relying on them. PyPI's JSON API and raw.githubusercontent.com did work, so library versions and the backtest data come from primary files. Older sources are flagged inline. "Our backtest" figures come from `fx_backtest.py` in this folder; its full output is reproduced in the Part 2 section.

---

## 1. Brokers and APIs a Python bot can use: 2026 status, jurisdictions, demo accounts, CCXT

### Takeaway
For a $1k–$50k account, the realistic API routes are **OANDA v20 REST** (free practice account; US, UK, EU, Australia and more; FTMO completed its takeover in Dec 2025), **Interactive Brokers** via TWS/IB Gateway and `ib_async` (all four regions; IdealPro needs $25k-equivalent orders, so smaller orders get odd-lot pricing), **IG REST + Lightstreamer** (UK, EU and Australia; not the US, where IG's brand is tastyfx), **Saxo OpenAPI** (free simulation environment; not the US) and **cTrader Open API** via brokers such as IC Markets or Pepperstone (not the US). The MetaTrader 5 Python package is Windows-only. FXCM is being broken up (Oct 2026). Dukascopy's API needs about $100k. CME micro FX futures through IBKR are a regulated, exchange-cleared alternative. **CCXT supports no FX broker.**

### Cited Findings
**OANDA**
- The v20 REST API uses separate hosts: `api-fxpractice.oanda.com` for practice (demo) accounts and `api-fxtrade.oanda.com` for live. Tokens are generated in the demo account under Tools → API, and a wrong host is a common cause of "Insufficient authorization" errors — [OANDA help: REST v20 troubleshooting](https://help.oanda.com/us/en/faqs/rest-v20-api-troubleshooting-guide.htm).
- Registering a demo/practice account is free and "provides full access to the API" (third-party wrapper documentation) — [ichimoku vignette (CRAN mirror)](https://packages.oit.ncsu.edu/cran/web/packages/ichimoku/vignettes/xoanda.html).
- Rate limits are not confirmed from OANDA itself. An unofficial Rust SDK cites 120 REST requests/second and 2 new connections/second per IP; another version of its docs says 100 — [docs.rs oanda-rs](https://docs.rs/oanda-rs).
- **Ownership:** CVC Asia Fund IV bought OANDA in 2018 — [Finance Magnates](https://www.financemagnates.com/forex/brokers/breaking-cvc-partners-asia-fund-acquires-oanda-in-landmark-deal/). The prop-trading firm FTMO agreed to buy it in Feb 2025 and **closed on 1 Dec 2025** after approvals from five regulators. It plans to run OANDA as a standalone business — [Finance Magnates](https://www.financemagnates.com/forex/prop-firm-ftmo-closes-oanda-acquisition-deal-after-ten-months/); [TradeInformer](https://tradeinformer.com/broker-news/ftmo-completes-acquisition-of-oanda-after-getting-green-light-from-5-regulators).
- **Entities:**
  - US: OANDA Corporation is registered as an FCM and RFED with the CFTC and is an NFA member.
  - UK: OANDA Europe Ltd, regulated by the FCA (No. 542574).
  - EU: OANDA Europe Markets Ltd, regulated by the MFSA (Malta). One source names a Polish entity (OANDA TMS, supervised by the KNF) instead.
  - Australia: OANDA Australia Pty Ltd, regulated by ASIC.
  - Also: Canada (CIRO), Singapore (MAS), Japan, and a BVI entity for other countries.
  - Sources: [BrokerChooser](https://brokerchooser.com/broker-reviews/oanda-review/is-oanda-legit); [OANDA group page](https://www.oanda.com/group/).
- OANDA CFDs are not available to US residents — [QuantConnect: CFD and forex brokerages](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/cfd-and-forex-brokerages).
- Myfxbook said OANDA was ending the connection method it used and was "introducing a new API" for third-party access (the article's year is unclear) — [Finance Magnates](https://www.financemagnates.com/forex/technology/myfxbook-no-longer-supports-oanda-accounts/).

**Interactive Brokers**
- All IdealPro orders must be at least **USD 25,000 or equivalent**. Smaller orders are odd lots routed to IB's "Ideal" venue. Their limit prices are not shown on IdealPro, and they "generally" fill **1–2 bp** outside the IdealPro quote (another IB page says 1–3 ticks) — [IBKB: Odd Lot FX Transactions](https://ibkb.interactivebrokers.com/tag/forex?page=2); [IBKB: Forex Basics](https://ibkb.interactivebrokers.com/es/node/1460).
- Commission is **0.20 bp of trade value, minimum USD 2.00 per order**, for up to $1bn a month; the rate falls at higher volume — [IBKR spot currency commissions (IE)](https://interactivebrokers.ie/en/pricing/commissions-spot-currencies.php); also cited by [NerdWallet (July 2025)](https://www.nerdwallet.com/p/best/investing/forex-brokers).
- **Paper trading:** you must open a live account first, but there is no minimum deposit. The API requires IBKR Pro, not Lite. Spot FX live data is free (IB Campus, 2020) — [BrokerListings](https://brokerlistings.com/reviews/interactive-brokers/does-interactive-brokers-have-paper-trading); [QuantConnect IB docs](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers).
- IB offers forex to clients in 200+ countries and territories — [QuantConnect IB docs](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers). IB is listed as a US FCM with a Forex Dealer Member designation — [CompareForexBrokers (checked 23 Sep 2026)](https://www.compareforexbrokers.com/us/cftc-regulated/).
- `ib_async` needs a running IB Gateway or TWS with the API port enabled — [ib_async README](https://raw.githubusercontent.com/ib-api-reloaded/ib_async/main/README.md).

**IG**
- IG's REST and streaming (Lightstreamer) APIs are offered to retail clients through IG Labs. The demo REST base path is `demo-api.ig.com/gateway/deal`. The streaming server address comes from the `/session` response, and the CST/X-SECURITY-TOKEN values from the REST login act as the password — [IG UK: how to use IG API](https://www.ig.com/uk/trading-platforms/trading-apis/how-to-use-ig-api); [IG Labs streaming guide](https://net-labs.ig.com/streaming-api-guide.html).
- IG regional pages disagree on demo sign-up: one says use the same email as your live account, another says use your API username — same sources.
- IG US rebranded to **tastyfx** on 24 Jun 2024 for US forex — [FinTech Futures](https://www.fintechfutures.com/press-releases/ig-us-rebrands-foreign-exchange-trading-platform-to-tastyfx). I found no evidence of a public tastyfx API — [ForexBrokers.com](https://forexbrokers.com/reviews/tastyfx).

**Saxo**
- The OpenAPI **simulation environment is free**, with a simulated $100,000 account. The portal issues 24-hour tokens; longer runs need an OAuth app key and secret. Sim REST base: `https://gateway.saxobank.com/sim/openapi`. Live access goes through application management and may need Saxo's approval — [Saxo developer portal](https://www.developer.saxo/openapi/learn/security); [OpenAPI environments](https://wlc1-developerportal.tst.saxobank.com/openapi/learn/openapi-environments).
- Saxo is not available to US residents (secondary source, plus Saxo's own FR page). Minimum deposits are reported as $0 for Classic, $2,000, or €100k in Portugal (sources conflict) — [TradersUnion](https://tradersunion.com/brokers/forex/view/saxo_bank/minimum-deposit/); [Saxo accounts](https://www.home.saxo/accounts/individual).

**cTrader Open API (IC Markets, Pepperstone)**
- The official Python package `ctrader-open-api` (OpenApiPy) uses **Twisted**, not asyncio. Messages are Protobuf (or JSON). Access is open to anyone registered with a cTrader broker — [OpenApiPy (GitHub)](https://github.com/spotware/OpenApiPy); [cTrader Open API docs](https://help.ctrader.com/open-api/).
- Forum reports from 2024–2025 describe broken samples and dropped connections — [cTrader community](https://community.ctrader.com/forum/connect-api-support/45567).
- cTrader is effectively unavailable to US clients, because the brokers that offer it cannot serve the US (2023 forum post) — [cTrader community](https://community.ctrader.com/forum/ctrader-support/11620).

**MetaTrader 5**
- The `MetaTrader5` PyPI package (5.0.6231, uploaded 27 Sep 2026) ships **only `win_amd64` wheels**. Linux needs a Wine bridge such as `mt5linux` (RPyC) — [PyPI MetaTrader5](https://pypi.org/project/MetaTrader5/); [mt5linux](https://pypi.org/project/mt5linux).
- FOREX.com is described as the only listed broker supporting MT5 in the US (Oct 2025). MetaQuotes cracked down on US grey labels in early 2024 — [Benzinga](https://www.benzinga.com/money/best-metatrader-5-brokers); [Finance Magnates](https://www.financemagnates.com/forex/prop-trading-on-metatrader-5-is-back-in-the-us/amp).

**FXCM**
- Jefferies took full ownership in late 2023 by foreclosing on FXCM's parent, which was rebranded Stratos.
- On **6 Oct 2026** Trade Nation agreed to acquire FXCM's UK client book.
- On **12 Oct 2026** AvaTrade announced it will acquire "the majority" of FXCM Group's business and brand rights. The price was not disclosed and the deal had not closed.
- FXCM's sister brand Tradu halted onboarding.
- Sources: [Finance Magnates (Trade Nation)](https://www.financemagnates.com/forex/exclusive-trade-nation-acquires-fxcms-uk-client-book/); [Bernama (AvaTrade release)](https://www.bernama.com/en/press/news.php?id=2618885); [Finance Magnates (Jefferies)](https://www.financemagnates.com/forex/is-jefferies-preparing-to-offload-fxcm/).

**Dukascopy**
- Swiss bank, regulated by FINMA (secondary source). **FIX API access requires a USD 100,000 minimum deposit** and a written project description reviewed by the bank. The JForex API is tied to account tiers starting at USD 100 or 1,000 (the tier table is garbled in search results) — [Dukascopy FIX API account](https://www.dukascopy.com/swiss/deutsch/forex/api/fix-api/fix-api-account/); [Dukascopy accounts](https://www.dukascopy.com/swiss/pt/forex/forex_trading_accounts/).

**CME micro FX futures**
- **Micro EUR/USD (M6E):** 12,500 euros per contract; tick 0.0001 = **$1.25**; quarterly; deliverable — [CME contract specs](https://cmegroup.com/trading/fx/e-micros/e-micro-euro_contractSpecs_futures.html).
- **Micro AUD/USD (M6A):** 10,000 AUD, $1.00 per tick. **Micro GBP/USD (M6B):** 6,250 GBP, $0.625 per tick — [Schwab](https://www.schwab.com/futures/micro-e-mini); [NinjaTrader](https://ninjatrader.com/futures/futures-contracts/currency/micro-currency/).
- M6E initial margin was cited at $340–405 (dated sources) — [Ironbeam](https://www.ironbeam.com/knowledge-base/micro-euro-futures-m6e-contract-specifications/).
- IBKR micro-futures commission is $0.10–0.25 per contract plus exchange and regulatory fees. The page is generic and does not confirm the FX micros — [IBKR micro futures](https://www.interactivebrokers.com/en/trading/micro-futures-comparison.php).

**CCXT**
- PyPI describes `ccxt` 4.5.88 (14 Oct 2026) as "a cryptocurrency trading API with more than 100 exchanges" — [PyPI ccxt](https://pypi.org/project/ccxt/).
- Searching CCXT's README for "oanda", "forex", "fxcm", "interactive brokers", "ig markets" and "saxo" gave **zero matches** — [CCXT README](https://raw.githubusercontent.com/ccxt/ccxt/master/README.md).

**US dealers**
- A third-party list checked 23 Sep 2026 shows six Forex Dealer Members as the retail FX counterparties, including GAIN Capital (FOREX.com; FCM and RFED), Charles Schwab and Interactive Brokers. OANDA Corporation is an FCM/RFED (BrokerChooser, above). RFEDs and FCMs need **$20m minimum net capital** — [CompareForexBrokers](https://www.compareforexbrokers.com/us/cftc-regulated/).

**Summary table** (inferred from the findings above; "?" means not confirmed)

| Route | US | UK | EU | AU | Free demo/paper with API | Python access | Notes for a $1k–50k account |
|---|---|---|---|---|---|---|---|
| OANDA v20 | ✅ (no CFDs) | ✅ | ✅ (Malta) | ✅ | ✅ practice | REST/stream; `oandapyV20`, `tpqoa`, or plain HTTP | Simplest fit; FTMO-owned since Dec 2025 |
| IBKR (TWS/Gateway) | ✅ | ✅ | ✅ | ✅ | ✅ paper (needs live account) | `ib_async`; NautilusTrader adapter | $2 minimum commission and odd-lot pricing below $25k |
| IG REST | ❌ (tastyfx) | ✅ | ✅ | ✅ | ✅ demo | `trading-ig` (community) | Spread betting option in the UK |
| Saxo OpenAPI | ❌ | ✅ | ✅ | ? | ✅ sim ($100k virtual) | REST (no official Python SDK found) | 24h tokens in sim unless OAuth app |
| cTrader Open API | ❌ | ✅ | ✅ | ✅ | ✅ (broker demo) | `ctrader-open-api` (Twisted) | Raw spread + commission accounts |
| MT5 Python | limited (FOREX.com) | ✅ | ✅ | ✅ | ✅ | `MetaTrader5` (Windows only) | Needs Windows VPS or Wine |
| Dukascopy | ? | ? | ✅ (Europe entity) | ? | ? | JForex (Java) / FIX | FIX needs $100k |
| CME micro FX futures | ✅ | ✅ | ✅ | ✅ | via IBKR paper | `ib_async` | M6E ≈ €12,500 notional per contract |
| FXCM | ❌ | being transferred | ? | ? | — | — | Avoid while ownership changes |

### Inferences
- **OANDA is the closest analogue to the current CCXT setup.** It has a plain REST/stream API, a free practice account that maps to the planned `TestnetBroker`, unit-level sizing, and coverage of all four candidate jurisdictions. Its new ownership by FTMO, a prop-trading firm, is a counterparty and governance change worth watching, but nothing found suggests the v20 API is going away.
- **IBKR is the best route for a $25k–50k account that wants exchange-cleared FX futures or the lowest spreads.** It is awkward below $25k, because of odd-lot pricing and the $2 minimum: $2 on a ~$11.7k (10k EUR) order is about 1.7 bp per side, before 1–2 bp of odd-lot slippage. It also needs a resident Gateway process (Java, daily restarts) on the VPS.
- **CME micro FX futures avoid** the retail-forex rules (FIFO, US leverage limits, unsegregated dealer funds). Their contract granularity (≈$7–15k notional) is coarse for a $1k–5k account.
- MT5 and cTrader are poor fits: MT5 is Windows-only, and cTrader's library is Twisted-based where the bot is asyncio.

### Gaps
- No primary OANDA documentation (rate limits, minimum units, the v20 roadmap) could be loaded.
- I could not confirm whether OANDA's EU entity is Malta or Poland in 2026.
- The status of a tastyfx API is unknown.
- IBKR's commission for FX micro futures specifically, and current margins for M6E/M6A/M6B, are unconfirmed.
- Whether Dukascopy demo accounts get API access is unknown.

---

## 2. Python tooling, and which fits the existing architecture

### Takeaway
None of the frameworks drops cleanly into the planned engine. The pragmatic choice is to **write a thin async OANDA v20 adapter (or use `ib_async` for IBKR) behind the existing `Broker` interface**. NautilusTrader is worth studying, since it has a stable IB adapter but no OANDA adapter. Lean/QuantConnect supports OANDA and IB but would replace our engine. backtrader is unmaintained, and vectorbt suits research only.

### Cited Findings
| Package (PyPI) | Latest version / upload | Python | Notes | Source |
|---|---|---|---|---|
| `oandapyV20` | 0.7.2 / 2021-08-27 | — | Third-party wrapper for OANDA REST v20; defaults to the practice environment | [PyPI](https://pypi.org/project/oandapyV20/); [docs](https://oanda-api-v20.readthedocs.io/en/master/oanda-api-v20.html) |
| `v20` (OANDA's official bindings) | 3.0.25.0 / 2018-09-28 | — | Official but untouched since 2018 | [PyPI](https://pypi.org/project/v20/) |
| `tpqoa` | not on PyPI (GitHub) | — | Wrapper class around OANDA's `v20` package, by The Python Quants; installed with `setup.py`; needs at least a practice account | [README](https://raw.githubusercontent.com/yhilpisch/tpqoa/master/README.md) |
| `ib_async` | 2.1.0 / 2025-12-08 | ≥3.10 | asyncio/eventkit; needs TWS or IB Gateway. Fork of `ib_insync` after its author Ewald de Wit died on 11 Mar 2024; IBKR says `ib_insync` is no longer updated and recommends `ib_async` | [PyPI](https://pypi.org/project/ib_async/); [IBKR docs](https://www.interactivebrokers.com/docs/tws-api/doc/third-party-api-platforms/non-standard-tws-api-languages-and-packages/ib-insync-and-ib-async); [changelog](https://data.safetycli.com/changelogs/ib-async) |
| `ib_insync` | 0.9.86 / 2023-07-02 | ≥3.6 | Superseded | [PyPI](https://pypi.org/project/ib_insync/) |
| `nautilus_trader` | 1.231.0 / 2026-08-02 | 3.12–3.14 | "Rust-native… event-driven"; integrations table lists **Interactive Brokers (stable)**, Databento and many crypto venues; **no OANDA** | [PyPI](https://pypi.org/project/nautilus_trader/); [README](https://raw.githubusercontent.com/nautechsystems/nautilus_trader/develop/README.md) |
| `lean` (QuantConnect CLI) | 1.0.230 / 2026-10-15 | ≥3.9 | LEAN supports OANDA (FX/CFD) and IB for live trading. The CLI runs locally or in the cloud; the CLI requires a paid organisation tier | [PyPI](https://pypi.org/project/lean/); [QuantConnect docs](https://www.quantconnect.com/docs/v2/lean-cli/live-trading/brokerages/cfd-and-forex-brokerages) |
| `backtrader` | 1.9.78.123 / 2023-04-19 | — | No release since April 2023 | [PyPI](https://pypi.org/project/backtrader/) |
| `vectorbt` | 1.1.2 / 2026-10-09 | 3.11–3.14 | Vectorised research backtester | [PyPI](https://pypi.org/project/vectorbt/) |
| `trading-ig` | 0.0.25 / 2026-08-25 | ≥3.10 | Community IG REST wrapper | [PyPI](https://pypi.org/project/trading-ig/) |
| `ctrader-open-api` | 0.9.2 / 2024-06-26 | ≥3.8 | Twisted-based | [PyPI](https://pypi.org/project/ctrader-open-api/) |
| `MetaTrader5` | 5.0.6231 / 2026-09-27 | ≥3.6 | win_amd64 wheels only | [PyPI](https://pypi.org/project/MetaTrader5/) |

- The project plan uses one `Broker` interface with `PaperBroker`, `TestnetBroker` and `LiveBroker` implementations, today all built on CCXT. It has a CCXT `exchange/` wrapper, a `Strategy` protocol (`on_candle` → `Signal`), and a `backtest/` module that replays candles through the same Strategy, Risk and PaperBroker code — local file `docs/PLAN.md`, §2.

### Inferences
- **OANDA fit:**
  - `oandapyV20` and `v20` are synchronous and stale (2021 and 2018).
  - An `OandaBroker` built on an async HTTP client (the v20 REST and streaming endpoints) keeps the asyncio engine and the `Decimal` rules intact.
  - The practice host gives the `TestnetBroker` equivalent for free.
- **IBKR fit:** `ib_async` is maintained and asyncio-native, so it slots in as an `IbkrBroker`. The cost is operational: IB Gateway must run alongside the bot.
- **NautilusTrader** is the best reference design for multi-venue FX (instrument specs, account-currency P&L, IB adapter). Adopting it would mean replacing, not extending, the engine, which goes against the plan's "build our own" decision.
- **Lean** has the most complete FX broker coverage, but it is a C# engine. Using it would mean abandoning most of the planned architecture.
- **Backtesting:** extend our own `backtest/` with financing cash flows and calendar-day accrual, as in `fx_backtest.py`. Use vectorbt only for exploratory sweeps.

### Gaps
- I did not verify OANDA's v20 streaming-endpoint details or rate limits from primary docs.
- I did not check whether NautilusTrader has a community OANDA adapter.

---

## 3. Real costs: spreads, commissions, rollover and news widening, slippage, financing markups, minimum sizes, margin

### Takeaway
On majors, **spread costs are small**: a standard account costs about 0.8–1.5 pips round trip on EURUSD, against 0.1–0.2 pip plus about $7 per 100k round turn on raw accounts (≈0.8–0.9 pip all-in). **Financing markups are what hurt a position-holding bot.** Brokers add roughly 0.3–2% a year to the interbank tom-next rate on each position. In our backtest this markup cost more than the spreads. Spreads widen at the 5pm New York rollover and around major data releases, so a daily bot should trade away from 17:00 ET.

### Cited Findings
**Standard-account spreads (IG spread bets, 12-week averages to 8 Jan 2021 — 5+ years old)**

| Pair | Minimum | Average 00:00–21:00 | Full-period average |
|---|---|---|---|
| EUR/USD | 0.6 | 0.85 | 1.04 |
| GBP/USD | 0.9 | 1.40 | 1.83 |
| USD/SEK | 25 | ~45 | ~51 |
| USD/NOK | 25 | ~46 | ~66 |
| NOK/SEK | 6 | — | 12.7–15.6 |

- IG says spreads widen "at illiquid times of day, or when major news or economic data is released" — [IG forex spread bet details](https://www.ig.com/uk/forex-bet-product-details); [IG IE CFD costs](https://www.ig.com/ie/markets/forex/forex-cfd-costs-and-details).
- The SEK/NOK column headers are ambiguous in the snippet.

**Raw + commission accounts**
- **IC Markets** MT4/MT5 Raw: average EUR/USD spread 0.1 pip plus **$3.50 per lot per side ($7 round turn)**. cTrader Raw charges **$3 per side per $100k USD traded** (IC's example gives about $3.90–3.93 per EURUSD lot) — [IC Markets accounts](https://www.icmarkets.com/trading-accounts/overview); [IC Markets EU trading costs](https://icmarkets.eu/de/trading-pricing/trading-costs).
- **Pepperstone** Razor: **$3.50 per side per 100k** for USD and AUD accounts (£2.25 for GBP, €2.60 for EUR), with measured EUR/USD averages of 0.1–0.19 pip. The Standard account has no commission and adds a ~1.0 pip markup on majors (third-party review, table dated 1 Jul 2026) — [CompareForexBrokers](https://www.compareforexbrokers.com/reviews/pepperstone-review/razor-vs-standard-account); [Pepperstone promo](https://pepperstone.com/en-ae/go/trade-forex-2024).
- **OANDA (US):** Standard from 1.1 pip EUR/USD with no commission. Core pricing is from 0.1 pip plus **$5 per side per 100k**, with a $10,000 minimum deposit (review site, unverified) — [CompareForexBrokers OANDA review](https://www.compareforexbrokers.com/reviews/oanda).
- Other OANDA EUR/USD figures conflict: 1.4–1.7 pips standard and 0.4–0.6 core in a 2026 blog — [NYC Servers](https://newyorkcityservers.com/blog/oanda-review); 0.9 pip per BrokerChooser — [BrokerChooser](https://brokerchooser.com/ko/broker-reviews/oanda-review/oanda-eurusd-spread).
- OANDA Australia's raw price sheet (Feb 2026) lists **$3.50 per 100k per side** on EUR/USD for USD accounts — [OANDA AU price sheet](https://www.oanda.com/assets/documents/2040/OANDA_Australia_Raw_spreads__Commissions_Price_Sheet_Feb26.pdf).
- **IBKR:** 0.20 bp of trade value, minimum $2 per order — see section 1.

**Rollover and news widening**
- 5pm New York is the start and end of the FX trading day, and positions open then are rolled. Spreads widen as banks refresh systems and roll value dates. Reports put the widening at "around 5 mins" (forum) or 30–60 minutes (broker blog); these accounts are anecdotal and inconsistent — [BlackBull](https://blackbull.com/en/education-hub/understanding-roll-over-and-widening-spreads-2); [BabyPips forum](https://forums.babypips.com/t/is-it-normal-or-not-for-spread-being-widen-like-that/46027).
- Wednesday's roll books three days of financing — [VT Markets](https://www.vtmarkets.com/discover/rollover-fees-explained-how-forex-swap-rates-rollover-rates-work/); [IG funding help](https://www.ig.com/uk/help-and-support/spread-betting-and-cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-).
- A vendor blog citing FCA research says liquidity providers widen quoted spreads by **more than 30%** and cut top-of-book depth by a similar share in the minute before releases such as Non-Farm Payrolls (unverified against the FCA) — [B2Broker](https://b2broker.com/news/how-nfp-affects-trading/).
- A broker-affiliated FXStreet piece says published "target spreads" cannot be relied on around NFP — [FXStreet](https://www.fxstreet.com/education/how-to-trade-nonfarm-payrolls-201508280000).

**Slippage**
- IBKR odd lots fill 1–2 bp (or 1–3 ticks) outside the IdealPro quote (section 1).
- I found no independent retail slippage statistics.

**Financing and swap markups**
- **IG:** tom-next plus an admin fee that varies by entity and contract size: 0.8% (mini) and 0.5% (standard) on the SG page; 0.3% (standard) and 0.8% (mini) on the global examples; **1.5%** in Australia; 1% in Switzerland; 0.5% on an older US page. The fee is charged as price × fee ÷ 360 — [IG funding help (SG)](https://ig.com/sg/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated); [IG AU](https://www.ig.com/au/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-).
- **Saxo:** a ±0.45–0.65% markup on tom/next by account tier, plus ±2.00% on overnight P/L financing — [Saxo FX financing](https://www.home.saxo/rates-and-conditions/forex/financing); [Saxo CH](https://www.home.saxo/en-ch/rates-and-conditions/forex/spreads-and-commissions).
- **OANDA:** FX financing is built from liquidity providers' tom-next rates "plus instrument-specific admin fees" (no FX figure found; index CFDs carry a 2.5–3% admin fee). Positions open at 5pm ET are financed, and weekend financing applies — [OANDA Canada financing](https://help.oanda.com/ca/en/faqs/financing-costs-ca.htm); [OANDA BVI](https://www.oanda.com/bvi-en/cfds/financing-costs).
- **IBKR:** debit interest is the benchmark plus 1.5% on the first tier (e.g. GBP 0–80k), falling at larger balances — [IBKR interest examples](https://www.interactivebrokers.com/en/accounts/fees/interestCharged-Examples.php).

**Margin and leverage caps (detail in section 4)**
- US: 2% deposit on majors and 5% on others (50:1 and 20:1).
- UK, EU and Australia: 30:1 on majors and 20:1 on minors.
- Sources: [Morgan Lewis (2010)](https://www.morganlewis.com/pubs/2010/09/cftc-issues-final-retail-forex-rules); [BrokerChooser UK limits](https://brokerchooser.com/safety/leverage-margin-limits-uk).
- IG lists a 3.33% retail margin on EUR/USD — [IG forex bet details](https://www.ig.com/uk/forex-bet-product-details).

**Minimum sizes**
- IBKR IdealPro: $25k (section 1).
- IG offers mini contracts — [IG funding help](https://ig.com/sg/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated).
- CME micros: €12,500, A$10,000, £6,250 (section 1).

### Inferences
- In bp of price: 1 pip on EURUSD at 1.12 ≈ 0.9 bp; on USDJPY at 158 ≈ 0.6 bp; 50 pips on USDSEK at 10.0 ≈ 5 bp (computed in our backtest output). Scandinavian pairs cost 4–6 times as much per trade as the majors.
- **Raw versus standard at retail size:**
  - Raw: $7 per round turn per 100k ≈ 0.7 pip on EURUSD, plus 0.1–0.2 pip spread, so about 0.8–0.9 pip all-in.
  - Standard: about 1.0–1.4 pip.
  - The difference is small for a daily system and does not change any conclusion in Part 2.
- **Financing markup scales with gross notional, not with trades.**
  - A 10%-vol FX portfolio carries roughly 1.5–3× NAV in gross notional (Part 2: average gross leverage 1.6–3.3).
  - So a 1% markup costs **about 1.6–3.3% of NAV a year**, more than the whole frictionless edge of any strategy tested.
  - This is the opposite of the BTC spot bot, where fees barely mattered.
- **Trade timing:** a daily bot should place orders well away from 17:00 ET and from scheduled releases, for example near the London/NY overlap or the noon-NY H.10 fixing time.

### Gaps
- No current (2025–2026) official spread tables could be loaded for OANDA, IG or Pepperstone. IG's averages date from 2020–2021.
- There are no published statistics on retail slippage.
- OANDA's FX admin-fee percentage is unknown.
- How IBKR credits interest on long currency balances (benchmark minus a spread, with a threshold) was not confirmed.

---

## 4. Regulation and taxes (US, UK, EU, Australia)

### Takeaway
- **US:** retail spot forex only through NFA-registered FCMs/RFEDs, at 50:1 on majors and 20:1 on others. No CFDs. FIFO applies and same-pair hedging is banned. Customer forex funds are **not segregated** in a dealer's bankruptcy.
- **UK:** the FCA made ESMA-style limits permanent from 1 Aug 2019: 30:1 on majors, 50% margin close-out and negative balance protection. The rules cover spread bets and rolling spot FX. Spread-bet gains are free of capital gains tax; CFD gains are taxed but losses are deductible.
- **EU:** ESMA's 2018 package (30:1, close-out, negative balance protection, risk warnings), since adopted nationally.
- **Australia:** ASIC's order since March 2021 (30:1, negative balance protection) runs to May 2027. A 10-year extension was proposed in Oct 2026.
- **US tax:** spot FX defaults to Section 988 (ordinary income or loss), with a contested opt-out to Section 1256 (60/40). Exchange FX futures fall under 1256.

### Cited Findings
**US**
- **CFTC final rule (effective 18 Oct 2010):**
  - Minimum security deposits are **2% of notional for major pairs and 5% for others**, i.e. 50:1 and 20:1.
  - The NFA sets the actual levels and designates which currencies are "major", reviewing at least annually.
  - Sources: [Morgan Lewis](https://www.morganlewis.com/pubs/2010/09/cftc-issues-final-retail-forex-rules); [Euromoney](https://www.euromoney.com/article/27bjsncxo5vak9tlbc179/foreign-exchange/fx-news-cftc-releases-final-rules-covering-retail-fx/).
- **NFA majors and changes since:**
  - The 2% majors were GBP, CHF, CAD, JPY, EUR, AUD, NZD, SEK, NOK and DKK.
  - After the Swiss franc shock, SEK and NOK deposits were raised to **3%**.
  - The NOK deposit went to **7%** from 22 Mar 2020 "until further notice".
  - Current levels are unconfirmed.
  - Sources: [FinanceFeeds](https://financefeeds.com/nfa-raises-required-minimum-security-deposits-certain-fx-transactions/); [NexusFi (2015)](https://nexusfi.com/currencies/34643-nfa-increase-required-minimum-security-deposit-forex-transactions-1-21-15-a.html).
- **NFA Compliance Rule 2-43:**
  - Bars dealers from letting a customer hold offsetting long and short positions in the same pair, and requires FIFO offsetting (effective from 2009).
  - The only FIFO exception is a customer-directed offset of a same-size position, which must still hit the oldest such position.
  - Steering US customers offshore to hedge violates Rule 2-36.
  - Sources: [Hedge Fund Law Blog](https://hedgefundlawblog.com/?p=2143); [OANDA US education](https://www.oanda.com/us-en/skills-and-insights/education/trading-asset-classes/forex/nfa-fifo-rule-challenges-expert-advisors/).
- **No CFDs for US residents** — [QuantConnect](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/cfd-and-forex-brokerages).
- The CFTC warned that off-exchange forex funds "may not be held in Section 4d segregated accounts", and that claiming special bankruptcy protection may violate the Act — [CFTC 2007 advisory](https://WWW.cftc.gov/idc/groups/public/@cpfraudawarenessandprotection/documents/file/forex_advretailcustomers2007.pdf).

**UK**
- **FCA PS19/18:**
  - Makes ESMA's temporary CFD restrictions permanent from **1 Aug 2019**.
  - Leverage is capped at 30:1 to 2:1 depending on the underlying's volatility.
  - Positions must be closed out at 50% of required margin, and clients cannot lose more than their account funds.
  - Inducements are banned, and firms must show a standardised warning with their own loss percentage.
  - References to CFDs **include financial spread bets and rolling spot forex**.
  - Sources: [FCA PS19/18](https://www.fca.org.uk/publications/policy-statements/ps19-18-restricting-contract-difference-products); [FCA press release](https://www.fca.org.uk/news/press-releases/fca-confirms-permanent-restrictions-sale-cfds-and-cfd-options-retail-consumers).
- Majors are capped at 30:1, minors and gold at 20:1 — [BrokerChooser](https://brokerchooser.com/safety/leverage-margin-limits-uk).
- **UK tax:**
  - Spread-betting profits are treated as gambling, so no capital gains tax and no self-assessment entry, but losses cannot offset other gains.
  - CFD profits are subject to capital gains tax: £3,000 allowance in 2025/26; **18% or 24%** after the Oct 2024 Budget. CFD losses can be offset.
  - If spread betting is your main income or a business, HMRC may challenge the tax-free status.
  - These are mostly broker sources, not HMRC — [IG UK tax](https://www.ig.com/uk/learn/trading/spread-betting-vs-cfds-tax); [CMC Markets](https://www.cmcmarkets.com/en-gb/spread-betting/spread-betting-tax-uk); [Trade Nation](https://tradenation.com/en-gb/articles/spread-betting-tax-in-uk/).

**EU**
- **ESMA's final product intervention measures (2018):**
  - Leverage limits from **30:1 (major FX)** down to 2:1.
  - Close-out at **50%** of minimum required margin, per account.
  - **Negative balance protection** per account.
  - Limits on incentives and a standardised risk warning.
  - The measures were temporary and renewable every three months under MiFIR.
  - Sources: [ESMA](https://www.esma.europa.eu/press-news/esma-news/esma-adopts-final-product-intervention-measures-cfds-and-binary-options).
- ESMA's March 2018 release found that **74–89% of retail CFD accounts lose money**, with average losses of €1,600–29,000 per client — [ESMA](https://www.esma.europa.eu/node/84933).

**Australia**
- **ASIC's CFD product intervention order:**
  - In force since **29 Mar 2021** and extended in 2022 to **23 May 2027**.
  - Leverage 30:1 to 2:1, standardised margin close-out, negative balance protection, and a ban on inducements.
  - In its first six months, aggregate net retail losses fell **91%**, from A$372m to A$33m a quarter, and loss-making accounts fell 51%.
  - Sources: [ASIC 22-082MR](https://asic.gov.au/about-asic/news-centre/find-a-media-release/2022-releases/22-082mr-asic-s-cfd-product-intervention-order-extended-for-five-years/); [Finance Magnates](https://www.financemagnates.com/forex/regulation/asic-extends-leverage-restrictions-on-cfds-for-another-five-years/).
- A law-firm summary says ASIC released consultation **CS 64 on 12 Oct 2026**, proposing to extend the order for a further 10 years (not verified on ASIC's site) — [Gilbert + Tobin](https://www.gtlaw.com.au/insights/key-topics/regulation-in-motion/asic-proposes-to-extend-and-strengthen-the-cfd-product-intervention-order).

**US tax**
- Spot forex falls under Section 988 by default: ordinary gain or loss, with losses fully deductible.
- Traders can reportedly elect out "internally" before trading, by a dated record kept with their books, to get 60/40 treatment under Section 1256. Sources disagree on whether spot forex qualifies (Section 1256(g) covers certain interbank forwards). These are practitioner and blog sources, not IRS guidance — [DayTradingToolkit](https://daytradingtoolkit.com/day-trading-basics/forex-trading-tax-section-988-vs-1256); [terms.law forum summary](https://terms.law/forum/thread/forex-trader-tax-treatment.html).
- Regulated futures (e.g. CME FX futures) are Section 1256 contracts with 60/40 treatment, reported on Form 6781 — [beancount.io guide (May 2026)](https://beancount.io/blog/2026/05/14/section-1256-contracts-60-40-tax-treatment-futures-broad-based-index-options-regulated-forex-form-6781-mark-to-market-traders-guide).

### Inferences
- **US FIFO and no-hedging rules** mean the bot must net positions per pair and close the oldest lots first. One position per instrument, as the current `Portfolio` design implies, already complies. A strategy that holds long EURUSD from one signal and short from another must net them.
- **Leverage caps do not bind for 10%-vol strategies.** Gross leverage of 1.5–3.3× is far below 20:1 or 30:1. But per-currency margin rates (e.g. NOK at 7% in the US) change how much margin is used, so the RiskManager should read margin rates from the broker rather than hard-coding them.
- **Tax shapes the product choice in the UK.** If the bot is expected to lose in some years, CFDs (deductible losses) beat spread bets; if it is expected to profit, spread bets are tax-free. That is a decision for the two developers and a tax adviser.

### Gaps
- Current NFA security-deposit levels for SEK and NOK were not confirmed.
- I did not verify the national ESMA measures (each country's permanent rules).
- No primary IRS text was found on spot-FX 1256 eligibility.
- ASIC's CS 64 consultation was not verified on ASIC's site.
- No Australian tax treatment was researched.

---

## 5. Retail outcomes: loss disclosures, US profitability data, academic studies

### Takeaway
Mandated disclosures in 2025–2026 show **about 62–82% of retail CFD/FX accounts losing money** at major brokers; the UK mean across 14 FCA brokers was 69.9% in April 2026. The last broad US data (2013–2014) showed **about 33–38% of active accounts profitable** in any quarter. Academic account-level studies find retail FX traders lose on average and do not get better with experience. Abbey & Doukas (2015) is the main dissenting study.

### Cited Findings
**Loss disclosures**
- **IG:** 78% of retail accounts lose money on CFDs, and 2.15% had positions closed by margin call over the last 12 months (snapshot date unclear; an older archived page said 64%) — [IG via search summary](https://www.ig.com/en-ch/profile/fabien-yip1).
- **CMC Markets:** 73% (BrokerChooser risk warning, May 2026) and 69% (BrokerChooser comparison, Oct 2026) — [BrokerChooser CMC](https://brokerchooser.com/broker-reviews/cmc-markets-review/cfd-risk-warning); [BrokerChooser IG vs CMC](https://brokerchooser.com/compare/ig-vs-cmc-markets).
- **Plus500:** 81% (BrokerChooser, Oct 2026); 76% in a TradingPlatforms.co.uk report. That report put IG and CMC at about 68% and Swissquote above 81% — [BrokerChooser](https://brokerchooser.com/compare/marketsx-vs-plus500); [Pound Sterling Live](https://www.poundsterlinglive.com/news/23132-even-at-major-uk-brokers-most-cfd-accounts-lost-money-report-finds).
- **Pepperstone:** 79.6% on its global (Bahamas-regulated) pages and 73% for its FCA entity (2026 pages) — [Pepperstone margin FX](https://pepperstone.com/en/markets/margin-fx); [Pepperstone UK sitemap](https://pepperstone.com/en-gb/sitemap).
- **OANDA:** 75% (BrokerChooser OANDA regulation page title) — [BrokerChooser](https://brokerchooser.com/pt/broker-reviews/oanda-review/oanda-regulation).
- **Markets.com:** 72.3% — [BrokerChooser](https://www.brokerchooser.com/broker-reviews/marketscom-review).
- **Other aggregates:**
  - UK mean across 14 FCA brokers, April 2026: **69.9%** — [The Investors Centre](https://www.theinvestorscentre.co.uk/trading/statistics/cfd-trading/).
  - LSE.co.uk's broker list ranges from 71% to 82.4% — [LSE.co.uk](https://lse.co.uk/brokers/).
- **Regulators:**
  - ESMA (2018): 74–89% of accounts lose, with average losses of €1,600–29,000 (section 4).
  - ASIC REP 579 (2017): **63% of margin-FX clients** and 72% of CFD clients lost money over 12 months; over 41,000 accounts went into negative balance (–A$33m), with leverage up to 500:1 — [ASIC REP 626](https://download.asic.gov.au/media/5241548/rep626-published-22-august-2019.pdf); [ASIC notice](https://download.asic.gov.au/media/5828628/public-notice-cfd-pip-22102020.pdf).
  - ASIC 2023–24: **68%** of retail CFD clients made a net loss, with aggregate net losses above A$458m — [Gilbert + Tobin summary](https://www.gtlaw.com.au/insights/key-topics/regulation-in-motion/asic-proposes-to-extend-and-strengthen-the-cfd-product-intervention-order).

**US profitability data (NFA quarterly figures compiled by Forex Magnates — old)**
- Q4 2014: **35.3%** of US forex traders profitable, against 37.8% in Q3 2014; US active retail accounts fell below 90,000 — [Finance Magnates](https://financemagnates.com/forex/brokers/exclusive-q4-2014-us-forex-profitability-report-accounts-fall-profits/amp).
- Q4 2013: **33.6%** profitable, with Interactive Brokers highest at 45.3% — [Finance Magnates](https://financemagnates.com/forex/brokers/exclusive-q4-us-retail-forex-profitability-report-ib-1-again-while-oanda-slipping).
- An earlier BabyPips snapshot (undated): FXCM and Forex.com 23%, GFT 33% — [BabyPips](https://www.babypips.com/news/hows_your_broker_doing).
- A secondary source cites 36.5% for Q1 2020 (unverified).

**Academic studies**
- **Hayley & Marsh (2016)**, *"What do retail FX traders learn?"*, JIMF 64:16–38:
  - Almost 100,000 traders over about 2.5 years.
  - No evidence that traders improve with experience. They learn about their ability (after losing days they trade less, smaller, or stop), and **even very experienced traders consistently lose money**.
  - Sources: [City Research Online](https://openaccess.city.ac.uk/15691); [Bayes summary](https://www.bayes.citystgeorges.ac.uk/faculties-and-research/research/bayes-knowledge/2017/november/what-do-retail-fx-traders-learn).
- **Heimer & Simon** (Cleveland Fed and Berkeley Research Group), data from a forex social network:
  - Individual forex traders **lose about 3% a week on average**, across more than 110,000 transactions.
  - Successful traders are about 50% more likely to talk about their trades, and those they tell trade about 20% more the next week.
  - Known only from Jason Zweig's column, not the paper — [Jason Zweig](https://jasonzweig.com/?p=2530).
- **Abbey & Doukas (2015, JIMF)** — the contrary result:
  - 428 accounts, 2004–2009.
  - Profits stay **positive after costs**; day traders beat non-day traders; performance rises with activity.
  - [Working copy](https://www.efmaefm.org/0doukas/publications/pdf/JIFM%20DoCurrencyTradersMakeMoney.pdf).
- **Nottingham Trent working paper**, *"The Retail FX Trader: Random Trading and the Negative Sum Game"*:
  - About **20%** of traders end with a profitable account, and about 40% face a margin call.
  - Profitability is strongly tied to spread costs, and there is little evidence of doing better than random trading.
  - [NTU IREP](https://irep.ntu.ac.uk/id/eprint/26837/).

### Inferences
- Disclosures count accounts, not traders or capital, and mix FX with index and crypto CFDs. Still, about 70% losers at large, regulated brokers is a stable base rate.
- The US figures (about 1/3 profitable per quarter) are on a different basis: per quarter, active accounts only, FX only.
- For a systematic daily bot the relevant lesson is cost drag plus leverage, not trader skill. In Part 2, the frictionless edge of the best rules (Sharpe ≈0.3–0.5) roughly halves after costs.

### Gaps
- No NFA or CFTC profitability data newer than 2014 was found from a primary or major source; the 2020 figure is unverified.
- The underlying Heimer & Simon paper was not retrieved.
- Broker loss percentages could not be verified on the brokers' own pages at a dated snapshot.
- There are no FX-only loss figures for UK or EU brokers.

---

## 6. Tail and operational risk: SNB 2015, GBP 2016, JPY 2019, yen carry unwind 2024, weekend gaps, broker insolvency and client money

### Takeaway
FX tail risk is real and comes from **jumps that skip stops**, not from daily volatility.
- **SNB, 15 Jan 2015:** the franc jumped about 30% intraday and bankrupted brokers.
- **GBP, 7 Oct 2016:** a ~9% flash crash in Asian hours.
- **JPY, 3 Jan 2019:** the yen rose ~3% in 30 seconds and AUDJPY fell 4–6%+.
- **Aug 2024:** USDJPY fell 11% from 161.7 to 144 at the noon fixings, in about four weeks.

Daily noon fixings miss the intraday extremes. In the US, a broker failure leaves forex customers as **unsecured creditors**. The UK (FSCS £85k) and EU (at least €20k) have compensation schemes and require client money to be segregated.

### Cited Findings
**SNB, 15 Jan 2015**
- The SNB dropped its EURCHF floor and the franc surged about 30% within minutes, settling about 15% higher.
- **FXCM:** clients ran up negative balances of about **$225m**, and FXCM needed a **$300m rescue from Leucadia**.
- **Alpari UK** became insolvent; client losses beyond account equity were passed to the firm.
- **IG's** losses were capped at under £30m.
- **Excel Markets** and **Global Brokers NZ** (New Zealand) failed (sources differ on which went first).
- Total industry losses were estimated at more than $1bn (Forex Magnates estimate).
- Sources: [Finance Magnates](https://www.financemagnates.com/forex/brokers/alpari-uk-first-major-casualty-chf-lcg-group-facing-2-5-mln-losses/); [Taipei Times (Reuters)](https://www.taipeitimes.com/News/biz/archives/2015/01/18/2003609482); [MQL5 blog](https://www.mql5.com/en/blogs/post/307632).
- In our H.10 data, USDCHF fell from 1.0172 to 0.8930 between the 14 and 15 Jan noon fixings (the CHF value of the dollar fell 12.2%; the CHF rose **+13.9%** in USD terms). The EURCHF cross went from 1.2009 to 1.0357 — [H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv).
- FXCM's 2015 losses later led to Jefferies taking ownership in 2023 (section 1).

**GBP flash crash, 7 Oct 2016**
- Sterling fell about **9% against the dollar in early Asian trading** and quickly retraced.
- The BIS found no single driver. Contributing factors were the time of day, options hedging, stop-loss execution, and algorithms used unsuitably in thin markets.
- Sources: [BIS Markets Committee](https://www.bis.org/publ/mktc09.htm); [BIS press release](https://www.bis.org/media-releases/20170113-report-sterling-flash-event-released-markets-committee).
- The H.10 noon rate that day was **1.2435**, against 1.2647 the day before, so the daily series shows only −1.7% — [H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv).

**Yen flash event, 3 Jan 2019**
- After Apple's guidance cut, with Japan on holiday and in the thinnest hour of the day, the yen rose about **3% against the dollar in about 30 seconds**, and bid-ask spreads widened — [RBA SMP Feb 2019, Box B](https://www.rba.gov.au/publications/smp/2019/feb/pdf/box-b-the-recent-japanese-yen-flash-event.pdf).
- AUDJPY fell by "over 4%" (XTB) or "over 6%" (DailyFX). Reported USDJPY lows range from 102.35 to 104.87, so the numbers conflict — [XTB](https://xtb.com/en/market-analysis/fx-markets-rocked-by-jpy-flash-rally); [DailyFX](https://www.dailyfx.com/forex/market_alert/2019/01/03/JPY-Soars-as-Flash-Crash-Moves-Spark-Flight-to-Havens-.html/amp).
- The H.10 noon USDJPY was **108.07**, against 109.22 the previous day: the flash low is invisible in daily data — [H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv).

**Carry unwind, Aug 2024**
- BIS Bulletin 90 (27 Aug 2024): TOPIX fell 12% on 5 Aug and the VIX spiked to Covid-era levels, amplified by deleveraging and higher margins — [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.pdf).
- A secondary summary says the BIS's "rough middle ballpark" for the carry unwind was **$250bn**, probably an underestimate — [The Full FX](https://thefullfx.com/what-does-250-billion-buy-a-carry-trade-blow-up/).
- H.10 USDJPY peaked at **161.73 on 10 Jul 2024** and was **143.95 on 5 Aug 2024**, down 11% — [H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv).
- Over 10 Jul–5 Aug 2024 our **G10 carry strategy lost 6.4% unscaled and 14.6% at a 10% vol target** (Part 2, tail-window table).

**Weekend gaps**
- From Jan 2001 to May 2020, EURUSD had 204 Sunday-open gaps and USDJPY 215, roughly one every five weeks — [Finance Magnates](https://financemagnates.com/thought-leadership/understanding-the-gaps-in-forex-trading).
- One vendor claims EURUSD gaps filled about 80% of the time over six months of 2024–25 (short sample) — [TradeThatSwing](https://tradethatswing.com/eurusd-monday-gap-fill-strategy-and-statistics/).
- In our H.10 data (2000–2026), noon-to-noon returns that span a weekend or holiday have about the same standard deviation as one-day returns: ratio 0.99 for EURUSD, 0.97 USDJPY, 1.04 GBPUSD, 1.00 AUDUSD. The largest such AUDUSD move was −8.2% (computed here from the [H.10 mirror](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv)).

**Client money and insolvency**
- **US:** off-exchange forex funds may not be held in segregated (Section 4d) accounts — [CFTC 2007 advisory](https://WWW.cftc.gov/idc/groups/public/@cpfraudawarenessandprotection/documents/file/forex_advretailcustomers2007.pdf). Commenters say PFG Best's bankruptcy left retail forex customers without segregation protection (advocacy comments) — [CFTC comment](https://comments.cftc.gov/PublicComments/ViewComment.aspx?id=59068).
- **UK:** the FSCS covers up to **£85,000** per person per firm when an authorised firm fails.
- **EU:** schemes must cover at least **€20,000**. Cyprus's ICF pays the lesser of €20k or 90% of the loss.
- MiFID II requires client assets to be segregated.
- Sources: [TopBrokers](https://topbrokers.com/all-about-forex-brokers/forex-broker-compensation-schemes-fscs-icf-explained/); [QuantRoutine](https://quantroutine.com/learn/investor-protection-europe/).
- Alpari UK stated that retail client funds remained segregated under FCA rules — [Finance Magnates](https://www.financemagnates.com/forex/brokers/alpari-uk-first-major-casualty-chf-lcg-group-facing-2-5-mln-losses/).
- Negative balance protection is mandatory for retail clients in the UK, EU and Australia (section 4).

### Inferences
- **Data hides tails:**
  - A backtest on daily fixings, ours included, cannot model stop-outs, margin close-outs at 50% (UK, EU, AU), or slippage through gaps.
  - Strategies short CHF or JPY (carry) or long high-yielders carry jump risk that daily data shows only as one large daily return.
  - The bot's risk limits need explicit stress tests: e.g. a 15% move against each currency leg, and the 2015 CHF and 2024 JPY paths.
- **Vol targeting amplifies carry crashes.** Carry looks calm before it crashes, so a 10% vol target levers it up (average gross 3.3× in 2022–26) just before the unwind. That is why the VT10 carry loss in Jul–Aug 2024 (−14.6%) was more than double the unscaled loss.
- **Operational rules for the RiskManager:**
  - Flatten or reduce before weekends and known event risk (central-bank meetings), if the strategy allows.
  - Use guaranteed stops where offered (IG) for disaster protection.
  - Keep only the margin needed at the broker.
- **Counterparty:** for a US account, broker failure means unsecured-creditor status. That favours a large, well-capitalised FCM, or CME futures with segregated customer funds.

### Gaps
- No primary account of Alpari UK's administration outcome (client recoveries) was retrieved.
- FXCM's final settlement of the 2015 negative balances was not confirmed.
- There are no robust statistics on the distribution of weekend-gap sizes.
- Whether CME futures customer segregation applies to micro FX futures was not checked (inferred).

---

## 7. Data: free historical FX sources and quality pitfalls

### Takeaway
- **Free bid/ask history:** Dukascopy tick data (via community downloaders) and OANDA's candles API (with a free practice account).
- **Free 1-minute bid bars:** HistData, stamped in fixed EST with no DST shift.
- **Free daily fixings:** FRED H.10 (noon New York buying rates, single mid-type fixing) and ECB reference rates (~14:10 CET, "not for transactions").
- TrueFX historical tick data was free in 2009; its current status is unknown.

Key pitfalls: mid versus bid/ask, the daily cut-off (17:00 NY vs noon NY vs 14:10 CET vs UTC midnight), DST shifts, Sunday stub bars, and holiday blanks.

### Cited Findings
- **H.10:** the New York Fed certifies **noon buying rates in New York for cable transfers** for customs purposes, quoted mostly as foreign currency per USD; the release is weekly — [Federal Reserve H.10 archive](https://www.federalreserve.gov/releases/h10/20030224/h10.htm).
- **Our H.10 mirror (datasets/exchange-rates):**
  - Built from FRED series (e.g. DEXUSEU, DEXJPUS).
  - The build script **inverts AUD, EUR, IEP, NZD and GBP**, so every value in `daily.csv` is foreign units per USD, despite the README saying those are USD per currency.
  - Coverage runs from 1971 (EUR from 1999-01-04) to **2026-10-09**.
  - US holidays appear as blank rows, and values carry 4–5 significant digits.
  - Sources: [build script](https://raw.githubusercontent.com/datasets/exchange-rates/main/exchange_rates_flow.py); [data](https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv); [datapackage.json](https://raw.githubusercontent.com/datasets/exchange-rates/main/datapackage.json).
- **ECB reference rates:** set by a concertation between central banks around 14:10 CET and published around 16:00 CET; "for information purposes only… use for transaction purposes is strongly discouraged". RUB publication was suspended after 1 Mar 2022 — [ECB](https://www.ecb.europa.eu/stats/eurofxref).
- **OANDA candles:** the `price` parameter takes any combination of M (mid), B (bid) and A (ask). Daily candles align by default at **17:00 America/New_York**, and weekly candles on Friday (per the async-v20 wrapper docs, not OANDA's own) — [async-v20 docs](https://async-v20.readthedocs.io/en/latest/api.html); [oandapyV20 definitions](https://oanda-api-v20.readthedocs.io/en/master/oandapyV20.definitions.instruments.html).
- **HistData:**
  - 1-minute OHLC bars of **bid** quotes, timestamped in **EST without daylight-saving adjustment**.
  - No header row; volume not published; tick timestamps not unique (documented by third-party wrappers).
  - Sources: [PyPI histdata](https://pypi.org/project/histdata); [FX-1-Minute-Data](https://github.com/philipperemy/FX-1-Minute-Data).
- **Dukascopy:**
  - Free historical tick and bar data via `dukascopy-node` (CLI/Node), an Elixir package (1,600+ instruments; price type bid, ask or mid, default bid), and the Python `tickterial` (bid and ask; current hour not available) and `TickVault`.
  - Terms of use were not confirmed.
  - Sources: [dukascopy-node](https://gittrend.io/repo/Leo4815162342/dukascopy-node); [theorycraft dukascopy](https://github.com/theorycraft-trading/dukascopy); [tickterial](https://pypi.org/project/tickterial/1.1.0/).
- **TrueFX (Integral):** launched in 2009 with free tick-by-tick historical and real-time data. In 2019, streaming tiers included a free set of 25 pairs for individuals. Current access terms are unknown — [Finance Magnates 2009](https://www.financemagnates.com/forex/brokers/integral-introduces-truefx-free-real-time-interbank-rates-for-all/); [TFX R docs](https://rdrr.io/cran/TFX).
- **Interest-rate data found on GitHub raw** (FRED/OECD mirrors, used in Part 2):
  - Monthly 3-month interbank rates `IR3TIB01xxM156N` for US, EZ, JP, GB, CH, AU, NZ, CA, SE and NO, plus the Japan call rate, ECB deposit rate and SONIA — [ethanl814/CIB](https://github.com/ethanl814/CIB/tree/main/forex-drift-idea/data/raw/fred).
  - Cross-checked against a second mirror; the maximum absolute difference was ≤0.005 pp on overlapping months — [itsTashfeen/FinEng](https://github.com/itsTashfeen/FinEng/tree/main/G10%20FX%20Carry%20Strat/data/raw/interest_rates).
- **Blocked from this container:** FRED, ECB, BIS, OECD, stooq, Yahoo, Dukascopy and HistData — task brief; confirmed for FRED in the proxy log ("403 to CONNECT … fred.stlouisfed.org").

### Inferences
**Pitfalls the bot's data layer must handle**
1. **Mid versus executable prices.**
   - H.10, ECB and OANDA "M" candles are mids.
   - A backtest on mids must add half the spread per side.
   - A bot that signals on bid candles but buys at the ask needs consistent handling of both.
2. **Daily close convention.**
   - Use 17:00 New York (with DST, so 21:00 or 22:00 UTC) for broker candles.
   - H.10 is 12:00 NY, ECB about 13:10/12:10 UTC, and many crypto feeds 00:00 UTC.
   - Mixing them shifts signals by hours and creates false lead-lag effects.
3. **DST.**
   - HistData's fixed EST and Dukascopy's UTC differ from the NY-17:00 cut by an hour for part of the year.
   - Resample from UTC ticks using `America/New_York` 17:00 boundaries.
4. **Sunday bars.**
   - With a 17:00 NY daily cut, the market's Sunday-evening open falls into Monday's bar.
   - With a UTC-midnight cut there is a tiny Sunday bar, which distorts daily-return statistics and day counts.
5. **Holidays and blanks.**
   - H.10 has blanks on US holidays (dropped in our script).
   - Brokers still trade some of those days.
6. **H.10 is a single fixing, not a bar.**
   - It has no high or low, so stops, intrabar Donchian triggers and flash events cannot be simulated (section 6).
7. **Rates data.**
   - OECD 3-month interbank series are monthly averages, published with a lag.
   - Several series ended or changed after LIBOR's retirement: the EZ and GB series in our mirror stop in Jan 2026.
   - Retail financing actually follows overnight tom-next rates.

### Gaps
- Dukascopy and HistData could not be downloaded here, so bid/ask spreads could not be measured from history.
- OANDA candle limits (e.g. maximum candles per request) were not confirmed.
- The current status of TrueFX is unknown.
- Dukascopy's terms of use were not checked.

---

## 8. Architecture differences from the BTC bot, and what to reuse

### Takeaway
**Most of the planned engine is reusable**: the Strategy protocol, event bus, Control, Telegram and dashboard, storage, and the backtest harness. The parts that must change are:
- the **exchange/Broker layer**, since CCXT has no FX brokers;
- **instrument metadata** (pips, units, margin rates);
- the **portfolio and P&L in the account currency**;
- **financing cash flows**;
- a **market-hours calendar** (Sunday 17:00 to Friday 17:00 NY, rollover at 17:00);
- **margin-aware risk**.

The strategies that showed any edge in Part 2 are multi-pair, which collides with the repo's "Bitcoin only / single `TRADING_PAIR`" decision.

### Cited Findings
- **Today's plan:**
  - Engine flow: MarketData → Strategy → RiskManager → OrderManager → Broker.
  - `exchange/` is a CCXT wrapper.
  - `PaperBroker` simulates fills from live prices.
  - Storage holds candles, orders, fills, positions and equity snapshots.
  - `TRADING_PAIR` is a single config value.
  - Source: local file `docs/PLAN.md` §2 and §7.
- The repo's decisions log says "Bitcoin only… Don't build multi-coin features… without both developers agreeing", and names CoinMarketCap as the one market-data aggregator — local file `CLAUDE.md`.
- **Rollover mechanics:**
  - The FX day starts and ends at 5pm New York.
  - Positions held through it are financed, and Wednesday books three days — [BlackBull](https://blackbull.com/en/education-hub/understanding-roll-over-and-widening-spreads-2); [IG](https://www.ig.com/uk/help-and-support/spread-betting-and-cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated-).
  - OANDA charges financing on positions open at 5pm ET, applies weekend financing, and credits or debits the account daily — [OANDA Canada financing](https://help.oanda.com/ca/en/faqs/financing-costs-ca.htm).
- **Units and costs:**
  - Brokers quote commissions per 100k units ("standard lot") and offer mini contracts; IG's funding fees differ for mini and standard — [IC Markets](https://www.icmarkets.com/trading-accounts/overview); [IG SG](https://ig.com/sg/help-and-support/cfds/fees-and-charges/why-is-overnight-funding-charged-and-how-is-it-calculated).
  - IBKR converts commissions into the account's base currency — [IBKR commissions](https://interactivebrokers.ie/en/pricing/commissions-spot-currencies.php).
- **US accounts:** FIFO and no-hedging (section 4).
- **Retail accounts in the UK, EU and AU:** 50% margin close-out (section 4).

### Inferences
**Market hours and calendar**
- Trading runs from about **Sunday 17:00 to Friday 17:00 America/New_York**. Daily bars should close at 17:00 NY.
- Avoid placing orders in the roughly 16:55–17:15 rollover window.
- Treat weekends as a gap risk. Positions earn or pay three days of financing on Wednesday, plus weekend days.
- The current daily BTC candle (00:00 UTC, 24/7) logic needs a trading-calendar abstraction.

**Pips, lots and units**
- 1 pip = 0.0001, or 0.01 for JPY pairs.
- 1 standard lot = 100,000 base units, a mini lot 10,000, a micro lot 1,000.
- Store size as integer **units of base currency** (OANDA style) and derive lots for display.
- Price precision per instrument comes from the broker's instrument endpoint. It replaces CCXT's `precision` and `limits`.

**Position sizing in the account currency**
- For pair B/Q (e.g. EUR/USD) and account currency A:
  - notional in A = units × price(B/A);
  - a 1-pip P&L = units × pip × price(Q/A).
- Example: a USD account long 10,000 USDJPY gains 10,000 × 0.01 = ¥100 per pip ≈ $0.63 at 158.
- Vol-targeted sizing: units_i = (target_vol × NAV_A / N) ÷ (σ_i × price(B_i/A)).
- So the engine needs live conversion rates for every quote and base currency into the account currency, and must treat them as `Decimal`.

**P&L and financing**
- Realised P&L arrives in the quote currency and is converted (or auto-converted by the broker) into A.
- Financing is a separate daily cash flow per position, which can be positive or negative.
- New storage tables: financing ledger and currency conversions. `portfolio/` needs balances per currency (IBKR keeps multi-currency cash), not one USDT balance.

**Margin**
- The RiskManager must track **margin used versus available**, check each order against per-instrument margin rates, and keep a buffer well above the 50% close-out level.
- Its limits should include **gross notional per currency** (aggregated across pairs, e.g. long EURUSD plus long EURJPY = double EUR exposure) and an event or weekend exposure cap.
- The existing `max position size` and `daily loss` checks remain, but in account-currency terms.

**Reuse as is**
- Strategy protocol, Control, EventBus, Telegram, FastAPI and dashboard, structlog, Sentry, healthchecks, and the `TRADING_MODE` paper/testnet/live gating (testnet maps to the OANDA practice, IB paper or Saxo sim account).

**Changes**
- `exchange/`: replace with `brokers/oanda.py` or `brokers/ibkr.py`, since CCXT cannot be used.
- `marketdata/`: OANDA streaming prices and candles instead of `watch_*`.
- `PaperBroker`: must simulate bid/ask, financing and margin close-outs.
- `backtest/`: add financing accrual and a calendar-day convention (as in `fx_backtest.py`).
- `config`: a list of instruments instead of a single `TRADING_PAIR`.
- **Market data:** the CoinMarketCap-only rule does not cover FX. The broker's own candles would become the FX data source, which needs a decision-log entry.

**Scope conflict**
- Part 2's only rules with any (weak) edge are 9-pair portfolios. A single-pair EURUSD bot would rely on rules like (e1) and (e2), which lost money.
- Going to FX therefore probably means agreeing to multi-instrument support. Under `CLAUDE.md`, both developers must sign off on that change.

### Gaps
- I did not verify OANDA's exact weekly open and close times or holiday schedule from primary docs.
- I did not check how OANDA reports financing in its transaction stream (field names).

---

## 9. Part 2: own sanity-check backtest of the main FX strategy candidates on free daily data (G10 vs USD, 2000 – Oct 2026)

### Takeaway
After realistic retail costs, **no candidate earned a meaningful return over 2000-01-03 to 2026-10-09**. Costs here mean half the spread plus slippage per side, and a **1%/yr financing markup on every USD-pair leg**.

| Strategy | Sharpe | CAGR | t-stat | Bootstrap p |
|---|---|---|---|---|
| (f) 50/50 trend + carry | **0.20** | 1.5% | 1.0 | ≈0.15 |
| (d) G10 carry | 0.13–0.14 | 0.8% | — | ≈0.23–0.26 |
| (a) TSMOM ensemble | 0.04 | — | — | ≈0.44 |
| (b) Donchian ensemble | 0.04 | — | — | ≈0.44 |
| (c) Cross-sectional momentum | −0.33 to −0.40 | — | — | — |
| (e) EURUSD mean reversion | −0.22 to −0.42 | — | — | — |
| Long-USD basket | −0.10 to −0.18 | — | — | — |

The edge is regime-dependent:
- Before 2008, carry (Sharpe ~1.0), trend (0.5–0.7) and the combo (1.1) all worked.
- In 2008–2014 trend was weakly positive (0.24–0.27) and carry lost (−0.27 to −0.51).
- In **2015–2021 and 2022–2026 every strategy was flat or negative** except carry (about 0) and the long-USD benchmark.

The largest single cost is the **financing markup**, not the spread. Removing the markup raises Sharpe by 0.15–0.25; halving or doubling spread costs moves it by only about ±0.05–0.1. One extra day of execution lag changes little for trend and carry.

### Cited Findings

#### Data (files in `data/`, SHA-256 recorded)
| Local file | Source URL | Content | SHA-256 |
|---|---|---|---|
| `data/fx_daily.csv` | https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv | FRED H.10 daily noon NY buying rates; all values foreign units per USD; to 2026-10-09 | `68349ef41ecc0cf35fa00ba0d9d63ec93b45a5182c37d2bb9a368fcd654bfeaa` |
| `data/rates/IR3TIB01USM156N.csv` | https://raw.githubusercontent.com/ethanl814/CIB/main/forex-drift-idea/data/raw/fred/IR3TIB01USM156N.csv | US 3m interbank, monthly avg, to 2026-08 | `3d2f2d7785d97ab9effc8e56a0c0687a4e096e38d8979b08f86cfbc9c27c71ee` |
| `data/rates/IR3TIB01EZM156N.csv` | …/fred/IR3TIB01EZM156N.csv (same repo path) | Euro area 3m, to 2026-01 | `bda18d6a61bc490560965e6acd9fc21e213f026ca68ac4670d3c9ec835043ce5` |
| `data/rates/IR3TIB01JPM156N.csv` | …/fred/IR3TIB01JPM156N.csv | Japan 3m, 2002-04 to 2026-07 | `cf59cf5ebc469237a03721a27fe08d261fb770d06df49fc1c269848634d92fea` |
| `data/rates/IR3TIB01GBM156N.csv` | …/fred/IR3TIB01GBM156N.csv | UK 3m, to 2026-01 | `40c23cc654a1380ed278a2b0be691f368d5cc1648493cadbbf1a2a2f654d33d4` |
| `data/rates/IR3TIB01CHM156N.csv` | …/fred/IR3TIB01CHM156N.csv | Switzerland 3m, 1999-07 to 2026-08 | `aec78fa05b526a3e5e057a910d0fb970a8655d7815098bfb92b055e22bc1dde8` |
| `data/rates/IR3TIB01AUM156N.csv` | …/fred/IR3TIB01AUM156N.csv | Australia 3m, to 2026-08 | `cc5a480e77a97ad2a10e93bab4631f577a43ef896853069beb2538b9539ae13f` |
| `data/rates/IR3TIB01NZM156N.csv` | …/fred/IR3TIB01NZM156N.csv | New Zealand 3m, to 2026-08 | `e763584a4cb24ed1acb4db41018bc59426b38bdc63bc67e2fff29f1ff1404f4f` |
| `data/rates/IR3TIB01CAM156N.csv` | …/fred/IR3TIB01CAM156N.csv | Canada 3m, to 2026-08 | `5d352ee34617e03ee74f28069c05cd3e7289a2f4d5c3d290f55ccf22924d7a1c` |
| `data/rates/IR3TIB01SEM156N.csv` | …/fred/IR3TIB01SEM156N.csv | Sweden 3m, to 2026-08 | `3540ddb279d0d8406dd97210c567130f2b5481849cc9d3a45efd75d69e7fb918` |
| `data/rates/IR3TIB01NOM156N.csv` | …/fred/IR3TIB01NOM156N.csv | Norway 3m, to 2026-08 | `27c9fe3bf7dd7c984d0d811b0c6a2958caf5a45a0e9aef2fbd7b2105ee25d9f1` |
| `data/rates/IRSTCI01JPM156N.csv` | …/fred/IRSTCI01JPM156N.csv | Japan call rate (fills JPY before 2002-04) | `41c22221dfb4d903227b2d9f54472765c29bedfd5bd0f075f9db71eebac66cd3` |
| `data/rates/ECBDFR.csv` | …/fred/ECBDFR.csv | ECB deposit rate, daily, to 2026-09-28 (extends EUR after 2026-01) | `df4ec4982213e556e883818da9fda01d9a98e7da0958e64af5fe1912660f6ac9` |
| `data/rates/IUDSOIA.csv` | …/fred/IUDSOIA.csv | SONIA, daily, to 2026-09-24 (extends GBP after 2026-01) | `5a9968eaa26720a681f010e0629f4aece4ef3aaf127e67d4c37f82e2a857d355` |

**Cross-check copies (not used by the script)**
- Saved in `data/rates_mirror2/`, from https://raw.githubusercontent.com/itsTashfeen/FinEng/main/G10%20FX%20Carry%20Strat/data/raw/interest_rates/<series>.csv.
- They cover the same nine foreign 3m series to 2026-01, plus DTB3 (US 3m T-bill).
- On overlapping months they match the primary files to within 0.005 pp.
- The US 3m interbank rate averaged 0.30 pp above the DTB3 T-bill rate.
- SHA-256 values:
  - DTB3 `8ed635fe…c0f3`, AU `94ca761a…2ca8`, CA `3bdfbd33…6d2`, CH `c9672737…e16`, EZ `f1451db4…89e5`
  - GB `7ae88802…eef`, JP `b7cfb6b3…eea`, NO `52b830cb…106`, NZ `f3c3a960…c09f4`, SE `da44198c…5ec`
  - Full hashes: `sha256sum data/rates_mirror2/*`.

**Rates found**
- Monthly 3-month interbank (OECD MEI via FRED) exists for all G10 countries on GitHub raw, so carry *could* be tested.
- Splices:
  - JPY before 2002-04 uses the call rate.
  - EUR and GBP after 2026-01 use the ECB deposit rate and SONIA monthly means, plus the spread at the last overlapping month (+0.028 pp and −0.015 pp).
  - Every series is forward-filled after its last observation (Aug or Sep 2026).

#### Method
**Script and run**
- `fx_backtest.py` in this folder (research scratch code, not bot code).
- Run as `uv run --no-project --with pandas --with numpy python -I fx_backtest.py data/fx_daily.csv data/rates`; it takes about 20 seconds.

**Universe and returns**
- The nine G10 currencies against USD.
- Each day's return is the change in the USD value of one unit of the foreign currency.
- Full test period 2000-01-03 to 2026-10-09: 6,965 fixings from 1999, about 250.7 a year. The first year is warm-up.

**Execution**
- Weights are decided on day t's H.10 fixing (noon NY) and earn t to t+1.
- A variant with one extra day of lag is also reported.

**Costs**
- Round-trip pips, spread plus slippage, set before the first run from the section 3 findings (IG averages):

  | Pair | Round-trip pips |
  |---|---|
  | EURUSD | 1.0 |
  | USDJPY | 1.2 |
  | AUDUSD | 1.3 |
  | GBPUSD | 1.8 |
  | USDCHF | 1.8 |
  | USDCAD | 1.8 |
  | NZDUSD | 2.0 |
  | USDSEK | 50 |
  | USDNOK | 50 |

- Half is charged per side and converted to a fraction of the quoted price on the trade date. At current prices that is 0.8–5.2 bp round trip.
- Sensitivity runs at ×0.5 and ×2.

**Financing**
- Each position earns w × (r_foreign − r_USD) × calendar days ÷ 365, using the monthly-average 3m rate of the holding month.
- It also pays **1%/yr × |w| on every leg** as the broker's markup.
- Sensitivity runs: markup 0 and 2%, "spot only" (no carry, no markup, no spread), and "frictionless" (spot plus carry, no costs at all; comparable to academic gross figures).
- Margin cash earns 0, so all returns are excess returns.

**Sizing**
- Per-pair risk weight = 10% ÷ σ_i, where σ_i is the EWMA standard deviation (centre of mass 60 days) of daily log returns.
- Multi-pair books are then scaled to a **10% ex-ante portfolio vol**, using the same EWMA on the book's own unscaled returns, capped at 4×.
- Monthly strategies update weights and scale only at month-ends.
- No rebalance band is applied.

**Strategies** (parameters fixed in advance from the literature, not optimised)

| Label | Rule | Rebalance | Sizing |
|---|---|---|---|
| (a) TSMOM ensemble | Average of sign(1/3/6/12-month return), i.e. 21/63/126/252 days, long-short per pair | Daily | Per-pair 10%, then portfolio VT10 |
| (b) Donchian ensemble 20/55/100/200 | Long on a new N-day closing high, short on a new N-day low; exit a long on an N/2-day low and a short on an N/2-day high | Daily | Per-pair 10%, then portfolio VT10 |
| (c) Cross-sectional momentum | Rank 10 currencies (USD = 0) by 3-month or 12-month spot return; +1/3 on each of the top 3, −1/3 on each of the bottom 3 (a USD leg means no position) | Monthly | Portfolio VT10 |
| (d) G10 carry | Same top/bottom construction ranked on the previous month's 3m rate (lagged one month) | Monthly | Unscaled, and portfolio VT10 |
| (e1) EURUSD 5-day reversal | −sign(5-day return) | Daily | Per-pair 10% |
| (e2) EURUSD RSI(2) fade | Long below 10 until above 50; short above 90 until below 50 | Daily | Per-pair 10% |
| (f) Combo | 50/50 of (a) and (d)-VT10 | Daily | Rescaled to VT10 |
| Benchmarks | Long-USD basket (−1/9 in each currency), unscaled and VT10; zero (cash) | — | — |

**Statistics**
- Sharpe = mean ÷ std × √250.7 of daily net returns.
- t ≈ Sharpe × √years.
- Block bootstrap: circular, 21-day and 63-day blocks, 2,000 resamples. It reports the share of resamples with Sharpe ≤ 0, a rough one-sided p-value against zero that is **not adjusted for multiple testing**.
- Turnover: Σ|Δw| ÷ 2 per year, in multiples of NAV ("RT/yr").
- Cost-drag columns: "Sprd" (spread and slippage %/yr), "Carry" (rate differential earned %/yr), "Mkup" (markup paid %/yr). "Lev" is the average gross notional ÷ NAV.

**Variants tried:** 9 strategy variants plus 2 benchmarks, each with 7 sensitivity runs. The script was run five times:
- Run 1 had a bug in one diagnostic print (the carry differential was averaged over all days instead of month-ends).
- Run 2 fixed it and added the "frictionless" column and a sign-change diagnostic.
- Runs 3–5 came after lint and formatting edits only, and printed byte-identical output.

No strategy, cost or sizing parameter changed between runs; the cost table was set before run 1.

#### Key results (all net of baseline costs; full output below)

**Full period, 2000-01-03 to 2026-10-09**

| Strategy | Sharpe | CAGR | Vol | MaxDD | Avg gross lev | RT/yr | Spread drag | Carry earned | Markup paid | Frictionless Sharpe | Boot p (21d) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (a) TSMOM ens, VT10 | 0.04 | −0.1% | 10.1% | −47.4% | 1.6 | 39.0 | 0.96% | +0.55% | 1.60% | 0.29 | 0.44 |
| (b) Donchian ens, VT10 | 0.04 | −0.1% | 10.2% | −55.8% | 1.6 | 16.4 | 0.40% | +0.51% | 1.58% | 0.23 | 0.44 |
| (c) XS mom 3m, VT10 | −0.40 | −4.7% | 10.6% | −75.1% | 2.5 | 13.3 | 0.36% | +0.50% | 2.47% | −0.14 | 0.99 |
| (c) XS mom 12m, VT10 | −0.33 | −4.1% | 10.7% | −71.7% | 2.5 | 8.3 | 0.22% | +0.78% | 2.53% | −0.08 | 0.97 |
| (d) Carry, unscaled | 0.14 | 0.8% | 8.0% | −39.6% | 1.8 | 0.6 | 0.02% | +3.28% | 1.77% | 0.36 | 0.23 |
| (d) Carry, VT10 | 0.13 | 0.8% | 10.5% | −61.3% | 2.7 | 2.1 | 0.06% | +4.99% | 2.73% | 0.39 | 0.26 |
| (e1) EURUSD 5d reversal | −0.22 | −2.6% | 10.0% | −52.9% | 1.2 | 62.8 | 0.54% | −0.05% | 1.24% | −0.04 | 0.86 |
| (e2) EURUSD RSI(2) fade | −0.42 | −2.9% | 6.5% | −57.8% | 0.5 | 34.1 | 0.29% | −0.05% | 0.54% | −0.29 | 0.99 |
| (f) 50/50 (a)+(d), VT10 | **0.20** | 1.5% | 10.2% | −46.8% | 2.5 | 32.6 | 0.81% | +3.91% | 2.55% | **0.52** | **0.15** |
| Long USD basket, unscaled | −0.18 | −1.8% | 8.0% | −57.7% | 1.0 | 0.0 | 0.00% | +0.06% | 1.00% | −0.06 | 0.83 |
| Long USD basket, VT10 | −0.10 | −1.6% | 10.2% | −69.1% | 1.4 | 1.5 | 0.04% | +0.23% | 1.42% | 0.04 | 0.70 |
| Zero (cash) | 0 | 0 | 0 | 0 | — | — | — | — | — | — | — |

**Sharpe by sub-period (net)**

| Strategy | 2000–07 | 2008–14 | 2015–21 | 2022–Oct 2026 |
|---|---|---|---|---|
| (a) TSMOM | 0.51 | 0.24 | −0.23 | −0.66 |
| (b) Donchian | 0.68 | 0.27 | −0.49 | −0.63 |
| (c) XS mom 3m / 12m | −0.22 / −0.17 | 0.00 / −0.21 | −0.93 / −0.57 | −0.48 / −0.46 |
| (d) Carry unscaled / VT10 | 0.96 / 1.05 | −0.27 / −0.51 | −0.13 / −0.25 | 0.04 / 0.06 |
| (e1) 5d reversal / (e2) RSI(2) | −0.13 / −0.63 | −0.42 / −0.55 | −0.03 / −0.40 | −0.33 / 0.08 |
| (f) Combo | **1.10** | −0.12 | −0.21 | −0.28 |
| Long USD unscaled / VT10 | −0.69 / −0.77 | −0.13 / 0.13 | 0.05 / 0.15 | 0.22 / 0.30 |

**Calendar-year net returns**

| Strategy | 2008 | 2015 | 2022 | 2024 | 2025 | 2026 YTD |
|---|---|---|---|---|---|---|
| (a) TSMOM | +14.8% | 0.0% | +8.6% | −18.5% | −10.6% | −5.2% |
| (b) Donchian | +19.3% | −3.2% | +10.0% | −13.9% | −10.9% | −3.0% |
| (c) XS 3m | +14.0% | −10.1% | −4.9% | −13.2% | +12.5% | −6.7% |
| (c) XS 12m | +5.1% | −1.4% | −0.3% | −13.5% | −4.4% | −5.4% |
| (d) Carry unscaled | −24.8% | −7.1% | −5.4% | +4.7% | −3.2% | +6.7% |
| (d) Carry VT10 | −21.2% | −10.9% | −8.7% | +9.2% | −6.8% | +14.7% |
| (e1) 5d reversal | −12.8% | −4.4% | −5.7% | −2.9% | −7.6% | −5.4% |
| (e2) RSI(2) | −6.4% | −8.5% | −2.0% | −4.8% | +5.4% | −3.7% |
| (f) Combo | −7.5% | −8.2% | +0.6% | −5.7% | −11.1% | +6.9% |
| Long USD unscaled | +9.2% | +6.8% | +7.4% | +9.2% | −8.5% | +1.7% |

**Robustness (full-period Sharpe)**

| Strategy | Base | +1 day lag | Spread ×0.5 | Spread ×2 | Markup 0 | Markup 2% | Spot only |
|---|---|---|---|---|---|---|---|
| (a) TSMOM | 0.04 | 0.00 | 0.09 | −0.06 | 0.20 | −0.12 | 0.24 |
| (d) Carry, unscaled | 0.14 | 0.12 | 0.14 | 0.13 | 0.36 | −0.08 | −0.05 |
| (f) Combo | 0.20 | 0.15 | 0.24 | 0.12 | 0.44 | −0.05 | 0.14 |
| (e2) RSI(2) | −0.42 | −0.13 | −0.40 | −0.47 | −0.34 | −0.50 | −0.29 |

- Carry's "spot only" Sharpe of −0.05 shows that the spot moves of high-yielders lost money on average; the whole carry return is the rate differential.
- The extra day of lag *improves* (e2), meaning the fade loses most on the first day.

**Tail windows (cumulative net return)**

| Strategy | Sep–Dec 2008 | SNB day 15 Jan 2015 | SNB week 12–16 Jan 2015 | Brexit day 24 Jun 2016 | Mar 2020 | 10 Jul – 5 Aug 2024 |
|---|---|---|---|---|---|---|
| (a) TSMOM | +11.6% | −2.3% | −1.9% | −2.6% | +3.7% | −0.1% |
| (b) Donchian | +11.7% | −2.3% | −1.9% | −1.8% | +2.0% | −0.6% |
| (c) XS mom 3m | +14.4% | +1.3% | −1.6% | −4.6% | +14.9% | −5.2% |
| (d) Carry unscaled | −23.4% | −3.3% | −4.9% | −0.1% | −4.1% | −6.4% |
| (d) Carry VT10 | −18.6% | −5.2% | −7.6% | −0.1% | −9.8% | **−14.6%** |
| (f) Combo | −6.8% | −4.7% | −5.6% | −2.4% | −3.9% | −9.6% |

- **Diversification:** the daily correlation of (a) with (d) is −0.02 to −0.05 (full output). That is why the combo has the best Sharpe despite weak components.
- **Carry book composition:**
  - Long NZD on 89% of month-ends, AUD 68%, NOK 65%, USD 37%.
  - Short CHF 100%, JPY 62%, SEK 55%, EUR 42%.
  - The ex-ante rate differential averaged **3.3%/yr**: 4–5.5% in 2000–08 and only 0.8–1.2% in 2020–21.
- **Turnover:** TSMOM's 39 round trips a year come mostly from daily vol re-scaling. Its weights change sign, including moves to and from flat, about 28 times per pair per year, but each such change is small. Donchian's is 9.

#### Caveats (stated honestly)
- **Prices**
  - H.10 is a **noon New York mid-type "buying rate" fixing**, not bid/ask, and it has **no intraday data**. Flash crashes (GBP 2016, JPY 2019) and intraday SNB extremes are invisible, and stops and margin close-outs are not modelled.
  - Values have 4–5 significant digits, a small source of quantisation noise.
- **Rates**
  - The rates are **monthly averages of 3-month interbank rates**, not the overnight tom-next rates retail swaps follow. They include term and credit premia, which were large in 2008.
  - EUR and GBP after Jan 2026 are spliced from the ECB deposit rate and SONIA, and every series is forward-filled for the last 1–3 months.
  - Carry signals use a one-month lag, so they are not look-ahead.
- **Costs are constant in pips for 26 years.**
  - Retail spreads in the early 2000s were wider, so pre-2008 results are flattered.
  - The constant 1% markup is a midpoint of the 0.3–2% range found in section 3; a large IG or Saxo account might pay about 0.5%.
  - Interpolating the markup 0 and 1% runs gives an inferred full-period Sharpe of roughly 0.12 for TSMOM and 0.32 for the combo at 0.5%.
- **Selection and survivorship bias**
  - The G10 universe, USD as the base currency, and the ensemble lookbacks were chosen with hindsight from a literature that studied much of 1999–2015.
  - Only roughly 2016–2026 is out-of-sample relative to most of that literature, and the strategies did worst in exactly that window.
- **Signals and sizing**
  - Momentum signals use spot, not carry-inclusive total returns.
  - Vol targeting uses EWMA(60) with a 4× cap, and there is no rebalance band. A band would reduce TSMOM's 0.96%/yr spread drag but not the markup.
- **Not modelled:** taxes, interest on margin cash, broker-specific margin calls, and negative-balance events.
- **Statistics**
  - The bootstrap p-values are not corrected for the 9 variants. With a Bonferroni-style bar, nothing comes close: the best is p ≈ 0.15 against a needed ≈ 0.006.
  - Every full-period t-statistic is about 1.0 or lower. Only the pre-2008 sub-period looks strong, and it is in-sample to the literature.

#### Full printed output (`uv run --no-project --with pandas --with numpy python -I fx_backtest.py data/fx_daily.csv data/rates`, uv's download/installation lines removed)
```
FX data: 1999-01-04 to 2026-10-09, 6965 fixing days, 250.7 obs/yr; dates with a partial-missing row dropped: 0
Rates: JPY before 2002-04: Japan call rate IRSTCI01JPM156N
Rates: EUR after 2026-01: ECBDFR monthly mean + +0.028pp spread
Rates: GBP after 2026-01: IUDSOIA monthly mean + -0.015pp spread
Rates: last observed month per series (then forward-filled): {'USD': '2026-08', 'EUR': '2026-09', 'JPY': '2026-07', 'GBP': '2026-09', 'CHF': '2026-08', 'AUD': '2026-08', 'NZD': '2026-08', 'CAD': '2026-08', 'SEK': '2026-08', 'NOK': '2026-08'}
Baseline round-trip cost (pips) and as bp of price on the last date:
  EUR:1p=0.89bp  JPY:1.2p=0.76bp  GBP:1.8p=1.36bp  CHF:1.8p=2.17bp  AUD:1.3p=1.86bp  NZD:2p=3.56bp  CAD:1.8p=1.26bp  SEK:50p=5.00bp  NOK:50p=5.23bp
Financing: rate differential of the holding month minus 1.0%/yr markup per leg

=== Data check: largest one-day moves of each currency vs USD (USD price) ===
EUR: min -2.96% on 2008-12-19  max +4.74% on 2009-03-19  ann.vol 9.1%
JPY: min -3.29% on 2013-04-04  max +5.35% on 2008-10-24  ann.vol 10.0%
GBP: min -7.84% on 2016-06-24  max +4.53% on 2008-10-29  ann.vol 9.1%
CHF: min -8.51% on 2011-09-06  max +13.91% on 2015-01-15  ann.vol 10.1%
AUD: min -7.89% on 2008-10-06  max +8.01% on 2008-10-14  ann.vol 12.0%
NZD: min -5.99% on 2008-10-24  max +6.11% on 2009-03-19  ann.vol 12.4%
CAD: min -3.74% on 2008-11-20  max +5.20% on 2008-10-29  ann.vol 8.3%
SEK: min -5.32% on 2009-02-17  max +5.44% on 2008-12-17  ann.vol 11.5%
NOK: min -5.93% on 2020-03-18  max +6.66% on 2009-03-19  ann.vol 12.0%

=== 3m rates used (annual averages, % p.a.) ===
       USD   EUR   JPY   GBP   CHF   AUD   NZD   CAD   SEK   NOK
2000  6.46  4.39  0.11  6.19  2.94  6.18  6.52  5.44  3.95  6.75
2001  3.69  4.26  0.06  5.04  2.81  4.90  5.74  3.86  4.00  7.23
2002  1.73  3.32  0.06  4.06  1.05  4.75  5.67  2.51  4.07  6.91
2003  1.15  2.33  0.09  3.74  0.22  4.90  5.42  2.86  3.03  4.10
2004  1.56  2.11  0.09  4.64  0.38  5.48  6.13  2.22  2.11  2.01
2005  3.51  2.18  0.09  4.76  0.71  5.64  7.11  2.70  1.72  2.21
2006  5.15  3.08  0.32  4.85  1.41  5.99  7.55  4.01  2.33  3.10
2007  5.27  4.28  0.75  6.00  2.34  6.67  8.33  4.14  3.55  4.96
2008  2.96  4.63  0.85  5.51  1.84  6.97  8.02  2.34  3.90  6.22
2009  0.56  1.23  0.58  1.21  0.09  3.43  3.04  0.33  0.40  2.46
2010  0.31  0.81  0.38  0.70  0.15  4.68  3.00  0.56  0.50  2.50
2011  0.30  1.39  0.33  0.87  0.06  4.85  2.80  0.91  1.66  2.87
2012  0.28  0.57  0.33  0.83 -0.06  3.73  2.67  0.94  1.25  2.24
2013  0.17  0.22  0.24  0.51 -0.05  2.78  2.66  0.97  0.93  1.76
2014  0.12  0.21  0.20  0.54  0.00  2.68  3.42  0.91  0.42  1.70
2015  0.23 -0.02  0.17  0.57 -0.72  2.26  3.24  0.53 -0.29  1.29
2016  0.64 -0.26  0.07  0.50 -0.77  1.99  2.33  0.49 -0.66  1.07
2017  1.15 -0.33  0.06  0.36 -0.85  1.74  1.96  0.69 -0.70  0.89
2018  2.19 -0.32  0.07  0.72 -0.81  1.95  1.94  1.37 -0.69  1.07
2019  2.21 -0.36  0.03  0.81 -0.77  1.34  1.52  1.66 -0.42  1.55
2020  0.60 -0.43 -0.04  0.30 -0.70  0.26  0.48  0.45 -0.14  0.70
2021  0.11 -0.55 -0.07  0.09 -0.74  0.03  0.49  0.11 -0.19  0.50
2022  2.23  0.34 -0.03  2.00 -0.18  1.64  2.77  2.18  0.74  2.14
2023  5.18  3.43  0.00  4.95  1.52  3.98  5.48  4.74  3.57  4.21
2024  5.05  3.57  0.19  5.00  1.24  4.39  5.26  4.37  3.47  4.72
2025  4.17  2.18  0.81  4.12  0.09  3.82  3.21  2.58  2.12  4.38
2026  3.75  2.16  1.34  3.71 -0.04  4.32  2.72  2.25  1.95  4.44

=== FULL 2000-01-03 to 2026-10-09 ===
strategy                                   CAGR   Vol  Shrp  MaxDD  Lev  RT/yr  Sprd  Carry  Mkup  WrstD  WrstM
(a) TSMOM ens 1/3/6/12m, VT10             -0.1% 10.1%  0.04 -47.4%  1.6   39.0 0.96% +0.55% 1.60%  -4.1%  -8.0%
(b) Donchian ens 20/55/100/200, VT10      -0.1% 10.2%  0.04 -55.8%  1.6   16.4 0.40% +0.51% 1.58%  -4.1%  -6.7%
(c) XS momentum 3m top3/bottom3, VT10     -4.7% 10.6% -0.40 -75.1%  2.5   13.3 0.36% +0.50% 2.47%  -5.6%  -8.9%
(c) XS momentum 12m top3/bottom3, VT10    -4.1% 10.7% -0.33 -71.7%  2.5    8.3 0.22% +0.78% 2.53%  -7.2% -10.0%
(d) G10 carry top3/bottom3, unscaled       0.8%  8.0%  0.14 -39.6%  1.8    0.6 0.02% +3.28% 1.77%  -6.1% -10.8%
(d) G10 carry top3/bottom3, VT10           0.8% 10.5%  0.13 -61.3%  2.7    2.1 0.06% +4.99% 2.73%  -5.5%  -9.8%
(e1) EURUSD 5d reversal, VT10             -2.6% 10.0% -0.22 -52.9%  1.2   62.8 0.54% -0.05% 1.24%  -4.0%  -8.8%
(e2) EURUSD RSI(2) 10/90 fade, VT10       -2.9%  6.5% -0.42 -57.8%  0.5   34.1 0.29% -0.05% 0.54%  -4.0%  -8.1%
(f) 50/50 (a)+(d), VT10                    1.5% 10.2%  0.20 -46.8%  2.5   32.6 0.81% +3.91% 2.55%  -4.7%  -6.0%
Bench: long USD basket, unscaled          -1.8%  8.0% -0.18 -57.7%  1.0    0.0 0.00% +0.06% 1.00%  -4.9%  -6.9%
Bench: long USD basket, VT10              -1.6% 10.2% -0.10 -69.1%  1.4    1.5 0.04% +0.23% 1.42%  -3.3%  -8.2%

=== pre-2008 (2000-01-03..2007-12-31) ===
strategy                                   CAGR   Vol  Shrp  MaxDD  Lev  RT/yr  Sprd  Carry  Mkup  WrstD  WrstM
(a) TSMOM ens 1/3/6/12m, VT10              4.7% 10.1%  0.51 -26.1%  1.5   33.1 0.81% +1.05% 1.50%  -3.2%  -5.5%
(b) Donchian ens 20/55/100/200, VT10       6.7% 10.3%  0.68 -17.4%  1.5   14.4 0.36% +1.08% 1.52%  -3.6%  -4.2%
(c) XS momentum 3m top3/bottom3, VT10     -2.8% 10.3% -0.22 -23.3%  2.3   11.8 0.33% +1.29% 2.27%  -4.7%  -5.4%
(c) XS momentum 12m top3/bottom3, VT10    -2.2% 10.2% -0.17 -32.8%  2.4    8.1 0.23% +2.16% 2.39%  -5.5%  -7.0%
(d) G10 carry top3/bottom3, unscaled       6.8%  7.1%  0.96 -11.7%  1.8    0.5 0.02% +4.58% 1.77%  -4.2%  -4.8%
(d) G10 carry top3/bottom3, VT10          11.2% 10.6%  1.05 -19.4%  2.8    1.9 0.06% +7.06% 2.75%  -5.0%  -7.5%
(e1) EURUSD 5d reversal, VT10             -1.8% 10.0% -0.13 -29.6%  1.1   56.9 0.51% -0.10% 1.12%  -2.4%  -6.0%
(e2) EURUSD RSI(2) 10/90 fade, VT10       -4.0%  6.2% -0.63 -30.2%  0.5   29.3 0.26% -0.03% 0.49%  -2.4%  -6.1%
(f) 50/50 (a)+(d), VT10                   11.4% 10.2%  1.10 -16.4%  2.4   26.1 0.65% +5.32% 2.37%  -3.9%  -4.3%
Bench: long USD basket, unscaled          -5.3%  7.4% -0.69 -46.9%  1.0    0.0 0.00% -0.12% 1.00%  -1.7%  -5.2%
Bench: long USD basket, VT10              -8.0% 10.2% -0.77 -62.3%  1.4    1.5 0.04% -0.08% 1.42%  -2.3%  -8.2%

=== 2008-2014 ===
strategy                                   CAGR   Vol  Shrp  MaxDD  Lev  RT/yr  Sprd  Carry  Mkup  WrstD  WrstM
(a) TSMOM ens 1/3/6/12m, VT10              1.9% 10.3%  0.24 -31.8%  1.5   36.3 1.05% +0.21% 1.49%  -3.0%  -6.5%
(b) Donchian ens 20/55/100/200, VT10       2.2% 10.3%  0.27 -31.1%  1.4   14.7 0.39% +0.13% 1.44%  -2.8%  -6.3%
(c) XS momentum 3m top3/bottom3, VT10     -0.5% 10.5%  0.00 -26.9%  1.9   10.2 0.31% +0.11% 1.94%  -3.6%  -6.2%
(c) XS momentum 12m top3/bottom3, VT10    -3.0% 11.7% -0.21 -41.3%  2.2    7.0 0.21% +0.31% 2.21%  -7.2% -10.0%
(d) G10 carry top3/bottom3, unscaled      -3.5% 11.1% -0.27 -30.3%  1.8    0.7 0.02% +3.13% 1.77%  -6.1% -10.8%
(d) G10 carry top3/bottom3, VT10          -5.9% 10.7% -0.51 -37.9%  2.0    1.7 0.05% +3.43% 1.98%  -5.5%  -8.6%
(e1) EURUSD 5d reversal, VT10             -4.6% 10.1% -0.42 -36.4%  1.1   51.8 0.38% -0.01% 1.08%  -4.0%  -8.3%
(e2) EURUSD RSI(2) 10/90 fade, VT10       -3.8%  6.6% -0.55 -30.5%  0.5   27.8 0.21% -0.00% 0.48%  -4.0%  -5.9%
(f) 50/50 (a)+(d), VT10                   -1.7% 10.2% -0.12 -28.9%  2.1   32.5 0.94% +2.82% 2.11%  -4.3%  -5.8%
Bench: long USD basket, unscaled          -1.7%  9.7% -0.13 -34.6%  1.0    0.0 0.00% -1.15% 1.00%  -4.9%  -6.9%
Bench: long USD basket, VT10               0.8% 10.1%  0.13 -30.9%  1.3    1.4 0.04% -1.46% 1.27%  -2.9%  -6.1%

=== 2015-2021 ===
strategy                                   CAGR   Vol  Shrp  MaxDD  Lev  RT/yr  Sprd  Carry  Mkup  WrstD  WrstM
(a) TSMOM ens 1/3/6/12m, VT10             -2.7% 10.0% -0.23 -25.4%  1.7   43.4 0.99% +0.40% 1.74%  -3.2%  -4.8%
(b) Donchian ens 20/55/100/200, VT10      -5.2% 10.0% -0.49 -37.8%  1.7   18.6 0.44% +0.35% 1.74%  -3.1%  -6.7%
(c) XS momentum 3m top3/bottom3, VT10    -10.7% 11.5% -0.93 -55.3%  2.8   15.9 0.41% -0.13% 2.80%  -5.6%  -7.9%
(c) XS momentum 12m top3/bottom3, VT10    -6.5% 10.7% -0.57 -41.0%  2.6    8.1 0.21% -0.24% 2.64%  -3.8%  -7.0%
(d) G10 carry top3/bottom3, unscaled      -1.1%  6.7% -0.13 -14.6%  1.8    0.5 0.01% +2.03% 1.82%  -3.3%  -4.1%
(d) G10 carry top3/bottom3, VT10          -3.1% 10.4% -0.25 -29.2%  3.0    2.0 0.05% +3.37% 3.07%  -5.2%  -9.8%
(e1) EURUSD 5d reversal, VT10             -0.8% 10.0% -0.03 -16.5%  1.4   74.0 0.65% -0.05% 1.44%  -3.4%  -8.8%
(e2) EURUSD RSI(2) 10/90 fade, VT10       -2.9%  6.8% -0.40 -21.0%  0.6   41.8 0.37% -0.06% 0.64%  -3.3%  -8.1%
(f) 50/50 (a)+(d), VT10                   -2.6% 10.2% -0.21 -23.8%  2.8   35.3 0.82% +2.74% 2.81%  -4.7%  -5.9%
Bench: long USD basket, unscaled           0.1%  6.9%  0.05 -18.8%  1.0    0.0 0.00% +0.60% 1.00%  -2.5%  -4.5%
Bench: long USD basket, VT10               1.1% 10.2%  0.15 -21.8%  1.6    1.7 0.04% +1.19% 1.60%  -3.3%  -7.5%

=== 2022-2026 (to end) ===
strategy                                   CAGR   Vol  Shrp  MaxDD  Lev  RT/yr  Sprd  Carry  Mkup  WrstD  WrstM
(a) TSMOM ens 1/3/6/12m, VT10             -6.9% 10.1% -0.66 -40.0%  1.7   46.5 1.02% +0.41% 1.72%  -4.1%  -8.0%
(b) Donchian ens 20/55/100/200, VT10      -6.7% 10.1% -0.63 -40.4%  1.6   18.8 0.41% +0.32% 1.63%  -4.1%  -6.7%
(c) XS momentum 3m top3/bottom3, VT10     -5.1% 10.0% -0.48 -32.0%  3.1   16.6 0.42% +0.68% 3.12%  -2.7%  -8.9%
(c) XS momentum 12m top3/bottom3, VT10    -5.0% 10.0% -0.46 -30.7%  3.1   10.8 0.27% +0.62% 3.08%  -2.6%  -5.7%
(d) G10 carry top3/bottom3, unscaled       0.1%  5.3%  0.04 -12.5%  1.7    0.9 0.02% +3.15% 1.72%  -1.8%  -3.7%
(d) G10 carry top3/bottom3, VT10           0.1% 10.2%  0.06 -23.2%  3.3    3.0 0.08% +6.14% 3.33%  -3.3%  -7.2%
(e1) EURUSD 5d reversal, VT10             -3.8% 10.1% -0.33 -22.0%  1.4   72.6 0.66% -0.02% 1.39%  -2.9%  -4.5%
(e2) EURUSD RSI(2) 10/90 fade, VT10        0.3%  6.4%  0.08  -9.1%  0.6   39.9 0.36% -0.10% 0.55%  -2.3%  -4.8%
(f) 50/50 (a)+(d), VT10                   -3.4% 10.2% -0.28 -29.0%  3.1   39.6 0.88% +4.86% 3.12%  -4.7%  -6.0%
Bench: long USD basket, unscaled           1.5%  7.8%  0.22 -13.3%  1.0    0.0 0.00% +1.38% 1.00%  -2.1%  -4.6%
Bench: long USD basket, VT10               2.5% 10.1%  0.30 -17.6%  1.4    1.5 0.04% +1.83% 1.36%  -2.8%  -5.4%

=== Calendar-year net returns ===
strategy                                    2008    2015    2022    2024    2025    2026
(a) TSMOM ens 1/3/6/12m, VT10              14.8%   -0.0%    8.6%  -18.5%  -10.6%   -5.2%
(b) Donchian ens 20/55/100/200, VT10       19.3%   -3.2%   10.0%  -13.9%  -10.9%   -3.0%
(c) XS momentum 3m top3/bottom3, VT10      14.0%  -10.1%   -4.9%  -13.2%   12.5%   -6.7%
(c) XS momentum 12m top3/bottom3, VT10      5.1%   -1.4%   -0.3%  -13.5%   -4.4%   -5.4%
(d) G10 carry top3/bottom3, unscaled      -24.8%   -7.1%   -5.4%    4.7%   -3.2%    6.7%
(d) G10 carry top3/bottom3, VT10          -21.2%  -10.9%   -8.7%    9.2%   -6.8%   14.7%
(e1) EURUSD 5d reversal, VT10             -12.8%   -4.4%   -5.7%   -2.9%   -7.6%   -5.4%
(e2) EURUSD RSI(2) 10/90 fade, VT10        -6.4%   -8.5%   -2.0%   -4.8%    5.4%   -3.7%
(f) 50/50 (a)+(d), VT10                    -7.5%   -8.2%    0.6%   -5.7%  -11.1%    6.9%
Bench: long USD basket, unscaled            9.2%    6.8%    7.4%    9.2%   -8.5%    1.7%
Bench: long USD basket, VT10                9.1%    9.0%   12.3%   13.0%  -11.0%    2.5%
(2026 = year to date)

=== Robustness on FULL period (Sharpe) and block-bootstrap P(Sharpe<=0) ===
strategy                                  base  +1lag  c0.5x    c2x    mk0   mk2%   spot frict0     t  p(21d)  p(63d)
(a) TSMOM ens 1/3/6/12m, VT10              0.04   0.00   0.09  -0.06   0.20  -0.12   0.24   0.29  0.20   0.435   0.445
(b) Donchian ens 20/55/100/200, VT10       0.04  -0.01   0.06   0.00   0.19  -0.11   0.18   0.23  0.20   0.437   0.432
(c) XS momentum 3m top3/bottom3, VT10     -0.40  -0.45  -0.39  -0.44  -0.17  -0.64  -0.19  -0.14 -2.09   0.986   0.989
(c) XS momentum 12m top3/bottom3, VT10    -0.33  -0.37  -0.32  -0.35  -0.10  -0.57  -0.15  -0.08 -1.72   0.967   0.967
(d) G10 carry top3/bottom3, unscaled       0.14   0.12   0.14   0.13   0.36  -0.08  -0.05   0.36  0.70   0.231   0.225
(d) G10 carry top3/bottom3, VT10           0.13   0.12   0.13   0.12   0.39  -0.13  -0.08   0.39  0.67   0.258   0.256
(e1) EURUSD 5d reversal, VT10             -0.22  -0.12  -0.19  -0.27  -0.09  -0.34  -0.03  -0.04 -1.12   0.858   0.882
(e2) EURUSD RSI(2) 10/90 fade, VT10       -0.42  -0.13  -0.40  -0.47  -0.34  -0.50  -0.29  -0.29 -2.17   0.987   0.991
(f) 50/50 (a)+(d), VT10                    0.20   0.15   0.24   0.12   0.44  -0.05   0.14   0.52  1.01   0.154   0.138
Bench: long USD basket, unscaled          -0.18  -0.18  -0.18  -0.18  -0.06  -0.31  -0.07  -0.06 -0.95   0.831   0.834
Bench: long USD basket, VT10              -0.10  -0.10  -0.10  -0.11   0.03  -0.24   0.02   0.04 -0.54   0.703   0.696
cols: base | one extra day of lag | spread cost x0.5 | x2 | markup 0 | markup 2%/yr | spot only (no carry, no markup, no spread) | frictionless (spot + carry, no costs) | t = Sharpe*sqrt(yrs)

=== Correlation of daily net returns, FULL period ===
            a     b    c3   c12  d_raw     d    e1    e2     f  usd_raw   usd
a        1.00  0.92  0.48  0.43  -0.05 -0.02 -0.24 -0.22  0.68     0.03  0.02
b        0.92  1.00  0.51  0.36  -0.06 -0.03 -0.21 -0.21  0.63     0.05  0.05
c3       0.48  0.51  1.00  0.51  -0.09 -0.02 -0.03 -0.02  0.31     0.09  0.07
c12      0.43  0.36  0.51  1.00  -0.05  0.03 -0.03 -0.02  0.29     0.08  0.05
d_raw   -0.05 -0.06 -0.09 -0.05   1.00  0.92  0.04  0.07  0.62    -0.29 -0.22
d       -0.02 -0.03 -0.02  0.03   0.92  1.00  0.03  0.06  0.69    -0.17 -0.14
e1      -0.24 -0.21 -0.03 -0.03   0.04  0.03  1.00  0.65 -0.15     0.02  0.02
e2      -0.22 -0.21 -0.02 -0.02   0.07  0.06  0.65  1.00 -0.12     0.02  0.02
f        0.68  0.63  0.31  0.29   0.62  0.69 -0.15 -0.12  1.00    -0.10 -0.07
usd_raw  0.03  0.05  0.09  0.08  -0.29 -0.17  0.02  0.02 -0.10     1.00  0.95
usd      0.02  0.05  0.07  0.05  -0.22 -0.14  0.02  0.02 -0.07     0.95  1.00
codes in table order: a=(a) TSMOM ens 1/3/6/12m, VT10, b=(b) Donchian ens 20/55/100/200, VT10, c3=(c) XS momentum 3m top3/bottom3, VT10, c12=(c) XS momentum 12m top3/bottom3, VT10, d_raw=(d) G10 carry top3/bottom3, unscaled, d=(d) G10 carry top3/bottom3, VT10, e1=(e1) EURUSD 5d reversal, VT10, e2=(e2) EURUSD RSI(2) 10/90 fade, VT10, f=(f) 50/50 (a)+(d), VT10, usd_raw=Bench: long USD basket, unscaled, usd=Bench: long USD basket, VT10

=== Tail windows: cumulative net return ===
strategy                                 GFC Sep-Dec  SNB 2015-01- SNB week 201 Brexit 2016- Covid Mar 20 Yen unwind 2
(a) TSMOM ens 1/3/6/12m, VT10                   11.6%        -2.3%        -1.9%        -2.6%         3.7%        -0.1%
(b) Donchian ens 20/55/100/200, VT10            11.7%        -2.3%        -1.9%        -1.8%         2.0%        -0.6%
(c) XS momentum 3m top3/bottom3, VT10           14.4%         1.3%        -1.6%        -4.6%        14.9%        -5.2%
(c) XS momentum 12m top3/bottom3, VT10          12.6%         0.9%        -1.0%         1.7%        10.2%        -6.0%
(d) G10 carry top3/bottom3, unscaled           -23.4%        -3.3%        -4.9%        -0.1%        -4.1%        -6.4%
(d) G10 carry top3/bottom3, VT10               -18.6%        -5.2%        -7.6%        -0.1%        -9.8%       -14.6%
(e1) EURUSD 5d reversal, VT10                   -9.4%        -2.4%        -3.6%         2.3%        -7.6%        -1.6%
(e2) EURUSD RSI(2) 10/90 fade, VT10             -9.0%        -2.4%        -3.6%         0.0%        -5.4%         0.6%
(f) 50/50 (a)+(d), VT10                         -6.8%        -4.7%        -5.6%        -2.4%        -3.9%        -9.6%
Bench: long USD basket, unscaled                 9.3%        -1.3%        -1.7%         2.2%         2.9%        -0.6%
Bench: long USD basket, VT10                     9.9%        -2.2%        -2.8%         2.6%         4.5%        -1.0%

=== Carry portfolio composition (share of month-ends long / short, FULL) ===
long : EUR:0% JPY:0% GBP:31% CHF:0% AUD:68% NZD:89% CAD:9% SEK:0% NOK:65% USD:37%
short: EUR:42% JPY:62% GBP:0% CHF:100% AUD:0% NZD:0% CAD:9% SEK:55% NOK:1% USD:30%
Ex-ante rate differential of the unscaled carry book, mean 3.30%/yr; by year: 2000:4.3% 2001:4.0% 2002:4.7% 2003:4.5% 2004:4.7% 2005:5.0% 2006:4.9% 2007:4.8% 2008:5.5% 2009:2.8% 2010:3.1% 2011:3.3% 2012:2.8% 2013:2.3% 2014:2.5% 2015:2.6% 2016:2.4% 2017:2.2% 2018:2.6% 2019:2.5% 2020:1.2% 2021:0.8% 2022:2.3% 2023:3.6% 2024:3.5% 2025:3.3% 2026:3.1%

=== Position sign changes per pair per year (FULL; signal turnover diagnostic) ===
(a) TSMOM ens 1/3/6/12m, VT10             27.8
(b) Donchian ens 20/55/100/200, VT10       9.1
(c) XS momentum 3m top3/bottom3, VT10      5.4
(c) XS momentum 12m top3/bottom3, VT10     3.3
(d) G10 carry top3/bottom3, unscaled       0.4
(d) G10 carry top3/bottom3, VT10           0.4
(e1) EURUSD 5d reversal, VT10             51.4
(e2) EURUSD RSI(2) 10/90 fade, VT10       52.8
(f) 50/50 (a)+(d), VT10                   12.4
Bench: long USD basket, unscaled           0.0
Bench: long USD basket, VT10               0.0

Variants: 9 strategy variants [(a), (b), (c)x2, (d)x2, (e1), (e2), (f)] + 2 benchmarks; the robustness columns are sensitivities of those, not extra selections. No parameter was tuned on this data.
```

### Inferences
- **FX trend and carry are not a free lunch for a small retail bot in 2026.**
  - Their frictionless G10 Sharpe ratios since 2000 are about 0.3–0.5. The retail financing markup alone removes roughly 0.15–0.25 of that, because these strategies hold 1.6–3.3× NAV in gross notional every day.
  - Spreads matter less. That reverses the BTC finding ("costs barely matter"), because there the gross edge was large and gross exposure was ≤1×.
- **The only defensible FX candidate is a diversified multi-pair book: trend plus carry, equal risk.** It reached a net Sharpe of 0.20 over 27 years (p ≈ 0.15) and has been negative since 2008 in every sub-period.
  - Expectation: a live net Sharpe of about 0 to 0.3 at best, with 30–50% drawdowns at a 10% vol target.
  - That is much weaker than the BTC trend case (Sharpe 0.6–0.9 in the ETF era), and it needs 9 instruments plus cross-currency risk management.
- **Single-pair EURUSD mean reversion (the "simple FX bot") lost money** on daily data in every sub-period except 2022–26 for RSI(2), and that only at about 0. It should not be built.
- **If FX is pursued, use the lowest-markup venue.**
  - Options: a large account at a broker charging about 0.5% (IG standard, Saxo); CME micro futures, where financing is in the futures basis at near-interbank rates (inferred, not tested); or IBKR spot with care about interest spreads.
  - Trade crosses directly (e.g. long AUDJPY) instead of two USD legs. That halves the legs that pay markup: at 1% per position, the carry book's 1.77%/yr markup would fall to about 0.9%/yr (inferred).
- **Vol-targeted carry is dangerous.** It levers up in calm periods just before crashes (−14.6% in four weeks in 2024). An unscaled or vol-capped carry sleeve is safer.

### Gaps
- No free bid/ask daily history could be downloaded (Dukascopy and HistData were blocked), so actual historical retail spreads, especially pre-2008, could not be measured.
- Tom-next or overnight rate histories for all G10 were not found, so carry uses 3-month interbank monthly averages.
- No intraday data, so stop-loss variants, the 17:00 NY close convention, and flash-event slippage could not be tested.
- CME micro futures roll costs and basis were not tested.
- Holding the out-of-sample period back was not possible in a meaningful way: the literature parameters already saw most of the sample.
