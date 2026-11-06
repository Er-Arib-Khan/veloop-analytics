#!/usr/bin/env python3
"""
scripts/09_build_kpi_catalogue.py
Generates 06_kpis/kpi_catalogue.xlsx with sheets:
1. 'KPIs' (13 exact columns, 34 comprehensive KPIs across 7 areas)
2. 'Coverage_By_Area' (Summary table of KPI counts per area and Confirmed/Blocked split)
3. 'SIMULATED_DATA_NOTICE' (governance notice)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_kpi_catalogue():
    wb = openpyxl.Workbook()

    # ----------------------------------------------------
    # Sheet 1: KPIs
    # ----------------------------------------------------
    ws_kpis = wb.active
    ws_kpis.title = "KPIs"

    headers = [
        "KPI ID",
        "KPI Name",
        "Area",
        "Definition",
        "Formula",
        "Required Fields",
        "Data Source",
        "Frequency",
        "Stakeholder",
        "Business Purpose",
        "Interpretation",
        "Limitation",
        "Status"
    ]

    kpi_catalog = [
        # ====================================================
        # AREA 1: USER (5 KPIs)
        # ====================================================
        (
            "KPI-USR-01",
            "Total Registered Users",
            "User",
            "Cumulative count of distinct user accounts registered on the platform.",
            "SELECT COUNT(DISTINCT user_id) AS total_registered_users FROM Users_1000_Clean;",
            "user_id",
            "Users_1000_Clean (WB2) / 01_Users_1000 (WB1)",
            "Daily / Real-time",
            "Executive, Growth",
            "Measures gross top-of-funnel customer acquisition reach and total platform member scale.",
            "Upward trend reflects healthy acquisition; flattening curve signals market saturation or acquisition channel fatigue.",
            "Does not measure user quality, retention, or post-registration earning activity; includes completely dormant accounts.",
            "Confirmed calculable"
        ),
        (
            "KPI-USR-02",
            "Email Verification Rate",
            "User",
            "Percentage of registered users who have successfully verified their primary email address.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN email_verification_status = 'Verified' THEN user_id END) / COUNT(DISTINCT user_id) AS email_verification_rate FROM Users_1000_Clean;",
            "user_id, email_verification_status",
            "Users_1000_Clean (WB2)",
            "Daily / Weekly",
            "Trust & Safety, Product",
            "Evaluates account legitimacy, trust tier progression, and contactability for transactional notifications.",
            "High verification (>85%) indicates legitimate user intent; low rate suggests disposable bot signups or verification friction.",
            "Simulated data records status as a static binary state; does not capture OTP delivery latency or email bounce logs.",
            "Confirmed calculable"
        ),
        (
            "KPI-USR-03",
            "Onboarding Completion Rate",
            "User",
            "Percentage of registered users who successfully complete the introductory onboarding orientation.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN onboarding_status = 'Completed' THEN user_id END) / COUNT(DISTINCT user_id) AS onboarding_completion_rate FROM Users_1000_Clean;",
            "user_id, onboarding_status",
            "Users_1000_Clean (WB2)",
            "Daily / Weekly",
            "Product, UX Design",
            "Measures initial tutorial conversion and user orientation success immediately post-signup.",
            "High rate (>70%) demonstrates low UX friction; drop-off highlights tutorial complexity or lack of user motivation.",
            "Tracked only as a coarse profile attribute; micro-step funnel events (onboarding_started, step_completed) are absent in simulated data.",
            "Confirmed calculable"
        ),
        (
            "KPI-USR-04",
            "Account Suspension Rate",
            "User",
            "Percentage of registered users whose accounts have been suspended due to risk or fraud rules.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN account_status = 'Suspended' THEN user_id END) / COUNT(DISTINCT user_id) AS account_suspension_rate FROM Users_1000_Clean;",
            "user_id, account_status",
            "Users_1000_Clean (WB2)",
            "Weekly / Monthly",
            "Risk & Compliance, Trust & Safety",
            "Monitors platform integrity enforcement intensity and the prevalence of abusive or sybil actors.",
            "Spikes indicate bot waves or multi-accounting attacks; very high rates may suggest overly aggressive automated fraud rules.",
            "Reason for suspension (suspension_reason) is absent in simulated data; cannot distinguish emulator detection from click spam.",
            "Confirmed calculable"
        ),
        (
            "KPI-USR-05",
            "User Inactivity Rate (30-day)",
            "User",
            "Percentage of total registered users who logged zero session visits in the preceding 30 days.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN is_active_30d = 'No' THEN user_id END) / COUNT(DISTINCT user_id) AS inactivity_rate_30d FROM Users_1000_Clean;",
            "user_id, is_active_30d",
            "Users_1000_Clean (WB2)",
            "Weekly / Monthly",
            "Lifecycle Marketing, Retention",
            "Quantifies monthly churn and measures the dormant user population requiring re-activation campaigns.",
            "Rising inactivity signals product disengagement, rewards fatigue, or lack of fresh earning inventory.",
            "Derived statically in simulated snapshot; production requires dynamic rolling 30-day event window calculation.",
            "Confirmed calculable"
        ),

        # ====================================================
        # AREA 2: ENGAGEMENT (7 KPIs)
        # ====================================================
        (
            "KPI-ENG-01",
            "Daily Active Users (DAU)",
            "Engagement",
            "Count of distinct qualified users who engage in at least one authenticated session on a given date.",
            "SELECT activity_date, COUNT(DISTINCT user_id) AS dau FROM Daily_Activity WHERE active_flag = 'Yes' GROUP BY activity_date;",
            "user_id, activity_date, active_flag",
            "04_Daily_Activity (WB1)",
            "Daily",
            "Product, Executive, Growth",
            "Primary operational barometer of daily platform traffic, active member scale, and habituation.",
            "Upward trend reflects strong retention and acquisition; downward trend signals engagement decay.",
            "Does not distinguish between brief check-in visits (under 10s) and productive micro-task earning sessions.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-02",
            "Average Session Duration (Seconds)",
            "Engagement",
            "Mean elapsed duration in seconds across all completed user session visits.",
            "SELECT AVG(session_duration_seconds) AS avg_session_duration FROM Sessions WHERE session_status = 'Completed';",
            "session_duration_seconds, session_status",
            "02_Sessions (WB1)",
            "Daily / Weekly",
            "Product, Core UX",
            "Measures user dwell time and depth of visit engagement across product surfaces.",
            "Moderate durations (40-90s) are healthy for micro-task platforms; very long sessions (>300s) may indicate video ad playback bugs.",
            "Capped at 180s in simulated dataset; does not capture backgrounded app dwell time or socket heartbeats.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-03",
            "Sessions per Active User",
            "Engagement",
            "Mean number of session visits initiated per distinct active user on a given day.",
            "SELECT activity_date, SUM(session_count)::FLOAT / COUNT(DISTINCT user_id) AS sessions_per_user FROM Daily_Activity WHERE active_flag = 'Yes' GROUP BY activity_date;",
            "session_count, user_id, activity_date, active_flag",
            "04_Daily_Activity (WB1)",
            "Daily / Weekly",
            "Product, Growth",
            "Measures daily return frequency, session fragmentation, and in-app habit formation.",
            "Higher ratio (>2.0) indicates multiple daily check-ins (e.g. morning spin wheel + evening rewarded video view).",
            "Does not account for sessions unintentionally fragmented by transient mobile cellular disconnects.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-04",
            "Feature Adoption Rate",
            "Engagement",
            "Percentage of total active platform users who have engaged with a specific platform feature.",
            "SELECT feature_name, 100.0 * unique_users / 984.0 AS feature_adoption_rate FROM Feature_Usage;",
            "unique_users, feature_name",
            "07_Feature_Usage (WB1) / 03_Feature_Events (WB1)",
            "Weekly / Monthly",
            "Product Feature Owners",
            "Evaluates user penetration, discovery, and reach for each of the 15 platform functional modules.",
            "Identifies underutilized feature surfaces requiring UX redesign, deeper tutorial onboarding, or higher XP yields.",
            "Measures binary feature participation; does not capture repeat engagement frequency or depth of feature reuse.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-05",
            "7-day Streak Retention Rate",
            "Engagement",
            "Percentage of total registered users who successfully maintain consecutive daily activity through day 7.",
            "SELECT 100.0 * COUNT(DISTINCT user_id) / 1000.0 AS streak_retention_7d FROM Milestones WHERE milestone_type = 'seventh_active_day';",
            "user_id, milestone_type",
            "06_Milestones (WB1) / 01_Users_1000 (WB1)",
            "Weekly / Monthly",
            "Product, Gamification",
            "Measures early-life habituation and conversion of newly acquired users into core retained cohorts.",
            "Strong predictor of 30-day and 90-day LTV; low rate indicates steep drop-off between Day 2 and Day 5.",
            "Milestones table records achievement once; does not track subsequent streak breakages and streak recovery freezes.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-06",
            "Platform Stickiness (DAU/MAU Ratio)",
            "Engagement",
            "Ratio of daily active users to monthly active users, expressing user habituation and retention frequency.",
            "SELECT (40.65 / COUNT(DISTINCT CASE WHEN is_active_30d = 'Yes' THEN user_id END)) * 100.0 AS stickiness_ratio FROM Users_1000_Clean;",
            "user_id, activity_date, is_active_30d",
            "04_Daily_Activity (WB1) / Users_1000_Clean (WB2)",
            "Monthly",
            "Executive, Leadership",
            "Industry-standard benchmark for consumer digital habituation and platform return frequency.",
            ">20% indicates strong daily habit formation; <10% signals low retention and utility-only churn risk.",
            "Requires a stable, mature user population; distorted during rapid burst acquisition phases.",
            "Confirmed calculable"
        ),
        (
            "KPI-ENG-07",
            "Session Bounce Rate",
            "Engagement",
            "Percentage of session visits containing only 1 event or lasting under 10 seconds.",
            "SELECT 100.0 * COUNT(CASE WHEN events_in_session <= 1 OR session_duration_seconds < 10 THEN 1 END) / COUNT(*) AS session_bounce_rate FROM Sessions;",
            "session_id, events_in_session, session_duration_seconds",
            "02_Sessions (WB1)",
            "Daily / Weekly",
            "Product, UX Engineering",
            "Measures immediate user drop-off, accidental app launches, and cold-start UX friction.",
            "High bounce rate points to slow cold-start load times, crash on launch, or misleading notification hooks.",
            "Background OS sync pings or silent notification handlers can occasionally trigger phantom short sessions.",
            "Confirmed calculable"
        ),

        # ====================================================
        # AREA 3: REWARD (6 KPIs)
        # ====================================================
        (
            "KPI-RWD-01",
            "Task Completion Rate",
            "Reward",
            "Percentage of initiated micro-task execution attempts that reach successful completion.",
            "SELECT 100.0 * COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) / COUNT(*) AS task_completion_rate FROM Task_Activity;",
            "activity_id, task_status",
            "05_Task_Activity (WB1)",
            "Daily / Weekly",
            "Operations, Product, Ad Monetization",
            "Primary operational throughput and productivity metric for platform micro-earning mechanisms.",
            "Higher rate indicates accessible tasks and smooth execution; drop indicates technical or partner inventory friction.",
            "Aggregates across heterogeneous task types (30s video vs 15-min survey) without weighting difficulty or duration.",
            "Confirmed calculable"
        ),
        (
            "KPI-RWD-02",
            "Task Failure Rate",
            "Reward",
            "Percentage of initiated task attempts that terminate in explicit technical failure or error.",
            "SELECT 100.0 * COUNT(CASE WHEN task_status = 'Failed' THEN 1 END) / COUNT(*) AS task_failure_rate FROM Task_Activity;",
            "activity_id, task_status",
            "05_Task_Activity (WB1)",
            "Daily / Real-time",
            "Engineering, DevOps, Ad Ops",
            "Monitors technical stability, broken SDK integrations, and third-party provider dropouts.",
            "Spikes indicate ad server downtime, bad creative video assets, or partner survey quota exhaustion.",
            "Does not capture user abandonment prior to clicking 'Start' on the task impression card.",
            "Confirmed calculable"
        ),
        (
            "KPI-RWD-03",
            "Task Abandonment Rate",
            "Reward",
            "Percentage of task attempts voluntarily abandoned by users before meeting completion requirements.",
            "SELECT 100.0 * COUNT(CASE WHEN task_status = 'Abandoned' THEN 1 END) / COUNT(*) AS task_abandonment_rate FROM Task_Activity;",
            "activity_id, task_status",
            "05_Task_Activity (WB1)",
            "Weekly",
            "UX Design, Content",
            "Measures user fatigue, task boredom, excessive duration, or misleading task descriptions.",
            "High abandonment on surveys indicates demographic screen-outs or repetitive question fatigue.",
            "Simulated data records abandonment as a static status without tracking the elapsed execution minute of exit.",
            "Confirmed calculable"
        ),
        (
            "KPI-RWD-04",
            "Reward Credit Volume",
            "Reward",
            "Total count and aggregate point valuation of rewards successfully credited to user accounts.",
            "SELECT COUNT(*) AS total_reward_events, SUM(reward_amount) AS total_xp_issued FROM Reward_Events WHERE status = 'Credited';",
            "reward_amount, reward_status, task_id",
            "05_Task_Activity (WB1) / Wallet_Transactions (er_diagram.dbml)",
            "Daily / Monthly",
            "Finance, Operations",
            "Monitors platform currency issuance velocity and gross virtual point liability creation.",
            "Issuance velocity must correlate with advertising revenue; divergence indicates reward point inflation.",
            "Currency volume in simulated data is partial: task completions lack explicit point values in 05_Task_Activity (counts are confirmed; total fiat valuation is blocked).",
            "Proposed"
        ),
        (
            "KPI-RWD-05",
            "Reward Reversal Rate",
            "Reward",
            "Percentage of previously credited reward points retroactively clawed back due to fraud or chargebacks.",
            "SELECT 100.0 * SUM(CASE WHEN transaction_type = 'REVERSAL' THEN amount END) / SUM(CASE WHEN transaction_type = 'CREDIT' THEN amount END) AS reward_reversal_rate FROM Wallet_Transactions;",
            "transaction_type, amount, status",
            "Wallet_Transactions (er_diagram.dbml)",
            "Weekly / Monthly",
            "Trust & Safety, Finance",
            "Evaluates fraud containment effectiveness, advertiser chargeback leakage, and partner reconciliation adjustments.",
            "Target is <1.0%; higher rates signal affiliate fraud, click-farms, or advertiser callback invalidations.",
            "Blocked. No reversal, clawback, or penalty telemetry exists in supplied simulated workbooks. Requires missing Wallet_Transactions double-entry ledger table.",
            "Blocked"
        ),
        (
            "KPI-RWD-06",
            "Daily Reward Claim Rate",
            "Reward",
            "Percentage of daily active users who claim their daily login check-in reward.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN daily_reward_claimed = 'Yes' THEN user_id END) / COUNT(DISTINCT CASE WHEN active_flag = 'Yes' THEN user_id END) AS daily_claim_rate FROM Daily_Activity;",
            "user_id, daily_reward_claimed, active_flag, activity_date",
            "04_Daily_Activity (WB1)",
            "Daily",
            "Gamification, Product",
            "Monitors user adoption of the baseline zero-friction daily retention check-in hook.",
            "High rate (>80%) indicates strong user awareness; low rate points to poor home screen placement or claim button latency.",
            "Does not record the specific streak tier claimed (e.g. Day 1 base points vs Day 7 multiplier).",
            "Confirmed calculable"
        ),

        # ====================================================
        # AREA 4: WALLET (4 KPIs)
        # ====================================================
        (
            "KPI-WAL-01",
            "Circulating Point Economy (Gross Liability)",
            "Wallet",
            "Total aggregate sum of unredeemed XP points held in user wallets across the platform.",
            "SELECT SUM(xp_balance) AS total_circulating_xp FROM Users_1000_Clean;",
            "xp_balance",
            "Users_1000_Clean (WB2) / Wallet_Transactions (er_diagram.dbml)",
            "Daily / Weekly",
            "Finance, Treasury, Executive",
            "Represents total nominal balance sheet liability owed to users redeemable for cash or vouchers.",
            "Growth must be backed by platform advertising cash reserves; runaway growth without redemptions signals inflation.",
            "In simulated data, only a static snapshot xp_balance is available; time-series historical reconstruction is blocked due to missing Wallet_Transactions ledger.",
            "To Be Verified"
        ),
        (
            "KPI-WAL-02",
            "Point Velocity (Accrual vs Burn Ratio)",
            "Wallet",
            "Ratio of total virtual points earned (issued) to total points redeemed (burned) within a period.",
            "SELECT SUM(CASE WHEN transaction_type = 'CREDIT' THEN amount END) / NULLIF(SUM(CASE WHEN transaction_type = 'DEBIT' THEN amount END), 0) AS point_velocity_ratio FROM Wallet_Transactions;",
            "amount, transaction_type, transaction_datetime",
            "Wallet_Transactions (er_diagram.dbml)",
            "Weekly / Monthly",
            "Finance, Economy Designer",
            "Monitors virtual economy balance; prevents hyper-inflation or deflation in virtual currency.",
            "Healthy ratio is typically 1.2 to 1.5 in growth phases; >3.0 signals lack of compelling cash-out options.",
            "Blocked. Complete absence of transactional Wallet_Transactions double-entry ledger table in supplied data.",
            "Blocked"
        ),
        (
            "KPI-WAL-03",
            "Wallet Screen Inspection Rate",
            "Wallet",
            "Percentage of active users who inspect their wallet balance on a given day.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN wallet_activity = 'Yes' THEN user_id END) / COUNT(DISTINCT CASE WHEN active_flag = 'Yes' THEN user_id END) AS wallet_inspection_rate FROM Daily_Activity;",
            "user_id, wallet_activity, active_flag, activity_date",
            "04_Daily_Activity (WB1)",
            "Daily / Weekly",
            "Product, Core UX",
            "Measures user awareness of their financial earnings, progress toward payout, and cash-out intent.",
            "High inspection rate correlates with withdrawal intent, earning motivation, and trust in platform tracking.",
            "Binary daily flag in simulated data; does not record dwell time or specific sub-screen actions in wallet.",
            "Confirmed calculable"
        ),
        (
            "KPI-WAL-04",
            "Average Wallet Balance per Active User",
            "Wallet",
            "Mean spendable XP balance held by currently active platform users.",
            "SELECT AVG(xp_balance) AS avg_active_user_balance FROM Users_1000_Clean WHERE account_status = 'Active';",
            "xp_balance, account_status",
            "Users_1000_Clean (WB2)",
            "Weekly / Monthly",
            "Finance, Product",
            "Benchmarks user distance from the minimum cash-out withdrawal threshold (e.g. 500 XP = ₹50 INR).",
            "If average balance is well below payout threshold, users may feel progress is too slow, increasing mid-tenure churn.",
            "Skewed by high-earning power user outliers; median wallet balance should be evaluated alongside mean.",
            "Confirmed calculable"
        ),

        # ====================================================
        # AREA 5: WITHDRAWAL (5 KPIs)
        # ====================================================
        (
            "KPI-WDL-01",
            "Withdrawal Completion Rate",
            "Withdrawal",
            "Percentage of submitted cash withdrawal requests that settle successfully into user destination accounts.",
            "SELECT 100.0 * COUNT(CASE WHEN payout_status = 'Completed' THEN 1 END) / COUNT(*) AS withdrawal_completion_rate FROM Withdrawals;",
            "withdrawal_id, payout_status",
            "Withdrawals (er_diagram.dbml)",
            "Daily / Weekly",
            "Operations, Product, Finance",
            "Core health metric for cash disbursement rails and user payout satisfaction.",
            "Target >95%; drop indicates banking rail outages, gateway downtimes, or invalid beneficiary data.",
            "Blocked. Complete absence of Withdrawals table in supplied simulated workbooks.",
            "Blocked"
        ),
        (
            "KPI-WDL-02",
            "Gross Withdrawal Value (GWV in INR)",
            "Withdrawal",
            "Total monetary fiat value in Indian Rupees of all submitted cash withdrawal requests.",
            "SELECT SUM(amount_inr) AS gross_withdrawal_value_inr FROM Withdrawals WHERE requested_datetime >= :start_date;",
            "amount_inr, requested_datetime, withdrawal_id",
            "Withdrawals (er_diagram.dbml)",
            "Daily / Monthly",
            "Finance, Treasury, Executive",
            "Measures cash burn, disbursement liquidity requirements, and payout scale.",
            "Essential for managing payment gateway escrow balances and banking float.",
            "Blocked. Missing Withdrawals transaction records in supplied simulated datasets.",
            "Blocked"
        ),
        (
            "KPI-WDL-03",
            "Average Payout Processing SLA (Hours)",
            "Withdrawal",
            "Mean elapsed hours from user cash-out submission to gateway confirmation of settlement.",
            "SELECT AVG(EXTRACT(EPOCH FROM (completed_at - requested_datetime))/3600.0) AS avg_payout_sla_hours FROM Withdrawals WHERE payout_status = 'Completed';",
            "requested_datetime, completed_at, payout_status",
            "Withdrawals (er_diagram.dbml)",
            "Daily / Weekly",
            "Operations, Product Support",
            "Monitors operational adherence to promised 24-hour payout turnaround SLA.",
            "Lower turnaround increases user trust and word-of-mouth viral growth.",
            "Blocked. Payout timestamps and gateway settlement webhooks are missing in simulated data.",
            "Blocked"
        ),
        (
            "KPI-WDL-04",
            "Withdrawal Rejection Rate",
            "Withdrawal",
            "Percentage of withdrawal requests blocked by risk rules or rejected by payment rails.",
            "SELECT 100.0 * COUNT(CASE WHEN payout_status = 'Rejected' THEN 1 END) / COUNT(*) AS withdrawal_rejection_rate FROM Withdrawals;",
            "withdrawal_id, payout_status, failure_category",
            "Withdrawals (er_diagram.dbml)",
            "Daily / Weekly",
            "Fraud & Risk, Customer Support",
            "Identifies invalid beneficiary VPAs, sybil abuse, and banking rail rejections.",
            "Spike suggests credential stuffing or widespread UPI handle verification failure.",
            "Blocked. Missing Withdrawals table and failure_category telemetry.",
            "Blocked"
        ),
        (
            "KPI-WDL-05",
            "Pending Escrow Payout Liability (INR)",
            "Withdrawal",
            "Total fiat value currently held in Processing state awaiting bank clearance.",
            "SELECT SUM(amount_inr) AS pending_escrow_liability FROM Withdrawals WHERE payout_status = 'Processing';",
            "amount_inr, payout_status",
            "Withdrawals (er_diagram.dbml)",
            "Real-time / Daily",
            "Treasury, Finance",
            "Dictates working capital balance required in aggregator payout accounts.",
            "High backlog indicates gateway processing delays or batch settlement congestion.",
            "Blocked. Missing Withdrawals table.",
            "Blocked"
        ),

        # ====================================================
        # AREA 6: REFERRAL (4 KPIs)
        # ====================================================
        (
            "KPI-REF-01",
            "Inbound Referral Acquisition Share",
            "Referral",
            "Percentage of total registered platform users acquired via viral referral channels.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN acquisition_source = 'Referral' THEN user_id END) / COUNT(DISTINCT user_id) AS referral_share FROM Users_1000_Clean;",
            "user_id, acquisition_source",
            "Users_1000_Clean (WB2) / 01_Users_1000 (WB1)",
            "Weekly / Monthly",
            "Growth, Marketing",
            "Measures organic viral contribution to gross user acquisition.",
            "High share (>20%) lowers blended CAC and demonstrates organic product advocacy.",
            "Confirmed calculable from user table (11.9% in WB2, 15.4% in WB1); but does not show outbound invitations sent.",
            "Confirmed calculable"
        ),
        (
            "KPI-REF-02",
            "Outbound Referral Sharing Rate",
            "Referral",
            "Percentage of active users who generate and share an outbound referral link.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN referral_activity = 'Yes' THEN user_id END) / COUNT(DISTINCT CASE WHEN active_flag = 'Yes' THEN user_id END) AS referral_sharing_rate FROM Daily_Activity;",
            "user_id, referral_activity, active_flag, activity_date",
            "04_Daily_Activity (WB1)",
            "Daily / Weekly",
            "Growth, Product",
            "Measures user propensity to invite peers and participate in the viral acquisition loop.",
            "Higher sharing rate expands top-of-funnel reach; low sharing indicates weak referral incentives.",
            "Measures in-app share button clicks only; outbound delivery success (e.g. WhatsApp opens) is untracked.",
            "Confirmed calculable"
        ),
        (
            "KPI-REF-03",
            "Referral Funnel Conversion Rate (K-factor)",
            "Referral",
            "Percentage of outbound referral invites that convert into commercially qualified earning users (>= 100 XP earned).",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN referral_status = 'Converted' THEN referred_user_id END) / COUNT(DISTINCT referral_id) AS referral_conversion_rate FROM Referrals;",
            "referral_id, referred_user_id, referral_status",
            "Referrals (er_diagram.dbml) / 01_Users_1000",
            "Monthly",
            "Growth, Finance",
            "Validates viral growth loop efficiency, viral coefficient (K-factor), and CAC payback.",
            "Ratio >1.0 represents self-sustaining viral growth; <1.0 requires paid marketing supplements.",
            "Partial/Proposed. Inbound referee share is confirmed, but outbound invite creation and downstream conversion qualification are blocked due to missing Referrals table.",
            "Proposed"
        ),
        (
            "KPI-REF-04",
            "Referral Qualification Drop-off Rate",
            "Referral",
            "Percentage of referred users who register but fail to achieve the 100 XP earning conversion threshold.",
            "SELECT 100.0 * (1.0 - (COUNT(DISTINCT CASE WHEN referral_status = 'Converted' THEN referred_user_id END) / NULLIF(COUNT(DISTINCT CASE WHEN referral_status = 'Registered' THEN referred_user_id END), 0))) AS qualification_dropoff_rate FROM Referrals;",
            "referral_status, referred_user_id",
            "Referrals (er_diagram.dbml)",
            "Monthly",
            "Growth, Product Activation",
            "Quantifies attrition between nominal registration and value-generating conversion (Registration != Conversion).",
            "High drop-off (>80%) suggests bot signups or high early-task friction for invited users.",
            "Blocked. Missing Referrals table in supplied simulated datasets.",
            "Blocked"
        ),

        # ====================================================
        # AREA 7: SUPPORT (3 KPIs)
        # ====================================================
        (
            "KPI-SUP-01",
            "Help Center Penetration Rate",
            "Support",
            "Percentage of active users who visit the Help Center / Support FAQ feature surface.",
            "SELECT 100.0 * COUNT(DISTINCT CASE WHEN feature_name = 'Help Center' THEN user_id END) / COUNT(DISTINCT user_id) AS help_center_penetration FROM Feature_Events;",
            "user_id, feature_name",
            "03_Feature_Events (WB1) / 07_Feature_Usage (WB1)",
            "Weekly / Monthly",
            "Customer Support, UX Operations",
            "Monitors user confusion, navigation difficulties, and demand for self-service assistance.",
            "Rising penetration indicates confusing app updates, delayed rewards, or broken features.",
            "Captures screen view only; does not record specific FAQ article read or ticket submission.",
            "Confirmed calculable"
        ),
        (
            "KPI-SUP-02",
            "Support Ticket Resolution SLA (Hours)",
            "Support",
            "Mean elapsed hours from support inquiry submission to final ticket resolution.",
            "SELECT AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/3600.0) AS avg_ticket_resolution_hours FROM Support_Tickets WHERE status = 'Resolved';",
            "created_at, resolved_at, status",
            "Support_Tickets (er_diagram.dbml / Proposed)",
            "Weekly / Monthly",
            "Customer Support Operations",
            "Evaluates customer service efficiency and dispute resolution responsiveness.",
            "Faster resolution preserves user retention and protects app store review ratings.",
            "Blocked. Support ticketing tables and interaction events are completely absent from the simulated dataset.",
            "Blocked"
        ),
        (
            "KPI-SUP-03",
            "Dispute Rate per 1,000 Completed Tasks",
            "Support",
            "Count of customer support tickets filed disputing uncredited rewards per 1,000 completed micro-tasks.",
            "SELECT (COUNT(ticket_id)::FLOAT / (COUNT(activity_id) / 1000.0)) AS dispute_rate_per_1k_tasks FROM Support_Tickets t JOIN Task_Activity a ON t.task_id = a.task_id WHERE t.category = 'Missing_Reward';",
            "ticket_id, category, task_id, task_status",
            "Support_Tickets (Proposed) / 05_Task_Activity (WB1)",
            "Monthly",
            "Ad Monetization, Customer Support",
            "Tracks partner postback reliability, tracking dropouts, and user reward frustration.",
            "Spikes point to partner postback server outages or aggressive client-side ad blockers.",
            "Blocked. Missing customer support ticketing telemetry.",
            "Blocked"
        )
    ]

    # Verify count
    print(f"Total KPIs defined: {len(kpi_catalog)}")

    # Write headers for Sheet 1
    ws_kpis.append(headers)
    for row_idx, kpi in enumerate(kpi_catalog, start=2):
        ws_kpis.append(list(kpi))

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
        cell = ws_kpis.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for row_idx in range(2, len(kpi_catalog) + 2):
        for col_idx in range(1, len(headers) + 1):
            cell = ws_kpis.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            # Alignment rules
            if col_idx in (1, 3, 8, 9, 13):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in (2, 6, 7):
                cell.alignment = Alignment(horizontal="left", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

            # Highlight status
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

    ws_kpis.freeze_panes = "C2"
    ws_kpis.auto_filter.ref = ws_kpis.dimensions

    col_widths = {
        "A": 14, # KPI ID
        "B": 30, # KPI Name
        "C": 16, # Area
        "D": 45, # Definition
        "E": 45, # Formula
        "F": 30, # Required Fields
        "G": 32, # Data Source
        "H": 18, # Frequency
        "I": 24, # Stakeholder
        "J": 45, # Business Purpose
        "K": 45, # Interpretation
        "L": 45, # Limitation
        "M": 22  # Status
    }
    for col_letter, width in col_widths.items():
        ws_kpis.column_dimensions[col_letter].width = width

    # ----------------------------------------------------
    # Sheet 2: Coverage_By_Area
    # ----------------------------------------------------
    ws_cov = wb.create_sheet(title="Coverage_By_Area")

    # Notes section at top
    notes_text = (
        "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Definitions marked "
        "'Proposed' are design recommendations, and 'Blocked' indicates missing source tables."
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

    # Aggregate area statistics
    area_stats = {}
    for item in kpi_catalog:
        area = item[2]
        status = item[12]
        if area not in area_stats:
            area_stats[area] = {
                "Confirmed calculable": 0,
                "Proposed": 0,
                "To Be Verified": 0,
                "Blocked": 0,
                "Total": 0
            }
        area_stats[area][status] += 1
        area_stats[area]["Total"] += 1

    cov_headers = ["Area", "Confirmed Calculable", "Proposed", "To Be Verified", "Blocked", "Total KPIs", "% Confirmed"]
    start_row = 4
    for col_idx, h in enumerate(cov_headers, start=1):
        cell = ws_cov.cell(row=start_row, column=col_idx)
        cell.value = h
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    curr_row = start_row + 1
    tot_conf = 0
    tot_prop = 0
    tot_tbv = 0
    tot_block = 0
    tot_all = 0

    for area, stats in area_stats.items():
        pct_conf = (stats["Confirmed calculable"] / stats["Total"]) * 100.0
        ws_cov.cell(row=curr_row, column=1, value=area).alignment = Alignment(horizontal="left")
        ws_cov.cell(row=curr_row, column=2, value=stats["Confirmed calculable"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=3, value=stats["Proposed"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=4, value=stats["To Be Verified"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=5, value=stats["Blocked"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=6, value=stats["Total"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=7, value=f"{pct_conf:.1f}%").alignment = Alignment(horizontal="center")

        for c in range(1, 8):
            cell = ws_cov.cell(row=curr_row, column=c)
            cell.font = data_font
            cell.border = border_thin

        tot_conf += stats["Confirmed calculable"]
        tot_prop += stats["Proposed"]
        tot_tbv += stats["To Be Verified"]
        tot_block += stats["Blocked"]
        tot_all += stats["Total"]
        curr_row += 1

    # Total Row
    tot_pct_conf = (tot_conf / tot_all) * 100.0
    ws_cov.cell(row=curr_row, column=1, value="TOTAL ALL AREAS")
    ws_cov.cell(row=curr_row, column=2, value=tot_conf)
    ws_cov.cell(row=curr_row, column=3, value=tot_prop)
    ws_cov.cell(row=curr_row, column=4, value=tot_tbv)
    ws_cov.cell(row=curr_row, column=5, value=tot_block)
    ws_cov.cell(row=curr_row, column=6, value=tot_all)
    ws_cov.cell(row=curr_row, column=7, value=f"{tot_pct_conf:.1f}%")

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

    # Add Summary Ratio Box below
    summary_box_row = curr_row + 2
    ws_cov.cell(row=summary_box_row, column=1, value="Master Feasibility Distribution:")
    ws_cov.cell(row=summary_box_row, column=1).font = Font(name="Calibri", size=11, bold=True)

    ratios = [
        ("Confirmed Calculable (Ready in Current Data)", f"{tot_conf} ({tot_conf/tot_all*100:.1f}%)"),
        ("Blocked (Missing Relational Tables / Telemetry)", f"{tot_block} ({tot_block/tot_all*100:.1f}%)"),
        ("Proposed (Calculable with Partial Aggregates)", f"{tot_prop} ({tot_prop/tot_all*100:.1f}%)"),
        ("To Be Verified (Requires Historical Ledger)", f"{tot_tbv} ({tot_tbv/tot_all*100:.1f}%)")
    ]
    for idx, (label, val_str) in enumerate(ratios, start=1):
        r_idx = summary_box_row + idx
        ws_cov.cell(row=r_idx, column=1, value=label).font = data_font
        ws_cov.cell(row=r_idx, column=2, value=val_str).font = Font(name="Calibri", size=10, bold=True)

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
        "All KPI formulas, feasibility classifications, and metrics in this catalogue derive from simulated testing data. "
        "No actual production company statistics, financial ledgers, or real user counts are represented."
    )
    ws_notice["A4"].font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 85

    output_path = "06_kpis/kpi_catalogue.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path} with {len(kpi_catalog)} KPIs.")

if __name__ == "__main__":
    build_kpi_catalogue()
