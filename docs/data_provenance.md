# VELOOP Analytics — Data Provenance

> **SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.**
> Every number in this repository describes the supplied simulated
> dataset. Not actual VELOOP statistics. None are actual VELOOP production metrics.

## 1. What Data Is In This Repository

Two simulated workbooks:
- `veloop_simulated_user_behavior_1000.xlsx` (10 sheets, ~42,000 rows)
- `veloop_rewards_data_01.xlsx` (5 sheets, including Users_Messy_Audit)

No production VELOOP data. No real user data. No real revenue,
earnings, withdrawals, retention, conversion, or performance statistics.

## 2. What Every Number Represents

A property of the simulated dataset. Not a VELOOP statistic. Not a
production metric. Every figure in `analysis_findings.md`,
`business_recommendations.md`, `executive_summary.md`, `02_kpis.json`,
and `docs/index.html` describes the simulated data, not the real
product. Not actual VELOOP statistics.

## 3. What This Repository CAN Be Used For

- Analytics design review (how KPIs should be defined)
- Schema review (ledger_entries, withdrawals, referrals)
- KPI definition review (formulas, sources, limitations)
- Dashboard UX review (layout, tab structure, chart types)
- Instrumentation requirements (event tracking plan)
- Data quality framework review (terminology, controls)

## 4. What This Repository CANNOT Be Used For

- VELOOP business reporting (numbers are simulated)
- Investor or board presentations
- Production capacity planning
- User-facing communication
- Marketing claims
- Financial forecasts

## 5. The Replacement Protocol

When production data becomes available:

1. Simulated workbooks are replaced (not merged) with governed
   production extracts.
2. Every KPI in `02_kpis.json` is recomputed against production data.
3. The `validate_kpis.py` harness is re-run to verify no regression.
4. Every dashboard chart is re-verified against the new values.
5. The simulated outputs are archived (not deleted) for audit trail.
6. Every "SIMULATED DATA" banner is removed from the production branch
   and replaced with "Production Data — <date>" header.
7. Every file in `13_analysis/outputs/` gets a `_archived_simulated`
   suffix so provenance is unambiguous.

## 6. Authenticity Statement (Full)

All datasets in this repository are simulated. They were not collected
from real VELOOP users. Every figure in analysis_findings.md,
business_recommendations.md, executive_summary.md, 02_kpis.json, and
docs/index.html describes a property of the simulated dataset, not a
claim about VELOOP's real-world performance. Where a KPI could not be
calculated from the supplied data, it is explicitly marked BLOCKED with
the missing dependency named. Where a fact could not be verified, it is
recorded in the Assumption Register as "To Be Verified."
