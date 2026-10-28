# Architectural & Technical Decision Log

| Decision ID | Date | Topic | Decision Made | Alternatives Considered | Rationale |
|---|---|---|---|---|---|
| **DEC-001** | 2026-10-28 | Runtime & Environment | Python 3.11 with `uv` virtual environment (`.venv`) | Python 3.14 system, Conda | Python 3.11 has full binary wheel compatibility for scientific stack (`pandas`, `numpy`, `scipy`, `matplotlib`). `uv` provides instant dependency resolution. |
| **DEC-002** | 2026-10-28 | Dataset Sourcing | Synthetic Generator conforming to Section 6 schema & Section 7 privacy | External Kaggle download, static mock array | Standalone reproducible generator avoids external network dependencies, strictly adheres to privacy mandate, and guarantees ground truth labels. |
| **DEC-003** | 2026-10-28 | Amount Outlier Threshold | Implement both $\mu + 3\sigma$ and $99\text{th}$ percentile ($P_{99}$), with $P_{99}$ as default | Only $\mu + 3\sigma$, only IQR | Financial amounts are heavily skewed. $P_{99}$ provides robust, interpretable cutoffs without suffering from outlier-induced variance inflation. |
| **DEC-004** | 2026-10-28 | Suspicion Threshold | Set alert cutoff at `Suspicion_Score >= 2` | Cutoff at $\ge 1$, weighted scoring | Single rules (Score 1) produce excessive false positives (e.g. normal late-night taxi payment). Requiring at least 2 co-occurring rules focuses investigation on high-risk events. |
| **DEC-005** | 2026-10-28 | Visualization Backend | Matplotlib headless backend (`Agg`) saving directly to PNG files | Interactive GUI (`plt.show()`), Seaborn, Plotly | Headless `Agg` backend executes reliably in CLI/terminal environments without hanging or needing desktop window server focus. |
| **DEC-006** | 2026-10-28 | Code Structure | Modular Python package (`src/`) with CLI + Pytest suite | Single monolithic Jupyter notebook | Satisfies industry-oriented software engineering standards, facilitates automated TDD testing, and enables batch automation. |
