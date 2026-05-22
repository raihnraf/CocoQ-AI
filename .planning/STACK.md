# Technology Stack

## Core Versions (Latest as of 2026-05)

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.12+ | Runtime |
| Flask | 3.1.x | Web framework + REST API |
| Scikit-Learn | 1.7.x | ML classification model |
| Pandas | 2.2.x | Data processing |
| NumPy | 2.2.x | Numerical operations |
| Joblib | 1.4.x | Model persistence |
| Chart.js | 4.4.x | Dashboard visualizations |
| SQLite | 3.45+ (built-in) | Data storage |

## Flask Application Structure

Following Flask official tutorial pattern:

```
cocoq-ai/
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Dashboard pages (Blueprint: main)
│   │   └── api.py           # REST API endpoints (Blueprint: api)
│   ├── models/
│   │   ├── __init__.py
│   │   └── batch.py         # SQLite batch model
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── predict.py       # Load model, run predictions
│   │   └── generate_data.py # Simulated sensor data
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── predict.html
│   │   └── history.html
│   └── static/
│       ├── css/style.css
│       └── js/charts.js     # Chart.js initialization
├── data/
│   └── coconut_sugar_batches.csv
├── models/
│   └── quality_model.pkl    # Trained model (Joblib)
├── train_model.py           # Standalone training script
├── requirements.txt
├── pyproject.toml           # Modern Python packaging
├── database.db              # SQLite (gitignored)
└── tests/
    ├── conftest.py
    ├── test_model.py
    ├── test_api.py
    └── test_routes.py
```

## Key Design Decisions

- **Application Factory Pattern** — `create_app()` for testability and config flexibility
- **Blueprints** — Separate `main` (pages) and `api` (REST endpoints) blueprints
- **MethodView** — REST API uses Flask MethodView class for clean HTTP method mapping
- **Scikit-Learn Pipeline** — `make_pipeline()` for preprocessing + model to prevent data leakage
- **Joblib with protocol=5** — Efficient serialization for NumPy arrays in model
- **Chart.js 4.x** — Responsive charts with `responsive: true`, `maintainAspectRatio: true`
- **Chart Container Pattern** — `<div style="position:relative">` wrapper for proper resizing
- **SQLite with `sqlite3` stdlib** — No external ORM needed for demo scope
- **pyproject.toml** — Modern Python packaging over setup.py

## Not Used (and why)

- **SQLAlchemy** — Overkill for demo; SQLite stdlib sufficient
- **Flask-RESTful / Flask-RESTX** — MethodView + Blueprint is simpler for this scope
- **PyTorch / TensorFlow** — Random Forest via Scikit-Learn is more interpretable for this use case
- **XGBoost** — Adds dependency complexity; Random Forest achieves similar results for demo
- **Gunicorn / WSGI server** — Demo runs with Flask dev server; production deployment out of scope
