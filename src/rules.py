"""Rule evaluation and suspicion scoring engine.

Implements Sections 11 through 18 of the project brief:
- Rule 1: Unusual Amount (Statistical 3-Sigma and 99th Percentile)
- Rule 2: Late-Night Window (23:00 to 05:59)
- Rule 3: High-Frequency Window (Rolling 1-Hour Count >= 5)
- Suspicion Score Aggregation (0 to 3) & Flag (>= 2)
- Rule Combination Bitmask Generation
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def apply_high_amount_rule(
    df: pd.DataFrame,
    method: str = "p99",
    threshold_val: float | None = None
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Evaluate Rule 1: High Transaction Amount.

    Args:
        df: DataFrame containing 'Amount' column.
        method: 'p99' for 99th percentile or '3sigma' for mean + 3*std.
        threshold_val: Optional custom explicit threshold value.

    Returns:
        Tuple of (df_with_rule_columns, metrics_dict).
    """
    df = df.copy()
    mean_val = float(df["Amount"].mean())
    std_val = float(df["Amount"].std()) if len(df) > 1 else 0.0
    amount_threshold = mean_val + (3.0 * std_val)
    amount_99 = float(df["Amount"].quantile(0.99))

    df["Rule_High_Amount_3Sigma"] = (df["Amount"] > amount_threshold).astype(int)
    df["Rule_Top_1pct_Amount"] = (df["Amount"] >= amount_99).astype(int)

    if threshold_val is not None:
        df["Rule_High_Amount"] = (df["Amount"] > threshold_val).astype(int)
        active_thresh = threshold_val
    elif method == "3sigma":
        df["Rule_High_Amount"] = df["Rule_High_Amount_3Sigma"]
        active_thresh = amount_threshold
    else:  # default 'p99'
        df["Rule_High_Amount"] = df["Rule_Top_1pct_Amount"]
        active_thresh = amount_99

    metrics = {
        "mean_amount": mean_val,
        "std_amount": std_val,
        "amount_threshold": amount_threshold,
        "amount_99": amount_99,
        "active_threshold": active_thresh,
        "high_amount_alerts": int(df["Rule_High_Amount"].sum()),
    }
    return df, metrics


def apply_late_night_rule(
    df: pd.DataFrame,
    start_hour: int = 23,
    end_hour: int = 5
) -> pd.DataFrame:
    """Evaluate Rule 2: Late-Night Activity (11:00 PM through 05:59 AM).

    Args:
        df: DataFrame containing 'Hour' column (0-23).
        start_hour: Late-night start boundary (default 23).
        end_hour: Late-night end boundary (default 5).

    Returns:
        DataFrame with 'Rule_Late_Night' column added.
    """
    df = df.copy()
    if "Hour" not in df.columns:
        raise ValueError("DataFrame must contain 'Hour' column to evaluate late night rule.")

    # 23:00 to 05:59 means Hour is either >= 23 or <= 5
    late_night_mask = (df["Hour"] >= start_hour) | (df["Hour"] <= end_hour)
    df["Rule_Late_Night"] = late_night_mask.astype(int)
    return df


def apply_high_frequency_rule(
    df: pd.DataFrame,
    threshold: int = 5,
    window: str = "1h"
) -> pd.DataFrame:
    """Evaluate Rule 3: High-Frequency Transaction Burst.

    Computes a rolling count over the specified window per Account_ID.

    Args:
        df: DataFrame containing 'Account_ID' and 'Transaction_Datetime'.
        threshold: Transaction count threshold within the window (default 5).
        window: Rolling window duration string (default '1h').

    Returns:
        DataFrame with 'Txn_Count_1H' and 'Rule_High_Frequency' columns added.
    """
    df = df.copy()

    # Ensure chronological order per account
    sort_cols = [c for c in ["Account_ID", "Transaction_Datetime"] if c in df.columns]
    df = df.sort_values(sort_cols).reset_index(drop=True)

    if "Transaction_Datetime" in df.columns and not df["Transaction_Datetime"].isnull().all():
        try:
            # Vectorized rolling window count per Account_ID
            counts = (
                df.groupby("Account_ID")
                  .rolling(window, on="Transaction_Datetime")["Transaction_ID"]
                  .count()
                  .reset_index(level=0, drop=True)
                  .values
            )
            df["Txn_Count_1H"] = counts.astype(int)
        except Exception:
            # Fallback to hourly window grouping (Section 15)
            df = _fallback_hourly_frequency(df)
    else:
        df = _fallback_hourly_frequency(df)

    df["Rule_High_Frequency"] = (df["Txn_Count_1H"] >= threshold).astype(int)
    return df


def _fallback_hourly_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Fallback grouping helper by Account_ID, Transaction_Date, and Hour."""
    group_cols = ["Account_ID"]
    if "Transaction_Date" in df.columns:
        group_cols.append("Transaction_Date")
    if "Hour" in df.columns:
        group_cols.append("Hour")

    hourly_counts = (
        df.groupby(group_cols)
          .size()
          .reset_index(name="Txn_Count_1H")
    )
    df = df.merge(hourly_counts, on=group_cols, how="left")
    df["Txn_Count_1H"] = df["Txn_Count_1H"].fillna(1).astype(int)
    return df


def apply_all_rules_and_score(
    df: pd.DataFrame,
    amount_method: str = "p99",
    freq_threshold: int = 5,
    suspicion_threshold: int = 2,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Apply all rules, compute the Suspicion Score, and generate alert flags.

    Formula:
    Suspicion_Score = Rule_High_Amount + Rule_Late_Night + Rule_High_Frequency
    Suspicious = 1 if Suspicion_Score >= suspicion_threshold else 0

    Args:
        df: Cleaned transaction DataFrame.
        amount_method: 'p99' (default) or '3sigma'.
        freq_threshold: Minimum transactions in 1-hour window for Rule 3.
        suspicion_threshold: Minimum score to trigger alert (default 2).

    Returns:
        Tuple of (scored_dataframe, summary_dictionary).
    """
    df, amount_metrics = apply_high_amount_rule(df, method=amount_method)
    df = apply_late_night_rule(df)
    df = apply_high_frequency_rule(df, threshold=freq_threshold)

    # Composite Suspicion Score (0 to 3)
    df["Suspicion_Score"] = (
        df["Rule_High_Amount"] +
        df["Rule_Late_Night"] +
        df["Rule_High_Frequency"]
    ).astype(int)

    # Flag for manual investigator review
    df["Suspicious"] = (df["Suspicion_Score"] >= suspicion_threshold).astype(int)

    # Rule Combination bitmask (e.g. '1_1_0')
    df["Rule_Combination"] = (
        df["Rule_High_Amount"].astype(str) + "_" +
        df["Rule_Late_Night"].astype(str) + "_" +
        df["Rule_High_Frequency"].astype(str)
    )

    summary: Dict[str, Any] = {
        "Total Transactions": len(df),
        "Suspicious Transactions": int(df["Suspicious"].sum()),
        "Suspicious %": round(float(df["Suspicious"].mean() * 100), 2),
        "High Amount Alerts": int(df["Rule_High_Amount"].sum()),
        "Late Night Alerts": int(df["Rule_Late_Night"].sum()),
        "High Frequency Alerts": int(df["Rule_High_Frequency"].sum()),
        "Score_0_Count": int((df["Suspicion_Score"] == 0).sum()),
        "Score_1_Count": int((df["Suspicion_Score"] == 1).sum()),
        "Score_2_Count": int((df["Suspicion_Score"] == 2).sum()),
        "Score_3_Count": int((df["Suspicion_Score"] == 3).sum()),
        **amount_metrics,
    }
    return df, summary
