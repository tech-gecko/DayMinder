from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db = SQLAlchemy(app)

    # Import models
    from app.models import User, Task, Reminder

    # Create all tables that don't exist
    with app.app_context():
        db.create_all()

    return app
