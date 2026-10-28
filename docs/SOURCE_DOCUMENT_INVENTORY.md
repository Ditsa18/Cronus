# Source Document Inventory

## 1. Document Overview
* **Document Title**: Bank Transaction Fraud Detection: Rule-Based Fraud Analytics — Industry-Oriented Student Project
* **Format**: Embedded Comprehensive Project Specification & Brief (Sections 1–42)
* **Date Received**: 2026-10-28
* **Context**: Junior Data Analyst portfolio/internship capstone at a retail banking institution.
* **Target Audience**: Internship evaluators, academic mentors, senior fraud risk managers.

## 2. Inventory of Sections and Acceptance Elements

| Section # | Section Heading | Key Content & Mandates |
|---|---|---|
| **1** | Project Overview | Build explainable, rule-based screening system using amount, time, and frequency to flag records for investigation without prematurely accusing customers. |
| **2** | Business Scenario | Screening layer for fraud monitoring team: identify large transactions, late-night hours, high burst frequencies, combine into score, summarize patterns. |
| **3** | Project Objectives | 11 core analytical goals: load, clean, analyze amounts, detect outliers, late-night, frequency, score, flag, group summaries, matplotlib visual charts, executive summary. |
| **4** | Libraries Required | Pandas, NumPy, Matplotlib (and extensions for evaluation like Scikit-learn). |
| **5 & 6** | Suggested Dataset & Fields | `bank_transactions.csv` with fields: `Transaction_ID`, `Account_ID`, `Transaction_Date`, `Transaction_Time`, `Amount`, `Transaction_Type`, `Channel`, `Merchant_Category`, `Location`, `Device_ID`, `Balance_Before`, `Balance_After`, `Fraud_Label`. |
| **7** | Privacy Rule | Use only anonymized or synthetic data; zero real customer PII (no real card numbers, passwords, PINs, CVVs, names, addresses). |
| **8** | Load and Inspect Data | Inspection commands: `.head()`, `.shape`, `.columns`, `.info()`, `.describe(include="all")`. |
| **9** | Data Cleaning | Drop exact duplicates, check duplicate IDs, parse datetimes, handle nulls, validate amounts (positive) and balances, standardize categories, document all cleaning actions. |
| **10** | Basic Transaction Analysis | Descriptive statistics: total count, total volume, mean, median, max. |
| **11 & 12** | Amount Rules | Rule 1A: Mean + 3 StdDev. Rule 1B: 99th percentile threshold for skewed distributions. |
| **13** | Late-Night Rule | Rule 2: Transactions between 23:00 (11 PM) and 05:59 (5:59 AM) inclusive (`Hour >= 23` or `Hour <= 5`). |
| **14–16** | High-Frequency Rule | Rule 3: Rolling 1-hour window per account with $\ge 5$ transactions. |
| **17 & 18** | Combine Rules & Scoring | `Suspicion_Score = Rule_High_Amount + Rule_Late_Night + Rule_High_Frequency`. Score $\ge 2$ triggers `Suspicious = 1`. Explain scores 0, 1, 2, 3. |
| **19 & 20** | Suspicious Inspection & Summary | Prioritized manual review table; global KPI summary (total, suspicious count, %, rule breakdown). |
| **21–25** | Detailed Drilldowns | Grouped analysis by `Transaction_Type`, `Channel`, `Hour`, `Account_ID`, and high-value suspicious subset ($\ge 99\text{th}$ percentile). |
| **26–30** | Visualizations | At least 6 charts: Amount histogram, Normal vs Suspicious bar chart, Suspicious by hour line chart, Suspicious rate by type bar chart, Amount vs Suspicion scatter plot, etc. |
| **31 & 32** | Pattern & Combination Analysis | Summary of triggered rules and bitmask combinations (`Amount_Night_Freq`, e.g., `1_1_0`). |
| **33** | Historical Fraud Evaluation | Confusion matrix, Precision, Recall, F1 against ground truth `Fraud_Label`. |
| **34** | Business Questions (1–10) | Ten specific business questions to answer with quantified metrics. |
| **35** | Deliverables | Python codebase, cleaned dataset, rule-definition table, reports, at least 6 charts, management summary, evaluation. |
| **36** | Recommended Rule Table | Tabular summary of conditions, scores, and business rationale. |
| **37** | Advanced Extensions | Velocity windows, ML baseline, location/device anomaly, customer profiling. |
| **38 & 39** | Analytical & Ethical Notes | Alert $\neq$ guilt, false positives, operational review workflows. |
| **40–42** | Outcomes & Final Challenge | Portfolio presentation, answering investigation prioritization challenge. |

## 3. Completeness Verification
All 42 sections were ingested verbatim from the user prompt. No pages or requirements were missing or omitted.
