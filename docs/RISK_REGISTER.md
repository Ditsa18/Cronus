# Project Risk Register

| Risk ID | Category | Risk Description | Likelihood | Impact | Severity | Mitigation Strategy | Status |
|---|---|---|:---:|:---:|:---:|---|:---:|
| **RSK-001** | Privacy / Legal | Accidental inclusion of real customer banking information (PII) | Low | High | Medium | Strict synthetic generation using randomized identifiers (`TX100001`, `ACC1001`) with zero real credentials. | MITIGATED |
| **RSK-002** | Algorithmic | Masking of high amount outliers due to heavy-tailed inflation of $\mu + 3\sigma$ | High | Medium | High | Dual implementation: offer both $\mu + 3\sigma$ and $99\text{th}$ percentile ($P_{99}$), defaulting to $P_{99}$ for robustness. | MITIGATED |
| **RSK-003** | Technical | Rolling window timestamp monotonicity issues in Pandas across account groups | Medium | High | High | Pre-sort strictly by `[Account_ID, Transaction_Datetime]` and provide hourly-grouping fallback helper. | MITIGATED |
| **RSK-004** | Operational | High false positive alert volume overwhelming manual review teams | High | Medium | High | Use composite scoring threshold ($\ge 2$) rather than single-rule triggers ($\ge 1$), prioritizing multi-factor risks. | MITIGATED |
| **RSK-005** | UI / Display | Matplotlib GUI backend errors when running headless on Windows/PowerShell | Medium | Low | Low | Force non-interactive `matplotlib.use('Agg')` prior to plotting. | MITIGATED |
| **RSK-006** | Testing | Test suite flakiness due to unseeded random numbers | Medium | Medium | Medium | Seed all random number generators (`numpy.random.seed(42)`, Python `random.seed(42)`). | MITIGATED |
