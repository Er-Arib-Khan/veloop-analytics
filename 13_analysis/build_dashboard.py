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

    # Additional verified task timing breakdown by category (computed from 05_Task_Activity)
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

    # Additional verified cohort active 30d breakdown (computed from 01_Users_1000 & 03_Feature_Events)
    cohort_data = {
        "cohorts": ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"],
        "registered": [186, 167, 182, 182, 177, 106],
        "active_30d": [118, 115, 142, 160, 171, 106]
    }

    today_str = datetime.date.today().strftime("%B %d, %Y")

    # Construct HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VELOOP Rewards — Simulated Data Analytics Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --bg-card: #131c2e;
      --bg-card-hover: #19253d;
      --bg-card-alt: #162238;
      --border-color: #23334d;
      --border-color-light: #334b6e;
      --text-main: #f1f5f9;
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

    /* Top Notice Banner */
    .banner-warning {{
      background: linear-gradient(90deg, #78350f, #92400e, #78350f);
      border-bottom: 1px solid #b45309;
      color: #fef3c7;
      text-align: center;
      padding: 10px 16px;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}

    /* Container */
    .dashboard-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 28px 60px;
    }}

    /* Header */
    header.dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-left h1 {{
      font-size: 1.75rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 6px;
    }}

    .header-left p {{
      color: var(--text-muted);
      font-size: 0.9rem;
    }}

    .header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid rgba(6, 182, 212, 0.3);
      color: var(--accent-cyan);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .header-badge .pulse-dot {{
      width: 7px;
      height: 7px;
      background-color: var(--accent-cyan);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-cyan);
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
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 10px 18px;
      border-radius: 10px;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    nav.tab-nav button.tab-btn:hover {{
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--border-color-light);
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
      animation: fadeIn 0.25s ease forwards;
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
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
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
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }}
    .card:hover {{
      border-color: var(--border-color-light);
    }}

    /* KPI Number Card */
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
      opacity: 0.8;
    }}
    .kpi-card.purple::before {{ background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue)); }}
    .kpi-card.emerald::before {{ background: linear-gradient(90deg, var(--accent-emerald), var(--accent-cyan)); }}
    .kpi-card.amber::before {{ background: linear-gradient(90deg, var(--accent-amber), var(--accent-rose)); }}
    .kpi-card.blocked::before {{ background: #475569; }}

    .kpi-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .kpi-id {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.1);
      padding: 2px 8px;
      border-radius: 6px;
      border: 1px solid rgba(6, 182, 212, 0.2);
    }}
    .kpi-id.blocked {{
      color: #94a3b8;
      background: rgba(148, 163, 184, 0.1);
      border-color: rgba(148, 163, 184, 0.2);
    }}
    .kpi-title {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    .kpi-value {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      line-height: 1.1;
      margin-bottom: 6px;
    }}
    .kpi-value.blocked {{
      font-size: 1.15rem;
      color: #94a3b8;
      font-weight: 700;
    }}
    .kpi-subtext {{
      font-size: 0.75rem;
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
      align-items: baseline;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .chart-title-wrap h3 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .chart-title-wrap p {{
      font-size: 0.8rem;
      color: var(--text-dim);
    }}
    .chart-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--text-dim);
      background: var(--bg-card-alt);
      border: 1px solid var(--border-color);
      padding: 3px 8px;
      border-radius: 6px;
    }}
    .chart-canvas-wrap {{
      position: relative;
      height: 320px;
      width: 100%;
    }}
    .chart-canvas-wrap.tall {{
      height: 420px;
    }}
    .chart-footer {{
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.7rem;
      font-weight: 600;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Blocked Container */
    .blocked-box {{
      height: 100%;
      min-height: 240px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(30, 41, 59, 0.4);
      border: 2px dashed rgba(148, 163, 184, 0.25);
      border-radius: 12px;
      padding: 32px;
      text-align: center;
    }}
    .blocked-badge {{
      display: inline-block;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 6px;
      margin-bottom: 12px;
      letter-spacing: 0.05em;
    }}
    .blocked-box h4 {{
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--text-main);
    }}
    .blocked-box p {{
      font-size: 0.85rem;
      color: var(--text-muted);
      max-width: 480px;
      line-height: 1.5;
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      background: var(--bg-card-alt);
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }}
    table.data-table th {{
      background: #111a2c;
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
    .badge-critical {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(244, 63, 94, 0.15);
      color: #fda4af;
      border: 1px solid rgba(244, 63, 94, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-high {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(245, 158, 11, 0.15);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-medium {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-pass {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: #6ee7b7;
      border: 1px solid rgba(16, 185, 129, 0.3);
      font-size: 0.72rem;
      font-weight: 700;
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
    ⚠️ SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Not actual VELOOP statistics.
  </div>

  <div class="dashboard-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1>VELOOP Rewards — Simulated Data Analytics Dashboard</h1>
        <p>Interactive verification telemetry computed from 1,000 simulated users across 15 relational sheets</p>
      </div>
      <div class="header-badge">
        <span class="pulse-dot"></span>
        Interactive GitHub Pages Build
      </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="tab-nav">
      <button class="tab-btn active" onclick="switchTab('tab-overview', this)">
        <span>📊</span> 1. Executive Overview
      </button>
      <button class="tab-btn" onclick="switchTab('tab-retention', this)">
        <span>👥</span> 2. User & Retention
      </button>
      <button class="tab-btn" onclick="switchTab('tab-engagement', this)">
        <span>⚡</span> 3. Engagement & Features
      </button>
      <button class="tab-btn" onclick="switchTab('tab-tasks', this)">
        <span>🎯</span> 4. Tasks
      </button>
      <button class="tab-btn" onclick="switchTab('tab-rewards', this)">
        <span>💎</span> 5. Rewards
      </button>
      <button class="tab-btn" onclick="switchTab('tab-quality', this)">
        <span>🛡️</span> 6. Data Quality
      </button>
      <button class="tab-btn" onclick="switchTab('tab-blocked', this)">
        <span>🚫</span> 7. Blocked KPIs
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
          <div class="kpi-subtext">48.6% of registered users active in last 7 days</div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-header">
            <span class="kpi-title">Monthly Active Users (MAU)</span>
            <span class="kpi-id">K05</span>
          </div>
          <div class="kpi-value">{kpi_map['K05']['value']:,}</div>
          <div class="kpi-subtext">81.2% of registered users active in last 30 days</div>
        </div>

        <div class="kpi-card amber">
          <div class="kpi-header">
            <span class="kpi-title">DAU / MAU Ratio (Stickiness)</span>
            <span class="kpi-id">K07</span>
          </div>
          <div class="kpi-value">{kpi_map['K07']['value'] * 100:.2f}%</div>
          <div class="kpi-subtext">Mean 30d DAU (103.5) ÷ 30d MAU (812)</div>
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
          <div class="kpi-subtext">5,627 completed out of 9,846 started tasks</div>
        </div>

        <div class="kpi-card purple">
          <div class="kpi-header">
            <span class="kpi-title">Total Rewards Credited</span>
            <span class="kpi-id">K28</span>
          </div>
          <div class="kpi-value">{kpi_map['K28']['value']:,} <span style="font-size: 1rem; color: var(--text-muted);">XP</span></div>
          <div class="kpi-subtext">4,799 milestone rewards (06_Milestones)</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Users Earning Rewards</span>
            <span class="kpi-id">K33</span>
          </div>
          <div class="kpi-value">{kpi_map['K33']['value']:,}</div>
          <div class="kpi-subtext">100.0% of cohort earned ≥1 reward / milestone</div>
        </div>
      </div>

      <!-- Overview Charts -->
      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>DAU Timeseries (Last 30 Calendar Days)</h3>
              <p>Daily unique active users with recorded event activity</p>
            </div>
            <span class="chart-tag">KPI K06</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-dau-timeseries"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 04_Daily_Activity & 03_Feature_Events</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Registrations by Day (Last 30 Days)</h3>
              <p>Daily volume of newly registered simulated accounts (Total: 184)</p>
            </div>
            <span class="chart-tag">KPI K02</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-reg-timeseries"></canvas>
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
              <h3>D1 / D7 / D30 Milestone Retention Rates</h3>
              <p>Percentage of eligible users active after registration day</p>
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
              <h3>Active Users by Monthly Cohort</h3>
              <p>Total cohort size vs. users active in final 30-day window</p>
            </div>
            <span class="chart-tag">Cohort Telemetry</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-cohorts"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 01_Users_1000 & 03_Feature_Events</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <div class="chart-grid-1">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Full Retention Curve (D1 through D30 Daily Cohort Decay)</h3>
              <p>Daily retention curve evaluated across eligible user cohorts</p>
            </div>
            <span class="chart-tag">KPI K37</span>
          </div>
          <div class="chart-canvas-wrap tall">
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
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Top-Line User Volume & Funnel Summary</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>Metric Name</th>
                <th>Value</th>
                <th>Proportion / Share</th>
                <th>Analytical Definition & Telemetry Source</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K01</td>
                <td>Total Registered Users</td>
                <td class="mono"><strong>1,000</strong></td>
                <td>100.0%</td>
                <td>Full user registry cohort size (01_Users_1000)</td>
              </tr>
              <tr>
                <td class="mono">K02</td>
                <td>New Users in Last 30 Days</td>
                <td class="mono">184</td>
                <td>18.4% of total</td>
                <td>Registrations between 2026-08-17 and 2026-09-15</td>
              </tr>
              <tr>
                <td class="mono">K03</td>
                <td>New Users in Last 7 Days</td>
                <td class="mono">47</td>
                <td>4.7% of total</td>
                <td>Registrations between 2026-09-09 and 2026-09-15</td>
              </tr>
              <tr>
                <td class="mono">K08</td>
                <td>Users Who Have Ever Logged In</td>
                <td class="mono">928</td>
                <td>92.8% of registered</td>
                <td>Users with non-null last_login_datetime (Users_1000_Clean); 98.4% have session logs</td>
              </tr>
              <tr>
                <td class="mono">K09</td>
                <td>Users Who NEVER Logged In</td>
                <td class="mono">72</td>
                <td>7.2% day-0 dormant</td>
                <td>Zero logins, pending verification state; 16 users have 0 sessions</td>
              </tr>
              <tr>
                <td class="mono">K10</td>
                <td>Returning Users (≥2 Active Days)</td>
                <td class="mono">826</td>
                <td>82.6% of registered</td>
                <td>Users logged into 04_Daily_Activity on at least 2 distinct calendar days</td>
              </tr>
              <tr>
                <td class="mono">K11</td>
                <td>Inactive Users (No Event in Last 14d)</td>
                <td class="mono">346</td>
                <td>34.6% dormant</td>
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
              <p>Percentage of all 1,000 registered users who engaged with each feature</p>
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

      <!-- Feature frequency table -->
      <div class="card" style="margin-top: 24px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Feature Frequency & Repeat Usage Matrix</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Feature Name</th>
                <th>Unique Users</th>
                <th>Total Events</th>
                <th>Adoption Rate (K15)</th>
                <th>Usage Frequency (K16)</th>
                <th>Repeat Usage Rate (K19)</th>
              </tr>
            </thead>
            <tbody id="feature-matrix-tbody">
              <!-- Dynamically populated from inline JSON -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 4: TASKS -->
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
      </div>

      <div class="chart-grid-2">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Task Outcome Distribution</h3>
              <p>Completion vs. explicit failure vs. user abandonment</p>
            </div>
            <span class="chart-tag">KPIs K22, K23</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-task-outcomes"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
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

      <div class="chart-grid-1">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Average Completion Time by Task Category (Seconds)</h3>
              <p>Average execution duration for successfully completed tasks</p>
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
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 5: REWARDS -->
    <!-- =================================================================== -->
    <div id="tab-rewards" class="tab-content">
      <div class="kpi-grid">
        <div class="kpi-card purple">
          <div class="kpi-header">
            <span class="kpi-title">Total Rewards Credited</span>
            <span class="kpi-id">K28</span>
          </div>
          <div class="kpi-value">{kpi_map['K28']['value']:,} <span style="font-size: 1rem; color: var(--text-muted);">XP</span></div>
          <div class="kpi-subtext">Sum of milestone_value (06_Milestones)</div>
        </div>

        <div class="kpi-card blocked">
          <div class="kpi-header">
            <span class="kpi-title">Avg Reward Per Completed Task</span>
            <span class="kpi-id blocked">K29</span>
          </div>
          <div class="kpi-value blocked">BLOCKED</div>
          <div class="kpi-subtext">05_Task_Activity lacks reward_amount column</div>
        </div>

        <div class="kpi-card blocked">
          <div class="kpi-header">
            <span class="kpi-title">Reward Reversal Rate</span>
            <span class="kpi-id blocked">K32</span>
          </div>
          <div class="kpi-value blocked">BLOCKED</div>
          <div class="kpi-subtext">Wallet_Ledger is missing; no reversal status</div>
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

      <div class="chart-grid-2">
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
            <h4>BLOCKED — See KPI K30 Blocker</h4>
            <p>05_Task_Activity contains reward_status ('Credited': 5,627) but completely lacks a numeric reward_amount or points column. Dedicated Task_Master and Wallet_Ledger tables are absent from the supplied workbook.</p>
          </div>
          <div class="chart-footer">
            <span>Source: 05_Task_Activity</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <h3>Reward Amount by Feature</h3>
              <p>Gross milestone reward units credited by feature source (Total: 242,830)</p>
            </div>
            <span class="chart-tag">KPI K31</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-rewards-feature"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: 06_Milestones & 03_Feature_Events</span>
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
              <p>Frequency of detected anomalies across messy audit baseline tables</p>
            </div>
            <span class="chart-tag">KPIs K38–K44</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-dq-issues"></canvas>
          </div>
          <div class="chart-footer">
            <span>Source: Users_Messy_Audit & 10_Event_Data_Quality_Audit</span>
            <span>SIMULATED DATA</span>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 24px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Comprehensive Telemetry Quality Audit Register</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>Data Quality Check</th>
                <th>Affected Records</th>
                <th>Affected %</th>
                <th>Severity</th>
                <th>Detection Scope & Example Record</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K38</td>
                <td>Duplicate user_ids</td>
                <td class="mono"><strong>16 rows</strong></td>
                <td>1.59%</td>
                <td><span class="badge-critical">Critical</span></td>
                <td>8 duplicate pairs in Users_Messy_Audit (e.g., VLUSR000142, Aditya Patel)</td>
              </tr>
              <tr>
                <td class="mono">K39</td>
                <td>Rows with missing user_id</td>
                <td class="mono">0 rows</td>
                <td>0.00%</td>
                <td><span class="badge-pass">Pass</span></td>
                <td>Zero nulls across Users_Messy_Audit and 10_Event_Data_Quality_Audit</td>
              </tr>
              <tr>
                <td class="mono">K40</td>
                <td>Malformed or null timestamps</td>
                <td class="mono"><strong>2 rows</strong></td>
                <td>0.20%</td>
                <td><span class="badge-critical">Critical</span></td>
                <td>Users_Messy_Audit: 1 null registration date (VLUSR000451) + 1 invalid month 14 '2026-14-05' (VLUSR000788)</td>
              </tr>
              <tr>
                <td class="mono">K41</td>
                <td>Invalid status values</td>
                <td class="mono"><strong>4 rows</strong></td>
                <td>0.01%</td>
                <td><span class="badge-medium">Medium</span></td>
                <td>10_Event_Data_Quality_Audit: 'success ' (lowercase + trailing space) outside canonical enum</td>
              </tr>
              <tr>
                <td class="mono">K42</td>
                <td>Orphan records (user_id not in users)</td>
                <td class="mono">0 records</td>
                <td>0.00%</td>
                <td><span class="badge-pass">Pass</span></td>
                <td>100% of events (35,714), sessions (7,913), and tasks (9,846) link to valid registered user IDs</td>
              </tr>
              <tr>
                <td class="mono">K43</td>
                <td>Negative amounts</td>
                <td class="mono"><strong>4 rows</strong></td>
                <td>0.40%</td>
                <td><span class="badge-medium">Medium</span></td>
                <td>Users_Messy_Audit: days_since_registration has negative values (-0.803, -0.655) due to snapshot baseline offset</td>
              </tr>
              <tr>
                <td class="mono">K44</td>
                <td>Trailing-whitespace categorical values</td>
                <td class="mono"><strong>4 rows</strong></td>
                <td>0.01%</td>
                <td><span class="badge-medium">Medium</span></td>
                <td>10_Event_Data_Quality_Audit: event_status column has unstripped trailing spaces</td>
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
      <div class="card" style="margin-bottom: 24px; border-left: 4px solid var(--accent-rose);">
        <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; color: #fca5a5;">Blocked KPI Transparency Notice</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">
          These KPIs cannot be calculated from the supplied simulated data because the required tables are absent. They are listed for transparency rather than invented. In production, these metrics require transactional ledgers and event broker instrumentation as documented in the table below.
        </p>
      </div>

      <div class="card">
        <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 14px;">Inventory of Blocked Metrics (8 KPIs)</h3>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI ID</th>
                <th>KPI Name</th>
                <th>Status</th>
                <th>Blocker Reason & Missing Source Entities</th>
                <th>Business Impact</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">K29</td>
                <td>Average reward per completed task</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>05_Task_Activity lacks a numeric reward_amount column; Task_Master and Wallet_Ledger tables are missing</td>
                <td>Cannot evaluate micro-task payout unit economics or user payout ROI.</td>
              </tr>
              <tr>
                <td class="mono">K30</td>
                <td>Reward distribution by task_type</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>05_Task_Activity lacks reward_amount column, and Task_Master / Wallet_Ledger tables are missing</td>
                <td>Inability to track financial liability burn segmented by task category.</td>
              </tr>
              <tr>
                <td class="mono">K32</td>
                <td>Reward reversals (count and %)</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Wallet_Ledger is missing and 05_Task_Activity reward_status lacks a Reversal status</td>
                <td>Blindness to clawbacks, fraud cancellations, and chargeback exposure.</td>
              </tr>
              <tr>
                <td class="mono">K45</td>
                <td>Wallet credits total</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Wallet_Ledger table is missing from supplied workbooks</td>
                <td>Cannot audit cumulative currency liabilities or platform XP inflation.</td>
              </tr>
              <tr>
                <td class="mono">K46</td>
                <td>Withdrawal completion rate</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Withdrawals table is missing from supplied workbooks</td>
                <td>Inability to assess cash, UPI, or voucher disbursement reliability and SLA.</td>
              </tr>
              <tr>
                <td class="mono">K47</td>
                <td>Withdrawal processing time (median)</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Withdrawals table is missing from supplied workbooks</td>
                <td>Disbursement lifecycle turnaround times cannot be measured.</td>
              </tr>
              <tr>
                <td class="mono">K48</td>
                <td>Referral conversion rate</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Referral_Invites and Referral_Conversions tracking tables are missing from supplied workbooks</td>
                <td>Cannot compute viral coefficient (K-factor) or invite-to-registration conversion.</td>
              </tr>
              <tr>
                <td class="mono">K49</td>
                <td>Referral activations</td>
                <td><span class="badge-critical">BLOCKED</span></td>
                <td>Referral_Activations table is missing from supplied workbooks</td>
                <td>Referee downstream milestone completion tracking is absent.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="dashboard-footer">
      <div>
        Data source: <span class="mono">veloop_simulated_user_behavior_1000.xlsx</span> and <span class="mono">veloop_rewards_data_01.xlsx</span> (simulated).
      </div>
      <div>
        Generated on <strong>{today_str}</strong> | Built for GitHub Pages
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

  <!-- Embedded Helper Datasets -->
  <script type="application/json" id="helper-data">
{json.dumps({
    "task_timing": task_timing_by_cat,
    "cohorts": cohort_data
}, indent=2)}
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

      // Trigger resize on visible Chart.js instances so canvas dimensions adjust properly
      window.dispatchEvent(new Event('resize'));
    }}

    // Parse embedded JSON payloads
    const kpiPayload = JSON.parse(document.getElementById('kpi-data').textContent);
    const helperPayload = JSON.parse(document.getElementById('helper-data').textContent);
    const kpis = {{}};
    kpiPayload.kpis.forEach(k => {{ kpis[k.kpi_id] = k; }});

    // Populate Feature Matrix Table in Tab 3
    (function populateFeatureMatrix() {{
      const tbody = document.getElementById('feature-matrix-tbody');
      if (!tbody) return;
      
      const adoptions = kpis['K15'].value; // {{feat: pct}}
      const frequencies = kpis['K16'].value; // {{feat: freq}}
      const repeats = kpis['K19'].value; // {{feat: pct}}
      const uniqueUsers = {{
        'Watch Ads': 836, 'Daily Reward': 835, 'Streak Rewards': 832, 'CAPTCHA': 824,
        'Referral': 811, 'Wallet': 810, 'Tap & Earn': 800, 'Mining Rewards': 799,
        'Level System': 773, 'Missions': 771, 'Spin the Wheel': 763, 'Exchange Center': 720,
        'Leaderboard': 686, 'Follow & Earn': 685, 'Badges': 674
      }};
      const totalEvents = {{
        'Watch Ads': 3126, 'Missions': 2780, 'Streak Rewards': 2734, 'CAPTCHA': 2733,
        'Tap & Earn': 2654, 'Mining Rewards': 2616, 'Referral': 2521, 'Daily Reward': 2499,
        'Level System': 2427, 'Spin the Wheel': 2425, 'Wallet': 2172, 'Leaderboard': 1836,
        'Badges': 1832, 'Exchange Center': 1690, 'Follow & Earn': 1659
      }};

      Object.keys(adoptions).forEach(feat => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{feat}}</strong></td>
          <td class="mono">${{uniqueUsers[feat] || '-'}}</td>
          <td class="mono">${{totalEvents[feat] ? totalEvents[feat].toLocaleString() : '-'}}</td>
          <td class="mono"><span style="color: var(--accent-cyan); font-weight: 600;">${{adoptions[feat]}}%</span></td>
          <td class="mono">${{frequencies[feat] || '-'}} events/user</td>
          <td class="mono"><span style="color: var(--accent-emerald); font-weight: 600;">${{repeats[feat]}}%</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }})();

    // Chart.js Theme Configurations
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.tooltip.backgroundColor = '#0b0f19';
    Chart.defaults.plugins.tooltip.borderColor = '#334b6e';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#cbd5e1';

    // 1. DAU Timeseries Line Chart (K06)
    const ctxDau = document.getElementById('chart-dau-timeseries').getContext('2d');
    const dauData = kpis['K06'].value; // {{date: count}}
    const dauLabels = Object.keys(dauData);
    const dauValues = Object.values(dauData);

    const gradDau = ctxDau.createLinearGradient(0, 0, 0, 300);
    gradDau.addColorStop(0, 'rgba(6, 182, 212, 0.4)');
    gradDau.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

    new Chart(ctxDau, {{
      type: 'line',
      data: {{
        labels: dauLabels,
        datasets: [{{
          label: 'Daily Active Users (DAU)',
          data: dauValues,
          borderColor: '#06b6d4',
          backgroundColor: gradDau,
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointBackgroundColor: '#06b6d4',
          pointHoverRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }}
        }},
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
    const ctxReg = document.getElementById('chart-reg-timeseries').getContext('2d');
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
          tooltip: {{
            callbacks: {{
              label: (ctx) => `${{ctx.parsed.y}}% of eligible cohort`
            }}
          }}
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

    // 4. Cohort Active 30d Bar Chart
    const ctxCohorts = document.getElementById('chart-cohorts').getContext('2d');
    new Chart(ctxCohorts, {{
      type: 'bar',
      data: {{
        labels: helperPayload.cohorts.cohorts,
        datasets: [
          {{
            label: 'Total Registered in Cohort',
            data: helperPayload.cohorts.registered,
            backgroundColor: 'rgba(71, 85, 105, 0.65)',
            borderRadius: 6
          }},
          {{
            label: 'Active in Final 30 Days',
            data: helperPayload.cohorts.active_30d,
            backgroundColor: '#10b981',
            borderRadius: 6
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top' }} }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 5. Full Retention Curve Line Chart (K37)
    const ctxCurve = document.getElementById('chart-retention-curve').getContext('2d');
    const curvePoints = kpis['K37'].value; // [{{day, eligible_users, retained_users, retention_rate_pct}}]
    const curveLabels = curvePoints.map(p => `D${{p.day}}`);
    const curveValues = curvePoints.map(p => p.retention_rate_pct);

    const gradCurve = ctxCurve.createLinearGradient(0, 0, 0, 400);
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
          pointHoverRadius: 7
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

    // 8. Feature Adoption Rate Horizontal Bar (K15)
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

    // 9. Task Outcome Doughnut (K22, K23)
    const ctxTaskOutcomes = document.getElementById('chart-task-outcomes').getContext('2d');
    new Chart(ctxTaskOutcomes, {{
      type: 'doughnut',
      data: {{
        labels: ['Completed (57.15%)', 'Abandoned (20.83%)', 'Failed (15.44%)', 'Pending (6.58%)'],
        datasets: [{{
          data: [5627, 2051, 1520, 648],
          backgroundColor: ['#10b981', '#f59e0b', '#f43f5e', '#64748b'],
          borderColor: '#131c2e',
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
              label: (ctx) => ` ${{ctx.label}}: ${{ctx.parsed.toLocaleString()}} tasks`
            }}
          }}
        }},
        cutout: '62%'
      }}
    }});

    // 10. Task Attempts by Category (K25)
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

    // 11. Average Duration by Task Category (K24 sub-breakdown)
    const ctxTaskDur = document.getElementById('chart-task-duration').getContext('2d');
    const durEntries = Object.entries(helperPayload.task_timing).sort((a,b) => b[1] - a[1]);
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
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: (ctx) => `${{ctx.parsed.y.toLocaleString()}} reward units / XP` }} }}
        }},
        scales: {{
          x: {{ grid: {{ display: false }} }},
          y: {{
            beginAtZero: true,
            grid: {{ color: 'rgba(255, 255, 255, 0.04)' }}
          }}
        }}
      }}
    }});

    // 13. Data Quality Issues Bar Chart (K38–K44)
    const ctxDq = document.getElementById('chart-dq-issues').getContext('2d');
    const dqLabels = [
      'Duplicate Users (K38)',
      'Missing User ID (K39)',
      'Malformed Timestamps (K40)',
      'Invalid Status Enum (K41)',
      'Orphan Records (K42)',
      'Negative Amounts (K43)',
      'Trailing Whitespace (K44)'
    ];
    const dqValues = [
      kpis['K38'].value,
      kpis['K39'].value,
      kpis['K40'].value,
      kpis['K41'].value,
      kpis['K42'].value,
      kpis['K43'].value,
      kpis['K44'].value
    ];
    const dqColors = [
      '#f43f5e', // Critical
      '#10b981', // Pass
      '#f43f5e', // Critical
      '#3b82f6', // Medium
      '#10b981', // Pass
      '#3b82f6', // Medium
      '#3b82f6'  // Medium
    ];

    new Chart(ctxDq, {{
      type: 'bar',
      data: {{
        labels: dqLabels,
        datasets: [{{
          label: 'Anomalous Records Count',
          data: dqValues,
          backgroundColor: dqColors,
          borderRadius: 6
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
    print(f"[OK] Dashboard successfully created at: {out_html.resolve()}")
    print(f"     File size: {file_size_kb:.2f} KB ({out_html.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
