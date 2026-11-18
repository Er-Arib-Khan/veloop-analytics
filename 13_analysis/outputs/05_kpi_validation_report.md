# VELOOP Analytics — Independent KPI Validation Report

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING**

## Summary

**`41 PASS · 0 PASS-ROUND · 0 FAIL · 8 BLOCKED-CONFIRMED · 0 BLOCKED-MISCLASSIFIED · 0 STRUCTURAL SUSPECT`**

---

## Part 0 — Structural Scan Results

No structural defects identified in `13_analysis/outputs/02_kpis.json`. All 49 KPI values are cleanly typed single values, validated numeric formats, structured objects, or canonical `null` blocks.

---

## Part 2 — Three-Way Reconciliation Diff Table (All 49 KPIs)

| KPI ID | Name | Reported Value | Recomputed Value | Delta | Verdict | Evidence / Formula |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **K01** | Total registered users | `1000` | `1000` | `0` | **PASS** | df_u1['user_id'].nunique() = 1000 |
| **K02** | Registrations by day (last 30 days) | `{'2026-08-17': 3, '2026-08-18': ...` | `{'2026-08-17': 3, '2026-08-18': ...` | `0` | **PASS** | u1_last_30.groupby('reg_date')['user_id'].count() over 30d (sum=184) |
| **K03** | New users in last 7 days | `47` | `47` | `0` | **PASS** | len(df_u1[reg_date in last_7d]) = 47 |
| **K04** | Users active in last 7 days (WAU) | `486` | `486` | `0` | **PASS** | df_events[ev_date in last_7d]['user_id'].nunique() = 486 |
| **K05** | Users active in last 30 days (MAU) | `812` | `812` | `0` | **PASS** | df_events[ev_date in last_30d]['user_id'].nunique() = 812 |
| **K06** | DAU for the last 30 calendar days | `{'2026-08-17': 72, '2026-08-18':...` | `{'2026-08-17': 72, '2026-08-18':...` | `0` | **PASS** | df_daily[active_flag=='Yes'].groupby('act_date')['user_id'].nunique() (30d mean=103.50) |
| **K07** | DAU/MAU ratio | `0.1275` | `0.1275` | `0.0` | **PASS** | mean(30d_DAU) / 30d_MAU = 103.50 / 812 = 0.1275 |
| **K08** | Users who have ever logged in | `98.4` | `98.4` | `0.0` | **PASS** | COUNT(DISTINCT user_id in 02_Sessions) / 1000 * 100.0 = 984 / 1000 * 100.0 = 98.4 |
| **K09** | Users who have NEVER logged in | `16` | `16` | `0` | **PASS** | 1,000 registered users - 984 session users = 16 |
| **K10** | Returning users (active on ≥2 distinct days) | `826` | `826` | `0` | **PASS** | (df_daily[active_flag=='Yes'].groupby('user_id')['act_date'].nunique() >= 2).sum() = 826 |
| **K11** | Inactive users (registered but no event in last 14 days) | `346` | `346` | `0` | **PASS** | len(set(01_Users_1000) - set(events_last_14d)) = 1000 - 654 = 346 |
| **K12** | Total sessions | `7913` | `7913` | `0` | **PASS** | len(df_sess) = 7913 |
| **K13** | Average sessions per user | `7.913` | `7.913` | `0.0` | **PASS** | 7913 sessions / 1000 users = 7.913 |
| **K14** | Average session duration (seconds) | `51.81` | `51.81` | `0.0` | **PASS** | df_sess['session_duration_seconds'].mean() = 51.81 |
| **K15** | Feature adoption rate per feature | `{'Watch Ads': 83.6, 'Daily Rewar...` | `{'Badges': 67.4, 'CAPTCHA': 82.4...` | `0` | **PASS** | df_events.groupby('feature_name')['user_id'].nunique() / 1000 * 100.0 across 15 features |
| **K16** | Feature usage frequency per user | `{'Badges': 2.72, 'CAPTCHA': 3.32...` | `{'Badges': 2.72, 'CAPTCHA': 3.32...` | `0` | **PASS** | events / unique_users per feature in 03_Feature_Events across 15 features |
| **K17** | Top 5 features by unique users | `[{'feature_name': 'Watch Ads', '...` | `[{'feature_name': 'Watch Ads', '...` | `0` | **PASS** | top 5 features: Watch Ads: 836, Daily Reward: 835, Streak Rewards: 832, CAPTCHA: 824, Referral: 811 |
| **K18** | Top 5 features by total events | `[{'feature_name': 'Watch Ads', '...` | `[{'feature_name': 'Watch Ads', '...` | `0` | **PASS** | top 5 features: Watch Ads: 3126, Missions: 2780, Streak Rewards: 2734, CAPTCHA: 2733, Tap & Earn: 2654 |
| **K19** | Repeat usage rate | `{'Badges': 63.06, 'CAPTCHA': 73....` | `{'Badges': 63.06, 'CAPTCHA': 73....` | `0` | **PASS** | repeat_users(>=2 events) / unique_users per feature across 15 features |
| **K20** | Total tasks started | `9846` | `9846` | `0` | **PASS** | len(df_task) = 9846 |
| **K21** | Total tasks completed | `5627` | `5627` | `0` | **PASS** | len(df_task[task_status=='Completed']) = 5627 |
| **K22** | Task completion rate | `0.5715` | `0.5715` | `0.0` | **PASS** | len(df[status=='Completed']) / len(df) = 5627 / 9846 = 0.5715 |
| **K23** | Task failure rate | `0.1544` | `0.1544` | `0.0` | **PASS** | len(df[status=='Failed']) / len(df) = 1520 / 9846 = 0.1544 |
| **K24** | Average task completion time (seconds) | `304.5` | `304.5` | `0.0` | **PASS** | comp_dur.mean() = 304.5 |
| **K25** | Task attempts per task_type | `{'Advertisement': 2203, 'App Tas...` | `{'Advertisement': 2203, 'App Tas...` | `0` | **PASS** | df_task['task_category'].value_counts() across 8 categories |
| **K26** | Users who completed ≥1 task | `981` | `981` | `0` | **PASS** | df_task[status=='Completed']['user_id'].nunique() = 981 |
| **K27** | Users who completed ≥5 tasks | `689` | `689` | `0` | **PASS** | (comp_tasks.groupby('user_id')['activity_id'].count() >= 5).sum() = 689 |
| **K28** | Total reward amount credited | `242830` | `242830` | `0` | **PASS** | df_miles['milestone_value'].sum() in 06_Milestones = 242830 |
| **K29** | Average reward per completed task | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | 05_Task_Activity cols: ['activity_id', 'user_id', 'task_id', 'task_category', 'task_viewed_at', 'task_started_at', 'task_completed_at', 'task_status', 'failure_reason', 'reward_status', 'device', 'session_id']; missing: reward_amount & Task_Master table |
| **K30** | Reward distribution by task_type | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | 05_Task_Activity lacks numeric reward_amount; Task_Master missing |
| **K31** | Reward distribution by feature | `{'Watch Ads': 22521, 'Streak Rew...` | `{'Watch Ads': 22521, 'Streak Rew...` | `0` | **PASS** | df_miles.groupby(mapped_feature)['milestone_value'].sum() across 16 features |
| **K32** | Reward reversals (count and %) | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Wallet_Ledger missing; 05_Task_Activity statuses: ['Failed', 'Abandoned', 'Completed', 'Pending'] (no Reversal) |
| **K33** | Users who have earned at least one reward | `1000` | `1000` | `0` | **PASS** | df_miles['user_id'].nunique() = 1000 |
| **K34** | D1 retention | `17.91` | `17.91` | `0.0` | **PASS** | 178 retained / 994 eligible = 17.91% |
| **K35** | D7 retention | `13.33` | `13.33` | `0.0` | **PASS** | 127 retained / 953 eligible = 13.33% |
| **K36** | D30 retention | `8.46` | `8.46` | `0.0` | **PASS** | 69 retained / 816 eligible = 8.46% |
| **K37** | Retention curve (D1..D30 timeseries) | `[{'day': 1, 'eligible_users': 99...` | `[{'day': 1, 'eligible_users': 99...` | `0` | **PASS** | D1..D30 retention curve matches 30 cohort evaluations |
| **K38** | Duplicate user_ids | `16` | `16` | `0` | **PASS** | len(df_messy[df_messy.duplicated('user_id', keep=False)]) = 16 rows (8 unique IDs duplicated) |
| **K39** | Rows with missing user_id | `0` | `0` | `0` | **PASS** | df_messy['user_id'].isna().sum() = 0 |
| **K40** | Rows with malformed or null timestamps | `2` | `2` | `0` | **PASS** | 1 null timestamp + 1 month-14 error in Users_Messy_Audit = 2 |
| **K41** | Invalid status values | `4` | `4` | `0` | **PASS** | len(df_dq_audit[event_status=='success ']) = 4 |
| **K42** | Orphan records (user_id not in users) | `0` | `0` | `0` | **PASS** | Orphan records across all activity tables = 0 |
| **K43** | Negative amounts | `4` | `4` | `0` | **PASS** | (df_clean['days_since_registration'] < 0).sum() = 4 |
| **K44** | Trailing-whitespace categorical values | `4` | `4` | `0` | **PASS** | len(df_dq_audit[event_status.str.endswith(' ')]) = 4 |
| **K45** | Wallet credits total | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Wallet_Ledger table missing from supplied workbooks |
| **K46** | Withdrawal completion rate | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Withdrawals table missing from supplied workbooks |
| **K47** | Withdrawal processing time (median) | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Withdrawals table missing from supplied workbooks |
| **K48** | Referral conversion rate | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Referral_Invites and Referral_Conversions tracking tables missing from workbooks |
| **K49** | Referral activations | `BLOCKED (null)` | `BLOCKED (null)` | `0` | **BLOCKED-CONFIRMED** | Referral_Activations tracking table missing from workbooks |

---

## Part 3 — Evidence Per KPI (Execution Log)

- **K01** [PASS]: df_u1['user_id'].nunique() = 1000  [reported: `1000`] → **PASS**
- **K02** [PASS]: u1_last_30.groupby('reg_date')['user_id'].count() over 30d (sum=184)  [reported: `dict(30 keys)`] → **PASS**
- **K03** [PASS]: len(df_u1[reg_date in last_7d]) = 47  [reported: `47`] → **PASS**
- **K04** [PASS]: df_events[ev_date in last_7d]['user_id'].nunique() = 486  [reported: `486`] → **PASS**
- **K05** [PASS]: df_events[ev_date in last_30d]['user_id'].nunique() = 812  [reported: `812`] → **PASS**
- **K06** [PASS]: df_daily[active_flag=='Yes'].groupby('act_date')['user_id'].nunique() (30d mean=103.50)  [reported: `dict(30 keys)`] → **PASS**
- **K07** [PASS]: mean(30d_DAU) / 30d_MAU = 103.50 / 812 = 0.1275  [reported: `0.1275`] → **PASS**
- **K08** [PASS]: COUNT(DISTINCT user_id in 02_Sessions) / 1000 * 100.0 = 984 / 1000 * 100.0 = 98.4  [reported: `98.4`] → **PASS**
- **K09** [PASS]: 1,000 registered users - 984 session users = 16  [reported: `16`] → **PASS**
- **K10** [PASS]: (df_daily[active_flag=='Yes'].groupby('user_id')['act_date'].nunique() >= 2).sum() = 826  [reported: `826`] → **PASS**
- **K11** [PASS]: len(set(01_Users_1000) - set(events_last_14d)) = 1000 - 654 = 346  [reported: `346`] → **PASS**
- **K12** [PASS]: len(df_sess) = 7913  [reported: `7913`] → **PASS**
- **K13** [PASS]: 7913 sessions / 1000 users = 7.913  [reported: `7.913`] → **PASS**
- **K14** [PASS]: df_sess['session_duration_seconds'].mean() = 51.81  [reported: `51.81`] → **PASS**
- **K15** [PASS]: df_events.groupby('feature_name')['user_id'].nunique() / 1000 * 100.0 across 15 features  [reported: `dict(15 keys)`] → **PASS**
- **K16** [PASS]: events / unique_users per feature in 03_Feature_Events across 15 features  [reported: `dict(15 keys)`] → **PASS**
- **K17** [PASS]: top 5 features: Watch Ads: 836, Daily Reward: 835, Streak Rewards: 832, CAPTCHA: 824, Referral: 811  [reported: `list(5 items)`] → **PASS**
- **K18** [PASS]: top 5 features: Watch Ads: 3126, Missions: 2780, Streak Rewards: 2734, CAPTCHA: 2733, Tap & Earn: 2654  [reported: `list(5 items)`] → **PASS**
- **K19** [PASS]: repeat_users(>=2 events) / unique_users per feature across 15 features  [reported: `dict(15 keys)`] → **PASS**
- **K20** [PASS]: len(df_task) = 9846  [reported: `9846`] → **PASS**
- **K21** [PASS]: len(df_task[task_status=='Completed']) = 5627  [reported: `5627`] → **PASS**
- **K22** [PASS]: len(df[status=='Completed']) / len(df) = 5627 / 9846 = 0.5715  [reported: `0.5715`] → **PASS**
- **K23** [PASS]: len(df[status=='Failed']) / len(df) = 1520 / 9846 = 0.1544  [reported: `0.1544`] → **PASS**
- **K24** [PASS]: comp_dur.mean() = 304.5  [reported: `304.5`] → **PASS**
- **K25** [PASS]: df_task['task_category'].value_counts() across 8 categories  [reported: `dict(8 keys)`] → **PASS**
- **K26** [PASS]: df_task[status=='Completed']['user_id'].nunique() = 981  [reported: `981`] → **PASS**
- **K27** [PASS]: (comp_tasks.groupby('user_id')['activity_id'].count() >= 5).sum() = 689  [reported: `689`] → **PASS**
- **K28** [PASS]: df_miles['milestone_value'].sum() in 06_Milestones = 242830  [reported: `242830`] → **PASS**
- **K29** [BLOCKED-CONFIRMED]: 05_Task_Activity cols: ['activity_id', 'user_id', 'task_id', 'task_category', 'task_viewed_at', 'task_started_at', 'task_completed_at', 'task_status', 'failure_reason', 'reward_status', 'device', 'session_id']; missing: reward_amount & Task_Master table  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K30** [BLOCKED-CONFIRMED]: 05_Task_Activity lacks numeric reward_amount; Task_Master missing  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K31** [PASS]: df_miles.groupby(mapped_feature)['milestone_value'].sum() across 16 features  [reported: `dict(16 keys)`] → **PASS**
- **K32** [BLOCKED-CONFIRMED]: Wallet_Ledger missing; 05_Task_Activity statuses: ['Failed', 'Abandoned', 'Completed', 'Pending'] (no Reversal)  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K33** [PASS]: df_miles['user_id'].nunique() = 1000  [reported: `1000`] → **PASS**
- **K34** [PASS]: 178 retained / 994 eligible = 17.91%  [reported: `17.91`] → **PASS**
- **K35** [PASS]: 127 retained / 953 eligible = 13.33%  [reported: `13.33`] → **PASS**
- **K36** [PASS]: 69 retained / 816 eligible = 8.46%  [reported: `8.46`] → **PASS**
- **K37** [PASS]: D1..D30 retention curve matches 30 cohort evaluations  [reported: `list(30 items)`] → **PASS**
- **K38** [PASS]: len(df_messy[df_messy.duplicated('user_id', keep=False)]) = 16 rows (8 unique IDs duplicated)  [reported: `16`] → **PASS**
- **K39** [PASS]: df_messy['user_id'].isna().sum() = 0  [reported: `0`] → **PASS**
- **K40** [PASS]: 1 null timestamp + 1 month-14 error in Users_Messy_Audit = 2  [reported: `2`] → **PASS**
- **K41** [PASS]: len(df_dq_audit[event_status=='success ']) = 4  [reported: `4`] → **PASS**
- **K42** [PASS]: Orphan records across all activity tables = 0  [reported: `0`] → **PASS**
- **K43** [PASS]: (df_clean['days_since_registration'] < 0).sum() = 4  [reported: `4`] → **PASS**
- **K44** [PASS]: len(df_dq_audit[event_status.str.endswith(' ')]) = 4  [reported: `4`] → **PASS**
- **K45** [BLOCKED-CONFIRMED]: Wallet_Ledger table missing from supplied workbooks  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K46** [BLOCKED-CONFIRMED]: Withdrawals table missing from supplied workbooks  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K47** [BLOCKED-CONFIRMED]: Withdrawals table missing from supplied workbooks  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K48** [BLOCKED-CONFIRMED]: Referral_Invites and Referral_Conversions tracking tables missing from workbooks  [reported: `None`] → **BLOCKED-CONFIRMED**
- **K49** [BLOCKED-CONFIRMED]: Referral_Activations tracking table missing from workbooks  [reported: `None`] → **BLOCKED-CONFIRMED**

---

## Part 4 — Hand-Calculated Spot Checks (Four Anchors)

These four spot checks provide verifiable anchors that any auditor can reproduce manually in Excel:

| KPI ID | KPI Name | Source Sheet & Column | Manual Arithmetic / Excel Formula | Expected | Reported | Verification |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **K01** | Total registered users | `01_Users_1000, Column A (user_id)` | `Filter Column A for unique values` | **1000** | **1000** | PASS (Exact Match) |
| **K08** | Users who have ever logged in | `02_Sessions, Column B (user_id)` | `Filter user_id for unique values in 02_Sessions` | **98.4** | **98.4** | PASS (Exact Match) |
| **K22** | Task completion rate | `05_Task_Activity, Column H (task_status)` | `=COUNTIF(status_column, 'Completed') / COUNTIF(status_column, 'started' or all rows)` | **0.5715** | **0.5715** | PASS (Exact Match) |
| **K38** | Duplicate user_ids | `Users_Messy_Audit, Column A (user_id)` | `8 distinct user_ids appear exactly 2 times each = 16 total rows participating in duplicates. K38 reports 'rows affected' = 16. Note: COUNTA(A:A) - COUNTUNIQUE(A:A) = 8 counts EXCESS rows, a different metric from K38's 'affected rows' count of 16.` | **16** | **16** | PASS (Exact Match) |

---

## Failures Requiring Attention

**None — all 49 KPIs passed independent validation or had their blocked dependencies confirmed.** Zero failures were detected.

---

## Reproducibility

To reproduce this validation report independently from the terminal:
```bash
python 13_analysis/validate_kpis.py
```

---

## Data Authenticity Statement
This report was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
