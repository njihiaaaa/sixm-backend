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

    # ✅ Load SECRET_KEY from environment variables (with a secure fallback)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(24).hex())

    # ✅ Improved SQLite database path (persistent across restarts)
    instance_path = os.path.join(os.getcwd(), "instance")
    os.makedirs(instance_path, exist_ok=True)  # Ensure the instance folder exists
    db_path = os.path.join(instance_path, "hardware_app.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Apply CORS
    CORS(app)

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()  # ✅ Ensure tables exist

    # ✅ Attach Routes
    configure_routes(app)

    return app
