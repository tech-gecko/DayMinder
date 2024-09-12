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

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Task, Reminder

    # Create all tables that don't exist within the app context
    with app.app_context():
        db.create_all()

    return app
