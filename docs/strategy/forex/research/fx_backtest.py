"""Daily sanity backtest of candidate G10 FX strategies (scratch research code, not project code).

Usage (from the notes folder):
    uv run --no-project --with pandas --with numpy python -I fx_backtest.py \
        data/fx_daily.csv data/rates

Data
- data/fx_daily.csv: datasets/exchange-rates mirror of FRED H.10 daily noon New York buying
  rates. Every value is foreign-currency units per USD (the build script inverts AUD, EUR, NZD,
  GBP). US holidays are present as blank rows.
- data/rates/: FRED/OECD monthly 3-month interbank rates (IR3TIB01xxM156N, monthly averages, %
  p.a.), Japan call rate IRSTCI01JPM156N (used before IR3TIB JPY starts in 2002-04), ECB deposit
  rate ECBDFR and SONIA IUDSOIA (used only to extend EUR and GBP after their 3m series stop).

Conventions
- Universe: EUR JPY GBP CHF AUD NZD CAD SEK NOK, each vs USD. P = USD price of one unit of the
  foreign currency. A weight w_i > 0 means long currency i vs USD (e.g. long EURUSD, short USDJPY).
- Weights are decided on the H.10 fixing of day t (noon New York) and earn the move from t to t+1.
  A variant with one extra day of lag is reported.
- P&L per day = sum_i w_i * (spot return_i + financing_i) - markup - spread costs, where
  financing_i = (r_i - r_USD) * days / 365 (calendar days, so weekends accrue) and the broker's
  markup = MARKUP * |w_i| * days / 365 on every open leg. Unfunded positions: margin cash earns 0.
- Spread + slippage: RT_PIPS round-trip pips per pair (half charged per side) converted to a
  fraction of the quoted market price on the trade date, charged on |delta w|.
- Volatility: EWMA std of daily log returns, centre of mass 60 days (Moskowitz-Ooi-Pedersen style),
  annualised. Per-pair risk weight = 10% / sigma_i. Multi-pair strategies are then scaled at the
  portfolio level to a 10% ex-ante vol (same EWMA on the strategy's own unscaled returns), with the
  scale capped at MAX_SCALE. Monthly strategies only update weights and scale at month-ends.
- All parameters were fixed before the first run and were not changed after seeing results.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CCYS = ["EUR", "JPY", "GBP", "CHF", "AUD", "NZD", "CAD", "SEK", "NOK"]
COUNTRY = {
    "EUR": "Euro",
    "JPY": "Japan",
    "GBP": "United Kingdom",
    "CHF": "Switzerland",
    "AUD": "Australia",
    "NZD": "New Zealand",
    "CAD": "Canada",
    "SEK": "Sweden",
    "NOK": "Norway",
}
# Market convention: True if the pair is quoted XXXUSD (USD per unit), else USDXXX.
XXXUSD = {"EUR": True, "GBP": True, "AUD": True, "NZD": True}
PIP = {c: (0.01 if c == "JPY" else 0.0001) for c in CCYS}
# Baseline all-in round-trip cost (spread + slippage) in pips for a retail standard account.
RT_PIPS = {
    "EUR": 1.0,
    "JPY": 1.2,
    "GBP": 1.8,
    "CHF": 1.8,
    "AUD": 1.3,
    "NZD": 2.0,
    "CAD": 1.8,
    "SEK": 50.0,
    "NOK": 50.0,
}
RATE_FILE = {
    "USD": "IR3TIB01USM156N",
    "EUR": "IR3TIB01EZM156N",
    "JPY": "IR3TIB01JPM156N",
    "GBP": "IR3TIB01GBM156N",
    "CHF": "IR3TIB01CHM156N",
    "AUD": "IR3TIB01AUM156N",
    "NZD": "IR3TIB01NZM156N",
    "CAD": "IR3TIB01CAM156N",
    "SEK": "IR3TIB01SEM156N",
    "NOK": "IR3TIB01NOM156N",
}
MARKUP = 0.01  # retail financing markup, per year, on each open USD-pair leg
TARGET = 0.10  # annualised vol target per pair and per portfolio
VOL_COM = 60
MAX_SCALE = 4.0
START = "2000-01-03"
BOOT_REPS = 2000


# ----------------------------------------------------------------------------- data
def load_fx(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = ["Date", "Country", "Rate"]
    df["Date"] = pd.to_datetime(df["Date"])
    wide = df.pivot(index="Date", columns="Country", values="Rate")
    wide = wide[[COUNTRY[c] for c in CCYS]]
    wide.columns = CCYS
    wide = wide.loc["1999-01-01":].astype(float)
    return wide  # foreign currency per USD, with NaN on holidays


def read_fred(path: Path) -> pd.Series:
    s = pd.read_csv(path, na_values=["."])
    s.columns = ["date", "v"]
    s["date"] = pd.to_datetime(s["date"])
    return s.set_index("date")["v"].astype(float).dropna()


def load_rates(rdir: str, end: pd.Timestamp) -> tuple[pd.DataFrame, list[str]]:
    d = Path(rdir)
    notes = []
    m = pd.DataFrame({c: read_fred(d / f"{f}.csv") for c, f in RATE_FILE.items()})
    m.index = m.index.to_period("M")
    # JPY: 3m interbank starts 2002-04; use the call rate before that.
    call = read_fred(d / "IRSTCI01JPM156N.csv")
    call.index = call.index.to_period("M")
    first = m["JPY"].first_valid_index()
    m.loc[m.index < first, "JPY"] = call.reindex(m.index[m.index < first])
    notes.append(f"JPY before {first}: Japan call rate IRSTCI01JPM156N")
    # EUR and GBP: extend after the 3m series stops with policy/overnight rate + last spread.
    for c, f in (("EUR", "ECBDFR"), ("GBP", "IUDSOIA")):
        o = read_fred(d / f"{f}.csv")
        om = o.groupby(o.index.to_period("M")).mean()
        last = m[c].last_valid_index()
        spread = m.loc[last, c] - om.loc[last]
        months = pd.period_range(last + 1, end.to_period("M"), freq="M")
        ext = om.reindex(months) + spread
        m = m.reindex(m.index.union(months))
        m.loc[months, c] = ext.values
        notes.append(f"{c} after {last}: {f} monthly mean + {spread:+.3f}pp spread")
    full = pd.period_range("1999-01", end.to_period("M"), freq="M")
    last_obs = {c: str(m[c].last_valid_index()) for c in m.columns}
    m = m.reindex(full).ffill()
    notes.append(f"last observed month per series (then forward-filled): {last_obs}")
    return m, notes


# ----------------------------------------------------------------------------- helpers
def ewm_vol(r: pd.DataFrame | pd.Series, ann: float) -> pd.DataFrame | pd.Series:
    return r.ewm(com=VOL_COM, min_periods=VOL_COM).std() * np.sqrt(ann)


def month_end_flags(idx: pd.DatetimeIndex) -> pd.Series:
    per = idx.to_period("M")
    nxt = pd.Series(per, index=idx).shift(-1)
    return pd.Series(per, index=idx) != nxt


def donchian_ls(px: pd.Series, lb: int) -> pd.Series:
    """Long on a new lb-day closing high, short on a new lb-day closing low; exit a long on a new
    lb/2-day low and a short on a new lb/2-day high (Turtle-style, closes only)."""
    hi = px.shift(1).rolling(lb).max().values
    lo = px.shift(1).rolling(lb).min().values
    xhi = px.shift(1).rolling(lb // 2).max().values
    xlo = px.shift(1).rolling(lb // 2).min().values
    out = np.zeros(len(px))
    pos = 0.0
    for i, p in enumerate(px.values):
        if np.isnan(hi[i]):
            continue
        if pos == 1.0 and p <= xlo[i] or pos == -1.0 and p >= xhi[i]:
            pos = 0.0
        if p >= hi[i]:
            pos = 1.0
        elif p <= lo[i]:
            pos = -1.0
        out[i] = pos
    return pd.Series(out, index=px.index)


def rsi(px: pd.Series, n: int) -> pd.Series:
    d = px.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def rsi2_fade(px: pd.Series) -> pd.Series:
    """Long when RSI(2) < 10 until RSI(2) > 50; short when RSI(2) > 90 until RSI(2) < 50."""
    r = rsi(px, 2).values
    out = np.zeros(len(px))
    pos = 0.0
    for i in range(len(px)):
        if np.isnan(r[i]):
            continue
        if pos == 1.0 and r[i] > 50 or pos == -1.0 and r[i] < 50:
            pos = 0.0
        if pos == 0.0:
            if r[i] < 10:
                pos = 1.0
            elif r[i] > 90:
                pos = -1.0
        out[i] = pos
    return pd.Series(out, index=px.index)


# ----------------------------------------------------------------------------- engine
class Market:
    def __init__(self, fx: pd.DataFrame, rates_m: pd.DataFrame):
        fx = fx.dropna(how="all")
        bad = fx.isna().any(axis=1)
        self.partial_missing = int(bad.sum())
        fx = fx.loc[~bad]
        self.S = fx  # foreign per USD
        self.P = 1.0 / fx  # USD per foreign unit
        self.idx = fx.index
        self.ann = len(fx.loc["2000":"2025"]) / 26.0
        self.R = self.P.pct_change()
        self.logR = np.log(self.P).diff()
        days = pd.Series(self.idx, index=self.idx).diff().dt.days
        self.days = days
        per = self.idx.to_period("M")
        rd = rates_m.reindex(per)
        rd.index = self.idx
        self.rates_daily = rd  # rate of the holding month (monthly average), % p.a.
        # carry earned from t-1 to t, labelled t, uses the rate of the month of t-1
        diff = rd[CCYS].sub(rd["USD"], axis=0) / 100.0
        self.carry = diff.shift(1).mul(days / 365.0, axis=0)
        mkt = pd.DataFrame({c: (fx[c] if not XXXUSD.get(c) else 1.0 / fx[c]) for c in CCYS})
        self.costfrac = pd.DataFrame(
            {c: RT_PIPS[c] / 2.0 * PIP[c] / mkt[c] for c in CCYS}, index=self.idx
        )
        self.vol = ewm_vol(self.logR, self.ann)
        # lagged rate for signals: month m-1 average, available at the month-m rebalance
        lag = rates_m.shift(1).reindex(per)
        lag.index = self.idx
        self.rates_signal = lag
        self.month_end = month_end_flags(self.idx)


def simulate(
    mk: Market,
    W: pd.DataFrame,
    lag: int = 0,
    cost_mult: float = 1.0,
    markup: float = MARKUP,
    financing: bool = True,
) -> pd.DataFrame:
    W = W.reindex(mk.idx).fillna(0.0)
    if lag:
        W = W.shift(lag).fillna(0.0)
    Wp = W.shift(1).fillna(0.0)  # weights held over (t-1, t]
    spot = (Wp * mk.R.fillna(0.0)).sum(axis=1)
    fin = (Wp * mk.carry.fillna(0.0)).sum(axis=1) if financing else spot * 0.0
    mku = Wp.abs().sum(axis=1) * markup * mk.days.fillna(0.0) / 365.0 if financing else spot * 0.0
    dW = (W - Wp).abs()
    tc_t = (dW * mk.costfrac).sum(axis=1) * cost_mult  # paid at t when trading
    net = spot + fin - mku - tc_t
    return pd.DataFrame(
        {
            "net": net,
            "spot": spot,
            "fin": fin,
            "markup": mku,
            "tc": tc_t,
            "turn": dW.sum(axis=1),
            "gross": W.abs().sum(axis=1),
        }
    )


def port_scale(mk: Market, Wraw: pd.DataFrame, monthly: bool) -> pd.DataFrame:
    """Scale raw weights to a 10% ex-ante portfolio vol using the EWMA vol of their own returns."""
    p = (Wraw.shift(1) * mk.R).sum(axis=1)
    p[Wraw.shift(1).abs().sum(axis=1) == 0] = np.nan
    sig = p.ewm(com=VOL_COM, min_periods=VOL_COM).std() * np.sqrt(mk.ann)
    scale = (TARGET / sig).clip(upper=MAX_SCALE)
    if monthly:
        scale = scale.where(mk.month_end).ffill()
    return Wraw.mul(scale.fillna(0.0), axis=0)


def hold_monthly(mk: Market, Wme: pd.DataFrame) -> pd.DataFrame:
    return Wme.where(mk.month_end, np.nan).ffill().fillna(0.0)


def rank_top_bottom(score: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """score includes a USD column; returns weights for CCYS (+1/k top k, -1/k bottom k)."""
    W = pd.DataFrame(0.0, index=score.index, columns=CCYS)
    valid = score.notna().all(axis=1)
    for t in score.index[valid]:
        s = score.loc[t].sort_values()
        for c in s.index[-k:]:
            if c != "USD":
                W.loc[t, c] += 1.0 / k
        for c in s.index[:k]:
            if c != "USD":
                W.loc[t, c] -= 1.0 / k
    return W


def build(mk: Market) -> dict[str, pd.DataFrame]:
    P = mk.P
    k = TARGET / mk.vol  # per-pair 10% risk weights
    n = len(CCYS)
    out = {}

    sig = sum(np.sign(P / P.shift(L) - 1.0) for L in (21, 63, 126, 252)) / 4.0
    sig = sig.where(P.shift(252).notna())
    out["(a) TSMOM ens 1/3/6/12m, VT10"] = port_scale(mk, (sig * k / n).fillna(0.0), False)

    don = pd.DataFrame(
        {c: sum(donchian_ls(P[c], lb) for lb in (20, 55, 100, 200)) / 4.0 for c in CCYS}
    )
    out["(b) Donchian ens 20/55/100/200, VT10"] = port_scale(mk, (don * k / n).fillna(0.0), False)

    for L, tag in ((63, "3m"), (252, "12m")):
        mom = (P / P.shift(L) - 1.0).copy()
        mom["USD"] = 0.0
        mom.loc[~P.shift(L).notna().all(axis=1)] = np.nan
        me = rank_top_bottom(mom.loc[mk.month_end])
        Wm = hold_monthly(mk, me.reindex(mk.idx))
        out[f"(c) XS momentum {tag} top3/bottom3, VT10"] = port_scale(mk, Wm, True)

    rs = mk.rates_signal[["USD"] + CCYS]
    me = rank_top_bottom(rs.loc[mk.month_end])
    Wc = hold_monthly(mk, me.reindex(mk.idx))
    out["(d) G10 carry top3/bottom3, unscaled"] = Wc
    out["(d) G10 carry top3/bottom3, VT10"] = port_scale(mk, Wc, True)

    pe = P["EUR"]
    w5 = -np.sign(pe / pe.shift(5) - 1.0) * k["EUR"]
    out["(e1) EURUSD 5d reversal, VT10"] = pd.DataFrame({"EUR": w5}).fillna(0.0)
    w_rsi = rsi2_fade(pe) * k["EUR"]
    out["(e2) EURUSD RSI(2) 10/90 fade, VT10"] = pd.DataFrame({"EUR": w_rsi}).fillna(0.0)

    combo = (
        0.5 * out["(a) TSMOM ens 1/3/6/12m, VT10"] + 0.5 * out["(d) G10 carry top3/bottom3, VT10"]
    )
    out["(f) 50/50 (a)+(d), VT10"] = port_scale(mk, combo, False)

    usd = pd.DataFrame(-1.0 / n, index=mk.idx, columns=CCYS)
    out["Bench: long USD basket, unscaled"] = usd
    out["Bench: long USD basket, VT10"] = port_scale(mk, usd, False)
    return out


# ----------------------------------------------------------------------------- reporting
def stats(res: pd.DataFrame, ann: float) -> dict:
    r = res["net"]
    eq = (1 + r).cumprod()
    yrs = len(r) / ann
    sd = r.std()
    m = r.groupby(r.index.to_period("M")).apply(lambda x: (1 + x).prod() - 1)
    return {
        "CAGR": eq.iloc[-1] ** (1 / yrs) - 1,
        "Vol": sd * np.sqrt(ann),
        "Sharpe": r.mean() / sd * np.sqrt(ann) if sd > 0 else np.nan,
        "MaxDD": (eq / eq.cummax() - 1).min(),
        "Lev": res["gross"].mean(),
        "RT": res["turn"].sum() / 2 / yrs,
        "TC": res["tc"].sum() / yrs,
        "Fin": res["fin"].sum() / yrs,
        "Mku": res["markup"].sum() / yrs,
        "WorstD": r.min(),
        "WorstM": m.min(),
    }


HDR = (
    f"{'strategy':<40} {'CAGR':>6} {'Vol':>5} {'Shrp':>5} {'MaxDD':>6} {'Lev':>4} {'RT/yr':>6} "
    f"{'Sprd':>5} {'Carry':>6} {'Mkup':>5} {'WrstD':>6} {'WrstM':>6}"
)


def fmt(d: dict) -> str:
    return (
        f"{d['CAGR']:>6.1%} {d['Vol']:>5.1%} {d['Sharpe']:>5.2f} {d['MaxDD']:>6.1%} "
        f"{d['Lev']:>4.1f} {d['RT']:>6.1f} {d['TC']:>5.2%} {d['Fin']:>+6.2%} {d['Mku']:>5.2%} "
        f"{d['WorstD']:>6.1%} {d['WorstM']:>6.1%}"
    )


def boot_p(r: pd.Series, block: int, reps: int = BOOT_REPS, seed: int = 11) -> float:
    """Circular block bootstrap: share of resamples with Sharpe <= 0 (rough one-sided p)."""
    x = r.values
    n = len(x)
    rng = np.random.default_rng(seed)
    nb = n // block + 1
    worse = 0
    for _ in range(reps):
        st = rng.integers(0, n, nb)
        idx = ((st[:, None] + np.arange(block)) % n).ravel()[:n]
        xs = x[idx]
        worse += xs.mean() / xs.std() <= 0
    return worse / reps


def main() -> None:
    fx = load_fx(sys.argv[1])
    rates_m, notes = load_rates(sys.argv[2], fx.dropna(how="all").index[-1])
    mk = Market(fx, rates_m)
    print(
        f"FX data: {mk.idx[0].date()} to {mk.idx[-1].date()}, {len(mk.idx)} fixing days, "
        f"{mk.ann:.1f} obs/yr; dates with a partial-missing row dropped: {mk.partial_missing}"
    )
    for n_ in notes:
        print("Rates:", n_)
    print("Baseline round-trip cost (pips) and as bp of price on the last date:")
    print(
        "  "
        + "  ".join(f"{c}:{RT_PIPS[c]:g}p={2 * mk.costfrac[c].iloc[-1] * 1e4:.2f}bp" for c in CCYS)
    )
    print(f"Financing: rate differential of the holding month minus {MARKUP:.1%}/yr markup per leg")

    print("\n=== Data check: largest one-day moves of each currency vs USD (USD price) ===")
    for c in CCYS:
        r = mk.R[c].dropna()
        lo, hi = r.idxmin(), r.idxmax()
        print(
            f"{c}: min {r[lo]:+.2%} on {lo.date()}  max {r[hi]:+.2%} on {hi.date()}  "
            f"ann.vol {r.std() * np.sqrt(mk.ann):.1%}"
        )

    print("\n=== 3m rates used (annual averages, % p.a.) ===")
    ra = rates_m.copy()
    ra.index = ra.index.to_timestamp()
    print(ra.loc["2000":].groupby(ra.loc["2000":].index.year).mean().round(2).to_string())

    strats = build(mk)
    full = {name: simulate(mk, W).loc[START:] for name, W in strats.items()}

    periods = {
        f"FULL {START} to {mk.idx[-1].date()}": (START, None),
        "pre-2008 (2000-01-03..2007-12-31)": (START, "2007-12-31"),
        "2008-2014": ("2008-01-01", "2014-12-31"),
        "2015-2021": ("2015-01-01", "2021-12-31"),
        "2022-2026 (to end)": ("2022-01-01", None),
    }
    for pname, (a, b) in periods.items():
        print(f"\n=== {pname} ===")
        print(HDR)
        for name, res in full.items():
            print(f"{name:<40} {fmt(stats(res.loc[a:b], mk.ann))}")

    print("\n=== Calendar-year net returns ===")
    years = [2008, 2015, 2022, 2024, 2025, 2026]
    print(f"{'strategy':<40} " + " ".join(f"{y:>7}" for y in years))
    for name, res in full.items():
        yr = res["net"].groupby(res.index.year).apply(lambda x: (1 + x).prod() - 1)
        print(f"{name:<40} " + " ".join(f"{yr.get(y, np.nan):>7.1%}" for y in years))
    print("(2026 = year to date)")

    print("\n=== Robustness on FULL period (Sharpe) and block-bootstrap P(Sharpe<=0) ===")
    print(
        f"{'strategy':<40} {'base':>5} {'+1lag':>6} {'c0.5x':>6} {'c2x':>6} {'mk0':>6} "
        f"{'mk2%':>6} {'spot':>6} {'frict0':>6} {'t':>5} {'p(21d)':>7} {'p(63d)':>7}"
    )
    for name, W in strats.items():
        base = full[name]
        sh = lambda res: stats(res.loc[START:], mk.ann)["Sharpe"]  # noqa: E731
        s0 = sh(base)
        row = [
            s0,
            sh(simulate(mk, W, lag=1)),
            sh(simulate(mk, W, cost_mult=0.5)),
            sh(simulate(mk, W, cost_mult=2.0)),
            sh(simulate(mk, W, markup=0.0)),
            sh(simulate(mk, W, markup=0.02)),
            sh(simulate(mk, W, cost_mult=0.0, financing=False)),
            sh(simulate(mk, W, cost_mult=0.0, markup=0.0)),
        ]
        yrs = len(base) / mk.ann
        p21 = boot_p(base["net"], 21)
        p63 = boot_p(base["net"], 63)
        print(
            f"{name:<40} "
            + " ".join(f"{v:>6.2f}" for v in row)
            + f" {s0 * np.sqrt(yrs):>5.2f} {p21:>7.3f} {p63:>7.3f}"
        )
    print(
        "cols: base | one extra day of lag | spread cost x0.5 | x2 | markup 0 | markup 2%/yr | "
        "spot only (no carry, no markup, no spread) | frictionless (spot + carry, no costs) | "
        "t = Sharpe*sqrt(yrs)"
    )

    print("\n=== Correlation of daily net returns, FULL period ===")
    codes = ["a", "b", "c3", "c12", "d_raw", "d", "e1", "e2", "f", "usd_raw", "usd"]
    cm = pd.DataFrame({c_: r["net"] for c_, r in zip(codes, full.values(), strict=True)}).corr()
    print(cm.round(2).to_string())
    print(
        "codes in table order: "
        + ", ".join(f"{c_}={n_}" for c_, n_ in zip(codes, full, strict=True))
    )

    print("\n=== Tail windows: cumulative net return ===")
    windows = {
        "GFC Sep-Dec 2008": ("2008-09-01", "2008-12-31"),
        "SNB 2015-01-15 (day)": ("2015-01-15", "2015-01-15"),
        "SNB week 2015-01-12..16": ("2015-01-12", "2015-01-16"),
        "Brexit 2016-06-24 (day)": ("2016-06-24", "2016-06-24"),
        "Covid Mar 2020": ("2020-03-01", "2020-03-31"),
        "Yen unwind 2024-07-10..08-05": ("2024-07-10", "2024-08-05"),
    }
    print(f"{'strategy':<40} " + " ".join(f"{k_[:12]:>12}" for k_ in windows))
    for name, res in full.items():
        vals = []
        for a, b in windows.values():
            x = res["net"].loc[a:b]
            vals.append((1 + x).prod() - 1)
        print(f"{name:<40} " + " ".join(f"{v:>12.1%}" for v in vals))

    print("\n=== Carry portfolio composition (share of month-ends long / short, FULL) ===")
    Wc = strats["(d) G10 carry top3/bottom3, unscaled"].loc[START:]
    me = Wc.loc[mk.month_end.loc[START:]]
    rs = mk.rates_signal.loc[START:][["USD"] + CCYS].loc[mk.month_end.loc[START:]]
    usd_long = (rs.rank(axis=1, ascending=False)["USD"] <= 3).mean()
    usd_short = (rs.rank(axis=1, ascending=True)["USD"] <= 3).mean()
    print(
        "long : " + " ".join(f"{c}:{(me[c] > 0).mean():.0%}" for c in CCYS) + f" USD:{usd_long:.0%}"
    )
    print(
        "short: "
        + " ".join(f"{c}:{(me[c] < 0).mean():.0%}" for c in CCYS)
        + f" USD:{usd_short:.0%}"
    )
    rsd = mk.rates_signal.loc[me.index]
    gross_diff = (rsd[CCYS].sub(rsd["USD"], axis=0) / 100 * me).sum(axis=1)
    print(
        f"Ex-ante rate differential of the unscaled carry book, mean {gross_diff.mean():.2%}/yr; "
        f"by year: "
        + " ".join(
            f"{y}:{v:.1%}" for y, v in gross_diff.groupby(gross_diff.index.year).mean().items()
        )
    )

    print("\n=== Position sign changes per pair per year (FULL; signal turnover diagnostic) ===")
    for name, W in strats.items():
        Ws = np.sign(W.loc[START:])
        flips = (Ws.diff().abs() > 0).sum() / (len(Ws) / mk.ann)
        active = flips[Ws.abs().sum() > 0]
        print(f"{name:<40} {active.mean():>5.1f}")

    print(
        "\nVariants: 9 strategy variants [(a), (b), (c)x2, (d)x2, (e1), (e2), (f)] + 2 benchmarks; "
        "the robustness columns are sensitivities of those, not extra selections. "
        "No parameter was tuned on this data."
    )


if __name__ == "__main__":
    main()
