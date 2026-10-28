<p align="left">
  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">
</p>

# Executive Fraud Monitoring & Suspicious Activity Analytics Report

**Prepared For**: Bank Fraud Monitoring Steering Committee & Risk Audit  
**Role**: Junior Data Analyst / Principal Autonomous Fraud Systems Engineer  
**Report Version**: 1.0.0 (Official Release)  
**Status**: COMPLETE & VERIFIED  

---

## 1. Executive Summary & KPIs
The bank evaluated a batch of **10,000 transactions** through our explainable first-level screening pipeline.
A total of **118 transactions (1.18%)** triggered two or more risk heuristics and were escalated to the manual investigation queue.

| Executive Metric | Value | Context |
|---|:---:|---|
| **Total Ingested Volume** | 10,000 | Processed and cleaned transaction records |
| **Total Monetary Volume** | $45,498,111.43 | Net portfolio turnover across monitored channels |
| **Average Transaction** | $4,549.81 | Population mean |
| **99th Percentile Threshold ($P_{99}$)** | $45,001.18 | Outlier cutoff for high-value transfers |
| **Statistical Threshold ($\mu + 3\sigma$)** | $43,732.38 | Baseline Gaussian 3-sigma cutoff |
| **Suspicious Flagged Volume** | **118 (1.18%)** | Prioritized for immediate analyst review (Score $\ge 2$) |
| **High Amount Alerts** | 100 | Single transactions exceeding outlier thresholds |
| **Late Night Alerts** | 750 | Transactions occurring between 23:00 and 05:59 |
| **High Frequency Bursts** | 113 | Accounts executing $\ge 5$ transactions in rolling 1-hour |

---

## 2. Answers to Core Business Questions (Section 34)

### Q1: What percentage of transactions are flagged as suspicious?
**Finding**: 1.18% (118 out of 10,000 transactions).

### Q2: Which rule generates the most alerts?
**Finding**: Late Night (Rule_Late_Night) with 750 alerts (7.5% of all transactions).

### Q3: How many transactions trigger two or more rules?
**Finding**: 118 transactions (1.18% of total), which represents all flagged high-priority alerts.

### Q4: Which transaction types have higher suspicious rates?
**Finding**: 'Transfer' exhibits the highest suspicious rate at 3.17% of its transaction volume.

### Q5: Which channels show higher suspicious activity?
**Finding**: 'Online' shows the highest suspicious rate at 2.56% of channel traffic.

### Q6: Which hours contain more suspicious transactions?
**Finding**: Hour 23:00 contains the peak number of suspicious transactions (34 flagged records), consistent with the late-night risk window.

### Q7: Are suspicious transactions generally larger than normal transactions?
**Finding**: Yes. Suspicious transactions average $53,416.15 versus $3,966.30 for normal transactions (a 13.47x increase).

### Q8: Which accounts have repeated suspicious activity?
**Finding**: 28 accounts have multiple suspicious transactions. The top flagged account is ACC1183 with 10 suspicious transactions.

### Q9: Which rule combinations occur most frequently?
**Finding**: Overall single anomaly: '0_1_0' (Late Night Only) with 635 transactions. Among escalated multi-rule alerts (Score >= 2), '0_1_1' (Late Night + High Frequency) is most frequent with 63 transactions.

### Q10: If verified fraud labels are available, how well do the simple rules identify known fraud cases?
**Finding**: The screening rules achieve a Recall of 29.5%, Precision of 100.0%, and F1-Score of 0.456, capturing known fraud while maintaining a low False Positive Rate of 0.00%.

---

## 3. Recommended Rule Definition Table (Section 36)

| Rule Name | Condition | Score Weight | Business & Operational Rationale |
|---|---|:---:|---|
| **Unusual Amount** | `Amount >= P99` (or `Amount > Mean + 3*Std`) | **+1** | Transaction value is unusually high compared to historical baseline. |
| **Late Night** | `23:00 <= Hour <= 05:59` | **+1** | Activity occurs during the customer's typical sleep hours; common in automated card draining. |
| **High Frequency** | `Rolling 1-Hour Txn Count >= 5` | **+1** | Rapid transaction bursts indicate credential stuffing, automated bots, or panic card testing. |
| **Alert Cutoff** | `Suspicion_Score >= 2` | **ALERT** | Combines multi-factor signals to suppress single-anomaly noise and prioritize true risk. |

---

## 4. Pattern & Rule Combination Distribution (Section 31 & 32)

### Individual Rule Alert Volume
| Pattern        | Rule_Name           |   Alerts |   Alert_Pct |
|:---------------|:--------------------|---------:|------------:|
| High Amount    | Rule_High_Amount    |      100 |        1    |
| Late Night     | Rule_Late_Night     |      750 |        7.5  |
| High Frequency | Rule_High_Frequency |      113 |        1.13 |

### Rule Bitmask Combination Analysis
|   Rule_Combination |   Transactions |   Percentage | Description                            |
|-------------------:|---------------:|-------------:|:---------------------------------------|
|              0_0_0 |           9162 |        91.62 | Baseline / Normal (No Rules Triggered) |
|              0_1_0 |            635 |         6.35 | Late Night Only                        |
|              0_1_1 |             63 |         0.63 | Late Night + High Frequency            |
|              1_0_0 |             45 |         0.45 | High Amount Only                       |
|              1_1_0 |             45 |         0.45 | High Amount + Late Night               |
|              0_0_1 |             40 |         0.4  | High Frequency Only                    |
|              1_1_1 |              7 |         0.07 | Critical Alert (All 3 Rules Triggered) |
|              1_0_1 |              3 |         0.03 | High Amount + High Frequency           |

---

## 5. Multi-Dimensional Risk Drilldowns

### Breakdown by Transaction Type
| Transaction_Type   |   Transactions |   Suspicious |   Suspicious_Rate |
|:-------------------|---------------:|-------------:|------------------:|
| Transfer           |           3725 |          118 |              3.17 |
| Deposit            |            958 |            0 |              0    |
| Payment            |           3890 |            0 |              0    |
| Withdrawal         |           1427 |            0 |              0    |

### Breakdown by Channel
| Channel    |   Transactions |   Suspicious |   Suspicious_Rate |
|:-----------|---------------:|-------------:|------------------:|
| Online     |           4606 |          118 |              2.56 |
| Atm        |            962 |            0 |              0    |
| Branch     |            501 |            0 |              0    |
| Mobile App |           3931 |            0 |              0    |

### Top High-Risk Customer Accounts (Top 10)
| Account_ID   |   Transactions |   Total_Value |   Avg_Amount |   Suspicious_Transactions |   Suspicious_Rate |
|:-------------|---------------:|--------------:|-------------:|--------------------------:|------------------:|
| ACC1183      |             43 |        570373 |      13264.5 |                        10 |             23.26 |
| ACC1290      |             37 |        797991 |      21567.3 |                         8 |             21.62 |
| ACC1340      |             35 |        699260 |      19978.8 |                         6 |             17.14 |
| ACC1492      |             26 |        527756 |      20298.3 |                         5 |             19.23 |
| ACC1161      |             26 |        636560 |      24483.1 |                         4 |             15.38 |
| ACC1420      |             23 |        438158 |      19050.4 |                         4 |             17.39 |
| ACC1186      |             27 |        385701 |      14285.2 |                         4 |             14.81 |
| ACC1030      |             31 |        368071 |      11873.2 |                         4 |             12.9  |
| ACC1344      |             26 |        323864 |      12456.3 |                         4 |             15.38 |
| ACC1430      |             20 |        249716 |      12485.8 |                         4 |             20    |

---

## 6. Ground-Truth Historical Evaluation (Section 33)

| Metric | Score | Industry Interpretation |
|---|:---:|---|
| **True Positives (TP)** | 118 | Confirmed fraud successfully caught by screening rules |
| **False Positives (FP)** | 0 | Legitimate customer actions flagged for review |
| **True Negatives (TN)** | 9600 | Legitimate transactions cleared without disruption |
| **False Negatives (FN)** | 282 | Undetected fraud slipping through first-tier rules |
| **Recall (Sensitivity)** | **29.50%** | Percentage of all actual frauds detected |
| **Precision** | **100.00%** | Percentage of flagged alerts that represent true fraud |
| **F1-Score** | **0.456** | Harmonic mean of precision and recall |
| **False Positive Rate (FPR)** | **0.00%** | Proportion of good customers inconvenienced (< 1% target) |

---

## 7. Operational & Ethical Limitations (Section 38)
1. **Investigation Signals vs. Proof of Guilt**: A flagged alert is an investigative signal for human-in-the-loop validation, **never legal or criminal proof of fraud**.
2. **False Positives**: Honest customers traveling abroad, paying for medical emergencies at 2:00 AM, or buying high-value electronics will trigger rules. Banks must use secondary verification (SMS OTP / phone callback) rather than punitive account blocking.
3. **Threshold Calibration**: Population-level thresholds ($\mu + 3\sigma$) should evolve toward personalized per-account baseline profiles to avoid penalizing high-net-worth commercial accounts.

---

## 8. Embedded Figures Reference
* Figure 1: Amount Distribution (`figures/01_amount_distribution.png`)
* Figure 2: Normal vs Suspicious Volume (`figures/02_normal_vs_suspicious.png`)
* Figure 3: Suspicious by Hour (`figures/03_suspicious_by_hour.png`)
* Figure 4: Suspicious Rate by Type (`figures/04_suspicious_rate_by_type.png`)
* Figure 5: Amount vs Suspicion Score (`figures/05_amount_vs_suspicion_score.png`)
* Figure 6: Rule Combinations (`figures/06_rule_combination_frequencies.png`)
* Figure 7: Channel Vulnerability (`figures/07_suspicious_rate_by_channel.png`)
