from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/task")
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    pass