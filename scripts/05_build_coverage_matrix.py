"""
Script: scripts/05_build_coverage_matrix.py
Purpose: Build 02_product_audit/data_coverage_matrix.xlsx,
         create 02_product_audit/product_data_audit.md,
         and append Gap Analysis Table to 02_product_audit/analytics_gaps.md.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_data_coverage_matrix():
    matrix_rows = [
        # 1. Registration
        ("Registration", "User Sign-up", "Submits registration form via email/credential or OAuth", "Creates user record, hashes credentials, generates user_id", "New user registered, acquisition recorded", "user_id, email, acquisition_source, device, timestamp", "user_registered", "01_Users_1000 / Users_1000_Clean", "What is the daily signup velocity by acquisition channel?", "Confirmed", "Critical"),
        ("Registration", "Email Verification", "Receives verification email and clicks tokenized link", "Validates verification token, updates verification_status to Verified", "Account verified, spam resistance improved", "user_id, token, verified_datetime", "email_verified", "Users_1000_Clean (email_verification_status)", "What percentage of users verify their email within 24 hours?", "Confirmed", "High"),
        
        # 2. Login
        ("Login", "Session Authentication", "Opens application, enters credentials or uses biometrics", "Validates session token, generates session_id, updates last_login", "Active session initialized, user authenticated", "session_id, user_id, session_start, device, platform", "user_logged_in", "02_Sessions (session_id, user_id, session_start)", "What is the daily login frequency and distribution by device?", "Confirmed", "Critical"),
        ("Login", "Session Termination", "Exits application, switches to background, or closes tab", "Computes session_duration_seconds, logs exit_feature, closes session", "Session container closed, engagement duration recorded", "session_id, session_end, session_duration_seconds, exit_feature", "session_ended", "02_Sessions (session_end, exit_feature)", "Where do users most frequently drop off when exiting the app?", "Confirmed", "High"),

        # 3. Onboarding
        ("Onboarding", "Onboarding Flow", "Initiates multi-step profile setup wizard post-registration", "Serves onboarding steps, tracks progression, sets onboarding_status", "User activated, baseline demographic preferences captured", "user_id, step_name, step_number, onboarding_status", "onboarding_step_completed", "Users_1000_Clean (onboarding_status)", "At which onboarding step do users abandon profile completion?", "Proposed", "High"),
        ("Onboarding", "Onboarding Completion", "Completes final tutorial step and enters main app dashboard", "Awards onboarding completion XP, updates onboarding_status to Completed", "User fully activated and ready for micro-task monetization", "user_id, completed_at, bonus_xp_awarded", "onboarding_completed", "Users_1000_Clean (onboarding_status)", "Does completing onboarding lift Day-7 task engagement?", "Confirmed", "Critical"),

        # 4. Watch Ads / Offers
        ("Watch Ads / Offers", "Ad Impression", "Views available video ads and offerwall sponsor cards", "Fetches rewarded video ad units from ad mediation partner", "Ad inventory displayed to user", "user_id, ad_unit_id, placement, timestamp", "ad_card_viewed", "03_Feature_Events (feature_name='Watch Ads')", "Which ad placements generate the highest clickthrough rates?", "Confirmed", "Medium"),
        ("Watch Ads / Offers", "Ad Playback", "Watches video ad to full completion (e.g. 30 seconds)", "Tracks video progress milestones (start, 25%, 50%, 75%, 100%)", "Monetizable rewarded ad impression verified with ad network", "session_id, user_id, ad_network, duration_watched", "ad_playback_completed", "03_Feature_Events (event_name='ad_completed')", "What is the video ad completion rate across Android vs iOS?", "Confirmed", "Critical"),
        ("Watch Ads / Offers", "Ad Reward Crediting", "Claims reward post-ad playback completion", "Credits reward points/XP to user balance via wallet engine", "User rewarded, publisher monetization earned", "user_id, event_id, reward_amount_xp, timestamp", "ad_reward_credited", "03_Feature_Events (reward_related_flag='Yes')", "What is the eCPM and average points earned per user ad session?", "Proposed", "Critical"),

        # 5. Daily Rewards
        ("Daily Rewards", "Daily Check-in View", "Navigates to Daily Reward check-in calendar surface", "Checks user daily claim status and streak count", "Daily reward surface impression logged", "user_id, session_id, current_streak_days, timestamp", "daily_reward_viewed", "03_Feature_Events (feature_name='Daily Reward')", "What proportion of DAU check the daily reward tab?", "Confirmed", "Medium"),
        ("Daily Rewards", "Daily Claim", "Clicks 'Claim Today's Reward' button", "Validates 24h eligibility window, increments streak, credits XP", "Habit formation reinforced, daily retention recorded", "user_id, claim_date, streak_count, reward_xp", "daily_reward_claimed", "04_Daily_Activity (daily_reward_claimed='Yes')", "How does daily reward claiming correlate with Day-30 retention?", "Confirmed", "Critical"),

        # 6. Tap & Earn
        ("Tap & Earn", "Tap Interaction", "Taps energy core / coin button rapidly to harvest points", "Decrements energy balance, increments accumulated taps", "Micro-engagement generated, in-session playtime extended", "session_id, user_id, tap_count, energy_consumed", "tap_action_executed", "03_Feature_Events (feature_name='Tap & Earn')", "What is the average number of taps per active session?", "Confirmed", "Medium"),
        ("Tap & Earn", "Tap Payout Claim", "Submits collected tap score to redeem for points", "Validates click velocity against anti-macro bot rules, credits points", "Safe point disbursement without click-fraud", "user_id, taps_submitted, points_awarded, timestamp", "tap_reward_claimed", "03_Feature_Events (reward_related_flag='Yes')", "What percentage of tap sessions trigger fraud velocity limits?", "Proposed", "High"),

        # 7. Mining
        ("Mining", "Mining Start", "Activates simulated cloud mining session / passive node", "Initiates passive yield timer (e.g. 8-hour mining countdown)", "Passive yield engine started, re-engagement hook established", "user_id, mining_rate, duration_hours, start_time", "mining_session_started", "03_Feature_Events (feature_name='Mining Rewards')", "What is the daily activation rate of passive mining nodes?", "Confirmed", "Medium"),
        ("Mining", "Mining Harvest", "Returns to app after countdown to claim mined points", "Computes accrued yield, resets timer, credits balance", "User re-engaged via push notification hook", "user_id, mined_amount_xp, session_id, timestamp", "mining_yield_claimed", "03_Feature_Events (event_name='mining_claimed')", "What is the claiming latency after a mining cycle ends?", "Confirmed", "High"),

        # 8. Spin the Wheel
        ("Spin the Wheel", "Wheel Access", "Navigates to Spin the Wheel mini-game screen", "Verifies available free daily spin or ticket balance", "Mini-game impression recorded", "user_id, available_spins, timestamp", "spin_screen_viewed", "03_Feature_Events (feature_name='Spin the Wheel')", "What is the daily participation rate in the spin mini-game?", "Confirmed", "Medium"),
        ("Spin the Wheel", "Wheel Spin Action", "Taps 'Spin' button to trigger lucky wheel animation", "Evaluates weighted RNG prize table, deducts ticket, returns prize", "Gamified reward delivered, suspense experience created", "session_id, user_id, prize_tier, prize_xp_value, ticket_cost", "wheel_spun", "03_Feature_Events (event_name='spin_completed')", "What is the distribution of prize payouts versus theoretical RTP?", "Confirmed", "High"),

        # 9. Tasks
        ("Tasks", "Task Discovery", "Scrolls through available micro-task catalog cards", "Fetches active tasks from partner APIs (Surveys, Games, Installs)", "Task catalog impressions logged", "user_id, task_id, task_category, list_position", "task_viewed", "05_Task_Activity (task_viewed_at)", "Which task categories generate the highest clickthrough rates?", "Confirmed", "High"),
        ("Tasks", "Task Initiation", "Clicks 'Start Task' and opens third-party game or survey", "Sets task_status to Started, logs task_started_at timestamp", "User engagement initiated with external advertiser partner", "activity_id, user_id, task_id, task_category, timestamp", "task_started", "05_Task_Activity (task_started_at)", "What is the drop-off rate between task viewed and task started?", "Confirmed", "Critical"),
        ("Tasks", "Task Completion", "Completes all survey questions or reaches target game level", "Receives partner server-to-server postback / client callback", "Micro-task objective fulfilled by user", "activity_id, user_id, task_id, task_completed_at", "task_completed", "05_Task_Activity (task_completed_at)", "What is the overall task completion rate across categories?", "Confirmed", "Critical"),
        ("Tasks", "Task Failure / Abandonment", "Exits survey early or experiences partner verification failure", "Logs failure_reason, updates task_status to Failed or Abandoned", "Task funnel friction identified, partner SLA monitored", "activity_id, task_status, failure_reason, timestamp", "task_failed", "05_Task_Activity (failure_reason, task_status)", "What are the primary failure reasons causing task drop-offs?", "Confirmed", "Critical"),

        # 10. Missions
        ("Missions", "Mission Progress Tracking", "Views daily/weekly achievement mission objectives", "Calculates user event counters against mission goal criteria", "Goal-gradient motivation triggered", "user_id, mission_id, target_goal, current_progress", "mission_viewed", "03_Feature_Events (feature_name='Missions')", "What percentage of active users engage with daily missions?", "Confirmed", "Medium"),
        ("Missions", "Mission Completion", "Reaches 100% mission goal (e.g. 'Complete 3 tasks today')", "Validates completion, unlocks mission reward tier", "Engagement milestone achieved, retention reinforced", "user_id, mission_id, reward_xp, completed_at", "mission_completed", "06_Milestones (milestone_type='first_mission')", "How many missions does an average retained user complete weekly?", "Confirmed", "High"),

        # 11. Badges
        ("Badges", "Badge Catalog View", "Opens profile achievements / trophies showcase", "Renders unlocked vs locked badge criteria", "Status and prestige motivation signaled to user", "user_id, badges_unlocked_count, timestamp", "badges_catalog_viewed", "03_Feature_Events (feature_name='Badges')", "Does badge viewing correlate with higher long-term retention?", "Confirmed", "Low"),
        ("Badges", "Badge Unlock", "Satisfies specific behavioral milestone (e.g. 100 tasks done)", "Awards commemorative badge NFT/token, publishes to profile", "User achievement solidified, social bragging rights enabled", "user_id, badge_id, badge_name, unlocked_at", "badge_unlocked", "06_Milestones (milestone_type='level_up')", "What is the time-to-unlock for the top 5 rarest badges?", "Confirmed", "Medium"),

        # 12. Levels (Level System)
        ("Levels", "Level Progress Check", "Inspects current XP progress bar towards next tier", "Calculates required XP delta and next tier benefits", "Progression visibility provided to motivate action", "user_id, current_level, current_xp, next_level_xp", "level_status_viewed", "03_Feature_Events (feature_name='Level System')", "At which level tiers do users experience engagement plateaus?", "Confirmed", "Medium"),
        ("Levels", "Level Up Achievement", "Crosses threshold points required for tier upgrade", "Increments user_tier, boosts earning multipliers, unlocks perks", "User status upgraded, platform lifetime value increased", "user_id, previous_level, new_level, multiplier_boost", "level_up_achieved", "06_Milestones (milestone_type='level_up')", "What is the cohort progression velocity from Level 1 to Level 5?", "Confirmed", "High"),

        # 13. Referrals
        ("Referrals", "Referral Hub View", "Navigates to 'Invite Friends & Earn' dashboard surface", "Generates personalized referral_code and deep-link URL", "Viral acquisition loop surface presented to user", "user_id, referral_code, available_invite_bonus", "referral_screen_viewed", "03_Feature_Events (feature_name='Referral')", "What percentage of active users view their referral link?", "Confirmed", "High"),
        ("Referrals", "Share Link Action", "Taps share button to distribute link via WhatsApp / Telegram", "Launches native OS share sheet with tracking UTM parameters", "Outbound viral distribution initiated", "user_id, share_channel, share_link_url, timestamp", "referral_link_shared", "Proposed (Referral_Invites Table)", "Which social channel generates the highest referral share volume?", "Proposed", "Critical"),
        ("Referrals", "Referee Attribution", "New user signs up using invite link or enters referral code", "Links referee to referrer_id, validates anti-self-referral rules", "Viral loop closed, acquisition attribution established", "referrer_id, referee_id, referral_code, converted_at", "referral_referee_converted", "Users_1000_Clean (acquisition_source='Referral')", "What is the viral K-factor and invite-to-install conversion rate?", "Confirmed", "Critical"),

        # 14. Wallet
        ("Wallet", "Balance Check", "Navigates to Wallet balance and financial summary screen", "Fetches current ledger balance, pending points, and INR estimate", "Financial transparent state displayed to user", "user_id, current_xp_balance, inr_equivalent, timestamp", "wallet_viewed", "03_Feature_Events (feature_name='Wallet')", "How frequently do users inspect their balance before withdrawing?", "Confirmed", "High"),
        ("Wallet", "Ledger Transaction Crediting", "Completes earning activity requiring wallet balance credit", "Generates immutable credit entry with reference_id, updates balance", "Balance credited safely with complete audit provenance", "transaction_id, user_id, amount_xp, balance_after, reference_id", "wallet_points_credited", "Proposed (Wallet_Ledger Table)", "What is the total daily points issuance and liability accrual?", "Proposed", "Critical"),
        ("Wallet", "Ledger Transaction Debiting", "Spends points on reward redemption or initiates withdrawal", "Generates debit entry, verifies non-negative balance constraint", "Points consumed, platform liability reduced", "transaction_id, user_id, amount_xp, balance_after, reason", "wallet_points_debited", "Proposed (Wallet_Ledger Table)", "What is the points velocity and burn-to-earn ratio?", "Proposed", "Critical"),

        # 15. Exchange Center
        ("Exchange Center", "Catalog Browsing", "Browses gift vouchers, brand cards, and merchandise", "Fetches reward catalog items, point costs, and stock status", "Redemption intent stimulated", "user_id, category_filter, catalog_item_id, timestamp", "exchange_catalog_viewed", "03_Feature_Events (feature_name='Exchange Center')", "Which reward categories attract the highest browsing interest?", "Confirmed", "Medium"),
        ("Exchange Center", "Order Placement", "Selects gift voucher (e.g. Amazon ₹100) and confirms trade", "Verifies XP balance, reserves stock, creates redemption order", "Redemption order created, points deducted from wallet", "order_id, user_id, reward_id, cost_xp, order_status", "exchange_order_placed", "Proposed (Reward_Redemptions Table)", "What is the average order value and reward point price elasticity?", "Proposed", "Critical"),

        # 16. Withdrawals
        ("Withdrawals", "Withdrawal Hub View", "Opens withdrawal screen and selects payout method (UPI, Bank)", "Verifies minimum withdrawal threshold (e.g. ₹50) and KYC state", "Payout requirements presented, liquidity demand captured", "user_id, eligible_balance_inr, kyc_status, min_threshold", "withdrawal_screen_viewed", "Proposed (Withdrawals UI)", "What percentage of users check withdrawals before reaching min threshold?", "Proposed", "High"),
        ("Withdrawals", "Payout Request Submission", "Enters UPI ID / account details, inputs amount, submits request", "Deducts points from wallet, sets status=Pending, queues for gateway", "Formal payout claim lodged, fraud risk checks triggered", "withdrawal_id, user_id, amount_inr, xp_deducted, upi_id_hash", "withdrawal_requested", "Proposed (Withdrawals Table)", "What is the daily liquidity cash-out demand across payment methods?", "Proposed", "Critical"),
        ("Withdrawals", "Gateway Disbursement", "Receives cash credit via payment gateway webhook", "Gateway dispatches funds, updates status=Success, sends alert", "Disbursement completed, user liquidity fulfilled", "withdrawal_id, gateway_ref, completed_at, fee_inr", "withdrawal_disbursed", "Proposed (Withdrawals Table)", "What is the average payout cycle time and gateway failure rate?", "Proposed", "Critical"),
        ("Withdrawals", "Disbursement Failure", "Bank declines transaction or invalid UPI ID rejected", "Reverses points back to user wallet, updates status=Failed", "Failed transaction resolved, user notified to update details", "withdrawal_id, failure_code, failure_reason, reversed_at", "withdrawal_failed", "Proposed (Withdrawals Table)", "What are the leading technical failure reasons on payout gateways?", "Proposed", "High"),

        # 17. Help Center
        ("Help Center", "FAQ / Article Search", "Opens support center and searches for reward withdrawal FAQ", "Serves knowledge base articles, tracks search query terms", "Self-service resolution enabled, support deflection achieved", "user_id, search_query, article_id, category", "help_article_viewed", "Proposed (Help_Center)", "What are the most searched customer support topics and friction points?", "Proposed", "Low"),
        ("Help Center", "Support Ticket Creation", "Submits customer support ticket regarding delayed reward", "Creates ticket record, routes to support queue, sends receipt", "Formal support escalation lodged, customer care SLA started", "ticket_id, user_id, issue_category, priority, created_at", "support_ticket_created", "Proposed (Support_Tickets)", "What is the average ticket resolution time for payout inquiries?", "Proposed", "Medium")
    ]

    out_xlsx = '02_product_audit/data_coverage_matrix.xlsx'
    print(f"Generating {out_xlsx} (Total rows: {len(matrix_rows)})...")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Coverage"
    ws.views.sheetView[0].showGridLines = True

    # SIMULATED_DATA_NOTICE sheet
    ws_notice = wb.create_sheet(title="SIMULATED_DATA_NOTICE")
    ws_notice.views.sheetView[0].showGridLines = True
    ws_notice["A1"] = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."
    ws_notice["A1"].font = Font(name="Calibri", size=14, bold=True, color="9C0006")
    ws_notice["A3"] = "This workbook contains the comprehensive Data Coverage Matrix auditing product features, user actions, system events, and telemetry feasibility."
    ws_notice["A3"].font = Font(name="Calibri", size=11, italic=True)

    headers = [
        "Product Area", "Feature", "User Action", "System Action",
        "Business Outcome", "Data Required", "Proposed Event Name",
        "Source", "Business Question", "Status", "Priority"
    ]
    ws.append(headers)
    for r in matrix_rows:
        ws.append(list(r))

    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='E0E0E0'),
        right=Side(style='thin', color='E0E0E0'),
        top=Side(style='thin', color='E0E0E0'),
        bottom=Side(style='thin', color='E0E0E0')
    )

    status_styles = {
        'Confirmed': {
            'fill': PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="006100")
        },
        'Proposed': {
            'fill': PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="1F4E79")
        },
        'To Be Verified': {
            'fill': PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="9C6500")
        }
    }

    priority_styles = {
        'Critical': {
            'fill': PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="9C0006")
        },
        'High': {
            'fill': PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="B25900")
        },
        'Medium': {
            'fill': PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="375623")
        },
        'Low': {
            'fill': PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid"),
            'font': Font(name="Calibri", size=10, bold=True, color="595959")
        }
    }

    ws.row_dimensions[1].height = 28
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    for row_idx in range(2, len(matrix_rows) + 2):
        ws.row_dimensions[row_idx].height = 36
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            val = cell.value

            col_name = headers[col_idx - 1]
            if col_name in ('Product Area', 'Feature', 'Status', 'Priority', 'Proposed Event Name'):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

            if col_name == 'Status' and val in status_styles:
                cell.fill = status_styles[val]['fill']
                cell.font = status_styles[val]['font']
            elif col_name == 'Priority' and val in priority_styles:
                cell.fill = priority_styles[val]['fill']
                cell.font = priority_styles[val]['font']

    col_widths = {
        1: 20, # Product Area
        2: 24, # Feature
        3: 38, # User Action
        4: 42, # System Action
        5: 38, # Business Outcome
        6: 35, # Data Required
        7: 28, # Proposed Event Name
        8: 30, # Source
        9: 42, # Business Question
        10: 16,# Status
        11: 14 # Priority
    }
    for col_idx, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.freeze_panes = "A2"
    wb.save(out_xlsx)
    print(f"Successfully saved {out_xlsx} with {len(matrix_rows)} rows!")

    # Build 02_product_audit/product_data_audit.md
    build_product_data_audit_md()

    # Append 10 gaps to 02_product_audit/analytics_gaps.md
    append_gaps_table()

def build_product_data_audit_md():
    out_md = '02_product_audit/product_data_audit.md'
    print(f"Generating {out_md}...")

    content = r"""# VELOOP Rewards — Product Data Audit & Telemetry Coverage

> **CRITICAL GOVERNANCE NOTICE**: All product features, telemetry evaluations, event taxonomies, and coverage statuses documented in this audit reflect **SIMULATED DATA** created for analytical testing and product architecture modeling. No real production telemetry or user PII was evaluated.

---

## 1. Product Areas Audit

### 1.1 Registration
- **User Action**: The prospective user installs or opens the application, selects an authentication provider (Google Sign-In, Email/Auth-Credential, or Phone OTP), enters required profile fields (name, age, gender, state, city), and submits the registration form.
- **System Action**: The backend authentication service creates a new user profile record, assigns an immutable `user_id` (`VLUSR000001`–`VLUSR001000`), logs the `acquisition_source` and UTM referral attributes, hashes security credentials, and generates a verification challenge.
- **Key Outcomes**: Acquisition channel velocity, top-of-funnel signup volume, demographic distribution (age, state, city), and user acquisition cost (CAC) attribution.

### 1.2 Login
- **User Action**: The returning user launches the application, presents biometrics or session credentials, and navigates into the main product viewport.
- **System Action**: The session management service authenticates the user, generates a unique `session_id` (`SESS0000001`–`SESS0007913`), logs client device and OS characteristics, updates `last_login_datetime`, and initializes session timeout counters.
- **Key Outcomes**: Daily and Monthly Active Users (DAU/MAU), session frequency per user, session duration distribution, and device landscape allocation (Android vs. iOS vs. Web).

### 1.3 Onboarding
- **User Action**: The newly registered user progresses through an introductory tutorial explaining earning mechanisms, reward point mechanics, and profile personalization preferences.
- **System Action**: The client app logs milestone step completions, records consent preferences (`consent_status`, `marketing_opt_in`), updates `onboarding_status` (`Completed`, `Started`, `Not Started`), and issues an initial activation XP bonus.
- **Key Outcomes**: Onboarding funnel drop-off rate, time-to-first-earning action, activation rate, and day-0 user drop-off mitigation.

### 1.4 Watch Ads / Offers
- **User Action**: The user selects rewarded video ads or sponsored offerwall cards on the dashboard and watches 15–30 second partner video promotions to full completion.
- **System Action**: The app requests ad unit inventory from third-party mediation SDKs, verifies complete ad playback, triggers an ad network postback validation webhook, and credits reward points to the user.
- **Key Outcomes**: Ad viewability, video completion rate, publisher eCPM revenue yield, and reward point unit economics per impression.

### 1.5 Daily Rewards
- **User Action**: The user visits the daily rewards screen each calendar day and taps the active check-in calendar card to claim their daily bonus.
- **System Action**: The server evaluates the 24-hour eligibility window, verifies unbroken daily continuity, increments `streak_activity`, awards escalating XP prizes, and schedules tomorrow's local push notification reminder.
- **Key Outcomes**: Consecutive day habituation, 7-day streak retention, daily retention cohorts, and push notification return-rate efficacy.

### 1.6 Tap & Earn
- **User Action**: The user repeatedly taps an energetic coin or core graphic on the screen during spare micro-moments to accumulate incremental earning units.
- **System Action**: The client-side gaming engine validates tap velocity against anti-macro bot thresholds, decrements an energy meter, buffers points locally, and syncs aggregated scores to the backend upon session close.
- **Key Outcomes**: Average session length extension, bot/autoclicker fraud rejection rate, engagement depth per active day, and point generation velocity.

### 1.7 Mining
- **User Action**: The user navigates to the passive earning hub, clicks 'Start Mining', and activates an automated cloud-mining cycle that generates points over an 8-hour duration.
- **System Action**: The backend initializes a mining timer, calculates passive yield accumulation based on the user's level multiplier, terminates accumulation upon cycle completion, and triggers a 'Yield Ready' notification.
- **Key Outcomes**: Re-engagement cycle interval, notification claim latency, passive-to-active session conversion, and platform stickiness.

### 1.8 Spin the Wheel
- **User Action**: The user enters the gamified lucky wheel viewport, spends an earned spin ticket or claims their free daily spin, and taps the 'Spin' control.
- **System Action**: The game engine verifies ticket balance, queries a server-side pseudo-random number generator (PRNG) with weighted prize tables, executes the spin visual reel, and credits the won prize.
- **Key Outcomes**: Gamification engagement rate, prize payout distribution vs. theoretical Return-to-Player (RTP), ticket sink velocity, and variable reward dopamine response.

### 1.9 Tasks
- **User Action**: The user browses partner micro-tasks (app testing, surveys, partner game levels), reviews task requirements and reward bounties, and clicks 'Start Task' to navigate to third-party partner surfaces.
- **System Action**: The task engine creates an `activity_id` in `05_Task_Activity`, sets `task_status` to `Started`, monitors completion via advertiser postback webhooks, records `failure_reason` if abandoned, and sets `reward_status` to `Credited` upon verified completion.
- **Key Outcomes**: Task conversion rate, task failure rate, partner advertiser ROI, revenue margin per task category (Games vs. Surveys vs. Installs), and user task churn.

### 1.10 Missions
- **User Action**: The user opens the Missions dashboard to review daily and weekly quest goals (e.g., 'Complete 2 surveys and watch 3 ads').
- **System Action**: The mission service aggregates user event telemetry across features, calculates goal completion percentages, unlocks completed quest tiers, and credits bonus milestone points.
- **Key Outcomes**: Multi-feature engagement cross-pollination, daily mission completion velocity, retention elasticity, and goal-gradient user motivation.

### 1.11 Badges
- **User Action**: The user browses their achievement profile showcase to view earned achievement trophies and review unlock criteria for locked badges.
- **System Action**: The milestone engine evaluates historical event aggregates, identifies achieved threshold criteria, awards permanent badge metadata to the user profile, and triggers a celebratory micro-animation.
- **Key Outcomes**: Long-term intrinsic motivation, status recognition, collection completion rates, and power-user differentiation.

### 1.12 Levels (Level System)
- **User Action**: The user tracks their progressive level bar and tier status (Bronze, Silver, Gold, Platinum) by accumulating cumulative lifetime XP.
- **System Action**: The progression engine checks accumulated points, triggers tier upgrades upon reaching XP milestones, unlocks higher earning multipliers, and adjusts payout maximums.
- **Key Outcomes**: User lifetime progression velocity, level-based retention lift, churn reduction at critical level gates, and long-term user monetization.

### 1.13 Referrals
- **User Action**: The user accesses the Referral Hub, copies their unique `referral_code`, and shares deep links with friends and family across WhatsApp, Telegram, or social media.
- **System Action**: The referral engine tracks outbound share link clicks, attributes referee signups to the inviter `referrer_id`, monitors referee milestone progression, and awards dual-sided bounty bonuses upon qualification.
- **Key Outcomes**: Viral coefficient (K-factor), invite-to-registration conversion rate, referral CAC efficiency, and referee Day-30 retention comparison against organic users.

### 1.14 Wallet
- **User Action**: The user opens the Wallet screen to inspect their real-time XP point balance, review equivalent local fiat valuation (INR), and inspect their earnings breakdown.
- **System Action**: The wallet service calculates net balance from ledger entries, evaluates pending escrow points, verifies point expiration policies, and displays categorized earning summaries.
- **Key Outcomes**: Financial liability tracking, point velocity, user balance accumulation before withdrawal, and platform economic transparency.

### 1.15 Exchange (Exchange Center)
- **User Action**: The user browses the reward voucher catalog, filters by merchant category (e.g., Amazon, Flipkart, Google Play), and places an order to exchange points for digital gift cards.
- **System Action**: The exchange engine checks user available points, reserves merchant inventory, places a redemption order, deducts points from the user's wallet, and delivers the voucher code.
- **Key Outcomes**: Reward catalog popularity, merchant brand affinity, redemption unit margins, and inventory turnover rate.

### 1.16 Withdrawals
- **User Action**: The user navigates to the cash payout section, selects their disbursement destination (UPI ID, IMPS Bank Account, Amazon Pay), enters the desired amount, and submits a payout request.
- **System Action**: The payout orchestrator validates minimum withdrawal thresholds, conducts anti-fraud and device integrity checks, freezes equivalent points, queues the transaction with payment gateway APIs, and logs disbursement status.
- **Key Outcomes**: Cash payout velocity, gateway processing success rate, payout cycle latency (requested-to-disbursed), liquidity demand forecasting, and payout fraud prevention.

### 1.17 Help Center (Support & FAQs)
- **User Action**: The user searches support knowledge base articles regarding delayed rewards or submits a customer support inquiry ticket.
- **System Action**: The support service logs search queries, measures article helpfulness ratings, routes support tickets to customer care queues, and tracks resolution SLAs.
- **Key Outcomes**: Customer issue deflection rate, user friction identification (e.g., failed payouts, task attribution disputes), and support resolution time.

---

## 2. Telemetry Architecture: User Action vs. System Event vs. Business Outcome

High-fidelity analytics requires cleanly separating **User Actions** (client-side intent), **System Events** (backend telemetry and operational logging), and **Business Outcomes** (macro performance, monetization, and liability).

### Conceptual Differentiation

```
[ User Action ]   --> Intent: What the human did on the glass (e.g. taps button)
      │
      ▼
[ System Event ]  --> Telemetry: What code executed, state transitioned, and logged
      │
      ▼
[Business Outcome]--> Impact: Financial, operational, retention, or fraud consequence
```

---

### Worked Lifecycle Example: The VELOOP Micro-Task System

The micro-task earning funnel demonstrates this multi-layer telemetry separation:

```mermaid
sequenceDiagram
    autonumber
    actor User as Simulated User
    participant App as Client Application
    participant Svr as VELOOP Backend Engine
    participant Partner as Third-Party Task Partner

    User->>App: 1. Scrolls and views task catalog
    App->>Svr: Log Telemetry: task_viewed
    Note over Svr: Outcome: Catalog Impression & Discovery

    User->>App: 2. Taps task card to read rules
    App->>Svr: Log Telemetry: task_opened
    Note over Svr: Outcome: Engagement Intent Registered

    User->>App: 3. Clicks 'Start Task'
    App->>Svr: Log Telemetry: task_started (status: Started)
    Svr->>Partner: Hand off user tracking session
    Note over Svr: Outcome: Active Task Commitment

    User->>Partner: 4. Completes task (survey / game level)
    Partner-->>Svr: 5. Server-to-server webhook callback
    Svr->>Svr: Log Telemetry: task_completed (task_completed_at)
    Note over Svr: Outcome: User Effort Fulfilled

    Svr->>Svr: 6. Anti-fraud & completion validation
    Svr->>Svr: Log Telemetry: task_validated (status: Verified)
    Note over Svr: Outcome: Payout Approved & Fraud Discharged

    Svr->>App: 7. Deliver reward points to user
    Svr->>Svr: Log Telemetry: reward_credited (reward_status: Credited)
    Note over Svr: Outcome: Liability Accrued & User Retention Lifted
```

| Lifecycle Stage | User Action (Client Intent) | System Event (Telemetry Logged) | Business Outcome (Impact & Value) |
| :--- | :--- | :--- | :--- |
| **1. Discovery** | User scrolls task feed and views available surveys. | `task_viewed` (`activity_id`, `task_id`, `category`, `position`) | Establishes catalog reach and placement clickthrough baseline. |
| **2. Consideration** | User taps task card to read duration and rules. | `task_opened` (`task_id`, `dwell_time_ms`) | Measures offer attractiveness and title clarity. |
| **3. Commitment** | User clicks 'Start Task' button. | `task_started` (`activity_id`, `user_id`, `task_started_at`) | Measures intent conversion; begins partner billing session. |
| **4. Execution** | User completes survey questions on partner site. | `task_completed` (`activity_id`, `task_completed_at`) | Work finished; initiates partner postback verification. |
| **5. Verification** | System receives partner webhook and audits IP/device. | `task_validated` (`validation_status`, `fraud_score`) | Discharges partner receivable; prevents multi-account fraud. |
| **6. Settlement** | User sees reward points added to in-app wallet. | `reward_credited` (`reward_status = 'Credited'`, `amount_xp`) | Books reward liability; delivers dopamine reward to drive Day-7 retention. |

---

## 3. Measurability Statement Across All 17 Product Areas

Based on rigorous data profiling and referential integrity testing conducted on the supplied datasets (`00_source_data/`), the current instrumentation status of each product area is codified below:

| # | Product Area | Instrumentation Status | Audited Telemetry Source in Simulated Data | Measurement Capability & Residual Gap |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **Registration** | **Already instrumented (per supplied data)** | `01_Users_1000` & `Users_1000_Clean` | Full demographic and acquisition source tracking. Micro-step registration drop-off funnel is proposed. |
| **2** | **Login** | **Already instrumented (per supplied data)** | `02_Sessions` (7,913 records) | Complete session start/end timestamps, durations, and device breakdown. In-app backgrounding heartbeat is proposed. |
| **3** | **Onboarding** | **Already instrumented (per supplied data)** | `Users_1000_Clean` (`onboarding_status`) | Final onboarding status (Completed/Started/Not Started) is confirmed. Step-level funnel telemetry is proposed. |
| **4** | **Watch Ads / Offers** | **Already instrumented (per supplied data)** | `03_Feature_Events` (3,126 events across 836 users) | Ad impression and completion events confirmed. Third-party ad network eCPM reconciliation is proposed. |
| **5** | **Daily Rewards** | **Already instrumented (per supplied data)** | `04_Daily_Activity` (`daily_reward_claimed`, 2,499 events) | Daily check-in claims confirmed. Calendar streak freeze/repair tracking is proposed. |
| **6** | **Tap & Earn** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,654 events across 800 users) | Micro-game engagement confirmed. Server-side tap velocity bot-filtering telemetry is proposed. |
| **7** | **Mining** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,616 events across 799 users) | Passive node interactions confirmed. Yield countdown claim latency telemetry is proposed. |
| **8** | **Spin the Wheel** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,425 events across 763 users) | Mini-game execution confirmed. Prize tier RTP distribution logging is proposed. |
| **9** | **Tasks** | **Already instrumented (per supplied data)** | `05_Task_Activity` (9,846 records across 80 tasks) | Full lifecycle tracking (started, completed, failed, abandoned). Parent `task_master` dimension table is proposed. |
| **10** | **Missions** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,780 events) & `06_Milestones` | Mission engagement and milestone unlocks confirmed. Multi-tiered quest progress telemetry is proposed. |
| **11** | **Badges** | **Already instrumented (per supplied data)** | `03_Feature_Events` (1,832 events across 674 users) | Feature usage confirmed. Rarity and unlock criteria catalog table is proposed. |
| **12** | **Levels** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,427 events) & `06_Milestones` | Level status checks and tier-up milestones confirmed. Dynamic XP tier multiplier tracking is proposed. |
| **13** | **Referrals** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,521 events across 811 users), `Users` | Inbound referee attribution confirmed. Outbound invite links and share channel telemetry are proposed. |
| **14** | **Wallet** | **Already instrumented (per supplied data)** | `03_Feature_Events` (2,172 events), `04_Daily_Activity` | User balance and daily wallet activity confirmed. Double-entry immutable ledger table is proposed. |
| **15** | **Exchange Center** | **Already instrumented (per supplied data)** | `03_Feature_Events` (1,690 events across 720 users) | Exchange catalog interactions confirmed. Order fulfillment and stock ledger tables are proposed. |
| **16** | **Withdrawals** | **Proposed** | *None in supplied data (TABLE MISSING)* | Entirely absent. Full withdrawal request queue and gateway disbursement tables are proposed. |
| **17** | **Help Center** | **Proposed** | *None in supplied data (TABLE MISSING)* | Entirely absent. Support inquiry ticketing and FAQ deflection event telemetry are proposed. |

---

## 4. Data Authenticity Statement
This product data audit and telemetry coverage assessment was prepared using simulated data created for analytical testing and product architecture modeling. No real production data or user PII was accessed, analyzed, or included. All metrics, user counts, and behavioral distributions reflect simulated test environments.
"""

    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated {out_md}!")

def append_gaps_table():
    gaps_file = '02_product_audit/analytics_gaps.md'
    print(f"Appending Comprehensive Gap Table to {gaps_file}...")

    with open(gaps_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    auth_split = existing_content.split('## Data Authenticity Statement')

    gaps_table_section = """
---

## 5. Master Analytics Gaps Register

The following systematic register logs the 12 core telemetry, architectural, and dimensional gaps identified across the VELOOP product analytics foundation:

| Gap ID | Product Area | Identified Telemetry / Data Gap | Impact on Reporting & Analytics | Priority | Underlying Technical Reason |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **GAP-001** | **Wallet** | Lack of an immutable double-entry wallet transactions ledger | Inability to reconstruct running balances over time, audit point breakage, reconcile liability, or model point economy inflation. | **Critical** | Supplied dataset only provides a static `xp_balance` snapshot on Users and a binary flag in Daily Activity; no transactional ledger exists. |
| **GAP-002** | **Withdrawals** | Complete absence of withdrawal requests and payout disbursement tables | Total blindness to platform cash burn, payout processing latency, payment gateway failure rates, and liquidity forecasting. | **Critical** | Standalone withdrawal tables were omitted entirely from the source data export. |
| **GAP-003** | **Referrals** | Missing outbound referral invitations, share channels, and link click tracking | Cannot calculate viral K-factor (invitations sent vs conversions), evaluate share-to-install drop-offs, or identify high-performing share channels. | **Critical** | Telemetry only records referee signups upon arrival; the outbound viral distribution funnel is not instrumented. |
| **GAP-004** | **Rewards Catalog** | Absence of a master reward catalog and redemption order fact table | Inability to evaluate reward SKU popularity, brand affinity (Amazon vs Flipkart), catalog stockouts, or merchant unit economic margins. | **Critical** | Datasets track only aggregate counts of reward events; item-level SKU redemptions are not captured. |
| **GAP-005** | **Tasks** | Missing Task Master dimension table for the 80 distinct `task_id`s in `Task_Activity` | Cannot benchmark task completion rates by difficulty tier, partner advertiser payout rate, or expected duration. | **High** | `05_Task_Activity` contains `task_id` strings (`TASK0001`–`TASK0080`) without a parent dimension catalog table. |
| **GAP-006** | **Telemetry Identity** | Absence of `task_id` attribute in `03_Feature_Events` clickstream table | Cannot join micro-level user clickstream events to specific task attempts to analyze user behavioral friction before task abandonment. | **High** | `Feature_Events` logs generic feature and event names but lacks task entity context in its event schema payload. |
| **GAP-007** | **Fraud & Risk** | Zero telemetry for reward clawbacks, multi-account device hashes, or dispute dispositions | Inability to detect emulator click-farms, calculate net earned vs clawed-back points, or audit anti-bot security filters. | **Critical** | No reversal status values, device hardware identifiers (IMEI/MAC), or fraud disposition codes exist in the data. |
| **GAP-008** | **Onboarding** | Onboarding tracked only as a coarse 3-state profile attribute without step-level funnel events | Product managers cannot identify specific tutorial friction screens causing new user activation drop-offs. | **High** | Only final state (`onboarding_status`) is stored on the user profile; micro-step progress events (`onboarding_step_completed`) are absent. |
| **GAP-009** | **Timezone Standards** | Absence of explicit ISO-8601 UTC designators and client clock synchronization metadata | Daily cohort boundaries, streak calculations, and retention curves may shift depending on whether timestamps are interpreted as UTC or IST. | **Medium** | Timestamps in source tables are unzoned datetime strings without explicit offset metadata (`Z` or `+05:30`). |
| **GAP-010** | **Help Center** | Zero tracking of customer support inquiries, FAQ article views, or ticket resolutions | Inability to identify user friction hot-spots, dispute frequency over failed payouts, or support resolution SLA efficiency. | **Medium** | No customer support ticketing or knowledge base interaction events exist in the telemetry taxonomy. |
| **GAP-011** | **Ad Mediation** | Missing third-party ad mediation postback webhooks and eCPM transaction logs | Cannot reconcile publisher revenue against awarded user points or verify ad viewability against click-fraud. | **High** | Ad views are captured solely via client-side events without third-party server-to-server validation. |
| **GAP-012** | **Observation Horizon** | Snapshot baseline calculation timestamp preceded registration for 8 users, with activity extending past Sept 15 | Produces negative derived metrics (`days_since_registration = -0.8`) and unpartitioned future activity data. | **Medium** | Snapshot date logic was hardcoded without boundary clamping against max registration timestamp in the synthetic generator. |

"""

    final_content = auth_split[0].rstrip() + gaps_table_section + "\n## Data Authenticity Statement" + auth_split[1]

    with open(gaps_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Successfully updated {gaps_file} with Master Gaps Register!")

if __name__ == '__main__':
    build_data_coverage_matrix()
