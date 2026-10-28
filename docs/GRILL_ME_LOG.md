# Requirements Challenge Log (Grill Me)

This document records the critical examination of the project requirements, identifying technical ambiguities, edge cases, risks, and justified decisions.

---

## 1. Challenge & Decisions Register

### Concern ID: C-001 — Dataset Sourcing vs. Privacy Compliance
* **Relevant Requirement**: Section 5, 6, 7 (Suggested Dataset & Privacy Rule).
* **Question / Ambiguity**: The brief suggests `bank_transactions.csv` but explicitly prohibits real customer financial data. No existing CSV was provided in the repository workspace.
* **Evidence Available**: Section 5 explicitly permits students to create a "synthetic educational dataset" conforming to Section 6 fields.
* **Risk If Unresolved**: Using real data violates privacy regulations; waiting for manual upload halts progress.
* **Recommended Decision**: Implement a high-fidelity, statistically grounded synthetic data generator (`src/data_generator.py`) that generates 10,000 realistic transactions with seeded randomness (`seed=42`), normal diurnal patterns, realistic account balances, intentional anomalies, and a ground-truth `Fraud_Label`.
* **Human Input Required**: No (autonomous resolution per Phase 3 Rule A & B).
* **Final Resolution**: Built-in synthetic generator creates `data/bank_transactions.csv` conforming strictly to all 13 specified fields.

---

### Concern ID: C-002 — Rolling 1-Hour Calculation Across Accounts
* **Relevant Requirement**: Section 14 & 15 (High-Frequency Transaction Detection).
* **Question / Ambiguity**: `rolling("1h", on="Transaction_Datetime")` in Pandas can be sensitive to duplicate timestamps and index ordering. Section 15 notes an alternative hourly window grouping if rolling fails.
* **Evidence Available**: Pandas `rolling('1h')` requires non-decreasing monotonic datetime indexes per group.
* **Risk If Unresolved**: If timestamps are not sorted per account, rolling will raise a `ValueError`.
* **Recommended Decision**: Sort strictly by `["Account_ID", "Transaction_Datetime"]`, set `Transaction_Datetime` as index or use `.rolling('1h', on='Transaction_Datetime')`, and verify with unit tests. Provide fallback logic in case of missing timestamps.
* **Human Input Required**: No.
* **Final Resolution**: Robust sorting and rolling calculation implemented with automated tests and a fallback grouping helper.

---

### Concern ID: C-003 — Amount Threshold Strategy: Mean+3Std vs. 99th Percentile
* **Relevant Requirement**: Section 11 & 12 (Amount Threshold Rules).
* **Question / Ambiguity**: Which threshold should be used for `Rule_High_Amount` when scoring? Section 11 specifies `mean + 3*std`, while Section 12 notes that financial amounts are skewed and introduces `amount_99`.
* **Evidence Available**: In heavy-tailed exponential or Pareto distributions, extreme fraud amounts artificially elevate both mean and standard deviation, causing $\mu + 3\sigma$ to suffer from outlier masking.
* **Risk If Unresolved**: Inconsistent scoring logic across different analysis sections.
* **Recommended Decision**: Implement both: calculate both thresholds, log their values, and make `Rule_High_Amount` configurable with the 99th percentile ($P_{99}$) as the default recommended method, while also recording `Rule_High_Amount_3Sigma` for comparative audit.
* **Human Input Required**: No.
* **Final Resolution**: Default `Rule_High_Amount` uses $P_{99}$ with dual reporting of $\mu + 3\sigma$.

---

### Concern ID: C-004 — Late-Night Boundary Handling
* **Relevant Requirement**: Section 13 (`Hour >= 23` or `Hour <= 5`).
* **Question / Ambiguity**: Are 05:00 to 05:59 considered late night?
* **Evidence Available**: The text states: *"transactions occurring from 11:00 PM through 5:59 AM"*. In Python integer hour extraction, `dt.hour` returns integers $0$ to $23$.
* **Risk If Unresolved**: Off-by-one error (e.g. including 06:00 or missing 05:30).
* **Recommended Decision**: `Hour == 5` covers all minutes between 05:00:00 and 05:59:59. Therefore, `(df["Hour"] >= 23) | (df["Hour"] <= 5)` precisely implements 23:00 through 05:59:59.
* **Human Input Required**: No.
* **Final Resolution**: Confirmed `(df["Hour"] >= 23) | (df["Hour"] <= 5)`.

---

### Concern ID: C-005 — Suspicion Score Interpretation & False Positives
* **Relevant Requirement**: Section 17 & 18 (Score combinations & ethical guidelines).
* **Question / Ambiguity**: Should single-rule alerts (Score 1) trigger automated blocking?
* **Evidence Available**: Section 18 states Score 1 is "monitor or review depending on context"; Score 2 is "higher investigation priority"; Section 38 states alerts are not proof of fraud.
* **Risk If Unresolved**: High false-positive rate degrades investigator trust.
* **Recommended Decision**: Define `Suspicious = (Suspicion_Score >= 2).astype(int)` as the primary alert threshold. Score 1 records are tagged for low-priority audit, but not alerted.
* **Human Input Required**: No.
* **Final Resolution**: Standardized on `Suspicion_Score >= 2` for primary alerts, with full visibility into individual rule components.
