from datetime import datetime
import requests
from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db
from app.models.goal import Goal
from sqlalchemy import desc
from sqlalchemy import asc

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify(details="Invalid data"), 400

        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify(task=new_task.to_json()), 201

    elif request.method == "GET":
        query = request.args.get("sort")
        if query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        else:
            tasks = Task.query.all()

        response_body = []
        for task in tasks:
            response_body.append(task.to_json())

        return jsonify(response_body), 200


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "GET":
        if task.goal_id:
            return jsonify(task=task.to_json_task()), 200
        else:
            return jsonify(task=task.to_json()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()
        return jsonify(task=task.to_json()), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify(details="Task 1 \"Go on my daily walk 🏞\" successfully deleted"), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def handle_task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return jsonify(task=task.to_json()), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def handle_task_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task=task.to_json()), 200