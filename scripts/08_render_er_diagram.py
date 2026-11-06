#!/usr/bin/env python3
"""
scripts/08_render_er_diagram.py
Renders a publication-grade logical ER Diagram PNG (05_data_model/er_diagram.png)
from the DBML specification using Matplotlib and Pillow.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def render_er_diagram():
    # Setup figure canvas (high resolution, 36 x 22 inches at 150 dpi = 5400 x 3300 px)
    fig, ax = plt.subplots(figsize=(36, 22), dpi=150)
    ax.set_facecolor("#F1F5F9") # slate-100 background
    fig.patch.set_facecolor("#F1F5F9")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # ----------------------------------------------------
    # Header & Governance Banner
    # ----------------------------------------------------
    # Header container
    header_box = patches.FancyBboxPatch(
        (2, 92.5), 96, 6.2,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#0F172A", edgecolor="#1E293B", linewidth=1.5
    )
    ax.add_patch(header_box)
    
    ax.text(
        4, 96.2, "VELOP Rewards — Logical Entity Relationship Diagram (ERD)",
        fontsize=22, fontweight="bold", color="#F8FAFC", va="center"
    )
    ax.text(
        4, 94.0, "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Entities & fields tagged /* proposed */ are design recommendations.",
        fontsize=12, fontweight="normal", color="#94A3B8", va="center"
    )
    
    # Legend in header
    legend_items = [
        ("#1E3A8A", "Confirmed Table"),
        ("#581C87", "Proposed Table"),
        ("#B45309", "[PK] Primary Key"),
        ("#0284C7", "[FK] Foreign Key"),
        ("#2563EB", "1:N Relational Link")
    ]
    lx = 68.0
    for color, label in legend_items:
        dot = patches.Circle((lx, 95.0), 0.6, facecolor=color, edgecolor="none")
        ax.add_patch(dot)
        ax.text(lx + 1.2, 95.0, label, fontsize=10, fontweight="bold", color="#E2E8F0", va="center")
        lx += 5.8

    # ----------------------------------------------------
    # Entity Definitions & Coordinates
    # Grid coordinates: (x, y, width, height) in 0-100 space
    # ----------------------------------------------------
    entities = {
        "Users": {
            "x": 2, "y": 48, "w": 18, "h": 42,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] user_id", "varchar(16)", "#B45309"),
                ("full_name", "varchar(100)", "#334155"),
                ("email", "varchar(150)", "#334155"),
                ("age", "integer", "#334155"),
                ("gender", "varchar(20)", "#334155"),
                ("state", "varchar(50)", "#334155"),
                ("city", "varchar(100)", "#334155"),
                ("registration_datetime", "timestamp", "#334155"),
                ("acquisition_source", "varchar(50)", "#334155"),
                ("referral_source_detail", "varchar(50)", "#334155"),
                ("primary_device", "varchar(30)", "#334155"),
                ("platform", "varchar(30)", "#334155"),
                ("account_status", "varchar(30)", "#334155"),
                ("email_verification_status", "varchar(30)", "#334155"),
                ("onboarding_status", "varchar(30)", "#334155"),
                ("last_login_datetime", "timestamp", "#334155"),
                ("lifetime_sessions", "integer", "#334155"),
                ("active_days", "integer", "#334155"),
                ("xp_balance", "integer", "#334155"),
                ("referral_code", "varchar(20)", "#334155"),
                ("days_since_reg", "float [tbv]", "#C2410C"),
                ("is_active_7d", "varchar(5)", "#334155"),
                ("is_active_30d", "varchar(5)", "#334155"),
                ("consent_status", "varchar(20)", "#334155"),
                ("marketing_opt_in", "varchar(5)", "#334155"),
                ("account_created_via", "varchar(50)", "#334155"),
                ("country", "varchar(50)", "#334155"),
            ]
        },
        "Sessions": {
            "x": 23, "y": 62, "w": 17, "h": 28,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] session_id", "varchar(16)", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("session_start", "timestamp", "#334155"),
                ("session_end", "timestamp", "#334155"),
                ("session_duration_sec", "integer", "#334155"),
                ("device", "varchar(30)", "#334155"),
                ("platform", "varchar(30)", "#334155"),
                ("entry_point", "varchar(50)", "#334155"),
                ("exit_feature", "varchar(50)", "#334155"),
                ("events_in_session", "integer", "#334155"),
                ("features_used_count", "integer", "#334155"),
                ("session_status", "varchar(30)", "#334155"),
            ]
        },
        "Feature_Events": {
            "x": 43, "y": 62, "w": 18, "h": 28,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] event_id", "varchar(16)", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("[FK] session_id", "varchar(16)", "#0284C7"),
                ("event_datetime", "timestamp", "#334155"),
                ("feature_name", "varchar(50)", "#334155"),
                ("event_name", "varchar(50)", "#334155"),
                ("event_status", "varchar(30)", "#334155"),
                ("device", "varchar(30)", "#334155"),
                ("platform", "varchar(30)", "#334155"),
                ("acquisition_source", "varchar(50)", "#334155"),
                ("sequence_number", "integer [tbv]", "#C2410C"),
                ("reward_related_flag", "varchar(5)", "#334155"),
                ("xp_related_flag", "varchar(5)", "#334155"),
            ]
        },
        "Daily_Activity": {
            "x": 64, "y": 57, "w": 17, "h": 33,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] [FK] user_id", "varchar(16)", "#B45309"),
                ("[PK] activity_date", "date", "#B45309"),
                ("session_count", "integer", "#334155"),
                ("session_duration_min", "float", "#334155"),
                ("event_count", "integer", "#334155"),
                ("feature_count", "integer", "#334155"),
                ("task_count", "integer", "#334155"),
                ("completed_task_cnt", "integer", "#334155"),
                ("reward_activity_cnt", "integer", "#334155"),
                ("xp_activity_count", "integer", "#334155"),
                ("streak_activity", "varchar(5)", "#334155"),
                ("daily_reward_claim", "varchar(5)", "#334155"),
                ("mission_activity", "varchar(5)", "#334155"),
                ("spin_activity", "varchar(5)", "#334155"),
                ("referral_activity", "varchar(5)", "#334155"),
                ("wallet_activity", "varchar(5)", "#334155"),
                ("active_flag", "varchar(5)", "#334155"),
            ]
        },
        "Referrals": {
            "x": 83, "y": 57, "w": 15, "h": 33,
            "status": "Proposed", "header_bg": "#581C87",
            "fields": [
                ("[PK] referral_id", "varchar(64) /*p*/", "#B45309"),
                ("[FK] referrer_user_id", "varchar(16)", "#0284C7"),
                ("[FK] referred_user_id", "varchar(16)", "#0284C7"),
                ("referral_code", "varchar(20)", "#334155"),
                ("share_channel", "varchar(50)", "#334155"),
                ("sub_channel", "varchar(100) /*p*/", "#6B21A8"),
                ("created_at", "timestamp /*p*/", "#6B21A8"),
                ("registered_at", "timestamp /*p*/", "#6B21A8"),
                ("activated_at", "timestamp /*p*/", "#6B21A8"),
                ("converted_at", "timestamp /*p*/", "#6B21A8"),
                ("referral_status", "varchar(30) /*p*/", "#6B21A8"),
                ("referrer_bounty_xp", "integer /*p*/", "#6B21A8"),
                ("referred_bonus_xp", "integer /*p*/", "#6B21A8"),
                ("disqualification_rsn", "varchar(50) /*p*/", "#6B21A8"),
            ]
        },
        "Task_Master": {
            "x": 23, "y": 28, "w": 17, "h": 26,
            "status": "Proposed", "header_bg": "#581C87",
            "fields": [
                ("[PK] task_id", "varchar(16) /*p*/", "#B45309"),
                ("task_name", "varchar(150) /*p*/", "#6B21A8"),
                ("task_category", "varchar(50)", "#334155"),
                ("reward_xp", "integer /*p*/", "#6B21A8"),
                ("reward_unit", "varchar(20) /*p*/", "#6B21A8"),
                ("estimated_duration_s", "integer /*p*/", "#6B21A8"),
                ("partner_id", "varchar(50) /*p*/", "#6B21A8"),
                ("partner_campaign_id", "varchar(100) /*p*/", "#6B21A8"),
                ("is_active", "boolean /*p*/", "#6B21A8"),
            ]
        },
        "Task_Activity": {
            "x": 43, "y": 28, "w": 18, "h": 28,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] activity_id", "varchar(16)", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("[FK] task_id", "varchar(16)", "#0284C7"),
                ("task_category", "varchar(50)", "#334155"),
                ("task_viewed_at", "timestamp", "#334155"),
                ("task_started_at", "timestamp", "#334155"),
                ("task_completed_at", "timestamp", "#334155"),
                ("task_status", "varchar(30)", "#334155"),
                ("failure_reason", "varchar(100)", "#334155"),
                ("reward_status", "varchar(30) [tbv]", "#C2410C"),
                ("device", "varchar(30)", "#334155"),
                ("[FK] session_id", "varchar(16)", "#0284C7"),
            ]
        },
        "Milestones": {
            "x": 64, "y": 34, "w": 17, "h": 20,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] milestone_id", "integer (surr)", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("milestone_type", "varchar(50)", "#334155"),
                ("milestone_datetime", "timestamp", "#334155"),
                ("milestone_value", "integer [tbv]", "#C2410C"),
                ("source_event", "varchar(50) [tbv]", "#C2410C"),
                ("[FK] session_id", "varchar(16)", "#0284C7"),
            ]
        },
        "Feature_Usage": {
            "x": 83, "y": 34, "w": 15, "h": 20,
            "status": "Confirmed", "header_bg": "#1E3A8A",
            "fields": [
                ("[PK] feature_name", "varchar(50)", "#B45309"),
                ("unique_users", "integer", "#334155"),
                ("total_events", "integer", "#334155"),
                ("sessions_with_feature", "integer", "#334155"),
                ("users_with_success", "integer", "#334155"),
                ("events_per_user", "float", "#334155"),
                ("sessions_per_user", "float", "#334155"),
            ]
        },
        "Wallet_Transactions": {
            "x": 23, "y": 2, "w": 18, "h": 23,
            "status": "Proposed", "header_bg": "#581C87",
            "fields": [
                ("[PK] transaction_id", "varchar(64) /*p*/", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("transaction_datetime", "timestamp /*p*/", "#6B21A8"),
                ("transaction_type", "varchar(30) /*p*/", "#6B21A8"),
                ("amount", "float /*p*/", "#6B21A8"),
                ("unit", "varchar(20) /*p*/", "#6B21A8"),
                ("status", "varchar(30) /*p*/", "#6B21A8"),
                ("source_feature", "varchar(50) /*p*/", "#6B21A8"),
                ("reference_id", "varchar(64) /*p*/", "#6B21A8"),
                ("reversal_link", "varchar(64) /*p*/", "#6B21A8"),
                ("balance_after", "float /*p*/", "#6B21A8"),
            ]
        },
        "Withdrawals": {
            "x": 44, "y": 2, "w": 20, "h": 23,
            "status": "Proposed", "header_bg": "#581C87",
            "fields": [
                ("[PK] withdrawal_id", "varchar(64) /*p*/", "#B45309"),
                ("[FK] user_id", "varchar(16)", "#0284C7"),
                ("requested_datetime", "timestamp /*p*/", "#6B21A8"),
                ("amount_inr", "float /*p*/", "#6B21A8"),
                ("xp_deducted", "integer /*p*/", "#6B21A8"),
                ("payout_method", "varchar(30) /*p*/", "#6B21A8"),
                ("payout_status", "varchar(30) /*p*/", "#6B21A8"),
                ("gateway_name", "varchar(50) /*p*/", "#6B21A8"),
                ("gateway_reference", "varchar(100) /*p*/", "#6B21A8"),
                ("failure_category", "varchar(50) /*p*/", "#6B21A8"),
                ("payout_account_hash", "varchar(64) /*p*/", "#6B21A8"),
                ("completed_at", "timestamp /*p*/", "#6B21A8"),
            ]
        },
        "Rewards": {
            "x": 67, "y": 2, "w": 18, "h": 23,
            "status": "Proposed", "header_bg": "#581C87",
            "fields": [
                ("[PK] reward_sku", "varchar(50) /*p*/", "#B45309"),
                ("reward_name", "varchar(150) /*p*/", "#6B21A8"),
                ("reward_category", "varchar(50) /*p*/", "#6B21A8"),
                ("cost_xp", "integer /*p*/", "#6B21A8"),
                ("fiat_value_inr", "float /*p*/", "#6B21A8"),
                ("stock_quantity", "integer /*p*/", "#6B21A8"),
                ("partner_merchant", "varchar(100) /*p*/", "#6B21A8"),
            ]
        }
    }

    # Render each entity table box
    for name, ent in entities.items():
        x, y, w, h = ent["x"], ent["y"], ent["w"], ent["h"]
        
        # Outer table container
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.6",
            facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2,
            zorder=2
        )
        ax.add_patch(box)
        
        # Header banner
        header_h = 2.4
        header_box = patches.FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle="round,pad=0.1,rounding_size=0.6",
            facecolor=ent["header_bg"], edgecolor=ent["header_bg"], linewidth=1.0,
            zorder=3
        )
        ax.add_patch(header_box)
        
        # Header text
        tag = " /* proposed */" if ent["status"] == "Proposed" else ""
        ax.text(
            x + 0.8, y + h - (header_h / 2.0),
            f"{name}{tag}",
            fontsize=11, fontweight="bold", color="#FFFFFF", va="center", zorder=4
        )
        
        # Table rows
        n_fields = len(ent["fields"])
        available_h = h - header_h - 0.8
        row_h = available_h / max(n_fields, 1)
        
        for i, (fname, ftype, fcolor) in enumerate(ent["fields"]):
            fy = (y + h - header_h - 0.4) - (i + 0.5) * row_h
            
            # Field name (bold for PK/FK)
            is_key = "[PK]" in fname or "[FK]" in fname
            ax.text(
                x + 0.6, fy, fname,
                fontsize=8.5, fontweight="bold" if is_key else "normal",
                color=fcolor, va="center", zorder=4
            )
            
            # Field data type (right-aligned)
            ax.text(
                x + w - 0.6, fy, ftype,
                fontsize=7.5, fontweight="normal", color="#64748B",
                va="center", ha="right", zorder=4
            )
            
            # Subtle divider line between fields
            if i < n_fields - 1:
                ax.plot(
                    [x + 0.5, x + w - 0.5], [fy - (row_h / 2.0), fy - (row_h / 2.0)],
                    color="#F1F5F9", linewidth=0.6, zorder=3
                )

    # ----------------------------------------------------
    # Relational Connectors & Foreign Key Arrows
    # ----------------------------------------------------
    relationships = [
        # (source_entity, target_entity, source_point, target_point, color, label)
        # Users -> Sessions (1:N)
        ("Users", "Sessions", (20.0, 78.0), (23.0, 78.0), "#2563EB", "1:N"),
        # Users -> Feature_Events (1:N)
        ("Users", "Feature_Events", (20.0, 72.0), (43.0, 72.0), "#2563EB", "1:N"),
        # Sessions -> Feature_Events (1:N)
        ("Sessions", "Feature_Events", (40.0, 75.0), (43.0, 75.0), "#0284C7", "1:N"),
        # Users -> Daily_Activity (1:N)
        ("Users", "Daily_Activity", (20.0, 84.0), (64.0, 84.0), "#2563EB", "1:N"),
        # Users -> Referrals (1:N Referrer)
        ("Users", "Referrals", (20.0, 88.0), (83.0, 88.0), "#7C3AED", "1:N"),
        # Users -> Task_Activity (1:N)
        ("Users", "Task_Activity", (20.0, 52.0), (43.0, 52.0), "#2563EB", "1:N"),
        # Sessions -> Task_Activity (1:N)
        ("Sessions", "Task_Activity", (31.5, 62.0), (43.0, 48.0), "#0284C7", "1:N"),
        # Task_Master -> Task_Activity (1:N)
        ("Task_Master", "Task_Activity", (40.0, 42.0), (43.0, 42.0), "#7C3AED", "1:N"),
        # Users -> Milestones (1:N)
        ("Users", "Milestones", (20.0, 60.0), (64.0, 46.0), "#2563EB", "1:N"),
        # Sessions -> Milestones (1:N)
        ("Sessions", "Milestones", (40.0, 66.0), (64.0, 42.0), "#0284C7", "1:N"),
        # Users -> Wallet_Transactions (1:N)
        ("Users", "Wallet_Transactions", (10.0, 48.0), (23.0, 18.0), "#7C3AED", "1:N"),
        # Users -> Withdrawals (1:N)
        ("Users", "Withdrawals", (12.0, 48.0), (44.0, 18.0), "#7C3AED", "1:N"),
    ]

    for src, dst, (x1, y1), (x2, y2), color, lbl in relationships:
        # Draw connector path
        arrow = patches.FancyArrowPatch(
            (x1, y1), (x2, y2),
            connectionstyle="arc3,rad=-0.08",
            arrowstyle="-|>", mutation_scale=12,
            color=color, linewidth=1.5, alpha=0.85, zorder=5
        )
        ax.add_patch(arrow)
        
        # Midpoint label
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        ax.text(
            mx, my + 0.6, lbl,
            fontsize=8, fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, linewidth=0.6, alpha=0.9),
            va="center", ha="center", zorder=6
        )

    plt.tight_layout()
    output_png = "05_data_model/er_diagram.png"
    plt.savefig(output_png, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    
    # Verify file existence and dimensions with Pillow
    img = Image.open(output_png)
    print(f"Successfully rendered ER diagram PNG to {output_png} (Size: {img.size[0]}x{img.size[1]} px)")

if __name__ == "__main__":
    render_er_diagram()
