from app import db
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from sqlalchemy import desc


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    task_response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
        }
    }

    return make_response(task_response, 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    task_query = Task.query

    sort_query = request.args.get("sort")  # query param key

    if sort_query == "asc":
        tasks = task_query.order_by(Task.title).all()
        # Task.query.order_by(Task.title.all()) is a list of title objects for all records in the task db table in that order
        # The default for order_by() is ascending. For descending, need to import "from sqlalchemy import desc"

    elif sort_query == "desc":
        tasks = task_query.order_by(desc(Task.title)).all()

    else:
        tasks = task_query.all()

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete  # bool(task.completed_at)
        })

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(task_id)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }


def validate_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))
    else:
        return task


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}))


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # # we never want to update an id. It's covered by postgreSQL

    db.session.commit()

    task_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }

    return make_response(task_response, 200)

## completed_at -> date time column
## is_complete -> boolean column
@tasks_bp.route("", methods=["PATCH"])
def update_complete():
    complete_query = request.args.get("mark_complete") 
