# VELOOP Rewards: Comprehensive Analytics Gap Assessment

**Document ID:** `02_product_audit/analytics_gap_assessment.md`  
**Version:** 1.0.0 (Pre-Launch Baseline)  
**Governance Classification:** Internal Technical Audit  
**Author:** Lead Analytics Engineer & Data Governance Architect  
**Scope:** Exhaustive evaluation of telemetry coverage, data models, dictionary specifications, KPI feasibility, data quality, dashboard readiness, engineering instrumentation, access control, technical documentation, and executive reporting.

---

## 1. Executive Summary & Assessment Methodology

This assessment consolidates and expands upon the telemetry and structural findings documented across `02_product_audit/analytics_gaps.md`, `07_data_quality/profiling_findings.md`, `07_data_quality/kpi_feasibility.xlsx`, and `09_engineering/developer_analytics_handoff.xlsx`. 

Every identified gap has been evaluated against pre-launch commercial readiness and assigned a priority rating:
- **Critical:** Complete blocker to core business measurement, financial reconciliation, statutory compliance, or platform launch. Immediate engineering action required.
- **High:** Substantial limitation causing analytical blindness, fraud exposure, or unmonitored user drop-off in high-value funnels. Must be resolved prior to public release.
- **Medium:** Operational friction, data hygiene anomaly, or reporting latency that can be mitigated with transformations or post-launch patches.
- **Low:** Cosmetic layout, secondary metadata enhancement, or minor documentation gap with negligible commercial risk.

---

## 2. Gap Assessment by Domain

### Section 1: Event Coverage

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-EVT-01** | **Absence of Atomic Wallet Ledger Mutation Events** (`wallet_transaction_created`, `wallet_transaction_completed`, `wallet_transaction_reversed`) | Total inability to track the lifecycle of virtual XP credits and debits, verify balance state consistency, or detect runaway point inflation. | **Critical** | Financial integrity blocker: virtual currency liabilities cannot be audited or reconciled against user activities without an immutable transaction stream. |
| **GAP-EVT-02** | **Missing Cash-Out and Fiat Disbursement Event Stream** (`withdrawal_requested`, `withdrawal_processing`, `withdrawal_completed`, `withdrawal_rejected`, `withdrawal_reversed`) | Complete blindness regarding cash redemption demand, payment rail processing latency, bank settlement failure rates, and liquidity burn. | **Critical** | Treasury and legal blocker: cannot monitor cash outflows, track gateway SLA compliance, or audit disbursement failures. |
| **GAP-EVT-03** | **Missing Outbound Referral Invitation and Share Telemetry** (`referral_invited`, `referral_link_clicked`, `referral_converted`) | Cannot measure viral K-factor, identify top acquisition share channels (WhatsApp vs Telegram), or detect drop-off between invite creation and app install. | **Critical** | Growth strategy blocker: marketing spend efficiency and referral unit economics cannot be evaluated with only inbound signups. |
| **GAP-EVT-04** | **Missing Real-Time Security and Reversal Events** (`reward_reversed`, `account_suspended`, `chargeback_logged`) | Inability to track fraud loss avoidance, sybil emulator detection, or clawback rates when partner networks reject fraudulent leads. | **High** | Risk control blocker: allows bot farms and abusive users to extract value without real-time audit event logging. |

---

### Section 2: Data Model

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-MOD-01** | **Absence of Relational Double-Entry Ledger Entity** (`Wallet_Transactions`) | Source data relies solely on a static `xp_balance` snapshot on the User entity; historical user balance reconstruction and temporal auditing are impossible. | **Critical** | Core relational architecture flaw: violates double-entry accounting standards and prevents point breakage modeling. |
| **GAP-MOD-02** | **Absence of Fiat Disbursement Relational Entity** (`Withdrawals`) | No database tables exist to track user cash redemption requests, beneficiary payout instruments, gateway transaction IDs, or settlement timestamps. | **Critical** | Relational omission: prevents transactional joins between user activity, point debits, and fiat cash disbursements. |
| **GAP-MOD-03** | **Absence of Task Master Dimension Catalog** (`Task_Master`) | 80 distinct `task_id` values (`TASK0001`–`TASK0080`) exist in `Task_Activity` without a parent dimension table documenting task name, advertiser, or payout rate. | **High** | Dimensional modeling gap: prevents segmenting task completion and failure rates by difficulty tier, partner advertiser, or target duration. |
| **GAP-MOD-04** | **Absence of Item-Level Reward Inventory Entity** (`Rewards_Catalog`) | Datasets track only aggregate counts of reward events; item-level SKU redemptions, brand catalog popularity, and merchant margins cannot be analyzed. | **High** | Catalog management gap: product team cannot determine whether users prefer Amazon, Flipkart, or Google Play vouchers. |
| **GAP-MOD-05** | **Absence of Outbound Referral Invites Entity** (`Referral_Invites`) | Missing entity linking inviter invite actions to referee accounts; prevents constructing a multi-touch referral attribution graph. | **High** | Graph modeling gap: limits referral analysis to a flat 1:1 user profile join rather than a dynamic viral tree. |

---

### Section 3: Data Dictionary

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-DIC-01** | **Ambiguous Timestamp Nomenclature Across Entities** (`timestamp` vs `event_datetime` vs `task_completed_at`) | Inconsistent datetime field naming across clickstream, task execution, and operational tables creates friction and syntax errors in automated joins. | **Medium** | Developer friction: causes pipeline mapping errors between client SDK payloads and warehouse ingestion schemas. |
| **GAP-DIC-02** | **Unclear Sequence Number Semantics** (`sequence_number`) | Data dictionary did not specify whether `sequence_number` in `Feature_Events` is scoped to parent session or global user stream, leading to duplicate values. | **Medium** | Data integrity ambiguity: downstream path reconstruction models require explicit scoping documentation. |
| **GAP-DIC-03** | **Lack of Documented Currency Pegging and Breakage Rules** (`reward_unit`, `cost_xp`) | Data dictionary lacks formal economic definitions pegging virtual XP points to fiat INR and defining expiration rules for dormant balances. | **High** | Financial documentation gap: legal and accounting teams require explicit documentation of platform virtual currency liabilities. |

---

### Section 4: KPI Definitions

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-KPI-01** | **Blocked Financial & Ledger KPIs** (`KPI-WAL-02`: Point Velocity (Accrual vs Burn Ratio), Reward Credit Volume, Reward Reversal Rate) | Executive leadership cannot measure gross point liability inflow, point inflation, or monetary clawback rates without double-entry ledger data. | **Critical** | Executive reporting blocker: core financial metrics in the KPI catalogue are blocked due to missing ledger tables. |
| **GAP-KPI-02** | **Blocked Payout & Liquidity KPIs** (`KPI-WDL-01`: Withdrawal Completion Rate, `KPI-WDL-02`: Gross Withdrawal Value (GWV in INR), `KPI-WDL-03`: Average Payout Processing SLA (Hours), `KPI-WDL-04`: Withdrawal Rejection Rate, `KPI-WDL-05`: Pending Escrow Payout Liability (INR)) | Operations team cannot track cash-out success rates, payout processing velocity, or payment gateway SLA compliance without withdrawal tables. | **Critical** | Operational blocker: platform cash burn and liquidity health metrics cannot be computed. |
| **GAP-KPI-03** | **Blocked Referral Qualification & Support Dispute KPIs** (`KPI-REF-04`: Referral Qualification Drop-off Rate, `KPI-SUP-02`: Support Ticket Resolution SLA (Hours), `KPI-SUP-03`: Dispute Rate per 1,000 Completed Tasks) | Growth and ops teams cannot measure referee qualification drop-offs, user task dispute rates, or ticket resolution SLAs due to missing referral lifecycle and support dispute tables. | **Critical** | Growth and operational risk blocker: prevents evaluating viral loop economics and customer dispute volumes. |
| **GAP-KPI-04** | **Ambiguous DAU Qualification Criteria** (App Foregrounding vs Value-Generating Action) | Calculating DAU strictly from raw session pings risks counting passive background wakeups and instant bounce exits (<3s). | **Medium** | Metric inflation risk: overstates active user base; requires qualification hurdle (at least 1 user interaction event). |

---

### Section 5: Data Quality

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-DQ-01** | **Duplicate Event ID Injections in Telemetry Stream** (`event_id` collisions) | Quality audit detected 10 duplicate `event_id` records in `10_Event_Data_Quality_Audit`, violating primary key uniqueness. | **High** | Telemetry ingestion risk: without stream deduplication (Redis cache / BigQuery unique keys), event counts and aggregations are inflated. |
| **GAP-DQ-02** | **Duplicate User Accounts in Master Audit Sheet** (`user_id` collisions) | Quality audit detected 8 duplicate `user_id` records in `Users_Messy_Audit`, breaking 1:1 primary key relationships. | **Critical** | Master data risk: corrupts user-level joins, distorts lifetime value metrics, and causes duplicate user profile records. |
| **GAP-DQ-03** | **Categorical Casing and Trailing Whitespace Anomalies** (`feature_name`, `event_status`, `device`) | Inconsistent casing (`Watch Ads` vs `watch ads`) and trailing whitespace fragment GROUP BY aggregations unless cleansed in transformation layer. | **Medium** | Reporting hygiene issue: causes split categories in BI charts; successfully mitigated via automated SQL `TRIM()` and `INITCAP()`. |
| **GAP-DQ-04** | **Negative `days_since_registration` Values** (-0.8 days) | Calculation logic produced negative tenure values for 8 users where synthetic snapshot generation timestamp preceded registration timestamp. | **Medium** | Derived metric defect: skews Day-0 cohort bins; requires clamping derived tenure metrics to `GREATEST(0, tenure)`. |
| **GAP-DQ-05** | **Unzoned Timestamps Without Explicit ISO-8601 Offset** | All timestamps in source tables lack explicit UTC (`Z`) or offset (`+05:30`) metadata, creating risk of diurnal curve shift across timezones. | **High** | Time-series integrity risk: daily streak calculations and cohort cutoffs shift by 5.5 hours if interpreted as local IST rather than UTC. |

---

### Section 6: Dashboard Readiness

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-DSH-01** | **Blocked Visuals on Executive, Wallet, and Withdrawal Dashboards** | Visuals requiring double-entry ledger transactions and cash-out disbursements cannot render live data and must display "DATA MISSING" alerts. | **Critical** | Dashboard delivery blocker: C-suite cannot inspect live cash flow or balance sheets until underlying tables are deployed. |
| **GAP-DSH-02** | **Lack of In-Memory BI Caching Layer** (BigQuery BI Engine / Looker Studio Cache) | Complex dimensional joins executed directly against raw BigQuery tables suffer query latencies > 4.0s and consume free tier query quota rapidly. | **Medium** | User experience friction: dashboard viewers experience sluggish filter updates; requires pre-aggregated marts and BI Engine caching. |
| **GAP-DSH-03** | **Incomplete Filter Hierarchy on User Analytics Dashboard** | Cross-filtering between `platform` and `primary_device` lacks cascading synchronization, allowing users to select invalid combinations (e.g. `iOS Native` + `Windows`). | **Low** | Minor UI usability defect: generates empty chart views when conflicting filters are applied simultaneously. |

---

### Section 7: Engineering Instrumentation

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-ENG-01** | **Absence of Server-to-Server Ad Mediation Postbacks** (AppsFlyer / AdMob / ironSource) | Relying exclusively on client-side video creative completion events exposes ad reward payouts to automated script spoofing and click fraud. | **High** | Fraud exposure: users can trigger `ad_completed` client events without actually rendering video impressions. |
| **GAP-ENG-02** | **Lack of Offline Event Spooling in Client Mobile SDK** | Network drops during task completion or ad viewing cause permanent telemetry loss if client lacks local encrypted SQLite buffer. | **High** | Data loss risk: undercounts user engagement and task completions in low-connectivity mobile environments. |
| **GAP-ENG-03** | **Missing Semantic App Build Version in Telemetry Payloads** | Telemetry logs capture broad platform (`Android Native`) but lack granular app release version (`v1.0.4+42`), preventing release regression tracking. | **Medium** | Engineering observability gap: cannot isolate telemetry crashes or UI drop-offs to specific client software releases. |

---

### Section 8: Access Control

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-ACC-01** | **Absence of Automated Least-Privilege Role Separation in Raw Storage** | Pre-launch engineering environment currently relies on shared administrative credentials rather than scoped IAM role policies. | **High** | Security risk: violates principle of least privilege; broad access increases risk of accidental dataset mutation or deletion. |
| **GAP-ACC-02** | **Unmasked PII Risk in Customer Support and Dispute Notes** | Free-text customer feedback notes lack automated regex redaction, risking unmasked phone numbers and bank account numbers in analytical tables. | **Critical** | Statutory privacy violation: exposing unmasked customer PII in analytics violates DPDP and privacy compliance frameworks. |
| **GAP-ACC-03** | **Missing Cryptographic Salt Rotation Policy for `payout_account_hash`** | SHA-256 hashing of UPI VPAs and bank accounts lacks a documented 90-day salt rotation and key versioning protocol. | **Medium** | Cryptographic hardening gap: static salts increase vulnerability to rainbow table reversal attacks over long time horizons. |

---

### Section 9: Documentation

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-DOC-01** | **Lack of Formal Event Deprecation and Schema Migration Guidelines** | No established RFC or change-management workflow for deprecating legacy event names or adding required payload properties. | **Medium** | Technical governance gap: unannounced schema modifications risk breaking downstream dbt transformation models. |
| **GAP-DOC-02** | **Missing Disaster Recovery Runbooks for Stream Ingestion Outages** | Engineering team lacks documented runbooks for isolating corrupted schemas and replaying quarantined Dead-Letter Queue (DLQ) records into BigQuery. | **High** | Operational resilience risk: extends MTTR (Mean Time to Recovery) during production ingestion outages. |

---

### Section 10: Reporting

| Gap ID | Identified Gap | Impact on Business & Analytics | Priority | Priority Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **GAP-REP-01** | **Absence of Automated Daily Standup KPI Dispatchers** (Slack / Telegram Webhooks) | Executive and product teams must manually log into BI dashboards; lacks automated daily morning summaries for DAU and revenue pacing. | **Medium** | Operational efficiency gap: delays executive awareness of diurnal performance trends and abnormal drops. |
| **GAP-REP-02** | **Missing Automated Double-Entry Balance Discrepancy Alerting** | Zero automated alerting triggers if total virtual points credited do not balance against debits, allowing accounting discrepancies to go unnoticed. | **Critical** | Financial audit risk: undetected balance drift creates unbacked currency liability and financial accounting misstatements. |

---

## 3. Gap Assessment Summary Table

The table below summarizes the distribution of the **33 total identified gaps** across all 10 operational domains and priority classifications:

| Operational Domain | Critical | High | Medium | Low | Total Gaps | Dominant Failure Mode / Impact |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Event Coverage** | 3 | 1 | 0 | 0 | **4** | Missing transactional event streams (Wallet, Withdrawals, Referrals) |
| **2. Data Model** | 2 | 3 | 0 | 0 | **5** | Relational omissions (Ledger, Disbursements, Task Catalog) |
| **3. Data Dictionary** | 0 | 1 | 2 | 0 | **3** | Datetime naming ambiguity, unzoned timestamps, currency peg rules |
| **4. KPI Definitions** | 2 | 1 | 1 | 0 | **4** | Financial, payout, and viral K-factor metrics completely blocked |
| **5. Data Quality** | 1 | 2 | 2 | 0 | **5** | Primary key collisions, casing anomalies, negative tenure metrics |
| **6. Dashboard Readiness** | 1 | 0 | 1 | 1 | **3** | Blocked financial visuals, lack of in-memory caching |
| **7. Engineering Instrumentation** | 0 | 2 | 1 | 0 | **3** | Lack of S2S ad postbacks, offline event spooling, release tagging |
| **8. Access Control** | 1 | 1 | 1 | 0 | **3** | Unmasked PII in free-text, shared credentials, static salt rotation |
| **9. Documentation** | 0 | 1 | 1 | 0 | **2** | Missing schema migration RFCs, lack of DLQ replay runbooks |
| **10. Reporting** | 1 | 0 | 1 | 0 | **2** | Missing automated balance drift alerts and daily standup webhooks |
| **TOTALS** | **11** | **12** | **9** | **1** | **33** | **70% of gaps concentrated in Critical & High priority categories** |

---

## 4. Remediation Roadmap & Backlog Mapping

All 33 gaps have been prioritized into three execution phases within the engineering implementation backlog:
- **Phase 1: Pre-Launch Blockers (11 Critical Gaps):** Deploy `Wallet_Transactions` double-entry ledger, `Withdrawals` table, referral attribution events, PII redaction filters, and automated balance drift circuit-breakers.
- **Phase 2: Commercial Launch Hardening (12 High Gaps):** Deploy `Task_Master` and `Rewards_Catalog` dimensions, server-to-server ad mediation postbacks, client offline SQLite queue, stream deduplication, and DLQ replay runbooks.
- **Phase 3: Post-Launch Optimization (10 Medium & Low Gaps):** Standardize datetime nomenclature, implement BigQuery BI Engine reservation, automate daily Slack KPI digest, and deploy cascading dashboard filters.

---

## 5. Data Authenticity Statement

> [!IMPORTANT]
> **Data Authenticity Statement**  
> All findings, gap classifications, and structural analyses documented in this report originate from the examination of simulated test datasets (`00_source_data/veloop_simulated_user_behavior_1000.xlsx` and `00_source_data/veloop_rewards_data_01.xlsx`).  
> 
> These datasets were created exclusively for analytical modeling, pipeline stress-testing, and schema verification. No real production data or live user PII was evaluated. All identified gaps represent engineering and architectural requirements necessary to elevate the simulated baseline to production commercial readiness.
