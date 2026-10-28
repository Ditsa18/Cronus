# Open Source & Industry Research

## 1. Overview of Fraud Detection Systems in Banking
In modern financial institutions (e.g., JPMorgan Chase, HSBC, Wells Fargo, ICICI Bank), fraud detection operates as a multi-tier defense:
1. **Tier 1 — Heuristic / Rule-Based Filtering**: High-throughput, microsecond-latency deterministic checks (velocity limits, sanctions lists, hard amount thresholds, late-night high-value transfers). These rules are fully explainable, audit-compliant, and immediately actionable.
2. **Tier 2 — Statistical Anomaly & Velocity Profiling**: Rolling window calculations (e.g. transactions per hour, z-scores over 30-day moving windows).
3. **Tier 3 — Machine Learning Models**: Gradient boosting (XGBoost/LightGBM), neural embeddings, and graph neural networks (GNNs) for detecting subtle, evolving collusion patterns.

The student project requirements explicitly focus on **Tier 1 and Tier 2** (explainable, transparent, rule-based screening) to serve as the foundational screening layer before machine learning models are applied.

---

## 2. GitHub & Open-Source Reference Architectures

We surveyed established GitHub patterns and open-source financial crime analysis tools:

### Reference A: FinTech Transaction Rule Engines (e.g., Marble, Apache Flink CEP patterns)
* **Architecture**: Event-driven or batch processing where each transaction is tested against a sequence of boolean rules. Each rule generates a structured audit reason code.
* **Key Strength**: Complete explainability. Instead of an uninterpretable score $0.87$, the analyst receives an explicit reason string: `["HIGH_AMOUNT", "LATE_NIGHT_WINDOW"]`.
* **Adoption in our design**: Implemented in `src/rules.py` through individual rule functions that output both boolean flags and descriptive reason tags.

### Reference B: Credit Card Fraud Detection Benchmarks (ULB ML Group / Kaggle)
* **Dataset characteristics**: Highly skewed amounts; fraud rate typically $<1\%$; power-law / log-normal distributions.
* **Key Lesson**: Traditional $\mu + 3\sigma$ assumes a Gaussian distribution. In financial datasets with heavy right tails, extreme fraud amounts inflate $\mu$ and $\sigma$, leading to outlier masking. Robust statistics (such as the 99th percentile $P_{99}$ or IQR) provide significantly more reliable cutoffs.
* **Adoption in our design**: We implement both Section 11's $\mu + 3\sigma$ and Section 12's 99th percentile ($P_{99}$), logging both and contrasting their behavior.

### Reference C: Velocity & Rolling Window Patterns in Pandas
* **Challenge**: Calculating rolling transaction counts within time windows per account.
* **Optimal Implementation**:
  ```python
  df = df.sort_values(["Account_ID", "Transaction_Datetime"])
  df["Txn_Count_1H"] = (
      df.groupby("Account_ID")
        .rolling("1h", on="Transaction_Datetime")["Transaction_ID"]
        .count()
        .reset_index(level=0, drop=True)
        .values
  )
  ```
* **Fallback Strategy**: Grouping by `[Account_ID, Date, Hour]` for environments where sub-second rolling windows encounter duplicate timestamps.

---

## 3. Evaluation Dimensions & Decision
All components will be implemented with clean, modular Python without external proprietary dependencies, ensuring 100% offline reproducibility and strict adherence to the project brief.
