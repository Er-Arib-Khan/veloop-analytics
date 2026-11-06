#!/usr/bin/env python3
"""
scripts/13_build_implementation_backlog.py
Generates 11_backlog/implementation_backlog.xlsx with sheets:
1. 'Backlog' (Columns: Priority | Requirement ID | Requirement | Reason | Dependency | Owner | Stage | Linked Gap ID | Linked Assumption ID)
2. 'Dependency_Graph' (Mermaid block rendered as text: Critical -> High -> Medium -> Low with dependency arrows)
3. 'SIMULATED_DATA_NOTICE' (governance notice)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_implementation_backlog():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Backlog
    # ----------------------------------------------------
    ws_backlog = wb.active
    ws_backlog.title = "Backlog"
    
    headers = [
        "Priority",
        "Requirement ID",
        "Requirement",
        "Reason",
        "Dependency",
        "Owner",
        "Stage",
        "Linked Gap ID",
        "Linked Assumption ID"
    ]
    
    backlog_data = [
        # ====================================================
        # CRITICAL REQUIREMENTS (10 Items)
        # ====================================================
        (
            "Critical",
            "REQ-BL-01",
            "Stable User Identifier Model (UUIDv4 / VLUSR)",
            "Enforces persistent, immutable user identifiers across auth, sessions, clickstream, and financial ledgers; strictly disallows recycling of deleted account IDs.",
            "Auth Service Database Migration",
            "Backend Lead Engineer",
            "Pre-launch",
            "GAP-DQ-02",
            "ASMP-002"
        ),
        (
            "Critical",
            "REQ-BL-02",
            "Double-Entry Wallet Transactions Ledger (wallet_transactions)",
            "Deploys append-only relational ledger table (transaction_id, user_id, amount, balance_after, reference_id) with strict double-entry journal integrity; directly unblocks KPI-WAL-02 (Point Velocity (Accrual vs Burn Ratio)).",
            "REQ-BL-01 (Stable User ID)",
            "Fintech Backend Lead",
            "Pre-launch",
            "GAP-MOD-01",
            "ASMP-009"
        ),
        (
            "Critical",
            "REQ-BL-03",
            "Fiat Cash Disbursements Relational Table (withdrawals)",
            "Deploys immutable payout request schema (withdrawal_id, user_id, amount_inr, xp_deducted, payout_method, payout_status, gateway_reference) for liquidity tracking; directly unblocks KPI-WDL-01 (Withdrawal Completion Rate), KPI-WDL-02 (Gross Withdrawal Value), KPI-WDL-03 (Average Payout Processing SLA), KPI-WDL-04 (Withdrawal Rejection Rate), and KPI-WDL-05 (Pending Escrow Payout Liability).",
            "REQ-BL-02 (Wallet Ledger)",
            "Fintech Backend Lead",
            "Pre-launch",
            "GAP-MOD-02",
            "ASMP-008"
        ),
        (
            "Critical",
            "REQ-BL-04",
            "Referral Attribution & Conversion Graph (referrals)",
            "Implements relational referral model capturing outbound invite links, referee registration linkage, and commercial conversion milestones (100 XP earned); directly unblocks KPI-REF-04 (Referral Qualification Drop-off Rate).",
            "REQ-BL-01 (Stable User ID)",
            "Growth Lead Engineer",
            "Pre-launch",
            "GAP-MOD-05",
            "ASMP-005"
        ),
        (
            "Critical",
            "REQ-BL-05",
            "Core Event Tracking Taxonomy & Ingress Gateway",
            "Deploys client/server telemetry pipeline enforcing object_action syntax, JSON payload validation against data dictionary, and device metadata stamping.",
            "REQ-BL-01 (Stable User ID)",
            "Lead Data Engineer",
            "Pre-launch",
            "GAP-EVT-01",
            "ASMP-001"
        ),
        (
            "Critical",
            "REQ-BL-06",
            "Reward Mutation Event Telemetry Stream (reward_credited, reward_reversed)",
            "Instruments settlement engine to emit atomic events on reward credits, escrow holds, and fraud reversals directly linked to wallet ledger transaction IDs.",
            "REQ-BL-02 (Wallet Ledger), REQ-BL-05 (Event Tracking)",
            "Fintech Backend Lead",
            "Pre-launch",
            "GAP-EVT-01",
            "ASMP-009"
        ),
        (
            "Critical",
            "REQ-BL-07",
            "Universal UTC ISO-8601 Timestamp Clock Standardization",
            "Enforces server-monotonic ISO-8601 UTC timestamps (YYYY-MM-DDTHH:MM:SS.sssZ) across all API gateways, eliminating timezone drift in retention and streak metrics.",
            "API Ingress Gateway Configuration",
            "Lead Backend Engineer",
            "Pre-launch",
            "GAP-DQ-05",
            "ASMP-003"
        ),
        (
            "Critical",
            "REQ-BL-08",
            "Ingress Stream Idempotency & Deduplication Engine",
            "Deploys Redis 24h sliding-window deduplication cache on (user_id, natural_key) / event_id and database unique constraints to prevent double-crediting.",
            "REQ-BL-05 (Event Tracking)",
            "Data Platform Engineer",
            "Pre-launch",
            "GAP-DQ-01",
            "ASMP-001"
        ),
        (
            "Critical",
            "REQ-BL-09",
            "Automated Real-Time Ledger Balance Discrepancy Circuit-Breaker & Dispute Engine",
            "Deploys automated hourly reconciliation script verifying sum(credits) - sum(debits) = balance_after; halts automated payouts upon variance; unblocks support & dispute tracking for KPI-SUP-02 (Support Ticket Resolution SLA) and KPI-SUP-03 (Dispute Rate per 1,000 Completed Tasks).",
            "REQ-BL-02 (Wallet Ledger), REQ-BL-03 (Withdrawals)",
            "Lead Data Engineer",
            "Pre-launch",
            "GAP-REP-02",
            "ASMP-009"
        ),
        (
            "Critical",
            "REQ-BL-10",
            "Customer PII Redaction & Pseudonymization Ingestion Filter",
            "Implements automated regex redaction filters in ingestion workers to scrub emails, phone numbers, and bank account numbers from free-text and event payloads.",
            "REQ-BL-05 (Event Tracking)",
            "Data Governance Lead",
            "Pre-launch",
            "GAP-ACC-02",
            "ASMP-008"
        ),

        # ====================================================
        # HIGH PRIORITY REQUIREMENTS (9 Items)
        # ====================================================
        (
            "High",
            "REQ-BL-11",
            "Automated Data Quality Testing Suite (dbt-expectations)",
            "Deploys CI/CD and scheduled dbt tests validating non-null primary keys, positive balances, approved categorical values, and foreign key completeness.",
            "REQ-BL-02, REQ-BL-05",
            "Analytics Engineer",
            "Pre-launch",
            "GAP-DQ-03",
            "ASMP-002"
        ),
        (
            "High",
            "REQ-BL-12",
            "Task Master Dimensional Catalog (task_master)",
            "Deploys dimension table for 80 distinct task IDs detailing advertiser partner, difficulty category, estimated completion duration, and reward XP payouts.",
            "Task Service Database",
            "Product Ops Lead",
            "Pre-launch",
            "GAP-MOD-03",
            "ASMP-004"
        ),
        (
            "High",
            "REQ-BL-13",
            "Reward SKU Inventory Dimension (rewards_catalog)",
            "Implements master catalog managing merchant partner vouchers (Amazon, Flipkart), inventory stock counts, fiat INR values, and XP redemption costs.",
            "Rewards Service Database",
            "Product Ops Lead",
            "Pre-launch",
            "GAP-MOD-04",
            "ASMP-009"
        ),
        (
            "High",
            "REQ-BL-14",
            "Client Offline SQLite Event Spooling & Jitter Replay",
            "Implements encrypted local SQLite buffer in mobile SDK storing up to 500 events during offline network states, flushing with random jitter upon reconnect.",
            "Mobile SDK Core",
            "Mobile Lead Engineer",
            "Pre-launch",
            "GAP-ENG-02",
            "ASMP-007"
        ),
        (
            "High",
            "REQ-BL-15",
            "Server-to-Server (S2S) Ad Mediation Postback Integration",
            "Connects third-party ad networks (AdMob, ironSource, AppsFlyer) via authenticated webhooks to verify creative completions prior to XP disbursement.",
            "REQ-BL-06 (Reward Telemetry)",
            "AdTech Integration Lead",
            "Pre-launch",
            "GAP-ENG-01",
            "ASMP-012"
        ),
        (
            "High",
            "REQ-BL-16",
            "Onboarding Step-Level Micro-Funnel Telemetry",
            "Instruments screen-level transition events (onboarding_step_viewed, permissions_requested) to pinpoint user drop-offs across introductory orientation screens.",
            "REQ-BL-05 (Event Tracking)",
            "Mobile Frontend Engineer",
            "Pre-launch",
            "GAP-EVT-04",
            "ASMP-010"
        ),
        (
            "High",
            "REQ-BL-17",
            "Core Operational BI Dashboards (Looker Studio / Metabase)",
            "Constructs and deploys the 7 core executive and product dashboards (Executive Overview, User, Engagement, Rewards, Wallet, Withdrawals, Referrals).",
            "REQ-BL-02, REQ-BL-03, REQ-BL-04, REQ-BL-05",
            "BI Developer",
            "Pre-launch",
            "GAP-DSH-01",
            "ASMP-008"
        ),
        (
            "High",
            "REQ-BL-18",
            "Ingress Telemetry Latency & P1/P2 Alerting Matrix",
            "Configures Cloud Monitoring and Telegram/Slack webhooks tracking ingress 5xx rates (>5%), dead-letter queue depth (>100), and P95 latency (>1s).",
            "REQ-BL-05 (Event Tracking)",
            "DevOps / SRE Lead",
            "Pre-launch",
            "GAP-REP-01",
            "ASMP-003"
        ),
        (
            "High",
            "REQ-BL-19",
            "Role-Based Access Control (RBAC) Warehouse Permissions",
            "Implements BigQuery IAM role separation enforcing least-privilege boundaries between Engineering, Data Analysts, Product/Ops, and Interns.",
            "BigQuery Project IAM",
            "Data Governance Steward",
            "Pre-launch",
            "GAP-ACC-01",
            "ASMP-008"
        ),

        # ====================================================
        # MEDIUM PRIORITY REQUIREMENTS (4 Items)
        # ====================================================
        (
            "Medium",
            "REQ-BL-20",
            "Semantic App Build Version Header Extraction",
            "Extracts app_version ('v1.0.4+42') and OS build number from client HTTP request headers and stamps onto analytical clickstream tables.",
            "REQ-BL-05 (Event Tracking)",
            "Mobile DevOps Engineer",
            "Post-launch",
            "GAP-ENG-03",
            "ASMP-015"
        ),
        (
            "Medium",
            "REQ-BL-21",
            "Automated Daily Executive Standup Webhook Dispatcher",
            "Deploys scheduled Python micro-service broadcasting 08:00 AM executive KPI digests (DAU, task completion rate, gross payout INR) to Slack #exec-standup.",
            "REQ-BL-17 (BI Dashboards)",
            "Analytics Engineer",
            "Post-launch",
            "GAP-REP-01",
            "ASMP-007"
        ),
        (
            "Medium",
            "REQ-BL-22",
            "BigQuery BI Engine In-Memory Query Acceleration",
            "Provisions 1 GB BI Engine memory reservation when concurrent dashboard viewers exceed 10 or query execution latency exceeds 4.0 seconds.",
            "REQ-BL-17 (BI Dashboards)",
            "Data Platform Engineer",
            "Post-launch",
            "GAP-DSH-02",
            "ASMP-008"
        ),
        (
            "Medium",
            "REQ-BL-23",
            "Cryptographic Salt Rotation Automation for Payout Hashes",
            "Deploys automated 90-day salt rotation in KMS Key Vault Manager with dual-version hash lookup to maintain long-term security of payout_account_hash.",
            "REQ-BL-03 (Withdrawals)",
            "Security / Crypto Lead",
            "Post-launch",
            "GAP-ACC-03",
            "ASMP-008"
        ),

        # ====================================================
        # LOW PRIORITY REQUIREMENTS (1 Item)
        # ====================================================
        (
            "Low",
            "REQ-BL-24",
            "Cascading Multi-Filter Synchronization on BI Dashboards",
            "Implements parameterized SQL dropdowns linking platform and primary_device filters in Looker Studio to eliminate empty chart states.",
            "REQ-BL-17 (BI Dashboards)",
            "BI Developer",
            "Post-launch",
            "GAP-DSH-03",
            "ASMP-004"
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
        cell = ws_backlog.cell(row=1, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_backlog.row_dimensions[1].height = 28
    
    # Write Data
    for r_idx, row_vals in enumerate(backlog_data, 2):
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws_backlog.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = border_thin
            
            # Alignments
            if c_idx in [1, 2, 7, 8, 9]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                
            # Highlight Priority
            if c_idx == 1:
                if val == "Critical":
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C00000")
                elif val == "High":
                    cell.font = Font(name="Calibri", size=10, bold=True, color="ED7D31")
                elif val == "Medium":
                    cell.font = Font(name="Calibri", size=10, color="70AD47")
                elif val == "Low":
                    cell.font = Font(name="Calibri", size=10, color="595959")
                    
        ws_backlog.row_dimensions[r_idx].height = 55
        
    # Auto-fit column widths
    col_widths = {
        1: 14, # Priority
        2: 18, # Requirement ID
        3: 35, # Requirement
        4: 45, # Reason
        5: 30, # Dependency
        6: 24, # Owner
        7: 16, # Stage
        8: 18, # Linked Gap ID
        9: 22  # Linked Assumption ID
    }
    for col_idx, width in col_widths.items():
        ws_backlog.column_dimensions[get_column_letter(col_idx)].width = width
        
    ws_backlog.freeze_panes = "A2"
    
    # ----------------------------------------------------
    # Sheet 2: Dependency_Graph
    # ----------------------------------------------------
    ws_graph = wb.create_sheet(title="Dependency_Graph")
    ws_graph.cell(row=1, column=1, value="IMPLEMENTATION DEPENDENCY GRAPH (MERMAID)").font = Font(name="Calibri", size=14, bold=True, color="1F497D")
    
    mermaid_text = """```mermaid
flowchart TD
    %% ====================================================
    %% STAGE 1: CRITICAL PRE-LAUNCH FOUNDATION
    %% ====================================================
    subgraph CRITICAL ["Critical Priority (Pre-Launch Blockers)"]
        direction TB
        C1["REQ-BL-01: Stable User ID<br/>(UUIDv4 / VLUSR)"]
        C7["REQ-BL-07: Timestamp Standard<br/>(ISO-8601 UTC)"]
        C5["REQ-BL-05: Event Tracking Ingress<br/>(object_action Taxonomy)"]
        
        C1 --> C2["REQ-BL-02: Double-Entry Ledger<br/>(wallet_transactions)"]
        C1 --> C4["REQ-BL-04: Referral Graph<br/>(referrals table)"]
        C1 & C7 --> C5
        
        C2 --> C3["REQ-BL-03: Payouts Table<br/>(withdrawals)"]
        C2 & C5 --> C6["REQ-BL-06: Reward Telemetry<br/>(reward_credited/reversed)"]
        C5 --> C8["REQ-BL-08: Ingress Deduplication<br/>(Redis TTL + DB Unique)"]
        C2 & C3 --> C9["REQ-BL-09: Balance Circuit-Breaker<br/>(Hourly Audit Trigger)"]
        C5 --> C10["REQ-BL-10: PII Redaction Filter<br/>(Regex Scrubbing)"]
    end

    %% ====================================================
    %% STAGE 2: HIGH PRIORITY COMMERCIAL LAUNCH HARDENING
    %% ====================================================
    subgraph HIGH ["High Priority (Commercial Launch Hardening)"]
        direction TB
        H1["REQ-BL-11: Data Quality Suite<br/>(dbt-expectations)"]
        H2["REQ-BL-12: Task Master Catalog<br/>(task_master dimension)"]
        H3["REQ-BL-13: Rewards SKU Inventory<br/>(rewards_catalog dimension)"]
        H4["REQ-BL-14: Client Offline Spooling<br/>(SQLite Queue + Jitter)"]
        H5["REQ-BL-15: S2S Ad Postbacks<br/>(Third-Party Verification)"]
        H6["REQ-BL-16: Onboarding Funnel<br/>(Step-Level Telemetry)"]
        H7["REQ-BL-17: 7 Core BI Dashboards<br/>(Looker Studio / Metabase)"]
        H8["REQ-BL-18: Latency Alerting<br/>(P1/P2 Webhooks)"]
        H9["REQ-BL-19: RBAC Warehouse IAM<br/>(Least-Privilege Roles)"]
    end

    %% ====================================================
    %% STAGE 3: MEDIUM & LOW PRIORITY POST-LAUNCH OPTIMIZATION
    %% ====================================================
    subgraph MEDIUM_LOW ["Medium & Low Priority (Post-Launch Optimization)"]
        direction TB
        M1["REQ-BL-20: App Build Versioning<br/>(Header Extraction)"]
        M2["REQ-BL-21: Standup Webhook<br/>(Daily Slack Digest)"]
        M3["REQ-BL-22: BI Engine Acceleration<br/>(Sub-Second In-Memory)"]
        M4["REQ-BL-23: Crypto Salt Rotation<br/>(Automated 90-Day KMS)"]
        L1["REQ-BL-24: Dashboard Cascading Filters<br/>(Parameterized SQL)"]
    end

    %% Dependencies between Tiers
    C2 & C5 --> H1
    C2 & C6 --> H3
    C5 --> H4
    C6 --> H5
    C5 --> H6
    C2 & C3 & C4 & C5 --> H7
    C5 --> H8
    C1 & C2 --> H9

    H5 --> M1
    H7 --> M2
    H7 --> M3
    C3 --> M4
    H7 --> L1

    classDef crit fill:#FCE8E6,stroke:#C5221F,stroke-width:2px;
    classDef high fill:#FEF7E0,stroke:#F9AB00,stroke-width:2px;
    classDef med fill:#E6F4EA,stroke:#137333,stroke-width:2px;

    class C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 crit;
    class H1,H2,H3,H4,H5,H6,H7,H8,H9 high;
    class M1,M2,M3,M4,L1 med;
```"""

    ws_graph.cell(row=3, column=1, value=mermaid_text)
    ws_graph.cell(row=3, column=1).font = Font(name="Consolas", size=10)
    ws_graph.cell(row=3, column=1).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws_graph.column_dimensions["A"].width = 120
    ws_graph.row_dimensions[3].height = 650

    # ----------------------------------------------------
    # Sheet 3: SIMULATED_DATA_NOTICE
    # ----------------------------------------------------
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.cell(row=1, column=1, value="SIMULATED DATA NOTICE").font = Font(name="Calibri", size=14, bold=True, color="C00000")
    ws_notice.cell(row=3, column=1, value="SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data.").font = Font(name="Calibri", size=11, bold=True)
    ws_notice.cell(row=5, column=1, value="All backlog requirements and dependency links represent engineered technical proposals derived from the analysis of simulated test datasets.").font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 100

    wb.save("11_backlog/implementation_backlog.xlsx")
    print(f"Successfully generated 11_backlog/implementation_backlog.xlsx with {len(backlog_data)} requirements.")

if __name__ == "__main__":
    build_implementation_backlog()
