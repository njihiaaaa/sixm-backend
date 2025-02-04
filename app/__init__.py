import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # ✅ Import Flask-Migrate
from .models import db  # ✅ Import models
from .routes import configure_routes  # ✅ Import the configured routes

migrate = Migrate()  # ✅ Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)

    # ✅ Database Configuration - Use PostgreSQL if available, else SQLite (local development)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///hardware_app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Apply CORS
    CORS(app)

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Attach Flask-Migrate to app

    with app.app_context():
        db.create_all()

    # ✅ Attach Routes
    configure_routes(app)

    return app
