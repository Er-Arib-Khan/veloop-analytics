# VELOOP Rewards — Analytics Foundation Blueprint

> **⚠️ SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.** All figures in this
> repository describe the supplied simulated dataset. They are **not** actual
> VELOOP users, revenue, earnings, withdrawals, retention, conversion rates,
> or company statistics.

**🔗 Live interactive dashboard:** https://er-arib-khan.github.io/veloop-analytics/
**📊 Analysis findings:** [`13_analysis/analysis_findings.md`](13_analysis/analysis_findings.md)
**💡 Business recommendations:** [`13_analysis/business_recommendations.md`](13_analysis/business_recommendations.md)
**📄 Executive summary:** [`12_final/executive_summary.md`](12_final/executive_summary.md)

---

## 📖 The 30-Second Read

| Metric | Value | Meaning |
|--------|-------|---------|
| **Registered users** | 1,000 | Base cohort (K01) |
| **Monthly active users** | 812 (81.2%) | K05 |
| **Task completion rate** | **57.15%** | 5,627 of 9,846 started (K22) |
| **Not-completed tasks** | **42.85%** | 4,219 tasks — 15.44% failed, 20.83% abandoned, 6.58% pending |
| **D1 / D7 / D30 retention** | 17.91% / 13.33% / 8.46% | K34–K36 — steepest drop is D1→D7 |
| **Duplicate user IDs** | 16 rows / 8 distinct IDs | K38 — data integrity flag |
| **Virtual currency gap** | **10,941 XP shortfall** | 242,830 milestone units vs 231,889 XP balance (K28 PARTIAL) |
| **KPIs computed** | 41 of 49 (83.7%) | 1 PARTIAL (K28), 8 BLOCKED (missing tables) |
| **Live dashboard** | 13 charts, 7 tabs, 127 KB | Working HTML, GitHub Pages deployed |

**Three headline findings:**
1. **Task funnel leaks 42.85%** — dominated by external dependencies (732 validation failures, 722 unavailable tasks), not user error.
2. **Retention collapses in week 1** — D1→D7 drops 4.58 points. The biggest possible improvement lever is first-week engagement.
3. **Wallet, Withdrawals, Referrals instrumentation is entirely missing** — 8 KPIs are BLOCKED until the tables exist.

---

## 🚦 Choose Your Path

| If you are... | Start here | Then read |
|---------------|-----------|-----------|
| **A reviewer or team lead** | [`12_final/executive_summary.md`](12_final/executive_summary.md) (3 pages) | [`13_analysis/analysis_findings.md`](13_analysis/analysis_findings.md) → live dashboard |
| **A data analyst** | [`13_analysis/run_analysis.py`](13_analysis/run_analysis.py) → [`13_analysis/outputs/02_kpis.json`](13_analysis/outputs/02_kpis.json) | [`07_data_quality/profiling_summary.xlsx`](07_data_quality/) → [`05_data_model/data_dictionary.xlsx`](05_data_model/) |
| **An engineer** | [`09_engineering/developer_analytics_handoff.xlsx`](09_engineering/) | [`04_events/event_tracking_plan.xlsx`](04_events/) → [`05_data_model/er_diagram.dbml`](05_data_model/) |
| **A product manager** | [`13_analysis/business_recommendations.md`](13_analysis/business_recommendations.md) | [`06_kpis/kpi_catalogue.xlsx`](06_kpis/) → [`11_backlog/implementation_backlog.xlsx`](11_backlog/) |
| **Someone who wants the live demo** | https://er-arib-khan.github.io/veloop-analytics/ | — |

---

## 🗂️ Project at a Glance
