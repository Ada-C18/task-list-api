from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_complete_request(request_body):
    try:
        if request_body["title"] and request_body["description"]:
            return request_body

    except:
        abort(make_response({"details": "Invalid data"}, 400))


def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    valid_data = validate_complete_request(request_body)
    new_task = Task.from_dict(valid_data)

    db.session.add(new_task)
    db.session.commit()

    task_response = {
        "task": new_task.to_dict_post_put()
    }
    return make_response(jsonify(task_response), 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks_sort_asc():
    task_query = Task.query.all()
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed at")
    sort_query = request.args.get("sort")
    if title_query:
        task_query = Task.query.filter_by(title=title_query)
    if description_query:
        task_query = Task.query.filter_by(description=description_query)
    if completed_at_query:
        task_query = Task.query.filter_by(completed_at=completed_at_query)
    if sort_query == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    if sort_query == "desc":
        task_query = Task.query.order_by(Task.title.desc())

    tasks = task_query

    tasks_response = [task.to_dict_get_patch() for task in tasks]

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model_id(Task, task_id)

    task_response = {
        "task": task.to_dict_get_patch()
    }

    return make_response(jsonify(task_response), 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def task_update_entire_entry(task_id):
    task = validate_model_id(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    task_response = {
        "task": task.to_dict_post_put()
    }

    return make_response((task_response), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_mark_complete(task_id):
    task = validate_model_id(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    task_response = {
        "task": task.to_dict_get_patch()
    }

    return make_response((task_response), 200)
    

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_mark_incomplete(task_id):
    task = validate_model_id(Task, task_id)
    task.completed_at = None

    db.session.commit()

    task_response = {
        "task": task.to_dict_get_patch()
    }

    return make_response((task_response), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def task_delete(task_id):
    task = validate_model_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details': f'Task {task.id} "{task.title}" successfully deleted'}, 200)