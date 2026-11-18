# VELOOP Analytics Dashboard — Quality Assurance Checklist

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.**

---

## 1. Scope & Test Environment

- **Canonical URL:** `https://er-arib-khan.github.io/veloop-analytics/`
- **Primary Committed Artifact:** [`docs/index.html`](file:///home/rib/project/veloop-analytics/docs/index.html)
- **Source of Truth:** [`13_analysis/outputs/02_kpis.json`](file:///home/rib/project/veloop-analytics/13_analysis/outputs/02_kpis.json)
- **Harness Runner:** [`docs/qa_dashboard_runner.py`](file:///home/rib/project/veloop-analytics/docs/qa_dashboard_runner.py)
- **Test Protocol:** Dual execution across local `file://` offline protocol and live GitHub Pages deployment.

---

## 2. Test Plan Groups & Check Catalog

### GROUP A — Structure & Navigation
| Check ID | Check Description | Verification Method | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **A1** | All 7 tabs exist and are clickable | Programmatic click / DOM inspect | Tabs 1–7 exist (`overview`, `retention`, `engagement`, `tasks`, `rewards`, `quality`, `blocked`), each transitions smoothly without DOM exceptions. |
| **A2** | Each tab loads within 2 seconds | Navigation timing benchmark | Tab switch and chart re-render latency $\le 2000$ ms. |
| **A3** | No console errors on any tab | Browser `page.on('console')` event listener | Zero unhandled JS errors, zero Chart.js initialization exceptions across all 7 views. |
| **A4** | Browser back/forward navigation works | Hash change / state history dispatch | History navigation toggles between previously viewed tabs without page reload or broken state. |
| **A5** | All 13 chart canvases exist in the DOM | Canvas element count & ID assertion | Exactly 13 `<canvas>` elements exist with valid rendering contexts (`chart-dau`, `chart-reg`, `chart-retention-bars`, `chart-retention-curve`, `chart-top5-users`, `chart-top5-events`, `chart-feature-adoption`, `chart-task-funnel`, `chart-task-categories`, `chart-task-duration`, `chart-task-failure-rate`, `chart-rewards-feature`, `chart-dq-issues`). |

---

### GROUP B — Calculation Accuracy & KPI Synchronization
| Check ID | Check Description | Verification Method | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **B1** | Every KPI card displays a value matching `02_kpis.json` | Cross-comparison against JSON ground truth | All computed KPI metric values (e.g. K01=1,000, K08=98.4%, K14=51.81s, K22=57.15%, K28=242,830, K34=17.91%, K38=16) match `02_kpis.json` values exactly. |
| **B2** | Every chart's segments sum to the total KPI value | Chart dataset summation | Segment components sum exactly to the parent total (e.g., Task Funnel segments: 5,627 completed + 2,051 abandoned + 1,520 failed + 648 pending = 9,846 total started tasks). |
| **B3** | Tooltips show the exact value, not "undefined" or "NaN" | Tooltip callback extraction / string inspection | Tooltips render formatted numeric values and percentages; no instances of `"undefined"`, `"NaN"`, or `"[object Object]"`. |
| **B4** | Units are correct (%, count, seconds, XP) | Card label and suffix parsing | Metric cards display explicit, standardized units: percentages (`%`), durations (`s`), currency/points (`XP`), and counts (`users`, `sessions`, `tasks`). |
| **B5** | K28 shows "PARTIAL" label with footnote visible | DOM badge and footnote presence | KPI K28 card prominently displays the `PARTIAL` scope badge and details the 10,941 XP reconciliation gap footnote. |
| **B6** | K30 shows "BLOCKED" diagnostic card | DOM inspection in Rewards and Blocked tabs | K30 renders with a `BLOCKED` status badge, diagnostic message explaining missing reward amount in `05_Task_Activity`, and unblock path. |

---

### GROUP C — Data Provenance & Governance
| Check ID | Check Description | Verification Method | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **C1** | "SIMULATED DATA" banner visible on every tab | Header / container visibility check | Prominent warning banner (`SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`) is permanently fixed and visible across all tab views. |
| **C2** | Footer shows source file names | Footer text parsing | Footer explicitly documents source files: `veloop_simulated_user_behavior_1000.xlsx` and `veloop_rewards_data_01.xlsx`. |
| **C3** | Blocked KPIs tab lists exactly 8 KPIs | Table row count in Tab 7 (`tab-blocked`) | Exactly 8 blocked KPIs are enumerated: `K29`, `K30`, `K32`, `K45`, `K46`, `K47`, `K48`, `K49`. |
| **C4** | No chart shows a value not in `02_kpis.json` | Dataset number auditing | All chart points, slices, and bar heights correspond strictly to audited figures in `02_kpis.json`. |

---

### GROUP D — Responsiveness & Layout
| Check ID | Check Description | Verification Method | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **D1** | Layout works at 375px (mobile) | Viewport 375×812 screenshot | No horizontal overflow, text wraps cleanly, tabs horizontally scroll or wrap. |
| **D2** | Layout works at 768px (tablet) | Viewport 768×1024 screenshot | Grid columns collapse gracefully to 2-column layout; charts maintain aspect ratio. |
| **D3** | Layout works at 1440px (desktop) | Viewport 1440×900 screenshot | Standard 4-column KPI card grid, 2-column chart grid, full navigation bar visibility. |
| **D4** | Charts resize without clipping labels | Canvas bounding box inspection | Chart axes, tick marks, and legend badges remain fully legible without label clipping. |
| **D5** | KPI cards stack in one column on mobile | CSS grid computed style at 375px | Card container computes to single column (`grid-template-columns: 1fr` or single card width $\ge 90\%$). |

---

### GROUP E — Edge Cases & Offline Reliability
| Check ID | Check Description | Verification Method | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **E1** | Blocked KPI charts show "BLOCKED" text, not blank | Blocked tab visual check | Blocked KPI visual cards display informative diagnostics rather than empty/broken canvas elements. |
| **E2** | No negative percentages where positive expected | Text regex search for `-\d+(\.\d+)?%` | No nonsensical negative percentages in retention, completion, or adoption rates. |
| **E3** | Page works offline (`file://` protocol) | Load `docs/index.html` via `file://` | CSS, inline SVG icons, inline Chart.js scripts render completely without external CDN network dependencies. |
