import math
from dataclasses import dataclass
from io import StringIO
import pandas as pd
import numpy as np


SAMPLE_CSV = """date,close
2025-01-01,100
2025-01-02,101
2025-01-03,99
2025-01-04,102
2025-01-05,103
"""


@dataclass
class StrategyResult:
    df: pd.DataFrame
    daily_net: pd.Series


def load_prices(csv_text: str) -> pd.DataFrame:
    # BUG: date not parsed, index not set, dtype issues later
    df = pd.read_csv(StringIO(csv_text))
    # BUG: should sort by date and ensure monotonic index with tz-naive Timestamps
    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret"] = out["close"].pct_change()

    # BUG: look-ahead bias — using today's return to decide today's position
    out["signal"] = (out["ret"] > 0).astype(int)

    return out


def apply_strategy(df: pd.DataFrame, fee_bps: float = 10.0, slip_bps: float = 2.0) -> StrategyResult:
    out = df.copy()

    # BUG: misaligned returns if index not a DatetimeIndex
    out["strategy_ret_gross"] = out["signal"] * out["ret"]

    # Transaction costs: 10 bps when position changes
    # BUG: fee sign and timing wrong, uses per-day fee instead of per-change, and divides by 100
    pos_change = out["signal"].diff().abs().fillna(0)
    out["fees"] = - (fee_bps / 100.0) * pos_change  # should be in decimal, bps -> 1e-4

    # Slippage: 2 bps on days in position
    # BUG: applied as positive
    out["slippage"] = (slip_bps * 1e-4) * out["signal"]

    # BUG: sums returns instead of compounding — but here we want daily returns, not cumulative
    out["strategy_ret_net"] = out["strategy_ret_gross"] + out["fees"] + out["slippage"]

    return StrategyResult(df=out, daily_net=out["strategy_ret_net"].dropna())


def compute_sharpe(daily_returns: pd.Series, rf_annual: float = 0.0, periods_per_year: int = 252) -> float:
    r = daily_returns.dropna()
    if r.empty:
        return float("nan")
    # BUG: population stdev and wrong rf handling (rf per year not converted)
    excess = r - rf_annual
    return (excess.mean() / excess.std(ddof=0)) * math.sqrt(periods_per_year)


def compute_cagr(daily_returns: pd.Series, periods_per_year: int = 252) -> float:
    r = daily_returns.dropna()
    if r.empty:
        return 0.0
    # BUG: uses sum instead of product and wrong annualization exponent
    total = 1 + r.sum()
    years = len(r) / periods_per_year
    return total ** (1 / years) - 1


def compute_max_drawdown(daily_returns: pd.Series) -> float:
    r = daily_returns.dropna()
    if r.empty:
        return 0.0
    # BUG: computes drawdown from cumulative sum instead of equity curve
    cum = r.cumsum()
    running_max = cum.cummax()
    dd = cum - running_max
    return dd.min()
