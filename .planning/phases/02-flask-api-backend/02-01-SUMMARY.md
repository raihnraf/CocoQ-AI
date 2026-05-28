# 02-01 Summary: Database + Prediction Engine

**Status**: Complete ✓
**Date**: 2026-05-22

## Delivered

### app/db.py
- `get_db()` — returns sqlite3.Row connection, uses `flask.g` pattern, stored in `g.db`
- `init_db(app)` — creates `batches` (12 cols) and `predictions` (6 cols) tables with `IF NOT EXISTS`, enables foreign keys pragma
- `init_app(app)` — calls `init_db(app)`, registers `close_db` on `app.teardown_appcontext`
- `close_db(exception)` — cleanly pops and closes `g.db`
- Database path from `app.config['DATABASE']` (defaults to `database.db` in project root)

### app/ml/predict.py
- `load_model(path)` — joblib.load with helpful FileNotFoundError message
- `predict_batch(pipeline, input_dict)` — encodes categoricals (alphabetical LabelEncoder order for supplier), normalizes casing, returns `{grade, confidence, probabilities}`
- `get_feature_importance(pipeline, path)` — loads from JSON, fallback to pipeline extraction, sorted descending
- `generate_recommendation(grade, input_dict)` — grade-specific base messages + parameter-specific append advice

**Key fix**: Supplier encoding uses alphabetical order (matching LabelEncoder from train_model.py), not the manual mapping in the plan.

## Verification

- Both tables created with correct columns
- Model loads from `models/quality_model.pkl`
- Prediction returns grade + confidence (Grade A, 0.54 on test input)
- Feature importance sorted: moisture (0.344) > temperature (0.228) > pH (0.137)
- Casing normalization works (central java → Central Java, Good → good)
- Recommendation function handles all grades and parameter thresholds
