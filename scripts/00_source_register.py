"""
Script: scripts/00_source_register.py
Purpose: Build 01_governance/source_verification_register.xlsx from source READMEs.
"""

import os
from datetime import date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_source_register():
    today_str = date.today().isoformat()
    # Fixed date for consistency with project timeline if required, or today: 2026-11-05
    today_str = "2026-11-05"

    wb = openpyxl.Workbook()
    
    # 1. Sheet: Register (Primary Sheet)
    ws_reg = wb.active
    ws_reg.title = "Register"
    ws_reg.views.sheetView[0].showGridLines = True

    # 2. Sheet: SIMULATED_DATA_NOTICE (Governance Compliance)
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.views.sheetView[0].showGridLines = True
    ws_notice["A1"] = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."
    ws_notice["A1"].font = Font(name="Calibri", size=14, bold=True, color="9C0006")
    ws_notice["A3"] = "This workbook contains the Source Verification Register tracking claims, statements, and assumptions against supplied simulated data manifests."
    ws_notice["A3"].font = Font(name="Calibri", size=11, italic=True)

    # Columns: ID | Information | Source | Source Type | Date Checked | Status | Notes
    headers = [
        "ID",
        "Information",
        "Source",
        "Source Type",
        "Date Checked",
        "Status",
        "Notes"
    ]
    ws_reg.append(headers)

    records = [
        (
            "SVR-001",
            "Both datasets are simulated, fictional, and intended solely for analytical testing; they do not contain actual VELOOP users, sessions, events, or production analytics.",
            "README_status.txt, lines 3, 12; README_data_status.txt, lines 2, 5",
            "Simulated",
            today_str,
            "Confirmed",
            "Explicitly confirmed in both READMEs: 'SIMULATED / FICTIONAL / FOR ANALYTICAL WORK ONLY' and 'NO. This workbook does not contain actual VELOOP users, sessions, events or production analytics.'"
        ),
        (
            "SVR-002",
            "Workbooks represent standalone analytical deliverables ('Standalone Users dataset for Task 01' and 'Standalone behavioral dataset for a 22–25 day Data Analyst project'); relational linkage between workbooks is not explicitly defined.",
            "README_data_status.txt, line 1; README_status.txt, line 2",
            "Simulated",
            today_str,
            "To Be Verified",
            "Relationship between Task 01 Users and Task 02 Users (shared vs disjoint user_ids) is not stated in source manifests and must be verified empirically via testing scripts."
        ),
        (
            "SVR-003",
            "Data was programmatically generated with controlled behavioral distributions, timestamps, feature interactions, and task outcomes.",
            "README_status.txt, line 13",
            "Simulated",
            today_str,
            "Confirmed",
            "Explicitly confirmed in README_status.txt under synthetic data generation methodology."
        ),
        (
            "SVR-004",
            "Field definitions, requirements, and validation rules are documented across dedicated Data Dictionary sheets (e.g. user_id, registration_datetime, session_duration_seconds, event_name).",
            "VELOOP_Simulated_User_Behavior_1000.xlsx, tab 08_Data_Dictionary; VELoop_Rewards_Data_01.xlsx, tab Data_Dictionary",
            "Simulated",
            today_str,
            "Confirmed",
            "Confirmed via workbook metadata sheets. Business semantic definitions and domain mappings for production systems remain To Be Verified."
        ),
        (
            "SVR-005",
            "A dedicated audit sheet contains controlled data quality anomalies including missing values, malformed dates, and duplicate rows for validation testing.",
            "README_data_status.txt, line 6",
            "Simulated",
            today_str,
            "Confirmed",
            "Explicitly stated in README_data_status.txt ('Audit sheet: Contains controlled missing values, malformed dates and duplicates') referring to Users_Messy_Audit."
        ),
        (
            "SVR-006",
            "Dedicated relational tables for Wallet balances/ledgers, cash/voucher withdrawals, and referral attribution chains are absent from the supplied files.",
            "README_status.txt & README_data_status.txt (manifest omissions)",
            "Internal",
            today_str,
            "To Be Verified",
            "Not stated in source. Workbooks contain Users, Sessions, Events, Daily Activity, Tasks, and Milestones, but no dedicated tables for Wallet or Withdrawal transactions."
        ),
        (
            "SVR-007",
            "Timestamp standard, ISO-8601 formatting, timezone normalization (e.g. UTC vs IST +05:30), and event logging latency rules are not defined in the source manifests.",
            "README_status.txt & README_data_status.txt",
            "Internal",
            today_str,
            "To Be Verified",
            "Not stated in source. Analysis period is documented as '01 Apr 2026 – 15 Sep 2026', but explicit timezone offsets and clock synchronization standards are absent."
        ),
        (
            "SVR-008",
            "Economic valuation of rewards, currency unit exchange rates, minimum withdrawal thresholds, and conversion formulas for 'xp_balance' are not defined in the source files.",
            "README_status.txt & README_data_status.txt",
            "Internal",
            today_str,
            "To Be Verified",
            "Not stated in source. Data dictionary indicates 'xp_balance' as integer (>=0), but reward economics and withdrawal parameters are absent from source manifests."
        ),
        (
            "SVR-009",
            "Controlled status enum values (e.g. account_status, email_verification_status, onboarding_status, task_status) are listed in dictionary sheets but need production schema formalization.",
            "VELoop_Rewards_Data_01.xlsx, tab Data_Dictionary; VELOOP_Simulated_User_Behavior_1000.xlsx, tab 08_Data_Dictionary",
            "Simulated",
            today_str,
            "Proposed",
            "Simulated dictionaries define categorical subsets; formal canonical enum constraints for production data modeling are proposed."
        ),
        (
            "SVR-010",
            "Production telemetry pipelines, live event collection infrastructure, and production database deployment status are pre-launch and not currently in production.",
            "README_status.txt, line 12; README_data_status.txt, line 5",
            "Official",
            today_str,
            "To Be Verified",
            "Not stated in source. Manifests confirm workbooks do not contain production records; live telemetry implementation status is To Be Verified with engineering."
        ),
        (
            "SVR-011",
            "Target population comprises 1,000 simulated user profiles spanning an observation period from 01 April 2026 to 15 September 2026.",
            "README_status.txt, lines 4, 5; README_data_status.txt, lines 3, 4",
            "Simulated",
            today_str,
            "Confirmed",
            "Explicitly confirmed across both README files: exactly 1,000 clean user records observed between 01 Apr 2026 and 15 Sep 2026."
        ),
        (
            "SVR-012",
            "All analytical conclusions must use mandatory wording ('In the provided simulated dataset...' or 'Within the synthetic sample...') and must never report metrics as real VELOOP performance.",
            "README_status.txt, lines 14, 15; README_data_status.txt, line 7",
            "Official",
            today_str,
            "Confirmed",
            "Explicit citation rule documented in both manifests: results must never be presented as actual VELOOP metrics or production behavior."
        )
    ]

    for row in records:
        ws_reg.append(row)

    # Styling
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # Status fills
    status_styles = {
        "Confirmed": {
            "fill": PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="006100")
        },
        "Proposed": {
            "fill": PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="1F4E79")
        },
        "To Be Verified": {
            "fill": PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="9C6500")
        }
    }

    # Format Header Row
    for col_idx in range(1, len(headers) + 1):
        cell = ws_reg.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws_reg.row_dimensions[1].height = 28

    # Format Data Rows
    for row_idx in range(2, len(records) + 2):
        ws_reg.row_dimensions[row_idx].height = 42
        for col_idx in range(1, len(headers) + 1):
            cell = ws_reg.cell(row=row_idx, column=col_idx)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            
            # Alignments
            if col_idx in (1, 4, 5):  # ID, Source Type, Date Checked
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx == 6:  # Status
                cell.alignment = Alignment(horizontal="center", vertical="top")
                status_val = cell.value
                if status_val in status_styles:
                    cell.fill = status_styles[status_val]["fill"]
                    cell.font = status_styles[status_val]["font"]
            else:  # Information, Source, Notes
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # Set Column Widths
    col_widths = {
        1: 12,  # ID
        2: 45,  # Information
        3: 35,  # Source
        4: 16,  # Source Type
        5: 14,  # Date Checked
        6: 16,  # Status
        7: 45   # Notes
    }
    for col_idx, width in col_widths.items():
        ws_reg.column_dimensions[get_column_letter(col_idx)].width = width

    ws_reg.freeze_panes = "A2"

    output_path = "/home/rib/project/veloop-analytics/01_governance/source_verification_register.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path}")
    print(f"Total rows in Register: {len(records)} data rows ({len(records) + 1} total including header)")

if __name__ == "__main__":
    build_source_register()
