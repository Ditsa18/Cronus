"""Tests for the synthetic bank transaction data generator."""

import pytest
import pandas as pd
from src.data_generator import generate_synthetic_transactions, REQUIRED_COLUMNS


def test_generate_synthetic_transactions_schema_and_size():
    """Verify that the generated dataset contains all required fields and the requested row count."""
    df = generate_synthetic_transactions(n=500, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 500
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing required column: {col}"


def test_generate_synthetic_transactions_reproducibility():
    """Verify that using the same seed produces identical datasets."""
    df1 = generate_synthetic_transactions(n=100, seed=123)
    df2 = generate_synthetic_transactions(n=100, seed=123)
    pd.testing.assert_frame_equal(df1, df2)


def test_generate_synthetic_transactions_privacy_rules():
    """Verify that no PII or real credentials exist in the generated dataset."""
    df = generate_synthetic_transactions(n=200, seed=42)
    
    # Check that Account_ID matches synthetic pattern ACC\d+
    assert df["Account_ID"].str.match(r"^ACC\d+$").all()
    # Check that Transaction_ID matches TX\d+
    assert df["Transaction_ID"].str.match(r"^TX\d+$").all()
    # Check that Device_ID matches DEV\d+
    assert df["Device_ID"].str.match(r"^DEV\d+$").all()
    
    # Prohibited PII columns must NOT exist
    prohibited_cols = ["card_number", "pin", "cvv", "ssn", "password", "customer_name", "address"]
    for col in prohibited_cols:
        assert col not in [c.lower() for c in df.columns]


def test_generate_synthetic_transactions_has_fraud_and_normal():
    """Verify dataset contains both legitimate transactions and fraud cases."""
    df = generate_synthetic_transactions(n=1000, seed=42)
    assert (df["Fraud_Label"] == 0).sum() > 0
    assert (df["Fraud_Label"] == 1).sum() > 0
    # Fraud should be a realistic minority class (typically between 1% and 10%)
    fraud_rate = df["Fraud_Label"].mean()
    assert 0.01 <= fraud_rate <= 0.15


def test_generate_synthetic_transactions_values_valid():
    """Verify amounts and balances are strictly positive."""
    df = generate_synthetic_transactions(n=200, seed=42)
    assert (df["Amount"] > 0).all()
    assert (df["Balance_Before"] >= 0).all()
    assert (df["Balance_After"] >= 0).all()
