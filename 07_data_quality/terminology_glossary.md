# VELOOP Rewards — Data Quality Terminology Glossary

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.**

---

## 1. Overview and Purpose

Precision in data quality terminology is critical for separating observational findings, hard structural failures, underlying engineering bugs, statistical distributions, and unverified business assumptions. Inconsistent use of terms like "issue", "bug", or "anomaly" obscures root cause ownership, confuses engineering triage, and risks attributing data anomalies to external third parties without proof.

This glossary defines the five canonical data-quality terms governing all VELOOP analytics, engineering audits, and governance registers.

---

## 2. Core Terminology Matrix

| Term | Definition | When to use | When NOT to use | Examples in this project |
| :--- | :--- | :--- | :--- | :--- |
| **ISSUE** | A detected deviation from the expected rule or constraint. | Any data-quality finding that documents a deviation. | For a process failure that has a clear code root cause. | K38 duplicate `user_id`s, K40 malformed timestamps, K41 invalid status enum, K43 negative `days_since_registration`. |
| **DEFECT** | A repeatable bug in code or schema that systematically causes data issues. | When the root cause is a code or schema design problem. | For one-off client payload errors or manual entry mistakes. | A014 (event naming drift between tracking plan and backend), the synthetic generation gap in A009 (`last_login` null for Pending Verification users). |
| **ANOMALY** | A statistical outlier that MAY be legitimate — an unusual value, not necessarily a wrong one. | When a value is unusual but not a constraint violation. | For a hard constraint violation (missing required field, invalid enum, negative amount where positive required). | In this dataset, no true anomalies were identified. All deviations found were violations of constraints, not legitimate outliers. (The absence of anomalies is a finding in itself.) |
| **VIOLATION** | A record that fails a hard constraint (NOT NULL, UNIQUE, enum, range). The row must be rejected or quarantined. | When the record breaches a database or schema rule. | For soft-rule breaches or statistical outliers. | K38 duplicate `user_id`s (UNIQUE violation), K40 malformed timestamp (format violation), K41 invalid enum (enum violation), K43 negative `days_since_registration` (range violation). |
| **ASSUMPTION** | A statement about the system, backend, or third-party that is NOT verified from the supplied data. | Any belief about production behavior that cannot be computed from the two supplied workbooks. | As a fact in a findings document. Assumptions must be marked "To Be Verified" and logged in the assumption register. | A009 (72 Pending Verification users = synthetic generation gap, not production loss), A010 (Validation failed tasks — cause unknown), A011–A013 (schema deviations), A014 (event name drift). |

---

## 3. Detailed Term Explanations and Application Guidelines

### 3.1 Issue vs. Violation vs. Defect
- **Issue**: An umbrella observational classification. When an automated scan identifies a deviation, it begins as an issue.
- **Violation**: The formal operational categorization applied when an issue breaks a defined database constraint, schema rule, or data contract. A violation requires row-level rejection, quarantine (DLQ), or staging sanitization.
- **Defect**: The root-cause classification applied when the issue or violation is produced by a persistent software flaw, erroneous ETL transform, schema misconfiguration, or data generator bug.

### 3.2 The Analytical Significance of Anomaly Absence
In this benchmark dataset, extensive profiling across users, sessions, feature events, and task activity revealed multiple data quality violations (e.g. malformed ISO-8601 strings, negative elapsed days, unmapped status enums). However, **zero statistical anomalies** (legitimate extreme values such as an ultra-high session count or rare milestone threshold) were observed. The observed distribution extremes were entirely traceable to hard constraint violations or synthetic generation artifacts. Documenting the absence of anomalies confirms that data filtering must focus on structural constraint enforcement rather than statistical outlier trimming.

### 3.3 Assumption Governance
Any hypothesis or explanatory statement regarding system behavior, user intent, backend processing, or third-party partner reliability that cannot be mathematically proven from the supplied datasets (`01_raw_data/veloop_raw_data.xlsx` and `01_raw_data/veloop_tracking_data.xlsx`) constitutes an **Assumption**.
- Assumptions MUST NOT be stated as factual conclusions in analytical reports.
- All assumptions must carry the status `"To Be Verified"` and be logged in `01_governance/assumption_verification_register.xlsx` with an assigned verification owner and risk rating.
