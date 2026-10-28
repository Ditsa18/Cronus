<p align="left">
  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">
</p>

# Test Strategy & Quality Assurance Framework

## 1. Quality Objectives
* Maintain $> 90\%$ test coverage on all core analytical modules.
* Follow Test-Driven Development (TDD): Red -> Green -> Refactor.
* Zero regressions on boundary conditions (e.g. 23:00 boundary, exact 5-transaction burst, negative amounts, duplicate IDs).

---

## 2. Test Pyramid & Layers

```
            / \
           /   \     E2E / CLI Integration Tests
          /     \    (Pipeline smoke tests, full workflow)
         /-------\
        /         \   Module Integration Tests
       /           \  (Rule scoring on cleaned datasets, analytics drilldowns)
      /-------------\
     /               \ Unit Tests
    /                 \(Threshold calculation, time parsing, individual rules)
   /-------------------\
```

### Layer 1: Unit Tests (`tests/test_*.py`)
* `test_data_generator.py`: Verifies row count, schema columns, absence of NaN in critical keys, value ranges (positive amounts, reasonable dates).
* `test_cleaning.py`: Verifies exact duplicate removal, malformed date string handling, negative amount rejection, hour extraction ($0-23$).
* `test_rules.py`:
  * `test_high_amount_statistical`: Checks $\mu + 3\sigma$ threshold calculation.
  * `test_high_amount_percentile`: Checks 99th percentile cutoff.
  * `test_late_night_rule`: Verifies hours 23, 0, 1, 2, 3, 4, 5 return 1; hours 6 through 22 return 0.
  * `test_high_frequency_rule`: Verifies account with 5 transactions in 40 minutes triggers rule, while account with 4 transactions or spaced 2 hours apart does not.
  * `test_suspicion_score`: Verifies summation ($0, 1, 2, 3$) and binary flag ($\ge 2$).
* `test_analytics.py`: Tests grouped aggregations, rate calculation, bitmask strings (`1_1_0`), and confusion matrix outputs against known ground-truth labels.

### Layer 2: Integration & E2E Tests (`tests/test_e2e_pipeline.py`)
* Tests the end-to-end execution of `run_pipeline(...)` from synthetic generation through cleaning, scoring, table aggregation, and figure output.
* Verifies files are written to expected paths with non-zero size.

---

## 3. Test Configuration & Tooling
* **Runner**: `pytest` with verbose output `-v`.
* **Coverage**: `pytest-cov` reporting terminal line coverage and HTML reports.
* **Deterministic Fixtures**: Seeded fixtures with isolated temporary output directories (`tmp_path`).
