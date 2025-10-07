import numpy as np
import pandas as pd
from backtest import (
    SAMPLE_CSV,
    load_prices,
    generate_signals,
    apply_strategy,
    compute_sharpe,
    compute_cagr,
    compute_max_drawdown,
)

# Expected behavior notes:
# - Signal should be based on *previous* day's return (no lookahead).
# - Fees: 10 bps applied only when position changes on that day (negative).
# - Slippage: 2 bps negative on days in position.
# - Daily returns are daily — compounding is used only when computing metrics.
# - Sharpe uses sample stdev (ddof=1) and annualizes by sqrt(252).
# - CAGR uses product of (1+r) and exponent 252/n.
# - Max drawdown computed on equity = cumprod(1+r).


def _pipeline():
    df = load_prices(SAMPLE_CSV)
    df = generate_signals(df)
    res = apply_strategy(df, fee_bps=10.0, slip_bps=2.0)
    return df, res


def test_pipeline_shapes_and_types():
    df, res = _pipeline()
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.is_monotonic_increasing
    assert "ret" in df and "signal" in df
    assert "strategy_ret_net" in res.df
    assert res.daily_net.index.equals(res.df.index[~res.df["strategy_ret_net"].isna()])


def test_no_lookahead_and_fees_slippage_signs():
    df, res = _pipeline()
    # On 2025-01-02, yesterday's ret is NaN -> signal must be 0
    assert df.loc["2025-01-02", "signal"] == 0
    # On 2025-01-03, yesterday's ret was +1% -> signal should be 1
    assert df.loc["2025-01-03", "signal"] == 1
    # Fees negative on change days, zero otherwise
    assert res.df.loc["2025-01-03", "fees"] < 0
    assert res.df.loc["2025-01-02", "fees"] == 0
    # Slippage is negative on days in position
    assert res.df.loc["2025-01-03", "slippage"] < 0


def test_metrics_values():
    _, res = _pipeline()
    r = res.daily_net.dropna()

    # Expected values computed correctly for the sample data
    # Net cumulative return
    cum = (1 + r).prod() - 1
    assert np.isclose(cum, -0.013566179261782274, atol=1e-12)

    # Sharpe
    sharpe = compute_sharpe(r, rf_annual=0.0)
    assert np.isclose(sharpe, -4.242527197813525, atol=1e-9)

    # CAGR
    cagr = compute_cagr(r)
    assert np.isclose(cagr, -0.5770577198114564, atol=1e-9)

    # Max drawdown
    mdd = compute_max_drawdown(r)
    assert np.isclose(mdd, -0.021980978217821745, atol=1e-12)
