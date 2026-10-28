<p align="left">
  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">
</p>

# Product Requirements Document (PRD)

**Project**: Rule-Based Bank Transaction Fraud Detection & Suspicious Activity Analytics  
**Version**: 1.0.0  
**Status**: APPROVED & IMPLEMENTATION READY  
**Author**: Junior Fraud Analytics Lead / Autonomous Principal Software Engineer  

---

## 1. Executive Summary
Financial institutions process vast daily transaction volumes where legitimate activity dwarfs fraudulent attempts. Conventional black-box models often lack explainability, complicating regulatory audits and customer service interactions. This project implements a transparent, explainable, rule-based screening engine that evaluates transactions on amount, timing, and velocity. The system computes a composite Suspicion Score, generates prioritized review queues for fraud analysts, and outputs executive-ready management reports and charts.

---

## 2. Problem Statement
Retail banks face escalating fraud losses (unauthorized wire transfers, card testing, account takeovers). Deploying complex black-box machine learning models as a primary filter poses compliance risks because investigators cannot easily explain why an alert was triggered. A robust, deterministic, rule-based first-level screening system is required to flag anomalous transactions, quantify risk patterns, and prioritize investigations without prematurely labeling customers as criminals.

---

## 3. Target Users & User Stories
1. **Fraud Operations Analyst**:
   * *As an analyst, I want a prioritized queue of flagged transactions with explicit trigger reasons, so that I can investigate high-risk events first without wading through low-risk noise.*
2. **Fraud Risk Policy Manager**:
   * *As a risk manager, I want aggregated summaries across transaction types, channels, and hours, so that I can adjust operational thresholds and banking policies.*
3. **Banking Compliance / Internal Auditor**:
   * *As an auditor, I want a deterministic rule-definition matrix and audit log for every flagged transaction, so that regulatory fairness and non-discrimination can be proven.*

---

## 4. Scope & Explicit Non-Goals
* **In-Scope**:
  * Synthetic banking dataset generation adhering to Section 6 schema and privacy constraints.
  * Automated data cleaning, datetime normalization, and duplicate removal.
  * Statistical amount thresholding ($\mu + 3\sigma$ and $99\text{th}$ percentile).
  * Late-night window anomaly detection ($23:00$ to $05:59$).
  * Rolling 1-hour transaction velocity tracking ($\ge 5$ transactions/hour).
  * Explainable composite scoring ($0$ to $3$) and alert flag ($\ge 2$).
  * Grouped reporting by type, channel, hour, and customer account.
  * Visual analytics suite with at least 6 Matplotlib charts.
  * Ground truth evaluation (confusion matrix, precision, recall, F1).
  * Management summary answering 10 business questions.
* **Explicit Non-Goals**:
  * Automatic blocking or frozen accounts without human review.
  * Deployment to external cloud environments or paid cloud APIs.
  * Real customer PII handling or real bank database write-backs.

---

## 5. Functional Requirements & Acceptance Criteria

### FR-001: Data Synthesis & Ingestion
* **Given** a request to generate transaction data,
* **When** `generate_synthetic_transactions(n=10000, seed=42)` is called,
* **Then** it produces a DataFrame with all 13 specified fields, no missing required keys, realistic distributions, and seeded reproducibility.

### FR-002: Data Cleansing & Normalization
* **Given** a raw transaction dataset containing duplicates and unparsed datetimes,
* **When** `clean_transaction_data(df)` is executed,
* **Then** exact duplicates are removed, `Transaction_Date` and `Transaction_Time` are converted to datetime/time types, `Hour` is extracted ($0-23$), invalid negative amounts are removed, and a cleaning audit log is returned.

### FR-003: Unusual Amount Anomaly Detection
* **Given** cleaned transaction amounts,
* **When** `apply_amount_rules(df, method='p99')` is executed,
* **Then** it calculates threshold values, flags transactions exceeding the threshold with `Rule_High_Amount = 1`, and logs the statistical values.

### FR-004: Late-Night Activity Detection
* **Given** transaction timestamps with extracted `Hour`,
* **When** `apply_late_night_rule(df)` is executed,
* **Then** transactions occurring between $23:00$ and $05:59$ receive `Rule_Late_Night = 1`, and all others receive `0`.

### FR-005: High-Frequency Burst Detection
* **Given** transaction records ordered by account and timestamp,
* **When** `apply_high_frequency_rule(df, threshold=5, window='1h')` is executed,
* **Then** `Txn_Count_1H` is calculated per account, and records with count $\ge 5$ receive `Rule_High_Frequency = 1`.

### FR-006: Composite Suspicion Scoring
* **Given** evaluated rules 1, 2, and 3,
* **When** `compute_suspicion_score(df)` is executed,
* **Then** `Suspicion_Score = Rule_High_Amount + Rule_Late_Night + Rule_High_Frequency` ($0 \le score \le 3$), and `Suspicious = 1` if `Suspicion_Score >= 2` else `0`.

### FR-007: Prioritized Queue & Account Risk Reports
* **Given** scored transactions,
* **When** generating investigation reports,
* **Then** `suspicious_transactions.csv` is produced (ordered by score and amount descending), along with `account_risk_summary.csv` summarizing repeat account anomalies.

### FR-008: Multi-Dimensional Pattern Analytics
* **Given** scored transactions,
* **When** executing aggregations,
* **Then** summary tables are generated for `Transaction_Type`, `Channel`, `Hour`, and 3-digit bitmask combinations (`Rule_Combination`).

### FR-009: Visual Analytics Generation
* **Given** scored transactions and aggregations,
* **When** `generate_visualizations(df, output_dir)` is executed,
* **Then** at least 6 high-resolution PNG charts are rendered and saved to `reports/figures/`.

### FR-010: Ground Truth Verification & Business Q&A
* **Given** ground truth `Fraud_Label`,
* **When** running evaluation,
* **Then** confusion matrix, precision, recall, and false positive rates are computed, and all 10 business questions are answered in `FRAUD_MONITORING_MANAGEMENT_REPORT.md`.

---

## 6. Non-Functional Requirements (NFR)
* **NFR-001 (Auditability)**: Complete traceability of why an alert was raised.
* **NFR-002 (Performance)**: Ingest and score 10,000 records in $< 3.0$ seconds.
* **NFR-003 (Privacy)**: Strictly zero PII.
* **NFR-004 (Code Quality)**: Modularity, PEP 8 styling, comprehensive docstrings, $> 90\%$ test coverage.

---

## 7. Release Gate & Verification Criteria
1. Full test suite passing via `pytest tests/ -v`.
2. Clean generation of synthetic dataset, cleaned dataset, priority queues, and summaries.
3. Successful rendering of 7 publication-ready charts.
4. Comprehensive executive summary report addressing all 10 business questions.
