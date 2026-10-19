"""Can a daily BTC trend bot improve by learning from its own results? (scratch analysis).

Usage: python -I learning_experiments.py <coinmetrics btc.csv>

Walk-forward test of "learning" schemes against a fixed, equal-weight trend ensemble. Every
scheme combines the same 14 long/flat sub-signals ("arms") and is sized and costed identically,
so the only difference is how it learns from past results. Each scheme only sees data that
would have been available at decision time.

Conventions follow btc_backtest.py (weight decided on the close of day t earns the return from
t to t+1; 0.15% per side; 10-point rebalance band; long/flat spot). All schemes are sized to a
40% volatility target, as in Option A.

Holdout: the script refuses to read prices after RESEARCH_END, so the most recent data stays
unseen for the one-time holdout test of whatever strategy we pre-register.
"""

import sys

import numpy as np
import pandas as pd

ANN = 365
COST_PER_SIDE = 0.0015
BAND = 0.10
VOL_TARGET = 0.40
RESEARCH_END = "2025-05-31"
EVAL_START = "2016-01-01"

TSMOM_LBS = (30, 60, 90, 180, 365)
DONCHIAN_LBS = (10, 20, 40, 80, 160)
SMA_LBS = (20, 50, 100, 200)


# --- data and building blocks -------------------------------------------------------------


def load(path: str) -> pd.Series:
    df = pd.read_csv(path, usecols=["time", "PriceUSD"], parse_dates=["time"])
    px = df.set_index("time")["PriceUSD"].dropna().sort_index()
    return px.loc["2013-01-01":RESEARCH_END]


def realized_vol(px: pd.Series, n: int = 30) -> pd.Series:
    return np.log(px).diff().rolling(n).std() * np.sqrt(ANN)


def donchian_long(px: pd.Series, lb: int) -> pd.Series:
    """Long on a new lb-day closing high, flat on a new lb/2-day closing low."""
    hi = px.shift(1).rolling(lb).max().values
    lo = px.shift(1).rolling(max(lb // 2, 2)).min().values
    out = np.zeros(len(px))
    pos = 0.0
    for i, p in enumerate(px.values):
        if np.isnan(hi[i]) or np.isnan(lo[i]):
            continue
        if pos == 0.0 and p >= hi[i]:
            pos = 1.0
        elif pos == 1.0 and p <= lo[i]:
            pos = 0.0
        out[i] = pos
    return pd.Series(out, index=px.index)


def build_arms(px: pd.Series) -> pd.DataFrame:
    arms = {}
    for n in TSMOM_LBS:
        arms[f"tsmom{n}"] = (px / px.shift(n) - 1 > 0).astype(float)
    for n in DONCHIAN_LBS:
        arms[f"don{n}"] = donchian_long(px, n)
    for n in SMA_LBS:
        arms[f"sma{n}"] = (px > px.rolling(n).mean()).astype(float)
    return pd.DataFrame(arms)


def vol_scale(signal: pd.Series, px: pd.Series, vol: pd.Series | None = None) -> pd.Series:
    v = realized_vol(px) if vol is None else vol
    return (signal * (VOL_TARGET / v).clip(upper=1.0)).fillna(0.0)


def simulate(target_w: pd.Series, px: pd.Series, band: float = BAND) -> pd.DataFrame:
    """Same engine as btc_backtest.py. equity[i] is the value after earning the t->t+1 return."""
    tw = target_w.reindex(px.index).fillna(0.0).clip(0, 1).values
    r = px.pct_change().shift(-1).fillna(0.0).values
    w, e = 0.0, 1.0
    eq, held, traded = np.empty(len(px)), np.empty(len(px)), np.empty(len(px))
    for i in range(len(px)):
        tgt = tw[i]
        if tgt == 0.0 or w == 0.0 or abs(tgt - w) >= band:
            dw, w = abs(tgt - w), tgt
        else:
            dw = 0.0
        e *= 1 - dw * COST_PER_SIDE
        e *= 1 + w * r[i]
        eq[i], held[i], traded[i] = e, w, dw
        w = w * (1 + r[i]) / (1 + w * r[i]) if w > 0 else 0.0
    return pd.DataFrame({"equity": eq, "w": held, "traded": traded}, index=px.index)


def daily_returns(res: pd.DataFrame) -> pd.Series:
    eq = res["equity"]
    return eq.pct_change().fillna(eq.iloc[0] - 1)


def stats(res: pd.DataFrame) -> dict:
    eq = res["equity"] / res["equity"].iloc[0]
    rets = daily_returns(res).iloc[1:]
    years = len(res) / ANN
    dd = (eq / eq.cummax() - 1).min()
    sd = rets.std()
    return {
        "CAGR": eq.iloc[-1] ** (1 / years) - 1,
        "Sharpe": rets.mean() / sd * np.sqrt(ANN) if sd > 0 else np.nan,
        "MaxDD": dd,
        "Expo": res["w"].mean(),
        "RT/yr": res["traded"].sum() / 2 / years,
    }


def paired_bootstrap(a: pd.Series, b: pd.Series, block: int = 30, reps: int = 2000) -> float:
    """Share of block-bootstrap resamples (same blocks for both) where Sharpe(a) <= Sharpe(b)."""
    ra, rb = a.values, b.values
    n = len(ra)
    rng = np.random.default_rng(7)
    nb = n // block + 1
    worse = 0
    for _ in range(reps):
        starts = rng.integers(0, n - block, nb)
        idx = (starts[:, None] + np.arange(block)).ravel()[:n]
        xa, xb = ra[idx], rb[idx]
        worse += xa.mean() / xa.std() <= xb.mean() / xb.std()
    return worse / reps


# --- learning schemes ---------------------------------------------------------------------
# Each returns a combined signal in [0, 1] indexed like px. Information discipline: the return
# an arm earns from t to t+1 is only known at t+1, so learners use arm_ret.shift(1).


def arm_net_returns(arms: pd.DataFrame, px: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        {c: daily_returns(simulate(arms[c], px, band=0.0)) for c in arms.columns}, index=px.index
    )


def trailing_sharpe(arm_ret: pd.DataFrame, window: int) -> pd.DataFrame:
    known = arm_ret.shift(1)
    m = known.rolling(window).mean()
    s = known.rolling(window).std()
    return (m / s).where(s > 0)


def hold_between_reviews(weights: pd.DataFrame, every: int) -> pd.DataFrame:
    """Only update weights every `every` days (a monthly review), holding them in between."""
    mask = np.zeros(len(weights), dtype=bool)
    mask[::every] = True
    out = weights.copy()
    out.iloc[~mask] = np.nan
    return out.ffill()


def combine(arms: pd.DataFrame, weights: pd.DataFrame) -> pd.Series:
    w = weights.fillna(0.0)
    tot = w.sum(axis=1)
    ew = arms.mean(axis=1)
    out = (arms * w).sum(axis=1) / tot.where(tot > 0)
    return out.fillna(ew)  # no usable weights yet: fall back to the fixed ensemble


def pick_best(arms: pd.DataFrame, arm_ret: pd.DataFrame, window: int, k: int = 1) -> pd.Series:
    sr = trailing_sharpe(arm_ret, window)
    rank = sr.rank(axis=1, ascending=False, method="first")
    weights = (rank <= k).astype(float)
    weights.loc[~sr.notna().all(axis=1)] = np.nan
    return combine(arms, hold_between_reviews(weights, 21))


def sharpe_weighted(arms: pd.DataFrame, arm_ret: pd.DataFrame, window: int) -> pd.Series:
    sr = trailing_sharpe(arm_ret, window)
    weights = sr.clip(lower=0.0)
    weights.loc[~sr.notna().all(axis=1)] = np.nan
    return combine(arms, hold_between_reviews(weights, 21))


def hedge(arms: pd.DataFrame, arm_ret: pd.DataFrame, eta: float) -> pd.Series:
    """Exponential weights on each arm's cumulative log return (classic online learning)."""
    cum = np.log1p(arm_ret.shift(1).fillna(0.0)).cumsum()
    z = eta * cum
    w = np.exp(z.sub(z.max(axis=1), axis=0))
    return combine(arms, w)


def recent_trades_gate(arms: pd.DataFrame, px: pd.Series, k: int) -> pd.Series:
    """Drop an arm while the mean of its last k closed trades (net of costs) is negative."""
    gated = {}
    for c in arms.columns:
        sig = arms[c].values
        p = px.values
        enabled = np.ones(len(sig))
        closed: list[float] = []
        entry = None
        for i in range(len(sig)):
            # gate for today uses only trades closed before today
            if len(closed) >= k and np.mean(closed[-k:]) <= 0:
                enabled[i] = 0.0
            prev = sig[i - 1] if i > 0 else 0.0
            if prev == 0.0 and sig[i] == 1.0:
                entry = p[i]
            elif prev == 1.0 and sig[i] == 0.0 and entry is not None:
                closed.append(p[i] / entry - 1 - 2 * COST_PER_SIDE)
                entry = None
        gated[c] = sig * enabled
    return pd.DataFrame(gated, index=arms.index).mean(axis=1)


def equity_curve_filter(base_signal: pd.Series, px: pd.Series, n: int) -> pd.Series:
    """Trade the base strategy only while its own (shadow) equity is above its n-day average."""
    shadow = simulate(vol_scale(base_signal, px), px)["equity"].shift(1)
    on = (shadow >= shadow.rolling(n).mean()).astype(float)
    return base_signal * on.fillna(1.0)


def _logit_fit(x: np.ndarray, y: np.ndarray, l2: float = 1.0) -> np.ndarray:
    xb = np.column_stack([np.ones(len(x)), x])
    beta = np.zeros(xb.shape[1])
    for _ in range(50):
        p = 1 / (1 + np.exp(-xb @ beta))
        g = xb.T @ (p - y) + l2 * np.r_[0.0, beta[1:]]
        h = xb.T @ (xb * (p * (1 - p))[:, None]) + l2 * np.diag(np.r_[0.0, np.ones(len(beta) - 1)])
        step = np.linalg.solve(h, g)
        beta -= step
        if np.abs(step).max() < 1e-8:
            break
    return beta


def meta_label_filter(base_signal: pd.Series, px: pd.Series, horizon: int = 10) -> pd.Series:
    """Walk-forward logistic 'should we take this signal?' filter, refit every quarter."""
    logp = np.log(px)
    feats = pd.DataFrame(
        {
            "strength": base_signal,
            "vol_ratio": realized_vol(px, 30) / realized_vol(px, 365),
            "dist_sma200": logp - np.log(px.rolling(200).mean()),
            "ret7": logp.diff(7),
            "ret30": logp.diff(30),
            "dd365": px / px.rolling(365).max() - 1,
        }
    )
    label = (px.shift(-horizon) / px - 1 > 0).astype(float)
    ok = feats.notna().all(axis=1) & (base_signal > 0)
    out = base_signal.copy()
    beta, mu, sd = None, None, None
    idx = px.index
    for i in range(len(idx)):
        if i % 63 == 0:
            # labels for day j are known at j + horizon; embargo one more day
            train = ok & (pd.Series(np.arange(len(idx)), index=idx) <= i - horizon - 1)
            if train.sum() >= 365:
                x = feats[train].values
                mu, sd = x.mean(axis=0), x.std(axis=0)
                beta = _logit_fit((x - mu) / sd, label[train].values)
        if beta is not None and ok.iloc[i]:
            xi = (feats.iloc[i].values - mu) / sd
            p = 1 / (1 + np.exp(-(beta[0] + xi @ beta[1:])))
            if p < 0.5:
                out.iloc[i] = 0.0
    return out


def turning_point_states(px: pd.Series) -> pd.Series:
    slow = px / px.shift(365) - 1 > 0
    fast = px / px.shift(30) - 1 > 0
    state = pd.Series("bear", index=px.index)
    state[slow & fast] = "bull"
    state[slow & ~fast] = "correction"
    state[~slow & fast] = "rebound"
    return state.where(px.shift(365).notna())


def turning_points_static(px: pd.Series) -> pd.Series:
    """Garg et al. style four-state momentum, long/flat: half size when slow and fast disagree."""
    m = {"bull": 1.0, "correction": 0.5, "rebound": 0.5, "bear": 0.0}
    return turning_point_states(px).map(m).fillna(0.0)


def turning_points_learned(px: pd.Series, min_obs: int = 250) -> pd.Series:
    """Learn from history whether each state has paid: long in a state while its mean
    next-day return so far is positive (static weights until a state has min_obs days)."""
    state = turning_point_states(px)
    nxt = px.pct_change().shift(-1)
    static = turning_points_static(px)
    out = static.copy()
    sums: dict[str, float] = {}
    counts: dict[str, int] = {}
    st, rv = state.values, nxt.values
    for i in range(len(px)):
        s = st[i]
        if isinstance(s, str) and counts.get(s, 0) >= min_obs:
            out.iloc[i] = 1.0 if sums[s] > 0 else 0.0
        # the return from i-1 to i is known now; credit it to yesterday's state
        if i > 0 and isinstance(st[i - 1], str) and not np.isnan(rv[i - 1]):
            sums[st[i - 1]] = sums.get(st[i - 1], 0.0) + rv[i - 1]
            counts[st[i - 1]] = counts.get(st[i - 1], 0) + 1
    return out


# --- volatility forecasting: a component with dense feedback ------------------------------


def ewma_vol(px: pd.Series, lam: float) -> pd.Series:
    r2 = np.log(px).diff() ** 2
    return np.sqrt(r2.ewm(alpha=1 - lam, adjust=False).mean() * ANN)


def vol_forecasts(px: pd.Series) -> dict[str, pd.Series]:
    return {
        "30d rolling (Option A)": realized_vol(px, 30),
        "90d rolling": realized_vol(px, 90),
        "EWMA 0.94": ewma_vol(px, 0.94),
        "EWMA 0.97": ewma_vol(px, 0.97),
        "Blend 30d+90d+EWMA0.97": (realized_vol(px, 30) + realized_vol(px, 90) + ewma_vol(px, 0.97))
        / 3,
    }


def qlike(real_var: pd.Series, fc_var: pd.Series) -> pd.Series:
    ratio = real_var / fc_var
    return ratio - np.log(ratio) - 1


def newey_west_t(d: pd.Series, lags: int) -> float:
    d = d.dropna().values
    n = len(d)
    u = d - d.mean()
    s = u @ u / n
    for lag in range(1, lags + 1):
        s += 2 * (1 - lag / (lags + 1)) * (u[lag:] @ u[:-lag]) / n
    return d.mean() / np.sqrt(s / n)


# --- report ---------------------------------------------------------------------------------

HEADER = f"{'scheme':<44} {'CAGR':>7} {'Sharpe':>6} {'MaxDD':>7} {'Expo':>5} {'RT/yr':>6}"


def fmt(d: dict) -> str:
    return (
        f"{d['CAGR']:>7.1%} {d['Sharpe']:>6.2f} {d['MaxDD']:>7.1%} {d['Expo']:>5.0%} "
        f"{d['RT/yr']:>6.1f}"
    )


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    px = load(sys.argv[1])
    arms = build_arms(px)
    arm_ret = arm_net_returns(arms, px)
    fixed = arms.mean(axis=1)
    option_a = (
        arms[[f"tsmom{n}" for n in TSMOM_LBS]].mean(axis=1)
        + arms[[f"don{n}" for n in DONCHIAN_LBS]].mean(axis=1)
    ) / 2

    schemes: dict[str, pd.Series] = {
        "FIXED: equal-weight 14-arm ensemble": fixed,
        "FIXED: Option A blend (TSMOM + Donchian)": option_a,
        "Pick best arm, trailing 180d Sharpe": pick_best(arms, arm_ret, 180),
        "Pick best arm, trailing 365d Sharpe": pick_best(arms, arm_ret, 365),
        "Pick best arm, trailing 730d Sharpe": pick_best(arms, arm_ret, 730),
        "Top-3 arms, trailing 365d Sharpe": pick_best(arms, arm_ret, 365, k=3),
        "Sharpe-weighted arms, trailing 365d": sharpe_weighted(arms, arm_ret, 365),
        "Hedge (exp. weights), eta=0.5": hedge(arms, arm_ret, 0.5),
        "Hedge (exp. weights), eta=2": hedge(arms, arm_ret, 2.0),
        "Hedge (exp. weights), eta=8": hedge(arms, arm_ret, 8.0),
        "Drop arm after losing trades, last 3": recent_trades_gate(arms, px, 3),
        "Drop arm after losing trades, last 5": recent_trades_gate(arms, px, 5),
        "Equity-curve filter on ensemble, 50d": equity_curve_filter(fixed, px, 50),
        "Equity-curve filter on ensemble, 100d": equity_curve_filter(fixed, px, 100),
        "Meta-label logistic filter (walk-forward)": meta_label_filter(fixed, px),
        "Turning points, static (4 states)": turning_points_static(px),
        "Turning points, learned state weights": turning_points_learned(px),
    }
    benchmarks = {
        "Buy & hold": pd.Series(1.0, index=px.index),
        "Buy & hold, vol-target 40%": pd.Series(1.0, index=px.index),
    }

    print(
        f"Data {px.index[0].date()}..{px.index[-1].date()} (research set; holdout starts after "
        f"{RESEARCH_END})  cost/side={COST_PER_SIDE:.2%} band={BAND} vol target={VOL_TARGET:.0%}"
    )
    print(f"Learning variants tested in this script: {len(schemes) - 2} (+2 fixed baselines)")

    periods = {
        f"EVALUATION {EVAL_START}..{RESEARCH_END}": (EVAL_START, None),
        "2016-2017 bull": ("2016-01-01", "2017-12-31"),
        "2018 bear": ("2018-01-01", "2018-12-31"),
        "2019-2021": ("2019-01-01", "2021-12-31"),
        "2022 bear": ("2022-01-01", "2022-12-31"),
        f"2023..{RESEARCH_END}": ("2023-01-01", None),
    }
    sized = {name: vol_scale(sig, px) for name, sig in schemes.items()}
    sized["Buy & hold"] = benchmarks["Buy & hold"]
    sized["Buy & hold, vol-target 40%"] = vol_scale(benchmarks["Buy & hold, vol-target 40%"], px)

    full_rets = {}
    for pname, (a, b) in periods.items():
        print(f"\n=== {pname} ===")
        print(HEADER)
        for name, w in sized.items():
            res = simulate(w.loc[a:b], px.loc[a:b])
            if pname.startswith("EVALUATION"):
                full_rets[name] = daily_returns(res)
            print(f"{name:<44} {fmt(stats(res))}")

    base = full_rets["FIXED: equal-weight 14-arm ensemble"]
    print(f"\n=== Each scheme vs the fixed ensemble, {EVAL_START}..{RESEARCH_END} ===")
    print("P(<=fixed): paired block bootstrap, share of resamples where the scheme's Sharpe")
    print("does not beat the fixed ensemble's. Years: live years for a Sharpe gain this size to")
    print("reach t = 2 at this correlation, 8(1 - rho) / dSharpe^2 (see the next table).")
    print(f"{'scheme':<44} {'dSharpe':>7} {'TE':>6} {'corr':>5} {'P(<=fixed)':>10} {'years':>6}")
    s_base = base.mean() / base.std() * np.sqrt(ANN)
    for name, r in full_rets.items():
        if name.startswith("FIXED: equal"):
            continue
        te = (r - base).std() * np.sqrt(ANN)
        rho = r.corr(base)
        dsr = r.mean() / r.std() * np.sqrt(ANN) - s_base
        yrs = f"{8 * (1 - rho) / dsr**2:>6.0f}" if dsr > 0 else f"{'never':>6}"
        p = paired_bootstrap(r, base)
        print(f"{name:<44} {dsr:>+7.2f} {te:>6.1%} {rho:>5.2f} {p:>10.2f} {yrs}")

    print("\n=== Plateau check on the one scheme that looked better: equity-curve filter ===")
    print(HEADER)
    for n in (20, 30, 50, 75, 100, 150, 200):
        w = vol_scale(equity_curve_filter(fixed, px, n), px).loc[EVAL_START:]
        label = f"Equity-curve filter, {n}d"
        print(f"{label:<44} {fmt(stats(simulate(w, px.loc[EVAL_START:])))}")

    print("\n=== How fast does live trading reveal a better variant? ===")
    print("Years of daily returns for the difference to reach t = 2, given the Sharpe gain")
    print("and the correlation between champion and challenger (equal volatility assumed).")
    print(f"{'dSharpe':>8} " + " ".join(f"{'rho=' + str(c):>9}" for c in (0.80, 0.90, 0.95, 0.99)))
    for dsr in (0.1, 0.2, 0.3, 0.5):
        row = [8 * (1 - rho) / dsr**2 for rho in (0.80, 0.90, 0.95, 0.99)]
        print(f"{dsr:>8.1f} " + " ".join(f"{y:>9.1f}" for y in row))

    print("\n=== Trade counts: what 'learning from trades' has to work with ===")
    ev = arms.loc[EVAL_START:]
    years = len(ev) / ANN
    entries = (ev.diff() == 1).sum()
    for c in arms.columns:
        print(f"{c:<10} {entries[c]:>4} entries in {years:.1f} years ({entries[c] / years:.1f}/yr)")
    oa = vol_scale(option_a, px).loc[EVAL_START:]
    res = simulate(oa, px.loc[EVAL_START:])
    starts = ((res["w"] > 0) & (res["w"].shift(1).fillna(0) == 0)).sum()
    print(f"Option A blend: {starts} flat-to-long entries ({starts / years:.1f}/yr)")

    print("\n=== Volatility forecasting: learning where feedback is dense ===")
    print("Target: realised vol over the next 30 days. Loss: QLIKE on variance (lower is better).")
    print("t-stat: Newey-West (30 lags) on the loss difference vs the 30d rolling estimator;")
    print("negative = better than 30d rolling.")
    real = (np.log(px).diff() ** 2).rolling(30).mean().shift(-30) * ANN
    fcs = vol_forecasts(px)
    base_loss = qlike(real, fcs["30d rolling (Option A)"] ** 2).loc[EVAL_START:]
    print(f"{'estimator':<26} {'QLIKE':>7} {'t (all)':>8} {'t (1st 1y)':>10} {'t (1st 2y)':>10}")
    for name, fc in fcs.items():
        loss = qlike(real, fc**2).loc[EVAL_START:]
        d = (loss - base_loss).dropna()
        if name.startswith("30d"):
            print(f"{name:<26} {loss.mean():>7.3f} {'-':>8} {'-':>10} {'-':>10}")
            continue
        t_all = newey_west_t(d, 30)
        t1 = newey_west_t(d.iloc[:365], 30)
        t2 = newey_west_t(d.iloc[:730], 30)
        print(f"{name:<26} {loss.mean():>7.3f} {t_all:>8.2f} {t1:>10.2f} {t2:>10.2f}")

    print("\nVol-target tracking: realised vol of buy & hold sized to 40% with each estimator")
    yrs = sorted(set(px.loc[EVAL_START:].index.year))
    print(f"{'estimator':<26} " + " ".join(f"{y:>6}" for y in yrs) + f" {'MAE':>6}")
    for name, fc in fcs.items():
        w = vol_scale(pd.Series(1.0, index=px.index), px, vol=fc)
        r = daily_returns(simulate(w, px)).loc[EVAL_START:]
        by_year = r.groupby(r.index.year).std() * np.sqrt(ANN)
        mae = (by_year - VOL_TARGET).abs().mean()
        print(f"{name:<26} " + " ".join(f"{v:>6.0%}" for v in by_year) + f" {mae:>6.1%}")

    print("\nOption A blend sized with each estimator (does better vol tracking change results?)")
    print(HEADER)
    for name, fc in fcs.items():
        w = vol_scale(option_a, px, vol=fc).loc[EVAL_START:]
        label = f"Option A, {name}"
        print(f"{label:<44} {fmt(stats(simulate(w, px.loc[EVAL_START:])))}")


if __name__ == "__main__":
    main()
