import json
import os
import joblib
import numpy as np


SUPPLIER_ENCODING = {
    'Central Java': 0,
    'Central Kalimantan': 1,
    'East Java': 2,
    'West Java': 3,
    'Yogyakarta': 4,
}

VISUAL_INSPECTION_ENCODING = {
    'poor': 1,
    'fair': 2,
    'good': 3,
    'excellent': 4,
}

GRADE_CLASSES = ['Grade A', 'Grade B', 'Reject']

FEATURE_ORDER = [
    'temperature', 'moisture', 'pH', 'color_score', 'cooking_time',
    'supplier_origin_encoded', 'dryness_level', 'visual_inspection_encoded',
]


def load_model(model_path='models/quality_model.pkl'):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Run train_model.py first to generate the model."
        )
    return joblib.load(model_path)


def predict_batch(pipeline, input_dict):
    supplier_raw = input_dict['supplier_origin'].strip().title()
    supplier_encoded = SUPPLIER_ENCODING[supplier_raw]

    visual_raw = input_dict['visual_inspection'].strip().lower()
    visual_encoded = VISUAL_INSPECTION_ENCODING[visual_raw]

    feature_array = np.array([[
        float(input_dict['temperature']),
        float(input_dict['moisture']),
        float(input_dict['pH']),
        float(input_dict['color_score']),
        float(input_dict['cooking_time']),
        supplier_encoded,
        int(input_dict['dryness_level']),
        visual_encoded,
    ]])

    proba = pipeline.predict_proba(feature_array)[0]
    predicted_index = int(np.argmax(proba))
    grade = GRADE_CLASSES[predicted_index]
    confidence = float(proba[predicted_index])

    probabilities = {
        GRADE_CLASSES[i]: float(proba[i])
        for i in range(len(GRADE_CLASSES))
    }

    return {
        'grade': grade,
        'confidence': confidence,
        'probabilities': probabilities,
    }


def get_feature_importance(pipeline, importance_path='models/feature_importance.json'):
    if os.path.exists(importance_path):
        with open(importance_path) as f:
            data = json.load(f)
        features = data['features']
        importances = data['importance']
    else:
        rf = pipeline.named_steps['randomforestclassifier']
        features = FEATURE_ORDER
        importances = rf.feature_importances_.tolist()

    pairs = [
        {'feature': features[i], 'importance': importances[i]}
        for i in range(len(features))
    ]
    pairs.sort(key=lambda x: x['importance'], reverse=True)
    return pairs


def generate_recommendation(grade, input_dict):
    if grade == 'Grade A':
        rec = 'Excellent quality — suitable for export-grade packaging.'
    elif grade == 'Grade B':
        rec = 'Good quality — suitable for domestic market. Consider adjusting moisture and pH for Grade A.'
    else:
        rec = 'Batch does not meet quality standards. Review production parameters.'

    moisture = float(input_dict.get('moisture', 3))
    ph = float(input_dict.get('pH', 5.5))
    temperature = float(input_dict.get('temperature', 115))

    advice = []
    if moisture > 4.0:
        advice.append('Moisture too high — increase drying time.')
    if moisture < 1.5:
        advice.append('Moisture too low — check for over-drying.')
    if ph < 4.5:
        advice.append('pH too acidic — review fermentation process.')
    if ph > 7.0:
        advice.append('pH too alkaline — check raw material quality.')
    if temperature < 105 or temperature > 125:
        advice.append('Temperature outside optimal range (105-125°C).')

    if advice:
        rec += ' ' + ' '.join(advice)

    return rec
