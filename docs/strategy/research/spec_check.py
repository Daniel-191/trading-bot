"""Numbers for the proposed v1 strategy spec in ../STRATEGY_SPEC.md (scratch analysis).

Usage: python -I spec_check.py <coinmetrics btc.csv>

Runs the exact v1 rules (Option A blend, EWMA 0.97 volatility, 40% target, 10-point band) on the
research set only. Reuses the engine in learning_experiments.py, including its refusal to read
prices after RESEARCH_END, so the holdout stays unseen. This spec was already counted as a
variant there ("Option A, EWMA 0.97"); nothing here adds a new strategy variant.
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_spec = importlib.util.spec_from_file_location(
    "learning_experiments", Path(__file__).with_name("learning_experiments.py")
)
le = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(le)

MOMENTUM = (30, 60, 90, 180, 365)
BREAKOUT = (10, 20, 40, 80, 160)
EVAL = (le.EVAL_START, le.RESEARCH_END)
EXAMPLE_DATES = ("2021-04-13", "2021-06-22", "2022-06-18", "2024-03-11")


def v1_components(px: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    mom = pd.DataFrame({f"mom{n}": (px > px.shift(n)).astype(float) for n in MOMENTUM})
    brk = pd.DataFrame({f"brk{n}": le.donchian_long(px, n) for n in BREAKOUT})
    return mom, brk


def v1_target(px: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]:
    mom, brk = v1_components(px)
    signal = 0.5 * mom.mean(axis=1) + 0.5 * brk.mean(axis=1)
    vol = le.ewma_vol(px, 0.97)
    return signal, vol, le.vol_scale(signal, px, vol=vol)


def slice_stats(res: pd.DataFrame, a: str, b: str) -> dict:
    """Stats for one stretch of a single continuous run, as the live bot would experience it
    (re-simulating each period from flat would reset the rebalance band's state)."""
    r = le.daily_returns(res).loc[a:b]
    eq = np.r_[1.0, (1 + r).cumprod().values]
    years = len(r) / le.ANN
    sd = r.std()
    return {
        "CAGR": eq[-1] ** (1 / years) - 1,
        "Sharpe": r.mean() / sd * np.sqrt(le.ANN) if sd > 0 else np.nan,
        "MaxDD": (eq / np.maximum.accumulate(eq) - 1).min(),
        "Expo": res["w"].loc[a:b].mean(),
        "RT/yr": res["traded"].loc[a:b].sum() / 2 / years,
    }


def max_dd(r: np.ndarray) -> float:
    eq = np.cumprod(1 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def bootstrap_max_dd(r: pd.Series, horizon: int, reps: int = 5000, block: int = 30) -> np.ndarray:
    x = r.values
    rng = np.random.default_rng(11)
    nb = horizon // block + 1
    out = np.empty(reps)
    for k in range(reps):
        starts = rng.integers(0, len(x) - block, nb)
        idx = (starts[:, None] + np.arange(block)).ravel()[:horizon]
        out[k] = max_dd(x[idx])
    return out


def main() -> None:
    px = le.load(sys.argv[1])
    signal, vol, target = v1_target(px)
    a, b = EVAL
    sub = px.loc[a:b]
    res = le.simulate(target.loc[a:b], sub)
    r = le.daily_returns(res)

    bench = {
        "v1 strategy": target,
        "Buy & hold": pd.Series(1.0, index=px.index),
        "Buy & hold, 40% vol target (EWMA 0.97)": le.vol_scale(
            pd.Series(1.0, index=px.index), px, vol=vol
        ),
        "200-day SMA filter": (px > px.rolling(200).mean()).astype(float),
    }
    periods = {
        f"Research set {a}..{b}": (a, b),
        "2016-2017 bull": ("2016-01-01", "2017-12-31"),
        "2018 bear": ("2018-01-01", "2018-12-31"),
        "2019-2021": ("2019-01-01", "2021-12-31"),
        "2022 bear": ("2022-01-01", "2022-12-31"),
        f"2023..{b} (incl. ETF launch)": ("2023-01-01", b),
    }
    print(f"v1 spec on research data only (holdout starts after {le.RESEARCH_END})")
    print("Each strategy is one continuous run from 2016-01-01; periods are slices of it.")
    runs = {name: le.simulate(w.loc[a:b], sub) for name, w in bench.items()}
    for pname, (pa, pb) in periods.items():
        print(f"\n=== {pname} ===")
        print(le.HEADER)
        for name, out in runs.items():
            print(f"{name:<44} {le.fmt(slice_stats(out, pa, pb))}")

    print("\n=== Calendar-year returns ===")
    bh = le.daily_returns(runs["Buy & hold"])
    yearly = pd.DataFrame(
        {
            "v1": (1 + r).groupby(r.index.year).prod() - 1,
            "buy&hold": (1 + bh).groupby(bh.index.year).prod() - 1,
        }
    )
    print(yearly.map(lambda v: f"{v:+.0%}").to_string())

    print("\n=== Behaviour ===")
    w = res["w"]
    in_mkt = w > 0
    spells = (in_mkt != in_mkt.shift()).cumsum()[in_mkt]
    lengths = spells.value_counts()
    print(f"Days with any BTC held: {in_mkt.mean():.0%}")
    print(f"Average weight when invested: {w[in_mkt].mean():.0%}")
    print(f"Invested spells: {len(lengths)}, median length {lengths.median():.0f} days")
    print(f"Rebalancing trades a year: {(res['traded'] > 0).sum() / (len(res) / 365):.1f}")
    print(f"Worst day: {r.min():.1%}  Best day: {r.max():.1%}")
    yearly_vol = vol.loc[a:b].groupby(vol.loc[a:b].index.year).median().round(2)
    print(f"Median EWMA 0.97 vol by year: {yearly_vol.to_dict()}")

    print("\n=== Block-bootstrap max drawdown (30-day blocks, 5,000 resamples) ===")
    for horizon, label in ((365, "1 year"), (1095, "3 years")):
        d = bootstrap_max_dd(r.iloc[1:], horizon)
        p50, p95, p99 = np.percentile(d, [50, 5, 1])
        print(f"{label}: median {p50:.0%}, 95th pct {p95:.0%}, 99th pct {p99:.0%}")

    print("\n=== Worked examples (how the daily decision is formed) ===")
    mom, brk = v1_components(px)
    for d in EXAMPLE_DATES:
        t = pd.Timestamp(d)
        m = " ".join(f"{c[3:]}d:{int(mom.at[t, c])}" for c in mom.columns)
        k = " ".join(f"{c[3:]}d:{int(brk.at[t, c])}" for c in brk.columns)
        print(
            f"{d} close ${px.at[t]:,.0f} | momentum {m} | breakout {k} | "
            f"signal {signal.at[t]:.2f} | vol {vol.at[t]:.0%} | target weight {target.at[t]:.0%}"
        )


if __name__ == "__main__":
    main()
