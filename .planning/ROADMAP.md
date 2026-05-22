# ROADMAP: CocoQ-AI

**Created:** 2026-05-22
**Total Phases:** 3
**Total v1 Requirements:** 23
**Mode:** YOLO | Granularity: Coarse | Parallel: Yes

---

## Phase 1: ML Pipeline & Data Foundation

**Goal:** Train a working classification model and create the simulated dataset that powers the entire demo.

**Requirements:** ML-01, ML-02, ML-04, DATA-01, DATA-02, DATA-03

**Success Criteria:**
1. `train_model.py` runs and produces `models/quality_model.pkl` with >80% training accuracy
2. `data/coconut_sugar_batches.csv` contains 100+ realistic batch records with all required features
3. Simulated data generator produces new batches with realistic parameter distributions
4. Feature importance output shows temperature, moisture, and pH as top predictors

**Threat Model:**
- Unrealistic data distributions → model learns noise instead of patterns
- Overfitting on small dataset → model performs poorly on "new" data
- Mitigation: Use domain-knowledge-based rules to generate realistic data

---

## Phase 2: Flask API & Backend

**Goal:** Build the Flask backend with REST endpoints for predictions, batch management, and SQLite persistence.

**Requirements:** API-01, API-02, API-03, API-04, ML-03

**Success Criteria:**
1. `POST /api/predict` accepts batch parameters and returns grade prediction with confidence
2. `GET /api/batches` returns paginated batch history
3. `POST /api/batches` creates new batch record and stores in SQLite
4. `GET /api/feature-importance` returns model feature importance data
5. SQLite database `database.db` persists across server restarts

**Threat Model:**
- API input validation gaps → crashes on malformed requests
- Model loading failures → server errors if model file missing
- Mitigation: Validate all inputs, graceful error handling with JSON responses

---

## Phase 3: Dashboard & Analytics UI

**Goal:** Build the interactive dashboard with forms, charts, predictions, and recommendations — the visible demo.

**Requirements:** UI-01 through UI-09, WF-01, WF-02, WF-03

**Success Criteria:**
1. Dashboard homepage displays production summary (total batches, grade distribution, reject rate)
2. Batch input form validates and submits data, shows prediction result with confidence score
3. Chart.js renders grade distribution chart and reject rate trend chart
4. Prediction history table shows past predictions with filtering
5. Feature importance chart displays top factors affecting quality
6. Recommendation messages appear based on predicted grade and conditions
7. Simulated IoT button generates and processes new batch data
8. Layout is responsive and works on mobile viewport

**UI hint:** yes

**Threat Model:**
- Chart rendering failures → blank dashboard sections
- Form submission errors → poor demo experience
- Mitigation: Graceful fallbacks, loading states, error messages

---

## Coverage Validation

| Phase | Requirements | Count |
|-------|-------------|-------|
| Phase 1 | ML-01, ML-02, ML-04, DATA-01, DATA-02, DATA-03 | 6 |
| Phase 2 | API-01, API-02, API-03, API-04, ML-03 | 5 |
| Phase 3 | UI-01–UI-09, WF-01, WF-02, WF-03 | 12 |
| **Total** | | **23** |

All 23 v1 requirements mapped ✓
