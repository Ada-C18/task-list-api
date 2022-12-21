from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SLACK_API_TOKEN"] = os.environ.get("SLACK_API_TOKEN")

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://gkmrmwhlxqlbwt:b869a91ef48a1d53454580e30292695dc000cfade593735f944559e7f23b6929@ec2-44-205-177-160.compute-1.amazonaws.com:5432/dcn4qe59fncf65"
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
    from .routes import tasks
    app.register_blueprint(tasks.bp)

    from .routes import goals
    app.register_blueprint(goals.bp)

    # addition for React task-list-front-end
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)

    return app
