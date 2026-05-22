# Requirements: CocoQ-AI

**Defined:** 2026-05-22
**Core Value:** A polished demo demonstrating end-to-end AI-driven quality control for coconut sugar manufacturing

## v1 Requirements

### Model & ML

- [ ] **ML-01**: Train Random Forest classifier to predict Grade A / Grade B / Reject
- [ ] **ML-02**: Model achieves reasonable accuracy on training data
- [ ] **ML-03**: Feature importance display showing which production factors affect quality most
- [ ] **ML-04**: Model saved to disk with Joblib for deployment

### Data

- [ ] **DATA-01**: Generate simulated production batch dataset (100+ records)
- [ ] **DATA-02**: Simulated sensor data generator with realistic parameter ranges
- [ ] **DATA-03**: Pandas preprocessing pipeline for feature engineering

### API & Backend

- [ ] **API-01**: Flask REST endpoint for single batch prediction
- [ ] **API-02**: Flask REST endpoint for batch history retrieval
- [ ] **API-03**: Flask REST endpoint to create new batch record
- [ ] **API-04**: SQLite database schema for batches and predictions

### Dashboard & UI

- [ ] **UI-01**: Dashboard homepage with production summary statistics
- [ ] **UI-02**: Batch input form with validation
- [ ] **UI-03**: Prediction result display with confidence score
- [ ] **UI-04**: Chart.js grade distribution pie/bar chart
- [ ] **UI-05**: Chart.js reject rate trend line chart
- [ ] **UI-06**: Prediction history table with filtering
- [ ] **UI-07**: Feature importance bar chart
- [ ] **UI-08**: Recommendation message based on predicted grade
- [ ] **UI-09**: Responsive, mobile-friendly layout

### Workflow

- [ ] **WF-01**: Simulated IoT data generation button on dashboard
- [ ] **WF-02**: Batch quality classification workflow (input → predict → display → store)
- [ ] **WF-03**: Rule-based recommendation engine (e.g., "Moisture too high — adjust drying time")

## v2 Requirements

(None — all scope is v1 for this demo project)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real IoT sensor integration | Demo project; simulated data sufficient |
| User authentication | Not needed for portfolio demo |
| Multi-tenant support | Single factory context |
| Production deployment | This is a demo, not production |
| Angular frontend | Flask templates sufficient for demo scope |
| PHP Slim 4 backend | Project focuses on Python/Flask + ML |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ML-01 | Phase 1 | Pending |
| ML-02 | Phase 1 | Pending |
| ML-03 | Phase 2 | Pending |
| ML-04 | Phase 1 | Pending |
| DATA-01 | Phase 1 | Pending |
| DATA-02 | Phase 1 | Pending |
| DATA-03 | Phase 1 | Pending |
| API-01 | Phase 2 | Pending |
| API-02 | Phase 2 | Pending |
| API-03 | Phase 2 | Pending |
| API-04 | Phase 2 | Pending |
| UI-01 | Phase 3 | Pending |
| UI-02 | Phase 3 | Pending |
| UI-03 | Phase 3 | Pending |
| UI-04 | Phase 3 | Pending |
| UI-05 | Phase 3 | Pending |
| UI-06 | Phase 3 | Pending |
| UI-07 | Phase 3 | Pending |
| UI-08 | Phase 3 | Pending |
| UI-09 | Phase 3 | Pending |
| WF-01 | Phase 3 | Pending |
| WF-02 | Phase 3 | Pending |
| WF-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-22*
*Last updated: 2026-05-22 after initial definition*
