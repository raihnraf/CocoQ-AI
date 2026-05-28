import os
import sys

from flask import Flask

from app.db import init_app as init_db_app
from app.ml.predict import load_model


def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['MODEL_PATH'] = os.path.join(
        app.root_path, '..', 'models', 'quality_model.pkl'
    )
    app.config['DATABASE'] = os.path.join(
        app.root_path, '..', 'database.db'
    )

    if config:
        app.config.update(config)

    try:
        app.config['MODEL'] = load_model(app.config['MODEL_PATH'])
    except FileNotFoundError:
        print(
            f'ERROR: Model file not found at {app.config["MODEL_PATH"]}. '
            'Run train_model.py first to generate the model.',
            file=sys.stderr,
        )
        sys.exit(1)

    init_db_app(app)

    from app.api import api_bp
    from app.main import main_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
