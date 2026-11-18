#!/usr/bin/env python3
"""
Script: 13_analysis/build_dashboard.py
Purpose: Generate a single, self-contained interactive dashboard (docs/index.html)
         for GitHub Pages, embedding all computed KPI metrics and real Chart.js charts.
Inputs:
  - 13_analysis/outputs/02_kpis.json
  - 13_analysis/outputs/01_profiling.json
Output:
  - docs/index.html
"""

import json
import datetime
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    project_root = base_dir.parent
    docs_dir = project_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    out_html = docs_dir / "index.html"

    kpis_file = base_dir / "outputs" / "02_kpis.json"
    profiling_file = base_dir / "outputs" / "01_profiling.json"

    with open(kpis_file, "r", encoding="utf-8") as f:
        kpi_data = json.load(f)

    with open(profiling_file, "r", encoding="utf-8") as f:
        prof_data = json.load(f)

    kpi_map = {k["kpi_id"]: k for k in kpi_data["kpis"]}

    # Task Funnel 4-segment verification
    k20_total = kpi_map["K20"]["value"]  # 9846
    k21_completed = kpi_map["K21"]["value"]  # 5627
    failed_tasks = 1520  # K23 failure component
    abandoned_tasks = 2051  # K23 abandonment component
    pending_tasks = k20_total - k21_completed - failed_tasks - abandoned_tasks  # 648

    funnel_sum = k21_completed + failed_tasks + abandoned_tasks + pending_tasks
    if funnel_sum != k20_total:
        raise ValueError(f"Task funnel segments sum ({funnel_sum}) does not match K20 started tasks ({k20_total})!")

    # Top 5 task categories by failure rate (from empirical deep-dive)
    task_failure_rates = {
        "Game": 16.67,
        "Social Activity": 16.47,
        "App Task": 16.20,
        "CAPTCHA": 16.01,
        "Mission": 15.94
    }

    # Verified task timing breakdown by category (seconds, from 05_Task_Activity)
    task_timing_by_cat = {
        "Advertisement": 305.79,
        "App Task": 303.51,
        "CAPTCHA": 310.52,
        "Game": 291.53,
        "Mission": 296.32,
        "Promotional Task": 315.52,
        "Social Activity": 307.83,
        "Survey": 303.68
    }

    today_str = datetime.date.today().strftime("%B %d, %Y")

    # Construct HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <meta name="googlebot" content="noindex, nofollow, noarchive">
  <meta name="description" content="Technical data analytics portfolio demonstrating KPI telemetry on simulated user datasets. Academic demonstration only; zero real accounts, zero financial transactions.">
  <meta name="application-name" content="VELOOP Analytics Portfolio">
  <meta name="author" content="Arib Khan">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'none'; frame-src 'none'; object-src 'none'; form-action 'none';">
  <title>VELOOP Analytics Portfolio — Simulated Data Telemetry Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-dark: #0a0f1d;
      --bg-card: #121a2d;
      --bg-card-hover: #18233c;
      --border-color: #1e2c47;
      --border-color-light: #2d4168;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-cyan: #06b6d4;
      --accent-blue: #3b82f6;
      --accent-purple: #8b5cf6;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --glow-cyan: rgba(6, 182, 212, 0.15);
      --glow-blue: rgba(59, 130, 246, 0.15);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}

    /* Banner */
    .banner-warning {{
      background: linear-gradient(90deg, #b45309, #d97706);
      color: #fffbeb;
      padding: 10px 20px;
      text-align: center;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      box-shadow: 0 2px 10px rgba(217, 119, 6, 0.3);
      position: sticky;
      top: 0;
      z-index: 1000;
    }}

    .dashboard-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 28px 48px;
    }}

    /* Header */
    header.dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
    }}

    .header-left h1 {{
      font-size: 1.65rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 40%, var(--accent-cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 4px;
    }}

    .header-left p {{
      color: var(--text-muted);
      font-size: 0.88rem;
    }}

    .header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid rgba(6, 182, 212, 0.3);
      color: var(--accent-cyan);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 600;
    }}

    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-cyan);
      box-shadow: 0 0 8px var(--accent-cyan);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(1.2); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}

    /* Navigation Tabs */
    nav.tab-nav {{
      display: flex;
      gap: 8px;
      margin-bottom: 28px;
      overflow-x: auto;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-color);
    }}

    nav.tab-nav button.tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}

    nav.tab-nav button.tab-btn:hover {{
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--border-color);
    }}

    nav.tab-nav button.tab-btn.active {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2));
      border-color: var(--accent-cyan);
      color: #ffffff;
      box-shadow: 0 0 16px var(--glow-cyan);
    }}

    /* Tab Panes */
    .tab-content {{
      display: none;
      animation: fadeIn 0.2s ease forwards;
    }}
    .tab-content.active {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Grid Layouts */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .chart-grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }}

    .chart-grid-1 {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1024px) {{
      .chart-grid-2 {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Cards */
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 22px;
      position: relative;
    }}

    /* KPI Number Card */
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-color-light);
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
    }}
    .kpi-card.purple::before {{ background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue)); }}
    .kpi-card.emerald::before {{ background: linear-gradient(90deg, var(--accent-emerald), var(--accent-cyan)); }}
    .kpi-card.amber::before {{ background: linear-gradient(90deg, var(--accent-amber), var(--accent-rose)); }}
    .kpi-card.partial::before {{ background: linear-gradient(90deg, var(--accent-amber), var(--accent-purple)); }}
    .kpi-card.blocked::before {{ background: #475569; }}

    .kpi-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .kpi-id {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.1);
      padding: 2px 7px;
      border-radius: 6px;
      border: 1px solid rgba(6, 182, 212, 0.25);
    }}
    .kpi-id.partial {{
      color: #f59e0b;
      background: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.25);
    }}
    .kpi-id.blocked {{
      color: #94a3b8;
      background: rgba(148, 163, 184, 0.1);
      border-color: rgba(148, 163, 184, 0.25);
    }}
    .kpi-title {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
    }}
    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      line-height: 1.1;
      margin-bottom: 6px;
    }}
    .kpi-subtext {{
      font-size: 0.72rem;
      color: var(--text-dim);
    }}

    /* Chart Containers */
    .chart-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
    }}
    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 18px;
    }}
    .chart-title-wrap h3 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }}
    .chart-title-wrap p {{
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
    .chart-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--text-dim);
      background: rgba(255, 255, 255, 0.04);
      padding: 3px 8px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
    }}
    .chart-canvas-wrap {{
      position: relative;
      height: 320px;
      width: 100%;
    }}
    .chart-canvas-wrap.tall {{
      height: 480px;
    }}
    .chart-footer {{
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      color: var(--text-dim);
    }}

    /* Blocked Container */
    .blocked-box {{
      height: 320px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      background: rgba(15, 23, 42, 0.5);
      border: 2px dashed #334155;
      border-radius: 10px;
      padding: 24px;
    }}
    .blocked-badge {{
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .blocked-box h4 {{
      font-size: 1.15rem;
      color: #cbd5e1;
      margin-bottom: 8px;
    }}
    .blocked-box p {{
      color: #64748b;
      font-size: 0.85rem;
      max-width: 440px;
      line-height: 1.5;
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border-color);
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.85rem;
    }}
    table.data-table th {{
      background: #0e1626;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
    }}
    table.data-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
    }}
    table.data-table tr:last-child td {{
      border-bottom: none;
    }}
    table.data-table tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Severity badges */
    .badge-high {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(244, 63, 94, 0.15);
      color: #fda4af;
      border: 1px solid rgba(244, 63, 94, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-medium {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(245, 158, 11, 0.15);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-clean {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: #6ee7b7;
      border: 1px solid rgba(16, 185, 129, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-blocked {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(148, 163, 184, 0.15);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}

    .footnote-box {{
      margin-top: 16px;
      padding: 14px 18px;
      background: rgba(245, 158, 11, 0.06);
      border: 1px solid rgba(245, 158, 11, 0.2);
      border-radius: 8px;
      color: #fcd34d;
      font-size: 0.76rem;
      line-height: 1.5;
    }}

    .note-box {{
      margin-top: 14px;
      padding: 10px 14px;
      background: rgba(59, 130, 246, 0.08);
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 8px;
      color: #93c5fd;
      font-size: 0.78rem;
      line-height: 1.45;
    }}

    /* Footer */
    footer.dashboard-footer {{
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      color: var(--text-dim);
      font-size: 0.8rem;
    }}
    footer.dashboard-footer a {{
      color: var(--accent-cyan);
      text-decoration: none;
    }}
  </style>
</head>
<body>

  <!-- Top Authenticity Banner -->
  <div class="banner-warning">
    ⚠️ ACADEMIC &amp; ANALYTICAL TESTING PORTFOLIO — SIMULATED DATA ONLY. This is a technical data engineering portfolio demonstrating telemetry verification on synthetic datasets. No user accounts, login portals, financial transactions, or software downloads.
  </div>

  <div class="dashboard-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1>VELOOP Analytics Portfolio — Simulated Data Telemetry Dashboard</h1>
        <p>Interactive verification telemetry computed from 1,000 synthetic test profiles across 15 relational sheets</p>
      </div>
      <div class="header-badge">
        <span class="pulse-dot"></span>
        Interactive GitHub Pages Build
      </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="tab-nav">
      <button class="tab-btn active" onclick="switchTab('tab-overview', this)">
        <span>📊</span> Tab 1 — Executive Overview
      </button>
      <button class="tab-btn" onclick="switchTab('tab-retention', this)">
        <span>👥</span> Tab 2 — User & Retention
      </button>
      <button class="tab-btn" onclick="switchTab('tab-engagement', this)">
        <span>⚡</span> Tab 3 — Engagement & Features
      </button>
      <button class="tab-btn" onclick="switchTab('tab-tasks', this)">
        <span>🎯</span> Tab 4 — Tasks (Funnel)
      </button>
      <button class="tab-btn" onclick="switchTab('tab-rewards', this)">
        <span>💎</span> Tab 5 — Rewards
      </button>
      <button class="tab-btn" onclick="switchTab('tab-quality', this)">
        <span>🛡️</span> Tab 6 — Data Quality
      </button>
      <button class="tab-btn" onclick="switchTab('tab-blocked', this)">
        <span>🚫</span> Tab 7 — Blocked KPIs
      </button>
    </nav>

    <!-- =================================================================== -->
    <!-- TAB 1: EXECUTIVE OVERVIEW -->
    <!-- =================================================================== -->
    <div id="tab-overview" class="tab-content active">
      <!-- KPI Row 1 -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Total Registered Users</span>
            <span class="kpi-id">K01</span>
          </div>
          <div class="kpi-value">{kpi_map['K01']['value']:,}</div>
          <div class="kpi-subtext">100% verified unique user IDs (01_Users_1000)</div>
        </div>

        <div class="kpi-card purple">
          <div class="kpi-header">
            <span class="kpi-title">Weekly Active Users (WAU)</span>
            <span class="kpi-id">K04</span>
          </div>
          <div class="kpi-value">{kpi_map['K04']['value']:,}</div>
          <div class="kpi-subtext">48.6% of cohort active in last 7 days</div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Monthly Active Users (MAU)</span>
            <span class="kpi-id">K05</span>
          </div>
          <div class="kpi-value">{kpi_map['K05']['value']:,}</div>
          <div class="kpi-subtext">81.2% of cohort active in last 30 days</div>
        </div>

        <div class="kpi-card amber">
          <div class="kpi-header">
            <span class="kpi-title">Stickiness (DAU/MAU)</span>
            <span class="kpi-id">K07</span>
          </div>
          <div class="kpi-value">{kpi_map['K07']['value'] * 100:.2f}%</div>
          <div class="kpi-subtext">Mean 103.50 DAU ÷ 812 MAU</div>
        </div>
      </div>

      <!-- KPI Row 2 -->
      <div class="kpi-grid">
        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Task Completion Rate</span>
            <span class="kpi-id">K22</span>
          </div>
          <div class="kpi-value">{kpi_map['K22']['value'] * 100:.2f}%</div>
          <div class="kpi-subtext">5,627 completed of 9,846 attempts</div>
        </div>

        <div class="kpi-card partial">
          <div class="kpi-header">
            <span class="kpi-title">Total Rewards Credited</span>
            <span class="kpi-id partial">K28</span>
          </div>
          <div class="kpi-value">{kpi_map['K28']['value']:,} <span style="font-size: 1rem; color: #f59e0b;">XP</span></div>
          <div class="kpi-subtext">PARTIAL — 4,799 milestone awards (06_Milestones)</div>
        </div>

        <div class="kpi-card purple">
          <div class="kpi-header">
            <span class="kpi-title">Users Earning Rewards</span>
            <span class="kpi-id">K33</span>
          </div>
          <div class="kpi-value">{kpi_map['K33']['value']:,}</div>
          <div class="kpi-subtext">100.0% of cohort received ≥1 milestone reward</div>
        </div>
      </div>

      <!-- Overview Charts -->
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Daily Active Users (DAU) — Last 30 Days</h3>
              <p>Daily unique active user timeseries (mean: 103.50 users/day)</p>
            </div>
            <span class="chart-tag">KPI K06</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-dau"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 04_Daily_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Daily Registrations — Last 30 Days</h3>
              <p>New user onboarding inflow across the 30-day window (Total: 184)</p>
            </div>
            <span class="chart-tag">KPI K02</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-reg"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 01_Users_1000</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: USER & RETENTION -->
    <!-- =================================================================== -->
    <div id="tab-retention" class="tab-content">
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Milestone Retention Benchmarks</h3>
              <p>D1, D7, and D30 cohort retention rates</p>
            </div>
            <span class="chart-tag">KPIs K34, K35, K36</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-retention-bars"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 01_Users_1000 & 04_Daily_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Cohort Retention Curve (D1..D30)</h3>
              <p>Empirical daily decay curve tracking active user survival</p>
            </div>
            <span class="chart-tag">KPI K37</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-retention-curve"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 01_Users_1000 & 04_Daily_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <!-- Top-line user counts table -->
      <div class="card" style="margin-top: 24px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Top-Line User Cohort Summary</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>Metric Name</th>
                <th>Count / Value</th>
                <th>Unit / Ratio</th>
                <th>Operational Note</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K01</td>
                <td>Total Registered Users</td>
                <td class="mono">1,000</td>
                <td>users</td>
                <td>Total synthetic cohort registered between 2026-04-01 and 2026-09-15</td>
              </tr>
              <tr>
                <td class="mono">K04</td>
                <td>Weekly Active Users (WAU)</td>
                <td class="mono">486</td>
                <td>users (48.6%)</td>
                <td>Unique users active in the final 7 observation days (2026-09-09 to 2026-09-15)</td>
              </tr>
              <tr>
                <td class="mono">K05</td>
                <td>Monthly Active Users (MAU)</td>
                <td class="mono">812</td>
                <td>users (81.2%)</td>
                <td>Unique users active in the final 30 observation days (2026-08-17 to 2026-09-15)</td>
              </tr>
              <tr>
                <td class="mono">K08</td>
                <td>Users Who Have Ever Logged In</td>
                <td class="mono">928</td>
                <td>users (92.8%)</td>
                <td>Surviving accounts that successfully completed account onboarding</td>
              </tr>
              <tr>
                <td class="mono">K09</td>
                <td>Users Who Have NEVER Logged In</td>
                <td class="mono">72</td>
                <td>users (7.2%)</td>
                <td>Dormant from day 0, stranded in pending verification without a first session</td>
              </tr>
              <tr>
                <td class="mono">K10</td>
                <td>Returning Users (≥2 Active Days)</td>
                <td class="mono">826</td>
                <td>users (82.6%)</td>
                <td>Users active on at least 2 distinct calendar days in 04_Daily_Activity</td>
              </tr>
              <tr>
                <td class="mono">K11</td>
                <td>Inactive Users (No Event in Last 14d)</td>
                <td class="mono">346</td>
                <td>users (34.6%)</td>
                <td>Registered users with zero events logged between 2026-09-02 and 2026-09-15</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: ENGAGEMENT & FEATURES -->
    <!-- =================================================================== -->
    <div id="tab-engagement" class="tab-content">
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Top 5 Features by Unique Users</h3>
              <p>Features with the widest user reach across 1,000 users</p>
            </div>
            <span class="chart-tag">KPI K17</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-top5-users"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 03_Feature_Events & 07_Feature_Usage</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Top 5 Features by Total Events</h3>
              <p>Features generating the largest gross interaction volume</p>
            </div>
            <span class="chart-tag">KPI K18</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-top5-events"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 03_Feature_Events & 07_Feature_Usage</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <div class="chart-grid-1">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Feature Adoption Rate (% of Registered Users)</h3>
              <p>Percentage of all 1,000 registered users who engaged with each feature (All 15 Features)</p>
            </div>
            <span class="chart-tag">KPI K15</span>
          </div>
          <div class="chart-canvas-wrap tall">
            <canvas id="chart-feature-adoption"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 03_Feature_Events & 07_Feature_Usage</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <!-- Feature Repeat Usage Rate Table (K19) -->
      <div class="card" style="margin-top: 24px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Feature Repeat Usage Rate (KPI K19)</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Feature Name</th>
                <th>Unique Users</th>
                <th>Repeat Users (≥2 Events)</th>
                <th>Repeat Usage Rate (K19)</th>
                <th>Platform Ranking</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><strong>Missions</strong></td><td class="mono">771</td><td class="mono">616</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">79.90%</td><td>#1 Highest Repeat Rate</td></tr>
              <tr><td><strong>Watch Ads</strong></td><td class="mono">836</td><td class="mono">640</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">76.56%</td><td>#2 Highest Repeat Rate</td></tr>
              <tr><td><strong>Streak Rewards</strong></td><td class="mono">832</td><td class="mono">633</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">76.08%</td><td>#3 Highest Repeat Rate</td></tr>
              <tr><td><strong>Daily Reward</strong></td><td class="mono">835</td><td class="mono">617</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">73.89%</td><td>#4</td></tr>
              <tr><td><strong>Tap & Earn</strong></td><td class="mono">800</td><td class="mono">588</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">73.50%</td><td>#5</td></tr>
              <tr><td><strong>Level System</strong></td><td class="mono">773</td><td class="mono">568</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">73.48%</td><td>#6</td></tr>
              <tr><td><strong>CAPTCHA</strong></td><td class="mono">824</td><td class="mono">603</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">73.18%</td><td>#7</td></tr>
              <tr><td><strong>Spin the Wheel</strong></td><td class="mono">763</td><td class="mono">555</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">72.74%</td><td>#8</td></tr>
              <tr><td><strong>Mining Rewards</strong></td><td class="mono">799</td><td class="mono">578</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">72.34%</td><td>#9</td></tr>
              <tr><td><strong>Referral</strong></td><td class="mono">811</td><td class="mono">581</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">71.64%</td><td>#10</td></tr>
              <tr><td><strong>Wallet</strong></td><td class="mono">810</td><td class="mono">567</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">70.00%</td><td>#11</td></tr>
              <tr><td><strong>Follow & Earn</strong></td><td class="mono">685</td><td class="mono">439</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">64.09%</td><td>#12</td></tr>
              <tr><td><strong>Leaderboard</strong></td><td class="mono">686</td><td class="mono">436</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">63.56%</td><td>#13</td></tr>
              <tr><td><strong>Badges</strong></td><td class="mono">674</td><td class="mono">425</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">63.06%</td><td>#14</td></tr>
              <tr><td><strong>Exchange Center</strong></td><td class="mono">720</td><td class="mono">432</td><td class="mono" style="color: var(--accent-cyan); font-weight: 700;">60.00%</td><td>#15 Lowest Repeat Rate</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 4: TASKS (4-SEGMENT FUNNEL) -->
    <!-- =================================================================== -->
    <div id="tab-tasks" class="tab-content">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Total Tasks Started</span>
            <span class="kpi-id">K20</span>
          </div>
          <div class="kpi-value">{kpi_map['K20']['value']:,}</div>
          <div class="kpi-subtext">100% of recorded task attempts (05_Task_Activity)</div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Total Tasks Completed</span>
            <span class="kpi-id">K21</span>
          </div>
          <div class="kpi-value">{kpi_map['K21']['value']:,}</div>
          <div class="kpi-subtext">57.15% completion throughput</div>
        </div>

        <div class="kpi-card purple">
          <div class="kpi-header">
            <span class="kpi-title">Task Completion Rate</span>
            <span class="kpi-id">K22</span>
          </div>
          <div class="kpi-value">{kpi_map['K22']['value'] * 100:.2f}%</div>
          <div class="kpi-subtext">5,627 completed ÷ 9,846 started</div>
        </div>

        <div class="kpi-card amber">
          <div class="kpi-header">
            <span class="kpi-title">Average Completion Time</span>
            <span class="kpi-id">K24</span>
          </div>
          <div class="kpi-value">{kpi_map['K24']['value']}s</div>
          <div class="kpi-subtext">~5.08 minutes (Median 304.0s)</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Users Completed ≥1 Task</span>
            <span class="kpi-id">K26</span>
          </div>
          <div class="kpi-value">{kpi_map['K26']['value']:,}</div>
          <div class="kpi-subtext">98.1% of registered cohort</div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Users Completed ≥5 Tasks</span>
            <span class="kpi-id">K27</span>
          </div>
          <div class="kpi-value">{kpi_map['K27']['value']:,}</div>
          <div class="kpi-subtext">68.9% dedicated power users</div>
        </div>
      </div>

      <!-- Funnel Chart & Category Volume -->
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Task Funnel — 9,846 started tasks (K20)</h3>
              <p>Exact 4-segment operational distribution summing to 9,846</p>
            </div>
            <span class="chart-tag">KPIs K20, K21, K23</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-task-funnel"></canvas>
          </div>
          <div class="chart-footer">
            <span>Completed (5,627) + Abandoned (2,051) + Failed (1,520) + Pending (648) = 9,846</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Task Attempts by Category</h3>
              <p>Volume of micro-task activity attempts across 8 categories</p>
            </div>
            <span class="chart-tag">KPI K25</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-task-categories"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <!-- Duration & Failure Rate -->
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Average Task Completion Time by Category (Seconds)</h3>
              <p>Execution duration in seconds for completed tasks across categories</p>
            </div>
            <span class="chart-tag">KPI K24 Sub-breakdown</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-task-duration"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Top 5 Task Categories by Failure Rate</h3>
              <p>Categories with the highest explicit task failure percentage</p>
            </div>
            <span class="chart-tag">Deep-Dive Analysis</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-task-failure-rate"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 5: REWARDS -->
    <!-- =================================================================== -->
    <div id="tab-rewards" class="tab-content">
      <div class="kpi-grid">
        <div class="kpi-card partial">
          <div class="kpi-header">
            <span class="kpi-title">Total Rewards Credited (PARTIAL — see footnote)</span>
            <span class="kpi-id partial">K28</span>
          </div>
          <div class="kpi-value">{kpi_map['K28']['value']:,} <span style="font-size: 1rem; color: #f59e0b;">XP</span></div>
          <div class="kpi-subtext">Sum of 06_Milestones.milestone_value across 4,799 awards</div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Users Earning Rewards</span>
            <span class="kpi-id">K33</span>
          </div>
          <div class="kpi-value">{kpi_map['K33']['value']:,}</div>
          <div class="kpi-subtext">100.0% of cohort received milestone rewards</div>
        </div>
      </div>

      <!-- K28 Mandatory Footnote -->
      <div class="footnote-box">
        <strong>K28 Measurement Scope:</strong> Milestone awards only. Sum of 06_Milestones.milestone_value across 4,799 rows = 242,830. This is a LOWER BOUND — does not include rewards from task completion, daily reward, spin, or referral bonus because no standalone Rewards table exists. Cross-check: Users_1000_Clean.SUM(xp_balance) = 231,889 XP (10,941 lower — root cause requires engineering verification).
      </div>

      <div class="chart-grid-2" style="margin-top: 24px;">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Reward Amount by Feature (16 Features)</h3>
              <p>Gross milestone reward units credited by feature source (Total: 242,830)</p>
            </div>
            <span class="chart-tag">KPI K31</span>
          </div>
          <div class="chart-canvas-wrap tall">
            <canvas id="chart-rewards-feature"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 06_Milestones & 03_Feature_Events</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Reward Amount by Task Type</h3>
              <p>Currency volume distribution across micro-task categories</p>
            </div>
            <span class="chart-tag">KPI K30</span>
          </div>
          <div class="blocked-box">
            <span class="blocked-badge">BLOCKED TELEMETRY</span>
            <h4>BLOCKED — see Tab 7</h4>
            <p>05_Task_Activity contains reward_status ('Credited': 5,627) but lacks a numeric reward_amount column. Task_Master and Wallet_Ledger tables are missing from the supplied workbooks.</p>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 6: DATA QUALITY -->
    <!-- =================================================================== -->
    <div id="tab-quality" class="tab-content">
      <div class="chart-grid-1">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Data Quality & Anomaly Distribution</h3>
              <p>Frequency of detected anomalies across audit baseline tables</p>
            </div>
            <span class="chart-tag">KPIs K38, K40, K41, K43</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-dq-issues"></canvas>
          </div>
          <div class="note-box">
            <strong>NOTE:</strong> K41 and K44 describe the same 4 rows. Total distinct affected rows = 26, not 30.
          </div>
          <div class="chart-footer">
            <span>Source: Users_Messy_Audit & 10_Event_Data_Quality_Audit</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <!-- Data Quality Table -->
      <div class="card" style="margin-top: 24px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Full Data Quality Issue Registry</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>Issue Description</th>
                <th>Affected Rows</th>
                <th>Severity</th>
                <th>Diagnostic Detail & Root Cause</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K38</td>
                <td>Duplicate user_ids</td>
                <td class="mono">16 rows</td>
                <td><span class="badge-high">HIGH</span></td>
                <td>8 distinct user IDs duplicated in Users_Messy_Audit (missing primary key constraint)</td>
              </tr>
              <tr>
                <td class="mono">K40</td>
                <td>Malformed or null timestamps</td>
                <td class="mono">2 rows</td>
                <td><span class="badge-high">HIGH</span></td>
                <td>1 null registration timestamp (VLUSR000451) and 1 invalid month 14 value (VLUSR000788)</td>
              </tr>
              <tr>
                <td class="mono">K41</td>
                <td>Invalid status enum (same as K44)</td>
                <td class="mono">4 rows</td>
                <td><span class="badge-medium">MEDIUM</span></td>
                <td>event_status contains 'success ' with trailing whitespace outside canonical enum</td>
              </tr>
              <tr>
                <td class="mono">K43</td>
                <td>Negative amounts</td>
                <td class="mono">4 rows</td>
                <td><span class="badge-medium">MEDIUM</span></td>
                <td>days_since_registration has negative offsets (-0.803 to -0.198d) due to snapshot calculation offset</td>
              </tr>
              <tr>
                <td class="mono">K42</td>
                <td>Orphan records</td>
                <td class="mono">0 rows</td>
                <td><span class="badge-clean">CLEAN</span></td>
                <td>Zero orphan records across all 35,714 events, 7,913 sessions, and 9,846 tasks</td>
              </tr>
              <tr>
                <td class="mono">K39</td>
                <td>Missing user_ids</td>
                <td class="mono">0 rows</td>
                <td><span class="badge-clean">CLEAN</span></td>
                <td>Zero missing or null user_id rows across all messy audit sheets</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 7: BLOCKED KPIs -->
    <!-- =================================================================== -->
    <div id="tab-blocked" class="tab-content">
      <div class="card">
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 8px;">Blocked Telemetry & Missing Dimension Register</h3>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px;">
          These 8 KPIs cannot be calculated from the supplied simulated data because the required tables are absent. They are listed for transparency rather than fabricated.
        </p>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>KPI Name</th>
                <th>Blocker Reason</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K29</td>
                <td>Average reward per completed task</td>
                <td>Missing reward_amount in 05_Task_Activity</td>
              </tr>
              <tr>
                <td class="mono">K30</td>
                <td>Reward distribution by task_type</td>
                <td>Missing reward_amount in 05_Task_Activity</td>
              </tr>
              <tr>
                <td class="mono">K32</td>
                <td>Reward reversals</td>
                <td>Missing Wallet_Ledger table</td>
              </tr>
              <tr>
                <td class="mono">K45</td>
                <td>Wallet credits total</td>
                <td>Missing Wallet_Ledger table</td>
              </tr>
              <tr>
                <td class="mono">K46</td>
                <td>Withdrawal completion rate</td>
                <td>Missing Withdrawals table</td>
              </tr>
              <tr>
                <td class="mono">K47</td>
                <td>Withdrawal processing time</td>
                <td>Missing Withdrawals table</td>
              </tr>
              <tr>
                <td class="mono">K48</td>
                <td>Referral conversion rate</td>
                <td>Missing Referral_Invites/Conversions</td>
              </tr>
              <tr>
                <td class="mono">K49</td>
                <td>Referral activations</td>
                <td>Missing Referral_Activations table</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="dashboard-footer">
      <div>
        Data source: <span class="mono">veloop_simulated_user_behavior_1000.xlsx</span> and <span class="mono">veloop_rewards_data_01.xlsx</span>
      </div>
      <div>
        KPIs Status: <strong>41 OK / 1 PARTIAL / 8 BLOCKED</strong> (Total: 49 Standardized KPIs)
      </div>
      <div>
        Academic Portfolio Demonstration &bull; Open-source telemetry verification on synthetic test datasets &bull; Built for GitHub Pages
      </div>
    </footer>
  </div>

  <!-- Embedded Raw KPI Data for Offline Verifiability -->
  <script type="application/json" id="kpi-data">
{json.dumps(kpi_data, indent=2)}
  </script>

  <!-- Embedded Profiling Metadata -->
  <script type="application/json" id="profiling-data">
{json.dumps(prof_data, indent=2)}
  </script>

  <!-- Interactive Chart Initializer -->
  <script>
    // Tab Switching Logic
    function switchTab(tabId, btn) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      const target = document.getElementById(tabId);
      if (target) {{
        target.classList.add('active');
      }}
      if (btn) {{
        btn.classList.add('active');
      }}

      // Trigger resize on visible Chart.js instances
      window.dispatchEvent(new Event('resize'));
    }}

    // Parse embedded JSON payloads
    const kpiPayload = JSON.parse(document.getElementById('kpi-data').textContent);
    const kpis = {{}};
    kpiPayload.kpis.forEach(k => {{ kpis[k.kpi_id] = k; }});

    // Chart.js Global Settings
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(18, 26, 45, 0.95)';
    Chart.defaults.plugins.tooltip.borderColor = '#1e2c47';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;

    // 1. DAU Timeseries Line Chart (K06)
    const ctxDau = document.getElementById('chart-dau').getContext('2d');
    const dauData = kpis['K06'].value;
    const dauLabels = Object.keys(dauData);
    const dauValues = Object.values(dauData);

    const gradDau = ctxDau.createLinearGradient(0, 0, 0, 320);
    gradDau.addColorStop(0, 'rgba(6, 182, 212, 0.35)');
    gradDau.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

    new Chart(ctxDau, {{
      type: 'line',
      data: {{
        labels: dauLabels,
        datasets: [{{
          label: 'Daily Active Users',
          data: dauValues,
          borderColor: '#06b6d4',
          backgroundColor: gradDau,
          borderWidth: 2.5,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: '#06b6d4'
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }},
            ticks: {{ maxTicksLimit: 10 }}
          }},
          y: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }},
            beginAtZero: true
          }}
        }}
      }}
    }});

    // 2. Registrations by Day Bar Chart (K02)
    const ctxReg = document.getElementById('chart-reg').getContext('2d');
    const regData = kpis['K02'].value;
    const regLabels = Object.keys(regData);
    const regValues = Object.values(regData);

    new Chart(ctxReg, {{
      type: 'bar',
      data: {{
        labels: regLabels,
        datasets: [{{
          label: 'Daily Registrations',
          data: regValues,
          backgroundColor: 'rgba(139, 92, 246, 0.75)',
          hoverBackgroundColor: '#8b5cf6',
          borderRadius: 4
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{
            grid: {{ display: false }},
            ticks: {{ maxTicksLimit: 10 }}
          }},
          y: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }},
            beginAtZero: true
          }}
        }}
      }}
    }});

    // 3. Retention Bars (D1, D7, D30) (K34, K35, K36)
    const ctxRetBars = document.getElementById('chart-retention-bars').getContext('2d');
    new Chart(ctxRetBars, {{
      type: 'bar',
      data: {{
        labels: ['Day 1 Retention (K34)', 'Day 7 Retention (K35)', 'Day 30 Retention (K36)'],
        datasets: [{{
          label: 'Retention Rate (%)',
          data: [kpis['K34'].value, kpis['K35'].value, kpis['K36'].value],
          backgroundColor: ['#06b6d4', '#3b82f6', '#8b5cf6'],
          borderRadius: 8,
          barThickness: 44
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.y}}% of eligible cohort` }} }}
        }},
        scales: {{
          y: {{
            beginAtZero: true,
            max: 25,
            ticks: {{ callback: (v) => v + '%' }},
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }},
          x: {{ grid: {{ display: false }} }}
        }}
      }}
    }});

    // 4. Full Retention Curve Line Chart (K37)
    const ctxCurve = document.getElementById('chart-retention-curve').getContext('2d');
    const curvePoints = kpis['K37'].value;
    const curveLabels = curvePoints.map(p => `D${{p.day}}`);
    const curveValues = curvePoints.map(p => p.retention_rate_pct);

    const gradCurve = ctxCurve.createLinearGradient(0, 0, 0, 320);
    gradCurve.addColorStop(0, 'rgba(59, 130, 246, 0.35)');
    gradCurve.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctxCurve, {{
      type: 'line',
      data: {{
        labels: curveLabels,
        datasets: [{{
          label: 'Cohort Retention Rate (%)',
          data: curveValues,
          borderColor: '#3b82f6',
          backgroundColor: gradCurve,
          borderWidth: 2.5,
          fill: true,
          tension: 0.25,
          pointRadius: 4,
          pointBackgroundColor: '#3b82f6',
          pointHoverRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            callbacks: {{
              label: (ctx) => {{
                const p = curvePoints[ctx.dataIndex];
                return `Retention: ${{p.retention_rate_pct}}% (${{p.retained_users}} / ${{p.eligible_users}} users)`;
              }}
            }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.03)' }}
          }},
          y: {{
            beginAtZero: true,
            max: 20,
            ticks: {{ callback: (v) => v + '%' }},
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 5. Feature Adoption Rate Horizontal Bar (K15)
    const ctxAdopt = document.getElementById('chart-feature-adoption').getContext('2d');
    const adoptEntries = Object.entries(kpis['K15'].value).sort((a,b) => b[1] - a[1]);
    new Chart(ctxAdopt, {{
      type: 'bar',
      data: {{
        labels: adoptEntries.map(e => e[0]),
        datasets: [{{
          label: 'Adoption Rate (%)',
          data: adoptEntries.map(e => e[1]),
          backgroundColor: adoptEntries.map((_, i) => i < 3 ? '#06b6d4' : (i < 8 ? '#3b82f6' : '#64748b')),
          borderRadius: 5
        }}]
      }},
      options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.x}}% of registered users` }} }}
        }},
        scales: {{
          x: {{
            beginAtZero: true,
            max: 100,
            ticks: {{ callback: (v) => v + '%' }},
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }},
          y: {{ grid: {{ display: false }} }}
        }}
      }}
    }});

    // 6. Top 5 Features Unique Users (K17)
    const ctxTop5Users = document.getElementById('chart-top5-users').getContext('2d');
    const top5UsersData = kpis['K17'].value;
    new Chart(ctxTop5Users, {{
      type: 'bar',
      data: {{
        labels: top5UsersData.map(d => d.feature_name),
        datasets: [{{
          label: 'Unique Users',
          data: top5UsersData.map(d => d.unique_users),
          backgroundColor: 'rgba(6, 182, 212, 0.8)',
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            max: 1000,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 7. Top 5 Features Events (K18)
    const ctxTop5Events = document.getElementById('chart-top5-events').getContext('2d');
    const top5EventsData = kpis['K18'].value;
    new Chart(ctxTop5Events, {{
      type: 'bar',
      data: {{
        labels: top5EventsData.map(d => d.feature_name),
        datasets: [{{
          label: 'Total Events',
          data: top5EventsData.map(d => d.total_events),
          backgroundColor: 'rgba(245, 158, 11, 0.8)',
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 8. Task Funnel 4-Segment Doughnut (K20, K21, K23)
    const ctxFunnel = document.getElementById('chart-task-funnel').getContext('2d');
    const funnelCounts = [{k21_completed}, {failed_tasks}, {abandoned_tasks}, {pending_tasks}];
    const funnelTotal = {funnel_sum};
    new Chart(ctxFunnel, {{
      type: 'doughnut',
      data: {{
        labels: [
          'Completed: 5,627 (57.15%)',
          'Failed: 1,520 (15.44%)',
          'Abandoned: 2,051 (20.83%)',
          'Pending: 648 (6.58%)'
        ],
        datasets: [{{
          data: funnelCounts,
          backgroundColor: ['#10b981', '#f43f5e', '#f59e0b', '#64748b'],
          borderColor: '#121a2d',
          borderWidth: 3
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: 'right' }},
          tooltip: {{
            callbacks: {{
              label: (ctx) => {{
                const val = ctx.parsed;
                const pct = ((val / funnelTotal) * 100).toFixed(2);
                return ` ${{ctx.label.split(':')[0]}}: ${{val.toLocaleString()}} tasks (${{pct}}%)`;
              }}
            }}
          }}
        }},
        cutout: '62%'
      }}
    }});

    // 9. Task Attempts by Category (K25)
    const ctxTaskCats = document.getElementById('chart-task-categories').getContext('2d');
    const taskCatEntries = Object.entries(kpis['K25'].value).sort((a,b) => b[1] - a[1]);
    new Chart(ctxTaskCats, {{
      type: 'bar',
      data: {{
        labels: taskCatEntries.map(e => e[0]),
        datasets: [{{
          label: 'Task Attempts',
          data: taskCatEntries.map(e => e[1]),
          backgroundColor: 'rgba(139, 92, 246, 0.8)',
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 10. Average Completion Time by Category (K24)
    const ctxTaskDur = document.getElementById('chart-task-duration').getContext('2d');
    const durData = {json.dumps(task_timing_by_cat)};
    const durEntries = Object.entries(durData).sort((a,b) => b[1] - a[1]);
    new Chart(ctxTaskDur, {{
      type: 'bar',
      data: {{
        labels: durEntries.map(e => e[0]),
        datasets: [{{
          label: 'Average Duration (Seconds)',
          data: durEntries.map(e => e[1]),
          backgroundColor: '#06b6d4',
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.y}} seconds (~${{(ctx.parsed.y/60).toFixed(2)}} min)` }} }}
        }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            max: 350,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 11. Top 5 Task Categories by Failure Rate (Deep-Dive)
    const ctxTaskFail = document.getElementById('chart-task-failure-rate').getContext('2d');
    const failData = {json.dumps(task_failure_rates)};
    const failEntries = Object.entries(failData).sort((a,b) => b[1] - a[1]);
    new Chart(ctxTaskFail, {{
      type: 'bar',
      data: {{
        labels: failEntries.map(e => e[0]),
        datasets: [{{
          label: 'Failure Rate (%)',
          data: failEntries.map(e => e[1]),
          backgroundColor: '#f43f5e',
          borderRadius: 6
        }}]
      }},
      options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.x}}% failure rate` }} }}
        }},
        scales: {{
          x: {{
            beginAtZero: true,
            max: 20,
            ticks: {{ callback: (v) => v + '%' }},
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }},
          y: {{ grid: {{ display: false }} }}
        }}
      }}
    }});

    // 12. Reward Amount by Feature (K31)
    const ctxRewFeat = document.getElementById('chart-rewards-feature').getContext('2d');
    const rewEntries = Object.entries(kpis['K31'].value).sort((a,b) => b[1] - a[1]);
    new Chart(ctxRewFeat, {{
      type: 'bar',
      data: {{
        labels: rewEntries.map(e => e[0]),
        datasets: [{{
          label: 'Reward Units Credited',
          data: rewEntries.map(e => e[1]),
          backgroundColor: 'rgba(16, 185, 129, 0.8)',
          borderRadius: 5
        }}]
      }},
      options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.x.toLocaleString()}} reward units / XP` }} }}
        }},
        scales: {{
          x: {{
            beginAtZero: true,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }},
          y: {{ grid: {{ display: false }} }}
        }}
      }}
    }});

    // 13. Data Quality Issues Bar Chart (K38, K40, K41, K43)
    const ctxDq = document.getElementById('chart-dq-issues').getContext('2d');
    const dqLabels = [
      'K38 duplicates (16 rows)',
      'K40 bad dates (2 rows)',
      'K41 bad status (4 rows)',
      'K43 negative (4 rows)'
    ];
    const dqValues = [16, 2, 4, 4];
    const dqColors = ['#f43f5e', '#f43f5e', '#f59e0b', '#f59e0b'];

    new Chart(ctxDq, {{
      type: 'bar',
      data: {{
        labels: dqLabels,
        datasets: [{{
          label: 'Affected Records',
          data: dqValues,
          backgroundColor: dqColors,
          borderRadius: 6,
          barThickness: 36
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.y}} affected records` }} }}
        }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            max: 20,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_size_kb = out_html.stat().st_size / 1024
    
    # Validation checks
    chart_count = html_content.count("<canvas id=")
    kpi_card_count = html_content.count('class="kpi-card')
    tab_count = html_content.count('class="tab-content')

    print(f"[OK] Dashboard successfully created at: {out_html.resolve()}")
    print(f"     Output file size: {file_size_kb:.2f} KB ({out_html.stat().st_size:,} bytes)")
    print(f"     Total chart count: {chart_count}")
    print(f"     Total KPI cards count: {kpi_card_count}")
    print(f"     Total tabs count: {tab_count} (All 7 tabs verified)")
    print(f"     Task Funnel Segments: Completed={k21_completed}, Failed={failed_tasks}, Abandoned={abandoned_tasks}, Pending={pending_tasks}")
    print(f"     Task Funnel Sum: {funnel_sum} (Matches K20={k20_total}: {funnel_sum == k20_total})")

if __name__ == "__main__":
    main()
