# 03-02-SUMMARY.md — Dashboard Homepage: Stats, Charts, IoT Button

**Status:** Complete  
**Requirements covered:** UI-01, WF-01  
**Depends on:** 03-01

## What was built

1. **GET /api/stats endpoint** (`StatsAPI` class in `app/api/routes.py`):
   - Returns `total_batches`, `grade_distribution` (count + percentage per grade), `reject_rate`, `reject_trend` (last 7 days)
   - Edge case: zero batches returns zeros gracefully
   - Queries both `batches` and `predictions` tables

2. **app/templates/dashboard.html** — extends base.html:
   - 4 stat cards (Total Batches, Grade A%, Grade B%, Reject Rate%)
   - 2 chart containers (grade-dist-chart, reject-trend-chart) using charts.js functions
   - IoT simulation button: generates random batch data → POST /api/predict → displays result → refreshes stats + chart
   - Button disabled during request to prevent spam

## Fixes during execution
- **PredictAPI.post now saves to DB**: Previously only returned prediction JSON. Now inserts into both `batches` and `predictions` tables so stats work.
- Refactored dashboard to use shared `charts.js` instead of duplicated inline chart code.

## Verification
- GET /api/stats returns correct distribution after predictions
- Dashboard renders with live data from API
- IoT button generates valid data, gets prediction, displays result, refreshes stats
- Charts render via charts.js functions
