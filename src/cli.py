"""Command-Line Interface (CLI) and End-to-End Fraud Analytics Pipeline.

Coordinates data loading, cleansing, rule evaluation, report generation,
and Matplotlib visual chart production.
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional
import pandas as pd
from tabulate import tabulate

from src.data_generator import generate_synthetic_transactions
from src.cleaning import clean_transaction_data, inspect_data_summary
from src.rules import apply_all_rules_and_score
from src.analytics import (
    get_suspicious_queue,
    get_type_analysis,
    get_channel_analysis,
    get_hour_analysis,
    get_account_risk_analysis,
    get_pattern_summary,
    get_rule_combination_analysis,
    evaluate_against_ground_truth,
    answer_business_questions,
)
from src.visualization import generate_all_visualizations


def run_fraud_pipeline(
    input_csv: Optional[str] = None,
    generate_n: int = 10000,
    output_csv: Optional[str] = None,
    reports_dir: str = "reports",
    seed: int = 42,
    amount_method: str = "p99",
    freq_threshold: int = 5,
    suspicion_threshold: int = 2,
) -> Dict[str, Any]:
    """Execute the complete end-to-end fraud screening pipeline."""
    os.makedirs(reports_dir, exist_ok=True)
    figures_dir = os.path.join(reports_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Ingestion / Generation
    if input_csv and os.path.exists(input_csv):
        raw_df = pd.read_csv(input_csv)
    else:
        raw_df = generate_synthetic_transactions(n=generate_n, seed=seed)
        if output_csv:
            os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
            raw_df.to_csv(output_csv, index=False)

    # 2. Data Cleaning & Inspection
    cleaned_df, cleaning_log = clean_transaction_data(raw_df)
    inspect_summary = inspect_data_summary(cleaned_df)

    # 3. Rule Evaluation & Scoring
    scored_df, score_summary = apply_all_rules_and_score(
        cleaned_df,
        amount_method=amount_method,
        freq_threshold=freq_threshold,
        suspicion_threshold=suspicion_threshold,
    )

    # 4. Analytics & Drilldowns
    suspicious_queue = get_suspicious_queue(scored_df)
    type_analysis = get_type_analysis(scored_df)
    channel_analysis = get_channel_analysis(scored_df)
    hour_analysis = get_hour_analysis(scored_df)
    account_analysis = get_account_risk_analysis(scored_df)
    pattern_summary = get_pattern_summary(scored_df)
    combination_analysis = get_rule_combination_analysis(scored_df)
    ground_truth_eval = evaluate_against_ground_truth(scored_df)
    business_answers = answer_business_questions(scored_df)

    # 5. Export Priority Queues and Data Artifacts
    suspicious_csv_path = os.path.join(reports_dir, "suspicious_transactions.csv")
    account_risk_csv_path = os.path.join(reports_dir, "account_risk_summary.csv")
    suspicious_queue.to_csv(suspicious_csv_path, index=False)
    account_analysis.to_csv(account_risk_csv_path, index=False)

    # 6. Generate Matplotlib Visualizations
    figure_paths = generate_all_visualizations(scored_df, output_dir=figures_dir)

    # 7. Generate Executive Management Report
    mgmt_report_path = os.path.join(reports_dir, "FRAUD_MONITORING_MANAGEMENT_REPORT.md")
    _write_management_report(
        filepath=mgmt_report_path,
        score_summary=score_summary,
        cleaning_log=cleaning_log,
        inspect_summary=inspect_summary,
        pattern_summary=pattern_summary,
        type_analysis=type_analysis,
        channel_analysis=channel_analysis,
        account_analysis=account_analysis,
        combination_analysis=combination_analysis,
        ground_truth_eval=ground_truth_eval,
        business_answers=business_answers,
    )

    return {
        "total_transactions": len(scored_df),
        "suspicious_count": int(scored_df["Suspicious"].sum()),
        "suspicious_rate": score_summary["Suspicious %"],
        "suspicious_csv_path": suspicious_csv_path,
        "account_risk_csv_path": account_risk_csv_path,
        "management_report_path": mgmt_report_path,
        "figure_paths": figure_paths,
        "score_summary": score_summary,
        "cleaning_log": cleaning_log,
        "business_answers": business_answers,
        "ground_truth_eval": ground_truth_eval,
    }


def _write_management_report(
    filepath: str,
    score_summary: Dict[str, Any],
    cleaning_log: Dict[str, Any],
    inspect_summary: Dict[str, Any],
    pattern_summary: pd.DataFrame,
    type_analysis: pd.DataFrame,
    channel_analysis: pd.DataFrame,
    account_analysis: pd.DataFrame,
    combination_analysis: pd.DataFrame,
    ground_truth_eval: Dict[str, Any],
    business_answers: Dict[str, Any],
) -> None:
    """Compile and write the comprehensive markdown management report."""
    total = score_summary["Total Transactions"]
    susp = score_summary["Suspicious Transactions"]
    susp_pct = score_summary["Suspicious %"]

    content = f"""# Executive Fraud Monitoring & Suspicious Activity Analytics Report

**Prepared For**: Bank Fraud Monitoring Steering Committee & Risk Audit  
**Role**: Junior Data Analyst / Principal Autonomous Fraud Systems Engineer  
**Report Version**: 1.0.0 (Official Release)  
**Status**: COMPLETE & VERIFIED  

---

## 1. Executive Summary & KPIs
The bank evaluated a batch of **{total:,} transactions** through our explainable first-level screening pipeline.
A total of **{susp:,} transactions ({susp_pct}%)** triggered two or more risk heuristics and were escalated to the manual investigation queue.

| Executive Metric | Value | Context |
|---|:---:|---|
| **Total Ingested Volume** | {total:,} | Processed and cleaned transaction records |
| **Total Monetary Volume** | ${inspect_summary['total_amount']:,.2f} | Net portfolio turnover across monitored channels |
| **Average Transaction** | ${inspect_summary['mean_amount']:,.2f} | Population mean |
| **99th Percentile Threshold ($P_{{99}}$)** | ${score_summary.get('amount_99', 0.0):,.2f} | Outlier cutoff for high-value transfers |
| **Statistical Threshold ($\\mu + 3\\sigma$)** | ${score_summary.get('amount_threshold', 0.0):,.2f} | Baseline Gaussian 3-sigma cutoff |
| **Suspicious Flagged Volume** | **{susp:,} ({susp_pct}%)** | Prioritized for immediate analyst review (Score $\\ge 2$) |
| **High Amount Alerts** | {score_summary['High Amount Alerts']:,} | Single transactions exceeding outlier thresholds |
| **Late Night Alerts** | {score_summary['Late Night Alerts']:,} | Transactions occurring between 23:00 and 05:59 |
| **High Frequency Bursts** | {score_summary['High Frequency Alerts']:,} | Accounts executing $\\ge 5$ transactions in rolling 1-hour |

---

## 2. Answers to Core Business Questions (Section 34)

"""
    for q_id, q_data in business_answers.items():
        content += f"### {q_id}: {q_data['question']}\n**Finding**: {q_data['answer']}\n\n"

    content += f"""---

## 3. Recommended Rule Definition Table (Section 36)

| Rule Name | Condition | Score Weight | Business & Operational Rationale |
|---|---|:---:|---|
| **Unusual Amount** | `Amount >= P99` (or `Amount > Mean + 3*Std`) | **+1** | Transaction value is unusually high compared to historical baseline. |
| **Late Night** | `23:00 <= Hour <= 05:59` | **+1** | Activity occurs during the customer's typical sleep hours; common in automated card draining. |
| **High Frequency** | `Rolling 1-Hour Txn Count >= 5` | **+1** | Rapid transaction bursts indicate credential stuffing, automated bots, or panic card testing. |
| **Alert Cutoff** | `Suspicion_Score >= 2` | **ALERT** | Combines multi-factor signals to suppress single-anomaly noise and prioritize true risk. |

---

## 4. Pattern & Rule Combination Distribution (Section 31 & 32)

### Individual Rule Alert Volume
{pattern_summary.to_markdown(index=False)}

### Rule Bitmask Combination Analysis
{combination_analysis.to_markdown(index=False)}

---

## 5. Multi-Dimensional Risk Drilldowns

### Breakdown by Transaction Type
{type_analysis.to_markdown(index=False)}

### Breakdown by Channel
{channel_analysis.to_markdown(index=False)}

### Top High-Risk Customer Accounts (Top 10)
{account_analysis.head(10).to_markdown(index=False)}

---

## 6. Ground-Truth Historical Evaluation (Section 33)

| Metric | Score | Industry Interpretation |
|---|:---:|---|
| **True Positives (TP)** | {ground_truth_eval.get('tp', 'N/A')} | Confirmed fraud successfully caught by screening rules |
| **False Positives (FP)** | {ground_truth_eval.get('fp', 'N/A')} | Legitimate customer actions flagged for review |
| **True Negatives (TN)** | {ground_truth_eval.get('tn', 'N/A')} | Legitimate transactions cleared without disruption |
| **False Negatives (FN)** | {ground_truth_eval.get('fn', 'N/A')} | Undetected fraud slipping through first-tier rules |
| **Recall (Sensitivity)** | **{ground_truth_eval.get('recall', 0.0)*100:.2f}%** | Percentage of all actual frauds detected |
| **Precision** | **{ground_truth_eval.get('precision', 0.0)*100:.2f}%** | Percentage of flagged alerts that represent true fraud |
| **F1-Score** | **{ground_truth_eval.get('f1_score', 0.0):.3f}** | Harmonic mean of precision and recall |
| **False Positive Rate (FPR)** | **{ground_truth_eval.get('false_positive_rate', 0.0)*100:.2f}%** | Proportion of good customers inconvenienced (< 1% target) |

---

## 7. Operational & Ethical Limitations (Section 38)
1. **Investigation Signals vs. Proof of Guilt**: A flagged alert is an investigative signal for human-in-the-loop validation, **never legal or criminal proof of fraud**.
2. **False Positives**: Honest customers traveling abroad, paying for medical emergencies at 2:00 AM, or buying high-value electronics will trigger rules. Banks must use secondary verification (SMS OTP / phone callback) rather than punitive account blocking.
3. **Threshold Calibration**: Population-level thresholds ($\\mu + 3\\sigma$) should evolve toward personalized per-account baseline profiles to avoid penalizing high-net-worth commercial accounts.

---

## 8. Embedded Figures Reference
* Figure 1: Amount Distribution (`figures/01_amount_distribution.png`)
* Figure 2: Normal vs Suspicious Volume (`figures/02_normal_vs_suspicious.png`)
* Figure 3: Suspicious by Hour (`figures/03_suspicious_by_hour.png`)
* Figure 4: Suspicious Rate by Type (`figures/04_suspicious_rate_by_type.png`)
* Figure 5: Amount vs Suspicion Score (`figures/05_amount_vs_suspicion_score.png`)
* Figure 6: Rule Combinations (`figures/06_rule_combination_frequencies.png`)
* Figure 7: Channel Vulnerability (`figures/07_suspicious_rate_by_channel.png`)
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """CLI entry point for running the fraud detection pipeline."""
    parser = argparse.ArgumentParser(
        description="Rule-Based Bank Transaction Fraud Detection & Suspicious Activity Analytics"
    )
    parser.add_argument("--input", type=str, default=None, help="Path to input CSV dataset.")
    parser.add_argument("--generate", type=int, default=10000, help="Number of synthetic transactions to generate if no input CSV.")
    parser.add_argument("--output-csv", type=str, default="data/bank_transactions.csv", help="Destination path for generated dataset.")
    parser.add_argument("--reports-dir", type=str, default="reports", help="Directory where reports and figures are saved.")
    parser.add_argument("--amount-method", type=str, default="p99", choices=["p99", "3sigma"], help="Method for high amount threshold.")
    parser.add_argument("--freq-threshold", type=int, default=5, help="Rolling 1-hour burst threshold count.")
    parser.add_argument("--suspicion-threshold", type=int, default=2, help="Suspicion score alert cutoff (default 2).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")

    args = parser.parse_args()

    print("\n" + "="*80)
    print("  BANK TRANSACTION FRAUD DETECTION — RULE-BASED SCREENING PIPELINE")
    print("="*80)

    results = run_fraud_pipeline(
        input_csv=args.input,
        generate_n=args.generate,
        output_csv=args.output_csv,
        reports_dir=args.reports_dir,
        seed=args.seed,
        amount_method=args.amount_method,
        freq_threshold=args.freq_threshold,
        suspicion_threshold=args.suspicion_threshold,
    )

    summary = results["score_summary"]
    print(f"\n[+] Processing Complete!")
    print(f"    Total Transactions Evaluated : {results['total_transactions']:,}")
    print(f"    Suspicious Transactions Flagged: {results['suspicious_count']:,} ({results['suspicious_rate']}%)")
    print(f"    High Amount Alerts (Rule 1)   : {summary['High Amount Alerts']:,}")
    print(f"    Late Night Alerts (Rule 2)    : {summary['Late Night Alerts']:,}")
    print(f"    High Frequency Alerts (Rule 3): {summary['High Frequency Alerts']:,}")
    print(f"\n[+] Outputs Generated:")
    print(f"    1. Priority Review Queue      : {results['suspicious_csv_path']}")
    print(f"    2. Account Risk Summary       : {results['account_risk_csv_path']}")
    print(f"    3. Management Report (MD)     : {results['management_report_path']}")
    print(f"    4. Matplotlib Visualizations  : {len(results['figure_paths'])} charts saved in {os.path.join(args.reports_dir, 'figures')}")

    print("\n" + "="*80)
    print("  EXECUTIVE SUMMARY TABLE")
    print("="*80)
    rows = [
        ["Total Transactions", f"{results['total_transactions']:,}"],
        ["Suspicious Transactions (Score >= 2)", f"{results['suspicious_count']:,}"],
        ["Suspicious Alert Rate", f"{results['suspicious_rate']}%"],
        ["Score 0 (Normal)", f"{summary['Score_0_Count']:,}"],
        ["Score 1 (Low Anomaly)", f"{summary['Score_1_Count']:,}"],
        ["Score 2 (High Priority Alert)", f"{summary['Score_2_Count']:,}"],
        ["Score 3 (Critical Multi-Factor Alert)", f"{summary['Score_3_Count']:,}"],
    ]
    print(tabulate(rows, headers=["Metric", "Value"], tablefmt="grid"))


if __name__ == "__main__":
    main()
