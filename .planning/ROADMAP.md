# ROADMAP: CocoQ-AI

**Created:** 2026-05-22
**Total Phases:** 3
**Total v1 Requirements:** 23
**Mode:** YOLO | Granularity: Coarse | Parallel: Yes

---

## Phase 1: ML Pipeline & Data Foundation ✓

**Goal:** Train a working classification model and create the simulated dataset that powers the entire demo.

**Requirements:** ML-01 ✓, ML-02 ✓, ML-04 ✓, DATA-01 ✓, DATA-02 ✓, DATA-03 ✓

**Status:** Complete — 2/2 plans, 100% accuracy model, 200 batch records, top 3 features: moisture/temperature/pH

**Success Criteria:**
1. `train_model.py` runs and produces `models/quality_model.pkl` with >80% training accuracy
2. `data/coconut_sugar_batches.csv` contains 200+ realistic batch records with all required features (temperature, moisture, pH, color score, cooking time, supplier origin, dryness level, visual inspection)
3. Simulated data generator (`app/ml/generate_data.py`) produces new batches with realistic parameter distributions based on domain rules
4. Feature importance output shows temperature, moisture, and pH as top predictors
5. Scikit-Learn Pipeline (`make_pipeline`) used for preprocessing + model to prevent data leakage
6. Model saved with Joblib using protocol=5 for efficient NumPy array serialization

**Technical Approach:**
- Use `sklearn.pipeline.make_pipeline` with `StandardScaler` + `RandomForestClassifier(n_estimators=100)`
- Generate synthetic data with domain-knowledge rules: Grade A batches have optimal ranges, Grade B slightly off, Reject outside acceptable bounds
- Features: temperature (105-125°C), moisture (1-5%), pH (4.5-7.0), color_score (0-100), cooking_time (60-120min), supplier_origin (categorical), dryness_level (1-5), visual_inspection (categorical)
- Target: grade (Grade A, Grade B, Reject)
- Split 80/20 train/test, report accuracy, classification report

**Plans:** 2 plans

Plans:
- [ ] 01-01-PLAN.md — Project structure, dependencies, and synthetic data generator with domain-knowledge rules
- [ ] 01-02-PLAN.md — Train Random Forest model with scikit-learn Pipeline, evaluate, and save

**Threat Model:**
- Unrealistic data distributions → model learns noise instead of patterns
- Overfitting on small dataset → model performs poorly on "new" data
- Mitigation: Use domain-knowledge-based rules to generate realistic data; cross-validation

---

## Phase 2: Flask API & Backend

**Goal:** Build the Flask backend with REST endpoints for predictions, batch management, and SQLite persistence.

**Requirements:** API-01, API-02, API-03, API-04, ML-03

**Success Criteria:**
1. `POST /api/predict` accepts batch parameters and returns `{grade, confidence, recommendation}` JSON
2. `GET /api/batches` returns paginated batch history from SQLite
3. `POST /api/batches` creates new batch record, stores in SQLite, returns created record
4. `GET /api/feature-importance` returns model feature importance data as JSON
5. SQLite database `database.db` persists across server restarts
6. Application factory pattern (`create_app()`) with separate `main` and `api` blueprints
7. MethodView used for REST API endpoints

**Technical Approach:**
- Flask 3.1.x with application factory: `app/__init__.py` → `create_app()`
- Blueprint `api` at `/api` prefix with MethodView classes: `PredictAPI`, `BatchAPI`, `FeatureImportanceAPI`
- Blueprint `main` at `/` for page routes: dashboard, predict form, history
- SQLite via `sqlite3` stdlib with row factory for dict-like access
- Model loaded once at app startup via `app/ml/predict.py` → `load_model()`
- Input validation on all API endpoints with JSON error responses

**Threat Model:**
- API input validation gaps → crashes on malformed requests
- Model loading failures → server errors if model file missing
- Mitigation: Validate all inputs, graceful error handling with JSON responses, check model file exists on startup

---

## Phase 3: Dashboard & Analytics UI

**Goal:** Build the interactive dashboard with forms, charts, predictions, and recommendations — the visible demo.

**Requirements:** UI-01 through UI-09, WF-01, WF-02, WF-03

**Success Criteria:**
1. Dashboard homepage displays production summary (total batches, grade distribution %, reject rate %)
2. Batch input form validates and submits data via fetch to `/api/predict`, shows prediction result with confidence score
3. Chart.js 4.x renders grade distribution (doughnut chart) and reject rate trend (line chart)
4. Prediction history table shows past 50 predictions with search/filter
5. Feature importance horizontal bar chart displays top factors
6. Recommendation messages appear based on predicted grade and conditions (e.g., "Moisture level is within export-grade range. Batch is suitable for packaging.")
7. Simulated IoT button generates random batch data, auto-submits to prediction API, updates dashboard
8. Layout is responsive — works on mobile viewport (375px+) using CSS grid/flexbox

**Technical Approach:**
- Flask templates with Jinja2: `base.html` (layout), `dashboard.html`, `predict.html`, `history.html`
- Chart.js 4.x via CDN, initialized in `static/js/charts.js`
- Responsive containers: `<div style="position:relative; height:40vh">` for each chart
- CSS grid for dashboard layout, flexbox for form elements
- Fetch API for async prediction calls, no page reload
- Bootstrap-like utility classes (custom, no heavy framework)
- Recommendation engine: rule-based logic in `app/ml/predict.py` that checks parameter ranges and returns actionable messages

**Threat Model:**
- Chart rendering failures → blank dashboard sections
- Form submission errors → poor demo experience
- Mitigation: Graceful fallbacks, loading states, error messages, try/catch in JS

---

## Coverage Validation

| Phase | Requirements | Count |
|-------|-------------|-------|
| Phase 1 | ML-01, ML-02, ML-04, DATA-01, DATA-02, DATA-03 | 6 |
| Phase 2 | API-01, API-02, API-03, API-04, ML-03 | 5 |
| Phase 3 | UI-01–UI-09, WF-01, WF-02, WF-03 | 12 |
| **Total** | | **23** |

All 23 v1 requirements mapped ✓

## CV Bullet Point Traceability

| CV Bullet | Phases | Requirements |
|-----------|--------|-------------|
| AI-Based Quality Control | 2, 3 | API-01, UI-01–UI-03, ML-01 |
| Predictive Quality Analytics | 1 | ML-01, ML-02 |
| Production Data Processing | 1 | DATA-01, DATA-03 |
| Smart Manufacturing Workflow | 3 | WF-02, WF-01 |
| Simulated IoT Integration | 1, 3 | DATA-02, WF-01 |
| Analytics Dashboard | 3 | UI-04–UI-07 |
| Data Storage & Model Deployment | 1, 2 | ML-04, API-04 |
| Recommendation Engine | 2, 3 | WF-03, UI-08 |

All 8 CV bullet points covered ✓
