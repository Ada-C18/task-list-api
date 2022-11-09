from app.models.task import Task
from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc, desc




task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # new_task = Task.from_dict(request_body)

    if "description" not in request_body or "title" not in request_body:
         abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task.from_dict(request_body)

    # if "completed_at" in request_body:
    #             new_task = Task(
    #             title=request_body['title'], 
    #             description=request_body['description'],
    #             is_complete=request_body['completed_at'])
    # else:
    #             new_task = Task(
    #             title=request_body['title'], 
    #             description=request_body['description'])
                

    db.session.add(new_task)
    db.session.commit()


    dict_response = {
            "task": new_task.to_dict()
                        }
    
    return make_response(jsonify(dict_response), 201)

def validate_task(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": f"Task {task_id} invalid"}, 400))

    task = cls.query.get(task_id)

    if not task:
        abort(make_response({"details": f"Task {task_id} not found"}, 404))
    
    return task

@task_bp.route("", methods=["GET"])
def get_tasks():

    sort_query = request.args.get("sort")
    if sort_query == "asc": 
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc": 
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200




@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(Task, task_id)
    return {"task": task.to_dict()
    }, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    dict_response = {
            "task": task.to_dict()
                        }

    return make_response(jsonify(dict_response),200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(Task, task_id)
    

    db.session.delete(task)
    db.session.commit()


    return make_response(jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"))






    




    
