#!/usr/bin/env python3
"""
scripts/06_build_tracking_plan.py
Generates 04_events/event_tracking_plan.xlsx with sheets:
1. 'Events' (16 exact columns)
2. 'KPI_Dependencies' (Event Name | KPI(s) it feeds)
3. 'SIMULATED_DATA_NOTICE' (governance notice)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_tracking_plan():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Events
    # ----------------------------------------------------
    ws_events = wb.active
    ws_events.title = "Events"
    
    headers = [
        "Event Name",
        "Trigger",
        "Definition",
        "User ID",
        "Event ID",
        "Timestamp",
        "Feature",
        "Status",
        "Required Properties",
        "Optional Properties",
        "Data Type",
        "Validation",
        "Source",
        "Business Purpose",
        "KPI Dependency",
        "Implementation Status"
    ]
    
    # Event catalog: 32 core requested + 14 confirmed simulated telemetry events = 46 total events
    events_data = [
        # --- Account & Identity ---
        (
            "user_registered",
            "User successfully completes account creation via form or OAuth",
            "Emitted when a new user entity is permanently created in the auth service",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Account Lifecycle",
            "Confirmed",
            '{"registration_method": "string", "source": "string", "platform": "string"}',
            '{"referral_code": "string", "utm_campaign": "string", "utm_source": "string"}',
            "JSON Object",
            "Valid RFC 5322 email; age >= 18; non-null user_id",
            "Auth Service",
            "Measures top-of-funnel customer acquisition, channel efficiency, and sign-up velocity",
            "Total Sign-ups, Customer Acquisition Cost (CAC), Registration-to-Activation Rate",
            "Proposed"
        ),
        (
            "user_logged_in",
            "User successfully authenticates and establishes a valid session token",
            "Emitted upon successful login credential validation or biometric resume",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Account Lifecycle",
            "Confirmed",
            '{"login_method": "string", "session_id": "string", "device_type": "string"}',
            '{"app_version": "string", "ip_address_hash": "string"}',
            "JSON Object",
            "Must resolve to an active account in users master table",
            "Auth Service",
            "Tracks active member return cadence, session frequency, and authentication method",
            "Daily Active Users (DAU), Weekly Active Users (WAU), Monthly Active Users (MAU)",
            "Proposed"
        ),
        (
            "user_logged_out",
            "User taps logout or server session expires after inactivity threshold",
            "Emitted when an active session container is explicitly or passively closed",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Account Lifecycle",
            "Confirmed",
            '{"session_id": "string", "reason": "string", "session_duration_seconds": "integer"}',
            '{"pages_viewed": "integer", "events_in_session": "integer"}',
            "JSON Object",
            "session_duration_seconds >= 0; session_id must match open session",
            "Client SDK / Gateway",
            "Measures session termination disposition and clean visit duration boundaries",
            "Average Session Duration, Bounce Rate",
            "Proposed"
        ),
        (
            "onboarding_started",
            "User lands on the initial screen of the new user tutorial wizard",
            "Emitted when the onboarding tutorial flow is first initiated",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Onboarding",
            "Proposed",
            '{"tutorial_version": "string", "initial_screen": "string"}',
            '{"experiment_variant": "string", "device_locale": "string"}',
            "JSON Object",
            "User must be newly registered with onboarding_status = 'Not Started'",
            "Client SDK (Android/iOS)",
            "Establishes the baseline start of the activation and habituation funnel",
            "Onboarding Funnel Drop-off Rate, Initial Funnel Velocity",
            "Proposed"
        ),
        (
            "onboarding_completed",
            "User completes or explicitly skips the final onboarding tutorial step",
            "Emitted when user finishes orientation, unlocking the full rewards interface",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Onboarding",
            "Proposed",
            '{"completion_type": "string", "steps_viewed": "integer", "duration_seconds": "integer"}',
            '{"welcome_bonus_awarded": "boolean", "permissions_granted": "array"}',
            "JSON Object",
            "completion_type IN ('finished', 'skipped'); steps_viewed >= 1",
            "Client SDK (Android/iOS)",
            "Validates user activation milestone and measures tutorial friction",
            "Onboarding Completion Rate, Day 1 Activation Rate",
            "Proposed"
        ),
        # --- Tasks & Earning ---
        (
            "task_viewed",
            "Task card, banner, or offerwall placement rendered on screen",
            "Emitted when an earning opportunity impression is rendered in user viewport",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Tasks",
            "Confirmed",
            '{"task_id": "string", "task_type": "string", "feature_name": "string"}',
            '{"placement_position": "integer", "reward_xp": "integer", "partner_id": "string"}',
            "JSON Object",
            "task_id must match registered catalog; placement_position >= 1",
            "Client SDK (Android/iOS)",
            "Measures catalog reach, impression inventory, and placement visibility",
            "Task Impression Reach, Task Discovery Click-Through Rate (CTR)",
            "Proposed"
        ),
        (
            "task_opened",
            "User taps task card or offer details to view instructions and reward payout",
            "Emitted when user expands a task modal or navigates to task detail view",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Tasks",
            "Confirmed",
            '{"task_id": "string", "task_type": "string", "feature_name": "string"}',
            '{"reward_xp": "integer", "time_estimate_seconds": "integer", "partner_id": "string"}',
            "JSON Object",
            "task_id must exist in catalog; non-null feature_name",
            "Client SDK (Android/iOS)",
            "Tracks user intent and evaluation behavior prior to committing to task execution",
            "Task Click-Through Rate (CTR), Task Selection Affinity",
            "Proposed"
        ),
        (
            "task_started",
            "User taps start/play/launch button, initiating task execution",
            "Emitted when user actively commences a micro-earning activity",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client/Server UTC ISO-8601)",
            "Tasks",
            "Confirmed",
            '{"task_id": "string", "task_type": "string", "session_id": "string"}',
            '{"partner_campaign_id": "string", "start_time": "string"}',
            "JSON Object",
            "User must have active session; concurrent task limits respected",
            "Client SDK / Task Engine",
            "Establishes task execution baseline to measure completion rates and latency",
            "Task Start Volume, Task Engagement Rate",
            "Proposed"
        ),
        (
            "task_completed",
            "User finishes all required actions for a task (ad watched, survey done)",
            "Emitted when client or partner postback signals successful task completion",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Tasks",
            "Confirmed",
            '{"task_id": "string", "task_type": "string", "duration_seconds": "integer"}',
            '{"reward_amount": "integer", "reward_unit": "string", "validation_status": "string"}',
            "JSON Object",
            "duration_seconds >= 0; reward_amount >= 0",
            "Task Engine / Partner Postback",
            "Primary production metric for user productivity and platform monetization",
            "Task Completion Rate, Earned XP per User, Advertiser Fill Efficiency",
            "Proposed"
        ),
        (
            "task_failed",
            "Task terminates unsuccessfully due to timeout, abandonment, or error",
            "Emitted when a task execution aborts without meeting reward requirements",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Tasks",
            "Confirmed",
            '{"task_id": "string", "task_type": "string", "failure_category": "string"}',
            '{"failure_reason": "string", "duration_before_failure_seconds": "integer"}',
            "JSON Object",
            "failure_category must match standard diagnostic taxonomy",
            "Client SDK / Task Engine",
            "Identifies technical roadblocks, broken partner offers, and UX friction",
            "Task Failure Rate, Technical Error Rate, Advertiser Discrepancy Rate",
            "Proposed"
        ),
        # --- Rewards & Economy ---
        (
            "reward_credited",
            "Task or milestone validation completes; XP ledger entry is posted",
            "Emitted the exact instant XP is permanently credited to user wallet balance",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Rewards",
            "Proposed",
            '{"transaction_id": "string", "reward_amount": "integer", "reward_unit": "string", "source": "string"}',
            '{"balance_after": "float", "task_id": "string", "milestone_id": "string"}',
            "JSON Object",
            "reward_amount > 0; transaction_id must be unique across ledger",
            "Reward Service / Ledger Engine",
            "Records platform reward liability inflow and user earning velocity",
            "Reward Credit Volume, Gross XP Liability Inflow, Average Yield per User",
            "Proposed"
        ),
        (
            "reward_pending",
            "High-value task finished; reward placed in escrow awaiting async validation",
            "Emitted when a reward requires third-party postback reconciliation or fraud check",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Rewards",
            "Proposed",
            '{"hold_id": "string", "expected_amount": "integer", "task_id": "string"}',
            '{"review_deadline": "string", "partner_id": "string"}',
            "JSON Object",
            "expected_amount > 0; review_deadline must be valid future timestamp",
            "Reward Service / Escrow Engine",
            "Monitors pending financial exposure and partner callback turnaround times",
            "Pending Escrow Balance, High-Value Task Hold Duration",
            "Proposed"
        ),
        (
            "reward_reversed",
            "Previously credited reward is clawed back due to fraud or chargeback",
            "Emitted when an offsetting debit entry is posted to negate an illegitimate credit",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Rewards",
            "Proposed",
            '{"reversal_id": "string", "original_transaction_id": "string", "clawback_amount": "integer"}',
            '{"reversal_reason": "string", "balance_after": "float"}',
            "JSON Object",
            "original_transaction_id must exist in ledger; clawback_amount > 0",
            "Audit Engine / Risk Service",
            "Tracks financial integrity, fraud containment efficiency, and chargeback impact",
            "Reward Reversal Rate, Chargeback Rate, Fraud Loss Avoidance",
            "Proposed"
        ),
        # --- Daily Rewards & Retention Mechanics ---
        (
            "daily_reward_claimed",
            "User taps 'Claim' button on the Daily Reward calendar surface",
            "Emitted when a user successfully collects their daily login bonus",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Daily Rewards",
            "Confirmed",
            '{"claim_day": "integer", "reward_amount": "integer", "reward_unit": "string"}',
            '{"streak_length": "integer", "bonus_multiplier": "float"}',
            "JSON Object",
            "claim_day BETWEEN 1 AND 30; reward_amount > 0; max 1 claim per UTC day",
            "Daily Reward Service",
            "Measures daily retention habituation and check-in cadence",
            "Daily Claim Velocity, Day 7 Retention, Habit Stickiness",
            "Exists in simulated data"
        ),
        (
            "streak_updated",
            "User active day count increments or resets following day boundary check",
            "Emitted when user's consecutive active streak counter is recalculated",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Streak",
            "Proposed",
            '{"current_streak": "integer", "previous_streak": "integer", "status": "string"}',
            '{"milestone_reached": "boolean", "streak_freeze_used": "boolean"}',
            "JSON Object",
            "current_streak >= 0; status IN ('incremented', 'reset', 'maintained')",
            "Streak Engine",
            "Tracks habituation persistence and identifies points of churn risk",
            "7-day Streak Retention, Streak Continuity Rate, Habituation Index",
            "Proposed"
        ),
        (
            "mission_started",
            "User unlocks or opts into an active multi-tier milestone mission",
            "Emitted when a user commences participation in a structured mission",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client/Server UTC ISO-8601)",
            "Missions",
            "Confirmed",
            '{"mission_id": "string", "mission_type": "string", "target_requirement": "integer"}',
            '{"reward_xp": "integer", "expiry_timestamp": "string"}',
            "JSON Object",
            "mission_id must exist in active missions table",
            "Missions Service",
            "Monitors user appetite for gamified long-term achievement challenges",
            "Mission Adoption Rate, Multi-Day Engagement Depth",
            "Exists in simulated data"
        ),
        (
            "mission_completed",
            "User reaches all goal criteria specified for an active mission",
            "Emitted upon successful verification of mission milestones",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Missions",
            "Confirmed",
            '{"mission_id": "string", "mission_type": "string", "reward_xp": "integer"}',
            '{"days_to_complete": "integer", "bonus_badge_id": "string"}',
            "JSON Object",
            "days_to_complete >= 0; reward_xp >= 0",
            "Missions Service",
            "Validates user gamification progression and mid-funnel retention",
            "Mission Completion Rate, Tier Progression Velocity",
            "Exists in simulated data"
        ),
        (
            "badge_earned",
            "User fulfills criteria to unlock an achievement status badge",
            "Emitted when a gamification trophy or status tier badge is granted",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Badges",
            "Confirmed",
            '{"badge_id": "string", "badge_name": "string", "badge_tier": "string"}',
            '{"bonus_xp": "integer", "milestone_unlocked": "string"}',
            "JSON Object",
            "badge_id must exist in badges catalog; badge_tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')",
            "Gamification Engine",
            "Measures recognition and non-monetary gamified engagement affinity",
            "Gamification Engagement Depth, Milestone Achievement Rate",
            "Exists in simulated data"
        ),
        (
            "spin_started",
            "User taps spin lever on the Spin & Win lucky wheel surface",
            "Emitted when a wheel spin transaction is initiated",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Spin",
            "Confirmed",
            '{"spin_id": "string", "spin_cost_xp": "integer", "session_id": "string"}',
            '{"is_free_daily_spin": "boolean"}',
            "JSON Object",
            "spin_cost_xp >= 0; user must have adequate balance if not free",
            "Spin Service",
            "Tracks mini-game participation, chance mechanic engagement, and token velocity",
            "Spin Feature Usage Rate, Chance Game Engagement",
            "Exists in simulated data"
        ),
        (
            "spin_completed",
            "Spin animation completes and winning sector prize is determined",
            "Emitted when RNG result resolves and prize is finalized",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Spin",
            "Confirmed",
            '{"spin_id": "string", "prize_type": "string", "prize_value": "integer"}',
            '{"sector_index": "integer", "is_jackpot": "boolean"}',
            "JSON Object",
            "prize_value >= 0; sector_index BETWEEN 0 AND 11",
            "Spin Engine",
            "Audits random prize distribution math and gamified payout sustainability",
            "Spin Completion Rate, Prize Distribution Economics",
            "Exists in simulated data"
        ),
        # --- Referrals & Viral Loops ---
        (
            "referral_created",
            "Referrer generates an outbound invitation link or shares referral code",
            "Emitted when an invitation record is generated in the growth service",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Referrals",
            "Confirmed",
            '{"referral_id": "string", "share_channel": "string", "referral_code": "string"}',
            '{"deep_link_url": "string", "campaign_tag": "string"}',
            "JSON Object",
            "referral_code must match referrer profile; share_channel non-empty",
            "Referral Engine",
            "Measures viral sharing propensity, distribution channels, and top-of-funnel reach",
            "Outbound Viral Invitation Volume, Sharing Channel Share",
            "Exists in simulated data"
        ),
        (
            "referral_registered",
            "Invited referee successfully creates account with referral code",
            "Emitted when an account is created with attribution to an inviting user",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Referrals",
            "Proposed",
            '{"referral_id": "string", "referrer_user_id": "string", "referred_user_id": "string"}',
            '{"channel": "string", "device_type": "string"}',
            "JSON Object",
            "referrer_user_id != referred_user_id (no self-referrals)",
            "Referral Engine / Auth",
            "Tracks inbound viral sign-ups and preliminary attribution link establishment",
            "Inbound Referral Share, Viral Reach",
            "Proposed"
        ),
        (
            "referral_activated",
            "Referred user completes onboarding and engages in first active session",
            "Emitted when a referee reaches basic operational activity hurdles",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Referrals",
            "Proposed",
            '{"referral_id": "string", "referred_user_id": "string", "activation_timestamp": "string"}',
            '{"steps_completed": "integer", "days_to_activate": "float"}',
            "JSON Object",
            "referred_user_id must have valid referral_id in Registered state",
            "Referral Engine",
            "Filters bot traffic from human installs; confirms initial product orientation",
            "Referral Activation Rate, Qualified Referral Funnel",
            "Proposed"
        ),
        (
            "referral_converted",
            "Referee fulfills commercial earning milestone (earns >= 100 XP from tasks)",
            "Emitted when referee meets qualification criteria, triggering bounty disbursement",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Referrals",
            "Proposed",
            '{"referral_id": "string", "referrer_user_id": "string", "bounty_xp": "integer"}',
            '{"referee_lifetime_xp": "integer", "qualification_tasks_count": "integer"}',
            "JSON Object",
            "bounty_xp > 0; referee_lifetime_xp >= 100; qualification_tasks_count >= 3",
            "Referral Engine / Milestone Engine",
            "Critical commercial conversion milestone unlocking dual-sided bounty payout",
            "Referral Conversion Rate, Viral Coefficient (K-factor), Referral CAC",
            "Proposed"
        ),
        # --- Wallet & Financial Ledger ---
        (
            "wallet_transaction_created",
            "Double-entry ledger entry is initiated for credit, debit, or hold",
            "Emitted when a balance mutation request is registered in the financial pipeline",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Wallet",
            "Proposed",
            '{"transaction_id": "string", "transaction_type": "string", "amount": "float", "unit": "string"}',
            '{"source_feature": "string", "reference_id": "string"}',
            "JSON Object",
            "amount > 0.0; transaction_type IN ('CREDIT', 'DEBIT', 'HOLD', 'REVERSAL')",
            "Wallet Service",
            "Ensures strict audit trail for all prospective changes to user currency balance",
            "Ledger Journal Volume, Gross Monetary Flow",
            "Proposed"
        ),
        (
            "wallet_transaction_completed",
            "Ledger entry is successfully committed to immutable double-entry database",
            "Emitted when database commit confirms persistent balance change",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Wallet",
            "Proposed",
            '{"transaction_id": "string", "balance_after": "float", "status": "string"}',
            '{"settled_timestamp": "string", "audit_hash": "string"}',
            "JSON Object",
            "balance_after >= 0.0; transaction_id must be unique across ledger",
            "Ledger Engine",
            "Guarantees financial settlement integrity and zero phantom balances",
            "Net Available Wallet Balance, Circulating Point Economy",
            "Proposed"
        ),
        (
            "wallet_transaction_reversed",
            "Erroneous or fraudulent ledger transaction is cancelled via offsetting entry",
            "Emitted when an offsetting balancing transaction is posted to the ledger",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Wallet",
            "Proposed",
            '{"reversal_transaction_id": "string", "original_transaction_id": "string", "amount": "float"}',
            '{"reason": "string", "authorizer_id": "string"}',
            "JSON Object",
            "original_transaction_id must exist; amount must match original debit/credit",
            "Audit Engine / Finance Service",
            "Monitors financial reconciliation errors, adjustments, and fraud clawbacks",
            "Ledger Discrepancy Rate, Financial Audit Reconciliation",
            "Proposed"
        ),
        # --- Withdrawals & Cash Disbursements ---
        (
            "withdrawal_requested",
            "User submits cash-out request; XP debited from available balance to escrow",
            "Emitted when user initiates a fiat disbursement request (UPI / IMPS / Voucher)",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Withdrawals",
            "Proposed",
            '{"withdrawal_id": "string", "amount_inr": "float", "xp_deducted": "integer", "payout_method": "string"}',
            '{"payout_account_hash": "string", "device_risk_score": "float"}',
            "JSON Object",
            "amount_inr >= 50.0; xp_deducted >= 500; payout_method IN ('UPI_VPA', 'IMPS_BANK', 'VOUCHER')",
            "Payout Service",
            "Tracks user cash-out demand, escrow lock-up, and top-of-funnel payout velocity",
            "Withdrawal Request Volume, Gross Withdrawal Value (GWV), Escrow Liability",
            "Proposed"
        ),
        (
            "withdrawal_processing",
            "Risk checks pass; payout payload dispatched to external payment gateway",
            "Emitted when transaction enters in-flight status with payment aggregator",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Withdrawals",
            "Proposed",
            '{"withdrawal_id": "string", "gateway_name": "string", "dispatched_at": "string"}',
            '{"gateway_batch_id": "string", "sla_target_hours": "integer"}',
            "JSON Object",
            "withdrawal_id must be in Requested state; gateway_name non-empty",
            "Payout Service / Router",
            "Measures internal queuing latency and tracks gateway dispatch throughput",
            "Payout Pipeline Velocity, Fraud Review Queue Time",
            "Proposed"
        ),
        (
            "withdrawal_completed",
            "Payment gateway confirms successful settlement into beneficiary account",
            "Emitted upon receipt of signed webhook confirming cash deposit",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Withdrawals",
            "Proposed",
            '{"withdrawal_id": "string", "amount_inr": "float", "gateway_reference": "string"}',
            '{"processing_duration_seconds": "integer", "completed_at": "string"}',
            "JSON Object",
            "gateway_reference non-empty; processing_duration_seconds >= 0",
            "Gateway Webhook Receiver",
            "Validates successful financial settlement and adherence to user SLA",
            "Withdrawal Completion Rate, Average Processing SLA, Net Settled Cash Outflow",
            "Proposed"
        ),
        (
            "withdrawal_rejected",
            "Payout blocked by anti-fraud engine or rejected by banking rail",
            "Emitted when a cash-out attempt fails; escrowed XP returned to available balance",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Withdrawals",
            "Proposed",
            '{"withdrawal_id": "string", "failure_category": "string", "failure_reason": "string"}',
            '{"rejection_source": "string", "xp_refunded": "integer"}',
            "JSON Object",
            "failure_category must match standard error list; xp_refunded must equal xp_deducted",
            "Risk Engine / Gateway Receiver",
            "Identifies invalid beneficiary accounts, fraud attempts, and bank rejections",
            "Withdrawal Rejection Rate, Beneficiary Validation Failure Rate",
            "Proposed"
        ),
        (
            "withdrawal_reversed",
            "Bank retroactively rejects or recalls previously acknowledged transfer",
            "Emitted when a settled payout is returned by destination clearing house",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Withdrawals",
            "Proposed",
            '{"withdrawal_id": "string", "gateway_reference": "string", "reversal_amount_inr": "float"}',
            '{"bank_return_code": "string", "reversal_timestamp": "string"}',
            "JSON Object",
            "withdrawal_id must be in Completed state; reversal_amount_inr > 0.0",
            "Gateway Reconciler",
            "Detects edge-case banking rail reversals requiring financial clawback",
            "Withdrawal Reversal Rate, Banking Rail Failure Rate",
            "Proposed"
        ),
        # --- Additional Verified Events from Simulated Telemetry ---
        (
            "daily_reward_viewed",
            "User navigates to Daily Reward calendar screen",
            "Emitted when the daily reward check-in interface is opened",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Daily Rewards",
            "Confirmed",
            '{"screen_name": "string", "session_id": "string"}',
            '{"current_streak": "integer"}',
            "JSON Object",
            "session_id must match active session",
            "Client SDK (Android/iOS)",
            "Measures discovery and screen penetration for daily retention mechanic",
            "Daily Reward Screen Penetration, View-to-Claim Conversion",
            "Exists in simulated data"
        ),
        (
            "streak_claimed",
            "User claims milestone bonus for maintaining consecutive active days",
            "Emitted when a milestone streak reward is collected",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Streak",
            "Confirmed",
            '{"streak_days": "integer", "reward_xp": "integer"}',
            '{"milestone_tier": "string"}',
            "JSON Object",
            "streak_days >= 3; reward_xp > 0",
            "Streak Engine",
            "Tracks milestone streak achievement and reward claim velocity",
            "Streak Milestone Claim Rate, 7-day Retention",
            "Exists in simulated data"
        ),
        (
            "streak_broken",
            "User fails to log in within daily grace window; streak resets to zero",
            "Emitted when streak engine detects broken login continuity",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Streak",
            "Confirmed",
            '{"broken_streak_length": "integer", "last_active_date": "string"}',
            '{"days_missed": "integer"}',
            "JSON Object",
            "broken_streak_length >= 1",
            "Streak Engine",
            "Measures habituation breakage points and triggers re-engagement campaigns",
            "Streak Drop-off Rate, Churn Early Warning Indicator",
            "Exists in simulated data"
        ),
        (
            "streak_viewed",
            "User views their current streak counter on home or profile screen",
            "Emitted when streak visual progress card is rendered",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Streak",
            "Confirmed",
            '{"streak_count": "integer", "next_milestone_days": "integer"}',
            '{"session_id": "string"}',
            "JSON Object",
            "streak_count >= 0",
            "Client SDK (Android/iOS)",
            "Tracks visibility and user awareness of habituation mechanics",
            "Streak Card View Rate",
            "Exists in simulated data"
        ),
        (
            "ad_started",
            "Rewarded video ad creative begins playback on client player",
            "Emitted when video playback starts following mediation ad load",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Watch Ads / Offers",
            "Confirmed",
            '{"ad_network": "string", "ad_unit_id": "string", "placement": "string"}',
            '{"creative_id": "string", "ecpm_floor": "float"}',
            "JSON Object",
            "ad_network IN ('AdMob', 'Unity', 'AppLovin', 'IronSource')",
            "Ad Mediation SDK",
            "Measures ad demand, SDK playback latency, and initial view starts",
            "Ad Start Volume, Ad Fill Rate",
            "Exists in simulated data"
        ),
        (
            "ad_completed",
            "User watches full duration of rewarded video ad creative",
            "Emitted when video player reaches terminal playback threshold",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Watch Ads / Offers",
            "Confirmed",
            '{"ad_network": "string", "ad_duration_seconds": "integer", "reward_granted": "boolean"}',
            '{"creative_id": "string", "ecpm": "float"}',
            "JSON Object",
            "ad_duration_seconds >= 5; reward_granted == True",
            "Ad Mediation SDK",
            "Primary billable event driving mobile advertising monetization",
            "Video Completion Rate (VCR), Ad Revenue per User (ARPU)",
            "Exists in simulated data"
        ),
        (
            "ad_skipped",
            "User taps close/skip button before rewarded video threshold is met",
            "Emitted when user abandons video ad playback prematurely",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Watch Ads / Offers",
            "Confirmed",
            '{"ad_network": "string", "watched_seconds": "integer", "total_seconds": "integer"}',
            '{"creative_id": "string"}',
            "JSON Object",
            "watched_seconds < total_seconds",
            "Ad Mediation SDK",
            "Measures creative fatigue, UX friction, and lost revenue opportunities",
            "Ad Abandonment Rate, User Creative Fatigue",
            "Exists in simulated data"
        ),
        (
            "tap_started",
            "User enters Tap & Earn interactive mini-game session",
            "Emitted when user opens tap game interface and begins clicking",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Tap & Earn",
            "Confirmed",
            '{"game_mode": "string", "energy_level": "integer"}',
            '{"session_id": "string"}',
            "JSON Object",
            "energy_level >= 0",
            "Client SDK (Android/iOS)",
            "Tracks micro-engagement participation in active tapping mechanics",
            "Tap & Earn Participation Rate",
            "Exists in simulated data"
        ),
        (
            "tap_completed",
            "User finishes tap game round and claims collected points",
            "Emitted when tap round concludes and points are aggregated",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client/Server UTC ISO-8601)",
            "Tap & Earn",
            "Confirmed",
            '{"taps_count": "integer", "points_earned": "integer", "duration_seconds": "integer"}',
            '{"multiplier": "float"}',
            "JSON Object",
            "taps_count >= 0; points_earned >= 0",
            "Tap Game Engine",
            "Measures user engagement intensity and anti-autoclicker velocity",
            "Taps per Session, Tap Earning Efficiency",
            "Exists in simulated data"
        ),
        (
            "mining_started",
            "User activates a passive cloud mining or simulated mining session",
            "Emitted when user taps 'Start Mining' to begin a timed earning cycle",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Mining",
            "Confirmed",
            '{"cycle_duration_hours": "integer", "hash_rate": "float"}',
            '{"boost_active": "boolean"}',
            "JSON Object",
            "cycle_duration_hours IN (4, 8, 12, 24); hash_rate > 0.0",
            "Mining Service",
            "Tracks activation of passive retention hooks and mining stickiness",
            "Mining Adoption Rate, Active Mining Sessions",
            "Exists in simulated data"
        ),
        (
            "mining_stopped",
            "Mining cycle timer expires or user claims accumulated mining tokens",
            "Emitted when mining session finishes and output is ready for harvest",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Server UTC ISO-8601)",
            "Mining",
            "Confirmed",
            '{"tokens_mined": "float", "actual_duration_hours": "float", "claimed": "boolean"}',
            '{"boost_multiplier": "float"}',
            "JSON Object",
            "tokens_mined >= 0.0; actual_duration_hours >= 0.0",
            "Mining Service",
            "Measures completion rate of mining cycles and token generation economics",
            "Mining Completion Rate, Harvest Frequency",
            "Exists in simulated data"
        ),
        (
            "wallet_viewed",
            "User navigates to Wallet screen to inspect balance and transaction history",
            "Emitted when wallet overview surface is rendered in user viewport",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Wallet",
            "Confirmed",
            '{"screen_name": "string", "session_id": "string"}',
            '{"displayed_balance": "float"}',
            "JSON Object",
            "session_id must match active session",
            "Client SDK (Android/iOS)",
            "Measures user interest in their accumulated earnings and liquidity status",
            "Wallet Screen View Rate, Balance Inspection Velocity",
            "Exists in simulated data"
        ),
        (
            "exchange_viewed",
            "User opens token exchange / conversion screen",
            "Emitted when token swap or exchange interface is loaded",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Exchange",
            "Confirmed",
            '{"screen_name": "string", "session_id": "string"}',
            '{"exchange_rate": "float"}',
            "JSON Object",
            "session_id must match active session",
            "Client SDK (Android/iOS)",
            "Measures interest in converting internal gaming tokens into spendable XP",
            "Exchange Feature Adoption Rate",
            "Exists in simulated data"
        ),
        (
            "leaderboard_viewed",
            "User views the community leaderboard / ranking screen",
            "Emitted when top earner or streak rankings are rendered",
            "Required (VLUSR / UUID)",
            "Required (EVT_UUIDv4)",
            "Required (Client UTC ISO-8601)",
            "Leaderboard",
            "Confirmed",
            '{"leaderboard_type": "string", "user_rank": "integer"}',
            '{"session_id": "string"}',
            "JSON Object",
            "leaderboard_type IN ('weekly_xp', 'daily_streak', 'all_time'); user_rank >= 1",
            "Client SDK (Android/iOS)",
            "Tracks social comparison and competitive gamification engagement",
            "Leaderboard Engagement Depth",
            "Exists in simulated data"
        )
    ]
    
    # Write headers for Sheet 1
    ws_events.append(headers)
    for row_idx, event in enumerate(events_data, start=2):
        ws_events.append(list(event))
        
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
        cell = ws_events.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for row_idx in range(2, len(events_data) + 2):
        for col_idx in range(1, len(headers) + 1):
            cell = ws_events.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            # Alignment rules
            if col_idx in (1, 7, 8, 11, 13, 16):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in (9, 10):
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                
            # Highlight implementation status
            if col_idx == 16:
                val = str(cell.value)
                if val == "Exists in simulated data":
                    cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # soft green
                    cell.font = Font(name="Calibri", size=10, bold=True, color="375623")
                elif val == "Proposed":
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # soft yellow
                    cell.font = Font(name="Calibri", size=10, bold=True, color="7F6000")
                elif val == "To Be Verified":
                    cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # soft orange
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C65911")

    ws_events.freeze_panes = "A2"
    ws_events.auto_filter.ref = ws_events.dimensions
    
    # ----------------------------------------------------
    # Sheet 2: KPI_Dependencies
    # ----------------------------------------------------
    ws_kpi = wb.create_sheet(title="KPI_Dependencies")
    kpi_headers = ["Event Name", "KPI(s) it feeds"]
    ws_kpi.append(kpi_headers)
    
    for col_idx in range(1, 3):
        cell = ws_kpi.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for row_idx, event in enumerate(events_data, start=2):
        ws_kpi.append([event[0], event[14]]) # Event Name and KPI Dependency
        cell_name = ws_kpi.cell(row=row_idx, column=1)
        cell_kpi = ws_kpi.cell(row=row_idx, column=2)
        cell_name.font = data_font
        cell_name.border = border_thin
        cell_name.alignment = Alignment(horizontal="center", vertical="top")
        cell_kpi.font = data_font
        cell_kpi.border = border_thin
        cell_kpi.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws_kpi.freeze_panes = "A2"
    ws_kpi.auto_filter.ref = ws_kpi.dimensions

    # ----------------------------------------------------
    # Sheet 3: SIMULATED_DATA_NOTICE
    # ----------------------------------------------------
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    notice_text = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."
    ws_notice["A1"] = notice_text
    ws_notice["A1"].font = Font(name="Calibri", size=14, bold=True, color="C00000")
    ws_notice["A3"] = "Notice Details:"
    ws_notice["A3"].font = Font(name="Calibri", size=11, bold=True)
    ws_notice["A4"] = "This tracking plan documents both simulated telemetry events present in the test workbooks and proposed events required for full production architecture. All event counts and schema validations derive from simulated testing data."
    ws_notice["A4"].font = Font(name="Calibri", size=10)

    # Auto-adjust column widths for all sheets
    for ws in [ws_events, ws_kpi]:
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = 0
            for cell in col:
                val_str = str(cell.value or "")
                # If wrapped text or json, clamp measurement length
                line_len = max([len(line) for line in val_str.split("\n")]) if val_str else 0
                if line_len > max_len:
                    max_len = line_len
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 45)
            
    ws_notice.column_dimensions["A"].width = 80
    
    output_path = "04_events/event_tracking_plan.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path} with {len(events_data)} events.")

if __name__ == "__main__":
    build_tracking_plan()
