from flask import Blueprint,request,jsonify,abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix ="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: {task_id} ID must be Integer"
        abort(make_response(jsonify({"message: response_str"}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task:
        response_str = f"Task with id {task_id} not found in database"
        abort(make_response(jsonify({"message": response_str}),404))

    return matching_task


@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        
    )
    db.session.add(new_task)
    db.session.commit()
    
    is_completed = True
    if new_task.completed_at is None:
        is_completed = False


    task_dict = {"id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": is_completed
    }

    return jsonify({"task":task_dict}), 201

@task_bp.route("", methods = ["GET"])
def get_task():
    tasks = Task.query.all()
    response= []
    
    for task in tasks:
        is_completed = True
        if task.completed_at is None:
            is_completed = False
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_completed
            
        }

        response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    tasks = Task.query.all()
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: {task_id} ID must be integer"
        return jsonify({"message": response_str}), 400

    for task in tasks:
        if task_id == task.task_id:
            is_completed = True
            if task.completed_at is None:
                is_completed = False
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_completed
            }
            return jsonify({"task": task_dict}), 200
    response_message = f"Could not find task with ID {task_id}"
    return jsonify({"message": response_message}), 404

@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = get_one_task_or_abort(task_id) # we are getting a validated task id here
    request_body = request.get_json() #converts json into dictionary

    is_completed = True
    if task.completed_at is None:
        is_completed=False
    task.title = request_body["title"]
    task.description = request_body["description"]
    

    db.session.commit()

    task_dict = {"id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": is_completed
    }

    return jsonify({"task":task_dict}), 200
    

# @task_bp.route("<task_id>", methods=["DELETE"])
# def delete_one_task(task_id):
#     chosen_task = get_one_task_or_abort(task_id)

#     db.session.delete(chosen_task)
#     db.session.commit()
#     return jsonify({"details": f"`{chosen_task}` Go on my daily walk successfully deleted"}),200






    


