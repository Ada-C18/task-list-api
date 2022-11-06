from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"Message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"Message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods =["GET"])
def read_all_tasks(): 
    tasks = Task.query.all()
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(
            {
                "id":task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )

    # dealing with Query Params (Wave 2):
    sorting_type = request.args.get("sort")
    if not sorting_type: #no sorting
        return jsonify(tasks_response)
    elif sorting_type == "asc":
        sorted_tasks_response = sorted(tasks_response, key = lambda task: task["title"])
    elif sorting_type == "desc":
        sorted_tasks_response = sorted(tasks_response, key = lambda task: task["title"], reverse=True)
    return jsonify(sorted_tasks_response)

@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task(title=request_body["title"], 
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":
                {
                "id":new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
                }
            }, 201)
    
@tasks_bp.route("/<task_id>", methods =["GET"])
def read_one_task(task_id):
    task = validate_model(Task,task_id)
    return {"task":
                {
                "id":task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                }
            }

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task":
                {
                "id":task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                }
            }
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

