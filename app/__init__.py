from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # ✅ Import Flask-Migrate
from .models import db  # Ensure models are correctly imported
from .routes import configure_routes  # ✅ Import the configured routes
import os  # ✅ Import os to handle environment variables

migrate = Migrate()  # ✅ Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)

    # ✅ Database Configuration (Supports both local & production)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///hardware_app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Apply CORS (Allow frontend domain)
    CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL", "*")}})

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Attach Flask-Migrate to app

    with app.app_context():
        db.create_all()

    # ✅ Attach Routes
    configure_routes(app)

    return app
