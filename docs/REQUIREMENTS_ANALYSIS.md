<p align="left">
  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">
</p>

# Requirements Analysis & Specifications Matrix

## 1. Overview & Business Goal
The objective is to implement a robust, explainable, rule-based fraud analytics system for banking transactions.
Instead of an opaque black-box machine learning model that acts without justification, this system evaluates every transaction against transparent domain-specific heuristic rules, assigns an interpretable suspicion score ($0$ to $3$), flags records exceeding a threshold ($\ge 2$) for human-in-the-loop compliance review, and outputs management reports and visualizations.

---

## 2. Functional Requirements (FR)

| Req ID | Requirement Title | Detailed Specification | Acceptance Criteria |
|---|---|---|---|
| **FR-001** | Synthetic Data Generation | Generate realistic, synthetic banking transaction dataset conforming to Section 6 schema and Section 7 privacy mandates ($N \ge 1,000$ records, realistic accounts, dates, hours, amounts, channels, types, balances, and ground truth `Fraud_Label`). | Dataset passes privacy checks; contains expected columns; exhibits expected distributions and anomalies. |
| **FR-002** | Data Loading & Inspection | Ingest CSV data via Pandas, output dimensions, column schemas, summary stats (`info()`, `describe(include='all')`), and missing value counts. | Inspection outputs printed cleanly without runtime errors. |
| **FR-003** | Data Cleansing & Validation | Deduplicate exact duplicate rows; verify unique `Transaction_ID`; parse `Transaction_Date` and `Transaction_Time`; extract `Hour`; filter or correct negative amounts; validate balance continuity where applicable (`Balance_Before - Amount \approx Balance_After`). | Zero unhandled nulls in required fields; valid datetime features; cleaning decisions logged. |
| **FR-004** | Descriptive Amount Analytics | Compute global summary statistics: Total count, total volume (sum), mean, median, standard deviation, min, max, 25th, 75th, 95th, and 99th percentiles. | Summary dictionary and console outputs generated with high precision. |
| **FR-005** | Rule 1: High Amount Detection | Calculate statistical threshold ($\mu + 3\sigma$) and percentile threshold ($99\text{th}$ percentile). Tag `Rule_High_Amount` ($1$ if `Amount > threshold`, else $0$). Provide configurable choice between $\mu + 3\sigma$ and $P_{99}$. | Indicator column created; outlier counts logged; handles skewed distributions. |
| **FR-006** | Rule 2: Late-Night Activity Detection | Tag `Rule_Late_Night` ($1$ if `Hour >= 23` or `Hour <= 5`, else $0$). Standard window 11:00 PM to 05:59 AM. | Proper boolean evaluation over `Hour` column. |
| **FR-007** | Rule 3: High-Frequency Burst Detection | Compute rolling 1-hour count per account (`Txn_Count_1H`). Tag `Rule_High_Frequency` ($1$ if `Txn_Count_1H >= 5`, else $0$). Provide fallback hourly window grouping method. | Rolling window correctly partitioned by `Account_ID` over sorted `Transaction_Datetime`. |
| **FR-008** | Suspicion Score Aggregation | Compute `Suspicion_Score = Rule_High_Amount + Rule_Late_Night + Rule_High_Frequency` (range 0 to 3). Compute `Suspicious = (Suspicion_Score >= 2).astype(int)`. | Both columns generated; distribution matches rule sums. |
| **FR-009** | Prioritized Manual Review Queue | Filter records with `Suspicious == 1`, order by `Suspicion_Score` descending, then `Amount` descending. Format for investigators. | Formatted dataframe exportable to CSV and Markdown. |
| **FR-010** | Multidimensional Drilldowns | Compute aggregated transaction counts, suspicious counts, and suspicious rates across: (a) Transaction Type, (b) Channel, (c) Hour of Day, (d) Account ID (top repeat offenders), and (e) High-Value Suspicious subset. | Aggregations match total counts exactly; rates represented as percentages. |
| **FR-011** | Visual Analytics Suite | Generate at least 6 high-resolution charts using Matplotlib: (1) Amount distribution, (2) Normal vs Suspicious count, (3) Suspicious volume by hour, (4) Suspicious rate by transaction type, (5) Amount vs Suspicion Score scatter plot, (6) Rule combination frequency breakdown, (7) Channel-wise suspicious rate. Save to disk. | PNG files rendered and saved to `reports/figures/`. |
| **FR-012** | Rule Combination Analysis | Construct bitmask string `Rule_Combination` (`HighAmt_Night_Freq`, e.g., `1_1_0`). Compute frequency table of all 8 possible combinations ($2^3$). | Clear explanation of prevalent multi-rule patterns. |
| **FR-013** | Ground-Truth Fraud Evaluation | If `Fraud_Label` is present, compute Confusion Matrix (TP, FP, TN, FN), Precision, Recall, F1-Score, and False Positive Rate. | Evaluation report clearly highlighting rule-based precision vs recall tradeoffs. |
| **FR-014** | Business Questions Answering | Answer all 10 explicit business questions from Section 34 with concrete metrics, percentages, and evidence. | Narrative section in report directly answering questions 1 through 10. |

---

## 3. Non-Functional Requirements (NFR)

* **NFR-001: Explainability**: Every flagged alert must provide human-understandable audit reasons (which rules triggered and why).
* **NFR-002: Performance & Scalability**: Clean processing of $10,000+$ records in $<5$ seconds on standard laptop CPU.
* **NFR-003: Reproducibility**: Seeded random state (`random_state=42`) for synthetic data generator to allow identical replication.
* **NFR-004: Code Modularity & TDD**: Clean separation of concerns into `data_generator.py`, `cleaning.py`, `rules.py`, `analytics.py`, `visualization.py`, and `cli.py` backed by comprehensive Pytest suite.
* **NFR-005: Zero Leakage / Privacy Compliance**: Zero PII (GDPR/RBI banking privacy principles).

---

## 4. Input / Output Data Contract

### Input: `bank_transactions.csv`
| Column Name | Expected Type | Description |
|---|---|---|
| `Transaction_ID` | String / Object | Unique ID (e.g., `TX100001`) |
| `Account_ID` | String / Object | Account ID (e.g., `ACC1001`) |
| `Transaction_Date` | String (YYYY-MM-DD) | Date of transaction |
| `Transaction_Time` | String (HH:MM or HH:MM:SS) | Time of transaction |
| `Amount` | Float | Transaction amount |
| `Transaction_Type` | String / Category | `Transfer`, `Withdrawal`, `Payment`, `Deposit`, etc. |
| `Channel` | String / Category | `Online`, `Mobile App`, `ATM`, `POS / Branch` |
| `Merchant_Category` | String / Category | `Electronics`, `Grocery`, `Jewelry`, `Entertainment`, `Utilities` |
| `Location` | String | City or region |
| `Device_ID` | String | Unique hardware device ID |
| `Balance_Before` | Float | Balance before transaction |
| `Balance_After` | Float | Balance after transaction |
| `Fraud_Label` | Integer (0 or 1) | Historical ground truth label |

### Output Deliverables:
1. `data/bank_transactions_raw.csv` & `data/bank_transactions_cleaned.csv`
2. `reports/suspicious_transactions.csv` & `reports/account_risk_summary.csv`
3. `reports/figures/*.png` (7 high-quality visualization figures)
4. `reports/FRAUD_MONITORING_MANAGEMENT_REPORT.md`
5. Test coverage report (`pytest --cov`)
