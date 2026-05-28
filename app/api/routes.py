import math
import sqlite3
from datetime import date

from flask import current_app, request, jsonify
from flask.views import MethodView

from app.api import api_bp
from app.api.errors import error_response
from app.api.validators import validate_batch_input
from app.db import get_db
from app.ml.predict import predict_batch, get_feature_importance, generate_recommendation


class PredictAPI(MethodView):
    def post(self):
        data = request.get_json()
        cleaned, error = validate_batch_input(data)
        if error:
            return error_response(error)

        try:
            pipeline = current_app.config['MODEL']
            result = predict_batch(pipeline, cleaned)
        except Exception as e:
            return error_response(f'Prediction failed: {str(e)}', 500)

        recommendation = generate_recommendation(result['grade'], cleaned)

        db = get_db()
        max_id = db.execute('SELECT MAX(id) FROM batches').fetchone()[0]
        next_num = (max_id or 0) + 1
        batch_id = f'B-{date.today().year}-{next_num:03d}'
        production_date = date.today().isoformat()

        try:
            db.execute(
                'INSERT INTO batches (batch_id, production_date, temperature, moisture, '
                'ph, color_score, cooking_time, supplier_origin, dryness_level, visual_inspection) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    batch_id, production_date,
                    cleaned['temperature'], cleaned['moisture'], cleaned['pH'],
                    cleaned['color_score'], cleaned['cooking_time'],
                    cleaned['supplier_origin'], cleaned['dryness_level'],
                    cleaned['visual_inspection'],
                )
            )
            db.execute(
                'INSERT INTO predictions (batch_id, predicted_grade, confidence, recommendation) '
                'VALUES (?, ?, ?, ?)',
                (batch_id, result['grade'], round(result['confidence'], 4), recommendation)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return error_response('Batch ID already exists', 409)

        return jsonify({
            'grade': result['grade'],
            'confidence': round(result['confidence'], 4),
            'recommendation': recommendation,
            'batch_id': batch_id,
        })


class BatchAPI(MethodView):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)
        if page < 1:
            page = 1

        db = get_db()
        total = db.execute('SELECT COUNT(*) FROM batches').fetchone()[0]
        pages = max(1, math.ceil(total / per_page))
        offset = (page - 1) * per_page

        rows = db.execute(
            'SELECT * FROM batches ORDER BY created_at DESC LIMIT ? OFFSET ?',
            (per_page, offset)
        ).fetchall()

        batches = [dict(row) for row in rows]

        return jsonify({
            'batches': batches,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pages,
        })

    def post(self):
        data = request.get_json()
        cleaned, error = validate_batch_input(data)
        if error:
            return error_response(error)

        batch_id = data.get('batch_id')
        if not batch_id:
            db = get_db()
            max_id = db.execute('SELECT MAX(id) FROM batches').fetchone()[0]
            next_num = (max_id or 0) + 1
            batch_id = f'B-{date.today().year}-{next_num:03d}'

        production_date = data.get('production_date', date.today().isoformat())

        try:
            db = get_db()
            db.execute(
                'INSERT INTO batches (batch_id, production_date, temperature, moisture, '
                'ph, color_score, cooking_time, supplier_origin, dryness_level, visual_inspection) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    batch_id, production_date,
                    cleaned['temperature'], cleaned['moisture'], cleaned['pH'],
                    cleaned['color_score'], cleaned['cooking_time'],
                    cleaned['supplier_origin'], cleaned['dryness_level'],
                    cleaned['visual_inspection'],
                )
            )
            db.commit()
        except sqlite3.IntegrityError:
            return error_response('Batch ID already exists', 409)

        row = db.execute(
            'SELECT * FROM batches WHERE batch_id = ?', (batch_id,)
        ).fetchone()

        return jsonify(dict(row)), 201


class FeatureImportanceAPI(MethodView):
    def get(self):
        try:
            pipeline = current_app.config['MODEL']
            features = get_feature_importance(pipeline)
        except Exception as e:
            return error_response(f'Failed to load feature importance: {str(e)}', 500)

        return jsonify({'features': features})


class StatsAPI(MethodView):
    def get(self):
        db = get_db()
        total = db.execute('SELECT COUNT(*) FROM batches').fetchone()[0]

        if total == 0:
            return jsonify({
                'total_batches': 0,
                'grade_distribution': {
                    'Grade A': {'count': 0, 'percentage': 0.0},
                    'Grade B': {'count': 0, 'percentage': 0.0},
                    'Reject': {'count': 0, 'percentage': 0.0},
                },
                'reject_rate': 0.0,
                'reject_trend': [],
            })

        grades = db.execute(
            'SELECT predicted_grade, COUNT(*) as cnt FROM predictions GROUP BY predicted_grade'
        ).fetchall()

        grade_counts = {}
        for row in grades:
            grade_counts[row['predicted_grade']] = row['cnt']

        grade_a = grade_counts.get('Grade A', 0)
        grade_b = grade_counts.get('Grade B', 0)
        reject = grade_counts.get('Reject', 0)

        grade_distribution = {
            'Grade A': {
                'count': grade_a,
                'percentage': round((grade_a / total) * 100, 1),
            },
            'Grade B': {
                'count': grade_b,
                'percentage': round((grade_b / total) * 100, 1),
            },
            'Reject': {
                'count': reject,
                'percentage': round((reject / total) * 100, 1),
            },
        }

        reject_rate = round((reject / total) * 100, 1)

        trend = db.execute(
            '''SELECT DATE(created_at) as date,
                      COUNT(*) as total,
                      SUM(CASE WHEN predicted_grade = 'Reject' THEN 1 ELSE 0 END) as rejects
               FROM predictions
               GROUP BY DATE(created_at)
               ORDER BY date DESC
               LIMIT 7'''
        ).fetchall()

        reject_trend = []
        for row in reversed(trend):
            day_total = row['total']
            day_rejects = row['rejects']
            rate = round((day_rejects / day_total) * 100, 1) if day_total > 0 else 0.0
            reject_trend.append({
                'date': row['date'],
                'reject_rate': rate,
            })

        return jsonify({
            'total_batches': total,
            'grade_distribution': grade_distribution,
            'reject_rate': reject_rate,
            'reject_trend': reject_trend,
        })


api_bp.add_url_rule('/predict', view_func=PredictAPI.as_view('predict'))
api_bp.add_url_rule('/stats', view_func=StatsAPI.as_view('stats'))
api_bp.add_url_rule('/batches', view_func=BatchAPI.as_view('batches'))
api_bp.add_url_rule('/feature-importance', view_func=FeatureImportanceAPI.as_view('feature_importance'))
