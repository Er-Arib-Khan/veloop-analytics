#!/usr/bin/env python3
"""
scripts/12_build_governance_artefacts.py
Generates:
1. 01_governance/metric_event_change_log.xlsx (Sheet "Changes", plus SIMULATED_DATA_NOTICE)
2. 01_governance/assumption_verification_register.xlsx (Sheet "Assumptions", plus SIMULATED_DATA_NOTICE)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_metric_event_change_log():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Changes
    # ----------------------------------------------------
    ws_changes = wb.active
    ws_changes.title = "Changes"
    
    headers = [
        "Date",
        "Change",
        "Old Definition",
        "New Definition",
        "Reason",
        "Affected KPIs",
        "Affected Dashboards",
        "Affected Reports",
        "Owner",
        "Version",
        "Notes"
    ]
    
    entries = [
        (
            "2026-11-15",
            "DAU Definition: Transition from Raw Session Ping to Qualified Active Engagement",
            "Any user initiating a session with session_duration_seconds > 0 regardless of interaction depth.",
            "User must complete at least one qualified value-generating interaction event (e.g. task_started, ad_completed, daily_reward_claimed, spin_completed) within the calendar day.",
            "Eliminates ghost session inflation caused by silent background push notifications, OS background wakeups, and instant bounce exits (<3s dwell).",
            "Daily Active Users (KPI-ENG-01), DAU/MAU Ratio (KPI-ENG-03), Average Revenue Per DAU (ARPDAU)",
            "Executive Overview, User Analytics, Engagement Dashboard",
            "Daily Executive Standup Digest, Board Investor Metrics Pack",
            "Lead Product Analyst",
            "v1.1.0-proposed",
            "Status = Proposed. Pending review post-beta launch telemetry audit."
        ),
        (
            "2026-11-20",
            "Task Completion Rate: Denominator Standardization on Execution Intent",
            "Total task_completed events divided by total task_viewed impressions recorded in task discovery catalog.",
            "Total task_completed events divided strictly by verified task_started events where user confirmed execution intent.",
            "Decouples catalog browsing and scroll dwell drop-off from technical execution reliability; browsing drop-off is moved to separate Task Discovery Funnel metric.",
            "Task Completion Rate (KPI-ENG-04), Task Abandonment Rate, Advertiser Campaign Fill Rate",
            "Engagement Dashboard, Rewards Dashboard",
            "Weekly Product Ops Health Report, Partner Advertiser Performance Pack",
            "Product Ops Manager",
            "v1.1.0-proposed",
            "Status = Proposed. Requires deployment of task_viewed telemetry."
        ),
        (
            "2026-11-25",
            "Referral Conversion Qualification: Stricter Hurdle to Prevent Sybil Abuse",
            "Referee creates account and reaches >= 100 XP cumulative earnings across any time window.",
            "Referee creates account, verifies phone number, and earns >= 250 XP strictly from third-party tasks across at least 2 distinct active calendar days.",
            "Pre-launch fraud audit revealed emulator farms automating introductory tutorials to claim 100 XP referral bounties without genuine ad engagement.",
            "Referral Conversion Rate (KPI-REF-03), Viral K-Factor (KPI-REF-02), Referral Bounty Expense (INR)",
            "Executive Overview, Referral Dashboard",
            "Weekly Growth & Acquisition Review, Fraud Risk Committee Digest",
            "Head of Growth / Risk Lead",
            "v1.2.0-proposed",
            "Status = Proposed. Aligned with anti-fraud sybil detection rules."
        ),
        (
            "2026-12-01",
            "Withdrawal Turnaround SLA Clock: Inception at Risk Clearance vs Form Submission",
            "Elapsed hours measured from withdrawal_requested timestamp to gateway webhook confirmation.",
            "Elapsed hours measured strictly from risk_screening_approved timestamp to gateway webhook confirmation; user submission to risk review is tracked as separate Escrow Queue Time.",
            "Isolates external banking payment rail throughput (RazorpayX/Cashfree) from internal compliance and manual review hold delays for high-value redemptions (>₹500).",
            "Average Withdrawal Turnaround Time (KPI-WDL-04), Withdrawal SLA Compliance Rate",
            "Withdrawal Dashboard, Executive Overview",
            "Daily Treasury Operations Report, Banking Rail SLA Review",
            "Lead Data Engineer",
            "v1.2.0-proposed",
            "Status = Proposed. Dependent on risk_screening_approved event instrumentation."
        ),
        (
            "2026-12-05",
            "Reward Currency Valuation: Dynamic Catalog Redemption Pricing vs Flat 10:1 Peg",
            "Virtual XP pegged at a fixed nominal ratio of 100 XP = ₹10.00 INR (10 XP = ₹1 INR) across all redemption options.",
            "Virtual XP pegged at baseline 100 XP = ₹10 INR for UPI cash-out, with dynamic merchant catalog voucher pricing (e.g. Amazon ₹100 voucher at 900 XP; Swiggy ₹50 voucher at 420 XP).",
            "Enables platform to capture merchant affiliate commission discounts and incentivize high-margin voucher redemptions over direct cash outflows.",
            "Average Cost Per XP Redeemed (KPI-REW-05), Gross Take-Rate, Net Platform Margin",
            "Rewards Dashboard, Executive Overview",
            "Monthly Finance & Margin Audit, Merchant Partnership Strategy Review",
            "VP Finance & Commercial Strategy",
            "v1.3.0-proposed",
            "Status = Proposed. Requires rewards_catalog master table rollout."
        )
    ]
    
    # Template Row for future append entries
    template_row = (
        "[YYYY-MM-DD]",
        "[Short Description of Metric or Event Modification]",
        "[Previous Formal Definition / Formula / Scope]",
        "[New Formal Definition / Formula / Scope]",
        "[Business or Technical Justification for the Modification]",
        "[Comma-separated KPI IDs, e.g. KPI-USR-01, KPI-ENG-02]",
        "[Comma-separated Dashboard Titles, e.g. Executive Overview]",
        "[Comma-separated Report Names, e.g. Weekly Financial Digest]",
        "[Name and Role of Accountable Specification Owner]",
        "[Semantic Version, e.g. v1.x.x-proposed]",
        "Status = Proposed | Confirmed | Deprecated. [Implementation Notes]"
    )
    
    # Styling
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    template_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    template_font = Font(name="Calibri", size=10, italic=True, color="595959")
    
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # Write Headers
    for c_idx, h in enumerate(headers, 1):
        cell = ws_changes.cell(row=1, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_changes.row_dimensions[1].height = 28
    
    # Write 5 entries
    for r_idx, entry in enumerate(entries, 2):
        for c_idx, val in enumerate(entry, 1):
            cell = ws_changes.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = border_thin
            align = "left" if c_idx not in [1, 10] else "center"
            cell.alignment = Alignment(horizontal=align, vertical="top", wrap_text=True)
        ws_changes.row_dimensions[r_idx].height = 65
        
    # Write Template Row at row 7
    r_template = len(entries) + 2
    for c_idx, val in enumerate(template_row, 1):
        cell = ws_changes.cell(row=r_template, column=c_idx, value=val)
        cell.fill = template_fill
        cell.font = template_font
        cell.border = border_thin
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws_changes.row_dimensions[r_template].height = 45

    # Auto-adjust column widths
    col_widths = {
        1: 14,  # Date
        2: 30,  # Change
        3: 35,  # Old Definition
        4: 38,  # New Definition
        5: 38,  # Reason
        6: 28,  # Affected KPIs
        7: 25,  # Affected Dashboards
        8: 28,  # Affected Reports
        9: 20,  # Owner
        10: 16, # Version
        11: 30  # Notes
    }
    for col_idx, width in col_widths.items():
        ws_changes.column_dimensions[get_column_letter(col_idx)].width = width
        
    ws_changes.freeze_panes = "A2"
    
    # ----------------------------------------------------
    # Sheet 2: SIMULATED_DATA_NOTICE
    # ----------------------------------------------------
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.cell(row=1, column=1, value="SIMULATED DATA NOTICE").font = Font(name="Calibri", size=14, bold=True, color="C00000")
    ws_notice.cell(row=3, column=1, value="SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data.").font = Font(name="Calibri", size=11, bold=True)
    ws_notice.cell(row=5, column=1, value="All entries in this change log represent proposed future governance iterations and simulated lifecycle specifications.").font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 100

    wb.save("01_governance/metric_event_change_log.xlsx")
    print("Successfully generated 01_governance/metric_event_change_log.xlsx")

def build_assumption_verification_register():
    wb = openpyxl.Workbook()
    
    ws_assump = wb.active
    ws_assump.title = "Assumptions"
    
    headers = [
        "ID",
        "Unknown",
        "Why It Matters",
        "Source Checked",
        "Risk",
        "Verification Owner",
        "Status"
    ]
    
    # 15 exhaustive rows capturing all 'To Be Verified' items across prior deliverables
    assumptions_data = [
        (
            "ASMP-001",
            "Event Sequence Number Integrity within Sessions",
            "Profiling revealed duplicate sequence_number values within single sessions in 03_Feature_Events. If client sequence counters reset or race across threads, user session navigation pathing and step drop-off funnels cannot be accurately reconstructed.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (03_Feature_Events), 07_data_quality/relationship_test.xlsx",
            "High",
            "Mobile SDK Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-002",
            "Negative Days Since Registration Anomaly in User Master",
            "Analysis revealed days_since_registration has a minimum value of -0.8 days for 8 users in Users_Messy_Audit / Users_Clean, indicating snapshot generation timestamp preceded user registration time. Affects cohort tenure groupings and Day-0 retention calculation.",
            "00_source_data/veloop_rewards_data_01.xlsx (Users_1000_Clean & Users_Messy_Audit), 07_data_quality/profiling_summary.xlsx",
            "Medium",
            "Data Pipeline Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-003",
            "Timestamp Timezone and Client Clock Offset Standards",
            "All timestamps in source workbooks are unzoned datetime strings without explicit UTC ('Z') designators or offset indicators (+05:30). If client clocks are unsynchronized, daily active boundaries, streak retention, and diurnal activity curves will skew across timezones.",
            "00_source_data (All sheets across both workbooks), 04_events/event_naming_standard.md",
            "High",
            "Lead Backend Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-004",
            "Task Category Controlled Taxonomy and Harmonization",
            "05_Task_Activity contains task_category values that require verification against Task_Master dimensional definitions to ensure partner campaigns, difficulty tiers, and reward payout weights are normalized without casing or trailing whitespace discrepancies.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (05_Task_Activity), 05_data_model/data_dictionary.xlsx",
            "Medium",
            "Product Ops Manager",
            "To Be Verified"
        ),
        (
            "ASMP-005",
            "Referral Attribution Linkage Mechanism: Code vs Deep-Link",
            "Users table provides static referral_code, but lacks underlying referral_invites event tracking to differentiate whether referee typed a code manually, clicked a WhatsApp deep link, or was attributed via dynamic install referrer API.",
            "00_source_data/veloop_rewards_data_01.xlsx, 03_specs/referral_engagement_analytics.md",
            "Critical",
            "Growth Product Manager",
            "To Be Verified"
        ),
        (
            "ASMP-006",
            "Milestone Unlocking Cadence: Idempotent vs Repeatable Seasons",
            "06_Milestones records 4,799 milestone unlock rows across 1,000 users. It must be verified whether milestones (e.g. 'seventh_active_day', 'points_500') are one-time lifetime achievements or reset cyclically per monthly season or promotional league.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (06_Milestones), 03_specs/reward_analytics_spec.md",
            "Medium",
            "Lead Game Designer",
            "To Be Verified"
        ),
        (
            "ASMP-007",
            "Session Termination Boundary: Dwell Time vs Background Heartbeat",
            "02_Sessions logs session_duration_seconds ranging from 5s to 180s (mean 51.8s). Must verify whether session end is determined by client app backgrounding, OS process kill, or a 30-minute inactivity sliding window.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (02_Sessions), 07_data_quality/kpi_feasibility.xlsx",
            "Medium",
            "Mobile Lead Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-008",
            "Payment Gateway Integration Feasibility for Instant UPI Payouts",
            "Withdrawal analytics spec assumes RazorpayX / Cashfree integration supporting instant UPI VPA disbursements. Technical support for webhook callbacks, return codes, and bank account name verification (penny drop) must be verified prior to launch.",
            "03_specs/wallet_withdrawal_analytics_spec.md, 09_engineering/developer_analytics_handoff.xlsx",
            "Critical",
            "Fintech Backend Lead",
            "To Be Verified"
        ),
        (
            "ASMP-009",
            "Virtual Currency Valuation Peg and Breakage Economics",
            "Current model assumes a fixed economic peg of 100 XP = ₹10 INR (10 XP = ₹1 INR). Financial assumptions regarding point breakage, unredeemed liability expiration (e.g. 12-month dormancy purge), and merchant catalog voucher margins require formal CFO sign-off.",
            "03_specs/reward_analytics_spec.md, 06_kpis/kpi_catalogue.xlsx",
            "Critical",
            "VP Finance & Commercial",
            "To Be Verified"
        ),
        (
            "ASMP-010",
            "Onboarding Wizard Screen Transitions and Micro-Funnels",
            "User table contains coarse onboarding_status ('Started', 'Completed', 'Skipped'). Technical instrumentation must verify whether client emits discrete step-level events (onboarding_step_viewed, permissions_prompt_answered) to identify tutorial drop-off screens.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (01_Users_1000), 03_specs/user_analytics_spec.md",
            "High",
            "UX / Mobile Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-011",
            "Withdrawal Approval Hierarchy and Automated Fraud Thresholds",
            "Assumed that withdrawal requests below ₹200 INR with low device risk scores disburse automatically via webhook, while requests >= ₹500 INR enter manual ops approval queue. Exact risk scoring thresholds and escalation queues must be confirmed.",
            "03_specs/wallet_withdrawal_analytics_spec.md, 10_privacy_governance/privacy_governance_proposal.md",
            "Critical",
            "Head of Trust & Safety",
            "To Be Verified"
        ),
        (
            "ASMP-012",
            "Standardized Failure Reason Taxonomy across Third-Party Tasks",
            "Task_Activity records failure_reason strings (e.g. 'Timeout', 'Network Drop', 'User Abort'). Must verify standardized error code mappings across disparate external offerwall SDKs (Tapjoy, ironSource, AdMob) to prevent unmapped failure categories.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (05_Task_Activity), 07_data_quality/data_quality_audit.xlsx",
            "High",
            "Third-Party Ad SDK Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-013",
            "7-Day Consecutive Streak Calendar Reset Definition",
            "7-day streak retention assumes consecutive calendar day logins. Must verify whether streak reset occurs at 00:00:00 UTC, 00:00:00 IST (UTC+5:30), or a 36-hour grace period window to prevent unfair streak loss for diurnal late-night users.",
            "07_data_quality/kpi_feasibility.xlsx (KPI 7), 06_kpis/kpi_catalogue.xlsx",
            "High",
            "Game Economy Designer",
            "To Be Verified"
        ),
        (
            "ASMP-014",
            "Daily Free Spin Limit Refresh Cadence",
            "Feature_Usage tracks daily Spin feature activity. Must verify whether free spins refresh on a fixed calendar date schedule (midnight) or on a rolling 24-hour cooldown timer from the moment of the user's previous spin.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (07_Feature_Usage), 02_product_audit/product_data_audit.md",
            "Medium",
            "Backend Game Engine Lead",
            "To Be Verified"
        ),
        (
            "ASMP-015",
            "App Build Version and OS Architecture Telemetry Capture",
            "Feature_Events provides platform ('Android Native', 'iOS Native') but lacks semantic app_version ('v1.0.4+42') and OS build number. Critical for isolating client-side crash regressions and SDK telemetry bugs to specific app releases.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (03_Feature_Events), 09_engineering/developer_analytics_handoff.xlsx",
            "High",
            "Mobile DevOps Engineer",
            "To Be Verified"
        ),
        (
            "ASMP-016",
            "Environment Tagging (data_environment) in User Master",
            "05_data_model/data_dictionary.xlsx and Users_Messy_Audit contain data_environment tag. Must verify whether synthetic testing environment tags or staging flags persist in production data schemas.",
            "00_source_data/veloop_rewards_data_01.xlsx (Users_Messy_Audit), 05_data_model/data_dictionary.xlsx (user data_environment)",
            "Low",
            "Data Governance Lead",
            "To Be Verified"
        ),
        (
            "ASMP-017",
            "Task Activity Reward Settlement Lifecycle (reward_status)",
            "05_Task_Activity and data_dictionary.xlsx define reward_status (Credited, Pending, None). Must verify reward settlement lifecycle rules, timeout durations for pending credits, and ledger reconciliation triggers.",
            "00_source_data/veloop_simulated_user_behavior_1000.xlsx (05_Task_Activity), 05_data_model/data_dictionary.xlsx (task_activity reward_status)",
            "Medium",
            "Fintech Backend Lead",
            "To Be Verified"
        )
    ]
    
    # Styling
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # Write Headers
    for c_idx, h in enumerate(headers, 1):
        cell = ws_assump.cell(row=1, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_assump.row_dimensions[1].height = 28
    
    # Write Rows
    for r_idx, row_vals in enumerate(assumptions_data, 2):
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws_assump.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = border_thin
            
            # Alignments
            if c_idx in [1, 5, 7]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                
            # Highlight Risk
            if c_idx == 5:
                if val == "Critical":
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C00000")
                elif val == "High":
                    cell.font = Font(name="Calibri", size=10, bold=True, color="ED7D31")
                elif val == "Medium":
                    cell.font = Font(name="Calibri", size=10, color="70AD47")
                    
        ws_assump.row_dimensions[r_idx].height = 65

    # Column widths
    col_widths = {
        1: 14, # ID
        2: 32, # Unknown
        3: 45, # Why It Matters
        4: 35, # Source Checked
        5: 14, # Risk
        6: 22, # Verification Owner
        7: 18  # Status
    }
    for col_idx, width in col_widths.items():
        ws_assump.column_dimensions[get_column_letter(col_idx)].width = width
        
    ws_assump.freeze_panes = "A2"
    
    # ----------------------------------------------------
    # Sheet 2: SIMULATED_DATA_NOTICE
    # ----------------------------------------------------
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.cell(row=1, column=1, value="SIMULATED DATA NOTICE").font = Font(name="Calibri", size=14, bold=True, color="C00000")
    ws_notice.cell(row=3, column=1, value="SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data.").font = Font(name="Calibri", size=11, bold=True)
    ws_notice.cell(row=5, column=1, value="All assumptions and unknowns cataloged in this register represent operational hypotheses and telemetry verification items identified during testing of simulated datasets.").font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 100

    wb.save("01_governance/assumption_verification_register.xlsx")
    print(f"Successfully generated 01_governance/assumption_verification_register.xlsx with {len(assumptions_data)} rows.")

if __name__ == "__main__":
    build_metric_event_change_log()
    build_assumption_verification_register()
