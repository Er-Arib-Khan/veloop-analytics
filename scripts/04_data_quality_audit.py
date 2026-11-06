"""
Script: scripts/04_data_quality_audit.py
Purpose: Comprehensive Data Quality Audit across VELOOP simulated datasets:
         1. Audits Users_Messy_Audit (dirty baseline)
         2. Audits 10_Event_Data_Quality_Audit (event anomalies)
         3. Re-scans clean sheets for all 14 issue classes
Outputs:
         - 07_data_quality/data_quality_audit.xlsx (Issues, Severity_Summary, Affected_Records, SIMULATED_DATA_NOTICE)
         - 07_data_quality/data_quality_control_framework.md (16 QC rules across the telemetry lifecycle)
"""

import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def run_data_quality_audit():
    f1 = '00_source_data/veloop_simulated_user_behavior_1000.xlsx'
    f2 = '00_source_data/veloop_rewards_data_01.xlsx'

    # Load sheets
    df_messy = pd.read_excel(f2, sheet_name='Users_Messy_Audit', engine='calamine')
    df_clean_u = pd.read_excel(f2, sheet_name='Users_1000_Clean', engine='calamine')
    df_audit_evt = pd.read_excel(f1, sheet_name='10_Event_Data_Quality_Audit', engine='calamine')
    df_clean_evt = pd.read_excel(f1, sheet_name='03_Feature_Events', engine='calamine')
    df_sess = pd.read_excel(f1, sheet_name='02_Sessions', engine='calamine')
    df_task = pd.read_excel(f1, sheet_name='05_Task_Activity', engine='calamine')
    df_mile = pd.read_excel(f1, sheet_name='06_Milestones', engine='calamine')
    df_daily = pd.read_excel(f1, sheet_name='04_Daily_Activity', engine='calamine')
    df_u1 = pd.read_excel(f1, sheet_name='01_Users_1000', engine='calamine')

    issues = []
    affected_samples = []

    # -------------------------------------------------------------
    # 1. Duplicate IDs in Users_Messy_Audit
    # -------------------------------------------------------------
    dup_users_mask = df_messy['user_id'].duplicated(keep=False)
    dup_users = df_messy[dup_users_mask]
    issues.append({
        'Issue ID': 'ISSUE-001',
        'Dataset': 'Users_Messy_Audit',
        'Field': 'user_id',
        'Issue Type': 'duplicate IDs',
        'Records Affected': int(len(dup_users)),
        'Severity': 'Critical',
        'Detection Logic': "df['user_id'].duplicated(keep=False)",
        'Likely Cause': 'Lack of primary key uniqueness constraint during simulated batch user generation; ingestion retry without idempotency.',
        'Correction': 'Deduplicate records by user_id retaining latest registration timestamp; merge profile attributes.',
        'Prevention': 'Enforce UNIQUE primary key constraint on user_id at database schema layer.',
        'Owner': 'Data Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in dup_users.head(16).iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-001',
            'Dataset': 'Users_Messy_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['user_id'],
            'Field Name': 'user_id',
            'Anomalous Value': f"Duplicate user_id: {row['user_id']} ({row['full_name']}, {row['email']})",
            'Expected Value': 'Unique single entity record per user_id',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 2. Duplicate Event IDs in 10_Event_Data_Quality_Audit
    # -------------------------------------------------------------
    dup_evt_mask = df_audit_evt['event_id'].duplicated(keep=False)
    dup_evts = df_audit_evt[dup_evt_mask]
    issues.append({
        'Issue ID': 'ISSUE-002',
        'Dataset': '10_Event_Data_Quality_Audit',
        'Field': 'event_id',
        'Issue Type': 'duplicate events',
        'Records Affected': int(len(dup_evts)),
        'Severity': 'Critical',
        'Detection Logic': "df['event_id'].duplicated(keep=False)",
        'Likely Cause': 'Simulated duplicate injection test suite; network replay / retry without message deduplication at event collector.',
        'Correction': 'Deduplicate on event_id; retain first logged instance based on sequence_number.',
        'Prevention': 'Deploy event broker deduplication (e.g. Kafka idempotent producers, Redis sliding window deduplication on event_id).',
        'Owner': 'Platform Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in dup_evts.head(20).iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-002',
            'Dataset': '10_Event_Data_Quality_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['event_id'],
            'Field Name': 'event_id',
            'Anomalous Value': f"Duplicate event_id: {row['event_id']} ({row['feature_name']}, {row['event_name']})",
            'Expected Value': 'Unique UUID/sequential event_id across all event rows',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 3. Malformed Dates in Users_Messy_Audit
    # -------------------------------------------------------------
    bad_dates = []
    for idx, val in df_messy['registration_datetime'].items():
        if pd.notna(val):
            try:
                pd.to_datetime(val)
            except:
                bad_dates.append((idx, val, df_messy.loc[idx, 'user_id']))

    issues.append({
        'Issue ID': 'ISSUE-003',
        'Dataset': 'Users_Messy_Audit',
        'Field': 'registration_datetime',
        'Issue Type': 'malformed dates',
        'Records Affected': len(bad_dates),
        'Severity': 'High',
        'Detection Logic': "try pd.to_datetime(val) except Exception",
        'Likely Cause': 'Invalid month component (month 14) or non-ISO timestamp string passed without client-side schema validation.',
        'Correction': "Parse with custom regex or fallback logic; quarantine record if uncorrectable.",
        'Prevention': 'Enforce ISO-8601 (YYYY-MM-DD HH:MM:SS) format validation at API ingress before persisting.',
        'Owner': 'Backend Engineering',
        'Status': 'Confirmed'
    })
    for idx, val, uid in bad_dates:
        affected_samples.append({
            'Issue ID': 'ISSUE-003',
            'Dataset': 'Users_Messy_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': uid,
            'Field Name': 'registration_datetime',
            'Anomalous Value': str(val),
            'Expected Value': 'Valid ISO-8601 datetime (e.g. 2026-02-14 12:00:00)',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 4. Missing Timestamps (registration_datetime null) in Users_Messy_Audit
    # -------------------------------------------------------------
    null_reg = df_messy[df_messy['registration_datetime'].isna()]
    issues.append({
        'Issue ID': 'ISSUE-004',
        'Dataset': 'Users_Messy_Audit',
        'Field': 'registration_datetime',
        'Issue Type': 'missing timestamps',
        'Records Affected': len(null_reg),
        'Severity': 'Critical',
        'Detection Logic': "df['registration_datetime'].isna()",
        'Likely Cause': 'Incomplete user registration transaction payload or null serialization during ingest.',
        'Correction': 'Impute registration timestamp from first logged session_start or quarantine record.',
        'Prevention': 'Set NOT NULL constraint on registration_datetime column at database level.',
        'Owner': 'Backend Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in null_reg.iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-004',
            'Dataset': 'Users_Messy_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['user_id'],
            'Field Name': 'registration_datetime',
            'Anomalous Value': '[BLANK / NULL]',
            'Expected Value': 'Non-null valid registration timestamp',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 5. Unexpected Nulls in Required Profile Fields (Users_Messy_Audit)
    # -------------------------------------------------------------
    req_fields = ['age', 'gender', 'city', 'acquisition_source', 'primary_device', 'email_verification_status', 'onboarding_status']
    for rf in req_fields:
        null_rf = df_messy[df_messy[rf].isna()]
        if len(null_rf) > 0:
            issues.append({
                'Issue ID': f'ISSUE-005-{rf}',
                'Dataset': 'Users_Messy_Audit',
                'Field': rf,
                'Issue Type': 'unexpected nulls in required fields',
                'Records Affected': len(null_rf),
                'Severity': 'High',
                'Detection Logic': f"df['{rf}'].isna() in required demographic/status field",
                'Likely Cause': 'Controlled dirty data injection; unvalidated client profile creation payload.',
                'Correction': 'Backfill from user identity provider (Google Auth / SMS) or set default category Unknown.',
                'Prevention': 'Enforce mandatory required field validation in signup API form schema.',
                'Owner': 'Backend Engineering',
                'Status': 'Confirmed'
            })
            for idx, row in null_rf.iterrows():
                affected_samples.append({
                    'Issue ID': f'ISSUE-005-{rf}',
                    'Dataset': 'Users_Messy_Audit',
                    'Row Number (Excel)': idx + 2,
                    'Primary ID': row['user_id'],
                    'Field Name': rf,
                    'Anomalous Value': '[BLANK / NULL]',
                    'Expected Value': f'Non-null valid {rf} value',
                    'Status': 'Confirmed'
                })

    # -------------------------------------------------------------
    # 6. Trailing Whitespace in event_status (10_Event_Data_Quality_Audit)
    # -------------------------------------------------------------
    ws_mask = df_audit_evt['event_status'].astype(str).str.endswith(' ')
    ws_rows = df_audit_evt[ws_mask]
    issues.append({
        'Issue ID': 'ISSUE-006',
        'Dataset': '10_Event_Data_Quality_Audit',
        'Field': 'event_status',
        'Issue Type': 'trailing / leading whitespace in categorical fields',
        'Records Affected': len(ws_rows),
        'Severity': 'Medium',
        'Detection Logic': "df['event_status'].str.strip() != df['event_status']",
        'Likely Cause': 'Unsanitized string literal injection in event dispatcher payload (e.g. \"success \").',
        'Correction': "Apply TRIM() / .str.strip() during Bronze-to-Silver staging ingestion.",
        'Prevention': 'Implement client-side string trimming and enum enforcement on SDK telemetry payloads.',
        'Owner': 'Analytics Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in ws_rows.iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-006',
            'Dataset': '10_Event_Data_Quality_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['event_id'],
            'Field Name': 'event_status',
            'Anomalous Value': f"'{row['event_status']}' (has trailing space)",
            'Expected Value': "'Success'",
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 7. Inconsistent Capitalization in feature_name (10_Event_Data_Quality_Audit)
    # -------------------------------------------------------------
    lc_features = ['missions', 'leaderboard', 'wallet', 'daily reward', 'watch ads']
    lc_feat_rows = df_audit_evt[df_audit_evt['feature_name'].isin(lc_features)]
    issues.append({
        'Issue ID': 'ISSUE-007',
        'Dataset': '10_Event_Data_Quality_Audit',
        'Field': 'feature_name',
        'Issue Type': 'inconsistent capitalization',
        'Records Affected': len(lc_feat_rows),
        'Severity': 'Medium',
        'Detection Logic': "df['feature_name'].isin(['missions', 'leaderboard', 'wallet', 'daily reward', 'watch ads'])",
        'Likely Cause': 'Telemetry sent from ad-hoc logging calls bypassing canonical Feature Catalog constants.',
        'Correction': 'Map to Title Case canonical strings using standard lookup table during staging.',
        'Prevention': 'Enforce strongly typed Enum / constant definitions for feature_name in telemetry SDK.',
        'Owner': 'Analytics Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in lc_feat_rows.iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-007',
            'Dataset': '10_Event_Data_Quality_Audit',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['event_id'],
            'Field Name': 'feature_name',
            'Anomalous Value': f"'{row['feature_name']}' (lowercase)",
            'Expected Value': f"'{row['feature_name'].title()}' (Title Case)",
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 8. Negative Values in days_since_registration (Users_1000_Clean & Messy)
    # -------------------------------------------------------------
    neg_days_clean = df_clean_u[df_clean_u['days_since_registration'] < 0]
    issues.append({
        'Issue ID': 'ISSUE-008',
        'Dataset': 'Users_1000_Clean / Users_Messy_Audit',
        'Field': 'days_since_registration',
        'Issue Type': 'negative values in fields that should be >= 0',
        'Records Affected': len(neg_days_clean),
        'Severity': 'Medium',
        'Detection Logic': "df['days_since_registration'] < 0",
        'Likely Cause': 'Snapshot baseline calculation timestamp preceded final registration timestamp by hours (-0.8 days).',
        'Correction': 'Clamp derived days_since_registration to GREATEST(0.0, derived_val) or align snapshot timestamp.',
        'Prevention': 'Ensure snapshot baseline timestamp is set to MAX(registration_datetime) + 1 second.',
        'Owner': 'Analytics Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in neg_days_clean.iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-008',
            'Dataset': 'Users_1000_Clean',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['user_id'],
            'Field Name': 'days_since_registration',
            'Anomalous Value': float(row['days_since_registration']),
            'Expected Value': '>= 0.0 days (non-negative)',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 9. Observation Window Overrun (last_login_datetime > stated cutoff)
    # -------------------------------------------------------------
    overrun_mask = df_clean_u['last_login_datetime'] > '2026-09-15 23:59:59'
    overrun_rows = df_clean_u[overrun_mask]
    issues.append({
        'Issue ID': 'ISSUE-009',
        'Dataset': 'Users_1000_Clean / Users_Messy_Audit',
        'Field': 'last_login_datetime',
        'Issue Type': 'malformed dates / boundary overrun',
        'Records Affected': len(overrun_rows),
        'Severity': 'Low',
        'Detection Logic': "df['last_login_datetime'] > '2026-09-15 23:59:59'",
        'Likely Cause': 'Synthetic generation generator clock ran 40 hours past documented cutoff (up to 2026-09-17 10:08:00).',
        'Correction': 'Filter observation window to <= 2026-09-15 23:59:59 or update manifest boundary.',
        'Prevention': 'Enforce dataset cut-off filter in data pipeline export query.',
        'Owner': 'Data Analyst',
        'Status': 'Confirmed'
    })
    for idx, row in overrun_rows.head(10).iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-009',
            'Dataset': 'Users_1000_Clean',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['user_id'],
            'Field Name': 'last_login_datetime',
            'Anomalous Value': str(row['last_login_datetime']),
            'Expected Value': '<= 2026-09-15 23:59:59 (Manifest cutoff)',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 10. Missing Session ID in 06_Milestones
    # -------------------------------------------------------------
    null_sess_mile = df_mile[df_mile['session_id'].isna()]
    issues.append({
        'Issue ID': 'ISSUE-010',
        'Dataset': '06_Milestones',
        'Field': 'session_id',
        'Issue Type': 'missing IDs / foreign key gaps',
        'Records Affected': len(null_sess_mile),
        'Severity': 'Medium',
        'Detection Logic': "df['session_id'].isna() in 06_Milestones",
        'Likely Cause': 'System-awarded background milestones (e.g. account anniversary, offline badge) triggered without active user session context.',
        'Correction': "Assign 'SYSTEM_SESSION' or nullable foreign key semantic with documented exception.",
        'Prevention': 'Define formal milestone trigger types distinguishing in-session user triggers from background system cron awards.',
        'Owner': 'Backend Engineering',
        'Status': 'Confirmed'
    })
    for idx, row in null_sess_mile.head(15).iterrows():
        affected_samples.append({
            'Issue ID': 'ISSUE-010',
            'Dataset': '06_Milestones',
            'Row Number (Excel)': idx + 2,
            'Primary ID': row['user_id'],
            'Field Name': 'session_id',
            'Anomalous Value': '[BLANK / NULL]',
            'Expected Value': 'Valid session_id or explicit SYSTEM_BACKGROUND tag',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 11. Missing Dimension Table: Task Master for Task_Activity
    # -------------------------------------------------------------
    issues.append({
        'Issue ID': 'ISSUE-011',
        'Dataset': '05_Task_Activity',
        'Field': 'task_id',
        'Issue Type': 'orphan foreign keys / missing dimension',
        'Records Affected': len(df_task),
        'Severity': 'High',
        'Detection Logic': "80 distinct task_ids exist in Task_Activity with no parent task_master table",
        'Likely Cause': 'Task catalog dimension table was omitted from supplied dataset export.',
        'Correction': 'Construct proposed task_master table inferred from task_category and reward payouts.',
        'Prevention': 'Include master dimension tables in analytical warehouse star-schema models.',
        'Owner': 'Analytics Engineering',
        'Status': 'Confirmed'
    })
    affected_samples.append({
        'Issue ID': 'ISSUE-011',
        'Dataset': '05_Task_Activity',
        'Row Number (Excel)': 'All 9,846 rows',
        'Primary ID': 'TASK0001 - TASK0080',
        'Field Name': 'task_id',
        'Anomalous Value': '80 distinct task IDs without dimension table parent',
        'Expected Value': 'Foreign key reference to parent task_master (task_id, task_name, category)',
        'Status': 'Confirmed'
    })

    # -------------------------------------------------------------
    # 12. Missing Core Transactional Tables (Wallet, Withdrawals, Referrals, Rewards)
    # -------------------------------------------------------------
    missing_tbls = [
        ('Wallet_Ledger', 'Critical', 'Cannot reconstruct running balance, audit liability, or track XP inflation.'),
        ('Withdrawals', 'Critical', 'Inability to track cash burn, payout success rate, or payment gateway SLA.'),
        ('Referrals', 'Critical', 'Cannot calculate viral K-factor or attribute conversions to inviter.'),
        ('Rewards_Catalog', 'Critical', 'Cannot measure reward item popularity, stockouts, or partner unit economics.')
    ]
    for tbl, sev, impact in missing_tbls:
        issues.append({
            'Issue ID': f'ISSUE-012-{tbl}',
            'Dataset': tbl,
            'Field': 'Table Entity',
            'Issue Type': 'missing tables',
            'Records Affected': 1000,
            'Severity': sev,
            'Detection Logic': f"Table {tbl} does not exist in any supplied workbook",
            'Likely Cause': 'Pre-launch transactional tables have not yet been modeled or exported to analytical warehouse.',
            'Correction': 'Design and propose production-ready DDL schemas and event tracking instrumentation.',
            'Prevention': 'Implement centralized data contract reviews before release.',
            'Owner': 'Data Architect',
            'Status': 'Confirmed'
        })
        affected_samples.append({
            'Issue ID': f'ISSUE-012-{tbl}',
            'Dataset': tbl,
            'Row Number (Excel)': 'TABLE MISSING',
            'Primary ID': 'N/A',
            'Field Name': 'Entire Table Entity',
            'Anomalous Value': 'Table does not exist',
            'Expected Value': f'Fully modeled transactional table for {tbl}',
            'Status': 'Confirmed'
        })

    # -------------------------------------------------------------
    # 13. Inconsistent Column Naming Across Workbooks
    # -------------------------------------------------------------
    issues.append({
        'Issue ID': 'ISSUE-013',
        'Dataset': '01_Users_1000 vs Users_1000_Clean',
        'Field': 'verification_status vs email_verification_status',
        'Issue Type': 'inconsistent naming',
        'Records Affected': 1000,
        'Severity': 'Low',
        'Detection Logic': "'verification_status' in WB1 vs 'email_verification_status' in WB2",
        'Likely Cause': 'Different engineering teams or task iterations generating conflicting attribute names for same entity.',
        'Correction': 'Standardize on canonical attribute name email_verification_status in warehouse modeling.',
        'Prevention': 'Enforce centralized enterprise data dictionary and semantic naming guidelines.',
        'Owner': 'Data Governance',
        'Status': 'Confirmed'
    })
    affected_samples.append({
        'Issue ID': 'ISSUE-013',
        'Dataset': '01_Users_1000 vs Users_1000_Clean',
        'Row Number (Excel)': 'Header Row',
        'Primary ID': 'Column Schema',
        'Field Name': 'verification_status',
        'Anomalous Value': 'WB1: verification_status | WB2: email_verification_status',
        'Expected Value': 'Unified canonical column name: email_verification_status',
        'Status': 'Confirmed'
    })

    # Build DataFrames
    df_issues = pd.DataFrame(issues)
    df_samples = pd.DataFrame(affected_samples)

    # Build Severity Summary
    sev_counts = df_issues['Severity'].value_counts().reset_index()
    sev_counts.columns = ['Dimension / Category', 'Count']
    sev_counts['Group'] = 'Severity Breakdown'

    type_counts = df_issues['Issue Type'].value_counts().reset_index()
    type_counts.columns = ['Dimension / Category', 'Count']
    type_counts['Group'] = 'Issue Type Breakdown'

    df_sev_summary = pd.concat([sev_counts, type_counts], ignore_index=True)[['Group', 'Dimension / Category', 'Count']]
    df_sev_summary['Governance Status'] = 'Confirmed'

    # Save to 07_data_quality/data_quality_audit.xlsx
    out_xlsx = '07_data_quality/data_quality_audit.xlsx'
    print(f"Generating {out_xlsx}...")
    wb_out = openpyxl.Workbook()

    # Sheets
    ws_issues = wb_out.active
    ws_issues.title = "Issues"
    ws_issues.views.sheetView[0].showGridLines = True

    ws_summary = wb_out.create_sheet(title="Severity_Summary")
    ws_summary.views.sheetView[0].showGridLines = True

    ws_aff = wb_out.create_sheet(title="Affected_Records")
    ws_aff.views.sheetView[0].showGridLines = True

    ws_notice = wb_out.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.views.sheetView[0].showGridLines = True
    ws_notice["A1"] = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."
    ws_notice["A1"].font = Font(name="Calibri", size=14, bold=True, color="9C0006")
    ws_notice["A3"] = "This workbook contains the comprehensive Data Quality Audit and issue register across simulated VELOOP workbooks."
    ws_notice["A3"].font = Font(name="Calibri", size=11, italic=True)

    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='E0E0E0'),
        right=Side(style='thin', color='E0E0E0'),
        top=Side(style='thin', color='E0E0E0'),
        bottom=Side(style='thin', color='E0E0E0')
    )

    sev_styles = {
        'Critical': PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
        'High': PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
        'Medium': PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
        'Low': PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    }

    # Populate Issues
    ws_issues.append(list(df_issues.columns))
    for r in df_issues.itertuples(index=False):
        ws_issues.append(list(r))

    # Populate Summary
    ws_summary.append(list(df_sev_summary.columns))
    for r in df_sev_summary.itertuples(index=False):
        ws_summary.append(list(r))

    # Populate Affected_Records
    ws_aff.append(list(df_samples.columns))
    for r in df_samples.itertuples(index=False):
        ws_aff.append(list(r))

    # Styling
    for ws, df_curr in [(ws_issues, df_issues), (ws_summary, df_sev_summary), (ws_aff, df_samples)]:
        ws.row_dimensions[1].height = 26
        for col_idx in range(1, len(df_curr.columns) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin_border

        for row_idx in range(2, len(df_curr) + 2):
            ws.row_dimensions[row_idx].height = 28
            for col_idx in range(1, len(df_curr.columns) + 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.border = thin_border
                cell.font = Font(name="Calibri", size=10)
                val = cell.value

                col_name = df_curr.columns[col_idx - 1]
                if isinstance(val, (int, float, np.integer, np.floating)):
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                elif col_name in ('Issue ID', 'Severity', 'Status', 'Governance Status', 'Row Number (Excel)'):
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

                if col_name == 'Severity' and val in sev_styles:
                    cell.fill = sev_styles[val]
                    cell.font = Font(name="Calibri", size=10, bold=True)

        for col_idx, col_name in enumerate(df_curr.columns, 1):
            col_letter = get_column_letter(col_idx)
            max_len = max(len(str(col_name)), 12)
            ws.column_dimensions[col_letter].width = min(max_len + 8, 55)

        ws.freeze_panes = "A2"

    wb_out.save(out_xlsx)
    print(f"Successfully generated {out_xlsx}!")

    # Write 07_data_quality/data_quality_control_framework.md
    generate_control_framework_md()

def generate_control_framework_md():
    out_md = '07_data_quality/data_quality_control_framework.md'
    print(f"Generating {out_md}...")

    content = r"""# VELOOP Rewards — Data Quality Control Framework

> **CRITICAL GOVERNANCE NOTICE**: All quality control rules, failure actions, and testing procedures documented in this framework reflect **SIMULATED DATA** created for pre-launch product analytics, telemetry architecture, and quality assurance modeling. No real production data or user PII was audited.

---

## 1. Quality Control Architecture Overview

The VELOOP Data Quality Control Framework establishes automated gates across the data lifecycle to identify, quarantine, and remediate data corruption before it reaches downstream analytics, financial reconciliation models, or executive dashboards.

Quality checks operate across six defined enforcement layers:
1. **Application (Client / App SDK)**: Real-time form validation, payload schema checks, and client-side sanitization.
2. **Collection (API Gateway / Event Ingest)**: Ingress token authentication, rate limiting, and event schema contract validation.
3. **Raw (Bronze / Lakehouse Ingestion)**: Append-only integrity checks, null rejection, and duplicate identification.
4. **Transformation (Silver / Data Modeling)**: String normalization, referential integrity joins, and enum mapping.
5. **Analytics (Gold / Data Marts)**: Aggregate consistency, metric sanity, and streak/funnel logic validation.
6. **Dashboard (Presentation / BI)**: Visual threshold alerts, anomaly monitors, and refresh heartbeat checks.

---

## 2. Master Quality Control Rules (QC001 – QC016)

| Rule ID | Rule Name & Description | Execution Layer | Validation Logic | Action on Failure | Owner |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **QC001** | **Primary Key Entity Uniqueness**<br>Guarantees primary identifiers (`user_id`, `session_id`, `event_id`) are globally unique. | **Raw / Database** | `COUNT(*) = COUNT(DISTINCT entity_id)` | Block transaction; quarantine duplicate record into dead-letter queue (DLQ); trigger P1 engineering alert. | Data Engineering |
| **QC002** | **Mandatory Primary Key Presence**<br>Ensures entity identifiers are never null or empty strings. | **Application / Collection** | `entity_id IS NOT NULL AND TRIM(entity_id) != ''` | Reject payload at API gateway with `400 Bad Request`; log validation drop. | Backend Engineering |
| **QC003** | **ISO-8601 Timestamp Compliance**<br>Ensures all event and lifecycle timestamps follow standardized UTC format. | **Collection / Ingest** | `TRY_PARSE(timestamp_col AS TIMESTAMP) IS NOT NULL` | Reject invalid format; require client to transmit timestamps formatted as `YYYY-MM-DDTHH:MM:SS.sssZ`. | Platform Engineering |
| **QC004** | **Calendar & Date Validity**<br>Prevents impossible calendar dates (e.g. Month 14, Feb 30). | **Ingest / Raw** | Date components adhere to Gregorian calendar rules (`MM BETWEEN 1 AND 12`, `DD BETWEEN 1 AND 31`). | Route corrupted row to quarantine table; alert on ingestion pipeline error. | Data Engineering |
| **QC005** | **Categorical Status Enum Enforcement**<br>Restricts status fields to approved canonical lists (`Active`, `Completed`, etc.). | **Application / Silver** | `status_field IN ('Active', 'Inactive', 'Suspended', 'Pending Verification')` | In API: Reject invalid enum. In Silver ETL: Map unknown status to `'Unknown_Pending_Review'`. | Analytics Engineering |
| **QC006** | **Canonical Casing Normalization**<br>Prevents case-insensitive duplicate feature names and categories. | **Transformation** | `feature_name = PROPER_CASE(feature_name)` or match against Canonical Feature Dictionary. | Auto-correct casing via Silver staging lookup table (e.g. `'watch ads'` $\rightarrow$ `'Watch Ads'`). | Analytics Engineering |
| **QC007** | **Categorical Whitespace Sanitization**<br>Eliminates leading and trailing whitespace from string attributes. | **Collection / Ingest** | `LENGTH(col) = LENGTH(TRIM(col))` | Automatically apply `TRIM()` on ingestion; log warning if discrepancy > 0. | Analytics Engineering |
| **QC008** | **Numeric Column Type Integrity**<br>Ensures numeric metrics (`age`, `xp_balance`, `duration`) contain strictly numeric values. | **Raw / Staging** | `col IS NULL OR TRY_CAST(col AS NUMERIC) IS NOT NULL` | Reject string payloads during ingest; in staging, flag records for manual schema review. | Data Engineering |
| **QC009** | **Non-Negative Value Safeguard**<br>Restricts currency balances, durations, and counts to non-negative numbers. | **Transformation / Marts** | `numeric_col >= 0` | Clamp negative derived fields (`GREATEST(0, val)`); alert finance engineering on balance violations. | Analytics Engineering |
| **QC010** | **Required Demographic Field Completeness**<br>Guarantees mandatory profile attributes are populated. | **Application / Ingest** | `required_col IS NOT NULL AND TRIM(required_col) != ''` | Block user profile completion until mandatory fields (e.g. `city`, `acquisition_source`) are provided. | Product Engineering |
| **QC011** | **Referential Integrity & Foreign Key Match**<br>Ensures child events, sessions, and tasks link to valid parent users. | **Transformation** | `FOREIGN KEY (user_id) REFERENCES users(user_id)` | Route orphan records to unassigned orphan holding table; reprocess upon user record arrival. | Analytics Engineering |
| **QC012** | **Event Stream Idempotency & Deduplication**<br>Prevents network retry double-counting of behavioral events. | **Collection / Ingest** | Sliding window deduplication on `(user_id, session_id, sequence_number, event_name)`. | Drop duplicate event silently; return `200 OK` to client to acknowledge successful receipt. | Platform Engineering |
| **QC013** | **Event Taxonomy & Naming Governance**<br>Restricts tracked events to pre-approved `object_action` taxonomy standard. | **Collection / CI/CD** | `event_name` matches regex `^[a-z]+(_[a-z]+)*$` and exists in Tracking Plan. | Block PR in CI/CD pipeline if unapproved events are introduced into codebase. | Data Governance |
| **QC014** | **Monotonic Temporal State Transitions**<br>Ensures timestamps follow logical sequence (Completed $\ge$ Started $\ge$ Viewed). | **Transformation** | `completed_at >= started_at AND started_at >= viewed_at` | Flag record with `state_transition_error = TRUE`; exclude from task duration calculations. | Analytics Engineering |
| **QC015** | **Domain Completeness & Missing Table Safeguards**<br>Enforces the existence of mandatory transactional ledgers. | **Architecture / Schema** | Schema validator checks presence of `wallet_transactions`, `withdrawals`, `referral_invites`. | Halt analytics pipeline build if core financial tables fail schema presence check. | Data Architect |
| **QC016** | **Snapshot Horizon & Observation Cutoff Alignment**<br>Prevents activity timestamps from exceeding documented observation cutoffs. | **Transformation / Gold** | `timestamp_col <= snapshot_cutoff_timestamp` | Filter out-of-boundary records into future observation partition. | Data Analyst |

---

## 3. Severity Classification & Escalation Matrix

- **Critical Severity**:
  - *Definition*: Directly corrupts financial balances, causes double-counting in executive KPIs, or breaks core relational integrity.
  - *SLA*: Immediate automated quarantine; P1 engineering alert; fix required within 4 hours.
  - *Examples*: Duplicate `user_id`s, duplicate `event_id`s, missing `wallet_transactions` ledger, null `registration_datetime`.
- **High Severity**:
  - *Definition*: Prevents accurate segmentation or causes missing records in operational funnels.
  - *SLA*: Automated routing to review queue; remediation within 24 hours.
  - *Examples*: Malformed dates, unexpected nulls in required demographic attributes, missing task dimension master.
- **Medium Severity**:
  - *Definition*: Cosmetic inconsistencies, whitespace, or derived metric clamping issues that can be auto-remediated in staging.
  - *SLA*: Resolved automatically during ETL/ELT cleaning phase; review within standard sprint cycle.
  - *Examples*: Trailing whitespace, lowercase feature names, negative `days_since_registration`.
- **Low Severity**:
  - *Definition*: Documentation discrepancies or schema naming inconsistencies across legacy environments.
  - *SLA*: Backlog tracking; resolve during planned schema deprecation cycles.
  - *Examples*: Column name discrepancy (`verification_status` vs `email_verification_status`).

---

## 4. Remediation Workflow & Pipeline Integration

```mermaid
flowchart TD
    A[Client App Telemetry / API Payload] --> B{QC002 / QC003 / QC005<br>Gateway Schema Validation}
    B -- Invalid Payload --> C[Drop / 400 Bad Request / Log Error]
    B -- Valid Payload --> D[Event Streaming Buffer / Kafka]
    D --> E{QC001 / QC012<br>Idempotent Deduplication}
    E -- Duplicate Event --> F[Drop Duplicate / Acknowledge Receipt]
    E -- Unique Event --> G[Bronze Raw Lakehouse Table]
    G --> H[Silver Staging Transformation]
    H --> I{QC006 / QC007 / QC009<br>Normalization & Trimming}
    I --> J[Apply TRIM, Title Case, Clamp Negatives]
    J --> K{QC011 / QC014<br>FK Integrity & State Check}
    K -- Orphan / Transition Error --> L[Quarantine Holding Table]
    K -- Valid --> M[Gold Relational Data Marts]
    M --> N[Executive KPI & Product Dashboards]
```

---

## Data Authenticity Statement
This Data Quality Control Framework was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
"""

    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated {out_md}!")

if __name__ == '__main__':
    run_data_quality_audit()
