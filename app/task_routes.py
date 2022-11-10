from flask import Blueprint, jsonify, make_response, request, abort
from .models.task import Task
from app import db
import datetime, requests, os

# ===================
# BLUEPRINTS
# ===================

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ===================
# HELPER FUNCTIONS
# ===================

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def slack_bot_message(text):
    URL = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API_KEY")

    query_params = {
        "channel": "task-notifications",
        "text": text
    }

    requests.post(URL, data=query_params, headers={"Authorization": API_KEY})

def put_or_patch_model(cls, model_id):
    model = validate_model(cls, model_id)
    request_body = request.get_json()
    model.patch(request_body)

    db.session.commit()

    return {cls.__name__.lower(): model.create_dict()}

# ===================
# ROUTES
# ===================

@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.new_instance_from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return {"task": new_task.create_dict()}, 201

    except KeyError:
        return {"details": "Invalid data"}, 400

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.create_dict() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    response = {"task": task.create_dict()}
    return make_response(response)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    return put_or_patch_model(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["PATCH"])
def patch_task(task_id):
    return put_or_patch_model(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_and_send_slackbot(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.datetime.utcnow()
    task.is_complete = True

    db.session.commit()

    slack_bot_message(f"Someone just completed the task {task.title}")

    return {"task": task.create_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    return {"task": task.create_dict()}
