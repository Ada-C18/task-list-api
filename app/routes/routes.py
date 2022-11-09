from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task
from datetime import datetime
from app.models.goal import Goal

#VALIDATE ID
def validate_id(class_obj,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{id} is an invalid id"}, 400))
    query_result = class_obj.query.get(id)
    if not query_result:
        abort(make_response({"message":f"{id} not found"}, 404))

    return query_result

#CREATE TASK
task_bp = Blueprint("Task", __name__, url_prefix="/tasks")
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        #TODO later wave will need 'or "completed_at" not in request_body', add above
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_json(request_body)

    # abort(make_response)  
    db.session.add(new_task)
    db.session.commit()
    response_body = {
        "task": new_task.to_dict()
        }
    return make_response(response_body, 201)

# @task_bp.route("", methods=["GET"])
# def read_all_task():
#     tasks_response = []
#     tasks = Task.query.all()
#     for task in tasks:
#         tasks_response.append(task.to_dict())
#     return jsonify(tasks_response)
##GET ALL TASKS AND SORT TASKS BY ASC & DESC

@task_bp.route("", methods=["GET"])
def read_all_task():
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())
    return jsonify(response)

#GET ONE TASK
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)
    response_body = {
        "task": task.to_dict()
    }
    return response_body

#UPDATE TASK
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json() 
    task.title = request_body["title"]
    task.description = request_body["description"]
    # TODO task.completed_at = request_body["completed_at"] #include later
    # task.update(request_body)
    db.session.commit()
    response_body =  {
        "task": task.to_dict()
        }
    return make_response(response_body, 200)

#DELETE ONE TASK
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    task_dict = task.to_dict()

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task_dict["title"]}" successfully deleted'}

#MARK COMPLETE
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) #custom endpoint mark task complete
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.utcnow()

    db.session.commit()
    response = {
        "task": task.to_dict()
    }
    
    return jsonify(response)


#MARK INCOMPLETE
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    
    db.session.commit()
    response = {
        "task": task.to_dict()
    }

    return jsonify(response)

