from flask import Blueprint
from app import db
from app.models.task import Task


task_bp = Blueprint("Task_bp", __name__, url_prefix="tasks")

