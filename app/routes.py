from flask import Blueprint, jsonify, request, abort, make_response
from app import db, Key
from app.models.task import Task
from app.models.goal import Goal
import datetime
import requests


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# # helper function to structure request response json
def make_task_dict(task):
        task_dict = {"id": task.task_id,
        "title": task.title,
        "description": task.description}

        if not task.completed_at:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True
            # task_dict["completed_at"] = task.completed_at
        
        return task_dict


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))
    
    else:
        new_task = Task(
        title = request_body["title"],
        description = request_body["description"])

        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]

        db.session.add(new_task)
        db.session.commit()

        new_task_dict = {"task": new_task.make_task_dict()}
        return jsonify(new_task_dict), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    sort_param = request.args.get("sort")


    response = []
    for task in tasks:
        task_dict = task.make_task_dict()
        response.append(task_dict)
    
    if sort_param == "asc":
        response = sorted(response, key=lambda i:i['title'])
    if sort_param == "desc":
        response = sorted(response, key=lambda i:i['title'], reverse=True)

    return jsonify(response), 200


#helper function to validate that task ids are valid
def validate_id(task_id):
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Could not find task with id {task_id}"
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task


@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    selected_task = validate_id(task_id)
    task_dict = selected_task.make_task_dict()
    response_dict = {"task": task_dict}
    return response_dict, 200


@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task_with_new_vals(task_id):
    selected_task = validate_id(task_id)

    request_body = request.get_json()
    if "title" in request_body:
        selected_task.title = request_body["title"]
    if "description" in request_body:
        selected_task.description = request_body["description"]
    
    db.session.commit()
    
    task_dict = selected_task.make_task_dict()
    response_dict = {"task": task_dict}
    return response_dict, 200


@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    selected_task = validate_id(task_id)
    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete(task_id):

    selected_task = validate_id(task_id)

    selected_task.completed_at = datetime.date.today()

    db.session.commit()

    #Slack Patch Request
    slack_message = f"Someone just completed the task {selected_task.title}"
    payload = {"channel":"task-notifications", "text":slack_message}
    headers = {"Authorization":f'Bearer {Key}'}
    requests.patch("https://slack.com/api/chat.postMessage", data=payload, headers=headers)


    task_dict = selected_task.make_task_dict()
    response_dict = {"task": task_dict}
    return response_dict, 200

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete(task_id):
    selected_task = validate_id(task_id)

    selected_task.completed_at = None
    db.session.commit()

    task_dict = selected_task.make_task_dict()
    response_dict = {"task": task_dict}
    return response_dict, 200


"""
GOAL ROUTES
"""

@goal_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()

    sort_param = request.args.get("sort")


    response = []
    for goal in goals:
        task_dict = make_task_dict(task)
        response.append(task_dict)
    
    if sort_param == "asc":
        response = sorted(response, key=lambda i:i['title'])
    if sort_param == "desc":
        response = sorted(response, key=lambda i:i['title'], reverse=True)

    return jsonify(response), 200
