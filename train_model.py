"""Train Random Forest classifier for coconut sugar quality prediction.

Uses scikit-learn Pipeline to prevent data leakage:
  StandardScaler → RandomForestClassifier(n_estimators=100)

Saves model with Joblib (protocol=5) and exports feature importance as JSON.
"""

import json
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def train_and_save_model(data_path="data/coconut_sugar_batches.csv", model_path="models/quality_model.pkl"):
    """Train and save a Random Forest classification model.

    Args:
        data_path: Path to the CSV dataset
        model_path: Path to save the trained model

    Returns:
        tuple: (pipeline, accuracy, feature_importance_dict)
    """
    # Load data
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records with columns: {list(df.columns)}")

    # Feature engineering
    # Drop non-feature columns
    df = df.drop(columns=['batch_id', 'production_date'])

    # Encode categorical features
    le_supplier = LabelEncoder()
    df['supplier_origin_encoded'] = le_supplier.fit_transform(df['supplier_origin'])

    # Ordinal mapping for visual inspection
    vi_map = {'poor': 1, 'fair': 2, 'good': 3, 'excellent': 4}
    df['visual_inspection_encoded'] = df['visual_inspection'].map(vi_map)

    # Encode target
    le_grade = LabelEncoder()
    y = le_grade.fit_transform(df['grade'])
    grade_classes = le_grade.classes_
    print(f"Grade classes: {dict(zip(grade_classes, range(len(grade_classes))))}")

    # Feature columns
    feature_cols = ['temperature', 'moisture', 'pH', 'color_score', 'cooking_time',
                    'supplier_origin_encoded', 'dryness_level', 'visual_inspection_encoded']
    X = df[feature_cols]

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {len(X_train)} samples, Test: {len(X_test)} samples")

    # Build Pipeline
    pipeline = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )

    # Train
    print("\nTraining Random Forest classifier...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=grade_classes))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path, protocol=5)
    print(f"\nModel saved to {model_path}")

    # Extract feature importance
    rf_model = pipeline.named_steps['randomforestclassifier']
    importances = rf_model.feature_importances_

    feature_importance = {
        'features': feature_cols,
        'importance': importances.tolist()
    }

    importance_path = os.path.join(os.path.dirname(model_path), 'feature_importance.json')
    with open(importance_path, 'w') as f:
        json.dump(feature_importance, f, indent=2)
    print(f"Feature importance saved to {importance_path}")

    # Print top features
    top_indices = np.argsort(importances)[::-1]
    print("\nTop features by importance:")
    for i in top_indices[:5]:
        print(f"  {feature_cols[i]}: {importances[i]:.4f}")

    return pipeline, accuracy, feature_importance


if __name__ == "__main__":
    train_and_save_model()
