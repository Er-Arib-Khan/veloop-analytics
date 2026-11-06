# VELOOP Analytics Governance & Operating Rules

> **CRITICAL NOTICE**: VELOOP Rewards is a real pre-launch product. ALL supplied data is **SIMULATED** and must never be described or treated as real production data.

---

## 1. Core Data Integrity & Operating Rules

1. **Never Fabricate Production Data**: Never fabricate production data or company statistics.
2. **Mandatory Dataset Labeling**: Label every generated dataset `"SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"`.
3. **Fact & Field Classification**: Mark every fact/field as `Confirmed`, `Proposed`, or `To Be Verified`.
4. **Accurate Lifecycle State**: Never claim a proposed event or table already exists.
5. **PII & Credential Safeguards**: Never request or expose authentication credentials, API tokens, payment credentials, or Personally Identifiable Information (PII).
6. **Strict Provenance & Traceability**: Every conclusion must trace to a verified source, a defined dataset, or a documented assumption.
7. **Explicit Gap Documentation**: If data is missing, document the gap explicitly — do not invent values.
8. **Automated Spreadsheet Delivery**: Use `.xlsx` generation via Python + `openpyxl` for all spreadsheets.
9. **Standardized Artifact Formats**: Use `.md` for written reports, and `.dbml` + rendered `.png` for Entity-Relationship (ER) diagrams.
10. **Data Integrity & Mixing Constraints**: Prefer supplied simulated data. Never silently mix simulated with synthetic extras.

---

## 2. Implementation Specifications

### A. Spreadsheet Status Column
- Every spreadsheet must have a **`Status`** column on relevant tabs/catalogues.
- The values in this column are restricted strictly to:
  - `Confirmed`
  - `Proposed`
  - `To Be Verified`

### B. Simulated Dataset Notice Sheet
- Every generated simulated dataset must contain a dedicated first sheet named:  
  **`SIMULATED_DATA_NOTICE`**
- This sheet must prominently display the text:  
  > **"SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."**

### C. Markdown Data Authenticity Statement
- Every markdown report must conclude with a standardized section:
  ```markdown
  ---
  ## Data Authenticity Statement
  This report was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
  ```

### D. PII & Credential Restrictions
- Zero tolerance for authentication credentials, private keys, authorization tokens, API tokens, or raw payment details.
- User data must remain strictly anonymized or pseudo-randomized simulated entities.

---

## 3. Directory Structure & Deliverable Mapping

| Folder | Purpose & Scope |
| :--- | :--- |
| [`00_source_data/`](../00_source_data/) | Raw simulated datasets, input manifests, and source data status logs |
| [`01_governance/`](../01_governance/) | Rules, source registers, assumption registers, and integrity standards |
| [`02_product_audit/`](../02_product_audit/) | Product surface audit, data coverage matrix, and analytics gap analysis |
| [`03_specs/`](../03_specs/) | Analytics specifications (User, Wallet & Withdrawal, Referral, Reward) |
| [`04_events/`](../04_events/) | Event taxonomy, event naming standards, and tracking plan |
| [`05_data_model/`](../05_data_model/) | Relational data dictionary, DBML schema, and rendered ER diagrams |
| [`06_kpis/`](../06_kpis/) | Core KPI catalogue, calculation logic, and dimension definitions |
| [`07_data_quality/`](../07_data_quality/) | Data profiling summaries, data quality audit, and DQ control framework |
| [`08_dashboards/`](../08_dashboards/) | Dashboard blueprints, metric layouts, and UI wireframes |
| [`09_engineering/`](../09_engineering/) | Engineering handoff sheets and data pipeline architecture proposals |
| [`10_privacy_governance/`](../10_privacy_governance/) | Data privacy policies, consent management, and governance proposals |
| [`11_backlog/`](../11_backlog/) | Phased implementation backlog and engineering ticket mappings |
| [`12_final/`](../12_final/) | Executive summary and final consolidated analytics foundation report |
| [`scripts/`](../scripts/) | Python scripts for data profiling, validation, testing, and XLSX generation |
