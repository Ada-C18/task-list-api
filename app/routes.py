from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc, desc
from app.models.task import Task
from app import db
from datetime import datetime
import os



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message":f"Task {task_id} invalid"}, 400))

#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"message":f"Task {task_id} not found"}, 404))

#     return task

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    order_by = request.args.get("sort")

    if order_by == 'asc':
        tasks = Task.query.order_by(asc('title')).all()
    elif order_by == 'desc':
        tasks = Task.query.order_by(desc('title')).all()
    else:
        tasks = Task.query.all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = get_validate_model(Task, task_id)
    task_response = {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        }

    return make_response(jsonify(task_response), 200)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)
    
    # try:
    #     new_task = Task.from_dict(request_body)
    # except KeyError:
    #     abort(make_response({
    #                             "details": "Invalid data"
    #                         }, 400))
    # new_task = Task.from_dict(request_body)
    new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=None)

    db.session.add(new_task) # track this object
    db.session.commit() # any changes that are pending commit those changes as data written in SQL

    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # task_model = get_validate_model(Task, task_id)

    request_body = request.get_json()

    task_model = Task.query.get(task_id)

    if not task_model: 
        return make_response({"message":f"Task {task_id} not found"}, 404)  

    task_model.title = request_body["title"]
    task_model.description = request_body["description"]

    db.session.commit()

    return make_response({
        "task": {
            "id": task_model.task_id,
            "title": task_model.title,
            "description": task_model.description,
            "is_complete": False
        }
    }, 200)



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # task = get_validate_model(Task, task_id)

    task_model = Task.query.get(task_id)

    if not task_model: 
        return make_response({"message":f"Task {task_id} not found"}, 404)  

    db.session.delete(task_model)
    db.session.commit()

    return make_response({"details": f'Task {task_id} {task_model.title} successfully deleted'}, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_incompleted_task_to_complete(task_id):
    # task = get_validate_model(Task, task_id)
    task_model = Task.query.get(task_id)

    if not task_model: 
        return make_response({"message":f"Task {task_id} not found"}, 404)  

    task_model.completed_at = datetime.now()

    db.session.commit()

    # slack_bot(task)
    # return make_response(jsonify({"task": task_response}), 200)
    return make_response(jsonify({
        "task": {
            "id": task_model.task_id,
            "title": task_model.title,
            "description": task_model.description,
            "is_complete": True
        }
    }), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_completed_task_to_incomplete(task_id):
   # task = get_validate_model(Task, task_id)
    task_model = Task.query.get(task_id)

    if not task_model: 
        return make_response({"message":f"Task {task_id} not found"}, 404)  

    task_model.completed_at = None

    db.session.commit()

    # slack_bot(task)
    # return make_response(jsonify({"task": task_response}), 200)
    return make_response(jsonify({
        "task": {
            "id": task_model.task_id,
            "title": task_model.title,
            "description": task_model.description,
            "is_complete": False
        }
    }), 200)

# def is_complete():
#     request_body = request.get_json()
#     if request_body["completed_at"] is not None:
#         return True
#     else:
#         return False


# def slack_bot(task):
#     PATH = "https://slack.com/api/chat.postMessage"
#     SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

#     query_params = {
#         "channel": "task-notifications",
#         "text": f"Someone just completed the task {task.title}"
#     }

#     requests.post(PATH, params=query_params, headers={"Authorization": SLACK_API_KEY})