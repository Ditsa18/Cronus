# Development Plan & Implementation Schedule

## 1. Plan Overview
The development plan is organized into small, test-driven vertical slices following strict TDD (Red -> Green -> Refactor) and local verification release criteria.

---

## 2. Iterative Milestones

### Milestone 1: Environment & Project Scaffolding (Phase 0 & 6)
* Set up virtual environment and install verified dependencies (`pandas`, `numpy`, `matplotlib`, `pytest`, `pytest-cov`, `scikit-learn`, `tabulate`).
* Create project package layout (`src/`, `tests/`, `docs/`, `data/`, `reports/`).
* Configure `pyproject.toml` and pytest test discovery.

### Milestone 2: Synthetic Data Generation (Slice 1)
* **TDD RED**: Write tests in `tests/test_data_generator.py` asserting schema conformity, privacy constraints, seeded randomness, and presence of anomalous records.
* **TDD GREEN**: Implement `src/data_generator.py`.
* **TDD REFACTOR**: Optimize distribution sampling and fraud injection realism.

### Milestone 3: Data Ingestion & Cleansing Engine (Slice 2)
* **TDD RED**: Write tests in `tests/test_cleaning.py` testing duplicate removal, datetime normalization, hour extraction, negative amount filtering, and audit logging.
* **TDD GREEN**: Implement `src/cleaning.py`.
* **TDD REFACTOR**: Ensure memory-efficient Pandas vectorization.

### Milestone 4: Rule Engine & Suspicion Scoring (Slice 3)
* **TDD RED**: Write tests in `tests/test_rules.py` covering Rule 1 (Amount $\mu+3\sigma$ and $P_{99}$), Rule 2 (Late Night), Rule 3 (Rolling 1-Hour Frequency), and Suspicion Score aggregation.
* **TDD GREEN**: Implement `src/rules.py`.
* **TDD REFACTOR**: Optimize rolling window per account and handle edge cases (single transactions, midnight wrap-arounds).

### Milestone 5: Analytics, Profiling & Drilldown Engine (Slice 4)
* **TDD RED**: Write tests in `tests/test_analytics.py` verifying grouping by type, channel, hour, account risk aggregations, bitmask combination table, and confusion matrix calculation.
* **TDD GREEN**: Implement `src/analytics.py`.
* **TDD REFACTOR**: Format tables for both console and CSV/Markdown outputs.

### Milestone 6: Visualization Suite (Slice 5)
* Implement `src/visualization.py` generating the required 7 Matplotlib figures.
* Verify figure generation without headless X-server display errors (`matplotlib.use('Agg')`).

### Milestone 7: CLI Application & End-to-End Orchestration (Slice 6)
* Write integration tests in `tests/test_e2e_pipeline.py`.
* Implement `src/cli.py` with arguments for data generation, input CSV, threshold tuning, and report generation.

### Milestone 8: Management Report & Business Questions (Slice 7)
* Generate final reports: `suspicious_transactions.csv`, `account_risk_summary.csv`, and comprehensive `FRAUD_MONITORING_MANAGEMENT_REPORT.md` answering all 10 business questions.

### Milestone 9: Code Review, Security Audit & Local Release Gate (Phase 11–15)
* Run full test suite with coverage (`pytest --cov=src`).
* Perform independent code review and security audit.
* Complete validation report and final handover.
