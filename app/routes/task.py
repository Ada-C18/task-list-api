from flask import Blueprint

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")