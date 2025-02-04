import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db
from .routes import configure_routes

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Load SECRET_KEY from environment variables
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

    # ✅ Database Configuration (SQLite for Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/hardware_app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Apply CORS
    CORS(app)

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # ✅ Attach Routes
    configure_routes(app)

    return app
