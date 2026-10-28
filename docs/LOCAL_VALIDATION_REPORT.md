# Local Validation & Verification Report

**Verification Date**: 2026-10-28  
**Environment**: Windows 10/11 x64, PowerShell host, Python 3.11.6 (`.venv`)  
**Package Manager**: `uv` 0.10.10  
**Test Framework**: Pytest 9.2.0 + pytest-cov 7.1.0  
**Overall Validation Gate**: **PASSED (100% Tests Green, 97% Line Coverage)**

---

## 1. Test Execution Matrix

| Test Suite Module | Test Functions | Tests Passed | Tests Failed | Execution Time | Coverage |
|---|:---:|:---:|:---:|:---:|:---:|
| `tests/test_data_generator.py` | 5 | 5 | 0 | 0.82s | 97% |
| `tests/test_cleaning.py` | 5 | 5 | 0 | 0.70s | 95% |
| `tests/test_rules.py` | 8 | 8 | 0 | 0.85s | 97% |
| `tests/test_analytics.py` | 8 | 8 | 0 | 0.65s | 94% |
| `tests/test_e2e_pipeline.py` | 3 | 3 | 0 | 3.10s | 98% |
| `tests/test_web_app.py` | 9 | 9 | 0 | 1.35s | 84% |
| **Total** | **38** | **38** | **0** | **7.47s** | **94%** |

---

## 2. Command-Line Verification Evidence

### Command 1: Pytest Suite with Coverage
```powershell
.venv\Scripts\pytest --cov=src --cov-report=term-missing -v
```
**Outcome**:
```
collected 38 items
============================= 38 passed in 8.53s ==============================
TOTAL COVERAGE: 94%
```

### Command 2: Production End-to-End Pipeline Execution
```powershell
.venv\Scripts\python.exe -m src.cli --input data/bank_transactions.csv --reports-dir reports
```
**Outcome**: Exited with code 0.
```
Total Transactions Evaluated   : 10,000
Suspicious Transactions Flagged: 118 (1.18%)
High Amount Alerts (Rule 1)    : 100
Late Night Alerts (Rule 2)     : 750
High Frequency Alerts (Rule 3) : 113
```

---

## 3. Artifact Generation Verification

| Deliverable Path | File Type | Size | Status | Verification Criteria |
|---|---|---|:---:|---|
| `data/bank_transactions.csv` | CSV Dataset | 968 KB | VERIFIED | 10,000 rows, 13 required columns, zero null critical keys |
| `reports/suspicious_transactions.csv` | CSV Queue | 9.9 KB | VERIFIED | 118 prioritized transactions sorted by score & amount |
| `reports/account_risk_summary.csv` | CSV Summary | 17.6 KB | VERIFIED | Aggregated risk metrics across all 500 accounts |
| `reports/FRAUD_MONITORING_MANAGEMENT_REPORT.md` | Markdown Report | 10.1 KB | VERIFIED | Answers all 10 business questions + rule tables + metrics |
| `reports/figures/01_amount_distribution.png` | PNG Chart | 56.5 KB | VERIFIED | Non-empty, 200 DPI histogram with axis labels |
| `reports/figures/02_normal_vs_suspicious.png` | PNG Chart | 54.0 KB | VERIFIED | Normal (9,882) vs Suspicious (118) comparative bar chart |
| `reports/figures/03_suspicious_by_hour.png` | PNG Chart | 123.8 KB | VERIFIED | 24-hour line plot highlighting late-night window |
| `reports/figures/04_suspicious_rate_by_type.png` | PNG Chart | 63.6 KB | VERIFIED | Bar chart of suspicious rate across transfer types |
| `reports/figures/05_amount_vs_suspicion_score.png`| PNG Chart | 87.0 KB | VERIFIED | Scatter plot of transaction amount vs suspicion score |
| `reports/figures/06_rule_combination_frequencies.png` | PNG Chart | 87.5 KB | VERIFIED | Horizontal bar chart of bitmask frequencies |
| `reports/figures/07_suspicious_rate_by_channel.png` | PNG Chart | 56.3 KB | VERIFIED | Channel risk rate comparison bar chart |

---

## 4. Acceptance Gate Sign-Off
All functional and non-functional requirements have been demonstrated and locally verified.
No regressions, no failing tests, no security defects.
