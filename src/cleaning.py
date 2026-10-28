"""Data loading, cleansing, validation, and normalization module.

Performs deterministic data validation, datetime standardization, duplicate removal,
and produces structured cleaning audit logs adhering to Section 8 & 9 requirements.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def clean_transaction_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Clean and validate raw banking transaction records.

    Cleaning steps:
    1. Drop exact duplicate records.
    2. Remove records with duplicate Transaction_ID values (keeping first).
    3. Drop records with missing critical fields (Transaction_ID, Account_ID, Amount, Transaction_Time).
    4. Remove negative or zero transaction amounts.
    5. Convert Transaction_Date and Transaction_Time into standardized datetimes.
    6. Extract integer 'Hour' (0 to 23).
    7. Standardize textual categories (Transaction_Type, Channel).

    Args:
        df: Raw transaction DataFrame.

    Returns:
        Tuple of (cleaned_dataframe, cleaning_log_dict).
    """
    initial_count = len(df)
    cleaning_log: Dict[str, Any] = {
        "initial_records": initial_count,
        "duplicates_removed": 0,
        "duplicate_ids_removed": 0,
        "missing_critical_dropped": 0,
        "invalid_amounts_removed": 0,
        "final_records": 0,
    }

    # Step 1: Drop exact duplicates
    df_clean = df.drop_duplicates().copy()
    cleaning_log["duplicates_removed"] = initial_count - len(df_clean)

    # Step 2: Check & remove duplicate Transaction_ID
    if "Transaction_ID" in df_clean.columns:
        pre_id_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=["Transaction_ID"], keep="first").copy()
        cleaning_log["duplicate_ids_removed"] = pre_id_count - len(df_clean)

    # Step 3: Check missing critical fields
    critical_cols = [c for c in ["Transaction_ID", "Account_ID", "Amount", "Transaction_Time"] if c in df_clean.columns]
    pre_na_count = len(df_clean)
    df_clean = df_clean.dropna(subset=critical_cols).copy()
    cleaning_log["missing_critical_dropped"] = pre_na_count - len(df_clean)

    # Step 4: Validate Amount > 0
    if "Amount" in df_clean.columns:
        pre_amt_count = len(df_clean)
        df_clean = df_clean[df_clean["Amount"] > 0].copy()
        cleaning_log["invalid_amounts_removed"] = pre_amt_count - len(df_clean)

    # Step 5: Convert dates and times
    if "Transaction_Date" in df_clean.columns:
        df_clean["Transaction_Date"] = pd.to_datetime(df_clean["Transaction_Date"], errors="coerce")

    if "Transaction_Time" in df_clean.columns:
        # Handle time string parsing to extract hour
        time_parsed = pd.to_datetime(df_clean["Transaction_Time"], format="%H:%M", errors="coerce")
        # Fallback for %H:%M:%S format if seconds are present
        if time_parsed.isnull().any():
            mask = time_parsed.isnull()
            time_parsed.loc[mask] = pd.to_datetime(df_clean.loc[mask, "Transaction_Time"], format="%H:%M:%S", errors="coerce")
        
        df_clean["Hour"] = time_parsed.dt.hour

        # Construct full unified Transaction_Datetime feature
        if "Transaction_Date" in df_clean.columns:
            df_clean["Transaction_Datetime"] = pd.to_datetime(
                df_clean["Transaction_Date"].dt.strftime("%Y-%m-%d") + " " +
                time_parsed.dt.strftime("%H:%M:%S"),
                errors="coerce"
            )

    # Step 6: Standardize string categories
    string_cols = ["Transaction_Type", "Channel", "Merchant_Category", "Location"]
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip().str.title()

    cleaning_log["final_records"] = len(df_clean)
    return df_clean, cleaning_log


def inspect_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute high-level exploratory statistics for logging and reporting."""
    summary: Dict[str, Any] = {
        "shape": df.shape,
        "columns": list(df.columns),
        "null_counts": df.isnull().sum().to_dict(),
        "total_amount": float(df["Amount"].sum()) if "Amount" in df.columns else 0.0,
        "mean_amount": float(df["Amount"].mean()) if "Amount" in df.columns else 0.0,
        "median_amount": float(df["Amount"].median()) if "Amount" in df.columns else 0.0,
        "max_amount": float(df["Amount"].max()) if "Amount" in df.columns else 0.0,
        "min_amount": float(df["Amount"].min()) if "Amount" in df.columns else 0.0,
    }
    return summary
