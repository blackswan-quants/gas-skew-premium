"""As-of filtering that enforces D-1 temporal discipline."""

from __future__ import annotations

from datetime import date

import pandas as pd

from gasskew.exceptions import DataValidationError


def filter_as_of(df: pd.DataFrame, as_of: date, date_col: str = "trade_date") -> pd.DataFrame:
    """Keep only rows observable on or before ``as_of``.

    Parameters
    ----------
    df : pd.DataFrame
        Any time-stamped market-data frame.
    as_of : date
        Valuation date; no information dated after it may be used.
    date_col : str
        Name of the date column. If it is not a column, the index is used.

    Returns
    -------
    pd.DataFrame
        Filtered copy.

    Raises
    ------
    DataValidationError
        If the date column (or index) is not ``datetime64``.

    Notes
    -----
    Call this as the first operation of every pricing, classification and analysis
    function, so that an implicit "today" can never leak future data into a backtest.
    The dtype check matters: comparing strings to a timestamp would silently misorder
    dates such as ``"2024-10-01"`` and ``"2024-9-30"``.
    """
    stamps = df[date_col] if date_col in df.columns else df.index.to_series()
    if not pd.api.types.is_datetime64_any_dtype(stamps):
        raise DataValidationError(f"{date_col!r} must be datetime64, got {stamps.dtype}")

    cutoff = pd.Timestamp(as_of)
    keep = (stamps <= cutoff).to_numpy()
    out = df.loc[keep].copy()

    kept = stamps[keep]
    assert kept.empty or kept.max() <= cutoff, f"rows after as_of={as_of} survived filtering"
    return out
