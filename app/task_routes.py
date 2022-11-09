from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from .routes_helper import get_one_obj_or_abort
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    print(request_body)
    if not "title" in request_body or not "description" in request_body:
        return jsonify({"details": "Invalid data"}), 400

    
    new_task = Task(
        title=request_body["title"], 
        description=request_body["description"]
        )


    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def get_saved_tasks_and_sort():
    sorted_query = request.args.get("sort")

    if sorted_query:
        if sorted_query == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sorted_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    
    return jsonify(task_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    task_dict = chosen_task.to_dict()
    if not task_dict:
        return jsonify({f"message": f"Task with id {task_id} was not found in the database."})
    else:
        return jsonify({"task": task_dict}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        return jsonify({"details": "Invalid data"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    task_dict = chosen_task.to_dict()

    db.session.commit()

    return jsonify({"task": task_dict}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    #chosen_task = Task.query.get(task_id)
    
    chosen_task.completed_at = datetime.now() 
    task_dict = chosen_task.to_dict()

    # db.session.add(chosen_task)
    db.session.commit()

    if not task_dict:
        return jsonify({f"message": f"Task with id {task_id} was not found in the database."}), 404

    return jsonify({"task": task_dict}), 200 

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_task_to_incomplete(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    #chosen_task = Task.query.get(task_id)
    print(chosen_task)
    chosen_task.completed_at = None
    task_dict = chosen_task.to_dict()

    # db.session.add(chosen_task)
    db.session.commit()

    if not task_dict:
        return jsonify({f"message": f"Task with id {task_id} was not found in the database."}), 404

    return jsonify({"task": task_dict}), 200 


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    task_dict = chosen_task.to_dict()

    db.session.delete(chosen_task)
    db.session.commit()

    if not task_dict:
        return jsonify({f"message": f"Task with id {task_id} was not found in the database."}), 404
    

    return jsonify({f"details": f"Task {task_id} \"{task_dict['title']}\" successfully deleted"}), 200
    

    
    
    

'''
    tasks = Task.query.order_by(sort=sort_asc)
    sort_asc = request.args.get("sort=asc")

    if sort_asc is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.order_by(sort=sort_asc)

    sort_desc = request.args.get("sort=desc")

    if sort_desc is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.sort_by(sort=sort_desc)

    response = [task.to_dict() for task in tasks] '''

#    return jsonify(response), 200

'''
Working code for wave 1 get method tests before working on sort for wave 2

@tasks_bp.route("", methods=["GET"])
def get_saved_tasks_and_sort():
    title_param = request.args.get("title")

    if title_param is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(title=title_param)

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200
'''