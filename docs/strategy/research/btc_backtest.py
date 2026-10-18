"""Quick daily-bar sanity backtest of candidate BTC strategies (scratch analysis, not project code).

Usage: python -I btc_backtest.py <coinmetrics btc.csv>

Conventions
- Daily close (Coin Metrics PriceUSD, 00:00 UTC). Target weight w_t is decided on the close of day t
  using data up to and including t, and earns the return from t to t+1 (BTC trades 24/7, so the
  close of t is the open of t+1). A 1-day-extra-lag variant is reported as a robustness check.
- Long-only / flat, spot, no leverage: 0 <= w <= 1. Idle USDT earns 0%.
- Costs: COST_PER_SIDE on every unit of notional traded (fee + slippage), charged on
  |w_target - w_drifted|.
- Rebalance band: vol-scaled positions only trade when the target moves >= BAND from the drifted
  weight (or goes to/from zero).
"""

import sys

import numpy as np
import pandas as pd

ANN = 365
COST_PER_SIDE = 0.0015  # 0.10% taker fee + 0.05% slippage
BAND = 0.10


def load(path: str) -> pd.Series:
    df = pd.read_csv(path, usecols=["time", "PriceUSD", "CapMVRVCur"], parse_dates=["time"])
    df = df.set_index("time").sort_index()
    return df


def realized_vol(px: pd.Series, n: int = 30) -> pd.Series:
    return np.log(px).diff().rolling(n).std() * np.sqrt(ANN)


def donchian_long(px: pd.Series, lb: int) -> pd.Series:
    """Long when close makes a new lb-day closing high, exit on a new lb/2-day closing low."""
    hi = px.shift(1).rolling(lb).max()
    lo = px.shift(1).rolling(max(lb // 2, 2)).min()
    state = np.zeros(len(px))
    pos = 0.0
    for i, (p, h, low) in enumerate(zip(px.values, hi.values, lo.values, strict=True)):
        if np.isnan(h) or np.isnan(low):
            state[i] = 0.0
            continue
        if pos == 0.0 and p >= h:
            pos = 1.0
        elif pos == 1.0 and p <= low:
            pos = 0.0
        state[i] = pos
    return pd.Series(state, index=px.index)


def rsi(px: pd.Series, n: int) -> pd.Series:
    d = px.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def connors_rsi2(px: pd.Series) -> pd.Series:
    """Buy when RSI(2) < 10 and close > SMA200; exit when close > SMA5."""
    r2 = rsi(px, 2)
    sma200 = px.rolling(200).mean()
    sma5 = px.rolling(5).mean()
    state = np.zeros(len(px))
    pos = 0.0
    for i in range(len(px)):
        p = px.iloc[i]
        if np.isnan(sma200.iloc[i]):
            continue
        if pos == 0.0 and r2.iloc[i] < 10 and p > sma200.iloc[i]:
            pos = 1.0
        elif pos == 1.0 and p > sma5.iloc[i]:
            pos = 0.0
        state[i] = pos
    return pd.Series(state, index=px.index)


def vol_scale(signal: pd.Series, px: pd.Series, target: float | None) -> pd.Series:
    if target is None:
        return signal
    scale = (target / realized_vol(px)).clip(upper=1.0)
    return (signal * scale).fillna(0.0)


def simulate(
    target_w: pd.Series,
    px: pd.Series,
    cost: float = COST_PER_SIDE,
    band: float = BAND,
    lag: int = 0,
) -> pd.DataFrame:
    tw = target_w.shift(lag).fillna(0.0).clip(0, 1).values
    r = px.pct_change().shift(-1).fillna(0.0).values  # return earned from t to t+1
    n = len(px)
    w = 0.0
    eq = np.empty(n)
    held = np.empty(n)
    traded = np.empty(n)
    e = 1.0
    for i in range(n):
        tgt = tw[i]
        if tgt == 0.0 or w == 0.0 or abs(tgt - w) >= band:
            dw = abs(tgt - w)
            w = tgt
        else:
            dw = 0.0
        e *= 1 - dw * cost
        traded[i] = dw
        held[i] = w
        e *= 1 + w * r[i]
        eq[i] = e
        w = w * (1 + r[i]) / (1 + w * r[i]) if w > 0 else 0.0
    return pd.DataFrame({"equity": eq, "w": held, "traded": traded}, index=px.index)


def stats(res: pd.DataFrame) -> dict:
    eq = res["equity"]
    rets = eq.pct_change().fillna(eq.iloc[0] - 1)
    years = len(eq) / ANN
    cagr = eq.iloc[-1] ** (1 / years) - 1
    vol = rets.std() * np.sqrt(ANN)
    sharpe = rets.mean() / rets.std() * np.sqrt(ANN) if rets.std() > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    return {
        "CAGR": cagr,
        "Vol": vol,
        "Sharpe": sharpe,
        "MaxDD": dd,
        "Calmar": cagr / abs(dd) if dd < 0 else np.nan,
        "Exposure": res["w"].mean(),
        "RT/yr": res["traded"].sum() / 2 / years,
        "Mult": eq.iloc[-1],
    }


def block_bootstrap_sharpe_diff(
    a: pd.Series, b: pd.Series, block: int = 30, reps: int = 2000
) -> float:
    """Share of stationary-ish block-bootstrap resamples where Sharpe(a) <= Sharpe(b)."""
    ra = a.pct_change().fillna(0).values
    rb = b.pct_change().fillna(0).values
    n = len(ra)
    rng = np.random.default_rng(7)
    worse = 0
    nb = n // block + 1
    for _ in range(reps):
        starts = rng.integers(0, n - block, nb)
        idx = (starts[:, None] + np.arange(block)).ravel()[:n]
        xa, xb = ra[idx], rb[idx]
        sa = xa.mean() / xa.std()
        sb = xb.mean() / xb.std()
        worse += sa <= sb
    return worse / reps


def build_strategies(df: pd.DataFrame) -> dict[str, pd.Series]:
    px = df["PriceUSD"]
    mvrv = df["CapMVRVCur"]
    ones = pd.Series(1.0, index=px.index)
    sma200 = (px > px.rolling(200).mean()).astype(float)
    ma_ens = pd.concat(
        [(px > px.rolling(n).mean()).astype(float) for n in (20, 50, 100, 200)], axis=1
    ).mean(axis=1)
    tsmom = pd.concat(
        [(px / px.shift(n) - 1 > 0).astype(float) for n in (30, 60, 90, 180, 365)], axis=1
    ).mean(axis=1)
    don = pd.concat([donchian_long(px, n) for n in (10, 20, 40, 80, 160)], axis=1).mean(axis=1)
    rsi2 = connors_rsi2(px)
    mvrv_cap = (mvrv < 3.0).astype(float)
    return {
        "Buy & hold": ones,
        "Buy & hold, vol-target 40%": vol_scale(ones, px, 0.40),
        "200d SMA filter": sma200,
        "MA ensemble (20/50/100/200)": ma_ens,
        "TSMOM ensemble (30-365d)": tsmom,
        "Donchian ensemble (10-160d)": don,
        "Donchian ensemble, vol-target 40%": vol_scale(don, px, 0.40),
        "Donchian ensemble, vol-target 25%": vol_scale(don, px, 0.25),
        "TSMOM ensemble, vol-target 40%": vol_scale(tsmom, px, 0.40),
        "RSI(2) dip-buy above 200d SMA": rsi2,
        "Buy & hold, flat when MVRV>3": mvrv_cap,
        "Donchian ens. + RSI2 dips (max)": pd.concat([don, rsi2], axis=1).max(axis=1),
    }


def fmt(d: dict) -> str:
    return (
        f"{d['CAGR']:>7.1%} {d['Vol']:>6.1%} {d['Sharpe']:>6.2f} {d['MaxDD']:>7.1%} "
        f"{d['Calmar']:>6.2f} {d['Exposure']:>6.0%} {d['RT/yr']:>6.1f} {d['Mult']:>9.1f}x"
    )


HEADER = (
    f"{'strategy':<36} {'CAGR':>7} {'Vol':>6} {'Sharpe':>6} {'MaxDD':>7} {'Calmar':>6} "
    f"{'Expo':>6} {'RT/yr':>6} {'Mult':>10}"
)


def main() -> None:
    df = load(sys.argv[1]).dropna(subset=["PriceUSD"])
    df = df.loc["2013-01-01":]
    strats = build_strategies(df)
    px = df["PriceUSD"]
    print(
        f"Data: {df.index[0].date()} to {df.index[-1].date()}  "
        f"cost/side={COST_PER_SIDE:.2%} band={BAND}"
    )

    periods = {
        "FULL 2015-01-01 to end": ("2015-01-01", None),
        "Binance era 2017-08-17 to end": ("2017-08-17", None),
        "2018 bear (2018-01-01..2018-12-31)": ("2018-01-01", "2018-12-31"),
        "2019-2021 (incl. Covid crash, bull)": ("2019-01-01", "2021-12-31"),
        "2022 bear": ("2022-01-01", "2022-12-31"),
        "2023-01-01 to end": ("2023-01-01", None),
        "ETF era 2024-01-11 to end": ("2024-01-11", None),
    }
    results = {}
    for pname, (a, b) in periods.items():
        print(f"\n=== {pname} ===")
        print(HEADER)
        sub_px = px.loc[a:b]
        for name, sig in strats.items():
            res = simulate(sig.loc[a:b], sub_px)
            results[(pname, name)] = res
            print(f"{name:<36} {fmt(stats(res))}")

    full = "FULL 2015-01-01 to end"
    print("\n=== Robustness on FULL period ===")
    base_bh_vt = results[(full, "Buy & hold, vol-target 40%")]["equity"]
    base_bh = results[(full, "Buy & hold")]["equity"]
    for name in [
        "200d SMA filter",
        "MA ensemble (20/50/100/200)",
        "TSMOM ensemble (30-365d)",
        "Donchian ensemble (10-160d)",
        "Donchian ensemble, vol-target 40%",
        "TSMOM ensemble, vol-target 40%",
        "RSI(2) dip-buy above 200d SMA",
    ]:
        sig = strats[name].loc["2015-01-01":]
        sub = px.loc["2015-01-01":]
        lag = stats(simulate(sig, sub, lag=1))
        hi = stats(simulate(sig, sub, cost=0.003))
        lo = stats(simulate(sig, sub, cost=0.0005))
        eq = results[(full, name)]["equity"]
        p_bh = block_bootstrap_sharpe_diff(eq, base_bh)
        p_vt = block_bootstrap_sharpe_diff(eq, base_bh_vt)
        print(
            f"{name:<36} +1d lag Sharpe {lag['Sharpe']:.2f} | cost 0.05%/side {lo['Sharpe']:.2f} "
            f"| 0.30%/side {hi['Sharpe']:.2f} | P(Sharpe<=B&H) {p_bh:.2f} "
            f"| P(Sharpe<=VT B&H) {p_vt:.2f}"
        )

    print("\n=== Parameter plateau, FULL period: single SMA filter length ===")
    sub = px.loc["2013-01-01":]
    for n in (20, 30, 50, 75, 100, 125, 150, 200, 250, 300):
        sig = (sub > sub.rolling(n).mean()).astype(float)
        s = stats(simulate(sig.loc["2015-01-01":], px.loc["2015-01-01":]))
        print(f"SMA {n:>3}: {fmt(s)}")

    print("\n=== Parameter plateau, FULL period: single Donchian lookback (exit = lb/2) ===")
    for n in (10, 20, 30, 40, 60, 80, 120, 160, 250):
        sig = donchian_long(sub, n)
        s = stats(simulate(sig.loc["2015-01-01":], px.loc["2015-01-01":]))
        print(f"Donchian {n:>3}: {fmt(s)}")

    print("\n=== MVRV context ===")
    m = df["CapMVRVCur"].dropna()
    for a, b in [("2017-01-01", "2018-12-31"), ("2020-01-01", "2022-12-31"), ("2023-01-01", None)]:
        mm = m.loc[a:b]
        print(
            f"MVRV {a}..{b or 'end'}: max {mm.max():.2f} on {mm.idxmax().date()}, "
            f"min {mm.min():.2f}"
        )

    print("\n=== Realised BTC vol (30d, annualised) by year: median ===")
    rv = realized_vol(px)
    print(rv.groupby(rv.index.year).median().loc[2015:].round(2).to_string())


if __name__ == "__main__":
    main()
