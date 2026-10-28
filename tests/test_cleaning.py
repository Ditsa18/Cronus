"""Unit tests for data cleansing and normalization module."""

import pytest
import pandas as pd
import numpy as np
from src.cleaning import clean_transaction_data, inspect_data_summary


def test_clean_transaction_data_drops_duplicates():
    """Verify that exact duplicate rows are removed."""
    raw = pd.DataFrame({
        "Transaction_ID": ["TX01", "TX01", "TX02"],
        "Account_ID": ["ACC1", "ACC1", "ACC2"],
        "Transaction_Date": ["2026-09-10", "2026-09-10", "2026-09-11"],
        "Transaction_Time": ["14:30", "14:30", "02:15"],
        "Amount": [100.0, 100.0, 5000.0],
        "Transaction_Type": ["Transfer", "Transfer", "Payment"],
        "Channel": ["Online", "Online", "Mobile App"],
    })
    cleaned, log = clean_transaction_data(raw)
    assert len(cleaned) == 2
    assert log["duplicates_removed"] == 1


def test_clean_transaction_data_hour_extraction_and_datetime():
    """Verify datetime parsing and Hour extraction."""
    raw = pd.DataFrame({
        "Transaction_ID": ["TX01", "TX02", "TX03"],
        "Account_ID": ["ACC1", "ACC2", "ACC3"],
        "Transaction_Date": ["2026-09-10", "2026-09-11", "2026-09-12"],
        "Transaction_Time": ["23:45", "00:15", "06:30"],
        "Amount": [200.0, 300.0, 400.0],
    })
    cleaned, log = clean_transaction_data(raw)
    assert "Hour" in cleaned.columns
    assert list(cleaned["Hour"]) == [23, 0, 6]
    assert "Transaction_Datetime" in cleaned.columns


def test_clean_transaction_data_removes_negative_and_zero_amounts():
    """Verify non-positive amounts are dropped or flagged."""
    raw = pd.DataFrame({
        "Transaction_ID": ["TX01", "TX02", "TX03"],
        "Account_ID": ["ACC1", "ACC2", "ACC3"],
        "Transaction_Date": ["2026-09-10", "2026-09-11", "2026-09-12"],
        "Transaction_Time": ["10:00", "11:00", "12:00"],
        "Amount": [50.0, -100.0, 0.0],
    })
    cleaned, log = clean_transaction_data(raw)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["Transaction_ID"] == "TX01"
    assert log["invalid_amounts_removed"] == 2


def test_clean_transaction_data_standardizes_strings():
    """Verify channels and types are stripped and title-cased."""
    raw = pd.DataFrame({
        "Transaction_ID": ["TX01", "TX02"],
        "Account_ID": ["ACC1", "ACC2"],
        "Transaction_Date": ["2026-09-10", "2026-09-11"],
        "Transaction_Time": ["10:00", "11:00"],
        "Amount": [50.0, 100.0],
        "Transaction_Type": [" transfer ", "PAYMENT"],
        "Channel": ["online", " MOBILE APP "],
    })
    cleaned, _ = clean_transaction_data(raw)
    assert cleaned.iloc[0]["Transaction_Type"] == "Transfer"
    assert cleaned.iloc[1]["Transaction_Type"] == "Payment"
    assert cleaned.iloc[0]["Channel"] == "Online"
    assert cleaned.iloc[1]["Channel"] == "Mobile App"


def test_inspect_data_summary_returns_metrics():
    """Verify inspection utility computes required exploratory metrics."""
    raw = pd.DataFrame({
        "Transaction_ID": ["TX01", "TX02"],
        "Account_ID": ["ACC1", "ACC2"],
        "Transaction_Date": ["2026-09-10", "2026-09-11"],
        "Transaction_Time": ["10:00", "11:00"],
        "Amount": [100.0, 200.0],
    })
    summary = inspect_data_summary(raw)
    assert summary["shape"] == (2, 5)
    assert summary["total_amount"] == 300.0
    assert summary["mean_amount"] == 150.0
