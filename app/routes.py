from os import abort
# from turtle import title
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(class_obj, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify({"message": f"task {task_id} has an invalid task_id"}), 400))

    query_result = class_obj.query.get(task_id)

    if not query_result:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return query_result

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
#     color_param =request.args.get("color")
#     name_param = request.args.get("name")
    
#     if color_param:
#         tasks = task.query.filter_by(color=color_param)
#     elif name_param:
#         tasks = task.query.filter_by(name=name_param)
#     else:
#         tasks = task.query.all()

    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
        #big question if we need all the params 
        # or we need to exclude COMPLETED_AT????
        # I've removed completed_at from to_dict
        # for now, commented it out
    
    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks_response = sorted(tasks_response, key=lambda dict: dict["title"])
    elif sorting_query == "desc":
        tasks_response = sorted(tasks_response, key=lambda dict: dict["title"], reverse=True) 
            
    return jsonify(tasks_response), 200
    
@tasks_bp.route("", methods=["POST"])
def create_task():
    #need to validate task
    request_body = request.get_json()
    print(request_body)
    # if request_body["title"] and request_body["description"]:
    if "title" in request_body and "description" in request_body:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        response_one_task = {}
        response_one_task["task"] = Task.to_dict(new_task)
        return jsonify(response_one_task), 201
    else:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))



@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(Task, task_id)
    response_one_task = {}
    response_one_task["task"] = Task.to_dict(task)
    return jsonify(response_one_task), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(Task, task_id)
    request_body = request.get_json()
    
    task.update(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    response_updated_task = {}
    response_updated_task["task"] = Task.to_dict(task)
    return jsonify(response_updated_task), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"})
