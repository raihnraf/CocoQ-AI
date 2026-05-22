# CocoQ-AI

## What This Is

An AI-powered quality prediction system for organic coconut sugar manufacturing. A Flask web dashboard that predicts whether a production batch is Grade A, Grade B, or Reject based on production parameters like temperature, moisture, pH, color score, and supplier origin. Built as a demo/portfolio project showcasing end-to-end ML pipeline: data processing, model training, prediction API, and interactive dashboard.

## Core Value

A polished, professional demo that demonstrates the ability to build a complete AI-driven quality control system — from data preprocessing and model training to a user-facing dashboard with real-time predictions and analytics.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Train a classification model (Random Forest) to predict batch quality grade
- [ ] Flask backend with REST API for predictions and batch management
- [ ] Dashboard with batch input form and prediction display
- [ ] Simulated sensor data generator for demo purposes
- [ ] Chart.js visualizations: grade distribution, reject rate, quality trends
- [ ] SQLite database for batch records and prediction history
- [ ] Feature importance display showing which factors most affect quality
- [ ] Rule-based recommendation engine based on predicted grade
- [ ] Model persistence with Joblib for deployment
- [ ] Responsive, mobile-friendly dashboard UI

### Out of Scope

- Real IoT hardware integration — simulated data is sufficient for demo
- Production-grade deployment — this is a portfolio/demo project
- User authentication system — not needed for demo scope
- Multi-tenant or multi-factory support — single factory context

## Context

This project is built as a portfolio piece for a software developer role requiring Flask, Scikit-Learn, and full-stack development skills. The job listing emphasizes Angular, PHP Slim 4, REST APIs, MySQL/PostgreSQL, and familiarity with Python/Flask and ML libraries (PyTorch, TensorFlow, Scikit-Learn). This project demonstrates the Python/Flask + ML side of that stack.

The project should produce CV-ready bullet points covering: predictive quality analytics, production data processing, smart manufacturing workflow, simulated IoT integration, analytics dashboard, data storage & model deployment, and recommendation engine.

## Constraints

- **Tech stack**: Python, Flask, Scikit-Learn, Pandas, NumPy, SQLite, Chart.js, Joblib — as specified
- **Timeline**: Build quickly for demo purposes — keep it simple but polished
- **Data**: Dummy/simulated dataset — no real production data required
- **Complexity**: Professional-looking but not overly complex ("tidak perlu terlalu ribet")

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Flask over PHP Slim 4 | Job requires familiarity with Flask; Python ecosystem better for ML integration | ✓ Good |
| SQLite over MySQL/PostgreSQL | Simpler setup for demo; job only requires familiarity with relational DBs | ✓ Good |
| Random Forest classifier | Good balance of accuracy, interpretability (feature importance), and simplicity | — Pending |
| Simulated IoT data | No real sensors needed; demonstrates IoT-readiness concept | ✓ Good |
| Chart.js over heavy charting libs | Lightweight, works well with Flask templates | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-22 after initialization*
