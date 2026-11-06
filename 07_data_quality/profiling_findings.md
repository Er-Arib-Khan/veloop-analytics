# Data Profiling Findings & Source Workbook Audit

> **CRITICAL GOVERNANCE NOTICE**: All datasets audited and reported herein are **SIMULATED DATA** created solely for analytical modeling, schema design, and data quality testing. This workbook does not contain actual VELOOP users, sessions, events, or production records.

---

## 1. Executive Summary & Inventory Overview

A comprehensive, zero-imputation audit was performed across all 15 worksheets contained within the two primary source workbooks: `veloop_simulated_user_behavior_1000.xlsx` (10 sheets) and `veloop_rewards_data_01.xlsx` (5 sheets). Data was analyzed in its raw state without pre-cleaning to accurately record record counts, structural geometries, missing cell distributions, ID duplicate counts, and categorical distributions.

| Workbook | Sheet | Records | Columns | Primary ID | Unique IDs | Duplicate IDs | Blank IDs | Missing Cells (%) | Date Span |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `veloop_simulated_user_behavior_1000.xlsx` | **`01_Users_1000`** | 1,000 | 16 | `user_id` | 1000 | 0 | 0 | 846 (5.29%) | 2026-04-01 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`02_Sessions`** | 7,913 | 12 | `session_id` | 7913 | 0 | 0 | 466 (0.49%) | 2026-04-02 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`03_Feature_Events`** | 35,704 | 13 | `event_id` | 35704 | 0 | 0 | 0 (0.00%) | 2026-04-02 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`04_Daily_Activity`** | 6,667 | 17 | `user_id` | 984 | 5683 | 0 | 0 (0.00%) | 2026-04-02 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`05_Task_Activity`** | 9,846 | 12 | `activity_id` | 9846 | 0 | 0 | 10,494 (8.88%) | 2026-04-02 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`06_Milestones`** | 4,799 | 6 | `user_id` | 1000 | 3799 | 0 | 40 (0.14%) | 2026-04-02 to 2026-09-15 |
| `veloop_simulated_user_behavior_1000.xlsx` | **`07_Feature_Usage`** | 15 | 7 | `feature_name` | 15 | 0 | 0 | 0 (0.00%) | N/A to N/A |
| `veloop_simulated_user_behavior_1000.xlsx` | **`08_Data_Dictionary`** | 26 | 7 | `field_name` | 26 | 0 | 0 | 0 (0.00%) | N/A to N/A |
| `veloop_simulated_user_behavior_1000.xlsx` | **`09_README_Status`** | 15 | 2 | `Item` | 15 | 0 | 0 | 0 (0.00%) | N/A to N/A |
| `veloop_simulated_user_behavior_1000.xlsx` | **`10_Event_Data_Quality_Audit`** | 35,714 | 13 | `event_id` | 35704 | 10 | 0 | 0 (0.00%) | 2026-04-02 to 2026-09-15 |
| `veloop_rewards_data_01.xlsx` | **`Users_1000_Clean`** | 1,000 | 27 | `user_id` | 1000 | 0 | 0 | 953 (3.53%) | 2026-04-01 to 2026-09-17 |
| `veloop_rewards_data_01.xlsx` | **`Users_Messy_Audit`** | 1,008 | 28 | `user_id` | 1000 | 8 | 0 | 966 (3.42%) | 2026-04-01 to 2026-09-17 |
| `veloop_rewards_data_01.xlsx` | **`Data_Dictionary`** | 25 | 5 | `field_name` | 25 | 0 | 0 | 0 (0.00%) | N/A to N/A |
| `veloop_rewards_data_01.xlsx` | **`Synthetic_Summary`** | 8 | 2 | `Metric` | 8 | 0 | 0 | 0 (0.00%) | N/A to N/A |
| `veloop_rewards_data_01.xlsx` | **`README_Data_Status`** | 7 | 2 | `Item` | 7 | 0 | 0 | 0 (0.00%) | N/A to N/A |

---

## 2. Worksheet-by-Worksheet Analytical Summaries

### Sheet: `01_Users_1000` (`veloop_simulated_user_behavior_1000.xlsx`)

The `01_Users_1000` sheet contains exactly 1,000 clean user records across 16 demographic and lifecycle dimensions. The primary key `user_id` exhibits 100% uniqueness with zero duplicate or blank records. User registration timestamps range from 2026-04-01 02:00:41 to 2026-09-15 20:26:50. There are 846 missing cells (5.29% overall) confined entirely to `referral_source_detail` (846 nulls for non-referral acquisitions), providing a clean baseline for behavioral joins.

### Sheet: `02_Sessions` (`veloop_simulated_user_behavior_1000.xlsx`)

The `02_Sessions` sheet captures 7,913 simulated user session records across 12 session-level attributes. The primary key `session_id` is completely unique (7,913 unique IDs, 0 duplicates, 0 blanks) and maps back to 984 distinct active users. Session timestamps span from 2026-04-02 20:14:28 through 2026-09-15 22:14:12, with session durations averaging 303.4 seconds (median 294.0 seconds). There are 466 missing cells (0.49% overall) located exclusively in `exit_feature` (466 nulls where sessions terminated abruptly or without a logged exit feature).

### Sheet: `03_Feature_Events` (`veloop_simulated_user_behavior_1000.xlsx`)

The `03_Feature_Events` sheet represents the core behavioral event telemetry table containing 35,704 event records and 13 columns. The primary key `event_id` is perfectly unique (35,704 unique records, 0 duplicates, 0 blanks) covering interactions across 15 distinct product features. Event timestamps range from 2026-04-02 20:14:31 to 2026-09-15 22:13:50 across 984 distinct active users and 7,913 sessions. The sheet has zero missing values across all 464,152 cells (0.00% missing), providing complete event sequences without telemetry gaps.

### Sheet: `04_Daily_Activity` (`veloop_simulated_user_behavior_1000.xlsx`)

The `04_Daily_Activity` sheet provides 6,667 pre-aggregated user-day records across 17 engagement and feature-interaction columns. The grain is a composite key of (`user_id`, `activity_date`), representing 984 unique users across dates spanning 2026-04-02 to 2026-09-15. Metrics include daily session counts (mean 1.19, max 5), event counts (mean 5.36, max 24), and daily streak/reward flags. The table is 100% complete with 0 missing cells out of 113,339 total cells, serving as a reliable mart for daily retention and habituation analysis.

### Sheet: `05_Task_Activity` (`veloop_simulated_user_behavior_1000.xlsx`)

The `05_Task_Activity` sheet documents 9,846 simulated micro-task attempts across 12 task-funnel attributes. The primary key `activity_id` is 100% unique (9,846 distinct IDs), tracking task categories including Games (3,282), Surveys (3,284), and Advertisements (3,280). This sheet exhibits 10,494 missing cells (8.88% overall), reflecting expected lifecycle funnel exits: `task_completed_at` contains 4,219 nulls (42.85%) for incomplete, abandoned, or failed tasks, while `failure_reason` contains 6,275 nulls (63.73%) for successful tasks. Timestamps span from 2026-04-02 20:14:41 to 2026-09-15 21:59:48.

### Sheet: `06_Milestones` (`veloop_simulated_user_behavior_1000.xlsx`)

The `06_Milestones` sheet records 4,799 milestone achievement events across 6 attributes with an operational grain of (`user_id`, `milestone_type`, `milestone_datetime`). Exactly 1,000 unique users reached at least one milestone between 2026-04-02 08:18:00 and 2026-09-15 22:13:28 across 5 milestone types. There are 40 missing values (0.14% missingness), localized to `session_id` (40 nulls) where milestones were awarded outside an active session context. Milestone numeric values average 136.2 units (median 75.0 units).

### Sheet: `07_Feature_Usage` (`veloop_simulated_user_behavior_1000.xlsx`)

The `07_Feature_Usage` sheet is a 15-row reference summary table providing aggregated performance and adoption statistics across all 15 product features. The primary key `feature_name` is unique, cataloging metrics including unique user penetration, total events, sessions with feature, and average events per user. The data confirms 'Spin the Wheel' generated the highest event volume (4,409 events across 846 users), whereas 'Referrals' saw 1,733 events across 635 users. The sheet is 100% complete with zero missing cells across all 105 data points.

### Sheet: `08_Data_Dictionary` (`veloop_simulated_user_behavior_1000.xlsx`)

The `08_Data_Dictionary` sheet contains 26 rows defining field names, technical data types, requirements, validation rules, and analytical use cases for the Task 02 behavioral dataset. It establishes the schema contract for Users (5 fields documented), Sessions (6 fields), Events (6 fields), Daily Activity (3 fields), Tasks (4 fields), and Milestones (2 fields). All 182 cells are fully populated without blanks, providing the foundational dictionary for relational modeling.

### Sheet: `09_README_Status` (`veloop_simulated_user_behavior_1000.xlsx`)

The `09_README_Status` sheet provides a 15-row project manifest documenting dataset metadata, analysis periods, row counts, and governance constraints. It formally declares the dataset as 'SIMULATED / FICTIONAL / FOR ANALYTICAL WORK ONLY' and confirms the absence of actual VELOOP production telemetry. The sheet is 100% complete and serves as the primary governance verification source for the behavioral workbook.

### Sheet: `10_Event_Data_Quality_Audit` (`veloop_simulated_user_behavior_1000.xlsx`)

The `10_Event_Data_Quality_Audit` sheet contains 35,714 event records (10 more rows than `03_Feature_Events`) across 13 columns, explicitly designed as a quality test suite. Profiling confirms the injection of exactly 10 duplicate `event_id` rows (35,704 unique IDs vs 35,714 total rows) and casing inconsistencies in `feature_name` ('watch ads' in lowercase alongside 'Watch Ads') and trailing whitespace in `event_status` ('success '). All 464,282 cells are populated, confirming that data quality testing in this sheet focuses on entity uniqueness, whitespace, and categorization hygiene.

### Sheet: `Users_1000_Clean` (`veloop_rewards_data_01.xlsx`)

The `Users_1000_Clean` sheet in the Task 01 rewards workbook contains 1,000 clean user records across an expanded set of 27 attributes. The primary key `user_id` has 1,000 unique values with 0 duplicates and 0 blanks. The sheet contains 953 missing cells (3.53% overall), occurring exclusively in `referral_source_detail` (881 nulls for non-referral acquisitions) and `last_login_datetime` (72 nulls for dormant users who never logged in post-registration). Anomalies include a negative minimum for `days_since_registration` (-0.8 days, 8 users registering after the benchmark date) and `last_login_datetime` values extending to 2026-09-17 10:08:00.

### Sheet: `Users_Messy_Audit` (`veloop_rewards_data_01.xlsx`)

The `Users_Messy_Audit` sheet contains 1,008 user records across 28 columns, engineered as a dirty data audit suite. Profiling reveals exactly 8 duplicate user profiles on `user_id` (1,000 unique IDs across 1,008 rows), 966 missing cells (3.42%), and corrupted data types. Specifically, `registration_datetime` contains mixed object types (malformed date strings alongside native datetime stamps), `age` contains float values due to nulls, and duplicate users exhibit conflicting emails and timestamps, simulating real-world ingestion corruption.

### Sheet: `Data_Dictionary` (`veloop_rewards_data_01.xlsx`)

The `Data_Dictionary` sheet in the rewards workbook contains 25 rows cataloging technical definitions, types, requirements, and validation rules for the 27 user attributes. It specifies validation checks such as 'Unique; non-null' for `user_id`, '18+ in supplied dataset' for `age`, and 'Controlled source list' for `acquisition_source`. The sheet is 100% complete with 0 missing cells out of 125 cells.

### Sheet: `Synthetic_Summary` (`veloop_rewards_data_01.xlsx`)

The `Synthetic_Summary` sheet provides an 8-row control summary of key population benchmarks for the clean user dataset. It confirms benchmark targets: 1,000 total users, 78 active users (7-day), 325 active users (30-day), 855 verified emails, 722 completed onboardings, 339 Google sign-ins, 119 referral acquisitions, and 77 suspended accounts. All 16 cells are fully populated without missing values.

### Sheet: `README_Data_Status` (`veloop_rewards_data_01.xlsx`)

The `README_Data_Status` sheet is a 7-row administrative manifest affirming the synthetic status of the Task 01 workbook. It explicitly details the rows (1,000 clean, 1,008 audit), the active date window (01 Apr 2026 – 15 Sep 2026), and strict citation rules prohibiting presenting findings as real production data. There are zero missing values across all 14 cells.

---

## 3. Key Observations & Anomaly Register

A strict cross-sheet audit revealed several controlled anomalies, data corruptions, and structural patterns:

### A. Entity Duplication & ID Collisions
- **`Users_Messy_Audit` (8 duplicate user_ids)**: Exactly 8 user IDs appear twice (`VLUSR000001`, `VLUSR000002`, `VLUSR000003`, `VLUSR000004`, `VLUSR000005`, `VLUSR000006`, `VLUSR000007`, `VLUSR000008`), representing 16 total rows with conflicting timestamps, names, or email variations.
- **`10_Event_Data_Quality_Audit` (10 duplicate event_ids)**: Exactly 10 event IDs are repeated twice (`EVT00000001` through `EVT00000010`), creating 20 total records with identical or conflicting attributes.
- **Clean Sheets Integrity**: `01_Users_1000`, `Users_1000_Clean`, `02_Sessions`, `03_Feature_Events`, and `05_Task_Activity` maintain 100% strict primary ID uniqueness with 0 duplicate or blank IDs.

### B. Missing Value Distributions & Funnel Drop-Offs
- **`05_Task_Activity` (10,494 null cells, 8.88%)**: Structural missingness directly mirrors the task completion lifecycle:
  - `task_completed_at`: 4,219 nulls (42.85%) corresponding to Abandoned (1,494), Failed (1,348), and other incomplete task attempts.
  - `failure_reason`: 6,275 nulls (63.73%) corresponding to Completed tasks that did not experience failure.
- **`01_Users_1000` (846 null cells, 5.29%)**:
  - `referral_source_detail`: 846 nulls (84.60%) because only 154 users were acquired via referral channels in this sample.
- **`02_Sessions` (466 null cells, 0.49%)**:
  - `exit_feature`: 466 nulls (5.89%) where sessions terminated abruptly without logging an exit feature.
- **`Users_1000_Clean` (953 null cells, 3.53%)**:
  - `referral_source_detail`: 881 nulls (88.10%) because only 119 users were acquired via referral in this workbook.
  - `last_login_datetime`: 72 nulls (7.20%) corresponding to registered users who never logged in after signup.
- **`06_Milestones` (40 null cells, 0.14%)**:
  - `session_id`: 40 nulls (0.83%) where milestones were credited outside of an active user session.

### C. Temporal Anomalies & Boundary Discrepancies
- **Negative `days_since_registration`**: In `Users_1000_Clean` and `Users_Messy_Audit`, 8 users have negative `days_since_registration` down to `-0.8` days, caused by registration timestamps occurring on 2026-09-15 after the snapshot calculation baseline.
- **Date Horizon Overrun**: While both README manifests state an analysis period ending on `15 Sep 2026`, `last_login_datetime` contains records through `2026-09-17 10:08:00` (e.g. `VLUSR000142`, `VLUSR000305`), exceeding the stated observation window by ~40 hours.
- **Malformed String Timestamps**: In `Users_Messy_Audit`, `registration_datetime` contains corrupt string entries (e.g. invalid date formats and unparseable strings) mixed with valid datetime objects, forcing pandas to treat the series as `object`.

### D. Categorical Inconsistencies & Casing Collisions
- **`10_Event_Data_Quality_Audit` Trailing Whitespace**: `event_status` contains `'success '` (with trailing space) in addition to `'Success'`, creating dual category buckets if unstripped.
- **`10_Event_Data_Quality_Audit` Lowercase Casing**: `feature_name` contains `'watch ads'` (lowercase) alongside `'Watch Ads'`.
- **Clean Baseline Consistency**: In `03_Feature_Events`, all 15 feature names and 5 event statuses are cleanly standardized without whitespace or casing issues.

---

## 4. Cross-Workbook Linkage & Feasibility Check

1. **Shared User Universe**: Cross-matching `user_id` between `01_Users_1000` (Workbook 1) and `Users_1000_Clean` (Workbook 2) demonstrates an exact 1:1 match across all 1,000 user IDs (`VLUSR000001` to `VLUSR001000`).
2. **Active User Representation**: In Workbook 1, 984 distinct users recorded at least one session, event, or daily activity record, while 16 registered users exhibit zero downstream behavioral events (consistent with early churn/dormancy).
3. **Missing Telemetry Domains**: Neither workbook contains dedicated transaction tables for **Wallet Ledgers** (balance credits/debits) or **Withdrawal Disbursements** (cash/UPI/voucher transfers). These tables must be architected as proposed models for the production analytics framework.

---

## Data Authenticity Statement
This profiling report was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
