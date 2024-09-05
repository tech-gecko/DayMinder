from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config.from_object('config.Config')

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints (api routes)
    from .routes import api
    app.register_blueprint(api)

    return app