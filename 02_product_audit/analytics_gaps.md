# VELOOP Rewards — Analytics Gaps & Structural Audit

> **CRITICAL NOTICE**: All findings, schemas, and metrics documented in this audit reflect **SIMULATED DATA** created for analytical testing and product architecture modeling. No real production telemetry or user PII was evaluated.

---

## 1. Executive Summary: Core Telemetry Gaps

A comprehensive referential integrity audit performed via `scripts/02_test_relationships.py` established that while downstream behavioral tables (`02_Sessions`, `03_Feature_Events`, `04_Daily_Activity`, `05_Task_Activity`, `06_Milestones`) demonstrate **0% orphan user IDs** against `01_Users_1000`, the supplied dataset suffers from critical architectural omissions. Key business domains — specifically **Wallet Ledgers**, **Withdrawal Disbursements**, **Referral Attribution Graphs**, and **Reward Catalogs** — exist only as high-level summary flags or counts, with no underlying transactional tables.

---

## 2. Missing Relational Tables Audit

| Missing Table | Domain / Scope | Current Proxy in Dataset | Impact | Priority | Architectural Requirement & Proposed Schema |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`Wallet_Ledger` / `Wallet_Transactions`** | Currency, XP credits/debits, balance snapshots | Binary flag `wallet_activity` in `04_Daily_Activity`, static `xp_balance` in `Users_1000_Clean` | **Critical** | **Critical** | Cannot reconstruct running balance over time, reconcile XP issuance vs breakage, audit double-crediting, or detect point economy inflation. Requires a dedicated append-only ledger (`transaction_id`, `user_id`, `transaction_datetime`, `transaction_type`, `amount`, `balance_after`, `reference_event_id`). |
| **`Withdrawals` / `Disbursements`** | Cash payouts, UPI transfers, gift voucher redemptions | None. No withdrawal tables, status flows, or failure logs exist. | **Critical** | **Critical** | Inability to track liquidity demand, payout cycle times, payment gateway failure rates, fraud rings, or unit economic margins. Requires an immutable withdrawal requests table (`withdrawal_id`, `user_id`, `requested_datetime`, `amount_inr`, `xp_deducted`, `payout_method`, `payout_status`, `gateway_reference`, `completed_at`). |
| **`Referrals` / `Referral_Conversions`** | Multi-touch invite tracking, viral loop attribution, referee conversion | Static `referral_code` on Users, high-level `referral_source_detail` string | **Critical** | **Critical** | Cannot calculate K-factor (viral coefficient), evaluate invite-to-install drop-offs, track invite link shares, or prevent self-referral fraud. Requires a dual tracking model: `referral_invites` (`invite_id`, `referrer_user_id`, `channel`, `sent_at`) and `referral_conversions` (`conversion_id`, `referrer_user_id`, `referee_user_id`, `converted_at`, `reward_status`). |
| **`Rewards_Catalog` / `Redemptions`** | Reward item inventory, point redemption orders, partner merchant vouchers | Count `reward_activity_count` in `04_Daily_Activity`, flag `reward_related_flag` in Events | **Critical** | **Critical** | Cannot measure reward popularity, brand catalog affinity, inventory stockouts, or user price elasticity. Requires a dimension table `rewards_catalog` (`reward_id`, `reward_name`, `cost_xp`, `category`, `stock`) and a fact table `reward_redemptions` (`redemption_id`, `user_id`, `reward_id`, `redeemed_at`, `delivery_status`). |
| **`Task_Master` / `Task_Catalog`** | Micro-task definitions, partner advertisers, survey durations, expected payout | String `task_id` (`TASK0001`–`TASK0080`) in `05_Task_Activity` with no parent table | **High** | **High** | 80 distinct task IDs exist without metadata regarding task length, advertiser payout rate, or difficulty tier, preventing task ROI analysis. Requires `task_master` (`task_id`, `task_name`, `task_category`, `reward_xp`, `estimated_seconds`, `is_active`). |

---

## 3. Downstream Analytical Implications

1. **Unit Economics & Margin Blindness**: Without withdrawal disbursements and partner reward costs, gross margin per active user and platform take-rate cannot be computed.
2. **Growth Loop Attribution Breakdown**: While acquisition source indicates referrals for 119 users (WB2) and 154 users (WB1), the specific inviter-invitee graph cannot be formed without a referral mapping table.
3. **Financial Reconciliation Risk**: Pre-launch testing cannot validate double-entry bookkeeping without an immutable ledger table.

---
---

## 4. KPI Feasibility Summary & Measurement Blockers

A feasibility audit was conducted via `scripts/03_kpi_feasibility.py` across the 10 core proposed executive and product KPIs. Metrics were evaluated strictly against supplied data structures:

| KPI Name | Available? | Feasibility Status | Simulated Result / Benchmark | Measurement Gap / Blockers |
| :--- | :---: | :---: | :--- | :--- |
| **1. Daily Active Users (DAU)** | **YES** | **Confirmed calculable** | **Mean: 40.65 users/day** (Min: 1, Max: 164 across 164 days; 6,667 user-days) | Fully calculable from `04_Daily_Activity`. Real-time streaming deduplication required for production. |
| **2. Task Completion Rate** | **YES** | **Confirmed calculable** | **57.15%** (5,627 completed / 9,846 total attempts) | Fully calculable from `05_Task_Activity`. Task master metadata table recommended for tier segmentation. |
| **3. Task Failure Rate** | **YES** | **Confirmed calculable** | **15.44%** explicit Failed (1,520 tasks); total non-completion rate is **36.27%** | Fully calculable from `05_Task_Activity`. Requires client error telemetry for root-cause diagnosis. |
| **4. Reward Credit Volume** | **PARTIAL** | **Proposed** | **5,627 task rewards + 4,799 milestone rewards (242,830 pts)**. Currency: **N/A — blocked** | Event counts confirmed; monetary valuation and currency transaction ledger are missing. |
| **5. Reward Reversal Rate** | **NO** | **Blocked** | **N/A — blocked** | Completely blocked. No reversal, clawback, or penalty telemetry exists in the dataset. |
| **6. Average Session Duration** | **YES** | **Confirmed calculable** | **51.81 seconds** (Median: 42.00s across 7,913 sessions; range 5s–180s) | Fully calculable from `02_Sessions`. Background heartbeat logging recommended for production. |
| **7. 7-day Streak Retention** | **YES** | **Confirmed calculable** | **42.10%** (421 users reached `seventh_active_day` milestone / 1,000 total users) | Fully calculable from `06_Milestones` and `04_Daily_Activity`. |
| **8. Feature Adoption Rate** | **YES** | **Confirmed calculable** | **98.40%** overall adoption (984 active feature users / 1,000 users) | Fully calculable from `03_Feature_Events`. Feature penetration ranges from 67.4% to 83.6%. |
| **9. Withdrawal Completion Rate** | **NO** | **Blocked** | **N/A — blocked** | Completely blocked. No withdrawal or payout transaction tables exist in either workbook. |
| **10. Referral Conversion Rate** | **PARTIAL** | **Proposed** | **11.90% to 15.40% referee acquisition share**. Outbound funnel: **N/A — blocked** | Inbound referee share confirmed; outbound referral invitation funnel conversion is blocked. |

### Architectural Recommendations for Blocked KPIs:
1. **Financial & Reward Reconciliation**: Implement a unified `wallet_transactions` double-entry ledger to enable Reward Credit Volume valuation, breakage analysis, and Reward Reversal Rate tracking.
2. **Disbursement Monitoring**: Deploy a dedicated `withdrawals` table integrated with payout gateway webhooks to track Withdrawal Completion Rate and payout latency.
3. **Growth Loop Instrumentation**: Implement a `referral_invites` table capturing outbound share events, channels, and deep-link clickthroughs to unlock end-to-end Referral Funnel Conversion tracking.
---

## 5. Master Analytics Gaps Register

The following systematic register logs the 12 core telemetry, architectural, and dimensional gaps identified across the VELOOP product analytics foundation:

| Gap ID | Product Area | Identified Telemetry / Data Gap | Impact on Reporting & Analytics | Priority | Underlying Technical Reason |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **GAP-001** | **Wallet** | Lack of an immutable double-entry wallet transactions ledger | Inability to reconstruct running balances over time, audit point breakage, reconcile liability, or model point economy inflation. | **Critical** | Supplied dataset only provides a static `xp_balance` snapshot on Users and a binary flag in Daily Activity; no transactional ledger exists. |
| **GAP-002** | **Withdrawals** | Complete absence of withdrawal requests and payout disbursement tables | Total blindness to platform cash burn, payout processing latency, payment gateway failure rates, and liquidity forecasting. | **Critical** | Standalone withdrawal tables were omitted entirely from the source data export. |
| **GAP-003** | **Referrals** | Missing outbound referral invitations, share channels, and link click tracking | Cannot calculate viral K-factor (invitations sent vs conversions), evaluate share-to-install drop-offs, or identify high-performing share channels. | **Critical** | Telemetry only records referee signups upon arrival; the outbound viral distribution funnel is not instrumented. |
| **GAP-004** | **Rewards Catalog** | Absence of a master reward catalog and redemption order fact table | Inability to evaluate reward SKU popularity, brand affinity (Amazon vs Flipkart), catalog stockouts, or merchant unit economic margins. | **Critical** | Datasets track only aggregate counts of reward events; item-level SKU redemptions are not captured. |
| **GAP-005** | **Tasks** | Missing Task Master dimension table for the 80 distinct `task_id`s in `Task_Activity` | Cannot benchmark task completion rates by difficulty tier, partner advertiser payout rate, or expected duration. | **High** | `05_Task_Activity` contains `task_id` strings (`TASK0001`–`TASK0080`) without a parent dimension catalog table. |
| **GAP-006** | **Telemetry Identity** | Absence of `task_id` attribute in `03_Feature_Events` clickstream table | Cannot join micro-level user clickstream events to specific task attempts to analyze user behavioral friction before task abandonment. | **High** | `Feature_Events` logs generic feature and event names but lacks task entity context in its event schema payload. |
| **GAP-007** | **Fraud & Risk** | Zero telemetry for reward clawbacks, multi-account device hashes, or dispute dispositions | Inability to detect emulator click-farms, calculate net earned vs clawed-back points, or audit anti-bot security filters. | **Critical** | No reversal status values, device hardware identifiers (IMEI/MAC), or fraud disposition codes exist in the data. |
| **GAP-008** | **Onboarding** | Onboarding tracked only as a coarse 3-state profile attribute without step-level funnel events | Product managers cannot identify specific tutorial friction screens causing new user activation drop-offs. | **High** | Only final state (`onboarding_status`) is stored on the user profile; micro-step progress events (`onboarding_step_completed`) are absent. |
| **GAP-009** | **Timezone Standards** | Absence of explicit ISO-8601 UTC designators and client clock synchronization metadata | Daily cohort boundaries, streak calculations, and retention curves may shift depending on whether timestamps are interpreted as UTC or IST. | **Medium** | Timestamps in source tables are unzoned datetime strings without explicit offset metadata (`Z` or `+05:30`). |
| **GAP-010** | **Help Center** | Zero tracking of customer support inquiries, FAQ article views, or ticket resolutions | Inability to identify user friction hot-spots, dispute frequency over failed payouts, or support resolution SLA efficiency. | **Medium** | No customer support ticketing or knowledge base interaction events exist in the telemetry taxonomy. |
| **GAP-011** | **Ad Mediation** | Missing third-party ad mediation postback webhooks and eCPM transaction logs | Cannot reconcile publisher revenue against awarded user points or verify ad viewability against click-fraud. | **High** | Ad views are captured solely via client-side events without third-party server-to-server validation. |
| **GAP-012** | **Observation Horizon** | Snapshot baseline calculation timestamp preceded registration for 8 users, with activity extending past Sept 15 | Produces negative derived metrics (`days_since_registration = -0.8`) and unpartitioned future activity data. | **Medium** | Snapshot date logic was hardcoded without boundary clamping against max registration timestamp in the synthetic generator. |
---

## 6. Required Telemetry Events Missing from Simulated Data

The cross-check between the production [event tracking plan](file:///home/rib/project/veloop-analytics/04_events/event_tracking_plan.xlsx) and the simulated telemetry tables (`02_Feature_Events`, `04_Task_Activity`) identified twenty-five (25) required canonical events that are completely absent from the simulated telemetry stream.

The table below catalogs these missing events, ranked by implementation priority, detailing the analytical blindness caused and the downstream KPIs blocked:

| Domain | Missing Event Name | Implementation Priority | Downstream KPIs Blocked / Blind Spots | Root Cause in Simulated Data | Required Engineering Action |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Wallet** | `wallet_transaction_created` | **Critical** | Ledger Inception Rate, Gross Point Pipeline | Wallet exists only as static balance; no journal event stream. | Instrument ledger journal writer upon credit/debit intent. |
| **Wallet** | `wallet_transaction_completed` | **Critical** | Net Available Balance, Circulating Point Economy | Cannot verify balance mutation settlement or double-credits. | Emit from wallet engine post-database commit. |
| **Wallet** | `wallet_transaction_reversed` | **Critical** | Ledger Discrepancy Rate, Financial Audit Reconciliation | Zero tracking of accounting reversals, clawbacks, or fixes. | Emit from audit engine upon posting offsetting journal entry. |
| **Withdrawals** | `withdrawal_requested` | **Critical** | Withdrawal Request Volume, Gross Withdrawal Value (GWV) | Entire cash-out domain missing from simulated workbooks. | Deploy client-side cash-out form submission telemetry. |
| **Withdrawals** | `withdrawal_completed` | **Critical** | Withdrawal Completion Rate, Net Settled Cash Outflow, SLA | Inability to track liquidity draw-down or payment settlement. | Connect payment aggregator webhook receiver to event bus. |
| **Rewards** | `reward_credited` | **Critical** | Reward Credit Volume, Gross XP Liability Inflow | Rewards logged only as static task attributes; no ledger stream. | Emit from reward engine upon successful validation. |
| **Rewards** | `reward_reversed` | **Critical** | Reward Reversal Rate, Chargeback Rate, Fraud Loss Avoidance | Completely blocked. No reversal or clawback telemetry. | Instrument risk engine clawback handler. |
| **Referrals** | `referral_converted` | **Critical** | Referral Conversion Rate, Viral K-factor, Referral CAC | Inbound referrals tracked, but conversion milestones omitted. | Deploy milestone listener when referee hits 100 XP hurdle. |
| **Withdrawals** | `withdrawal_processing` | **High** | Payout Pipeline Velocity, Fraud Review Queue Time | No intermediate escrow or gateway dispatch tracking. | Emit when risk checks clear and payload sent to gateway. |
| **Withdrawals** | `withdrawal_rejected` | **High** | Withdrawal Rejection Rate, Beneficiary Validation Failures | Cannot identify invalid UPI VPAs or banking rail rejections. | Capture gateway failure webhooks and risk quarantine rules. |
| **Withdrawals** | `withdrawal_reversed` | **High** | Withdrawal Reversal Rate, Banking Rail Failure Rate | Inability to detect post-settlement banking return codes. | Ingest bank clearing house retroactive debit notices. |
| **Rewards** | `reward_pending` | **High** | Pending Escrow Balance, High-Value Hold Duration | High-value surveys lack asynchronous escrow hold tracking. | Emit when task finished but awaiting S2S callback. |
| **Referrals** | `referral_registered` | **High** | Inbound Referral Share, Attribution Linkage Rate | Only final user profile stores referral code; no clickstream event. | Emit from auth gateway when new user applies referral code. |
| **Referrals** | `referral_activated` | **High** | Referral Activation Rate, Human vs Bot Install Ratio | No event distinguishing active referees from empty signups. | Emit when referee finishes onboarding + first active session. |
| **Account** | `user_registered` | **High** | Total Sign-ups, CAC by Channel, Registration Velocity | Registration timestamp stored in DB table, but no streaming event. | Instrument auth service registration form handler. |
| **Account** | `user_logged_in` | **High** | DAU, WAU, MAU, Session Initiation Cadence | Sessions stored in aggregate mart; atomic login event missing. | Emit from auth gateway upon JWT issuance. |
| **Account** | `onboarding_started` | **High** | Onboarding Funnel Drop-off Rate, Initial Funnel Velocity | Only final onboarding status is tracked on user profile. | Emit from client SDK upon tutorial wizard launch. |
| **Account** | `onboarding_completed`| **High** | Onboarding Completion Rate, Day 1 Activation Rate | No event capturing step progression or tutorial friction screens. | Emit from client SDK upon tutorial completion/skip. |
| **Tasks** | `task_started` | **High** | Task Start Volume, Task Engagement Rate | Simulated data uses feature-specific verbs (`ad_started`). | Deploy unified canonical `task_started` wrapper event. |
| **Tasks** | `task_completed` | **High** | Task Completion Rate, Earned XP per User | Logged as row in `04_Task_Activity`, not in event stream. | Emit unified streaming event alongside DB row insertion. |
| **Tasks** | `task_failed` | **High** | Task Failure Rate, Technical Error Rate | Non-completions exist in task table without streaming errors. | Instrument client SDK crash/timeout/abandonment handlers. |
| **Account** | `user_logged_out` | **Medium** | Average Session Duration, Session Clean Boundary Rate | Inactivity timeouts inferred retrospectively; no logout event. | Emit from client SDK on explicit logout or app backgrounding. |
| **Tasks** | `task_viewed` | **Medium** | Task Impression Reach, Task Discovery CTR | Impression-level catalog views are not instrumented. | Deploy viewport visibility tracker on task catalog cards. |
| **Tasks** | `task_opened` | **Medium** | Task Detail Click-Through Rate (CTR), Selection Affinity | User click-intent before launching tasks is omitted. | Emit when user expands task detail modal/drawer. |
| **Daily Habits** | `streak_updated` | **Medium** | Streak Continuity Rate, Habituation Index | Streak resets and increments calculated off-line in daily mart. | Emit from streak service upon midnight UTC day rollover. |

---
---

## 5. Master Analytics Gaps Register

The following systematic register logs the 12 core telemetry, architectural, and dimensional gaps identified across the VELOOP product analytics foundation:

| Gap ID | Product Area | Identified Telemetry / Data Gap | Impact on Reporting & Analytics | Priority | Underlying Technical Reason |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **GAP-001** | **Wallet** | Lack of an immutable double-entry wallet transactions ledger | Inability to reconstruct running balances over time, audit point breakage, reconcile liability, or model point economy inflation. | **Critical** | Supplied dataset only provides a static `xp_balance` snapshot on Users and a binary flag in Daily Activity; no transactional ledger exists. |
| **GAP-002** | **Withdrawals** | Complete absence of withdrawal requests and payout disbursement tables | Total blindness to platform cash burn, payout processing latency, payment gateway failure rates, and liquidity forecasting. | **Critical** | Standalone withdrawal tables were omitted entirely from the source data export. |
| **GAP-003** | **Referrals** | Missing outbound referral invitations, share channels, and link click tracking | Cannot calculate viral K-factor (invitations sent vs conversions), evaluate share-to-install drop-offs, or identify high-performing share channels. | **Critical** | Telemetry only records referee signups upon arrival; the outbound viral distribution funnel is not instrumented. |
| **GAP-004** | **Rewards Catalog** | Absence of a master reward catalog and redemption order fact table | Inability to evaluate reward SKU popularity, brand affinity (Amazon vs Flipkart), catalog stockouts, or merchant unit economic margins. | **Critical** | Datasets track only aggregate counts of reward events; item-level SKU redemptions are not captured. |
| **GAP-005** | **Tasks** | Missing Task Master dimension table for the 80 distinct `task_id`s in `Task_Activity` | Cannot benchmark task completion rates by difficulty tier, partner advertiser payout rate, or expected duration. | **High** | `05_Task_Activity` contains `task_id` strings (`TASK0001`–`TASK0080`) without a parent dimension catalog table. |
| **GAP-006** | **Telemetry Identity** | Absence of `task_id` attribute in `03_Feature_Events` clickstream table | Cannot join micro-level user clickstream events to specific task attempts to analyze user behavioral friction before task abandonment. | **High** | `Feature_Events` logs generic feature and event names but lacks task entity context in its event schema payload. |
| **GAP-007** | **Fraud & Risk** | Zero telemetry for reward clawbacks, multi-account device hashes, or dispute dispositions | Inability to detect emulator click-farms, calculate net earned vs clawed-back points, or audit anti-bot security filters. | **Critical** | No reversal status values, device hardware identifiers (IMEI/MAC), or fraud disposition codes exist in the data. |
| **GAP-008** | **Onboarding** | Onboarding tracked only as a coarse 3-state profile attribute without step-level funnel events | Product managers cannot identify specific tutorial friction screens causing new user activation drop-offs. | **High** | Only final state (`onboarding_status`) is stored on the user profile; micro-step progress events (`onboarding_step_completed`) are absent. |
| **GAP-009** | **Timezone Standards** | Absence of explicit ISO-8601 UTC designators and client clock synchronization metadata | Daily cohort boundaries, streak calculations, and retention curves may shift depending on whether timestamps are interpreted as UTC or IST. | **Medium** | Timestamps in source tables are unzoned datetime strings without explicit offset metadata (`Z` or `+05:30`). |
| **GAP-010** | **Help Center** | Zero tracking of customer support inquiries, FAQ article views, or ticket resolutions | Inability to identify user friction hot-spots, dispute frequency over failed payouts, or support resolution SLA efficiency. | **Medium** | No customer support ticketing or knowledge base interaction events exist in the telemetry taxonomy. |
| **GAP-011** | **Ad Mediation** | Missing third-party ad mediation postback webhooks and eCPM transaction logs | Cannot reconcile publisher revenue against awarded user points or verify ad viewability against click-fraud. | **High** | Ad views are captured solely via client-side events without third-party server-to-server validation. |
| **GAP-012** | **Observation Horizon** | Snapshot baseline calculation timestamp preceded registration for 8 users, with activity extending past Sept 15 | Produces negative derived metrics (`days_since_registration = -0.8`) and unpartitioned future activity data. | **Medium** | Snapshot date logic was hardcoded without boundary clamping against max registration timestamp in the synthetic generator. |


## Data Authenticity Statement
This analytics gap audit was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.

