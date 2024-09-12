from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config.from_object('app.config.Config')

    # Initialize the database with the app
    db.init_app(app)

    # Bind Migrate to the app and db
    migrate.init_app(app, db)

    # Register blueprints (api routes)
    #from .routes import api
    #app.register_blueprint(api)

    return app
