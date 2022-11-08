from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")



def validate_task(task_id):
    try:
        verified_id = int(task_id)
    except ValueError:
        abort(make_response("Invalid ID: id must be an integer", 400))

    task = Task.query.get(verified_id)

    if not task:
        abort(make_response(jsonify("Invalid ID: id does not exist"), 404))

    return task

def format_return_json_object(target_task):
    task = Task.query.filter_by(task_id=target_task.task_id)
    return {"id": target_task.task_id,
            "title": target_task.title,
            "description": target_task.description,
            "is_complete": target_task.completed_at
            }
    return task


@tasks_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"],
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task":format_return_json_object(new_task)}, 201
   


@tasks_bp.route("", methods=["GET"])
def list_all_tasks():
    
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()



    response = [format_return_json_object(task) for task in tasks]
    return jsonify(response), 200




@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_task(task_id)

    return {"task":format_return_json_object(task)}, 200
