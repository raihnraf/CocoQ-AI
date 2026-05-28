import sqlite3
from flask import g, current_app


def get_db():
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE', 'database.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    db_path = app.config.get('DATABASE', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT UNIQUE NOT NULL,
            production_date TEXT,
            temperature REAL NOT NULL,
            moisture REAL NOT NULL,
            ph REAL NOT NULL,
            color_score REAL NOT NULL,
            cooking_time REAL NOT NULL,
            supplier_origin TEXT NOT NULL,
            dryness_level INTEGER NOT NULL,
            visual_inspection TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT NOT NULL,
            predicted_grade TEXT NOT NULL,
            confidence REAL NOT NULL,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (batch_id) REFERENCES batches(batch_id)
        );
    ''')
    conn.commit()
    conn.close()


def init_app(app):
    init_db(app)
    app.teardown_appcontext(close_db)
