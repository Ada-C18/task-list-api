from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import requests


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app

def slack_bot_message(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get('API_KEY')

    query_params = {
        "channel": "task-notifications",
        "text": message
    }

    requests.post(PATH, params=query_params, headers={"Authorization": SLACK_API_KEY})
