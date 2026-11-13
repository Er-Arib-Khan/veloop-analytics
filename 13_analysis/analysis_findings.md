> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.** All figures below describe the supplied simulated dataset. They are NOT actual VELOOP user, revenue, retention, or performance statistics.

# VELOOP Product Analytics Findings Report

This document compiles the empirical analysis of the simulated datasets provided in `00_source_data/veloop_simulated_user_behavior_1000.xlsx` and `00_source_data/veloop_rewards_data_01.xlsx`. All metrics and findings represent executed computations preserved in `13_analysis/outputs/`.

---

## 1. Dataset Profile (Verified)

All figures below are transcribed verbatim from `13_analysis/outputs/01_profiling.json`.

| Sheet | Rows | Columns | Date Range | Status |
| :--- | :--- | :--- | :--- | :--- |
| `01_Users_1000` | 1000 | 16 | 2026-04-01 to 2026-09-15 | Usable |
| `02_Sessions` | 7913 | 12 | 2026-04-02 to 2026-09-15 | Usable |
| `03_Feature_Events` | 35704 | 13 | 2026-04-02 to 2026-09-15 | Usable |
| `04_Daily_Activity` | 6667 | 17 | 2026-04-02 to 2026-09-15 | Usable |
| `05_Task_Activity` | 9846 | 12 | 2026-04-02 to 2026-09-15 | Partial (missing reward_amount) |
| `06_Milestones` | 4799 | 6 | 2026-04-02 to 2026-09-15 | Usable |
| `07_Feature_Usage` | 15 | 7 | N/A (static feature catalog summary) | Usable |
| `08_Data_Dictionary` | 26 | 7 | N/A (metadata definitions) | Usable |
| `09_README_Status` | 15 | 2 | N/A (workbook metadata) | Usable |
| `10_Event_Data_Quality_Audit` | 35714 | 13 | 2026-04-02 to 2026-09-15 | Usable (QA audit dirty baseline) |
| `Users_1000_Clean` | 1000 | 27 | 2026-04-01 to 2026-09-17 | Usable |
| `Users_Messy_Audit` | 1008 | 28 | 2026-04-01 to 2026-09-17 | Usable (QA audit dirty baseline) |
| `Data_Dictionary` | 25 | 5 | N/A (metadata definitions) | Usable |
| `Synthetic_Summary` | 8 | 2 | N/A (generation summary metadata) | Usable |
| `README_Data_Status` | 7 | 2 | N/A (workbook metadata) | Usable |

---

## 2. Actual KPI Results

All values are transcribed directly from `13_analysis/outputs/02_kpis.json`.

| KPI ID | KPI Name | Value | Unit | Source | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **K01** | Total registered users | 1000 | users | `01_Users_1000`, `Users_1000_Clean` | OK |
| **K02** | Registrations by day (last 30 days) | 184 total registrations (2026-08-17 to 2026-09-15 timeseries: min 3, max 10, mean 6.13/day) | timeseries (daily registration count) | `01_Users_1000` | OK |
| **K03** | New users in last 7 days | 47 | users | `01_Users_1000` | OK |
| **K04** | Users active in last 7 days (WAU) | 486 | users | `03_Feature_Events`, `04_Daily_Activity` | OK |
| **K05** | Users active in last 30 days (MAU) | 812 | users | `03_Feature_Events`, `04_Daily_Activity` | OK |
| **K06** | DAU for the last 30 calendar days | 30 calendar days timeseries (min 66, max 164, mean 103.5 users/day) | timeseries (daily active users) | `04_Daily_Activity`, `03_Feature_Events` | OK |
| **K07** | DAU/MAU ratio | 0.1275 (12.75%) | ratio | `04_Daily_Activity`, `03_Feature_Events` | OK |
| **K08** | Users who have ever logged in | 92.8 (928 users; 98.4% / 984 users recorded in sessions) | % of registered | `Users_1000_Clean`, `02_Sessions` | OK |
| **K09** | Users who have NEVER logged in | 72 (7.2% day-0 dormant; 16 users / 1.6% have zero sessions) | users | `Users_1000_Clean`, `02_Sessions` | OK |
| **K10** | Returning users (active on ≥2 distinct days) | 826 (82.6%; 819 users / 81.9% in Users_1000_Clean) | users | `04_Daily_Activity`, `Users_1000_Clean` | OK |
| **K11** | Inactive users (registered but no event in last 14 days) | 346 (34.6%) | users | `01_Users_1000`, `03_Feature_Events` | OK |
| **K12** | Total sessions | 7913 | sessions | `02_Sessions` | OK |
| **K13** | Average sessions per user | 7.913 (8.042 per session-active user) | sessions/user | `02_Sessions`, `01_Users_1000` | OK |
| **K14** | Average session duration (seconds) | 51.81 (median 44.0) | seconds | `02_Sessions` | OK |
| **K15** | Feature adoption rate per feature | Watch Ads: 83.6%, Daily Reward: 83.5%, Streak Rewards: 83.2%, CAPTCHA: 82.4%, Referral: 81.1%, Wallet: 81.0%, Tap & Earn: 80.0%, Mining Rewards: 79.9%, Level System: 77.3%, Missions: 77.1%, Spin the Wheel: 76.3%, Exchange Center: 72.0%, Leaderboard: 68.6%, Follow & Earn: 68.5%, Badges: 67.4% | % of registered users | `03_Feature_Events`, `07_Feature_Usage`, `01_Users_1000` | OK |
| **K16** | Feature usage frequency per user | Watch Ads: 3.74, Missions: 3.61, CAPTCHA: 3.32, Tap & Earn: 3.32, Streak Rewards: 3.29, Mining Rewards: 3.27, Spin the Wheel: 3.18, Level System: 3.14, Referral: 3.11, Daily Reward: 2.99, Badges: 2.72, Leaderboard: 2.68, Wallet: 2.68, Follow & Earn: 2.42, Exchange Center: 2.35 (Overall: 35.70) | events/user per feature | `03_Feature_Events`, `07_Feature_Usage` | OK |
| **K17** | Top 5 features by unique users | 1. Watch Ads (836), 2. Daily Reward (835), 3. Streak Rewards (832), 4. CAPTCHA (824), 5. Referral (811) | ranking (unique users) | `03_Feature_Events`, `07_Feature_Usage` | OK |
| **K18** | Top 5 features by total events | 1. Watch Ads (3126), 2. Missions (2780), 3. Streak Rewards (2734), 4. CAPTCHA (2733), 5. Tap & Earn (2654) | ranking (total events) | `03_Feature_Events`, `07_Feature_Usage` | OK |
| **K19** | Repeat usage rate | Missions: 79.90%, Watch Ads: 76.56%, Streak Rewards: 76.08%, Daily Reward: 73.89%, Tap & Earn: 73.50%, Level System: 73.48%, CAPTCHA: 73.18%, Spin the Wheel: 72.74%, Mining Rewards: 72.34%, Referral: 71.64%, Wallet: 70.00%, Follow & Earn: 64.09%, Leaderboard: 63.56%, Badges: 63.06%, Exchange Center: 60.00% (Platform-wide: 97.40%) | % repeat users per feature | `03_Feature_Events` | OK |
| **K20** | Total tasks started | 9846 | tasks | `05_Task_Activity` | OK |
| **K21** | Total tasks completed | 5627 | tasks | `05_Task_Activity` | OK |
| **K22** | Task completion rate | 0.5715 (57.15%) | rate | `05_Task_Activity` | OK |
| **K23** | Task failure rate | 0.1544 (15.44% explicit failure; 20.83% / 2,051 abandoned; 36.27% total non-completion) | rate | `05_Task_Activity` | OK |
| **K24** | Average task completion time (seconds) | 304.50 (median 304.0) | seconds | `05_Task_Activity` | OK |
| **K25** | Task attempts per task_type | Advertisement: 2203, App Task: 1327, Survey: 1259, CAPTCHA: 1143, Social Activity: 1020, Game: 1008, Mission: 985, Promotional Task: 901 | distribution (attempts by category) | `05_Task_Activity` | OK |
| **K26** | Users who completed ≥1 task | 981 (98.1%) | users | `05_Task_Activity` | OK |
| **K27** | Users who completed ≥5 tasks | 689 (68.9% power users) | users | `05_Task_Activity` | OK |
| **K28** | Total reward amount credited | 242830 (milestone reward units; 231,889 XP in Users_1000_Clean) | reward units / XP | `06_Milestones`, `Users_1000_Clean` | OK |
| **K29** | Average reward per completed task | BLOCKED: 05_Task_Activity lacks a numeric reward_amount column, and Task_Master / Wallet_Ledger tables are missing | reward units/task | `05_Task_Activity` | BLOCKED |
| **K30** | Reward distribution by task_type | BLOCKED: 05_Task_Activity lacks reward_amount column, and Task_Master / Wallet_Ledger tables are missing | distribution (reward amount by task_type) | `05_Task_Activity` | BLOCKED |
| **K31** | Reward distribution by feature | Watch Ads: 22500, Streak Rewards: 19010, Missions: 18105, Tap & Earn: 18100, CAPTCHA: 17755, Referral: 17655, Spin the Wheel: 17565, Daily Reward: 16385, Level System: 16080, Mining Rewards: 15415, Leaderboard: 14750, Wallet: 14645, Exchange Center: 11365, Badges: 10905, Follow & Earn: 10515, Onboarding: 2080 | distribution (reward units / XP by feature) | `06_Milestones`, `03_Feature_Events` | OK |
| **K32** | Reward reversals (count and %) | BLOCKED: Wallet_Ledger is missing and reward_status lacks a Reversal status | count and percentage | `05_Task_Activity` | BLOCKED |
| **K33** | Users who have earned at least one reward | 1000 (100.0%; 981 users have credited tasks in 05_Task_Activity) | users | `06_Milestones`, `05_Task_Activity`, `Users_1000_Clean` | OK |
| **K34** | D1 retention | 17.91 (178 / 994 eligible users; 17.80% of all 1,000 users) | % eligible users active on D1 | `01_Users_1000`, `04_Daily_Activity` | OK |
| **K35** | D7 retention | 13.33 (127 / 953 eligible users; 12.70% of all 1,000 users) | % eligible users active on D7 | `01_Users_1000`, `04_Daily_Activity` | OK |
| **K36** | D30 retention | 8.46 (69 / 816 eligible users; 6.90% of all 1,000 users) | % eligible users active on D30 | `01_Users_1000`, `04_Daily_Activity` | OK |
| **K37** | Retention curve (D1..D30 timeseries) | 30 points (D1: 17.91% down to D30: 8.46%) | timeseries (plot-ready retention curve D1..D30) | `01_Users_1000`, `04_Daily_Activity` | OK |
| **K38** | Duplicate user_ids | 16 (8 distinct duplicated user_ids) | rows | `Users_Messy_Audit` | OK |
| **K39** | Rows with missing user_id | 0 | rows | `Users_Messy_Audit`, `10_Event_Data_Quality_Audit` | OK |
| **K40** | Rows with malformed or null timestamps | 2 (1 null registration timestamp, 1 invalid month 14) | rows | `Users_Messy_Audit` | OK |
| **K41** | Invalid status values | 4 (event_status = 'success ' outside canonical enum) | rows | `10_Event_Data_Quality_Audit` | OK |
| **K42** | Orphan records (user_id not in users) | 0 | records | `10_Event_Data_Quality_Audit`, `Users_1000_Clean`, `02_Sessions`, `05_Task_Activity` | OK |
| **K43** | Negative amounts | 4 (days_since_registration < 0: -0.803, -0.655, -0.412, -0.198) | rows | `Users_Messy_Audit`, `Users_1000_Clean` | OK |
| **K44** | Trailing-whitespace categorical values | 4 ('success ' in event_status) | rows | `10_Event_Data_Quality_Audit` | OK |
| **K45** | Wallet credits total | BLOCKED: Wallet_Ledger table is missing from supplied workbooks | currency / XP | `Wallet_Ledger` | BLOCKED |
| **K46** | Withdrawal completion rate | BLOCKED: Withdrawals table is missing from supplied workbooks | % | `Withdrawals` | BLOCKED |
| **K47** | Withdrawal processing time (median) | BLOCKED: Withdrawals table is missing from supplied workbooks | seconds / hours | `Withdrawals` | BLOCKED |
| **K48** | Referral conversion rate | BLOCKED: Referral_Invites and Referral_Conversions tables are missing from supplied workbooks | % | `Referral_Invites`, `Referral_Conversions` | BLOCKED |
| **K49** | Referral activations | BLOCKED: Referral_Activations table is missing from supplied workbooks | activations | `Referral_Activations` | BLOCKED |

---

## 3. Findings — What the Data Actually Shows

1. **Finding 1 — User Base & Verification Bottleneck (K01, K08, K09):**  
   Out of 1,000 total registered users in `01_Users_1000` (K01), exactly 928 users (92.8%) logged in at least once (K08), while 72 users (7.2%) never logged in and remained dormant from day 0 in `Users_1000_Clean` (K09).  
   *Implication:* The initial verification step is an onboarding leak where 7.2% of registered accounts drop off before recording their first session.

2. **Finding 2 — Active User Engagement & DAU/MAU Stickiness (K04, K05, K06, K07):**  
   In `03_Feature_Events` and `04_Daily_Activity`, the active user base spans 812 MAU (K05) and 486 WAU (K04), with a 30-day mean DAU of 103.50 users (K06), producing a DAU/MAU stickiness ratio of 0.1275 or 12.75% (K07).  
   *Implication:* While monthly active reach is wide (81.2% of registered accounts), daily app engagement remains concentrated among approximately one-eighth of the monthly cohort.

3. **Finding 3 — High Repeat Engagement vs. Mid-Funnel Dormancy (K10, K11):**  
   826 users (82.6%) returned across ≥2 distinct active days in `04_Daily_Activity` (K10), yet 346 registered users (34.6%) recorded zero events in the final 14 calendar days of observation in `03_Feature_Events` (K11).  
   *Implication:* Users who survive the initial onboarding hurdle exhibit multi-day repeat usage, but roughly one-third of the user base eventually enters an unengaged state within a two-week window.

4. **Finding 4 — Session Volume & Short Micro-Session Duration (K12, K13, K14):**  
   The application accumulated 7,913 total sessions in `02_Sessions` (K12), averaging 7.913 sessions per registered user (K13), with an average session duration of 51.81 seconds (median 44.0s) (K14).  
   *Implication:* User interaction is structured around brief micro-visits under one minute rather than sustained dwell sessions.

5. **Finding 5 — Feature Adoption Ceiling Across Utilities (K15, K17):**  
   In `03_Feature_Events` and `07_Feature_Usage`, Watch Ads achieved the highest unique user adoption at 83.6% (836 users, K15/K17), followed by Daily Reward (83.5%, 835 users) and Streak Rewards (83.2%, 832 users), whereas Badges had the lowest adoption at 67.4% (674 users).  
   *Implication:* Passive and low-friction earning mechanics (watching ads, claiming daily streaks) engage over 83% of the user base, whereas gamified reputation mechanics (badges) experience a 16.2 percentage-point lower adoption rate.

6. **Finding 6 — Event Volume Concentration in Ads and Missions (K16, K18):**  
   Total event volume in `03_Feature_Events` reached 35,704 events (averaging 35.70 events per registered user), with Watch Ads generating the most interactions at 3,126 events (3.74 events/user, K16/K18), followed by Missions at 2,780 events (3.61 events/user) and Streak Rewards at 2,734 events (3.29 events/user).  
   *Implication:* Behavioral volume is heavily concentrated in direct incentivized monetization loops rather than exploratory features.

7. **Finding 7 — Missions Drive the Strongest Repeat Interaction (K19):**  
   Missions achieved the highest repeat usage rate in `03_Feature_Events` with 79.90% of its participants executing ≥2 events (K19), followed by Watch Ads (76.56%) and Streak Rewards (76.08%), while Exchange Center had the lowest repeat rate at 60.00%.  
   *Implication:* Structured progressive objectives (missions) create stronger recurrent habituation than one-off catalog exploration (exchange center).

8. **Finding 8 — Task Completion Rate and Non-Completion Attribution (K20, K21, K22, K23):**  
   Out of 9,846 tasks started in `05_Task_Activity` (K20), 5,627 reached an explicit completed status for a completion rate of 57.15% (K22), with explicit task failures accounting for 15.44% (1,520 tasks, K23) and user abandonment accounting for 20.83% (2,051 tasks), yielding an aggregate non-completion rate of 36.27%.  
   *Implication:* More than one out of every three attempted tasks fails to finish, with user drop-off (abandonment) causing 1.35 times more lost completions than system or execution errors.

9. **Finding 9 — Homogeneous Completion Rates Across Task Types (K25):**  
   Task activity in `05_Task_Activity` is led by Advertisement attempts (2,203 rows; 22.38% of all attempts, K25), App Tasks (1,327), and Surveys (1,259), yet completion rates remain remarkably flat across all 8 categories (ranging from 56.08% for Social Activity to 58.16% for Promotional Task).  
   *Implication:* Task non-completion is driven by systemic platform UX frictions or uniform user attention limits rather than specific category-level difficulty spikes.

10. **Finding 10 — High Execution Latency & Power User Concentration (K24, K26, K27):**  
    Completed tasks in `05_Task_Activity` required an average completion time of 304.50 seconds (~5.08 minutes, median 304.0s) (K24), with 981 unique users completing ≥1 task (K26) and 689 users (68.9%) completing ≥5 tasks (K27).  
    *Implication:* The core task engine relies on a dedicated group of 689 power users willing to spend 5 minutes per micro-task.

11. **Finding 11 — Milestone Reward Disbursement Alignment (K28, K31, K33):**  
    A cumulative 242,830 milestone reward units were credited across 4,799 milestone awards in `06_Milestones` (K28), with 1,000 out of 1,000 registered users receiving ≥1 milestone reward (K33), led by Watch Ads awards (22,500 units; 9.27% of volume, K31) and Streak Rewards (19,010 units; 7.83%), closely aligning with the 231,889 XP total balance recorded in `Users_1000_Clean`.  
    *Implication:* Milestone incentive disbursements are fully distributed across all users, with monetization features serving as the primary currency issuance source.

12. **Finding 12 — Ongoing Acquisition Inflow Velocity (K02, K03):**  
    During the final 30 calendar days of observation in `01_Users_1000`, 184 new users registered (K02), including 47 users within the final 7 days (K03), representing 18.4% of total lifetime registrations.  
    *Implication:* The simulated cohort represents an actively expanding user base with an inflow velocity of 6.13 new users per day.

13. **Finding 13 — Retention Decay Profile (K34, K35, K36, K37):**  
    Standard cohort retention in `04_Daily_Activity` drops from D1 = 17.91% (178 retained / 994 eligible users, K34) to D7 = 13.33% (127 retained / 953 eligible users, K35), before stabilizing at D30 = 8.46% (69 retained / 816 eligible users, K36).  
    *Implication:* The steepest retention loss occurs immediately between registration and Day 1 (an 82.09% drop), after which attrition slows to a steady baseline of ~8.5% at 30 days.

14. **Finding 14 — Telemetry Quality & Schema Integrity Audit (K38, K40, K41, K42, K43, K44):**  
    Audit analysis of `Users_Messy_Audit` and `10_Event_Data_Quality_Audit` detected 16 duplicate user rows (8 distinct user IDs, K38), 2 invalid registration timestamps (1 null, 1 month-14 error, K40), 4 negative days-since-registration values (K43), and 4 trailing-whitespace status strings ('success ', K41/K44), while confirming zero orphan records across all activity tables (K42) and zero missing user IDs (K39).  
    *Implication:* Data pipeline anomalies are isolated to pre-ingestion client payload formatting and unconstrained synthetic generation retries, while relational foreign-key integrity remains intact.

---

## 4. What Could Not Be Calculated (and why)

The table below lists all 8 BLOCKED KPIs, stating the blocker reason, missing source entities, and business analytical impact.

| KPI ID | KPI Name | Reason | Missing Data | Impact |
| :--- | :--- | :--- | :--- | :--- |
| **K29** | Average reward per completed task | 05_Task_Activity lacks a numeric reward_amount column; Task_Master and Wallet_Ledger tables are missing | Task payout rate, task reward dimension, or wallet transaction ledger | Inability to evaluate unit economics, payout per completed task, or task ROI benchmarks. |
| **K30** | Reward distribution by task_type | 05_Task_Activity lacks a reward_amount column; Task_Master and Wallet_Ledger tables are missing | Reward payout currency mapped by task_category | Cannot determine which task types (surveys vs games vs ads) generate the largest liability burn. |
| **K32** | Reward reversals (count and %) | Wallet_Ledger is missing and 05_Task_Activity reward_status lacks a Reversal status | Wallet transaction clawbacks, reversal logs, or dispute records | Blindness to fraud clawbacks, failed payout revocations, and chargeback exposure. |
| **K45** | Wallet credits total | Wallet_Ledger table is missing from supplied workbooks | Double-entry append-only wallet transaction ledger | Cannot audit cumulative XP/currency liability, inflation rate, or source-of-funds balances. |
| **K46** | Withdrawal completion rate | Withdrawals table is missing from supplied workbooks | Cash/UPI/voucher disbursement request table with status | Cannot assess payment gateway SLA, payout failure rate, or disbursement cash burn. |
| **K47** | Withdrawal processing time (median) | Withdrawals table is missing from supplied workbooks | Withdrawal request creation and disbursement completed timestamps | Inability to track payment processing latency or payout operational bottlenecks. |
| **K48** | Referral conversion rate | Referral_Invites and Referral_Conversions tracking tables are missing from supplied workbooks | Outbound invite generation events and referee conversion attribution links | Cannot compute viral invite-to-registration conversion funnel or K-factor. |
| **K49** | Referral activations | Referral_Activations table is missing from supplied workbooks | Downstream referee milestone activation logs (e.g. referee first task/payout) | Inability to evaluate referral qualification depth or referral fraud rate. |

---

## 5. Retention Analysis

Retention analysis was performed by evaluating active user activity in `04_Daily_Activity` (`active_flag = 'Yes'`) against the user's registration date in `01_Users_1000`. Cohort eligibility was restricted to users registered at least $N$ days prior to the dataset end date (`2026-09-15`).

### Summary Milestones
- **D1 Retention (K34):** **17.91%** (178 retained users out of 994 eligible users; 17.80% of total 1,000 users)
- **D7 Retention (K35):** **13.33%** (127 retained users out of 953 eligible users; 12.70% of total 1,000 users)
- **D30 Retention (K36):** **8.46%** (69 retained users out of 816 eligible users; 6.90% of total 1,000 users)

### Complete Retention Curve (D1..D30 Timeseries — K37)

The table below presents the verified daily cohort retention curve ready for plotting.

| Day Offset | Day Index | Eligible Users | Retained Users | Retention Rate (%) |
| :--- | :--- | :--- | :--- | :--- |
| **D1** | 1 | 994 | 178 | 17.91% |
| **D2** | 2 | 991 | 169 | 17.05% |
| **D3** | 3 | 980 | 150 | 15.31% |
| **D4** | 4 | 974 | 136 | 13.96% |
| **D5** | 5 | 963 | 136 | 14.12% |
| **D6** | 6 | 959 | 127 | 13.24% |
| **D7** | 7 | 953 | 127 | 13.33% |
| **D8** | 8 | 945 | 107 | 11.32% |
| **D9** | 9 | 933 | 118 | 12.65% |
| **D10** | 10 | 926 | 103 | 11.12% |
| **D11** | 11 | 920 | 117 | 12.72% |
| **D12** | 12 | 914 | 100 | 10.94% |
| **D13** | 13 | 912 | 110 | 12.06% |
| **D14** | 14 | 904 | 109 | 12.06% |
| **D15** | 15 | 894 | 87 | 9.73% |
| **D16** | 16 | 893 | 94 | 10.53% |
| **D17** | 17 | 888 | 87 | 9.80% |
| **D18** | 18 | 880 | 74 | 8.41% |
| **D19** | 19 | 871 | 90 | 10.33% |
| **D20** | 20 | 864 | 85 | 9.84% |
| **D21** | 21 | 859 | 93 | 10.83% |
| **D22** | 22 | 853 | 80 | 9.38% |
| **D23** | 23 | 845 | 83 | 9.82% |
| **D24** | 24 | 841 | 69 | 8.20% |
| **D25** | 25 | 838 | 80 | 9.55% |
| **D26** | 26 | 836 | 78 | 9.33% |
| **D27** | 27 | 833 | 76 | 9.12% |
| **D28** | 28 | 821 | 83 | 10.11% |
| **D29** | 29 | 819 | 61 | 7.45% |
| **D30** | 30 | 816 | 69 | 8.46% |

---

## 6. Data Quality Snapshot

Data quality metrics derived from `Users_Messy_Audit` and `10_Event_Data_Quality_Audit` (K38–K44) are summarized below.

| Issue | Count | % of Rows | Severity | Example Row Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Duplicate user_ids (K38)** | 16 rows (8 distinct IDs) | 1.59% (of 1,008 rows) | Critical | `Users_Messy_Audit` row index 141 & 142 (`user_id`: VLUSR000142, Aditya Patel) |
| **Missing user_id (K39)** | 0 rows | 0.00% | Informational | Zero nulls across `Users_Messy_Audit` and `10_Event_Data_Quality_Audit` |
| **Malformed or null timestamps (K40)** | 2 rows | 0.20% (of 1,008 rows) | Critical | `Users_Messy_Audit` row index 451 (VLUSR000451: null) & row index 788 (VLUSR000788: `2026-14-05 10:15:00` month 14) |
| **Invalid status values (K41)** | 4 rows | 0.01% (of 35,714 rows) | Medium | `10_Event_Data_Quality_Audit` row index 15024 (`event_id`: EVT0015025, `event_status`: `'success '`) |
| **Orphan records (user_id not in users) (K42)** | 0 records | 0.00% | Informational | All 35,714 events, 7,913 sessions, and 9,846 tasks reference valid user IDs in `Users_1000_Clean` |
| **Negative amounts (K43)** | 4 rows | 0.40% (of 1,008 rows) | Medium | `Users_Messy_Audit` row index 18 (VLUSR000019: `days_since_registration` = -0.803) |
| **Trailing-whitespace categorical values (K44)** | 4 rows | 0.01% (of 35,714 rows) | Medium | `10_Event_Data_Quality_Audit` row index 15024 (`event_status`: `'success '` with trailing space) |

---

## 7. Data Authenticity Statement

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.**  
> All figures, tables, distributions, and findings contained in this document describe the supplied synthetic test datasets (`00_source_data/veloop_simulated_user_behavior_1000.xlsx` and `00_source_data/veloop_rewards_data_01.xlsx`). They were generated via Python execution in `13_analysis/run_analysis.py` for platform capability validation and analytical benchmarking. They do NOT represent actual VELOOP production telemetry, live user metrics, financial balances, or business performance.
