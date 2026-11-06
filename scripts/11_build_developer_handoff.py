#!/usr/bin/env python3
"""
scripts/11_build_developer_handoff.py
Generates 09_engineering/developer_analytics_handoff.xlsx with sheets:
1. 'Events' (15 exact columns, field-level granularity across 15 high-priority events)
2. 'Acceptance_Tests' (Requirement ID | Given | When | Then)
3. 'SIMULATED_DATA_NOTICE' (governance notice)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_developer_handoff():
    wb = openpyxl.Workbook()

    # ----------------------------------------------------
    # Sheet 1: Events
    # ----------------------------------------------------
    ws_events = wb.active
    ws_events.title = "Events"

    headers = [
        "Requirement ID",
        "Event",
        "Trigger",
        "Payload Fields",
        "Field",
        "Data Type",
        "Required",
        "Validation",
        "Deduplication",
        "Timestamp",
        "Source",
        "Why Needed",
        "KPI Dependency",
        "Acceptance Test",
        "Priority"
    ]

    # Define the 15 highest-priority events with field-level granularity
    # Every field traces directly to data_dictionary.xlsx
    events_spec = [
        # ====================================================
        # 1. user_registered (High)
        # ====================================================
        {
            "event": "user_registered",
            "trigger": "User successfully submits registration form or completes OAuth verification.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, registration_datetime); enforced at Ingestion Gateway via Redis 24h TTL cache and DB unique index on email.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Auth Service Gateway",
            "kpi": "Total Registered Users (KPI-USR-01), CAC by Channel, Registration-to-Activation Rate",
            "acceptance": "Given an unauthenticated visitor, when valid registration form/OAuth is submitted, then exactly one user_registered row is recorded with fields (event_id, user_id, timestamp, account_created_via, acquisition_source, primary_device, platform) and no duplicates for the same (user_id, email).",
            "given": "An anonymous user on the registration surface with valid unallocated credentials.",
            "when": "The user submits valid signup credentials or Google OAuth authentication.",
            "then": "Exactly one user_registered event is emitted and ingested with valid user_id and no duplicate records for the same email address.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Prefix VLUSR + 6 digits; unique non-null", "Persistent master account entity identifier across all behavioral tables."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp; monotonic", "Baseline registration timestamp for cohort tenure and retention curves."),
                ("account_created_via", "Categorical", "Yes", "Controlled list: Web Registration, Google Sign-In, Phone OTP", "Tracks authentication provider mix and frictionless credential-less signup adoption."),
                ("acquisition_source", "Categorical", "Yes", "Controlled list: Organic Search, Direct, Social Media, Referral, WhatsApp, Telegram, Other", "Primary marketing channel attribution for CAC and blended acquisition efficiency."),
                ("referral_code", "String", "Conditional", "Format VL + 6 hex characters; required if acquired via referral", "Outbound viral code linking referee to inviting referrer."),
                ("primary_device", "Categorical", "Yes", "Controlled list: Android, iOS, Windows, macOS", "Hardware OS environment used to benchmark platform stability."),
                ("platform", "Categorical", "Yes", "Controlled list: Android Native, iOS Native, Web", "Client build framework used for release health and cross-platform benchmarking.")
            ]
        },

        # ====================================================
        # 2. user_logged_in (High)
        # ====================================================
        {
            "event": "user_logged_in",
            "trigger": "User authenticates successfully and obtains a valid JWT session token.",
            "priority": "High",
            "dedupe": "Idempotency key: session_id; enforced at Session Manager Ingress via Redis session registry.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Auth Service / Session Gateway",
            "kpi": "Daily Active Users (KPI-ENG-01), Help Center Penetration Rate (KPI-SUP-01), Sessions per Active User (KPI-ENG-03), Session Bounce Rate (KPI-ENG-07)",
            "acceptance": "Given a registered user, when valid credentials or biometric resume is submitted, then exactly one user_logged_in row is recorded with fields (event_id, user_id, session_id, timestamp, device, platform) and no duplicate for the same session_id.",
            "given": "A registered user with account_status in ('Active', 'Pending Verification').",
            "when": "The user enters valid credentials or resumes an expired session via biometric token.",
            "then": "Exactly one user_logged_in event is emitted with a newly issued session_id container and authenticated user_id.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Must resolve to active user in master DB", "Associates session visit to user profile and cohort history."),
                ("session_id", "String", "Yes", "Prefix SESS_ + UUIDv4; unique non-null", "Visit container identifier tracking user dwell and app focus boundaries."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp", "Timestamp mark of session commencement for diurnal curve tracking."),
                ("device", "Categorical", "Yes", "Controlled list: Android, iOS, Web", "Operating system used during session visit."),
                ("platform", "Categorical", "Yes", "Controlled list: Android Native, iOS Native, Web", "Build framework for cross-platform session duration comparisons."),
                ("entry_point", "Categorical", "Yes", "Controlled list of 15 features (e.g. Home, Daily Reward, Tasks)", "Deep link or landing surface where user initiated engagement.")
            ]
        },

        # ====================================================
        # 3. onboarding_completed (High)
        # ====================================================
        {
            "event": "onboarding_completed",
            "trigger": "User finishes or explicitly skips the final onboarding tutorial step.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, 'onboarding_completed'); enforced at User Profile State Service (at-most-once per user).",
            "timestamp": "Client / Server UTC ISO-8601",
            "source": "Client Telemetry SDK (Android/iOS)",
            "kpi": "Onboarding Completion Rate (KPI-USR-03), Day 1 Activation Rate",
            "acceptance": "Given a user with onboarding_status = 'Started', when user finishes/skips tutorial, then exactly one onboarding_completed row is recorded with fields (event_id, user_id, session_id, completion_type, duration_seconds) and no duplicates for the same user_id.",
            "given": "A newly registered user currently active in the onboarding tutorial wizard.",
            "when": "The user taps 'Complete' on the final screen or taps 'Skip Orientation'.",
            "then": "Exactly one onboarding_completed event is logged, updating the user profile onboarding_status to 'Completed'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "Identifies user clearing initial product orientation hurdles."),
                ("session_id", "String", "Yes", "Must match active visit session container", "Links tutorial completion to initial installation session."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp", "Milestone timestamp for time-to-onboard latency calculation."),
                ("onboarding_status", "Categorical", "Yes", "Fixed value: 'Completed'", "Updates user master profile state from Started to Completed."),
                ("duration_seconds", "Integer", "Yes", "Integer >= 0; elapsed tutorial duration", "Measures UX friction and dwell time on introductory onboarding wizard.")
            ]
        },

        # ====================================================
        # 4. task_started (High)
        # ====================================================
        {
            "event": "task_started",
            "trigger": "User taps 'Start', 'Play', or 'Launch' on an earning task modal.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, task_id, session_id, start_time); enforced at Task Ingress Gateway within 60s sliding window.",
            "timestamp": "Client / Server UTC ISO-8601",
            "source": "Client SDK / Task Engine",
            "kpi": "Task Start Volume, Task Engagement Rate, Task Completion Rate (KPI-RWD-01)",
            "acceptance": "Given a user on a task detail card, when user initiates execution, then exactly one task_started row is recorded with fields (event_id, user_id, session_id, task_id, task_type, feature_name) and no duplicates within 60s.",
            "given": "An active user with valid session inspecting available tasks in task catalog.",
            "when": "The user clicks the start action button to launch an ad, survey, or micro-game.",
            "then": "Exactly one task_started event is recorded, initializing an active execution record with task_status = 'Started'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User initiating micro-earning task attempt."),
                ("session_id", "String", "Yes", "Must match active visit container", "Visit context tracking concurrency and task sequence."),
                ("task_id", "String", "Yes", "Format TASK + 4 digits (TASK0001 - TASK0080)", "Foreign key referencing task definition in Task_Master catalog."),
                ("task_category", "Categorical", "Yes", "Controlled list matching product taxonomy", "Functional earning type (Watch Ads / Offers, Spin, Tap & Earn, Mining)."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp", "Execution start timestamp marking beginning of duration measurement.")
            ]
        },

        # ====================================================
        # 5. task_completed (High)
        # ====================================================
        {
            "event": "task_completed",
            "trigger": "Client video completes or partner S2S postback confirms task fulfillment.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, task_id, activity_id); enforced at Task Verification Engine.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Task Verification Engine / S2S Receiver",
            "kpi": "Task Completion Rate (KPI-RWD-01), Earned XP per User, Advertiser Fill Efficiency",
            "acceptance": "Given an active task execution record, when completion requirements are verified, then exactly one task_completed row is recorded with fields (event_id, activity_id, user_id, task_id, duration_seconds, reward_status) and no duplicate for the same activity_id.",
            "given": "A task execution record in 'Started' state.",
            "when": "Client reports video creative completed or partner sends verified postback.",
            "then": "Exactly one task_completed event is emitted, updating Task_Activity status to 'Completed' and triggering reward validation.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("activity_id", "String", "Yes", "Prefix ACT + 7 digits (ACT0000001 - ACT0009846)", "Unique execution attempt primary key linking start to completion."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User earning reward upon task fulfillment."),
                ("session_id", "String", "Yes", "Must match active session container", "Session visit context for task completion."),
                ("task_id", "String", "Yes", "Must match task started", "Identifies specific task completed from catalog."),
                ("duration_seconds", "Integer", "Yes", "Integer >= 0; elapsed execution duration", "Total elapsed seconds from task start to completion."),
                ("reward_status", "Categorical", "Yes", "Controlled list: Credited, Pending", "Immediate settlement disposition of earned reward points.")
            ]
        },

        # ====================================================
        # 6. task_failed (High)
        # ====================================================
        {
            "event": "task_failed",
            "trigger": "Task execution aborts due to client timeout, network drop, or partner rejection.",
            "priority": "High",
            "dedupe": "Idempotency key: (activity_id, failure_category); enforced at Error Logging Gateway.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Client SDK / Error Handler",
            "kpi": "Task Failure Rate (KPI-RWD-02), Dispute Rate per 1,000 Completed Tasks (KPI-SUP-03), Technical Error Rate",
            "acceptance": "Given an active task execution record, when execution encounters fatal error or user aborts, then exactly one task_failed row is recorded with fields (event_id, activity_id, user_id, task_id, failure_reason) and no duplicate for the same activity_id.",
            "given": "A task execution record currently in progress.",
            "when": "The video player crashes, network stream drops, or user closes ad prematurely.",
            "then": "Exactly one task_failed event is emitted with diagnostic failure_reason and task_status set to 'Failed'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("activity_id", "String", "Yes", "Prefix ACT + 7 digits", "Unique execution attempt primary key."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User whose task execution failed."),
                ("task_id", "String", "Yes", "Must match task started", "Identifies failing task item from catalog."),
                ("failure_reason", "Categorical", "Yes", "Controlled list: User Abandoned, Network Disconnect, Ad Skip, Timeout", "Diagnostic root cause categorizing non-completion reason."),
                ("duration_seconds", "Integer", "Yes", "Integer >= 0; elapsed duration before failure", "Seconds elapsed before task was abandoned or crashed.")
            ]
        },

        # ====================================================
        # 7. daily_reward_claimed (High)
        # ====================================================
        {
            "event": "daily_reward_claimed",
            "trigger": "User taps 'Claim' button on the Daily Reward calendar surface.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, activity_date); enforced at Daily Reward DB unique constraint (max 1 claim per UTC day).",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Daily Reward Service Engine",
            "kpi": "Daily Reward Claim Rate (KPI-RWD-06), 7-day Streak Retention (KPI-ENG-05)",
            "acceptance": "Given an active user with unclaimed daily reward, when user taps Claim, then exactly one daily_reward_claimed row is recorded with fields (event_id, user_id, activity_date, claim_day, reward_amount) and no duplicates for the same (user_id, activity_date).",
            "given": "An authenticated user with daily_reward_claimed = 'No' on the current calendar date.",
            "when": "The user taps the 'Claim Daily Bonus' button on the daily check-in surface.",
            "then": "Exactly one daily_reward_claimed event is committed, locking the claim date and crediting bonus XP to wallet.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User claiming daily retention check-in reward."),
                ("session_id", "String", "Yes", "Must match active visit container", "Visit context tracking claim surface."),
                ("activity_date", "Date", "Yes", "ISO-8601 date string (YYYY-MM-DD)", "Calendar date partition enforcing max 1 claim per UTC day."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp", "Server timestamp when claim transaction occurred."),
                ("streak_activity", "Categorical", "Yes", "Controlled list: Yes, No", "Indicates whether consecutive daily login streak was maintained.")
            ]
        },

        # ====================================================
        # 8. reward_credited (Critical)
        # ====================================================
        {
            "event": "reward_credited",
            "trigger": "Validation engine clears task/milestone; XP balance committed to wallet ledger.",
            "priority": "Critical",
            "dedupe": "Idempotency key: transaction_id; enforced at Wallet Ledger DB unique primary key constraint.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Wallet Service / Ledger Engine",
            "kpi": "Reward Credit Volume (KPI-RWD-04), Gross XP Liability Inflow, Circulating Point Economy (KPI-WAL-01)",
            "acceptance": "Given a verified task completion or milestone unlock, when credit ledger posting commits, then exactly one reward_credited row is recorded with fields (event_id, transaction_id, user_id, amount, unit, balance_after) and no duplicate for the same transaction_id.",
            "given": "A validated task completion or milestone achievement awaiting credit settlement.",
            "when": "The reward engine commits a positive balance mutation to the double-entry database.",
            "then": "Exactly one reward_credited event is emitted with immutable transaction_id and updated running balance.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("transaction_id", "String", "Yes", "Format TXN_ + UUIDv4; unique non-null", "Immutable primary key of double-entry ledger journal entry."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "Beneficiary user account receiving points credit."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Exact moment virtual point liability was committed."),
                ("amount", "Float", "Yes", "Float > 0.0; strictly positive magnitude", "Number of virtual XP points permanently credited."),
                ("unit", "Categorical", "Yes", "Controlled list: XP, INR (Default: XP)", "Currency denomination of credited reward."),
                ("source_feature", "Categorical", "Yes", "Controlled list of 15 features (e.g. Watch Ads, Daily Reward)", "Upstream product module driving the earning transaction."),
                ("reference_id", "String", "Yes", "Matches activity_id, milestone_id, or task_id", "Originating foreign key linking credit to verifiable event."),
                ("balance_after", "Float", "Yes", "Float >= 0.0; running total post-credit", "Snapshot balance immediately after ledger posting.")
            ]
        },

        # ====================================================
        # 9. reward_pending (High)
        # ====================================================
        {
            "event": "reward_pending",
            "trigger": "High-value task completed; reward placed into escrow awaiting async S2S validation.",
            "priority": "High",
            "dedupe": "Idempotency key: (user_id, reference_id); enforced at Escrow Engine via Redis lock.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Reward Service / Escrow Engine",
            "kpi": "Pending Escrow Balance, High-Value Task Hold Duration",
            "acceptance": "Given a completed high-value survey or offerwall task, when client reports completion, then exactly one reward_pending row is recorded with fields (event_id, user_id, task_id, reference_id, amount) and points remain in escrow until postback.",
            "given": "A user completing an offerwall task requiring third-party S2S callback confirmation.",
            "when": "The client app finishes task execution but third-party callback has not yet arrived.",
            "then": "Exactly one reward_pending event is emitted, holding points in escrow without mutating spendable balance.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User awaiting asynchronous reward verification."),
                ("task_id", "String", "Yes", "Must match task from catalog", "High-value task requiring extended validation window."),
                ("reference_id", "String", "Yes", "Prefix ACT + 7 digits (activity_id)", "Execution record link placed under escrow review."),
                ("amount", "Float", "Yes", "Float > 0.0; expected reward payout", "Magnitude of points queued in pending escrow state."),
                ("timestamp", "Datetime", "Yes", "Valid ISO-8601 UTC timestamp", "Timestamp when pending hold window commenced.")
            ]
        },

        # ====================================================
        # 10. reward_reversed (Critical)
        # ====================================================
        {
            "event": "reward_reversed",
            "trigger": "Post-audit fraud engine flags click-farm or partner issues billing chargeback.",
            "priority": "Critical",
            "dedupe": "Idempotency key: reversal_link; enforced at Audit Engine DB unique constraint.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Anti-Fraud Engine / Finance Audit",
            "kpi": "Reward Reversal Rate (KPI-RWD-05), Chargeback Rate, Fraud Loss Avoidance",
            "acceptance": "Given a previously credited transaction, when fraud/chargeback is confirmed, then exactly one reward_reversed row is recorded with fields (event_id, transaction_id, reversal_link, user_id, amount) and spendable balance is debited by amount.",
            "given": "A user account with historical credited transactions identified as fraudulent.",
            "when": "Risk engine executes clawback protocol or advertiser files billing dispute.",
            "then": "Exactly one reward_reversed event is committed, posting an offsetting negative ledger entry referencing original TXN.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("transaction_id", "String", "Yes", "Format TXN_ + UUIDv4; new reversal record key", "Unique primary key of offsetting ledger reversal entry."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User account subjected to point clawback."),
                ("reversal_link", "String", "Yes", "Must match an existing historical transaction_id", "Pointer linking reversal to original illegitimate credit entry."),
                ("amount", "Float", "Yes", "Float > 0.0; matching original credit amount", "Magnitude of virtual points debited from balance."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Timestamp when clawback entry was committed."),
                ("failure_reason", "Categorical", "Yes", "Controlled list: Fraud Suspected, Chargeback, Duplicate Credit", "Audit justification code authorizing point clawback.")
            ]
        },

        # ====================================================
        # 11. wallet_transaction_created (Critical)
        # ====================================================
        {
            "event": "wallet_transaction_created",
            "trigger": "A balance mutation intent (credit, debit, hold) is registered in the financial pipeline.",
            "priority": "Critical",
            "dedupe": "Idempotency key: transaction_id; enforced at Ledger API Ingress Gateway.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Wallet Service API Gateway",
            "kpi": "Ledger Journal Volume, Gross Monetary Flow, Point Velocity (KPI-WAL-02)",
            "acceptance": "Given an approved credit or debit request, when dispatched to ledger engine, then exactly one wallet_transaction_created row is recorded with fields (event_id, transaction_id, user_id, transaction_type, amount, status) and no duplicate for transaction_id.",
            "given": "An upstream service requesting a point mutation (e.g. task reward or cash-out debit).",
            "when": "The wallet service generates a formal journal entry payload.",
            "then": "Exactly one wallet_transaction_created event is recorded with status = 'PENDING_CLEARANCE' before commit.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("transaction_id", "String", "Yes", "Format TXN_ + UUIDv4; unique non-null", "Primary key identifying prospective double-entry journal entry."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "Account identity undergoing balance mutation."),
                ("transaction_type", "Categorical", "Yes", "Controlled list: CREDIT, DEBIT, HOLD, RELEASE, REVERSAL", "Accounting direction of transaction in double-entry ledger."),
                ("amount", "Float", "Yes", "Float > 0.0; strictly positive magnitude", "Quantity of virtual points to be committed."),
                ("unit", "Categorical", "Yes", "Controlled list: XP, INR (Default: XP)", "Denomination unit of transacted currency."),
                ("status", "Categorical", "Yes", "Fixed value: 'PENDING_CLEARANCE'", "Pre-commit clearance state in financial pipeline."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Timestamp when mutation intent was registered.")
            ]
        },

        # ====================================================
        # 12. withdrawal_requested (Critical)
        # ====================================================
        {
            "event": "withdrawal_requested",
            "trigger": "User submits cash-out request; points debited from available balance to escrow.",
            "priority": "Critical",
            "dedupe": "Idempotency key: withdrawal_id; enforced at Payout Service DB unique constraint.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Payout Service / Client Form",
            "kpi": "Withdrawal Request Volume, Gross Withdrawal Value (KPI-WDL-02), Pending Escrow Liability (KPI-WDL-05), Support Ticket Resolution SLA (KPI-SUP-02), Withdrawal Rejection Rate (KPI-WDL-04)",
            "acceptance": "Given an active user with xp_balance >= 500, when user submits cash-out form, then exactly one withdrawal_requested row is recorded with fields (event_id, withdrawal_id, user_id, amount_inr, xp_deducted, payout_method) and points are moved to escrow.",
            "given": "An active verified user with spendable balance >= minimum cash-out threshold (500 XP).",
            "when": "The user enters a valid UPI VPA or bank account and confirms cash redemption.",
            "then": "Exactly one withdrawal_requested event is logged, creating a disbursement row with payout_status = 'Requested'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("withdrawal_id", "String", "Yes", "Format WDL_ + UUIDv4; unique non-null", "Unique disbursement primary key for external payment rail tracking."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User account requesting fiat cash disbursement."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Submission timestamp marking start of payout SLA clock."),
                ("amount_inr", "Float", "Yes", "Float >= 50.0; minimum threshold ₹50 INR", "Nominal fiat cash value requested for disbursement."),
                ("xp_deducted", "Integer", "Yes", "Integer >= 500; pegged conversion ratio", "Virtual points debited from available balance into escrow."),
                ("payout_method", "Categorical", "Yes", "Controlled list: UPI_VPA, IMPS_BANK, VOUCHER", "Target payment instrument selected by user."),
                ("payout_account_hash", "String", "Yes", "64-char hex string (SHA-256 of VPA/Account)", "One-way cryptographic hash masking beneficiary PII while detecting sybil abuse.")
            ]
        },

        # ====================================================
        # 13. withdrawal_completed (Critical)
        # ====================================================
        {
            "event": "withdrawal_completed",
            "trigger": "Payment aggregator signed webhook confirms cash settlement into beneficiary bank.",
            "priority": "Critical",
            "dedupe": "Idempotency key: (withdrawal_id, gateway_reference); enforced at Gateway Webhook Receiver DB unique constraint.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Payment Gateway Webhook Receiver",
            "kpi": "Withdrawal Completion Rate (KPI-WDL-01), Average Processing SLA (KPI-WDL-03), Gross Settled Cash Outflow",
            "acceptance": "Given a withdrawal in 'Processing' state, when gateway webhook confirms successful transfer, then exactly one withdrawal_completed row is recorded with fields (event_id, withdrawal_id, user_id, amount_inr, gateway_reference) and payout_status is updated to 'Completed'.",
            "given": "A cash withdrawal request dispatched to payment aggregator rail in 'Processing' state.",
            "when": "A cryptographically signed HMAC webhook arrives from Cashfree/RazorpayX confirming settlement.",
            "then": "Exactly one withdrawal_completed event is logged, closing escrow hold and setting payout_status to 'Completed'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("withdrawal_id", "String", "Yes", "Must match pending withdrawal record", "Disbursement transaction primary key."),
                ("user_id", "String", "Yes", "Must exist in Users master table", "User receiving settled cash funds."),
                ("gateway_name", "Categorical", "Yes", "Controlled list: CASHFREE, RAZORPAYX, PAYU", "Aggregator payment rail confirming transfer."),
                ("gateway_reference", "String", "Yes", "Alphanumeric string (12-25 chars UTR)", "External banking UTR or gateway payment ID verifying transfer."),
                ("amount_inr", "Float", "Yes", "Float >= 50.0; matches requested amount", "Settled fiat cash amount in Indian Rupees."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Webhook receipt timestamp marking terminal settlement."),
                ("completed_at", "Datetime", "Yes", "ISO-8601 UTC timestamp", "Timestamp when banking rails settled funds into user account.")
            ]
        },

        # ====================================================
        # 14. referral_registered (High)
        # ====================================================
        {
            "event": "referral_registered",
            "trigger": "Invited referee creates account using an active referrer's referral code.",
            "priority": "High",
            "dedupe": "Idempotency key: referred_user_id; enforced at Referral Engine DB unique constraint (1 referee = 1 referrer).",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Referral Engine / Auth Ingress",
            "kpi": "Inbound Referral Share (KPI-REF-01), Viral Reach, Referral Attribution Rate",
            "acceptance": "Given an unauthenticated referee with a valid referral link, when account registration completes, then exactly one referral_registered row is recorded with fields (event_id, referral_id, referrer_user_id, referred_user_id, referral_code) and no duplicate for referred_user_id.",
            "given": "A new user completing signup with a valid referral code entered or deep-linked.",
            "when": "Account creation succeeds and credentials are confirmed in auth service.",
            "then": "Exactly one referral_registered event is emitted, establishing attribution link with referral_status = 'Registered'.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("referral_id", "String", "Yes", "Format REF_ + UUIDv4; unique non-null", "Directional viral relationship primary key."),
                ("referrer_user_id", "String", "Yes", "Must exist in Users master table", "Inviting member credited with referral attribution."),
                ("referred_user_id", "String", "Yes", "Must exist in Users master table; != referrer", "Newly registered referee establishing account."),
                ("referral_code", "String", "Yes", "Format VL + 6 hex characters", "Referral code matching referrer profile."),
                ("share_channel", "Categorical", "Yes", "Controlled list: WhatsApp, Telegram, Direct_Link, Social_Media", "Viral sharing platform through which referee was acquired."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Timestamp when referee registration occurred.")
            ]
        },

        # ====================================================
        # 15. referral_converted (Critical)
        # ====================================================
        {
            "event": "referral_converted",
            "trigger": "Referee fulfills commercial earning threshold (>= 100 XP from tasks across >= 2 active days).",
            "priority": "Critical",
            "dedupe": "Idempotency key: (referral_id, 'converted'); enforced at Referral Milestone Engine DB state lock.",
            "timestamp": "Server Clock UTC ISO-8601 (YYYY-MM-DDTHH:MM:SS.sssZ)",
            "source": "Referral Engine / Milestone Service",
            "kpi": "Referral Funnel Conversion Rate (KPI-REF-03), Viral K-Factor, Referral CAC Payback",
            "acceptance": "Given a referred user in 'Registered' state, when referee reaches >= 100 XP from micro-tasks, then exactly one referral_converted row is recorded with fields (event_id, referral_id, referrer_user_id, referred_user_id, referrer_bounty_xp) and bounties are disbursed to both wallets.",
            "given": "A referred user active in the app with attribution link in 'Registered' or 'Activated' state.",
            "when": "The referee accumulates >= 100 XP strictly through verified micro-tasks.",
            "then": "Exactly one referral_converted event is committed, unlocking 100 XP bounty for referrer and 25 XP for referee.",
            "fields": [
                ("event_id", "String", "Yes", "Prefix EVT_ + UUIDv4; unique non-null", "Atomic event record key for stream deduplication and idempotency."),
                ("referral_id", "String", "Yes", "Must match an existing referral in Registered state", "Directional viral relationship primary key."),
                ("referrer_user_id", "String", "Yes", "Must exist in Users master table", "Inviter receiving 100 XP bounty upon conversion."),
                ("referred_user_id", "String", "Yes", "Must exist in Users master table", "Referee qualifying as a commercial earner."),
                ("timestamp", "Datetime", "Yes", "Server monotonic UTC timestamp", "Timestamp when qualification hurdle was met."),
                ("referrer_bounty_xp", "Integer", "Yes", "Fixed value: 100 XP", "Bounty reward points committed to inviter's wallet."),
                ("referred_bonus_xp", "Integer", "Yes", "Fixed value: 25 XP", "Welcome bonus points committed to referee's wallet."),
                ("transaction_id", "String", "Yes", "Format TXN_ + UUIDv4; ledger key", "Ledger reference linking bounty payment to financial books.")
            ]
        }
    ]

    # Populate Sheet 1 (Events) at field granularity
    req_counter = 1
    events_sheet_rows = []
    acceptance_tests_rows = []

    for ev_idx, ev in enumerate(events_spec, start=1):
        event_name = ev["event"]
        trigger = ev["trigger"]
        priority = ev["priority"]
        dedupe = ev["dedupe"]
        ts_spec = ev["timestamp"]
        source = ev["source"]
        kpi_dep = ev["kpi"]
        acceptance = ev["acceptance"]
        payload_fields_str = ", ".join([f[0] for f in ev["fields"]])

        # Sheet 2 row
        req_id_event = f"REQ-EVT-{ev_idx:02d}"
        acceptance_tests_rows.append((req_id_event, ev["given"], ev["when"], ev["then"]))

        # Field-level rows for Sheet 1
        for f_idx, (fname, ftype, freq, fval, fwhy) in enumerate(ev["fields"], start=1):
            req_id_field = f"REQ-EVT-{ev_idx:02d}-{f_idx:02d}"
            row = (
                req_id_field,
                event_name,
                trigger,
                payload_fields_str,
                fname,
                ftype,
                freq,
                fval,
                dedupe,
                ts_spec,
                source,
                fwhy,
                kpi_dep,
                acceptance,
                priority
            )
            events_sheet_rows.append(row)

    print(f"Total field-level requirement rows: {len(events_sheet_rows)} across {len(events_spec)} events.")

    # Write Sheet 1
    ws_events.append(headers)
    for r in events_sheet_rows:
        ws_events.append(list(r))

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

    for row_idx in range(2, len(events_sheet_rows) + 2):
        for col_idx in range(1, len(headers) + 1):
            cell = ws_events.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            # Alignment rules
            if col_idx in (1, 2, 6, 7, 15):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in (4, 5):
                cell.alignment = Alignment(horizontal="left", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

            # Priority highlighting
            if col_idx == 15:
                val = str(cell.value)
                if val == "Critical":
                    cell.fill = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid") # soft red/coral
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C00000")
                elif val == "High":
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # soft yellow
                    cell.font = Font(name="Calibri", size=10, bold=True, color="7F6000")
                elif val == "Medium":
                    cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # soft green
                    cell.font = Font(name="Calibri", size=10, color="375623")

    ws_events.freeze_panes = "C2"
    ws_events.auto_filter.ref = ws_events.dimensions

    col_widths = {
        "A": 16, # Requirement ID
        "B": 24, # Event
        "C": 35, # Trigger
        "D": 35, # Payload Fields
        "E": 22, # Field
        "F": 14, # Data Type
        "G": 12, # Required
        "H": 35, # Validation
        "I": 40, # Deduplication
        "J": 30, # Timestamp
        "K": 26, # Source
        "L": 40, # Why Needed
        "M": 35, # KPI Dependency
        "N": 45, # Acceptance Test
        "P": 14  # Priority
    }
    for col_letter, width in col_widths.items():
        ws_events.column_dimensions[col_letter].width = width

    # ----------------------------------------------------
    # Sheet 2: Acceptance_Tests
    # ----------------------------------------------------
    ws_tests = wb.create_sheet(title="Acceptance_Tests")
    test_headers = ["Requirement ID", "Given", "When", "Then"]
    ws_tests.append(test_headers)

    for col_idx in range(1, len(test_headers) + 1):
        cell = ws_tests.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for row_idx, (req_id, given, when, then) in enumerate(acceptance_tests_rows, start=2):
        ws_tests.append([req_id, given, when, then])
        for col_idx in range(1, len(test_headers) + 1):
            cell = ws_tests.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws_tests.freeze_panes = "B2"
    ws_tests.auto_filter.ref = ws_tests.dimensions

    ws_tests.column_dimensions["A"].width = 18
    ws_tests.column_dimensions["B"].width = 38
    ws_tests.column_dimensions["C"].width = 38
    ws_tests.column_dimensions["D"].width = 50

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
        "This developer analytics handoff workbook establishes the engineering telemetry contract for production ingestion. "
        "All payload schemas and acceptance tests reflect architectural design specifications for analytical testing. "
        "No claim is made that these events are currently implemented in production."
    )
    ws_notice["A4"].font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 85

    output_path = "09_engineering/developer_analytics_handoff.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path} with {len(events_sheet_rows)} field requirements across {len(events_spec)} events.")

if __name__ == "__main__":
    build_developer_handoff()
