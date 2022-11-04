from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details": "Invalid data"
            }), 400
    
    new_task = Task( 
        title=request_body["title"],
        description=request_body["description"],)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({ 
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }
    }), 201 

@task_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append({
            "id":task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(task_response)
   
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify ({ 
        "task": {
        "id": chosen_task.task_id,
        "title": chosen_task.title,
        "description": chosen_task.description,
        "is_complete": False
    }
    })

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()

    task = get_task_from_id(task_id)

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"msg": "Request must include a title and description."}),400


    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }

    })

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):

    task = get_task_from_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        })
    



#helper function to get task by id:
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg":f"Invalid data type: {task_id}"}, 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find task item with id: {task_id}"}, 404))
    return chosen_task
