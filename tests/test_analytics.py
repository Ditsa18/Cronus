"""Unit tests for analytics, drilldown aggregations, and evaluation metrics."""

import pytest
import pandas as pd
import numpy as np
from src.analytics import (
    get_suspicious_queue,
    get_type_analysis,
    get_channel_analysis,
    get_hour_analysis,
    get_account_risk_analysis,
    get_rule_combination_analysis,
    evaluate_against_ground_truth,
    answer_business_questions,
)


@pytest.fixture
def scored_sample_df():
    """Create a sample scored dataset for testing analytical aggregations."""
    return pd.DataFrame({
        "Transaction_ID": [f"TX{i}" for i in range(1, 9)],
        "Account_ID": ["ACC1", "ACC1", "ACC2", "ACC2", "ACC3", "ACC3", "ACC4", "ACC4"],
        "Amount": [100.0, 50000.0, 200.0, 60000.0, 300.0, 400.0, 150.0, 80000.0],
        "Hour": [14, 2, 10, 1, 15, 16, 12, 3],
        "Transaction_Type": ["Payment", "Transfer", "Payment", "Transfer", "Withdrawal", "Deposit", "Payment", "Transfer"],
        "Channel": ["Online", "Mobile App", "ATM", "Online", "Branch", "Online", "Online", "Online"],
        "Rule_High_Amount": [0, 1, 0, 1, 0, 0, 0, 1],
        "Rule_Late_Night": [0, 1, 0, 1, 0, 0, 0, 1],
        "Rule_High_Frequency": [0, 1, 0, 0, 0, 0, 0, 0],
        "Suspicion_Score": [0, 3, 0, 2, 0, 0, 0, 2],
        "Suspicious": [0, 1, 0, 1, 0, 0, 0, 1],
        "Rule_Combination": ["0_0_0", "1_1_1", "0_0_0", "1_1_0", "0_0_0", "0_0_0", "0_0_0", "1_1_0"],
        "Fraud_Label": [0, 1, 0, 1, 0, 0, 0, 0],  # TX8 is FP (Rule Alert 1, Actual 0)
    })


def test_get_suspicious_queue(scored_sample_df):
    """Verify priority queue filters only Suspicious==1 and sorts by score descending."""
    queue = get_suspicious_queue(scored_sample_df)
    assert len(queue) == 3
    assert (queue["Suspicious"] == 1).all()
    # First item should have highest score (3)
    assert queue.iloc[0]["Suspicion_Score"] == 3
    assert queue.iloc[0]["Transaction_ID"] == "TX2"


def test_get_type_analysis(scored_sample_df):
    """Verify type analysis computes transactions, suspicious sum, and rate."""
    type_df = get_type_analysis(scored_sample_df)
    assert "Transaction_Type" in type_df.columns
    assert "Suspicious_Rate" in type_df.columns
    # Transfer has 3 total transactions and 3 suspicious (100% rate)
    transfer_row = type_df[type_df["Transaction_Type"] == "Transfer"].iloc[0]
    assert transfer_row["Transactions"] == 3
    assert transfer_row["Suspicious"] == 3
    assert transfer_row["Suspicious_Rate"] == 100.0


def test_get_channel_analysis(scored_sample_df):
    """Verify channel analysis computes correctly."""
    ch_df = get_channel_analysis(scored_sample_df)
    assert "Channel" in ch_df.columns
    assert "Suspicious_Rate" in ch_df.columns
    assert ch_df["Transactions"].sum() == len(scored_sample_df)


def test_get_hour_analysis(scored_sample_df):
    """Verify hour analysis covers hours with transactions."""
    hr_df = get_hour_analysis(scored_sample_df)
    assert "Hour" in hr_df.columns
    assert "Suspicious_Rate" in hr_df.columns


def test_get_account_risk_analysis(scored_sample_df):
    """Verify account risk aggregates suspicious volume per account."""
    acc_df = get_account_risk_analysis(scored_sample_df)
    assert "Account_ID" in acc_df.columns
    assert "Suspicious_Transactions" in acc_df.columns
    # ACC1, ACC2, ACC4 each have 1 suspicious transaction
    assert acc_df["Suspicious_Transactions"].max() == 1


def test_get_rule_combination_analysis(scored_sample_df):
    """Verify rule combination counts matches dataset combinations."""
    comb_df = get_rule_combination_analysis(scored_sample_df)
    assert "Rule_Combination" in comb_df.columns
    assert "Transactions" in comb_df.columns
    assert comb_df["Transactions"].sum() == len(scored_sample_df)


def test_evaluate_against_ground_truth(scored_sample_df):
    """Verify confusion matrix and precision/recall calculations."""
    eval_metrics = evaluate_against_ground_truth(scored_sample_df)
    assert "confusion_matrix" in eval_metrics
    assert "precision" in eval_metrics
    assert "recall" in eval_metrics
    # In fixture:
    # Actual 1s: TX2, TX4 (both predicted 1) -> TP = 2, FN = 0 (Recall = 1.0)
    # Actual 0s: TX1, TX3, TX5, TX6, TX7 (all predicted 0 -> TN=5), TX8 (predicted 1 -> FP=1)
    # Precision = TP / (TP + FP) = 2 / 3 = ~0.667
    assert eval_metrics["tp"] == 2
    assert eval_metrics["fp"] == 1
    assert eval_metrics["fn"] == 0
    assert eval_metrics["tn"] == 5
    assert round(eval_metrics["recall"], 2) == 1.0
    assert round(eval_metrics["precision"], 2) == 0.67


def test_answer_business_questions(scored_sample_df):
    """Verify all 10 business questions are answered with values."""
    q_dict = answer_business_questions(scored_sample_df)
    assert len(q_dict) == 10
    for q_num in range(1, 11):
        assert f"Q{q_num}" in q_dict
        assert "question" in q_dict[f"Q{q_num}"]
        assert "answer" in q_dict[f"Q{q_num}"]
