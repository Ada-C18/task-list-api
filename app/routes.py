from os import abort
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

from sqlalchemy import asc, desc
import time
from datetime import date

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
    task_response = []
    
    task_query = request.args.get("title")
    sorting_query =request.args.get("sort")

    if task_query is not None:
        tasks = Task.query.filter_by(title=task_query) #do the sort by asc and desc
    elif sorting_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sorting_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
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

#wave 3 creating a custom endpoint--mark a task as complete = True 
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_a_complete_task(task_id):
    # a task is_complete=True when there is a datemine for the task's completed_at value.
    
    task = get_task_from_id(task_id)
    
    task.is_complete = True
    task.completed_at = date.today()

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }

    }), 200

#wave 3 creating a custom endpoint--mark a task as incomplete = False
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_an_uncomplete_task(task_id):
    # a task is_complete=True when there is a datemine for the task's completed_at value.
    task = get_task_from_id(task_id)
    task.is_complete = False
    task.completed_at = None #date.today()
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }),200

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
