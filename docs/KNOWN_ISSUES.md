# Known Issues, Limitations & Future Work

## 1. Known Architectural Limitations

### 1. Population-Level vs. Customer-Specific Baselines
* **Limitation**: The current system applies a global amount threshold (e.g. 99th percentile across all transactions). A \$45,000 transaction from a small student account is treated under the same threshold as a \$45,000 transaction from a high-net-worth business account.
* **Mitigation / Next Step**: Implement per-account rolling z-scores or dynamic percentile thresholds based on the individual customer's 90-day history (Advanced Extension, Section 37).

### 2. Timezone Normalization
* **Limitation**: Timestamps are assumed to be recorded in the bank's home timezone (IST). For international card transactions originating across foreign time zones, local customer time may differ from bank server time.
* **Mitigation**: Add a `Transaction_Timezone` field and convert to customer local time prior to evaluating the Late-Night rule.

### 3. Rule Weighting
* **Limitation**: All three rules contribute an equal weight (+1 point). In reality, a late-night burst of 7 rapid transactions may carry higher inherent risk than a single late-night transaction.
* **Mitigation**: Introduce configurable floating-point weights (e.g., Late Night: 0.8, High Frequency: 1.5, High Amount: 1.2) or calibrate weights via logistic regression (Advanced Extension, Section 37).

---

## 2. Unresolved Defects
* **Zero Critical / Blocker Defects**: All unit and end-to-end tests are passing with 97% line coverage.
