#!/usr/bin/env python3
"""
scripts/07_build_data_dictionary.py
Generates 05_data_model/data_dictionary.xlsx with sheets:
1. 'Coverage' (Summary table of field counts per entity and Status split + merged top Notes notice)
2. 'Fields' (12 exact columns, 151 comprehensive fields)
3. 'SIMULATED_DATA_NOTICE' (governance notice)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_data_dictionary():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Data definition catalog: 151 fields across 12 entities
    # ----------------------------------------------------
    fields_data = [
        # ====================================================
        # 1. USER ENTITY (29 fields: 26 Confirmed, 3 To Be Verified)
        # ====================================================
        (
            "User", "user_id", "String",
            "Unique simulated user identifier serving as master primary key",
            "VLUSR000001", "Yes", "Format VLUSR + 6 digits (VLUSR000001 - VLUSR001000)",
            "Unique; non-null; regex ^VLUSR[0-9]{6}$", "01_Users_1000 / Users_1000_Clean",
            "Restricted", "Master join key for all user-level behavioral, session, and financial data", "Confirmed"
        ),
        (
            "User", "full_name", "String",
            "Simulated display name of the user",
            "Aarav Sharma", "Yes", "Length 2-100 characters",
            "Non-empty; trimmed of leading/trailing whitespace", "User Form / Ingress",
            "Restricted", "User profile personalization and outbound notification templates", "Confirmed"
        ),
        (
            "User", "email", "String",
            "Simulated primary user email address",
            "aarav.sharma@example.com", "Yes", "RFC 5322 compliant simulated email string",
            "Valid email format; lowercase normalized", "Auth Service",
            "Restricted", "Account identity, login authentication, and communications", "Confirmed"
        ),
        (
            "User", "age", "Integer",
            "Simulated age in years at registration",
            24, "Yes", "Range 18-65 in simulated dataset",
            "Integer >= 18 (legal rewards threshold)", "User Form Input",
            "Internal", "Demographic segmentation and age compliance verification", "Confirmed"
        ),
        (
            "User", "gender", "Categorical",
            "Simulated self-reported user gender",
            "Male", "No", "Male, Female, Other",
            "Controlled categorical values; null allowed in messy audit", "User Form Input",
            "Internal", "Demographic cohort engagement and behavioral preference analysis", "Confirmed"
        ),
        (
            "User", "state", "Categorical",
            "Simulated Indian state or union territory of residence",
            "Maharashtra", "Yes", "Controlled list of 36 Indian states and UTs",
            "Controlled list; non-empty string", "User Form / GeoIP",
            "Public", "Geographic cohort analysis, regional growth campaigns, and state penetration", "Confirmed"
        ),
        (
            "User", "city", "Categorical",
            "Simulated city of residence",
            "Mumbai", "Yes", "Non-empty string matching state jurisdiction",
            "Consistent with state; validated against master city catalog", "User Form / GeoIP",
            "Restricted", "Urban tier segmentation (Tier 1 vs Tier 2/3) and localized targeting", "Confirmed"
        ),
        (
            "User", "registration_datetime", "Datetime",
            "Simulated timestamp when user account was created",
            "2026-03-01T10:15:30Z", "Yes", "ISO-8601 UTC datetime string",
            "Valid parseable datetime; monotonic server clock", "Auth Service / DB",
            "Internal", "Baseline timestamp for cohort tenure, activation funnels, and retention curves", "Confirmed"
        ),
        (
            "User", "acquisition_source", "Categorical",
            "Primary simulated marketing or acquisition channel",
            "Social Media", "Yes", "Organic Search, Direct, Social Media, Referral, WhatsApp, Telegram, Other",
            "Controlled source list; non-null", "Attribution Ingress / UTM",
            "Public", "Channel CAC analysis, blended marketing efficiency, and growth attribution", "Confirmed"
        ),
        (
            "User", "referral_source_detail", "Categorical",
            "Granular sub-channel classification for referral acquisition",
            "Friend/Family", "Conditional", "Friend/Family, Influencer, Social Post, Community Group",
            "Required if acquisition_source = 'Referral'; otherwise null", "Attribution SDK / Deep Link",
            "Internal", "Viral attribution optimization and referral partner segmentation", "Confirmed"
        ),
        (
            "User", "primary_device", "Categorical",
            "Primary hardware operating system recorded at signup",
            "Android", "Yes", "Android, iOS, Windows, macOS",
            "Controlled device list; non-null", "Client SDK / User-Agent",
            "Public", "Platform segmentation, mobile vs desktop distribution, and SDK targeting", "Confirmed"
        ),
        (
            "User", "platform", "Categorical",
            "Client build framework utilized by the user",
            "Android Native", "Yes", "Android Native, iOS Native, Web",
            "Controlled platform list; non-null", "Client App Build",
            "Public", "Cross-platform feature parity, error tracking, and release management", "Confirmed"
        ),
        (
            "User", "account_status", "Categorical",
            "Simulated operational state of user account",
            "Active", "Yes", "Active, Inactive, Suspended, Pending Verification",
            "Controlled status list; non-null", "User DB / Admin Engine",
            "Internal", "User lifecycle analysis, churn monitoring, and risk containment", "Confirmed"
        ),
        (
            "User", "email_verification_status", "Categorical",
            "Verification status of user email address",
            "Verified", "Yes", "Verified, Pending",
            "Controlled list; non-null in clean table", "Auth Database",
            "Internal", "Trust tier classification, KYC gating, and fraud mitigation", "Confirmed"
        ),
        (
            "User", "verification_status", "Categorical",
            "Legacy verification status attribute in WB1 (01_Users_1000)",
            "Verified", "Yes", "Verified, Pending",
            "Controlled list; duplicate semantic meaning with email_verification_status", "01_Users_1000",
            "Internal", "Legacy attribute alias; to be standardized to email_verification_status in production", "To Be Verified"
        ),
        (
            "User", "onboarding_status", "Categorical",
            "Simulated progression status through new user tutorial",
            "Completed", "Yes", "Completed, Started, Not Started",
            "Controlled list; non-null in clean table", "User Profile DB",
            "Internal", "New user onboarding completion rate and early activation hurdles", "Confirmed"
        ),
        (
            "User", "last_login_datetime", "Datetime",
            "Timestamp of the most recent authenticated session",
            "2026-09-14T20:45:10Z", "No", "ISO-8601 UTC datetime string",
            ">= registration_datetime; null if user never returned", "Auth Service / Session Mart",
            "Internal", "Recency (RFM) scoring, inactivity detection, and churn flagging", "Confirmed"
        ),
        (
            "User", "lifetime_sessions", "Integer",
            "Cumulative total count of sessions initiated by user",
            48, "Yes", "Integer >= 0",
            "Non-negative integer; matches count in 02_Sessions", "User Profile Mart",
            "Internal", "User loyalty tiering, engagement depth, and power-user segmentation", "Confirmed"
        ),
        (
            "User", "active_days", "Integer",
            "Distinct calendar days on which user logged at least one session",
            22, "Yes", "Integer >= 0 and <= lifetime_sessions",
            "Integer between 0 and 198 (observation window length)", "Daily Activity Aggregator",
            "Internal", "L28 stickiness, engagement frequency, and habituation modeling", "Confirmed"
        ),
        (
            "User", "xp_balance", "Integer",
            "Simulated current spendable XP balance in wallet snapshot",
            1450, "Yes", "Integer >= 0",
            "Non-negative integer; snapshot balance", "Wallet Engine",
            "Internal", "Point economy liability estimation and user wealth tiering", "Confirmed"
        ),
        (
            "User", "referral_code", "String",
            "Unique outbound viral referral share code assigned to user",
            "VLA1B2C3", "Yes", "Format VL + 6 alphanumeric characters",
            "Unique per user; non-null", "Referral Engine",
            "Public", "Viral distribution attribution, invite link creation, and referral tracking", "Confirmed"
        ),
        (
            "User", "days_since_registration", "Decimal",
            "Derived account age in days relative to dataset snapshot date",
            197.5, "Yes", "Float/Decimal >= 0.0 (4 negative anomalies detected in test data)",
            "Ambiguity flagged: generator snapshot baseline preceded registration for 8 users", "Derived Calculation",
            "Internal", "Tenure normalization; requires boundary clamping against snapshot date", "To Be Verified"
        ),
        (
            "User", "is_active_7d", "Categorical",
            "Derived rolling 7-day user activity indicator flag",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list; derived from session recency", "Daily Mart",
            "Internal", "Weekly Active Users (WAU) calculation and short-term retention tracking", "Confirmed"
        ),
        (
            "User", "is_active_30d", "Categorical",
            "Derived rolling 30-day user activity indicator flag",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list; derived from session recency", "Daily Mart",
            "Internal", "Monthly Active Users (MAU) calculation and platform stickiness (DAU/MAU)", "Confirmed"
        ),
        (
            "User", "consent_status", "Categorical",
            "Data privacy policy and terms agreement status",
            "Accepted", "Yes", "Accepted, Pending",
            "Controlled list; non-null in clean table", "Client Ingress Form",
            "Internal", "DPDP Act / GDPR compliance enforcement and legal auditability", "Confirmed"
        ),
        (
            "User", "marketing_opt_in", "Categorical",
            "Consent preference to receive promotional push notifications and emails",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list; non-null in clean table", "User Settings DB",
            "Internal", "Marketing outreach campaign eligibility and opt-in rate tracking", "Confirmed"
        ),
        (
            "User", "account_created_via", "Categorical",
            "Authentication provider used to establish account",
            "Web Registration", "Yes", "Web Registration, Google Sign-In, Phone OTP",
            "Controlled list of auth providers", "Auth Gateway",
            "Internal", "Authentication method conversion, drop-off analysis, and credential-less authentication adoption", "Confirmed"
        ),
        (
            "User", "country", "Categorical",
            "Country of residence (Default: India in pre-launch version)",
            "India", "Yes", "ISO-3166-1 alpha-2 or country name (India)",
            "Controlled country list; non-null in clean table", "IP Geolocation / Form",
            "Public", "Geographic partitioning, international expansion, and localization", "Confirmed"
        ),
        (
            "User", "data_environment", "Categorical",
            "Environment tag present only in Users_Messy_Audit sheet",
            "SIMULATED_TEST", "No", "SIMULATED_TEST, PRODUCTION",
            "Appears only in messy audit table; absent from clean table and dictionary", "Synthetic Generator",
            "Internal", "Metadata flag separating synthetic from production data; to be formally verified", "To Be Verified"
        ),

        # ====================================================
        # 2. SESSION ENTITY (12 fields: 12 Confirmed)
        # ====================================================
        (
            "Session", "session_id", "String",
            "Unique simulated session visit identifier",
            "SESS0000001", "Yes", "Format SESS + 7 digits (SESS0000001 - SESS0007913)",
            "Unique; non-null; primary key of Sessions table", "Session Manager / Gateway",
            "Internal", "Visit container joins, session duration analysis, and journey pathing", "Confirmed"
        ),
        (
            "Session", "user_id", "String",
            "Foreign key associating session to parent user entity",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Token Context",
            "Restricted", "Links visit activity and dwell time to user identity and demographic cohorts", "Confirmed"
        ),
        (
            "Session", "session_start", "Datetime",
            "Timestamp when session visit was initialized",
            "2026-03-01T10:15:30Z", "Yes", "ISO-8601 UTC datetime string",
            "Valid datetime; monotonic client/server timestamp", "Client / Gateway Ingress",
            "Internal", "Session start volume, diurnal distribution, and session partition keys", "Confirmed"
        ),
        (
            "Session", "session_end", "Datetime",
            "Timestamp when session visit was terminated",
            "2026-03-01T10:18:45Z", "Yes", "ISO-8601 UTC datetime string",
            ">= session_start; non-null", "Client / Gateway Ingress",
            "Internal", "Visit boundary calculation and duration calculation", "Confirmed"
        ),
        (
            "Session", "session_duration_seconds", "Integer",
            "Total elapsed duration of visit in seconds",
            195, "Yes", "Integer >= 0 (Range 5s to 180s in simulated data)",
            "Non-negative integer; matches (session_end - session_start)", "Derived Calculation",
            "Internal", "Average Session Duration KPI, engagement depth, and short-session bounce analysis", "Confirmed"
        ),
        (
            "Session", "device", "Categorical",
            "Hardware operating system used during session",
            "Android", "Yes", "Android, iOS, Web",
            "Controlled list matching user primary_device", "Client Telemetry SDK",
            "Public", "Cross-device engagement duration and hardware platform performance", "Confirmed"
        ),
        (
            "Session", "platform", "Categorical",
            "Client build framework utilized during session",
            "Android Native", "Yes", "Android Native, iOS Native, Web",
            "Controlled list matching platform catalog", "Client App Build",
            "Public", "Platform stability comparison and build adoption tracking", "Confirmed"
        ),
        (
            "Session", "entry_point", "Categorical",
            "Product surface or screen where user entered application",
            "Home", "Yes", "Home, Daily Reward, Tasks, Wallet, Referral, Mining",
            "Controlled list of 15 platform feature surfaces", "Client Router / Deep Link",
            "Internal", "Deep-link conversion, notification re-engagement, and entry point distribution", "Confirmed"
        ),
        (
            "Session", "exit_feature", "Categorical",
            "Last feature surface recorded immediately prior to session exit",
            "Watch Ads / Offers", "No", "Controlled list of 15 features; null on abrupt termination",
            "Controlled list or null", "App State Router",
            "Internal", "Exit bounce analysis, churn drop-off surfaces, and flow friction points", "Confirmed"
        ),
        (
            "Session", "events_in_session", "Integer",
            "Total count of discrete event interactions recorded during session",
            8, "Yes", "Integer >= 0",
            "Matches count of child rows in 03_Feature_Events", "Event Stream Aggregator",
            "Internal", "Interaction density per visit, engagement intensity, and bot detection", "Confirmed"
        ),
        (
            "Session", "features_used_count", "Integer",
            "Count of distinct platform features touched during session",
            3, "Yes", "Integer between 0 and 15",
            "Range 0 to 15; non-negative integer", "Event Stream Aggregator",
            "Internal", "Session exploration breadth and cross-feature navigation behavior", "Confirmed"
        ),
        (
            "Session", "session_status", "Categorical",
            "Technical termination status of the session",
            "Completed", "Yes", "Completed, Timed Out, Terminated",
            "Controlled list of session closure codes", "Gateway Session Manager",
            "Internal", "Technical stability, background timeout tracking, and crash detection", "Confirmed"
        ),

        # ====================================================
        # 3. EVENT ENTITY (13 fields: 12 Confirmed, 1 To Be Verified)
        # ====================================================
        (
            "Event", "event_id", "String",
            "Unique atomic telemetry record identifier",
            "EVT00000001", "Yes", "Format EVT + 8 digits (EVT00000001 - EVT00035704)",
            "Unique; non-null; primary key of Feature_Events table", "Event Ingestion Gateway",
            "Internal", "Stream deduplication, idempotency verification, and atomic clickstream joins", "Confirmed"
        ),
        (
            "Event", "user_id", "String",
            "Foreign key linking event to user entity",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Token Context",
            "Restricted", "User behavioral pathing, cohort segmentation, and feature adoption", "Confirmed"
        ),
        (
            "Event", "session_id", "String",
            "Foreign key associating event to visit container",
            "SESS0000001", "Yes", "Must exist in Sessions table",
            "Foreign key constraint; non-null", "Client Context Header",
            "Internal", "In-session funnel analysis, drop-off tracking, and visit dwell attribution", "Confirmed"
        ),
        (
            "Event", "event_datetime", "Datetime",
            "Timestamp when atomic event occurred",
            "2026-03-01T10:16:12Z", "Yes", "ISO-8601 UTC datetime string",
            "Within session_start and session_end bounds", "Server Clock (UTC)",
            "Internal", "Time-series behavioral analysis, event sequence reconstruction, and velocity", "Confirmed"
        ),
        (
            "Event", "feature_name", "Categorical",
            "Product surface or module hosting the event",
            "Watch Ads / Offers", "Yes", "Controlled list of 15 features",
            "Controlled list (casing anomalies flagged in audit)", "Client Navigation Router",
            "Internal", "Feature Adoption Rate KPI, feature usage distribution, and UX popularity", "Confirmed"
        ),
        (
            "Event", "event_name", "Categorical",
            "Specific behavioral action performed by user",
            "ad_completed", "Yes", "Controlled list of 35 distinct simulated event names",
            "Controlled list conforming to object_action syntax", "Client Telemetry / SDK",
            "Internal", "Core behavioral conversion funnels, event volume tracking, and engagement depth", "Confirmed"
        ),
        (
            "Event", "event_status", "Categorical",
            "Operational outcome or state of the event",
            "Success", "Yes", "Started, Success, Abandoned, Failed",
            "Controlled list (trailing whitespace anomalies flagged in audit)", "Event Execution Engine",
            "Internal", "Feature success rates, technical failure rates, and abandonment tracking", "Confirmed"
        ),
        (
            "Event", "device", "Categorical",
            "Client operating system at event emission",
            "Android", "Yes", "Android, iOS, Web",
            "Matches session device; controlled list", "Client SDK Header",
            "Public", "Cross-device event breakdown and hardware stability monitoring", "Confirmed"
        ),
        (
            "Event", "platform", "Categorical",
            "Client application build framework at event emission",
            "Android Native", "Yes", "Android Native, iOS Native, Web",
            "Matches session platform; controlled list", "Client App Header",
            "Public", "Build-specific telemetry validation and regression detection", "Confirmed"
        ),
        (
            "Event", "acquisition_source", "Categorical",
            "User acquisition channel stamped on event for denormalized analysis",
            "Social Media", "Yes", "Matches user profile acquisition_source",
            "Controlled source list", "User Profile Join",
            "Public", "Direct slicing of clickstream behavior by acquisition cohort without table joins", "Confirmed"
        ),
        (
            "Event", "sequence_number", "Integer",
            "Ordinal sequence index of event within its parent session",
            4, "Yes", "Integer >= 1",
            "Ambiguity flagged: audit revealed duplicate sequence numbers within sessions", "Client SDK Event Counter",
            "Internal", "Reconstruction of user session navigation paths; sequence integrity to be verified", "To Be Verified"
        ),
        (
            "Event", "reward_related_flag", "Categorical",
            "Binary flag indicating whether event relates to reward earning features",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Event Router Classifier",
            "Internal", "Quick filtering for earning vs navigation interactions in event mart", "Confirmed"
        ),
        (
            "Event", "xp_related_flag", "Categorical",
            "Binary flag indicating whether event affects XP point balance",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Event Router Classifier",
            "Internal", "Classification of economic vs non-economic events for point pipeline modeling", "Confirmed"
        ),

        # ====================================================
        # 4. DAILY ACTIVITY ENTITY (17 fields: 17 Confirmed)
        # ====================================================
        (
            "Daily_Activity", "user_id", "String",
            "Foreign key linking daily aggregated summary to user entity",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Daily Aggregator Mart",
            "Restricted", "User joins for longitudinal daily activity and retention curves", "Confirmed"
        ),
        (
            "Daily_Activity", "activity_date", "Date",
            "Calendar date of aggregated activity partition",
            "2026-03-01", "Yes", "ISO-8601 date string (YYYY-MM-DD)",
            "Valid calendar date; within observation window", "Daily Aggregator Mart",
            "Internal", "Daily Active Users (DAU) date partition and calendar retention tracking", "Confirmed"
        ),
        (
            "Daily_Activity", "session_count", "Integer",
            "Total sessions initiated by user on this calendar date",
            3, "Yes", "Integer >= 0",
            "Non-negative integer; matches session count for date", "Daily Aggregator Mart",
            "Internal", "Daily visit frequency and user return intensity", "Confirmed"
        ),
        (
            "Daily_Activity", "session_duration_minutes", "Float",
            "Total active session dwell time in minutes on this calendar date",
            12.5, "Yes", "Float >= 0.0",
            "Non-negative float; matches sum(duration_seconds)/60", "Daily Aggregator Mart",
            "Internal", "Daily active engagement time per user", "Confirmed"
        ),
        (
            "Daily_Activity", "event_count", "Integer",
            "Total discrete event actions logged by user on this calendar date",
            24, "Yes", "Integer >= 0",
            "Non-negative integer; matches event count for date", "Daily Aggregator Mart",
            "Internal", "Daily interaction density and activity volume", "Confirmed"
        ),
        (
            "Daily_Activity", "feature_count", "Integer",
            "Count of distinct platform features engaged with on this date",
            4, "Yes", "Integer between 0 and 15",
            "Range 0 to 15; non-negative integer", "Daily Aggregator Mart",
            "Internal", "Daily feature exploration breadth index", "Confirmed"
        ),
        (
            "Daily_Activity", "task_count", "Integer",
            "Total task execution attempts initiated on this date",
            5, "Yes", "Integer >= 0",
            "Non-negative integer; matches task starts in 05_Task_Activity", "Daily Aggregator Mart",
            "Internal", "Daily earning attempt volume and demand", "Confirmed"
        ),
        (
            "Daily_Activity", "completed_task_count", "Integer",
            "Total tasks successfully completed on this date",
            3, "Yes", "Integer >= 0 and <= task_count",
            "Non-negative integer; matches task completions", "Daily Aggregator Mart",
            "Internal", "Daily user productivity and task completion efficiency", "Confirmed"
        ),
        (
            "Daily_Activity", "reward_activity_count", "Integer",
            "Total reward collection and claiming actions on this date",
            4, "Yes", "Integer >= 0",
            "Non-negative integer; count of reward events", "Daily Aggregator Mart",
            "Internal", "Daily reward collection velocity and habituation", "Confirmed"
        ),
        (
            "Daily_Activity", "xp_activity_count", "Integer",
            "Total events directly generating XP credits on this date",
            4, "Yes", "Integer >= 0",
            "Non-negative integer; count of xp-generating events", "Daily Aggregator Mart",
            "Internal", "Daily point accrual velocity across features", "Confirmed"
        ),
        (
            "Daily_Activity", "streak_activity", "Categorical",
            "Binary flag indicating whether consecutive active streak was maintained",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Streak Engine",
            "Internal", "Verification of daily streak continuity and habit formation", "Confirmed"
        ),
        (
            "Daily_Activity", "daily_reward_claimed", "Categorical",
            "Binary flag indicating whether daily check-in bonus was claimed",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Daily Reward Service",
            "Internal", "Daily login reward claim rate and retention stickiness", "Confirmed"
        ),
        (
            "Daily_Activity", "mission_activity", "Categorical",
            "Binary flag indicating active engagement with gamified missions",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Missions Service",
            "Internal", "Daily mission participation and goal engagement", "Confirmed"
        ),
        (
            "Daily_Activity", "spin_activity", "Categorical",
            "Binary flag indicating engagement with Spin & Win lucky wheel",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Spin Service",
            "Internal", "Daily chance game adoption and engagement", "Confirmed"
        ),
        (
            "Daily_Activity", "referral_activity", "Categorical",
            "Binary flag indicating viral referral sharing or invite generation",
            "No", "Yes", "Yes, No",
            "Controlled binary list", "Referral Engine",
            "Internal", "Daily viral sharing propensity and organic growth loop activity", "Confirmed"
        ),
        (
            "Daily_Activity", "wallet_activity", "Categorical",
            "Binary flag indicating wallet balance inspection or withdrawal intent",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list", "Wallet Service",
            "Internal", "Daily financial interest and liquidity monitoring", "Confirmed"
        ),
        (
            "Daily_Activity", "active_flag", "Categorical",
            "Official platform qualification flag marking user as active on this date",
            "Yes", "Yes", "Yes, No",
            "Controlled binary list; 'Yes' if session_count > 0", "Daily Aggregator Mart",
            "Internal", "Canonical filter for Daily Active Users (DAU) metric calculations", "Confirmed"
        ),

        # ====================================================
        # 5. TASK ACTIVITY ENTITY (12 fields: 11 Confirmed, 1 To Be Verified)
        # ====================================================
        (
            "Task_Activity", "activity_id", "String",
            "Unique task activity execution record identifier",
            "ACT0000001", "Yes", "Format ACT + 7 digits (ACT0000001 - ACT0009846)",
            "Unique; non-null; primary key of Task_Activity table", "Task Engine",
            "Internal", "Task attempt primary key, execution tracking, and completion joins", "Confirmed"
        ),
        (
            "Task_Activity", "user_id", "String",
            "Foreign key linking task execution to user entity",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Token Context",
            "Restricted", "User productivity, earning distribution, and task fraud scoring", "Confirmed"
        ),
        (
            "Task_Activity", "task_id", "String",
            "Foreign key referencing the task definition in the task catalog",
            "TASK0012", "Yes", "Format TASK + 4 digits (TASK0001 - TASK0080)",
            "80 distinct task IDs in simulated data; parent catalog missing", "Task Catalog Master",
            "Internal", "Task-level conversion, failure rate, and advertiser inventory benchmarking", "Confirmed"
        ),
        (
            "Task_Activity", "task_category", "Categorical",
            "Functional category of the micro-earning activity",
            "Watch Ads / Offers", "Yes", "Controlled list of task categories matching feature catalog",
            "Controlled list; non-null", "Product Feature Taxonomy",
            "Public", "Task Completion Rate and Failure Rate segmentation by category", "Confirmed"
        ),
        (
            "Task_Activity", "task_viewed_at", "Datetime",
            "Timestamp when task card was rendered on client screen",
            "2026-03-01T10:16:15Z", "Yes", "ISO-8601 UTC datetime string",
            "Valid timestamp; within session boundaries", "Client Telemetry SDK",
            "Internal", "Task discovery reach and impression-to-start conversion latency", "Confirmed"
        ),
        (
            "Task_Activity", "task_started_at", "Datetime",
            "Timestamp when user tapped to start task execution",
            "2026-03-01T10:16:20Z", "Yes", "ISO-8601 UTC datetime string",
            ">= task_viewed_at; valid timestamp", "Client SDK / Task Engine",
            "Internal", "Task execution start volume and timing baseline", "Confirmed"
        ),
        (
            "Task_Activity", "task_completed_at", "Datetime",
            "Timestamp when user finished task requirements",
            "2026-03-01T10:16:50Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= task_started_at; null if task status is Failed or Abandoned", "Task Engine / Callback",
            "Internal", "Task execution duration calculation and throughput measurement", "Confirmed"
        ),
        (
            "Task_Activity", "task_status", "Categorical",
            "Operational execution outcome of task attempt",
            "Completed", "Yes", "Completed, Failed, Abandoned",
            "Controlled status list; non-null", "Task Engine",
            "Internal", "Task Completion Rate and Task Failure Rate KPI calculations", "Confirmed"
        ),
        (
            "Task_Activity", "failure_reason", "Categorical",
            "Diagnostic error cause explaining why task was not completed",
            "User Abandoned", "Conditional", "Controlled list: User Abandoned, Network Disconnect, Ad Skip, Timeout",
            "Null if task_status = 'Completed'; controlled list otherwise", "Error Handler / SDK",
            "Internal", "Task failure root cause analysis, UX friction diagnosis, and partner error alerts", "Confirmed"
        ),
        (
            "Task_Activity", "reward_status", "Categorical",
            "Settlement and credit status of reward associated with task",
            "Credited", "Yes", "Credited, Pending, None",
            "Present in data table; omitted from 08_Data_Dictionary documentation", "Reward Engine",
            "Internal", "Reward payout reconciliation; documentation discrepancy to be verified", "To Be Verified"
        ),
        (
            "Task_Activity", "device", "Categorical",
            "Hardware operating system used for task attempt",
            "Android", "Yes", "Android, iOS, Web",
            "Matches session device; controlled list", "Client SDK Header",
            "Public", "Hardware-specific task failure rates and technical compatibility analysis", "Confirmed"
        ),
        (
            "Task_Activity", "session_id", "String",
            "Foreign key linking task execution to visit container",
            "SESS0000001", "Yes", "Must exist in Sessions table",
            "Foreign key constraint; non-null", "Client Context Header",
            "Internal", "Session journey context for task completions and dwell attribution", "Confirmed"
        ),

        # ====================================================
        # 6. MILESTONE ENTITY (6 fields: 4 Confirmed, 2 To Be Verified)
        # ====================================================
        (
            "Milestone", "user_id", "String",
            "Foreign key linking milestone achievement to user entity",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Milestone Engine",
            "Restricted", "User progression analysis and gamified milestone attribution", "Confirmed"
        ),
        (
            "Milestone", "milestone_type", "Categorical",
            "Category of gamified achievement milestone reached",
            "seventh_active_day", "Yes", "first_session, seventh_active_day, 10_tasks_completed, level_5_reached, 500_xp_earned",
            "Controlled list of milestone types", "Milestone Engine",
            "Internal", "Long-term habituation tracking and 7-day Streak Retention KPI", "Confirmed"
        ),
        (
            "Milestone", "milestone_datetime", "Datetime",
            "Timestamp when milestone requirements were fulfilled",
            "2026-03-07T14:22:10Z", "Yes", "ISO-8601 UTC datetime string",
            "Valid datetime; >= user registration_datetime", "Milestone Engine",
            "Internal", "Velocity to milestone achievement and cohort progression cadence", "Confirmed"
        ),
        (
            "Milestone", "milestone_value", "Integer",
            "Numeric bonus reward points awarded for unlocking milestone",
            100, "Yes", "Integer >= 0 (50, 100, 200 pts in simulated data)",
            "Present in data; omitted from 08_Data_Dictionary documentation", "Milestone Engine",
            "Internal", "Milestone bonus reward liability and gamification incentive economics", "To Be Verified"
        ),
        (
            "Milestone", "source_event", "String",
            "Specific event action that triggered the milestone unlock",
            "daily_reward_claimed", "Yes", "Non-empty string matching an approved event_name",
            "Present in data; omitted from 08_Data_Dictionary documentation", "Event Stream Listener",
            "Internal", "Event causation analysis for gamification milestone unlocks", "To Be Verified"
        ),
        (
            "Milestone", "session_id", "String",
            "Foreign key linking milestone unlock to visit container",
            "SESS0000045", "Yes", "Must exist in Sessions table",
            "Foreign key constraint; non-null", "Client Context Header",
            "Internal", "Session attribution for celebratory in-app milestone animations", "Confirmed"
        ),

        # ====================================================
        # 7. FEATURE USAGE ENTITY (7 fields: 7 Confirmed)
        # ====================================================
        (
            "Feature_Usage", "feature_name", "Categorical",
            "Product feature surface identifier",
            "Daily Reward", "Yes", "Controlled list of 15 features",
            "Unique primary key of Feature_Usage mart table", "Core Analytics Mart",
            "Public", "Feature dimension key for adoption and engagement benchmarking", "Confirmed"
        ),
        (
            "Feature_Usage", "unique_users", "Integer",
            "Total distinct users who interacted with feature in observation window",
            836, "Yes", "Integer between 0 and 1000",
            "Range 0 to 1000; non-negative integer", "Core Analytics Mart",
            "Internal", "Feature penetration volume and total feature reach", "Confirmed"
        ),
        (
            "Feature_Usage", "total_events", "Integer",
            "Total interaction events logged across feature in observation window",
            3540, "Yes", "Integer >= 0",
            "Non-negative integer; matches count in Feature_Events", "Core Analytics Mart",
            "Internal", "Feature traffic volume and interaction density", "Confirmed"
        ),
        (
            "Feature_Usage", "sessions_with_feature", "Integer",
            "Total distinct sessions containing at least one interaction with feature",
            2810, "Yes", "Integer >= 0",
            "Non-negative integer; matches session distribution", "Core Analytics Mart",
            "Internal", "Feature appearance across user visits and workflow integration", "Confirmed"
        ),
        (
            "Feature_Usage", "users_with_success_event", "Integer",
            "Distinct users recording at least one successful completion on feature",
            812, "Yes", "Integer <= unique_users",
            "Non-negative integer; success rate denominator", "Core Analytics Mart",
            "Internal", "Successful feature adoption rate and value realization", "Confirmed"
        ),
        (
            "Feature_Usage", "events_per_user", "Float",
            "Mean event interactions logged per active feature user",
            4.23, "Yes", "Float >= 0.0",
            "Non-negative float; matches total_events / unique_users", "Core Analytics Mart",
            "Internal", "Feature engagement depth and repeat interaction intensity", "Confirmed"
        ),
        (
            "Feature_Usage", "sessions_per_user", "Float",
            "Mean distinct sessions containing feature interaction per user",
            3.36, "Yes", "Float >= 0.0",
            "Non-negative float; matches sessions_with_feature / unique_users", "Core Analytics Mart",
            "Internal", "Feature habituation and return visit frequency", "Confirmed"
        ),

        # ====================================================
        # 8. WALLET TRANSACTION ENTITY (Proposed: 11 fields)
        # ====================================================
        (
            "Wallet_Transaction", "transaction_id", "String",
            "Immutable primary key for double-entry ledger entry",
            "TXN_9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d", "Yes", "Format TXN_ + UUIDv4",
            "Unique; non-null; immutable append-only record", "Wallet Service / Ledger Engine",
            "Internal", "Provides immutable audit trail for all prospective changes to user currency balance", "Proposed"
        ),
        (
            "Wallet_Transaction", "user_id", "String",
            "Foreign key linking ledger entry to user account",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Context",
            "Restricted", "Associates all ledger credit and debit entries to the permanent user account", "Confirmed"
        ),
        (
            "Wallet_Transaction", "transaction_datetime", "Datetime",
            "Exact server timestamp when ledger entry was committed",
            "2026-03-01T10:16:50Z", "Yes", "ISO-8601 UTC datetime string",
            "Monotonic server clock timestamp; non-null", "Server Clock (UTC)",
            "Internal", "Reconciliation of point issuance vs breakage and running balance calculation", "Proposed"
        ),
        (
            "Wallet_Transaction", "transaction_type", "Categorical",
            "Accounting direction and nature of transaction",
            "CREDIT", "Yes", "CREDIT, DEBIT, HOLD, RELEASE, REVERSAL, CORRECTION",
            "Controlled list of accounting entry types", "Ledger Engine",
            "Internal", "Double-entry bookkeeping validation and point flow segmentation", "Proposed"
        ),
        (
            "Wallet_Transaction", "amount", "Float",
            "Quantitative magnitude of currency transacted",
            50.0, "Yes", "Float > 0.0",
            "Strictly positive magnitude; non-negative", "Ledger Engine",
            "Internal", "Gross monetary flow, credit volume, and debit burn rate", "Proposed"
        ),
        (
            "Wallet_Transaction", "unit", "Categorical",
            "Currency or point denomination unit",
            "XP", "Yes", "XP, INR",
            "Controlled list (Default: XP)", "Ledger Engine",
            "Public", "Multi-currency ledger segmentation and currency conversion math", "Proposed"
        ),
        (
            "Wallet_Transaction", "status", "Categorical",
            "Settlement and clearance disposition of transaction",
            "POSTED", "Yes", "POSTED, PENDING_CLEARANCE, REVERSED, FAILED",
            "Controlled list of transaction settlement states", "Ledger Engine",
            "Internal", "Financial settlement verification and reconciliation audit", "Proposed"
        ),
        (
            "Wallet_Transaction", "source_feature", "Categorical",
            "Upstream product feature driving transaction",
            "Watch Ads / Offers", "Yes", "Controlled list of 15 features + Admin + Withdrawal",
            "Controlled list matching product taxonomy", "Event Engine",
            "Internal", "Revenue, liability, and point issuance attribution by feature", "Proposed"
        ),
        (
            "Wallet_Transaction", "reference_id", "String",
            "Foreign key linking origin activity, task, or payout entity",
            "ACT0000001", "Yes", "Format matches task_id, activity_id, or withdrawal_id",
            "Non-empty foreign key string", "Domain Services",
            "Internal", "End-to-end tracing from clickstream execution to ledger journal entry", "Proposed"
        ),
        (
            "Wallet_Transaction", "reversal_link", "String",
            "Pointer to original transaction_id if this is an offsetting reversal",
            "TXN_original_uuid", "Conditional", "Format TXN_ + UUIDv4",
            "Required if transaction_type = 'REVERSAL'; null otherwise", "Audit Engine",
            "Internal", "Clawback audit trail, chargeback analysis, and fraud reconciliation", "Proposed"
        ),
        (
            "Wallet_Transaction", "balance_after", "Float",
            "Running snapshot balance immediately post-transaction",
            1450.0, "Yes", "Float >= 0.0",
            "Calculated running total: SUM(credits) - SUM(debits)", "Ledger Engine",
            "Internal", "Continuous running balance verification and zero phantom balance guarantee", "Proposed"
        ),

        # ====================================================
        # 9. WITHDRAWAL ENTITY (Proposed: 15 fields)
        # ====================================================
        (
            "Withdrawal", "withdrawal_id", "String",
            "Unique global identifier for payout disbursement instance",
            "WDL_8f3a9b1c-4d2e-4b6a-9c7d-1e3f5a7b9c1d", "Yes", "Format WDL_ + UUIDv4",
            "Unique; non-null; immutable disbursement primary key", "Payout Service",
            "Restricted", "Tracks the asynchronous lifecycle of external fiat disbursements", "Proposed"
        ),
        (
            "Withdrawal", "user_id", "String",
            "Foreign key identifying user requesting cash disbursement",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Token Context",
            "Restricted", "User payout history, cash-out frequency limits, and KYC checks", "Confirmed"
        ),
        (
            "Withdrawal", "requested_datetime", "Datetime",
            "Client submission timestamp for cash-out request",
            "2026-03-15T18:30:00Z", "Yes", "ISO-8601 UTC datetime string",
            "Monotonic server clock timestamp; non-null", "Server Clock (UTC)",
            "Internal", "Withdrawal demand velocity, queue latency, and SLA turnaround baseline", "Proposed"
        ),
        (
            "Withdrawal", "amount_inr", "Float",
            "Fiat cash disbursement value in Indian Rupees",
            100.0, "Yes", "Float >= 50.0",
            "Minimum payout threshold ₹50 INR", "Payout Engine",
            "Restricted", "Gross Withdrawal Value (GWV), platform cash burn, and liquidity demand", "Proposed"
        ),
        (
            "Withdrawal", "xp_deducted", "Integer",
            "Total XP debited from user wallet and placed into escrow",
            1000, "Yes", "Integer >= 500",
            "Pegged ratio: 10 XP = ₹1 INR in simulated model", "Wallet Engine",
            "Internal", "Platform currency liability reduction and point burn volume", "Proposed"
        ),
        (
            "Withdrawal", "payout_method", "Categorical",
            "Target payment instrument rail for disbursement",
            "UPI_VPA", "Yes", "UPI_VPA, IMPS_BANK, AMAZON_PAY_VOUCHER, FLIPKART_VOUCHER",
            "Controlled list of payout rails", "User Form Input",
            "Internal", "Disbursement rail volume mix, processing fee optimization, and rail reliability", "Proposed"
        ),
        (
            "Withdrawal", "payout_status", "Categorical",
            "Operational state machine disposition of payout",
            "Completed", "Yes", "Requested, Processing, Completed, Rejected, Reversed",
            "Controlled finite-state machine statuses", "Payout Service",
            "Internal", "Withdrawal Completion Rate KPI, gateway failure rate, and SLA monitoring", "Proposed"
        ),
        (
            "Withdrawal", "gateway_name", "Categorical",
            "External payment aggregator processing disbursement",
            "CASHFREE", "Conditional", "CASHFREE, RAZORPAYX, PAYU",
            "Required when payout_status in ('Processing', 'Completed', 'Rejected')", "Payout Router",
            "Internal", "Payment aggregator SLA benchmarking and failover volume routing", "Proposed"
        ),
        (
            "Withdrawal", "gateway_reference", "String",
            "External banking UTR or gateway payment transaction reference",
            "UTR20260315123456", "Conditional", "Alphanumeric string (12-25 characters)",
            "Required if payout_status = 'Completed'; non-empty", "Gateway Webhook",
            "Restricted", "Banking settlement verification, dispute defense, and financial audit", "Proposed"
        ),
        (
            "Withdrawal", "failure_category", "Categorical",
            "Standardized root-cause category if disbursement is rejected",
            "INVALID_BENEFICIARY", "Conditional", "INVALID_BENEFICIARY, FRAUD_SUSPECTED, GATEWAY_TIMEOUT, USER_LIMIT_EXCEEDED",
            "Required if payout_status in ('Rejected', 'Reversed')", "Risk / Gateway Receiver",
            "Internal", "Disbursement failure classification, risk diagnosis, and alerting rules", "Proposed"
        ),
        (
            "Withdrawal", "failure_reason", "String",
            "Diagnostic error message returned by bank or risk engine",
            "UPI ID validation failed: VPA does not exist", "Conditional", "Max 255 characters",
            "Null if payout_status = 'Completed'", "Gateway / Risk Engine",
            "Restricted", "Customer support dispute resolution and user-facing error guidance", "Proposed"
        ),
        (
            "Withdrawal", "risk_score", "Float",
            "Automated anti-fraud anomaly score evaluated at request submission",
            0.12, "Yes", "Float between 0.00 and 1.00",
            "Range 0.00 (trusted) to 1.00 (critical risk)", "Anti-Fraud Engine",
            "Internal", "Fraud quarantine rate, sybil bot containment, and manual review routing", "Proposed"
        ),
        (
            "Withdrawal", "payout_account_hash", "String",
            "One-way cryptographic hash of beneficiary UPI VPA or bank account",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Yes", "64-character hex string (SHA-256)",
            "Format HEX(SHA256(vpa)); non-null", "Security Module",
            "Restricted", "Detects multi-account payout abuse while completely preventing PII exposure", "Proposed"
        ),
        (
            "Withdrawal", "processed_at", "Datetime",
            "Timestamp when request was dispatched to payment gateway rail",
            "2026-03-15T18:32:10Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= requested_datetime; null if rejected in initial risk check", "Payout Service",
            "Internal", "Internal queue processing latency and risk evaluation turnaround", "Proposed"
        ),
        (
            "Withdrawal", "completed_at", "Datetime",
            "Timestamp when bank settlement webhook confirmed payout settlement",
            "2026-03-15T18:35:45Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= processed_at; required if payout_status = 'Completed'", "Gateway Webhook",
            "Internal", "Average Processing SLA (Hours) KPI calculation and settlement latency", "Proposed"
        ),

        # ====================================================
        # 10. REFERRAL ENTITY (Proposed: 14 fields)
        # ====================================================
        (
            "Referral", "referral_id", "String",
            "Unique global identifier for directional referral relationship instance",
            "REF_3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d", "Yes", "Format REF_ + UUIDv4",
            "Unique; non-null; referral primary key", "Referral Engine",
            "Internal", "Primary key for directional viral invitation tree and bounty qualification", "Proposed"
        ),
        (
            "Referral", "referrer_user_id", "String",
            "User ID of the inviting member",
            "VLUSR000001", "Yes", "Must exist in Users master table",
            "Foreign key constraint; non-null", "Auth Context",
            "Restricted", "Referrer attribution, viral invite volume, and bounty disbursement", "Confirmed"
        ),
        (
            "Referral", "referred_user_id", "String",
            "User ID of the invited referee member",
            "VLUSR000512", "Conditional", "Must exist in Users master table",
            "referrer_user_id != referred_user_id; null prior to registration", "Auth Context",
            "Restricted", "Referee attribution, welcome bonus issuance, and qualification tracking", "Confirmed"
        ),
        (
            "Referral", "referral_code", "String",
            "Outbound referral share code utilized to form attribution link",
            "VLA1B2C3", "Yes", "Format VL + 6 alphanumeric characters",
            "Must match referrer_user_id referral_code; non-null", "Referral Engine",
            "Public", "Attribution verification across deep links and manual entry", "Confirmed"
        ),
        (
            "Referral", "share_channel", "Categorical",
            "Outbound distribution platform selected by referrer",
            "WhatsApp", "Yes", "WhatsApp, Telegram, Direct_Link, Social_Media, Organic",
            "Controlled list of distribution channels", "Deep Link Tracker",
            "Public", "Viral distribution channel effectiveness and sharing propensity", "Confirmed"
        ),
        (
            "Referral", "sub_channel", "String",
            "Granular campaign or UI placement sub-tag",
            "whatsapp_story", "Conditional", "Max 100 characters",
            "Non-empty string if provided; null otherwise", "UTM Parameters",
            "Public", "Granular placement attribution and creative conversion benchmarking", "Proposed"
        ),
        (
            "Referral", "created_at", "Datetime",
            "Timestamp when invitation link or share event occurred",
            "2026-03-02T11:00:00Z", "Yes", "ISO-8601 UTC datetime string",
            "Monotonic server clock timestamp; non-null", "Server Clock (UTC)",
            "Internal", "Outbound viral invitation volume and share-to-signup latency baseline", "Proposed"
        ),
        (
            "Referral", "registered_at", "Datetime",
            "Timestamp when referee successfully created account credentials",
            "2026-03-02T14:15:20Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= created_at; null if invite link was never used", "Auth Service",
            "Internal", "Invite-to-registration conversion rate and top-of-funnel viral reach", "Proposed"
        ),
        (
            "Referral", "activated_at", "Datetime",
            "Timestamp when referee completed onboarding and initial active session",
            "2026-03-02T14:25:00Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= registered_at; null if referee bounced immediately", "Onboarding Engine",
            "Internal", "Referral Activation Rate, filtering real human installs from bot farms", "Proposed"
        ),
        (
            "Referral", "converted_at", "Datetime",
            "Timestamp when referee reached commercial earning milestone (>= 100 XP)",
            "2026-03-05T09:30:15Z", "Conditional", "ISO-8601 UTC datetime string",
            ">= activated_at; null if referee never converted", "Milestone Engine",
            "Internal", "Commercial referral conversion milestone (Registration != Conversion gate)", "Proposed"
        ),
        (
            "Referral", "referral_status", "Categorical",
            "Operational state machine disposition of referral relationship",
            "Converted", "Yes", "Created, Registered, Activated, Converted, Disqualified",
            "Controlled finite-state machine list", "Referral Engine",
            "Internal", "Referral conversion funnel metrics and viral K-factor calculation", "Proposed"
        ),
        (
            "Referral", "referrer_bounty_xp", "Integer",
            "Bonus XP reward credited to referrer upon qualified conversion",
            100, "Conditional", "Integer >= 0",
            "Default 100 XP; strictly positive if referral_status = 'Converted'", "Reward Engine",
            "Internal", "Referral user acquisition cost (CAC) and viral incentive liability", "Proposed"
        ),
        (
            "Referral", "referred_bonus_xp", "Integer",
            "Welcome bonus XP reward credited to referee upon qualified conversion",
            25, "Conditional", "Integer >= 0",
            "Default 25 XP; strictly positive if referral_status = 'Converted'", "Reward Engine",
            "Internal", "Referee onboarding bonus cost and early retention incentive", "Proposed"
        ),
        (
            "Referral", "disqualification_reason", "Categorical",
            "Diagnostic error cause explaining why referral was denied",
            "SAME_DEVICE", "Conditional", "SAME_DEVICE, IP_COLLISION, SUSPECTED_BOT, TIME_LIMIT_EXCEEDED",
            "Required if referral_status = 'Disqualified'; null otherwise", "Anti-Fraud Engine",
            "Internal", "Referral fraud monitoring, sybil detection, and abuse mitigation", "Proposed"
        ),

        # ====================================================
        # 11. TASK MASTER DIMENSION (Proposed: 9 fields)
        # ====================================================
        (
            "Task_Master", "task_id", "String",
            "Unique primary key for task catalog item",
            "TASK0012", "Yes", "Format TASK + 4 digits (TASK0001 - TASK0080)",
            "Unique; non-null; master primary key for task dimension", "Product Task Catalog",
            "Internal", "Master join key for 05_Task_Activity benchmarking and reporting", "Proposed"
        ),
        (
            "Task_Master", "task_name", "String",
            "Human-readable title and display name of the task",
            "Install and Reach Level 5", "Yes", "Length 2-150 characters",
            "Non-empty descriptive string", "Product Task Catalog",
            "Public", "Task catalog presentation, UI cards, and analytical reporting", "Proposed"
        ),
        (
            "Task_Master", "task_category", "Categorical",
            "Functional earning category of the task",
            "Watch Ads / Offers", "Yes", "Controlled list of task categories matching feature catalog",
            "Controlled list; non-null", "Product Feature Taxonomy",
            "Public", "Task portfolio segmentation, tiering, and category mix analysis", "Confirmed"
        ),
        (
            "Task_Master", "reward_xp", "Integer",
            "Standard XP payout awarded to user upon verified task completion",
            25, "Yes", "Integer > 0",
            "Strictly positive integer", "Product Task Catalog",
            "Internal", "Task reward valuation, point liability forecasting, and user earning potential", "Proposed"
        ),
        (
            "Task_Master", "reward_unit", "Categorical",
            "Currency denomination of task reward",
            "XP", "Yes", "XP, Points",
            "Controlled list (Default: XP)", "Product Task Catalog",
            "Public", "Currency standardization and multi-reward catalog segmentation", "Proposed"
        ),
        (
            "Task_Master", "estimated_duration_seconds", "Integer",
            "Expected time in seconds required for user to complete task",
            60, "Yes", "Integer > 0",
            "Strictly positive integer", "Product Task Catalog",
            "Internal", "Hourly earning yield benchmark (XP/hour) and user productivity analysis", "Proposed"
        ),
        (
            "Task_Master", "partner_id", "String",
            "Third-party advertising, offerwall, or survey vendor identifier",
            "ADMOB_01", "Conditional", "Alphanumeric string (e.g. ADMOB_01, BITLABS_02)",
            "Required for third-party tasks; null for native gamified tasks", "Partner Registry",
            "Internal", "Partner volume attribution, postback verification, and SLA monitoring", "Proposed"
        ),
        (
            "Task_Master", "partner_campaign_id", "String",
            "External campaign or offer reference provided by partner",
            "CAMP_9921", "Conditional", "Alphanumeric string",
            "Non-empty string if provided by partner postback", "Partner Offerwall Feed",
            "Internal", "Partner campaign performance, margin tracking, and inventory reconciliation", "Proposed"
        ),
        (
            "Task_Master", "is_active", "Boolean",
            "Operational flag indicating whether task is currently available to users",
            True, "Yes", "True, False",
            "Boolean flag; non-null", "Product Task Catalog",
            "Internal", "Filtering active earning inventory from retired or paused campaigns", "Proposed"
        ),

        # ====================================================
        # 12. REWARDS CATALOG DIMENSION (Proposed: 7 fields)
        # ====================================================
        (
            "Rewards_Catalog", "reward_sku", "String",
            "Unique primary key for reward catalog redemption item",
            "RWD_AMZN_050", "Yes", "Format RWD_ + Brand + Value",
            "Unique; non-null; master primary key for reward items", "Rewards Inventory Catalog",
            "Public", "Primary key for reward item redemptions, stock tracking, and orders", "Proposed"
        ),
        (
            "Rewards_Catalog", "reward_name", "String",
            "Human-readable display title of redemption item",
            "Amazon Pay ₹50 Gift Card", "Yes", "Length 2-150 characters",
            "Non-empty descriptive string", "Rewards Inventory Catalog",
            "Public", "Item display in redemption catalog UI and transactional receipts", "Proposed"
        ),
        (
            "Rewards_Catalog", "reward_category", "Categorical",
            "Category classification of redemption item",
            "Voucher", "Yes", "Voucher, Cash, Merchandise, In-Game Token",
            "Controlled list of redemption categories", "Rewards Inventory Catalog",
            "Public", "Redemption category preference analysis and catalog diversification", "Proposed"
        ),
        (
            "Rewards_Catalog", "cost_xp", "Integer",
            "XP point price required to redeem item",
            500, "Yes", "Integer > 0",
            "Strictly positive integer; matches conversion economics", "Rewards Inventory Catalog",
            "Internal", "Redemption pricing, point sink elasticity, and user wealth burn rate", "Proposed"
        ),
        (
            "Rewards_Catalog", "fiat_value_inr", "Float",
            "Nominal cash monetary value in Indian Rupees",
            50.0, "Yes", "Float > 0.0",
            "Strictly positive float", "Rewards Inventory Catalog",
            "Internal", "Redemption unit economics, gross take-rate, and platform margin calculation", "Proposed"
        ),
        (
            "Rewards_Catalog", "stock_quantity", "Integer",
            "Current available voucher inventory count in stock",
            250, "Yes", "Integer >= 0",
            "Non-negative integer", "Voucher Inventory Service",
            "Internal", "Inventory stockout alerting and automated replenishment triggering", "Proposed"
        ),
        (
            "Rewards_Catalog", "partner_merchant", "String",
            "Merchant brand fulfilling the redemption item",
            "Amazon", "Yes", "Controlled list: Amazon, Flipkart, Swiggy, Google Play, UPI",
            "Controlled merchant list; non-null", "Merchant Partner Registry",
            "Public", "Brand affinity benchmarking, merchant spend share, and partnership prioritization", "Proposed"
        ),
        (
            "Event", "timestamp", "Datetime",
            "Standard UTC ISO-8601 timestamp emitted by client/server event payloads representing occurrence time (synonymous with event_datetime)",
            "2026-03-01T10:16:12Z", "Yes", "ISO-8601 UTC datetime string",
            "Valid ISO-8601 UTC timestamp", "Server Clock / Client Telemetry SDK",
            "Internal", "Primary event timestamp for sequence reconstruction, velocity, and time-series aggregation", "Proposed"
        ),
        (
            "Event", "duration_seconds", "Integer",
            "Elapsed duration in seconds for event execution, tutorial progression, or task completion",
            45, "Conditional", "Integer >= 0",
            "Non-negative integer", "Client Telemetry SDK / Task Engine",
            "Internal", "UX friction measurement, task engagement depth, and dwell time analysis", "Proposed"
        ),
        (
            "Event", "registration_method", "String",
            "Event payload telemetry attribute emitted on user_registered",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on user_registered ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for user_registered analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "source", "String",
            "Event payload telemetry attribute emitted on user_registered, reward_credited",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on user_registered, reward_credited ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for user_registered, reward_credited analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "login_method", "String",
            "Event payload telemetry attribute emitted on user_logged_in",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on user_logged_in ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for user_logged_in analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "device_type", "String",
            "Event payload telemetry attribute emitted on user_logged_in",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on user_logged_in ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for user_logged_in analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reason", "String",
            "Event payload telemetry attribute emitted on user_logged_out",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on user_logged_out ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for user_logged_out analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "tutorial_version", "String",
            "Event payload telemetry attribute emitted on onboarding_started",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on onboarding_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for onboarding_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "initial_screen", "String",
            "Event payload telemetry attribute emitted on onboarding_started",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on onboarding_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for onboarding_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "completion_type", "String",
            "Event payload telemetry attribute emitted on onboarding_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on onboarding_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for onboarding_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "steps_viewed", "Integer",
            "Event payload telemetry attribute emitted on onboarding_completed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on onboarding_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for onboarding_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "task_type", "String",
            "Event payload telemetry attribute emitted on task_viewed, task_opened",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on task_viewed, task_opened ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for task_viewed, task_opened analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reward_amount", "Integer",
            "Event payload telemetry attribute emitted on reward_credited, daily_reward_claimed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on reward_credited, daily_reward_claimed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for reward_credited, daily_reward_claimed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "hold_id", "String",
            "Event payload telemetry attribute emitted on reward_pending",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on reward_pending ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for reward_pending analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "expected_amount", "Integer",
            "Event payload telemetry attribute emitted on reward_pending",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on reward_pending ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for reward_pending analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reversal_id", "String",
            "Event payload telemetry attribute emitted on reward_reversed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on reward_reversed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for reward_reversed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "original_transaction_id", "String",
            "Event payload telemetry attribute emitted on reward_reversed, wallet_transaction_reversed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on reward_reversed, wallet_transaction_reversed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for reward_reversed, wallet_transaction_reversed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "clawback_amount", "Integer",
            "Event payload telemetry attribute emitted on reward_reversed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on reward_reversed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for reward_reversed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "claim_day", "Integer",
            "Event payload telemetry attribute emitted on daily_reward_claimed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on daily_reward_claimed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for daily_reward_claimed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "current_streak", "Integer",
            "Event payload telemetry attribute emitted on streak_updated",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_updated ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_updated analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "previous_streak", "Integer",
            "Event payload telemetry attribute emitted on streak_updated",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_updated ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_updated analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "mission_id", "String",
            "Event payload telemetry attribute emitted on mission_started, mission_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on mission_started, mission_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mission_started, mission_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "mission_type", "String",
            "Event payload telemetry attribute emitted on mission_started, mission_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on mission_started, mission_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mission_started, mission_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "target_requirement", "Integer",
            "Event payload telemetry attribute emitted on mission_started",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on mission_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mission_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "badge_id", "String",
            "Event payload telemetry attribute emitted on badge_earned",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on badge_earned ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for badge_earned analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "badge_name", "String",
            "Event payload telemetry attribute emitted on badge_earned",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on badge_earned ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for badge_earned analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "badge_tier", "String",
            "Event payload telemetry attribute emitted on badge_earned",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on badge_earned ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for badge_earned analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "spin_id", "String",
            "Event payload telemetry attribute emitted on spin_started, spin_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on spin_started, spin_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for spin_started, spin_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "spin_cost_xp", "Integer",
            "Event payload telemetry attribute emitted on spin_started",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on spin_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for spin_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "prize_type", "String",
            "Event payload telemetry attribute emitted on spin_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on spin_completed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for spin_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "prize_value", "Integer",
            "Event payload telemetry attribute emitted on spin_completed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on spin_completed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for spin_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "activation_timestamp", "String",
            "Event payload telemetry attribute emitted on referral_activated",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on referral_activated ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for referral_activated analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "bounty_xp", "Integer",
            "Event payload telemetry attribute emitted on referral_converted",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on referral_converted ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for referral_converted analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reversal_transaction_id", "String",
            "Event payload telemetry attribute emitted on wallet_transaction_reversed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on wallet_transaction_reversed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for wallet_transaction_reversed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "dispatched_at", "String",
            "Event payload telemetry attribute emitted on withdrawal_processing",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on withdrawal_processing ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for withdrawal_processing analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reversal_amount_inr", "Float",
            "Event payload telemetry attribute emitted on withdrawal_reversed",
            10.5, "Yes", "Valid Float value formatted per event contract",
            "Non-null on withdrawal_reversed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for withdrawal_reversed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "screen_name", "String",
            "Event payload telemetry attribute emitted on daily_reward_viewed, wallet_viewed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on daily_reward_viewed, wallet_viewed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for daily_reward_viewed, wallet_viewed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "streak_days", "Integer",
            "Event payload telemetry attribute emitted on streak_claimed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_claimed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_claimed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "broken_streak_length", "Integer",
            "Event payload telemetry attribute emitted on streak_broken",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_broken ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_broken analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "last_active_date", "String",
            "Event payload telemetry attribute emitted on streak_broken",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on streak_broken ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_broken analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "streak_count", "Integer",
            "Event payload telemetry attribute emitted on streak_viewed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_viewed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_viewed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "next_milestone_days", "Integer",
            "Event payload telemetry attribute emitted on streak_viewed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on streak_viewed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for streak_viewed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "ad_network", "String",
            "Event payload telemetry attribute emitted on ad_started, ad_completed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on ad_started, ad_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_started, ad_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "ad_unit_id", "String",
            "Event payload telemetry attribute emitted on ad_started",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on ad_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "placement", "String",
            "Event payload telemetry attribute emitted on ad_started",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on ad_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "ad_duration_seconds", "Integer",
            "Event payload telemetry attribute emitted on ad_completed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on ad_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "reward_granted", "Boolean",
            "Event payload telemetry attribute emitted on ad_completed",
            "True", "Yes", "Valid Boolean value formatted per event contract",
            "Non-null on ad_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "watched_seconds", "Integer",
            "Event payload telemetry attribute emitted on ad_skipped",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on ad_skipped ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_skipped analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "total_seconds", "Integer",
            "Event payload telemetry attribute emitted on ad_skipped",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on ad_skipped ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for ad_skipped analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "game_mode", "String",
            "Event payload telemetry attribute emitted on tap_started",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on tap_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for tap_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "energy_level", "Integer",
            "Event payload telemetry attribute emitted on tap_started",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on tap_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for tap_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "taps_count", "Integer",
            "Event payload telemetry attribute emitted on tap_completed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on tap_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for tap_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "points_earned", "Integer",
            "Event payload telemetry attribute emitted on tap_completed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on tap_completed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for tap_completed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "cycle_duration_hours", "Integer",
            "Event payload telemetry attribute emitted on mining_started",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on mining_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mining_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "hash_rate", "Float",
            "Event payload telemetry attribute emitted on mining_started",
            10.5, "Yes", "Valid Float value formatted per event contract",
            "Non-null on mining_started ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mining_started analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "tokens_mined", "Float",
            "Event payload telemetry attribute emitted on mining_stopped",
            10.5, "Yes", "Valid Float value formatted per event contract",
            "Non-null on mining_stopped ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mining_stopped analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "actual_duration_hours", "Float",
            "Event payload telemetry attribute emitted on mining_stopped",
            10.5, "Yes", "Valid Float value formatted per event contract",
            "Non-null on mining_stopped ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mining_stopped analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "claimed", "Boolean",
            "Event payload telemetry attribute emitted on mining_stopped",
            "True", "Yes", "Valid Boolean value formatted per event contract",
            "Non-null on mining_stopped ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for mining_stopped analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "leaderboard_type", "String",
            "Event payload telemetry attribute emitted on leaderboard_viewed",
            "TEST_VAL", "Yes", "Valid String value formatted per event contract",
            "Non-null on leaderboard_viewed ingress", "Client / Server Telemetry SDK",
            "Internal", "Required attribute for leaderboard_viewed analytics and KPI calculation", "Proposed"
        ),
        (
            "Event", "user_rank", "Integer",
            "Event payload telemetry attribute emitted on leaderboard_viewed",
            100, "Yes", "Valid Integer value formatted per event contract",
            "Non-null on leaderboard_viewed ingress", "Client / Server Telemetry SDK",
            "Restricted", "Required attribute for leaderboard_viewed analytics and KPI calculation", "Proposed"
        ),
    ]

    # Verify count
    print(f"Total catalog fields defined: {len(fields_data)}")

    # ----------------------------------------------------
    # Styling Setup
    # ----------------------------------------------------
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # ----------------------------------------------------
    # Sheet 1: Coverage
    # ----------------------------------------------------
    ws_cov = wb.active
    ws_cov.title = "Coverage"

    # Notes section at the top (merged cell A1:E2)
    notes_text = (
        "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Definitions marked "
        "'Proposed' are design recommendations, not existing implementations."
    )
    ws_cov.merge_cells("A1:E2")
    cell_notes = ws_cov["A1"]
    cell_notes.value = notes_text
    cell_notes.font = Font(name="Calibri", size=11, bold=True, color="C00000")
    cell_notes.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell_notes.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
    
    # Border for merged note
    for row in range(1, 3):
        for col in range(1, 6):
            ws_cov.cell(row=row, column=col).border = border_thin

    # Compute coverage breakdown
    entity_stats = {}
    for item in fields_data:
        entity = item[0]
        status = item[11]
        if entity not in entity_stats:
            entity_stats[entity] = {"Confirmed": 0, "Proposed": 0, "To Be Verified": 0, "Total": 0}
        entity_stats[entity][status] += 1
        entity_stats[entity]["Total"] += 1

    cov_headers = ["Entity", "Confirmed Fields", "Proposed Fields", "To Be Verified Fields", "Total Fields"]
    start_row = 4
    for col_idx, h in enumerate(cov_headers, start=1):
        cell = ws_cov.cell(row=start_row, column=col_idx)
        cell.value = h
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    curr_row = start_row + 1
    total_conf = 0
    total_prop = 0
    total_tbv = 0
    total_all = 0

    for entity, stats in entity_stats.items():
        ws_cov.cell(row=curr_row, column=1, value=entity).alignment = Alignment(horizontal="left")
        ws_cov.cell(row=curr_row, column=2, value=stats["Confirmed"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=3, value=stats["Proposed"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=4, value=stats["To Be Verified"]).alignment = Alignment(horizontal="center")
        ws_cov.cell(row=curr_row, column=5, value=stats["Total"]).alignment = Alignment(horizontal="center")
        
        for c in range(1, 6):
            cell = ws_cov.cell(row=curr_row, column=c)
            cell.font = data_font
            cell.border = border_thin
            
        total_conf += stats["Confirmed"]
        total_prop += stats["Proposed"]
        total_tbv += stats["To Be Verified"]
        total_all += stats["Total"]
        curr_row += 1

    # Total Row
    ws_cov.cell(row=curr_row, column=1, value="TOTAL ALL ENTITIES")
    ws_cov.cell(row=curr_row, column=2, value=total_conf)
    ws_cov.cell(row=curr_row, column=3, value=total_prop)
    ws_cov.cell(row=curr_row, column=4, value=total_tbv)
    ws_cov.cell(row=curr_row, column=5, value=total_all)
    
    total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    for c in range(1, 6):
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
    ws_cov.cell(row=summary_box_row, column=1, value="Overall Implementation Split:")
    ws_cov.cell(row=summary_box_row, column=1).font = Font(name="Calibri", size=11, bold=True)
    
    ratios = [
        ("Confirmed Fields (In Simulated Data)", f"{total_conf} ({total_conf/total_all*100:.1f}%)"),
        ("Proposed Fields (Production Architecture)", f"{total_prop} ({total_prop/total_all*100:.1f}%)"),
        ("To Be Verified (Ambiguity / Discrepancies)", f"{total_tbv} ({total_tbv/total_all*100:.1f}%)")
    ]
    for idx, (label, val_str) in enumerate(ratios, start=1):
        r_idx = summary_box_row + idx
        ws_cov.cell(row=r_idx, column=1, value=label).font = data_font
        ws_cov.cell(row=r_idx, column=2, value=val_str).font = Font(name="Calibri", size=10, bold=True)

    # Auto-adjust column widths for Coverage sheet
    ws_cov.column_dimensions["A"].width = 30
    ws_cov.column_dimensions["B"].width = 20
    ws_cov.column_dimensions["C"].width = 20
    ws_cov.column_dimensions["D"].width = 24
    ws_cov.column_dimensions["E"].width = 16

    # ----------------------------------------------------
    # Sheet 2: Fields
    # ----------------------------------------------------
    ws_fields = wb.create_sheet(title="Fields")
    fields_headers = [
        "Entity", "Field Name", "Data Type", "Definition", "Example", "Required",
        "Allowed Values", "Validation", "Source", "Sensitivity", "Analytical Use", "Status"
    ]
    
    ws_fields.append(fields_headers)
    for col_idx in range(1, len(fields_headers) + 1):
        cell = ws_fields.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for row_idx, item in enumerate(fields_data, start=2):
        ws_fields.append(list(item))
        for col_idx in range(1, len(fields_headers) + 1):
            cell = ws_fields.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            # Alignment rules
            if col_idx in (1, 3, 6, 10, 12):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in (2, 5):
                cell.alignment = Alignment(horizontal="left", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                
            # Sensitivity color accents
            if col_idx == 10:
                sens = str(cell.value)
                if sens == "Restricted":
                    cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C65911")
                elif sens == "Internal":
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, color="7F6000")
                elif sens == "Public":
                    cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, color="375623")

            # Status color accents
            if col_idx == 12:
                stat = str(cell.value)
                if stat == "Confirmed":
                    cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="375623")
                elif stat == "Proposed":
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="7F6000")
                elif stat == "To Be Verified":
                    cell.fill = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color="C00000")

    ws_fields.freeze_panes = "C2"
    ws_fields.auto_filter.ref = ws_fields.dimensions

    # Auto-adjust column widths for Fields sheet
    col_widths = {
        "A": 18, # Entity
        "B": 26, # Field Name
        "C": 14, # Data Type
        "D": 45, # Definition
        "E": 26, # Example
        "F": 12, # Required
        "G": 35, # Allowed Values
        "H": 35, # Validation
        "I": 24, # Source
        "J": 14, # Sensitivity
        "K": 45, # Analytical Use
        "L": 16  # Status
    }
    for col_letter, width in col_widths.items():
        ws_fields.column_dimensions[col_letter].width = width

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
        "All data schemas, field definitions, and entity relationships in this data dictionary "
        "reflect simulated testing environments and proposed architectural models. Definitions marked "
        "'Proposed' are design recommendations, not existing implementations."
    )
    ws_notice["A4"].font = Font(name="Calibri", size=10)
    ws_notice.column_dimensions["A"].width = 85

    output_path = "05_data_model/data_dictionary.xlsx"
    wb.save(output_path)
    print(f"Successfully generated {output_path} with {len(fields_data)} fields.")

if __name__ == "__main__":
    build_data_dictionary()
