#!/usr/bin/env python3
"""
scripts/10_build_dashboards.py
Builds:
1. 08_dashboards/dashboard_blueprint.xlsx (Sheet 'Visuals', 'Coverage_By_Dashboard', 'SIMULATED_DATA_NOTICE')
2. 08_dashboards/wireframes/*.svg (7 complete vector wireframes adhering to all rules)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# =====================================================================
# PART 1: 08_dashboards/dashboard_blueprint.xlsx
# =====================================================================

def build_blueprint_spreadsheet():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Visuals
    # ----------------------------------------------------
    ws = wb.active
    ws.title = "Visuals"
    
    headers = [
        "Dashboard",
        "Visual ID",
        "Visual Type",
        "Metric / KPI ID",
        "Calculation",
        "Source",
        "Filters",
        "Dimensions",
        "Date Range",
        "Refresh Frequency",
        "Business Question",
        "Decision Supported",
        "Status"
    ]
    
    visuals_data = [
        # --- 1. Executive Overview ---
        (
            "Executive Overview", "VIS-EXEC-01", "KPI Card", "KPI-ENG-01",
            "COUNT(DISTINCT user_id) WHERE active_flag = 'Yes'",
            "04_Daily_Activity", "Platform, Country", "None", "Yesterday (T-1)", "Daily",
            "How many unique members actively engaged with the platform yesterday?",
            "Evaluate immediate health and platform daily engagement baseline.", "Confirmed calculable"
        ),
        (
            "Executive Overview", "VIS-EXEC-02", "KPI Card", "KPI-RWD-01",
            "100.0 * COUNT(status = 'Completed') / COUNT(*)",
            "05_Task_Activity", "Platform, Task Category", "None", "Trailing 7 Days", "Daily",
            "What proportion of earning micro-tasks are successfully completed?",
            "Identify operational bottlenecks and advertiser inventory delivery.", "Confirmed calculable"
        ),
        (
            "Executive Overview", "VIS-EXEC-03", "KPI Card", "KPI-WAL-01",
            "SUM(xp_balance)",
            "Users_1000_Clean", "Account Status", "None", "Current Snapshot", "Daily",
            "What is the total outstanding virtual point liability owed to users?",
            "Determine platform balance sheet exposure and reserve requirements.", "To Be Verified"
        ),
        (
            "Executive Overview", "VIS-EXEC-04", "KPI Card", "KPI-WDL-01",
            "100.0 * COUNT(payout_status = 'Completed') / COUNT(*)",
            "Withdrawals (er_diagram.dbml)", "Payout Method, Gateway", "None", "Trailing 30 Days", "Daily",
            "What percentage of cash withdrawal requests settle without error?",
            "Evaluate banking rail stability. Blocked by missing Withdrawals table (Gap GAP-002).", "Blocked"
        ),
        (
            "Executive Overview", "VIS-EXEC-05", "Timeseries Line", "KPI-ENG-01",
            "COUNT(DISTINCT user_id) GROUP BY activity_date",
            "04_Daily_Activity", "Active Flag = 'Yes'", "activity_date", "Trailing 30 Days", "Daily",
            "Is daily active user engagement growing, stable, or decaying over time?",
            "Calibrate marketing spend and re-engagement push notification cadence.", "Confirmed calculable"
        ),

        # --- 2. User Analytics ---
        (
            "User Analytics", "VIS-USR-01", "KPI Card", "KPI-USR-01",
            "COUNT(DISTINCT user_id)",
            "Users_1000_Clean", "Country, Primary Device", "None", "All Time", "Daily",
            "What is the total cumulative registered user base of VELOOP?",
            "Measures gross top-of-funnel customer acquisition scale.", "Confirmed calculable"
        ),
        (
            "User Analytics", "VIS-USR-02", "KPI Card", "KPI-USR-02",
            "100.0 * COUNT(email_verification_status = 'Verified') / COUNT(*)",
            "Users_1000_Clean", "Acquisition Source", "None", "All Time", "Daily",
            "What percentage of registered users verified their email identity?",
            "Validate user authenticity and gate high-value earning opportunities.", "Confirmed calculable"
        ),
        (
            "User Analytics", "VIS-USR-03", "KPI Card", "KPI-USR-03",
            "100.0 * COUNT(onboarding_status = 'Completed') / COUNT(*)",
            "Users_1000_Clean", "Primary Device, Platform", "None", "All Time", "Daily",
            "What proportion of new users successfully complete the tutorial onboarding?",
            "Optimize introductory wizard steps and reduce activation friction.", "Confirmed calculable"
        ),
        (
            "User Analytics", "VIS-USR-04", "Donut Chart", "KPI-USR-04",
            "100.0 * COUNT(account_status = 'Suspended') / COUNT(*)",
            "Users_1000_Clean", "Acquisition Source", "acquisition_source", "All Time", "Weekly",
            "What proportion of registered accounts have been suspended for fraud or policy violations?",
            "Reallocate marketing budget away from high-suspension acquisition channels.", "Confirmed calculable"
        ),
        (
            "User Analytics", "VIS-USR-05", "Horizontal Bar", "KPI-USR-05",
            "100.0 * COUNT(days_since_last_login > 30) / COUNT(*)",
            "Users_1000_Clean", "Country = 'India'", "state", "All Time", "Weekly",
            "What proportion of registered users have remained inactive for greater than 30 days?",
            "Target automated push notification re-engagement campaigns to dormant user cohorts.", "Confirmed calculable"
        ),

        # --- 3. Engagement ---
        (
            "Engagement", "VIS-ENG-01", "KPI Card", "KPI-ENG-02",
            "AVG(session_duration_seconds) WHERE session_status = 'Completed'",
            "02_Sessions", "Device, Platform", "None", "Trailing 7 Days", "Daily",
            "What is the average dwell time of a completed user session?",
            "Assess user attention span and calibrate rewarded ad duration pacing.", "Confirmed calculable"
        ),
        (
            "Engagement", "VIS-ENG-02", "KPI Card", "KPI-ENG-05",
            "100.0 * COUNT(milestone_type = 'seventh_active_day') / 1000.0",
            "06_Milestones", "None", "None", "All Time", "Weekly",
            "What percentage of members achieve 7-day streak retention?",
            "Evaluate gamification habituation mechanics and early retention stickiness.", "Confirmed calculable"
        ),
        (
            "Engagement", "VIS-ENG-03", "KPI Card", "KPI-ENG-06",
            "AVG(Daily DAU) / MAU_Count * 100.0",
            "04_Daily_Activity / Users_1000_Clean", "Platform", "None", "Trailing 30 Days", "Monthly",
            "How frequently do monthly active users return to VELOOP on a daily basis?",
            "Benchmark product stickiness against industry consumer standards.", "Confirmed calculable"
        ),
        (
            "Engagement", "VIS-ENG-04", "Horizontal Bar", "KPI-ENG-04",
            "unique_users per feature_name ORDER BY unique_users DESC",
            "07_Feature_Usage", "None", "feature_name", "All Time", "Weekly",
            "Which of the 15 platform feature surfaces have the highest user penetration?",
            "Identify underperforming modules requiring home screen redesign or XP boosts.", "Confirmed calculable"
        ),
        (
            "Engagement", "VIS-ENG-05", "Column Chart", "KPI-ENG-03",
            "COUNT(session_id) / NULLIF(COUNT(DISTINCT user_id), 0)",
            "02_Sessions", "Device", "Hour of Day (0-23)", "Trailing 30 Days", "Weekly",
            "How many sessions does an active user generate on average per day?",
            "Measure daily session frequency depth across mobile and web platforms.", "Confirmed calculable"
        ),

        # --- 4. Rewards ---
        (
            "Rewards", "VIS-RWD-01", "KPI Card", "KPI-RWD-01",
            "100.0 * COUNT(task_status = 'Completed') / COUNT(*)",
            "05_Task_Activity", "Device, Task Category", "None", "Trailing 7 Days", "Daily",
            "What percentage of initiated earning tasks are completed successfully?",
            "Ensure advertiser campaign fulfillment and publisher payout viability.", "Confirmed calculable"
        ),
        (
            "Rewards", "VIS-RWD-02", "KPI Card", "KPI-RWD-02",
            "100.0 * COUNT(task_status = 'Failed') / COUNT(*)",
            "05_Task_Activity", "Device, Task Category", "None", "Trailing 7 Days", "Daily",
            "What percentage of task attempts end in technical failure or error?",
            "Trigger automated engineering alerts when provider failure rates spike.", "Confirmed calculable"
        ),
        (
            "Rewards", "VIS-RWD-03", "KPI Card", "KPI-RWD-05",
            "100.0 * SUM(reversal_amount) / SUM(credit_amount)",
            # DEPRECATED TABLE — Wallet_Transactions is superseded by ledger_entries.
            # See 03_specs/wallet_ledger_spec.md §5 for migration.
            # Retained for historical reference only. Do not add new reads/writes.
            "Wallet_Transactions (er_diagram.dbml)", "Feature", "None", "Trailing 30 Days", "Weekly",
            "What percentage of credited points are clawed back due to fraud/chargebacks?",
            "Contain sybil bot farming and advertiser billing disputes (Blocked - Gap GAP-001/GAP-007).", "Blocked"
        ),
        (
            "Rewards", "VIS-RWD-04", "Stacked Bar", "KPI-RWD-01",
            "COUNT(activity_id) GROUP BY task_category, task_status",
            "05_Task_Activity", "Device", "task_category, task_status", "All Time", "Daily",
            "How do task completion, failure, and abandonment vary across earning categories?",
            "Deprioritize broken offer categories and optimize rewarded video placement.", "Confirmed calculable"
        ),
        (
            "Rewards", "VIS-RWD-05", "Donut Chart", "KPI-RWD-03",
            "COUNT(activity_id) GROUP BY failure_reason WHERE task_status != 'Completed'",
            "05_Task_Activity", "Task Category", "failure_reason", "All Time", "Weekly",
            "What are the dominant root causes driving non-completion of tasks?",
            "Address client network drops, video timeout bugs, and survey screening friction.", "Confirmed calculable"
        ),

        # --- 5. Wallet ---
        (
            "Wallet", "VIS-WAL-01", "KPI Card", "KPI-WAL-01",
            "SUM(xp_balance)",
            "Users_1000_Clean", "Account Status", "None", "Current Snapshot", "Daily",
            "What is the total aggregate spendable XP liability across all user wallets?",
            "Ensure company cash reserves adequately cover potential user redemptions.", "To Be Verified"
        ),
        (
            "Wallet", "VIS-WAL-02", "KPI Card", "KPI-WAL-04",
            "AVG(xp_balance) WHERE account_status = 'Active'",
            "Users_1000_Clean", "None", "None", "Current Snapshot", "Daily",
            "What is the average points balance held by an active platform member?",
            "Calibrate minimum cash-out thresholds so average users can redeem in reasonable time.", "Confirmed calculable"
        ),
        (
            "Wallet", "VIS-WAL-03", "KPI Card", "KPI-WAL-02",
            "SUM(Credits) / NULLIF(SUM(Debits), 0)",
            # DEPRECATED TABLE — Wallet_Transactions is superseded by ledger_entries.
            # See 03_specs/wallet_ledger_spec.md §5 for migration.
            # Retained for historical reference only. Do not add new reads/writes.
            "Wallet_Transactions (er_diagram.dbml)", "Unit", "None", "Trailing 30 Days", "Monthly",
            "What is the ratio of points earned (issued) to points redeemed (burned)?",
            "Maintain virtual currency stability and prevent points hyper-inflation (Blocked - Gap GAP-001).", "Blocked"
        ),
        (
            "Wallet", "VIS-WAL-04", "Bar Chart", "KPI-WAL-03",
            "100.0 * COUNT(DISTINCT user_id WHERE visited_wallet = 'Yes') / COUNT(DISTINCT user_id)",
            "03_Feature_Events", "Device", "platform", "Trailing 30 Days", "Weekly",
            "What percentage of active members navigate to the wallet balance screen?",
            "Gauge user awareness of earned point balances and redemption readiness.", "Confirmed calculable"
        ),
        (
            "Wallet", "VIS-WAL-05", "Stacked Area", "KPI-WAL-01",
            "Running SUM(credits - debits) OVER (ORDER BY date)",
            # DEPRECATED TABLE — Wallet_Transactions is superseded by ledger_entries.
            # See 03_specs/wallet_ledger_spec.md §5 for migration.
            # Retained for historical reference only. Do not add new reads/writes.
            "Wallet_Transactions (er_diagram.dbml)", "Feature", "Date", "Trailing 90 Days", "Daily",
            "How has the cumulative virtual currency liability evolved over time?",
            "Forecast working capital requirements (Blocked by missing ledger table - Gap GAP-001).", "Blocked"
        ),

        # --- 6. Withdrawals ---
        (
            "Withdrawals", "VIS-WDL-01", "KPI Card", "KPI-WDL-01",
            "100.0 * COUNT(payout_status = 'Completed') / COUNT(*)",
            "Withdrawals (er_diagram.dbml)", "Payout Method", "None", "Trailing 30 Days", "Daily",
            "What percentage of cash withdrawal requests successfully settle into bank accounts?",
            "Monitor payout rail reliability and banking partner SLAs (Blocked - Gap GAP-002).", "Blocked"
        ),
        (
            "Withdrawals", "VIS-WDL-02", "KPI Card", "KPI-WDL-02",
            "SUM(amount_inr)",
            "Withdrawals (er_diagram.dbml)", "Gateway Name", "None", "Trailing 30 Days", "Monthly",
            "What is the total fiat cash volume (INR) disbursed to users this month?",
            "Monitor platform cash burn and operational disbursement liquidity (Blocked - Gap GAP-002).", "Blocked"
        ),
        (
            "Withdrawals", "VIS-WDL-03", "KPI Card", "KPI-WDL-03",
            "AVG(completed_at - requested_datetime)",
            "Withdrawals (er_diagram.dbml)", "Payout Method", "None", "Trailing 30 Days", "Daily",
            "What is the average turnaround time from user cash-out request to bank deposit?",
            "Enforce the platform's promised 24-hour payout turnaround SLA (Blocked - Gap GAP-002).", "Blocked"
        ),
        (
            "Withdrawals", "VIS-WDL-04", "Donut Chart", "KPI-WDL-04",
            "100.0 * COUNT(payout_status = 'Rejected') / COUNT(*)",
            "Withdrawals (er_diagram.dbml)", "Payout Method", "payout_method", "Trailing 30 Days", "Weekly",
            "What proportion of cash redemption requests are rejected by banking rails or fraud checks?",
            "Diagnose invalid UPI VPA formats and banking rail return codes (Blocked - Gap GAP-002).", "Blocked"
        ),
        (
            "Withdrawals", "VIS-WDL-05", "Funnel Chart", "KPI-WDL-05",
            "SUM(amount_inr) WHERE payout_status IN ('Requested', 'Processing')",
            "Withdrawals (er_diagram.dbml)", "None", "payout_status", "Trailing 30 Days", "Daily",
            "What is the total pending cash liability currently held in disbursement escrow?",
            "Forecast liquidity requirements for daily settlement clearing (Blocked - Gap GAP-002).", "Blocked"
        ),

        # --- 7. Referrals ---
        (
            "Referrals", "VIS-REF-01", "KPI Card", "KPI-REF-01",
            "100.0 * COUNT(acquisition_source = 'Referral') / COUNT(*)",
            "Users_1000_Clean", "Platform", "None", "All Time", "Weekly",
            "What percentage of platform signups originated from viral peer invitations?",
            "Quantify word-of-mouth organic growth contribution and viral coefficient.", "Confirmed calculable"
        ),
        (
            "Referrals", "VIS-REF-02", "KPI Card", "KPI-REF-02",
            "100.0 * COUNT(referral_activity = 'Yes') / COUNT(active_flag = 'Yes')",
            "04_Daily_Activity", "None", "None", "Trailing 7 Days", "Daily",
            "What percentage of active daily users generate an outbound invitation link?",
            "Measure viral sharing propensity and evaluate referral incentive banners.", "Confirmed calculable"
        ),
        (
            "Referrals", "VIS-REF-03", "KPI Card", "KPI-REF-03",
            "100.0 * COUNT(referral_status = 'Converted') / COUNT(referral_id)",
            "Referrals (er_diagram.dbml)", "Share Channel", "None", "Trailing 30 Days", "Monthly",
            "What percentage of shared invites convert into qualified earners (>= 100 XP)?",
            "Validate unit economics and prevent fraudulent bounty disbursements.", "Proposed"
        ),
        (
            "Referrals", "VIS-REF-04", "Funnel Bar", "KPI-REF-04",
            "100.0 * (COUNT(referral_status = 'Registered') - COUNT(referral_status = 'Converted')) / NULLIF(COUNT(referral_status = 'Registered'), 0)",
            "Referrals (er_diagram.dbml)", "Share Channel", "referral_status", "All Time", "Weekly",
            "What proportion of referred signups drop off before reaching the 100 XP earning threshold?",
            "Diagnose referee onboarding friction and optimize initial earning hurdles (Blocked - Gap GAP-003).", "Blocked"
        ),
        (
            "Referrals", "VIS-REF-05", "Donut Chart", "KPI-REF-01",
            "COUNT(user_id) GROUP BY referral_source_detail WHERE acquisition_source = 'Referral'",
            "Users_1000_Clean", "None", "referral_source_detail", "All Time", "Weekly",
            "Which viral distribution sub-channels drive the highest volume of referees?",
            "Prioritize deep-link SDK optimization for WhatsApp and Telegram sharing.", "Confirmed calculable"
        )
    ]
    
    ws.append(headers)
    for row in visuals_data:
        ws.append(list(row))
        
    # Styling Sheet 1
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for row_idx in range(2, len(visuals_data) + 2):
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            if col_idx in (1, 2, 3, 4, 8, 9, 10, 13):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in (5, 6, 7):
                cell.alignment = Alignment(horizontal="left", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                
            # Status highlighting
            if col_idx == 13:
                val = str(cell.value)
                if val == "Confirmed calculable":
                    cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="375623")
                elif val == "Proposed":
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="7F6000")
                elif val == "To Be Verified":
                    cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C65911")
                elif val == "Blocked":
                    cell.fill = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C00000")

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    
    col_widths = {
        "A": 22, # Dashboard
        "B": 14, # Visual ID
        "C": 18, # Visual Type
        "D": 16, # Metric / KPI ID
        "E": 40, # Calculation
        "F": 32, # Source
        "G": 24, # Filters
        "H": 22, # Dimensions
        "I": 18, # Date Range
        "J": 18, # Refresh Frequency
        "K": 42, # Business Question
        "L": 42, # Decision Supported
        "M": 22  # Status
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # ----------------------------------------------------
    # Sheet 2: Coverage_By_Dashboard
    # ----------------------------------------------------
    ws_cov = wb.create_sheet(title="Coverage_By_Dashboard")
    
    notes_text = (
        "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Definitions marked "
        "'Blocked' indicate visuals dependent on missing transactional tables (Gaps GAP-001, GAP-002, GAP-003)."
    )
    ws_cov.merge_cells("A1:G2")
    cell_notes = ws_cov["A1"]
    cell_notes.value = notes_text
    cell_notes.font = Font(name="Calibri", size=11, bold=True, color="C00000")
    cell_notes.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell_notes.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

    for row in range(1, 3):
        for col in range(1, 8):
            ws_cov.cell(row=row, column=col).border = border_thin

    dash_stats = {}
    for item in visuals_data:
        dash = item[0]
        status = item[12]
        if dash not in dash_stats:
            dash_stats[dash] = {"Confirmed calculable": 0, "Proposed": 0, "To Be Verified": 0, "Blocked": 0, "Total": 0}
        dash_stats[dash][status] += 1
        dash_stats[dash]["Total"] += 1

    cov_headers = ["Dashboard Name", "Confirmed Calculable", "Proposed", "To Be Verified", "Blocked", "Total Visuals", "% Confirmed"]
    start_row = 4
    for col_idx, h in enumerate(cov_headers, start=1):
        cell = ws_cov.cell(row=start_row, column=col_idx)
        cell.value = h
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    curr_row = start_row + 1
    t_conf = t_prop = t_tbv = t_block = t_all = 0

    for dash, stats in dash_stats.items():
        pct = (stats["Confirmed calculable"] / stats["Total"]) * 100.0
        ws_cov.cell(row=curr_row, column=1, value=dash).alignment = Alignment(horizontal="left")
        ws_cov.cell(row=curr_row, column=2, value=stats["Confirmed calculable"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=3, value=stats["Proposed"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=4, value=stats["To Be Verified"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=5, value=stats["Blocked"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=6, value=stats["Total"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=7, value=f"{pct:.1f}%").alignment = Alignment(horizontal="center")

        for c in range(1, 8):
            cell = ws_cov.cell(row=curr_row, column=c)
            cell.font = data_font
            cell.border = border_thin

        t_conf += stats["Confirmed calculable"]
        t_prop += stats["Proposed"]
        t_tbv += stats["To Be Verified"]
        t_block += stats["Blocked"]
        t_all += stats["Total"]
        curr_row += 1

    # Total row
    t_pct = (t_conf / t_all) * 100.0
    ws_cov.cell(row=curr_row, column=1, value="TOTAL ALL DASHBOARDS")
    ws_cov.cell(row=curr_row, column=2, value=t_conf)
    ws_cov.cell(row=curr_row, column=3, value=t_prop)
    ws_cov.cell(row=curr_row, column=4, value=t_tbv)
    ws_cov.cell(row=curr_row, column=5, value=t_block)
    ws_cov.cell(row=curr_row, column=6, value=t_all)
    ws_cov.cell(row=curr_row, column=7, value=f"{t_pct:.1f}%")

    total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    for c in range(1, 8):
        cell = ws_cov.cell(row=curr_row, column=c)
        cell.font = Font(name="Calibri", size=11, bold=True)
        cell.fill = total_fill
        cell.border = border_thin
        if c == 1:
            cell.alignment = Alignment(horizontal="left")
        else:
            cell.alignment = Alignment(horizontal="center")

    ws_cov.column_dimensions["A"].width = 24
    ws_cov.column_dimensions["B"].width = 22
    ws_cov.column_dimensions["C"].width = 16
    ws_cov.column_dimensions["D"].width = 18
    ws_cov.column_dimensions["E"].width = 16
    ws_cov.column_dimensions["F"].width = 16
    ws_cov.column_dimensions["G"].width = 18

    # ----------------------------------------------------
    # Sheet 3: SIMULATED_DATA_NOTICE
    # ----------------------------------------------------
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    notice_text = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."
    ws_notice["A1"] = notice_text
    ws_notice["A1"].font = Font(name="Calibri", size=14, bold=True, color="C00000")
    ws_notice["A3"] = "Governance Compliance Notice:"
    ws_notice["A3"].font = Font(name="Calibri", size=11, bold=True)
    ws_notice["A4"] = (
        "All visual specifications and metric dependencies in this blueprint derive from simulated testing data. "
        "Visuals marked 'Blocked' indicate missing underlying transactional tables in the source data export."
    )
    ws_notice["A4"].font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 85

    output_path = "08_dashboards/dashboard_blueprint.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path} with {len(visuals_data)} visual specifications.")

# =====================================================================
# PART 2: 08_dashboards/wireframes/*.svg
# =====================================================================

def generate_svg_wireframe(filename, title, kpis, charts, filters, data_source, blocked_callout=None):
    """
    Renders a clean, high-resolution SVG dashboard wireframe (1200x800).
    """
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">')
    svg.append('  <defs>')
    svg.append('    <style>')
    svg.append('      .bg { fill: #F8FAFC; }')
    svg.append('      .header-bg { fill: #0F172A; }')
    svg.append('      .title { font-family: "Segoe UI", Arial, sans-serif; font-size: 20px; font-weight: bold; fill: #FFFFFF; }')
    svg.append('      .subtitle { font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; fill: #94A3B8; }')
    svg.append('      .panel-bg { fill: #FFFFFF; stroke: #E2E8F0; stroke-width: 1.5; rx: 6px; }')
    svg.append('      .card-title { font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; font-weight: 600; fill: #64748B; }')
    svg.append('      .card-val { font-family: "Segoe UI", Arial, sans-serif; font-size: 22px; font-weight: bold; fill: #0F172A; }')
    svg.append('      .card-sub { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; fill: #10B981; }')
    svg.append('      .card-sub-neg { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; fill: #EF4444; }')
    svg.append('      .chart-title { font-family: "Segoe UI", Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #1E293B; }')
    svg.append('      .chart-desc { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; fill: #64748B; }')
    svg.append('      .filter-label { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; font-weight: 600; fill: #475569; }')
    svg.append('      .filter-val { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; fill: #0F172A; }')
    svg.append('      .footer-txt { font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; fill: #64748B; }')
    svg.append('      .notice-txt { font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #DC2626; }')
    svg.append('      .alert-box { fill: #FEF2F2; stroke: #EF4444; stroke-width: 1.5; stroke-dasharray: 4,4; rx: 6px; }')
    svg.append('      .alert-txt { font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #B91C1C; }')
    svg.append('    </style>')
    svg.append('  </defs>')
    
    # Background
    svg.append('  <rect width="1200" height="800" class="bg" />')
    
    # Top Header Banner
    svg.append('  <rect width="1200" height="60" class="header-bg" />')
    svg.append(f'  <text x="30" y="32" class="title">VELOP Rewards — {title}</text>')
    svg.append('  <text x="30" y="50" class="subtitle">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</text>')
    
    # Filter Panel Bar (y: 72 to 110)
    svg.append('  <rect x="30" y="72" width="1140" height="38" class="panel-bg" />')
    svg.append('  <text x="45" y="96" class="filter-label">GLOBAL FILTERS:</text>')
    
    fx = 150
    for flt, val in filters:
        svg.append(f'  <rect x="{fx}" y="79" width="150" height="24" rx="4" fill="#F1F5F9" stroke="#CBD5E1" />')
        svg.append(f'  <text x="{fx+8}" y="95" class="filter-val">{flt}: <tspan font-weight="bold">{val}</tspan></text>')
        fx += 165
        
    svg.append(f'  <rect x="{fx}" y="79" width="100" height="24" rx="4" fill="#2563EB" />')
    svg.append(f'  <text x="{fx+25}" y="95" font-family="Segoe UI" font-size="10" font-weight="bold" fill="#FFFFFF">Apply Filters</text>')

    # Blocked Callout Alert Box (if applicable)
    content_start_y = 122
    if blocked_callout:
        svg.append(f'  <rect x="30" y="120" width="1140" height="34" class="alert-box" />')
        svg.append(f'  <text x="50" y="142" class="alert-txt">⚠️ {blocked_callout}</text>')
        content_start_y = 164

    # KPI Cards Row (3-4 cards)
    card_y = content_start_y
    card_h = 75
    card_w = (1140 - (len(kpis) - 1) * 20) / len(kpis)
    
    for idx, (label, val, sub, is_pos) in enumerate(kpis):
        cx = 30 + idx * (card_w + 20)
        svg.append(f'  <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" class="panel-bg" />')
        svg.append(f'  <text x="{cx+15}" y="{card_y+22}" class="card-title">{label}</text>')
        svg.append(f'  <text x="{cx+15}" y="{card_y+50}" class="card-val">{val}</text>')
        sub_cls = "card-sub" if is_pos else "card-sub-neg"
        svg.append(f'  <text x="{cx+15}" y="{card_y+66}" class="{sub_cls}">{sub}</text>')

    # Charts Grid (2-3 blocks)
    chart_y = card_y + card_h + 16
    remaining_h = 740 - chart_y
    
    if len(charts) == 2:
        cw = 560
        for idx, (ctitle, cdesc, ctype) in enumerate(charts):
            cx = 30 + idx * 580
            svg.append(f'  <rect x="{cx}" y="{chart_y}" width="{cw}" height="{remaining_h}" class="panel-bg" />')
            svg.append(f'  <text x="{cx+20}" y="{chart_y+28}" class="chart-title">{ctitle}</text>')
            svg.append(f'  <text x="{cx+20}" y="{chart_y+46}" class="chart-desc">{cdesc}</text>')
            # Chart wireframe placeholder graphic
            svg.append(f'  <rect x="{cx+20}" y="{chart_y+60}" width="{cw-40}" height="{remaining_h-80}" fill="#F8FAFC" stroke="#E2E8F0" rx="4" />')
            svg.append(f'  <text x="{cx+cw/2}" y="{chart_y+remaining_h/2+10}" font-family="Segoe UI" font-size="13" font-weight="600" fill="#94A3B8" text-anchor="middle">[{ctype} Placeholder: {ctitle}]</text>')
    elif len(charts) == 3:
        # 1 wide chart left, 2 stacked right
        w_left = 680
        w_right = 440
        h_right = (remaining_h - 16) / 2
        
        # Left Chart
        c1_title, c1_desc, c1_type = charts[0]
        svg.append(f'  <rect x="30" y="{chart_y}" width="{w_left}" height="{remaining_h}" class="panel-bg" />')
        svg.append(f'  <text x="50" y="{chart_y+28}" class="chart-title">{c1_title}</text>')
        svg.append(f'  <text x="50" y="{chart_y+46}" class="chart-desc">{c1_desc}</text>')
        svg.append(f'  <rect x="50" y="{chart_y+60}" width="{w_left-40}" height="{remaining_h-80}" fill="#F8FAFC" stroke="#E2E8F0" rx="4" />')
        svg.append(f'  <text x="{30+w_left/2}" y="{chart_y+remaining_h/2+10}" font-family="Segoe UI" font-size="13" font-weight="600" fill="#94A3B8" text-anchor="middle">[{c1_type} Placeholder: {c1_title}]</text>')
        
        # Right Top Chart
        c2_title, c2_desc, c2_type = charts[1]
        svg.append(f'  <rect x="730" y="{chart_y}" width="{w_right}" height="{h_right}" class="panel-bg" />')
        svg.append(f'  <text x="750" y="{chart_y+24}" class="chart-title">{c2_title}</text>')
        svg.append(f'  <text x="750" y="{chart_y+40}" class="chart-desc">{c2_desc}</text>')
        svg.append(f'  <rect x="750" y="{chart_y+50}" width="{w_right-40}" height="{h_right-65}" fill="#F8FAFC" stroke="#E2E8F0" rx="4" />')
        svg.append(f'  <text x="{730+w_right/2}" y="{chart_y+h_right/2+10}" font-family="Segoe UI" font-size="11" font-weight="600" fill="#94A3B8" text-anchor="middle">[{c2_type} Placeholder]</text>')
        
        # Right Bottom Chart
        c3_title, c3_desc, c3_type = charts[2]
        c3_y = chart_y + h_right + 16
        svg.append(f'  <rect x="730" y="{c3_y}" width="{w_right}" height="{h_right}" class="panel-bg" />')
        svg.append(f'  <text x="750" y="{c3_y+24}" class="chart-title">{c3_title}</text>')
        svg.append(f'  <text x="750" y="{c3_y+40}" class="chart-desc">{c3_desc}</text>')
        svg.append(f'  <rect x="750" y="{c3_y+50}" width="{w_right-40}" height="{h_right-65}" fill="#F8FAFC" stroke="#E2E8F0" rx="4" />')
        svg.append(f'  <text x="{730+w_right/2}" y="{c3_y+h_right/2+10}" font-family="Segoe UI" font-size="11" font-weight="600" fill="#94A3B8" text-anchor="middle">[{c3_type} Placeholder]</text>')

    # Footnote & Notice Footer
    svg.append(f'  <text x="30" y="782" class="footer-txt">Data Source: {data_source}</text>')
    svg.append('  <text x="1170" y="782" class="notice-txt" text-anchor="end">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</text>')
    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated wireframe: {filename}")

def build_all_wireframes():
    os.makedirs("08_dashboards/wireframes", exist_ok=True)
    
    # 1. Executive Overview
    generate_svg_wireframe(
        "08_dashboards/wireframes/exec_overview.svg",
        "Executive Overview Dashboard",
        [
            ("DAILY ACTIVE USERS (DAU)", "40.65", "+5.2% vs 7d avg", True),
            ("TASK COMPLETION RATE", "57.15%", "+1.8% vs last week", True),
            ("CIRCULATING XP (EST)", "1.45M XP", "Snapshot total", True),
            ("WITHDRAWAL COMPLETION", "BLOCKED", "Data missing (Gap GAP-002)", False)
        ],
        [
            ("DAU Engagement Trend (Trailing 30 Days)", "Timeseries line showing distinct daily active users", "Line Chart"),
            ("Task Execution Throughput by Category", "Breakdown of completed vs failed attempts by task type", "Stacked Bar"),
            ("Top Platform Features by Adoption", "User penetration across 15 feature surfaces", "Horizontal Bar")
        ],
        [("Date Range", "Trailing 30 Days"), ("Platform", "All Platforms"), ("Country", "India")],
        "04_Daily_Activity, 05_Task_Activity, Users_1000_Clean, 07_Feature_Usage",
        blocked_callout="DATA MISSING — see Gap GAP-002: Cash withdrawal table missing from dataset; payout metrics blocked."
    )

    # 2. User Analytics
    generate_svg_wireframe(
        "08_dashboards/wireframes/user_analytics.svg",
        "User Analytics & Demographics Dashboard",
        [
            ("TOTAL USERS", "1,000", "Simulated baseline", True),
            ("EMAIL VERIFIED", "85.5%", "855 verified accounts", True),
            ("ONBOARDING COMPLETE", "72.2%", "722 completed orientation", True),
            ("30-DAY ACTIVE USERS", "71.7%", "717 monthly active users", True)
        ],
        [
            ("User Acquisition by Marketing Channel", "Donut chart of Organic, Social Media, Direct, Referral", "Donut Chart"),
            ("Geographic Distribution (Top 10 Indian States)", "Horizontal bar chart of user count by state", "Horizontal Bar"),
            ("User Tenure & Age Group Segmentation", "Distribution of account age and demographic cohorts", "Grouped Column")
        ],
        [("Date Range", "All Time"), ("Acquisition Source", "All Channels"), ("Device", "All Devices")],
        "Users_1000_Clean, 01_Users_1000"
    )

    # 3. Engagement
    generate_svg_wireframe(
        "08_dashboards/wireframes/engagement.svg",
        "Engagement & Retention Dashboard",
        [
            ("AVG SESSION DURATION", "51.81s", "Median: 42.0s across 7,913 sess", True),
            ("7-DAY STREAK RETENTION", "42.10%", "421 users reached milestone", True),
            ("STICKINESS (DAU/MAU)", "20.4%", "Daily return habit benchmark", True),
            ("SESSION BOUNCE RATE", "8.4%", "Sessions < 10s or 1 event", False)
        ],
        [
            ("Feature Penetration & Adoption (15 Features)", "User adoption rate across all platform surfaces", "Horizontal Bar"),
            ("Diurnal Hourly Session Volume (24h)", "Distribution of app launches by hour of day", "Column Chart"),
            ("Consecutive Active Streak Distribution", "Histogram of user active streak days", "Area Chart")
        ],
        [("Date Range", "Trailing 30 Days"), ("Platform", "Android / iOS"), ("Entry Point", "All Surfaces")],
        "02_Sessions, 04_Daily_Activity, 06_Milestones, 07_Feature_Usage"
    )

    # 4. Rewards
    generate_svg_wireframe(
        "08_dashboards/wireframes/rewards.svg",
        "Rewards & Micro-Task Performance Dashboard",
        [
            ("TASK COMPLETIONS", "5,627", "57.15% completion rate", True),
            ("TASK FAILURES", "1,520", "15.44% technical failure rate", False),
            ("TASK ABANDONMENT", "2,051", "20.83% premature drop-off", False),
            ("REWARD REVERSAL RATE", "BLOCKED", "Data missing (Gap GAP-001/GAP-007)", False)
        ],
        [
            ("Task Performance by Category (Completed / Failed / Abandoned)", "Categorical breakdown of task execution outcomes", "Grouped Bar"),
            ("Diagnostic Failure Root Cause Analysis", "Distribution of errors: Network Disconnect, Ad Skip, Timeout", "Donut Chart"),
            ("Daily Reward Claim Velocity", "Daily check-in claim frequency across observation period", "Line Chart")
        ],
        [("Date Range", "Trailing 30 Days"), ("Task Category", "All Categories"), ("Device", "All Devices")],
        "05_Task_Activity, 04_Daily_Activity",
        blocked_callout="DATA MISSING — see Gap GAP-001 / GAP-007: Reward clawback and reversal telemetry missing from dataset."
    )

    # 5. Wallet
    generate_svg_wireframe(
        "08_dashboards/wireframes/wallet.svg",
        "Wallet & Currency Economics Dashboard",
        [
            ("CIRCULATING XP (EST)", "1.45M XP", "Snapshot sum on clean users", True),
            ("AVG ACTIVE BALANCE", "1,450 XP", "≈ ₹145 INR nominal value", True),
            ("WALLET VIEW RATE", "32.6%", "Users inspecting balance daily", True),
            ("POINT VELOCITY (EARN/BURN)", "BLOCKED", "Data missing (Gap GAP-001)", False)
        ],
        [
            ("User Balance Tier Distribution", "User count across 0-500, 501-1000, 1001-2000, 2000+ XP tiers", "Bar Chart"),
            ("Wallet Screen Inspection Cadence", "Daily count of wallet visits vs task completions", "Line Chart"),
            ("Projected Point Liability Accrual (Blocked)", "Simulated ledger credit/debit accumulation over time", "Stacked Area")
        ],
        [("Date Range", "Current Snapshot"), ("Account Status", "Active / Pending"), ("Balance Tier", "All Tiers")],
        # DEPRECATED TABLE — Wallet_Transactions is superseded by ledger_entries.
        # See 03_specs/wallet_ledger_spec.md §5 for migration.
        # Retained for historical reference only. Do not add new reads/writes.
        "Users_1000_Clean, 04_Daily_Activity, Wallet_Transactions (Proposed)",
        blocked_callout="DATA MISSING — see Gap GAP-001: Double-entry wallet transaction ledger table is absent; running balance timeseries blocked."
    )

    # 6. Withdrawals
    generate_svg_wireframe(
        "08_dashboards/wireframes/withdrawals.svg",
        "Withdrawal & Cash Disbursement Dashboard",
        [
            ("COMPLETION RATE", "BLOCKED", "Missing table (Gap GAP-002)", False),
            ("GROSS DISBURSED (GWV)", "BLOCKED", "Missing table (Gap GAP-002)", False),
            ("AVERAGE PAYOUT SLA", "BLOCKED", "Missing table (Gap GAP-002)", False),
            ("PENDING ESCROW", "BLOCKED", "Missing table (Gap GAP-002)", False)
        ],
        [
            ("Payout Funnel: Requested -> Processing -> Settled (Blocked)", "Disbursement state machine progression and drop-offs", "Funnel Chart"),
            ("Disbursement Volume by Payout Rail (Blocked)", "Share of payouts across UPI, IMPS, and Merchant Vouchers", "Donut Chart"),
            ("Daily Cash Burn & Gateway Failure Rate (Blocked)", "Disbursement value and banking rail error trend over time", "Timeseries Bar")
        ],
        [("Date Range", "Trailing 30 Days"), ("Payout Rail", "UPI / IMPS / Voucher"), ("Gateway", "All Gateways")],
        "Withdrawals (Proposed Entity - er_diagram.dbml)",
        blocked_callout="DATA MISSING — see Gap GAP-002: Standalone Withdrawals table completely omitted from source data; all payout visuals blocked."
    )

    # 7. Referrals
    generate_svg_wireframe(
        "08_dashboards/wireframes/referrals.svg",
        "Referral & Viral Growth Dashboard",
        [
            ("INBOUND REFERRAL SHARE", "11.9% - 15.4%", "119 users (WB2) / 154 users (WB1)", True),
            ("OUTBOUND SHARING RATE", "18.2%", "Daily active users sharing links", True),
            ("VIRAL K-FACTOR (CONV)", "PROPOSED", "Partial: Outbound funnel blocked", False),
            ("QUALIFICATION DROPOFF", "BLOCKED", "Data missing (Gap GAP-003)", False)
        ],
        [
            ("Referral Funnel: Created -> Registered -> Qualified (Blocked)", "End-to-end viral progression enforcing Registration != Conversion", "Funnel Chart"),
            ("Referee Acquisition by Sub-Channel Detail", "Friend/Family vs Influencer vs Social Post share breakdown", "Donut Chart"),
            ("Referee Retention vs Organic Retention Benchmark", "Cohort retention curves comparing referral vs direct acquisition", "Line Chart")
        ],
        [("Date Range", "All Time"), ("Channel", "WhatsApp / Telegram / Social"), ("Status", "All Statuses")],
        "Users_1000_Clean, 04_Daily_Activity, Referrals (Proposed Entity - er_diagram.dbml)",
        blocked_callout="DATA MISSING — see Gap GAP-003: Outbound referral invitation table missing; full viral conversion funnel blocked."
    )

if __name__ == "__main__":
    build_blueprint_spreadsheet()
    build_all_wireframes()
