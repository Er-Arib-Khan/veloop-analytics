# VELOOP Rewards — Analytics Foundation: Executive Summary

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.** All figures in this
> document describe the supplied simulated dataset. Not actual VELOOP statistics.
> They are NOT actual VELOOP user, revenue, retention, conversion, or performance statistics.

**Live interactive dashboard:** https://er-arib-khan.github.io/veloop-analytics/
**Data provenance & authenticity:** [docs/data_provenance.md](../docs/data_provenance.md)
**Full analysis:** [13_analysis/analysis_findings.md](../13_analysis/analysis_findings.md)
**Recommendations:** [13_analysis/business_recommendations.md](../13_analysis/business_recommendations.md)
**KPI register (49 KPIs):** [13_analysis/outputs/02_kpis.json](../13_analysis/outputs/02_kpis.json)

---

## 1. What the Data Shows

• Task completion rate is 57.15% (K22): of 9,846 tasks started, only 5,627 completed. 15.44% failed (1,520), 20.83% were abandoned (2,051), and 6.58% are still pending (648) — an aggregate not-completed rate of 42.85%. This aggregate drop-off reveals severe friction across the primary monetization funnel, where more than four in ten initiated tasks fail to yield completed actions.

• Failure attribution: across 1,520 explicit task failures, failure is concentrated in two categories: Validation failed (48.16%, 732 tasks) and Task unavailable (47.50%, 722 tasks), with Timeout at 4.34% (66 tasks). In total, 95.66% of explicit task failures (1,454 attempts, K23) fall into these two buckets. The supplied data does not distinguish whether "Validation failed" originates from VELOOP's own rule engine, a third-party callback, or client payload issues, and "Task unavailable" could stem from VELOOP internal inventory exhaustion or third-party partner supply (requires verification; logged in Assumption Register as A010).

• Retention decays steeply: D1 = 17.91% (K34), D7 = 13.33% (K35), D30 = 8.46% (K36). The steepest single drop is D1→D7 (−4.58 points). More than four-fifths of newly acquired users drop off before recording activity on Day 1, and early cohort decay concentrates heavily in the first post-registration week before flattening into a long-tail baseline of 8.46% at Day 30 (K36).

• Activation gap: 72 users (7.2%) registered but never logged in — dormant from day 0 (K09). 346 users (34.6%) have no event in the final 14 days (K11). A critical onboarding friction point occurs during initial verification, while more than one-third of the user cohort exhibits complete late-stage dormancy with zero recorded sessions or feature interactions in the final two weeks (K11).

• Engagement is concentrated: 689 users (68.9%) completed ≥5 tasks (K27), while the three lowest-adopted features — Badges (67.4%), Follow & Earn (68.5%), Leaderboard (68.6%) — trail the platform's 83.6% top adoption (Watch Ads, K15). The user base bifurcates into a highly engaged core of multi-task power users and a passive majority that gravitates toward low-friction ad viewing while underutilizing social and community modules.

• Data integrity: 16 duplicate user rows across 8 distinct user IDs (K38), 2 malformed timestamps (K40), 4 invalid status-enum rows (K41 = K44, same 4 rows), 4 negative days-since-registration values (K43). Zero orphan records across all activity tables (K42) — referential integrity is intact. While foreign-key linkages across sessions, events, tasks, and milestones are clean, client-side logging edge cases and ingestion pipelines introduce profile duplications and formatting defects that distort user aggregations.

• Virtual currency discrepancy: milestone awards sum to 242,830 units (K28, PARTIAL scope) while user XP balances sum to 231,889 XP — a 10,941 XP shortfall requiring engineering verification against transaction logs. The aggregate balance credited across recorded milestone events exceeds the cumulative user balances in the clean user profiles, demonstrating the absence of an authoritative, reconciled double-entry accounting ledger.

---

## 2. What Could Not Be Calculated (and Why)

| KPI ID | KPI Name | Missing Data | Business Impact |
| :--- | :--- | :--- | :--- |
| K29 | Average reward per completed task | 05_Task_Activity lacks reward_amount | Cannot price per-task economics |
| K30 | Reward distribution by task_type | 05_Task_Activity lacks reward_amount | Cannot detect reward bias by task category |
| K32 | Reward reversals | Wallet_Ledger missing | Cannot detect fraudulent or corrected rewards |
| K45 | Wallet credits total | Wallet_Ledger missing | Cannot measure total outstanding liability |
| K46 | Withdrawal completion rate | Withdrawals table missing | Cannot measure payout reliability |
| K47 | Withdrawal processing time | Withdrawals table missing | Cannot measure operational SLA |
| K48 | Referral conversion rate | Referral_Invites / Referral_Conversions missing | Cannot evaluate growth program ROI |
| K49 | Referral activations | Referral_Activations missing | Cannot attribute referral contribution to activation |

These 8 KPIs are blocked because the required transactional tables do not exist in the supplied simulated dataset. They are documented in the Assumption & Verification Register rather than invented.

---

## 3. Top 5 Business Recommendations

• **R7 — Build the double-entry Wallet_Ledger table (Priority: Critical).** Unblocks 4 blocked KPIs (K29, K30, K32, K45). Without a ledger, VELOOP cannot measure its own currency liability — the single largest analytics gap in the current model. Engineering must deploy an append-only ledger logging all credits, debits, and reversals with explicit currency types and source IDs to resolve reconciliation shortfalls like the 10,941 XP discrepancy (K28).

• **R2 — Deploy OTP verification and D1 activation bonuses (Priority: Critical).** Targets the 72 dormant users (K09) and 17.91% D1 retention (K34). Lowest effort of any critical recommendation. Product teams should implement automated SMS and WhatsApp verification retry triggers for pending signups, paired with an immediate first-login XP incentive credited upon opening the app within 24 hours of account creation to convert onboarding dropouts into retained daily active participants (K09, K34).

• **R4 — Restructure first-week streak progression (Priority: Critical).** Targets the −4.58 point D1→D7 drop (K34→K35), the steepest decay interval in the retention curve. Introducing an onboarding streak calendar with dedicated milestone reward multipliers and daily countdown push notifications creates habituation loops that bridge the week-one drop and lift downstream Day 30 retention (8.46%, K36).

• **R1 — Pre-filter task inventory and add retry logic for validation (Priority: High).** Targets the 42.85% not-completed rate (K22, K23), concentrated in two primary failure categories: Validation failed (732 tasks) and Task unavailable (722 tasks). Root-cause attribution between VELOOP internal engines and third-party systems requires engineering verification (A010). Deploying task inventory health checks and server-side validation retry logic targets up to 1,454 failed attempts (K23), driving overall task completion toward 70% (K22).

• **R6 — Enforce database UNIQUE constraints on user_id and enum-sanitize client status strings (Priority: High).** Eliminates the 16 duplicate rows (K38) and 4 whitespace-defect rows (K41/K44) that are currently being caught only at audit time. Applying strict primary key uniqueness in PostgreSQL ingestion pipelines and automated string trim sanitization in the logging SDK guarantees 100% data hygiene across all downstream analytics models.

---

## 4. What Engineering Must Do Next

1. Add a wallet_ledger table with columns: transaction_id (PK), user_id (FK), timestamp, transaction_type, amount, unit, status, reference_id, reversal_of (nullable FK). Unblocks K29, K30, K32, K45.

2. Add a withdrawals table with columns: withdrawal_id (PK), user_id (FK), requested_amount, method, requested_at, processing_at, completed_at, status, reason_category. Unblocks K46, K47.

3. Add referral_invites and referral_conversions tables with columns referral_id (PK), referrer_user_id, referred_user_id, created_at, registered_at, activated_at, converted_at, status. Unblocks K48, K49.

4. Add reward_amount and reward_unit columns to 05_Task_Activity. Unblocks K29, K30.

5. Add a task_abandoned_at timestamp to 05_Task_Activity so average time-to-abandon becomes measurable. Currently the 2,051 abandoned tasks have task_completed_at = null with no abandonment timestamp (K23).

---

## 5. Deliverables Index

- Live dashboard: https://er-arib-khan.github.io/veloop-analytics/
- Analysis findings: [13_analysis/analysis_findings.md](../13_analysis/analysis_findings.md)
- Business recommendations: [13_analysis/business_recommendations.md](../13_analysis/business_recommendations.md)
- KPI register (49 KPIs, 41 computed): [13_analysis/outputs/02_kpis.json](../13_analysis/outputs/02_kpis.json)
- Data profiling: [07_data_quality/profiling_summary.xlsx](../07_data_quality/profiling_summary.xlsx)
- Data dictionary: [05_data_model/data_dictionary.xlsx](../05_data_model/data_dictionary.xlsx)
- Data quality audit: [07_data_quality/data_quality_audit.xlsx](../07_data_quality/data_quality_audit.xlsx)
- Assumption & verification register: [01_governance/assumption_verification_register.xlsx](../01_governance/assumption_verification_register.xlsx)
- Implementation backlog: [11_backlog/implementation_backlog.xlsx](../11_backlog/implementation_backlog.xlsx)

---

## 6. Data Authenticity Statement

All figures in this document describe the supplied simulated dataset. Not actual VELOOP statistics. They are NOT actual VELOOP user counts, revenue, earnings, withdrawals, retention rates, conversion rates, or company statistics. Any figure that could not be computed from the supplied data is marked BLOCKED with the missing dependency named in Section 2. No production statistics are claimed or implied. See [docs/data_provenance.md](../docs/data_provenance.md) for the full provenance statement.
