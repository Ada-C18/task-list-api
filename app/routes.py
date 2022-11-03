from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    pass

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    pass

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task():
    pass

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task():
    pass

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task():
    pass