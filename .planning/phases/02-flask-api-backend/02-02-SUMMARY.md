# 02-02 Summary: REST API Endpoints

**Status**: Complete ✓
**Date**: 2026-05-22

## Delivered

### app/api/__init__.py
- Blueprint `api_bp` at `/api` prefix, imports routes at bottom

### app/api/errors.py
- `error_response(message, status_code=400)` — consistent `{"error": ...}` JSON wrapper

### app/api/validators.py
- `validate_batch_input(data)` — validates all 8 fields (presence, type, range, categoricals)
- Returns `(cleaned_dict, None)` on success, `(None, error_message)` on failure
- Normalizes casing: supplier → title, visual → lowercase
- Ranges: temperature 90-140, moisture 0-10, pH 2-9, color_score 0-100, cooking_time 30-150, dryness_level 1-5

### app/api/routes.py

| Endpoint | Method | Class | Description |
|----------|--------|-------|-------------|
| `/api/predict` | POST | PredictAPI | Validate → predict → recommend → 200 `{grade, confidence, recommendation}` |
| `/api/batches` | GET | BatchAPI | Paginated list (per_page ≤ 100), `{batches, total, page, per_page, pages}` |
| `/api/batches` | POST | BatchAPI | Create batch (auto-generates B-YYYY-NNN), returns 201 with full record |
| `/api/feature-importance` | GET | FeatureImportanceAPI | Returns `{features: [{feature, importance}...]}` sorted descending |

## Edge Cases Verified
- Missing fields → 400 with field name
- Out-of-range values → 400 with range message
- Invalid categoricals → 400 with allowed values
- Duplicate batch_id → 409 Conflict
- Empty/invalid JSON body → 400
- per_page > 100 → silently capped to 100
- page > total pages → empty list, not error
- All parameterized SQL queries (no string concatenation)
