"""Unit tests for the rule evaluation and scoring engine."""

import pytest
import pandas as pd
import numpy as np
from src.rules import (
    apply_high_amount_rule,
    apply_late_night_rule,
    apply_high_frequency_rule,
    apply_all_rules_and_score,
)


@pytest.fixture
def sample_transaction_df():
    """Create a controlled transaction DataFrame for rule testing."""
    # 25 baseline normal transactions + 1 outlier + late night + burst
    acc101_txns = [
        {"Transaction_ID": f"TX{i:03d}", "Account_ID": "ACC101", "Transaction_Date": "2026-09-10",
         "Transaction_Time": f"02:{i*5:02d}", "Hour": 2, "Amount": 100.0 + i*10,
         "Transaction_Datetime": f"2026-09-10 02:{i*5:02d}:00"}
        for i in range(1, 6)
    ]
    # Add the extreme amount in burst
    acc101_txns.append({
        "Transaction_ID": "TX006", "Account_ID": "ACC101", "Transaction_Date": "2026-09-10",
        "Transaction_Time": "02:30", "Hour": 2, "Amount": 95000.0,
        "Transaction_Datetime": "2026-09-10 02:30:00"
    })
    # Add 20 normal baseline daytime transactions for other accounts
    other_txns = [
        {"Transaction_ID": f"TX{i:03d}", "Account_ID": f"ACC{102 + (i%3)}", "Transaction_Date": "2026-09-10",
         "Transaction_Time": f"{10 + (i%8):02d}:15", "Hour": 10 + (i%8), "Amount": 150.0 + (i%5)*20,
         "Transaction_Datetime": f"2026-09-10 {10 + (i%8):02d}:15:00"}
        for i in range(7, 27)
    ]
    # Add one late-night non-outlier
    other_txns.append({
        "Transaction_ID": "TX027", "Account_ID": "ACC105", "Transaction_Date": "2026-09-10",
        "Transaction_Time": "23:45", "Hour": 23, "Amount": 220.0,
        "Transaction_Datetime": "2026-09-10 23:45:00"
    })
    df = pd.DataFrame(acc101_txns + other_txns)
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])
    df["Transaction_Datetime"] = pd.to_datetime(df["Transaction_Datetime"])
    return df


def test_apply_high_amount_rule_statistical(sample_transaction_df):
    """Verify Rule 1 statistical mean + 3 sigma threshold."""
    df, metrics = apply_high_amount_rule(sample_transaction_df, method="3sigma")
    assert "Rule_High_Amount" in df.columns
    assert "amount_threshold" in metrics
    # Only TX006 ($95,000) should trigger high amount
    assert df["Rule_High_Amount"].sum() == 1
    assert df.loc[df["Transaction_ID"] == "TX006", "Rule_High_Amount"].iloc[0] == 1


def test_apply_high_amount_rule_percentile(sample_transaction_df):
    """Verify Rule 1 99th percentile threshold."""
    df, metrics = apply_high_amount_rule(sample_transaction_df, method="p99")
    assert "Rule_Top_1pct_Amount" in df.columns
    assert "amount_99" in metrics
    assert df["Rule_High_Amount"].sum() >= 1


def test_apply_late_night_rule(sample_transaction_df):
    """Verify Rule 2 flags hours 23 to 5 and clears others."""
    df = apply_late_night_rule(sample_transaction_df)
    assert "Rule_Late_Night" in df.columns
    expected = ((df["Hour"] >= 23) | (df["Hour"] <= 5)).astype(int)
    assert (df["Rule_Late_Night"] == expected).all()
    # Explicitly check known late-night row TX006 (Hour 2) and TX027 (Hour 23)
    assert df.loc[df["Transaction_ID"] == "TX006", "Rule_Late_Night"].iloc[0] == 1
    assert df.loc[df["Transaction_ID"] == "TX027", "Rule_Late_Night"].iloc[0] == 1


def test_apply_high_frequency_rule(sample_transaction_df):
    """Verify Rule 3 rolling 1-hour count flags >= 5 transactions."""
    df = apply_high_frequency_rule(sample_transaction_df, threshold=5, window="1h")
    assert "Txn_Count_1H" in df.columns
    assert "Rule_High_Frequency" in df.columns
    # ACC101 has 6 txns within 50 mins: txns 5 and 6 have rolling counts >= 5
    acc101_txns = df[df["Account_ID"] == "ACC101"]
    assert (acc101_txns["Rule_High_Frequency"] == 1).sum() >= 2
    # ACC102 has max 1 txn/hour -> must be 0
    acc102_txns = df[df["Account_ID"] == "ACC102"]
    assert (acc102_txns["Rule_High_Frequency"] == 0).all()


def test_apply_all_rules_and_score(sample_transaction_df):
    """Verify composite scoring and Suspicious flag (Score >= 2)."""
    df, summary = apply_all_rules_and_score(sample_transaction_df)
    assert "Suspicion_Score" in df.columns
    assert "Suspicious" in df.columns
    assert "Rule_Combination" in df.columns

    # Suspicion score must be in range 0..3
    assert df["Suspicion_Score"].between(0, 3).all()
    # Suspicious must equal Suspicion_Score >= 2
    assert (df["Suspicious"] == (df["Suspicion_Score"] >= 2).astype(int)).all()
    # TX006 is late night (1), high amount (1), and in 5+ burst (1) -> Score 3!
    tx6 = df[df["Transaction_ID"] == "TX006"].iloc[0]
    assert tx6["Suspicion_Score"] == 3
    assert tx6["Suspicious"] == 1
    assert tx6["Rule_Combination"] == "1_1_1"


def test_custom_amount_threshold(sample_transaction_df):
    """Verify custom explicit threshold in apply_high_amount_rule."""
    df, metrics = apply_high_amount_rule(sample_transaction_df, threshold_val=50000.0)
    assert metrics["active_threshold"] == 50000.0
    assert df["Rule_High_Amount"].sum() == 1


def test_late_night_rule_missing_hour_raises_error():
    """Verify ValueError is raised if Hour column is missing."""
    df = pd.DataFrame({"Amount": [100.0]})
    with pytest.raises(ValueError, match="DataFrame must contain 'Hour' column"):
        apply_late_night_rule(df)


def test_fallback_hourly_frequency():
    """Verify fallback frequency logic works when Transaction_Datetime is not available."""
    df = pd.DataFrame({
        "Transaction_ID": [f"T{i}" for i in range(1, 7)],
        "Account_ID": ["A1"] * 6,
        "Transaction_Date": pd.to_datetime(["2026-09-10"] * 6),
        "Hour": [14] * 6,
    })
    result = apply_high_frequency_rule(df, threshold=5)
    assert "Rule_High_Frequency" in result.columns
    assert (result["Rule_High_Frequency"] == 1).all()

