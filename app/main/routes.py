from flask import render_template

from app.main import main_bp


@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')


@main_bp.route('/predict')
def predict_page():
    return render_template('predict.html')


@main_bp.route('/history')
def history_page():
    return render_template('history.html')
