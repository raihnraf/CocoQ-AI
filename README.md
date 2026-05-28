# CocoQ-AI

**AI-Powered Quality Prediction System for Organic Coconut Sugar Manufacturing**

A Flask web dashboard that uses machine learning to predict whether a production batch of organic coconut sugar is **Grade A**, **Grade B**, or **Reject** based on 8 production parameters. Built as an end-to-end ML pipeline demo showcasing data processing, model training, prediction API, and interactive dashboard.

---

## Table of Contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [ML Pipeline](#ml-pipeline)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Input Parameters](#input-parameters)
- [Validation Rules](#validation-rules)
- [Configuration](#configuration)

---

## Screenshots

> _Coming soon — dashboard, prediction form, and history views_

---

## Features

### Core Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Production Dashboard** | Summary stats cards showing total batches, grade percentages, and reject rate |
| 2 | **Batch Prediction** | Manual input form for 8 production parameters → instant ML prediction |
| 3 | **Grade Classification** | Random Forest classifies each batch as Grade A, Grade B, or Reject |
| 4 | **Confidence Score** | Displays prediction confidence as percentage (e.g., _"Grade A with 91.2% confidence"_) |
| 5 | **Prediction History** | Paginated table of all predictions with grade and batch ID search/filter |
| 6 | **Grade Distribution Chart** | Color-coded doughnut chart (green/yellow/red) showing overall quality spread |
| 7 | **Reject Rate Trend** | 7-day line chart tracking the reject percentage over time |
| 8 | **IoT Simulator** | One-click _"Generate & Predict"_ button that creates realistic random batch data and runs prediction |
| 9 | **Feature Importance** | Horizontal bar chart ranking which production parameters influence predictions most |
| 10 | **Smart Recommendations** | Context-aware advice based on parameters (e.g., _"Moisture too high — increase drying time"_) |

### Data Pipeline Features

- **Synthetic data generator** — creates 200 realistic batch records with domain-knowledge distributions
- **Stratified train/test split** — prevents class imbalance in evaluation
- **Feature scaling** — StandardScaler inside the pipeline to prevent data leakage
- **Model persistence** — trained model saved via Joblib, ready for production inference
- **Feature importance export** — saved as JSON alongside the model

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Flask 3.1+ | Web framework with Blueprint architecture |
| **ML Engine** | Scikit-Learn 1.4+ | Random Forest classifier via Pipeline |
| **Data Processing** | Pandas 2.0+, NumPy 1.26+ | Data loading, manipulation, and feature engineering |
| **Database** | SQLite | Lightweight relational storage for batches and predictions |
| **Model Serialization** | Joblib 1.3+ | Save and load trained ML pipeline |
| **Frontend** | HTML5, CSS3, Vanilla JS | Responsive dashboard with no framework overhead |
| **Charts** | Chart.js | Interactive doughnut, line, and bar charts |
| **Language** | Python 3.10+ | Core application and ML logic |

---

## Project Structure

```
IMC/
├── README.md
├── AGENTS.md                           # Project documentation (GSD format)
├── plan.md                             # Original project proposal/brainstorm
├── requirements.txt                    # Python dependencies
├── train_model.py                      # Trains Random Forest, saves model + feature importance
├── database.db                         # SQLite database (auto-created on first run)
│
├── data/
│   └── coconut_sugar_batches.csv       # Synthetic dataset (200 batches)
│
├── models/
│   ├── quality_model.pkl               # Trained Random Forest pipeline (StandardScaler + RF)
│   └── feature_importance.json         # Exported feature importance scores
│
└── app/
    ├── __init__.py                     # Flask app factory (create_app)
    ├── db.py                           # SQLite init, connection management, schema
    │
    ├── main/                           # Frontend routes (HTML views)
    │   ├── __init__.py                 # Blueprint: main
    │   └── routes.py                   # /, /predict, /history
    │
    ├── api/                            # REST API Blueprint (/api/*)
    │   ├── __init__.py                 # Blueprint: api
    │   ├── routes.py                   # PredictAPI, BatchAPI, StatsAPI, FeatureImportanceAPI
    │   ├── validators.py              # Input validation (ranges, enums, required fields)
    │   └── errors.py                   # Error response helper
    │
    ├── ml/                             # Machine Learning utilities
    │   ├── predict.py                  # predict_batch(), get_feature_importance(), generate_recommendation()
    │   └── generate_data.py            # Synthetic data generator with domain-knowledge distributions
    │
    ├── templates/                      # Jinja2 templates
    │   ├── base.html                   # Layout shell: navbar, footer, Chart.js CDN
    │   ├── dashboard.html              # Stats cards, doughnut chart, line chart, IoT simulator
    │   ├── predict.html                # Batch prediction form + result card
    │   └── history.html                # Paginated table with grade/search filters
    │
    └── static/
        ├── css/
        │   └── style.css               # Custom design system (CSS variables, responsive)
        └── js/
            ├── charts.js               # Chart.js rendering (doughnut, line, bar)
            └── predict.js              # Client-side form validation + API submission
```

---

## How It Works

### Architecture

```
User Browser
    │
    ├── GET /              → main blueprint → dashboard.html
    │                          (loads /api/stats → renders charts)
    │
    ├── GET /predict       → main blueprint → predict.html
    │                          (form submits → POST /api/predict)
    │
    ├── GET /history       → main blueprint → history.html
    │                          (paginated via GET /api/batches)
    │
    └── REST API (/api/*)
        ├── POST /api/predict           → input validation
        │                                  → feature encoding
        │                                  → Random Forest prediction
        │                                  → recommendation generation
        │                                  → SQLite insert (batches + predictions)
        │                                  → JSON response
        │
        ├── GET  /api/stats             → SQLite aggregation
        │                                  → grade distribution
        │                                  → reject rate
        │                                  → 7-day trend
        │
        ├── GET  /api/batches           → paginated batch list
        │
        ├── POST /api/batches           → create batch manually
        │
        └── GET  /api/feature-importance → JSON importance scores
```

### Prediction Flow (Step-by-Step)

1. **User submits** a form with 8 production parameters (or clicks "Generate & Predict")
2. **Client-side validation** checks all values are within valid ranges
3. **Server-side validation** re-checks and sanitizes inputs (`validators.py`)
4. **Feature encoding** — categorical fields (supplier origin, visual inspection) are mapped to numeric values
5. **Pipeline inference** — StandardScaler normalizes features, Random Forest predicts class + probabilities
6. **Recommendation** generated based on grade + specific parameter thresholds
7. **Database write** — batch record inserted into `batches` table, prediction into `predictions` table
8. **JSON response** returned with grade, confidence, recommendation, and batch ID

---

## ML Pipeline

### Model

- **Type**: `Pipeline(StandardScaler() → RandomForestClassifier(n_estimators=100, random_state=42))`
- **Input features**: 8 (temperature, moisture, pH, color score, cooking time, supplier origin encoded, dryness level, visual inspection encoded)
- **Output classes**: 3 (Grade A, Grade B, Reject)

### Training Data

- **Source**: 200 synthetically generated batch records
- **Distribution**: ~40% Grade A, ~35% Grade B, ~25% Reject
- **Key design**: Temperature, moisture, and pH are engineered as the most discriminative features (highest feature importance). Color score and visual inspection are intentionally noisier to reflect real-world measurement uncertainty.

### Data Leakage Prevention

- StandardScaler is **inside** the Pipeline — fit only on training data, transform on test data
- Stratified `train_test_split` (80/20) maintains class proportions
- Categorical features are label-encoded consistently across train and test

### Feature Importance

Loaded from `models/feature_importance.json`. The top features typically rank as:

1. **Moisture** — strongest predictor; clear separation between grades
2. **Temperature** — optimal range is narrow for Grade A
3. **pH** — both too acidic and too alkaline push toward Reject
4. **Cooking Time** — moderate influence
5. **Color Score** — weaker predictor by design (measurement noise)
6. **Dryness Level** — ordinal, weaker signal
7. **Supplier Origin** — one-hot encoded; minor variation
8. **Visual Inspection** — intentionally weak correlation

---

## API Endpoints

### POST `/api/predict`

Predict quality grade for a production batch.

**Request Body** (JSON):

```json
{
  "temperature": 115.0,
  "moisture": 2.3,
  "pH": 6.1,
  "color_score": 78.5,
  "cooking_time": 90,
  "dryness_level": 4,
  "supplier_origin": "Central Java",
  "visual_inspection": "good"
}
```

**Response** (200):

```json
{
  "batch_id": "B-2026-012",
  "grade": "Grade A",
  "confidence": 0.8912,
  "recommendation": "Excellent quality — suitable for export-grade packaging."
}
```

**Response** (400):

```json
{
  "error": "Invalid value for temperature: must be between 90.0 and 140.0"
}
```

---

### GET `/api/stats`

Get aggregate statistics for the dashboard.

**Response** (200):

```json
{
  "total_batches": 45,
  "grade_distribution": {
    "Grade A": { "count": 20, "percentage": 44.4 },
    "Grade B": { "count": 15, "percentage": 33.3 },
    "Reject": { "count": 10, "percentage": 22.2 }
  },
  "reject_rate": 22.2,
  "reject_trend": [
    { "date": "2026-05-16", "reject_rate": 25.0 },
    { "date": "2026-05-17", "reject_rate": 20.0 },
    { "date": "2026-05-18", "reject_rate": 22.2 }
  ]
}
```

---

### GET `/api/batches`

Get paginated list of batches.

**Query Parameters**:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (max 100) |

**Response** (200):

```json
{
  "batches": [
    {
      "id": 45,
      "batch_id": "B-2026-045",
      "production_date": "2026-05-22",
      "temperature": 115.0,
      "moisture": 2.3,
      "pH": 6.1,
      "color_score": 78.5,
      "cooking_time": 90,
      "supplier_origin": "Central Java",
      "dryness_level": 4,
      "visual_inspection": "good",
      "created_at": "2026-05-22 14:30:00"
    }
  ],
  "total": 45,
  "page": 1,
  "per_page": 20,
  "pages": 3
}
```

---

### POST `/api/batches`

Create a batch record manually (without prediction).

**Request Body** (JSON): Same as `/api/predict` input.

**Response** (201): Created batch object.

---

### GET `/api/feature-importance`

Get feature importance scores for the model.

**Response** (200):

```json
{
  "features": [
    { "feature": "moisture", "importance": 0.3215 },
    { "feature": "temperature", "importance": 0.2487 },
    { "feature": "pH", "importance": 0.1832 },
    { "feature": "cooking_time", "importance": 0.0914 },
    { "feature": "color_score", "importance": 0.0651 },
    { "feature": "dryness_level", "importance": 0.0406 },
    { "feature": "supplier_origin_encoded", "importance": 0.0283 },
    { "feature": "visual_inspection_encoded", "importance": 0.0212 }
  ]
}
```

---

## Data Model

### SQLite Schema

#### `batches`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Auto-incremented row ID |
| `batch_id` | TEXT | UNIQUE NOT NULL | Human-readable ID (e.g., `B-2026-012`) |
| `production_date` | TEXT | | ISO date string (`YYYY-MM-DD`) |
| `temperature` | REAL | NOT NULL | Cooking temperature in °C |
| `moisture` | REAL | NOT NULL | Moisture percentage |
| `pH` | REAL | NOT NULL | pH level |
| `color_score` | REAL | NOT NULL | Visual color rating (0-100) |
| `cooking_time` | REAL | NOT NULL | Cooking duration in minutes |
| `supplier_origin` | TEXT | NOT NULL | Supplier region |
| `dryness_level` | INTEGER | NOT NULL | Dryness rating (1-5) |
| `visual_inspection` | TEXT | NOT NULL | Visual inspection result |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

#### `predictions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Auto-incremented row ID |
| `batch_id` | TEXT | NOT NULL, FK → batches | Associated batch |
| `predicted_grade` | TEXT | NOT NULL | Grade A / Grade B / Reject |
| `confidence` | REAL | NOT NULL | Prediction confidence (0-1) |
| `recommendation` | TEXT | | Quality recommendation text |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Prediction timestamp |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd IMC

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate synthetic dataset (produces data/coconut_sugar_batches.csv)
python -m app.ml.generate_data

# 5. Train the model (produces models/quality_model.pkl and models/feature_importance.json)
python train_model.py

# 6. Run the Flask application
flask --app app run --debug --port 5000
```

The app will be available at **http://localhost:5000**.

### Quick Start (if data and model already exist)

If `data/coconut_sugar_batches.csv`, `models/quality_model.pkl`, and `models/feature_importance.json` are already present:

```bash
pip install -r requirements.txt
flask --app app run --debug --port 5000
```

---

## Testing the App — Step by Step

This walks through every feature so you can verify everything works.

### Step 1: Start the Server

```bash
cd IMC
source venv/bin/activate   # if using virtualenv
flask --app app run --debug --port 5000
```

Open **http://localhost:5000** in your browser. You should see the Dashboard page.

---

### Step 2: Verify the Dashboard

1. The top row shows **4 stat cards**: Total Batches, Grade A %, Grade B %, Reject Rate
2. Below that, a **doughnut chart** shows the grade distribution (green/yellow/red)
3. A **line chart** shows the 7-day reject rate trend
4. A **horizontal bar chart** shows feature importance (which parameters influence predictions most)
5. If the database is empty, all stats show zeros — that's normal. Predict a few batches first.

---

### Step 3: Test the API Directly (curl)

Before using the form, verify the API works:

```bash
# Check stats (may be empty if no predictions yet)
curl -s http://localhost:5000/api/stats | python -m json.tool

# Predict a Grade A batch
curl -s -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 115.0,
    "moisture": 2.2,
    "pH": 6.0,
    "color_score": 80,
    "cooking_time": 90,
    "dryness_level": 4,
    "supplier_origin": "Central Java",
    "visual_inspection": "good"
  }' | python -m json.tool

# Expected output:
# {
#   "batch_id": "B-2026-XXX",
#   "grade": "Grade A",
#   "confidence": 0.91,
#   "recommendation": "Excellent quality — suitable for export-grade packaging."
# }

# Predict a Reject batch (extreme values)
curl -s -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 130.0,
    "moisture": 5.5,
    "pH": 3.5,
    "color_score": 35,
    "cooking_time": 130,
    "dryness_level": 1,
    "supplier_origin": "Yogyakarta",
    "visual_inspection": "poor"
  }' | python -m json.tool

# Expected output: grade "Reject" with advice about moisture, pH, and temperature

# Check batch history
curl -s http://localhost:5000/api/batches?page=1 | python -m json.tool

# Check feature importance
curl -s http://localhost:5000/api/feature-importance | python -m json.tool
```

---

### Step 4: Test the Prediction Form

1. Go to **http://localhost:5000/predict**
2. Fill in the form with these values:

| Field | Value |
|-------|-------|
| Temperature | `115.0` |
| Moisture | `2.3` |
| pH | `6.1` |
| Color Score | `78` |
| Cooking Time | `90` |
| Dryness Level | `4` |
| Supplier Origin | `Central Java` |
| Visual Inspection | `good` |

3. Click **"Get Prediction"**
4. A result card appears below the form showing:
   - **Grade A** (in green)
   - Confidence percentage (e.g., `91.2%`)
   - Recommendation text

---

### Step 5: Test Client-Side Validation

Try submitting these invalid values to confirm the validation works:

| Test | Value | Expected Error |
|------|-------|---------------|
| Temperature too high | `145` | _"Temperature must be between 90 and 140"_ |
| Missing supplier | (leave blank) | _"Please select a valid supplier"_ |
| Invalid pH | `11` | _"pH must be between 2 and 9"_ |

The error should appear as a red banner at the top of the form.

---

### Step 6: Test the IoT Simulator

1. Go to **http://localhost:5000/** (Dashboard)
2. Find the **IoT Simulator** section (below the charts)
3. Click **"Generate Random Batch & Predict"**
4. The system will:
   - Generate realistic random production parameters
   - Run the prediction immediately
   - Show the result (grade + confidence + recommendation)

You can click it multiple times — each generates a different random batch.

---

### Step 7: Check the History Page

1. Go to **http://localhost:5000/history**
2. You should see all predictions you've made so far in a paginated table
3. Try the **grade filter** dropdown — filter to "Grade A" only, or "Reject"
4. Try the **batch ID search** — type part of a batch ID like `B-2026`
5. If you have more than 20 records, pagination links appear at the bottom

---

### Step 8: Test API Error Handling

```bash
# Missing required field
curl -s -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 115}' | python -m json.tool

# Expected: {"error": "Missing required field: moisture"}

# Invalid range
curl -s -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 150, "moisture": 3, "pH": 6,
    "color_score": 80, "cooking_time": 90,
    "dryness_level": 4, "supplier_origin": "Central Java",
    "visual_inspection": "good"
  }' | python -m json.tool

# Expected: {"error": "Invalid value for temperature: must be between 90.0 and 140.0"}
```

---

### Step 9: Regenerate Everything (Optional)

To start from a clean slate — regenerate data, retrain model, and clear database:

```bash
# Delete existing artifacts
rm -f database.db models/quality_model.pkl models/feature_importance.json data/coconut_sugar_batches.csv

# Regenerate
python -m app.ml.generate_data
python train_model.py

# Start fresh
flask --app app run --debug --port 5000
```

This is useful when you want a clean demo with zero predictions in the history.

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `ERROR: Model file not found` | Run `python train_model.py` first |
| Port 5000 already in use | Use a different port: `flask --app app run --debug --port 5001` |
| Empty charts on dashboard | Make some predictions first — charts show prediction data |
| `database is locked` | Kill any stale Flask processes: `pkill -f "flask --app app"` |

---

## Usage Guide

### Dashboard (`/`)

The landing page shows:
- **Stats cards**: Total batches, Grade A%, Grade B%, Reject Rate
- **Grade distribution doughnut chart**: Green (A), yellow (B), red (Reject)
- **Reject rate trend line chart**: Last 7 days
- **Feature importance bar chart**: Horizontal bars ranking the 8 parameters
- **IoT Simulator**: _"Generate Random Batch & Predict"_ button

### Predict a Batch (`/predict`)

1. Fill in all 8 production parameters manually
2. Click **"Get Prediction"**
3. Result card shows: predicted grade (color-coded), confidence percentage, and recommendation text
4. The batch and prediction are automatically saved to the database and appear on the History page

### Prediction History (`/history`)

- Paginated table of all batches sorted by most recent
- Search by batch ID
- Filter by grade (All / Grade A / Grade B / Reject)

### Using the IoT Simulator

On the Dashboard, click **"Generate Random Batch & Predict"**. The system will:
1. Generate realistic random production parameters
2. Fill them into the prediction form
3. Run the prediction
4. Show the result instantly

---

## Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Cooking temperature (°C) |
| `moisture` | float | Moisture content (%) |
| `pH` | float | pH level |
| `color_score` | float | Visual color rating (0-100) |
| `cooking_time` | float | Cooking duration (minutes) |
| `supplier_origin` | string | Supplier region |
| `dryness_level` | int | Dryness rating (1-5) |
| `visual_inspection` | string | Visual inspection result |

### Allowed Values

**supplier_origin**: `Central Java`, `East Java`, `West Java`, `Yogyakarta`, `Central Kalimantan`

**visual_inspection**: `poor`, `fair`, `good`, `excellent`

**dryness_level**: `1`, `2`, `3`, `4`, `5`

---

## Validation Rules

Validation happens on both client-side and server-side.

| Parameter | Min | Max | Type |
|-----------|-----|-----|------|
| `temperature` | 90.0 | 140.0 | float |
| `moisture` | 0.0 | 10.0 | float |
| `pH` | 2.0 | 9.0 | float |
| `color_score` | 0.0 | 100.0 | float |
| `cooking_time` | 30.0 | 150.0 | float |
| `dryness_level` | 1 | 5 | int |

`supplier_origin` must be one of the 5 allowed regions (case-insensitive, auto-titlecased).  
`visual_inspection` must be one of the 4 allowed values (case-insensitive, auto-lowercased).  
All 8 fields are required — missing fields return a 400 error.

---

## Configuration

Configuration is set in `app/__init__.py`'s `create_app()` factory:

| Config Key | Default | Description |
|------------|---------|-------------|
| `SECRET_KEY` | `'dev'` | Flask secret key |
| `MODEL_PATH` | `models/quality_model.pkl` | Path to trained model |
| `DATABASE` | `database.db` | SQLite database path |

The app will **fail to start** if the model file (`models/quality_model.pkl`) is not found. Run `python train_model.py` to generate it.
