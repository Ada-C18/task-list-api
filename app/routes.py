
from flask import Blueprint, jsonify, request, make_response, abort
from app import db 
from app.models.task import Task
from sqlalchemy import desc, asc


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(f'"details": invalid data'), 400)

    task = Task.query.get(task_id)

    if not task:
        response = f"task not found"
        abort(make_response(jsonify({"message":response}), 404))

    return task




@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"},400)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])       
    db.session.add(new_task)
    db.session.commit()

    
    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.completed_at is not None
        }

    }
    return make_response(jsonify(response)), 201 
   


@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():

    title_query = request.args.get("sort")
    # print(title_query)
    if title_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
        
    elif title_query == "asc": 
        tasks = Task.query.order_by(asc(Task.title))
    else:
        tasks = Task.query.all()


    task_response = [] 
    for task in tasks:
        task_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        })

    return jsonify(task_response), 200



@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }

    }, 200


    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }
    

  
    return make_response(jsonify(response)), 200



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200



# @tasks_bp.route("/<task_id>/<mark_complete_or_not>", methods=["PATCH"])
# def task_is_complete():
    




