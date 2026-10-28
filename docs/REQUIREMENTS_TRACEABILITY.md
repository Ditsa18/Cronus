# Requirements Traceability Matrix (RTM)

This matrix maps every section of the user requirements document to its design, implementation module, test suite, and verification status.

| Req ID | Brief Section | Requirement Description | Design / PRD Mapping | Implementation Component | Verification Test | Status |
|---|---|---|---|---|---|:---:|
| **RTM-001** | Sec 1–4 | Explainable, rule-based screening system | PRD Sec 1, 2 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-002** | Sec 5–7 | Privacy-compliant synthetic dataset | PRD FR-001 | `src/data_generator.py` | `tests/test_data_generator.py` | VERIFIED |
| **RTM-003** | Sec 8–9 | Data loading & cleaning pipeline | PRD FR-002 | `src/cleaning.py` | `tests/test_cleaning.py` | VERIFIED |
| **RTM-004** | Sec 10 | Descriptive summary statistics | PRD FR-002 | `src/analytics.py` | `tests/test_analytics.py` | VERIFIED |
| **RTM-005** | Sec 11 | Rule 1A: Amount Outlier ($\mu + 3\sigma$) | PRD FR-003 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-006** | Sec 12 | Rule 1B: Amount Outlier ($99\text{th}$ percentile) | PRD FR-003 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-007** | Sec 13 | Rule 2: Late-Night Window ($23:00 - 05:59$) | PRD FR-004 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-008** | Sec 14–16 | Rule 3: High-Frequency Window (1-Hour $\ge 5$) | PRD FR-005 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-009** | Sec 17–18 | Suspicion Score (0–3) & Flag ($\ge 2$) | PRD FR-006 | `src/rules.py` | `tests/test_rules.py` | VERIFIED |
| **RTM-010** | Sec 19–20 | Prioritized queue & global summary | PRD FR-007 | `src/analytics.py` | `tests/test_analytics.py` | VERIFIED |
| **RTM-011** | Sec 21–25 | Grouped analysis (Type, Channel, Hour, Account, High Value) | PRD FR-008 | `src/analytics.py` | `tests/test_analytics.py` | VERIFIED |
| **RTM-012** | Sec 26–30 | Matplotlib Visualizations (6+ charts) | PRD FR-009 | `src/visualization.py` | `tests/test_e2e_pipeline.py` | VERIFIED |
| **RTM-013** | Sec 31–32 | Pattern & Bitmask Combination Analysis | PRD FR-008 | `src/analytics.py` | `tests/test_analytics.py` | VERIFIED |
| **RTM-014** | Sec 33 | Historical Ground Truth Evaluation | PRD FR-010 | `src/analytics.py` | `tests/test_analytics.py` | VERIFIED |
| **RTM-015** | Sec 34 | Answer 10 Business Questions | PRD FR-010 | `src/cli.py` & Report | `tests/test_e2e_pipeline.py` | VERIFIED |
| **RTM-016** | Sec 35–39 | Deliverables, Rule Table, Limitations & Ethics | PRD Sec 4, 7 | `README.md`, Report | `tests/test_e2e_pipeline.py` | VERIFIED |
