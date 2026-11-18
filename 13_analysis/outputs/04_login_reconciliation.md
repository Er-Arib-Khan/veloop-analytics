# Forensic Login & Session Count Reconciliation and Retention Verification

**Dataset Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Execution Date:** 2026-11-18  
**Scope:** Forensic reconciliation of user login/session metrics (K08, K09), root-cause analysis of the 928 vs. 984 discrepancy, and exact cohort retention verification (K34, K35, K36).

---

## Executive Summary

A forensic audit was performed across `00_source_data/veloop_simulated_user_behavior_1000.xlsx`, `00_source_data/veloop_rewards_data_01.xlsx`, and `13_analysis/outputs/02_kpis.json`. Every count reported below has been directly calculated and verified against raw data without estimation or heuristic rounding.

Key findings:
1. **The 928 vs. 984 Discrepancy is Fully Resolved:** The gap is a **cross-workbook data generation mismatch** between the behavioral telemetry workbook (`veloop_simulated_user_behavior_1000.xlsx`) and the standalone user demographic workbook (`veloop_rewards_data_01.xlsx`).
   - In `Users_1000_Clean`, `last_login_datetime` was synthetically set to `NULL` for all 72 users whose `account_status` is `"Pending Verification"`. However, in the behavioral transaction log (`02_Sessions`), **all 72 of these users actually logged in**, recording 560 completed sessions, 486 daily activity records, and 2,710 feature events.
   - Conversely, 16 users who recorded **zero sessions and zero activity** in the behavioral workbook were given synthetic login timestamps and fabricated session counts in `Users_1000_Clean`.
2. **Canonical Definition Established for K08 & K09:** Definition A (`distinct user_id in 02_Sessions`) is selected as canonical.
   - **K08 (Users who have ever logged in):** `98.4%` (984 users out of 1,000 registered).
   - **K09 (Users who have NEVER logged in):** `16 users` (1.6% of registered users).
   - Dual-number formats have been eliminated from `02_kpis.json`.
3. **Retention Math Verified to the Exact Basis Point (K34, K35, K36):**
   - **D1 Retention (K34):** 178 retained of 994 eligible users = **17.91%** (delta: `0.0000%`).
   - **D7 Retention (K35):** 127 retained of 953 eligible users = **13.33%** (delta: `0.0000%`).
   - **D30 Retention (K36):** 69 retained of 816 eligible users = **8.46%** (delta: `0.0000%`).

---

## Step 1 — Enumeration of Every Possible "Logged In" Definition

Each definition was executed on the source datasets. Below is the exact inventory:

| Definition | Description | Count | Source Sheet | Column | Filter Applied | Rows Excluded |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **Definition A** | Distinct users in session telemetry | **984** | `02_Sessions` (WB1) | `user_id` | `user_id IS NOT NULL` | 0 |
| **Definition B** | Distinct users in clean users registry with non-null login column | **0** | `01_Users_1000` (WB1) | None (column absent) | N/A (no login column exists in sheet) | 1,000 |
| **Definition C** | Distinct users in feature events matching login event names | **0** | `03_Feature_Events` (WB1) | `event_name` (`event_type` absent) | `event_type = 'login' OR event_name = 'user_logged_in'` | 35,704 |
| **Definition D** | Distinct users in rewards clean user table with non-null login timestamp | **928** | `Users_1000_Clean` (WB2) | `last_login_datetime` | `last_login_datetime IS NOT NULL` | 72 |
| **Definition E** | Distinct users in session telemetry within observation window | **984** | `02_Sessions` (WB1) | `session_start` | `session_start BETWEEN '2026-04-01' AND '2026-09-15 23:59:59'` | 0 |

### Detailed Technical Notes on Definitions:
- **Definition A (`02_Sessions`):** Contains 7,913 total session rows. All 7,913 rows have a populated `user_id`, mapping to exactly 984 distinct user IDs (`VLUSR000001` through `VLUSR001000`). Zero rows are excluded.
- **Definition B (`01_Users_1000`):** The primary user registry in Workbook 1 contains 16 columns: `user_id`, `full_name`, `email`, `age`, `gender`, `state`, `city`, `registration_datetime`, `acquisition_source`, `referral_source_detail`, `primary_device`, `platform`, `account_status`, `verification_status`, `onboarding_status`, and `referral_code`. There is **no column tracking login timestamp or login count** in this table. If surrogate columns are examined: `verification_status = 'Verified'` yields 851 users; `onboarding_status != 'Not Started'` yields 847 users; `account_status = 'Active'` yields 602 users. None of these represent a login definition.
- **Definition C (`03_Feature_Events`):** Contains 35,704 event records. There is no `event_type` column (columns are `event_id`, `user_id`, `session_id`, `event_datetime`, `feature_name`, `event_name`, `event_status`, `device`, `platform`, `acquisition_source`, `sequence_number`, `reward_related_flag`, `xp_related_flag`). Across all 35 distinct `event_name` values (e.g., `ad_started`, `mission_viewed`, `daily_reward_claimed`), there are zero authentication-level events (`login` or `user_logged_in`). The event stream only captures in-app feature interactions.
- **Definition D (`Users_1000_Clean`):** Contains 1,000 rows. The column `last_login_datetime` is non-null for 928 users and null for exactly 72 users.
- **Definition E (`02_Sessions` Windowed):** The observation window for the dataset spans 2026-04-01 through 2026-09-15. The earliest session start timestamp in `02_Sessions` is `2026-04-02 20:14:28` and the latest is `2026-09-15 22:13:22`. Because 100% of the 7,913 recorded sessions fall within the observation window, zero rows are excluded, resulting in the identical count of 984 distinct users. (Note: Restricting to the final 30 calendar days [≥ 2026-08-17] yields 818 distinct users across 4,001 sessions, excluding 3,912 rows; restricting to the final 7 calendar days [≥ 2026-09-09] yields 497 distinct users across 1,409 sessions, excluding 6,504 rows).

---

## Step 2 — Identification of 928 vs 984 & Forensic Gap Root Cause

### Summary Comparison Table

| Number | Which Definition Produced It | Which Sheet | Why It Differs |
| :---: | :--- | :--- | :--- |
| **928** | **Definition D** (`last_login_datetime IS NOT NULL`) | `Users_1000_Clean` (WB2) | Excludes 72 users whose `account_status` was set to `"Pending Verification"`, because the synthetic demographic generator assumed unverified accounts cannot have a login timestamp. |
| **984** | **Definition A / E** (`DISTINCT user_id`) | `02_Sessions` (WB1) | Measures actual client session telemetry; captures 912 verified users plus the 72 "unverified" users who actually generated sessions, but excludes 16 users who never initiated any session in the app. |

### The Root-Cause Explanation

The gap between 928 and 984 is **not an unexplainable anomaly**, but a **cross-workbook synthetic generation discrepancy and join artifact** between the standalone demographic table (`Users_1000_Clean` in `veloop_rewards_data_01.xlsx`) and the transactional event stream (`02_Sessions` in `veloop_simulated_user_behavior_1000.xlsx`). In `Users_1000_Clean`, the synthetic generator hardcoded `last_login_datetime = NULL` for all 72 accounts flagged as `account_status = 'Pending Verification'`, under the business assumption that unverified users cannot authenticate. However, the simulation script that created `02_Sessions` operated independently: it generated 560 completed sessions, 486 daily activity records, and 2,710 feature events for those exact same 72 users. Simultaneously, 16 users who recorded zero sessions and zero feature events in the behavioral logs were assigned synthetic `last_login_datetime` timestamps and artificial `lifetime_sessions` counts in `Users_1000_Clean`. Joining the two tables on `user_id` reveals that 912 users overlap, 72 users are active in sessions despite having null login timestamps in the clean user table, and 16 users have clean login timestamps despite having zero sessions in the transaction logs (912 + 72 = 984; 912 + 16 = 928; 912 + 72 + 16 = 1,000).

### Mathematical Partition of the 1,000 Registered Users

Performing an exact set intersection across `user_id` between `02_Sessions` and `Users_1000_Clean` partitions the 1,000 user base into four mutually exclusive quadrants:

```
                                  Users_1000_Clean: last_login_datetime
                                      NON-NULL              NULL
                            ┌─────────────────────────┬──────────────┐
  02_Sessions:   HAS        │     912 users           │   72 users   │  --> 984 users
  Session Rows   SESSIONS   │   (Both populated)      │ (Discrepancy)│
                            ├─────────────────────────┼──────────────┤
                 ZERO       │      16 users           │    0 users   │  -->  16 users
                 SESSIONS   │   (Discrepancy)         │ (Empty cell) │
                            └─────────────────────────┴──────────────┘
                                        │                     │
                                        v                     v
                                    928 users              72 users
```

1. **Quadrant 1 (912 users) — Fully Consistent Active Users:**  
   Users who have both recorded sessions in `02_Sessions` and a valid `last_login_datetime` in `Users_1000_Clean`.
2. **Quadrant 2 (72 users) — False Dormancy Artifact in Clean Table:**  
   Users who have `last_login_datetime IS NULL` in `Users_1000_Clean`, but are **provably active** in Workbook 1:
   - All 72 have `account_status = 'Pending Verification'` and `email_verification_status = 'Pending'`.
   - Total sessions recorded in `02_Sessions`: **560 completed sessions** (mean 7.78 sessions/user, range 1 to 29 sessions).
   - Total events in `03_Feature_Events`: **2,710 feature events** (all 72 users present).
   - Total records in `04_Daily_Activity`: **486 active user-days** (all 72 users present).
3. **Quadrant 3 (16 users) — True Day-0 Inactive Users:**  
   Users who have **zero sessions** in `02_Sessions`, but were incorrectly assigned a `last_login_datetime` and synthetic session counts in `Users_1000_Clean`:
   - Exact user IDs: `VLUSR000068`, `VLUSR000117`, `VLUSR000195`, `VLUSR000221`, `VLUSR000282`, `VLUSR000298`, `VLUSR000344`, `VLUSR000440`, `VLUSR000443`, `VLUSR000477`, `VLUSR000540`, `VLUSR000599`, `VLUSR000620`, `VLUSR000677`, `VLUSR000877`, `VLUSR000919`.
   - In `02_Sessions`: **0 sessions**.
   - In `03_Feature_Events`: **0 events**.
   - In `04_Daily_Activity`: **0 active days**.
   - In `05_Task_Activity`: **0 task attempts**.
4. **Quadrant 4 (0 users) — Zero Unaccounted Records:**  
   There are zero users who have both zero sessions and a null login timestamp.

---

## Step 3 — Canonical KPI Definitions for K08 & K09

### Chosen Canonical Definition
**Definition A (`distinct user_id in 02_Sessions`) is selected as canonical for users who have ever logged in.**

### One-Sentence Justification
Definition A (`distinct user_id in 02_Sessions`) is selected as canonical because session start timestamps represent ground-truth, immutable client activity telemetry in the product behavior logs, whereas `last_login_datetime` in `Users_1000_Clean` is a synthetic demographic attribute that erroneously nullified login timestamps for 72 active users solely due to unverified account status.

### Corrected KPI Values

| KPI ID | KPI Name | Previous Formatted Value | Canonical Single Value | Canonical Unit | Canonical Source Sheets | Canonical Computation Formula |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- |
| **K08** | Users who have ever logged in | `92.8 (928 users; 984 users / 98.4%)` | **98.4** | `% of registered` | `02_Sessions`, `01_Users_1000` | `COUNT(DISTINCT user_id) FROM 02_Sessions * 100.0 / COUNT(DISTINCT user_id) FROM 01_Users_1000 = 984 / 1000 = 98.4%` |
| **K09** | Users who have NEVER logged in | `72 (7.2% dormant; 16 users / 1.6%)` | **16** | `users` | `01_Users_1000`, `02_Sessions` | `1,000 registered users − 984 session-active users = 16 users (1.6% of registered)` |

Each KPI now possesses exactly one unambiguous number, one canonical source, and zero dual-parenthetical notations.

---

## Step 4 — Verification of Cohort Retention Calculations (K34, K35, K36)

Retention was audited using the standard cohort retention specification:
- $\text{eligible\_users} = \text{COUNT(DISTINCT } \text{user\_id with } \text{registration\_date} \le (\text{observation\_end} - N \text{ days)})$
- $\text{retained\_users} = \text{COUNT(DISTINCT } \text{user\_id in } \text{04\_Daily\_Activity with } \text{day\_diff} = N)$
- $\text{retention\_rate} = \frac{\text{retained\_users}}{\text{eligible\_users}} \times 100.0$

### Verification Parameters
- **Dataset Observation End Date (`observation_end`):** `2026-09-15` (maximum date in `04_Daily_Activity` and `01_Users_1000`).
- **Activity Table:** `04_Daily_Activity` (6,667 rows; 100% have `active_flag = 'Yes'`).
- **Registration Table:** `01_Users_1000` (1,000 distinct registered users).

### Detailed Results Table

| KPI ID | Retention Interval | Cutoff Registration Date ($\le$) | Eligible Users | Retained Users | Recomputed Rate (%) | Current `02_kpis.json` Value | Absolute Difference | Audit Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **K34** | **D1** (Day 1) | `2026-09-14` | **994** | **178** | **17.9074%** (17.91%) | `17.91` | `0.0000%` | **VERIFIED (Pass)** |
| **K35** | **D7** (Day 7) | `2026-09-08` | **953** | **127** | **13.3263%** (13.33%) | `13.33` | `0.0000%` | **VERIFIED (Pass)** |
| **K36** | **D30** (Day 30) | `2026-08-16` | **816** | **69** | **8.4559%** (8.46%) | `8.46` | `0.0000%` | **VERIFIED (Pass)** |

### Audit Finding:
- **K34 (D1):** Exactly 6 users registered on `2026-09-15` (the final observation day), leaving $1,000 - 6 = 994$ eligible users. 178 of these 994 users logged activity on Day 1. Rate = $178 / 994 = 17.9074\% \to 17.91\%$.
- **K35 (D7):** Exactly 47 users registered between `2026-09-09` and `2026-09-15`, leaving $1,000 - 47 = 953$ eligible users. 127 of these 953 users logged activity on Day 7. Rate = $127 / 953 = 13.3263\% \to 13.33\%$.
- **K36 (D30):** Exactly 184 users registered in the last 30 calendar days (`2026-08-17` to `2026-09-15`), leaving $1,000 - 184 = 816$ eligible users. 69 of these 816 users logged activity on Day 30. Rate = $69 / 816 = 8.4559\% \to 8.46\%$.
- **Flag Evaluation:** All recomputed rates match the stored values in `02_kpis.json` to the second decimal place (difference = `0.00%`, well below the `0.01%` threshold). No retention calculation is flagged for error.

---

## Step 5 — Updates to Artifacts

### 1. Updates to `13_analysis/outputs/02_kpis.json`
- **K08:**
  - `value`: Changed from `92.8` to `98.4`.
  - `computation_note`: Replaced dual-source text with `"COUNT(DISTINCT user_id) FROM 02_Sessions * 100.0 / COUNT(DISTINCT user_id) FROM 01_Users_1000 = 984 / 1000 = 98.4%"`.
  - `source_sheets`: Updated to `["02_Sessions", "01_Users_1000"]`.
- **K09:**
  - `value`: Changed from `72` to `16`.
  - `computation_note`: Replaced dual-source text with `"COUNT(DISTINCT user_id) FROM 01_Users_1000 WHERE user_id NOT IN (SELECT DISTINCT user_id FROM 02_Sessions) = 1000 - 984 = 16 users (1.6% of registered)"`.
  - `source_sheets`: Updated to `["01_Users_1000", "02_Sessions"]`.
- **K34, K35, K36:**
  - Standardized `computation_note` to explicitly state `retained_users ÷ eligible_users` without secondary whole-base parentheticals (`"(or ... of all 1,000 registered users)"`).

### 2. Updates to `13_analysis/analysis_findings.md`
- **Finding 1:**
  - Replaced: `"Out of 1,000 total registered users in 01_Users_1000 (K01), exactly 928 users (92.8%) logged in at least once (K08), while 72 users (7.2%) never logged in and remained dormant from day 0 in Users_1000_Clean (K09)."`
  - Updated to: `"Out of 1,000 total registered users in 01_Users_1000 (K01), exactly 984 users (98.4%) recorded at least one session in 02_Sessions (K08), while 16 users (1.6%) never logged in or initiated a session (K09)."`
  - Updated implication to explain that onboarding drop-off is 1.6% rather than 7.2%, and that the 72-user figure was an artifact of `Users_1000_Clean`'s synthetic generator.
- **Finding 13:**
  - Updated formatting to explicitly display the `eligible_users` denominator as requested: `D1 = 17.91% (178 of 994 eligible users, K34)`, `D7 = 13.33% (127 of 953 eligible users, K35)`, and `D30 = 8.46% (69 of 816 eligible users, K36)`.

---

## Governance & Assumption Register Verification Note

In accordance with project governance protocols, formal entries have been logged in `01_governance/assumption_verification_register.xlsx`:

### Registered Governance Assumptions

#### 1. Assumption A009 — Cross-Pipeline Synthetic Generation Discrepancy (Resolved)
- **ID:** `A009`
- **Statement / Unknown:** The 72 "Pending Verification" users with sessions and the 16 users with login timestamps but zero sessions are independent synthetic-generator artifacts, NOT a VELOOP production data-loss event.
- **Why It Matters:** `Users_1000_Clean` (demographic) and `02_Sessions` (behavioral) were generated by separate pipelines with no cross-validation. This confirms that true Day-0 onboarding drop-off before first session is 1.6% (16 users), not 7.2% (72 users), preventing misplaced engineering alarms over telemetry data loss.
- **Source Checked:** `00_source_data/veloop_simulated_user_behavior_1000.xlsx` (`02_Sessions`), `00_source_data/veloop_rewards_data_01.xlsx` (`Users_1000_Clean`), `13_analysis/outputs/04_login_reconciliation.md`
- **Risk:** `Low` (simulated-data artifact)
- **Verification Owner:** Data Engineering
- **Status:** `Confirmed as simulated generation issue`

#### 2. Assumption A010 — Provenance of Task "Validation failed" Failures (Active Blocker)
- **ID:** `A010`
- **Statement / Unknown:** "Validation failed" tasks (48.16%, 732 tasks in `05_Task_Activity`) originate from VELOOP's own rule engine OR a third-party callback OR client payload — the supplied data does not distinguish which.
- **Why It Matters:** Determines technical remediation owner and architecture. Blocks recommendation **R1** precision regarding whether the engineering fix requires internal rule engine refactoring, partner webhook retry handling, or client SDK payload validation.
- **Source Checked:** `00_source_data/veloop_simulated_user_behavior_1000.xlsx` (`05_Task_Activity`), `13_analysis/business_recommendations.md` (`R1`)
- **Risk:** `High` (determines remediation owner)
- **Verification Owner:** Engineering
- **Status:** `To Be Verified`
- **Impact / Dependency:** Blocks R1 recommendation precision

---

## Data Authenticity Statement
This report was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
