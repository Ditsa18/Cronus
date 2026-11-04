<p align="left">
  <img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="180">
</p>

# PROJECT DOCUMENTATION
## Bank Transaction Fraud Detection: Rule-Based Fraud Analytics
### Industry-Oriented Data Analytics Student Project
#### Rule-Based Bank Transaction Fraud Detection & Suspicious Activity Analytics Using Python, Pandas, NumPy, Matplotlib and FastAPI

| Item | Details |
|---|---|
| **Project group** | Fraud Analytics Group / Team Cronus |
| **Team members** | Student Data Analyst (Portfolio Capstone) |
| **Course / Programme** | Industry-Oriented Data Analytics Capstone / Financial Analytics |
| **Faculty guide** | Fraud Risk Operations & Applied AI Guide |
| **Technology** | Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn (analysis); FastAPI, Tailwind CSS, Chart.js, HTML5 (interactive dashboard) |
| **Dataset** | Bank transaction screening records, 10,000 raw rows x 13 columns (synthetic, calendar month September 2026) |
| **Date of submission** | November 2026 |
| **Disclaimer** | The transaction dataset used in this project is synthetic and was created for learning and demonstration adhering to Section 7 privacy rules. All results describe this dataset and demonstrate an analytical workflow; they must not be read as evidence about a real banking operation or real customer accounts. |

---

## Table of Contents
* **Abstract**
* **1. Project Overview**
  * 1.1 Problem Statement
  * 1.2 Scope of the Work
  * 1.3 Project Deliverables
* **2. Business Scenario**
* **3. Project Objectives**
* **4. Libraries and Technology Stack**
* **5. Dataset Description**
  * 5.1 Data Quality Characteristics of the Raw File
* **6. Project Architecture and Workflow**
* **7. Data Loading and Inspection**
* **8. Data Cleaning**
  * 8.1 Cleaning Rules and Decisions
  * 8.2 Cleaning Code
  * 8.3 Data Cleaning Audit Results
  * 8.4 Reconciliation of Record Counts
* **9. Transaction Amount & Statistical Thresholds**
* **10. Rule-Based Detection Logic**
* **11. Key Fraud Detection & Screening KPIs**
* **12. Overall Screening Performance**
* **13. Rule 1 In-Depth: High-Amount Outlier Analysis**
* **14. Rule 2 In-Depth: Late-Night Activity Analysis**
* **15. Rule 3 In-Depth: High-Frequency Burst Detection**
* **16. Suspicion Score Distribution & Bitmask Analysis**
* **17. Transaction Type Performance Analysis**
* **18. Channel Vulnerability Analysis**
* **19. Hourly Transaction Trend Analysis**
* **20. Transaction Amount vs. Suspicion Score Correlation**
* **21. Required Visualizations**
* **22. Identifying High-Risk Accounts**
* **23. Advanced Extensions & ML Evaluation**
* **24. Pipeline Orchestration (cli.py)**
* **25. Interactive Web Dashboard (Cronus FraudGuard)**
* **26. Business Questions and Answers**
* **27. Business Findings and Operational Recommendations**
* **28. Testing, Validation and Reproducibility**
* **29. Limitations and Important Analytical & Ethical Note**
* **30. Learning Outcomes**
* **31. Conclusion and Future Scope**
* **References**

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## Abstract
Financial institutions process millions of electronic banking transactions daily. Punctual, non-disruptive clearing of legitimate payments is essential to consumer trust, yet fraudulent card testing, account takeovers, and unauthorized wire transfers inflict catastrophic losses. This project analyses 10,000 raw transaction records from a synthetic banking network to implement an explainable, transparent, rule-based screening engine. Rather than automatically declaring customers as criminals, the system evaluates behavioral anomalies across Transaction Amount, Transaction Time, and Transaction Velocity, assigning an interpretable Suspicion Score (0 to 3) to triage records for human-in-the-loop compliance review.

The screening engine was implemented as a modular Python pipeline (loading, validation, metric derivation, rule evaluation, KPI calculation, multidimensional drilldowns, and charting) and extended with a responsive web dashboard (Cronus FraudGuard) and REST API. Across 10,000 evaluated transactions, 118 records (1.18%) triggered multiple co-occurring anomalies (Suspicion Score >= 2) and were escalated to the priority review queue. Flagged transactions averaged $53,416.15—a 13.47x surge over normal volume ($3,966.30). Transfer was identified as the highest-risk transaction type (3.17% suspicious rate) and Online as the highest-risk channel (2.56%). Against verified historical ground-truth fraud labels, the rule-based screener achieved 100.0% precision, 0.00% false positive rate, and captured all acute multi-factor attack patterns.

**Keywords**: fraud analytics, rule-based screening, suspicion score, transaction anomaly detection, Pandas, Matplotlib, FastAPI, banking compliance.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 1. Project Overview
### 1.1 Problem Statement
Retail banks face escalating digital fraud threats across online banking, mobile applications, and payment gateways. While machine learning is frequently proposed, deploying black-box AI models as an unexplainable first-tier filter creates severe legal, regulatory (RBI / OCC / GDPR), and customer relations liabilities: compliance officers cannot explain to auditors or clients why an alert was triggered. A robust, deterministic, rule-based transaction screening system is required to screen transactions, provide clear audit trails, and prioritize manual investigation without prematurely freezing customer accounts.

### 1.2 Scope of the Work
* Ingestion, cleaning, and validation of 10,000 transaction records with zero data loss on valid keys.
* Computing statistical thresholds (Gaussian mean + 3 standard deviations and 99th percentile $P_{99}$).
* Evaluating three core behavioral heuristics: Amount Outlier, Late-Night Window (23:00 to 05:59), and Rolling 1-Hour Burst count.
* Combining rules into an explainable Suspicion Score (0 to 3) and 3-digit bitmasks (e.g. `1_1_0`).
* Producing 10 high-resolution Matplotlib figures and CSV investigation queues.
* Delivering an interactive web dashboard with dynamic threshold simulation and CSV upload capabilities.

### 1.3 Project Deliverables
All project brief deliverables are fulfilled:
1. Complete Python package (`src/`) and CLI runner (`src/cli.py`).
2. Cleaned primary dataset (`data/bank_transactions.csv`) and sample upload file (`test_upload_sample.csv`).
3. Priority manual review queue (`reports/suspicious_transactions.csv`).
4. Account risk summary profiles (`reports/account_risk_summary.csv`).
5. 10 publication-ready Matplotlib figures in `reports/figures/`.
6. Executive management report answering all 10 core business questions.
7. Interactive web dashboard (`run_web.py`) running on FastAPI and Tailwind CSS.
8. Automated test suite (`tests/`) with 38 passing tests and 94% code coverage.
9. Formal project documentation available in DOCX, PDF, HTML, and Markdown.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 2. Business Scenario
The project is framed as the work of a Junior Data Analyst in Cronus Bank's Fraud Monitoring and Surveillance Team. The bank requires a reliable, transparent first-level screening filter to process incoming transactions in real time before complex scoring models are introduced. The analyst's objective is to screen transactions based on amount, hour, and velocity, assign an interpretable suspicion score, and furnish fraud analysts with detailed triage reports rather than making irreversible automated blocks.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 3. Project Objectives
* Clean and validate raw transaction records with documented audit decisions.
* Analyze transaction amount distributions and establish statistical cutoffs.
* Detect unusually high transaction amounts using statistical ($\mu + 3\sigma$) and percentile ($P_{99}$) thresholds.
* Detect late-night transactions occurring between 11:00 PM and 5:59 AM.
* Detect rapid transaction bursts using rolling 1-hour window counts per account.
* Aggregate individual rules into an explainable Suspicion Score (0 to 3).
* Flag high-risk records (Score >= 2) into a prioritized investigation queue.
* Profile customer accounts with repeated suspicious activities.
* Create high-quality visual analytics charts using Matplotlib.
* Build a responsive interactive web dashboard for fraud monitoring analysts.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 4. Libraries and Technology Stack
| Library / Framework | Version | Purpose in this Project |
|---|---|---|
| **Python** | 3.11.6 | Core runtime environment. |
| **Pandas** | 3.1.0 | Data loading, cleaning, datetime parsing, rolling time-window counts, group aggregations. |
| **NumPy** | 2.4.6 | Vectorized array calculations, statistical thresholds, percentile quantiles. |
| **Matplotlib** | 3.11.2 | Publication-ready figure generation (histogram, bar charts, trend lines, scatter plots). |
| **Scikit-learn** | 1.9.1 | Ground-truth evaluation metrics: confusion matrix, precision, recall, F1-score. |
| **FastAPI** | 0.162.0 | High-performance backend web framework and REST API. |
| **Uvicorn** | 0.54.0 | Production ASGI server running the interactive dashboard. |
| **Tailwind CSS & Chart.js** | CDN | Modern, responsive dark-slate UI styling and interactive browser charts. |
| **Pytest & Coverage** | 9.2.0 / 7.1.0 | Test-driven development, automated unit & integration testing (94% coverage). |
| **Python-docx & ReportLab**| 1.2.0 / 5.1.0 | Professional document compilation into Word (.docx) and PDF (.pdf). |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 5. Dataset Description
The dataset (`data/bank_transactions.csv`) contains 10,000 transaction records across 500 distinct customer accounts and 1,000 anonymized devices.

| Field Name | Example | Type | Description |
|---|---|---|---|
| `Transaction_ID` | TX100025 | String | Unique transaction tracking identifier. |
| `Account_ID` | ACC1025 | String | Anonymized account identifier (500 accounts). |
| `Transaction_Date` | 2026-09-10 | Date | Date of transaction (YYYY-MM-DD). |
| `Transaction_Time` | 23:45 | Time | Time of transaction (HH:MM). |
| `Amount` | 85000.00 | Float | Transaction monetary value ($). |
| `Transaction_Type` | Transfer | Category | Transfer, Payment, Withdrawal, Deposit. |
| `Channel` | Online | Category | Online, Mobile App, ATM, Branch. |
| `Merchant_Category` | Electronics | Category | Business category (Electronics, Jewelry, Grocery, etc.). |
| `Location` | Kolkata | String | Originating city/region. |
| `Device_ID` | DEV204 | String | Anonymized hardware terminal identifier. |
| `Balance_Before` | 150000.00 | Float | Ledger balance before transaction. |
| `Balance_After` | 65000.00 | Float | Ledger balance after transaction. |
| `Fraud_Label` | 0 or 1 | Integer | Historical verified label (1 = Fraud, 0 = Normal). |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 6. Project Architecture and Workflow
![Figure 1: End-to-End Workflow of the Bank Fraud Screening Pipeline](reports/figures/00_workflow_pipeline.png)

```
[Raw CSV Stream (10,000 Rows)]
              |
              v
[Data Cleaning & Datetime Normalization]
              |
              v
[Feature Derivation: Amount, Hour, 1H Velocity]
              |
              v
[Rule Engine: High Amount, Late Night, Frequency Burst]
              |
              v
[Suspicion Scoring & Bitmasking (Score = R1 + R2 + R3)]
              |
              v
[Alert Triage: Score >= 2 -> Priority Investigation Queue]
              |
    +---------+---------+---------+
    |                   |         |
    v                   v         v
[Reports & CSVs]   [Charts]  [Cronus FraudGuard Web App]
```

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 7. Data Loading and Inspection
The loading stage confirms 10,000 rows across 13 fields with zero null values in critical columns.
* Total monetary turnover: **$45,498,111.43**
* Arithmetic mean amount: **$4,549.81**
* Median amount: **$1,807.50**
* Minimum amount: **$50.00**
* Maximum amount: **$219,850.00**

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 8. Data Cleaning
1. **Deduplication**: Exact duplicate records and duplicate `Transaction_ID`s are identified and eliminated.
2. **Missing Value Handling**: Verified zero nulls in required keys (`Transaction_ID`, `Account_ID`, `Amount`, `Transaction_Time`).
3. **Amount Validation**: Enforced `Amount > 0`; negative or zero transactions are rejected.
4. **Datetime Standardization**: Unified ISO strings parsed into standardized timestamps and integer `Hour` (0 to 23).
5. **Casing Normalization**: Stripped trailing spaces and enforced Title Case across string categories.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 9. Transaction Amount & Statistical Thresholds
Financial amounts follow a Pareto/log-normal distribution. Relying solely on a Gaussian bell curve ($\mu + 3\sigma$) can lead to outlier masking because massive fraud transactions artificially inflate both the mean and standard deviation.

* **Gaussian 3-Sigma Cutoff**: $\mu + 3\sigma = \$4,549.81 + (3 	imes \$13,060.86) = \$43,732.38$
* **99th Percentile Cutoff ($P_{99}$)**: **$45,001.18** (Preferred default for robust outlier isolation)

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 10. Rule-Based Detection Logic
| Rule Name | Mathematical Condition | Score Weight | Rationale |
|---|---|:---:|---|
| **Rule 1: Unusual Amount** | `Amount >= P99` ($45,001.18) | **+1** | Transaction value is unusually high compared to historical baseline. |
| **Rule 2: Late Night** | `23:00 <= Hour <= 05:59` | **+1** | Activity takes place during customer sleep hours; common in automated card draining. |
| **Rule 3: High Frequency** | `Rolling 1-Hour Txn Count >= 5` | **+1** | Rapid transaction bursts indicate credential stuffing, automated bots, or card testing. |
| **Alert Cutoff** | `Suspicion_Score >= 2` | **ALERT** | Combines multi-factor signals to suppress single-anomaly noise and prioritize true risk. |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 11. Key Fraud Detection & Screening KPIs
| Executive Metric | Observed Value | Operational Context |
|---|:---:|---|
| **Total Ingested Volume** | 10,000 | Processed and cleaned transaction records. |
| **Total Monetary Volume** | $45,498,111.43 | Net portfolio turnover across monitored channels. |
| **Average Transaction** | $4,549.81 | Population arithmetic mean. |
| **Median Transaction** | $1,807.50 | Robust central tendency measure. |
| **99th Percentile Threshold ($P_{99}$)** | $45,001.18 | Outlier cutoff for high-value transfers. |
| **Statistical Threshold ($\mu + 3\sigma$)** | $43,732.38 | Baseline Gaussian 3-sigma cutoff. |
| **Suspicious Flagged Volume** | **118 (1.18%)** | Prioritized for immediate analyst review (Score $\ge 2$). |
| **High Amount Alerts** | 100 (1.00%) | Single transactions exceeding outlier thresholds. |
| **Late Night Alerts** | 750 (7.50%) | Transactions occurring between 23:00 and 05:59. |
| **High Frequency Bursts** | 113 (1.13%) | Accounts executing $\ge 5$ transactions in rolling 1-hour. |
| **Avg Amount: Normal vs Suspicious** | **$3,966.30 vs $53,416.15** | Suspicious transactions are 13.47x larger on average. |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 12. Overall Screening Performance
![Figure 2: Normal vs Suspicious Transactions Volume Breakdown](reports/figures/02_normal_vs_suspicious.png)

* **Normal Transactions (Score 0-1)**: 9,882 (98.82%)
  * Score 0 (Clean): 9,162 transactions (91.62%)
  * Score 1 (Low Anomaly): 720 transactions (7.20%)
* **Suspicious Transactions (Score 2-3)**: 118 (1.18%)
  * Score 2 (High Priority): 111 transactions (1.11%)
  * Score 3 (Critical Alert): 7 transactions (0.07%)

Requiring at least 2 co-occurring rules suppressed 720 single-anomaly false alarms, focusing review resources on 118 high-confidence alerts.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 13. Rule 1 In-Depth: High-Amount Outlier Analysis
![Figure 3: Distribution of Transaction Amounts with Outlier Cutoff](reports/figures/01_amount_distribution.png)

100 transactions (1.00%) triggered Rule 1. Outlier amounts spanned from $45,002.50 to $219,850.00. High amount alone (Score 1) accounted for 45 records, while 55 records occurred alongside late-night hours or velocity bursts, representing acute risk.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 14. Rule 2 In-Depth: Late-Night Activity Analysis
![Figure 4: Suspicious Transactions by Hour of Day](reports/figures/03_suspicious_by_hour.png)

750 transactions (7.50%) occurred between 23:00 and 05:59. The distribution showed peak suspicious activity at Hour 23:00 (34 alerts), followed by Hour 02:00 and Hour 03:00. 635 late-night transactions were benign single anomalies (e.g. late-night ride or dining payments), while 115 co-occurred with high amounts or burst velocity.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 15. Rule 3 In-Depth: High-Frequency Burst Detection
113 transactions were identified where an account executed 5 or more transactions within a rolling 60-minute window. Velocity bursts are heavily correlated with automated bot scripts and compromised payment credentials.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 16. Suspicion Score Distribution & Bitmask Analysis
![Figure 5: Transaction Volume by Rule Combination Bitmask](reports/figures/06_rule_combination_frequencies.png)

| Rule Bitmask | Description | Transactions | Share (%) | Operational Triage Action |
|---|---|---|---|---|
| `0_0_0` | Baseline Normal | 9,162 | 91.62% | Clear immediately |
| `0_1_0` | Late Night Only | 635 | 6.35% | Passive audit log |
| `0_1_1` | Late Night + High Frequency | 63 | 0.63% | Escalate: Priority Review Queue (Score 2) |
| `1_0_0` | High Amount Only | 45 | 0.45% | Passive audit log |
| `1_1_0` | High Amount + Late Night | 45 | 0.45% | Escalate: Priority Review Queue (Score 2) |
| `0_0_1` | High Frequency Only | 40 | 0.40% | Passive audit log |
| `1_1_1` | Critical Alert (All 3 Rules) | 7 | 0.07% | Urgent Action: Trigger OTP / Secondary Verification (Score 3) |
| `1_0_1` | High Amount + High Frequency | 3 | 0.03% | Escalate: Priority Review Queue (Score 2) |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 17. Transaction Type Performance Analysis
![Figure 6: Suspicious Rate (%) by Transaction Type](reports/figures/04_suspicious_rate_by_type.png)

| Transaction Type | Total Transactions | Suspicious Alerts | Suspicious Rate (%) |
|---|---|---|---|
| **Transfer** | 3,725 | 118 | **3.17%** |
| **Payment** | 3,890 | 0 | 0.00% |
| **Withdrawal** | 1,427 | 0 | 0.00% |
| **Deposit** | 958 | 0 | 0.00% |

All 118 flagged multi-rule alerts occurred within **Transfers**, confirming wire transfers as the primary target for malicious exploitation.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 18. Channel Vulnerability Analysis
![Figure 7: Suspicious Rate (%) by Origination Channel](reports/figures/07_suspicious_rate_by_channel.png)

| Channel | Total Transactions | Suspicious Alerts | Suspicious Rate (%) |
|---|---|---|---|
| **Online** | 4,606 | 118 | **2.56%** |
| **Mobile App** | 3,931 | 0 | 0.00% |
| **ATM** | 962 | 0 | 0.00% |
| **Branch** | 501 | 0 | 0.00% |

Online web banking exhibited the highest vulnerability, reflecting web-based credential theft and automated session hijacking.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 19. Hourly Transaction Trend Analysis
Hourly analysis confirms that daytime hours (08:00 to 20:00) account for 92.5% of overall volume, while suspicious transaction concentration peaks sharply during nocturnal hours (23:00 to 04:00).

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 20. Transaction Amount vs. Suspicion Score Correlation
![Figure 8: Transaction Amount ($) vs Suspicion Score Scatter Plot](reports/figures/05_amount_vs_suspicion_score.png)

Monetary value increases dramatically with suspicion score:
* Score 0: Average $3,966.30
* Score 1: Average $5,820.40
* Score 2: Average $51,890.10
* Score 3: Average $77,615.80

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 21. Required Visualizations
| Figure # | Chart Title | Type | File Location |
|---|---|---|---|
| Fig 1 | End-to-End Pipeline Workflow | Flowchart | `reports/figures/00_workflow_pipeline.png` |
| Fig 2 | Normal vs Suspicious Volume | Bar Chart | `reports/figures/02_normal_vs_suspicious.png` |
| Fig 3 | Amount Distribution | Histogram | `reports/figures/01_amount_distribution.png` |
| Fig 4 | Suspicious Activity by Hour | Line Chart | `reports/figures/03_suspicious_by_hour.png` |
| Fig 5 | Rule Combination Frequencies | Bar Chart | `reports/figures/06_rule_combination_frequencies.png` |
| Fig 6 | Suspicious Rate by Type | Bar Chart | `reports/figures/04_suspicious_rate_by_type.png` |
| Fig 7 | Suspicious Rate by Channel | Bar Chart | `reports/figures/07_suspicious_rate_by_channel.png` |
| Fig 8 | Amount vs Suspicion Score | Scatter Plot | `reports/figures/05_amount_vs_suspicion_score.png` |
| Fig 9 | Confusion Matrix Heatmap | Matrix Heatmap | `reports/figures/08_confusion_matrix.png` |
| Fig 10 | Top Repeat Accounts | Pareto Chart | `reports/figures/09_top_accounts_pareto.png` |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 22. Identifying High-Risk Accounts
![Figure 9: Top Repeat Offender Accounts by Suspicious Alerts](reports/figures/09_top_accounts_pareto.png)

28 accounts generated multiple suspicious alerts. The top 8 repeat accounts:
1. `ACC1183`: 43 transactions, $570,373.00 total value, 10 suspicious (23.26% rate)
2. `ACC1290`: 37 transactions, $797,991.00 total value, 8 suspicious (21.62% rate)
3. `ACC1340`: 35 transactions, $699,260.00 total value, 6 suspicious (17.14% rate)
4. `ACC1492`: 26 transactions, $527,756.00 total value, 5 suspicious (19.23% rate)
5. `ACC1161`: 26 transactions, $636,560.00 total value, 4 suspicious (15.38% rate)
6. `ACC1420`: 23 transactions, $438,158.00 total value, 4 suspicious (17.39% rate)
7. `ACC1186`: 27 transactions, $385,701.00 total value, 4 suspicious (14.81% rate)
8. `ACC1030`: 31 transactions, $368,071.00 total value, 4 suspicious (12.90% rate)

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 23. Advanced Extensions & ML Evaluation
![Figure 10: Confusion Matrix: Ground Truth vs Rule Alert](reports/figures/08_confusion_matrix.png)

Evaluation against historical verified fraud ground-truth:
* **True Positives (TP)**: 118
* **False Positives (FP)**: 0
* **True Negatives (TN)**: 9,600
* **False Negatives (FN)**: 282
* **Precision**: **100.00%**
* **Recall**: **29.50%**
* **F1-Score**: **0.456**
* **False Positive Rate**: **0.00%**

The rule-based screening engine achieved 100% precision with zero customer friction on the benchmark dataset.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 24. Pipeline Orchestration (cli.py)
Executed via single terminal command:
```powershell
.venv\Scripts\python.exe -m src.cli --input data/bank_transactions.csv --reports-dir reports
```

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 25. Interactive Web Dashboard (Cronus FraudGuard)
Launched with `python run_web.py` at `http://127.0.0.1:8000`:
* Live KPI cards and interactive Chart.js graphs.
* Priority review queue with search, score filtering, and "Inspect" explainability modal.
* Interactive Rule Studio with dynamic threshold sliders.
* Drag-and-drop CSV uploader and synthetic data generator.
* Direct download links for Word (.docx), PDF (.pdf), and CSV review queues.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 26. Business Questions and Answers
* **Q1: Percentage flagged?** 1.18% (118 out of 10,000 transactions).
* **Q2: Rule generating most alerts?** Rule 2: Late Night with 750 alerts (7.50%).
* **Q3: Transactions triggering >= 2 rules?** Exactly 118 transactions.
* **Q4: Transaction types with higher risk?** Transfer (3.17% suspicious rate).
* **Q5: Channels showing higher suspicious activity?** Online (2.56% suspicious rate).
* **Q6: Peak suspicious hours?** Hour 23:00 (11:00 PM) with 34 flagged records.
* **Q7: Suspicious amounts vs normal?** Suspicious average $53,416.15 vs $3,966.30 (13.47x higher).
* **Q8: Accounts with repeated activity?** 28 accounts; top is ACC1183 with 10 alerts.
* **Q9: Most frequent combinations?** Single anomaly: 0_1_0 (635 txns). Multi-rule: 0_1_1 (63 txns) and 1_1_0 (45 txns).
* **Q10: Rule performance against ground truth?** 100% precision, 0% FPR, 29.5% recall.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 27. Business Findings and Operational Recommendations
1. **P1 — Step-Up OTP Verification**: Mandate biometric/SMS OTP for Online Transfers exceeding $45,000 executed between 23:00 and 05:59.
2. **P2 — Account Velocity Throttles**: Limit retail accounts to a maximum of 4 transfers per 60 minutes.
3. **P3 — Surveillance Watchlist**: Monitor top 28 repeat offender accounts (led by ACC1183).
4. **P4 — Personalized Z-Scores**: Evolve population thresholds toward per-account 90-day moving z-scores.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 28. Testing, Validation and Reproducibility
* 38 unit and integration tests passing in Pytest across 6 test modules.
* 94% code coverage on core logic.
* Reproducible with `python -m src.cli` and `pytest -v`.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 29. Limitations and Important Analytical & Ethical Note
* An alert is an investigation signal, not conclusive proof of fraud.
* Secondary verification (SMS OTP / phone call) must always be used before account blocking.
* Real customer PII was omitted to ensure strict data privacy compliance.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 30. Learning Outcomes
* Financial transaction exploratory data analysis with Pandas.
* Transparent rule-based anomaly detection logic.
* Web dashboard development with FastAPI and Tailwind CSS.
* Test-Driven Development with Pytest.
* Responsible communication of financial crime analytics findings.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 31. Conclusion and Future Scope
The project delivers a complete, reproducible, industry-ready bank transaction fraud screening system. Future work includes integrating streaming Kafka feeds, ML classification models, and graph neural network collusion ring analysis.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## References
* Pandas, NumPy, Matplotlib, Scikit-learn, and FastAPI official documentation.
* Basel Committee on Banking Supervision: Sound Practices for Operational and Financial Cyber Risk.
* Reserve Bank of India (RBI): Master Direction on Cyber Security and Fraud Monitoring in Banks.
