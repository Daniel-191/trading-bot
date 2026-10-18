# Project plan

How we build the bot: the parts it needs, the APIs it uses, what they cost, and the order we
build things in. Trading strategy is deliberately out of scope here. The engine has a
pluggable strategy interface, and strategies come later. Strategy research and the options
we're choosing between are in [`strategy/STRATEGY_OPTIONS.md`](strategy/STRATEGY_OPTIONS.md).

**Scope: Bitcoin only.** The bot trades a single BTC pair (e.g. `BTC/USDT`). The pair is a
config setting (`TRADING_PAIR`), not hardcoded, so adding another pair later is a config
change rather than a rewrite. We don't build multi-coin features (screening, rankings,
coin lists) unless we decide to widen the scope.

Prices and limits below were researched in October 2026 and come partly from third-party
comparison sites. **Check the vendor's own pricing page before paying for anything.**

---

## 1. Build vs. use an existing framework

Some open-source bots already have most of what we want:

| Framework | What it gives you | Notes |
|---|---|---|
| [Freqtrade](https://www.freqtrade.io) | Backtesting, paper/live trading, **built-in Telegram control**, web UI (FreqUI), uses CCXT | Python. Closest to this plan. Strategies are Python classes. |
| [Hummingbot](https://hummingbot.org) | Market making and arbitrage, many connectors | Built around market making. |
| [Jesse](https://jesse.trade) | Backtesting and live trading, clean strategy API | Some live features are paid. |

**Decision needed:** we're building our own, because we want to learn and to own the
architecture. That's a reasonable choice. Freqtrade is still the reference design: when
we're unsure how to do something (order state, Telegram commands, dry-run fills), see how
it does it first.

---

## 2. Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │                  Engine (asyncio)            │
 Exchange WS/REST ─▶│ MarketData ─▶ Strategy ─▶ RiskManager ─▶ OrderManager ─▶ Broker
   (via CCXT)       │      │                                   │          (paper | testnet | live)
                    │      ▼                                   ▼          │
                    │   Storage (SQLite → Postgres)      Portfolio/Positions
                    │                     │                                │
                    │                 EventBus (fills, errors, risk events, heartbeats)
                    └─────────┬───────────────────────────┬────────────────┘
                              │ Control API (one place for commands)
                     ┌────────┴────────┐          ┌───────┴────────┐
                     │  Telegram bot   │          │ FastAPI + WS   │──▶ Dashboard (web)
                     │ commands+alerts │          │  REST + live   │
                     └─────────────────┘          └────────────────┘
```

### Key principles
- **The engine is the single source of truth.** Telegram and the dashboard never touch the
  exchange directly. Both call the same internal `Control` interface (pause, resume, status,
  flatten), so the two front-ends can't drift apart.
- **One `Broker` interface, three implementations:** `PaperBroker` (simulated fills from live
  prices), `TestnetBroker` and `LiveBroker` (both CCXT). `TRADING_MODE` selects one and
  defaults to `paper`.
- **Event bus:** components publish events (`OrderFilled`, `RiskLimitHit`, `EngineError`,
  `Heartbeat`). The Telegram alerter and the dashboard WebSocket subscribe to them, so neither
  is wired into the engine.
- **Start as one process** (engine, API and Telegram as asyncio tasks in one loop). Split
  into separate services only when we need to.
- `Decimal` everywhere for prices, quantities and money (see CLAUDE.md).

### Components

| Module (`src/trading_bot/…`) | Responsibility |
|---|---|
| `config.py` | Load settings from env vars (pydantic-settings), validate them, refuse to start `live` without explicit flags |
| `exchange/` | CCXT wrapper: markets, precision/min-size rules, OHLCV, order book, balances. Retries and rate-limit handling. |
| `marketdata/` | WebSocket streams (`ccxt` `watch_*`), candle building, gap backfill from REST |
| `strategy/` | `Strategy` protocol: `on_candle` / `on_tick` → `Signal`. Ships with a dummy strategy only. |
| `risk/` | Pre-trade checks: max position size, max open orders, daily loss limit, max drawdown, kill switch |
| `orders/` | Order lifecycle state machine (new → open → partial → filled/cancelled/rejected), reconciliation with the exchange on startup |
| `broker/` | `PaperBroker`, `TestnetBroker`, `LiveBroker` |
| `portfolio/` | Positions, average entry, realised/unrealised PnL, equity curve |
| `storage/` | SQLAlchemy models: candles, orders, fills, positions, equity snapshots, events. SQLite first, Postgres later. |
| `events.py` | In-process async pub/sub |
| `control.py` | The command interface Telegram and the API both use |
| `telegram/` | Bot commands and alert formatting |
| `api/` | FastAPI app: REST endpoints and a WebSocket for live updates |
| `backtest/` | Replays stored candles through the same Strategy, Risk and PaperBroker code |

---

## 3. Backend stack

| Need | Choice | Why |
|---|---|---|
| Language/runtime | Python 3.13, asyncio | Already set up. Every library below is async. |
| Exchange access | [`ccxt`](https://docs.ccxt.com) (MIT, free) | One API for 100+ exchanges. WebSocket support ("CCXT Pro") is now bundled free in the main package. |
| Web API | FastAPI + uvicorn | Async, typed, automatic OpenAPI docs, built-in WebSockets |
| Config | pydantic-settings | Typed env-var config |
| DB | SQLAlchemy 2 (async) + Alembic; SQLite then Postgres | Starts with no setup and migrates cleanly |
| Telegram | `python-telegram-bot` (v21+, async) | Mature, good docs, built-in rate limiter |
| Logging | `structlog` (JSON logs) | Logs you can search on a VPS |
| Errors | Sentry (free tier) | Alerts on exceptions |
| Tests | pytest, pytest-asyncio, recorded exchange responses | No real exchange calls in tests |

---

## 4. Telegram bot

Free. Create the bot with [@BotFather](https://t.me/BotFather) to get a token.

### Commands
| Command | Action |
|---|---|
| `/status` | Mode (paper/testnet/live), running or paused, uptime, last heartbeat |
| `/balance` | Exchange balances / paper equity |
| `/positions` | Open positions with unrealised PnL |
| `/orders` | Open orders |
| `/pnl [today\|week\|all]` | Realised PnL summary |
| `/pause`, `/resume` | Stop/start opening new positions (existing ones stay) |
| `/flatten` | Cancel all orders and close all positions. **Needs an inline-button confirmation.** |
| `/kill` | Flatten, then stop the engine. **Needs confirmation.** |
| `/risk` | Show current risk limits and how much of each is used |
| `/help` | Command list |

### Alerts (push)
Order filled/rejected · risk limit hit · engine error/exception · exchange disconnected/reconnected ·
missed heartbeat · daily summary at a fixed time.

### Security
- **Allowlist:** only respond to user IDs in `TELEGRAM_ALLOWED_USER_IDS`. Silently ignore
  everyone else and log the attempt.
- Destructive commands need a confirmation button and are written to an audit log.
- No command can change mode to `live` or edit API keys.

### Limits
Telegram doesn't publish exact numbers. The community consensus is about 30 messages/second
overall, about 1/second per chat and about 20/minute per group. That's plenty for alerts.
Batch bursts (e.g. many fills at once) into one message. Use PTB's `AIORateLimiter`
(`python-telegram-bot[rate-limiter]`).

---

## 5. Dashboard

The backend is FastAPI (REST + WebSocket). Two options for the front end:

| Option | Pros | Cons |
|---|---|---|
| **A. React + Vite + [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts)** (Apache-2.0, free) | Proper real-time UI, good candlestick charts, scales up | Second language (TypeScript), more work |
| B. Streamlit | All Python, a working page in a day | Clunky for live updates, harder to make look good |

**Recommendation:** start with **B** if we want something soon. Move to **A** once the API
is stable. Both use the same FastAPI endpoints, so nothing is wasted.

### Pages
Overview (equity curve, PnL, mode, running/paused) · Positions & open orders · Trade history ·
Live chart with our fills marked · Logs/events · Risk limits · Controls (pause/resume/flatten,
going through the same `Control` interface as Telegram).

### Security
Never expose the dashboard publicly without auth. Simplest: bind to localhost on the VPS and
reach it over [Tailscale](https://tailscale.com) (free for personal use) or an SSH tunnel.
Otherwise put it behind a login (basic auth over HTTPS, or Cloudflare Access).

---

## 6. APIs: what we need and what it costs

### 6a. Exchange APIs (required)

Exchange APIs are **free**. You pay trading fees per trade. Pick **one** exchange to start.
Which one depends on where we live: Binance in particular is restricted in several
countries, and Coinbase fees vary by region.

| Exchange | Entry spot fees (maker / taker) | Paper/testnet | Notes |
|---|---|---|---|
| **Binance** | ~0.10% / 0.10% (0.075% paying in BNB) | ✅ Spot testnet (testnet.binance.vision) | Deepest liquidity, best API docs. Check availability in our country. |
| **Bybit** | ~0.10% / 0.10% | ✅ Testnet + demo trading | Good API, strong derivatives |
| **OKX** | ~0.08% / 0.10% | ✅ Demo trading | Good API |
| **Kraken** | ~0.16–0.25% / 0.26–0.40% (sources disagree) | ⚠️ No full spot sandbox, as far as we can tell (futures demo exists) | Strongly regulated. Check its docs. |
| **Coinbase Advanced** | Region-dependent after a Sept 2026 overhaul (reported ~0.25/0.50% EU/UK, higher in US) | ⚠️ Limited sandbox | Most expensive at low volume |

**Recommendation:** Binance or Bybit, whichever is available to us. Both have real testnets,
so we can test the whole `testnet` path without any risk.

Key safety settings for any exchange API key: **trading only, withdrawals disabled, IP
allowlisted to the VPS.**

Rate limits are weight-based and per IP (Binance: read live values from `exchangeInfo`,
watch the `X-MBX-USED-WEIGHT-*` headers, back off on 429 or you get an IP ban (418)). Use
WebSockets for market data instead of polling REST.

### 6b. Market data (mostly free)

**The exchange's own WebSocket and REST APIs are the best data source for a trading bot.**
They are real-time and free, and the prices are exactly where our orders will fill. Paid
aggregators are only needed for cross-exchange screening, coin metadata or on-chain metrics.

**We use CoinMarketCap as our one aggregator** (key in `COINMARKETCAP_API_KEY`). Live prices,
order books and our own orders still come free from the exchange; CoinMarketCap covers what the
exchange doesn't. We don't add CoinGecko alongside it.

| Source | Free tier | Paid | Use for |
|---|---|---|---|
| Exchange WS/REST via CCXT | ✅ Free | — | Live prices, order books, OHLCV, our orders/balances |
| [Binance public data](https://data.binance.vision) | ✅ Free bulk downloads | — | Historical candles/trades for backtesting |
| [CoinMarketCap](https://coinmarketcap.com/api/pricing/) | Basic: ~10–15k credits/mo | ~$29/mo and ~$79/mo tiers (annual billing; plan names inconsistent across sources) | Market caps, coin metadata, cross-exchange prices |
| CoinDesk Data (ex-CryptoCompare) | ❌ Free tier retired May 2026 | Sales-only pricing | Skip |
| [Glassnode](https://glassnode.com) | Free web studio only | ~$49/mo Advanced includes only a "Light API" (~50 calls/day); full API ~$999/mo+ | On-chain metrics. Only if a strategy needs them. |
| Kaiko / Amberdata / CoinAPI | — | Enterprise, quote-based | Not needed |
| [Alternative.me Fear & Greed](https://alternative.me/crypto/fear-and-greed-index/) | ✅ Free | — | Sentiment indicator |

### 6c. Other services

| Service | Cost |
|---|---|
| Telegram Bot API | Free |
| VPS (Hetzner ~€4–6/mo; DigitalOcean/Vultr ~$6/mo) | ~$5–7/mo. Hetzner raised prices in 2026, so check current rates. |
| Sentry (errors) | Free tier |
| [Healthchecks.io](https://healthchecks.io) (dead-man's switch: alerts if the bot stops pinging) | Free tier |
| Tailscale (private dashboard access) | Free (personal) |
| GitHub Actions CI | Free for this usage |

**Expected monthly cost for MVP: about $5–10** (just the VPS). Paid data APIs are optional.

---

## 7. Configuration (env vars to add to `.env.example` as we build)

```
TRADING_MODE=paper              # paper | testnet | live
EXCHANGE=binance
TRADING_PAIR=BTC/USDT           # BTC only for now
EXCHANGE_API_KEY=
EXCHANGE_API_SECRET=
COINMARKETCAP_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USER_IDS=      # comma-separated numeric IDs
DATABASE_URL=sqlite+aiosqlite:///./data/bot.db
API_HOST=127.0.0.1
API_PORT=8000
SENTRY_DSN=
HEALTHCHECK_URL=
# Risk limits
RISK_MAX_POSITION_PCT=
RISK_DAILY_LOSS_LIMIT_PCT=
RISK_MAX_OPEN_ORDERS=
```

---

## 8. Roadmap

Each phase is a GitHub issue (linked below). Each phase can be split into smaller PRs.
Phases 4 and 5 can run in parallel once phase 3's `Control` interface and event bus exist,
so one of us can take Telegram and the other the dashboard.

| Phase | Deliverable | Issue |
|---|---|---|
| 1. Foundations | Config, logging, exchange adapter over CCXT, `Decimal` money types, test fixtures with recorded exchange data | #2 |
| 2. Market data & storage | WebSocket price/candle streams, REST backfill, DB schema + migrations | #3 |
| 3. Engine core | Strategy interface (dummy strategy), risk manager, order manager, `PaperBroker`, portfolio/PnL, event bus, `Control` interface | #4 |
| 4. Telegram bot | Commands, alerts, allowlist, confirmations | #5 |
| 5. API & dashboard | FastAPI REST/WS, first dashboard | #6 |
| 6. Backtesting | Replay historical candles through the same engine path | #7 |
| 7. Deploy & monitoring | Docker, VPS, Sentry, healthchecks, run on **testnet** for weeks | #8 |

Going live is deliberately **not** a phase here. It needs its own issue, both of us agreeing,
and very small position sizes, after a long testnet run.

---

## Sources
- CCXT (Pro bundled, exchange counts): https://docs.ccxt.com/docs/comparisons/ccxt-vs-ccxws
- Binance spot testnet & rate limits: https://developers.binance.com/docs/binance-spot-api-docs
- CoinMarketCap pricing: https://costbench.com/software/blockchain-data-api/coinmarketcap-api/, https://coinmarketcap.com/academy/es/article/understanding-crypto-api-subscription-models-for-traders-in-2026
- CoinDesk Data / Glassnode: https://www.spark.money/tools/crypto-api-pricing-comparison, https://comparedge.com/tools/glassnode/pricing
- Exchange fees: https://www.dextools.io/tutorials/binance-vs-coinbase-vs-kraken-best-exchange-comparison-2026, https://coingape.com/crypto-exchanges/low-fees/, https://www.spark.money/tools/crypto-exchange-fee-comparison
- Telegram limits: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits, https://docs.python-telegram-bot.org/en/stable/telegram.ext.aioratelimiter.html
- Hetzner pricing: https://kimmo.suominen.com/stuff/cpc-2026-08.txt
