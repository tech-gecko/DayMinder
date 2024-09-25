from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os


# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config.from_object('app.config.Config')

    # SMTP email settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = ('DayMinder', os.getenv('GMAIL_USER'))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import and register blueprints for users, tasks, and reminders
    from .user_routes import user_bp
    from .task_routes import task_bp
    from .reminder_routes import reminder_bp

    app.register_blueprint(user_bp, url_prefix='/api')  # Prefix all user routes with /api
    app.register_blueprint(task_bp, url_prefix='/api')  # Prefix all task routes with /api
    app.register_blueprint(reminder_bp, url_prefix='/api')  # Prefix all reminder routes with /api

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Task, Reminder

    return app
