from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request,abort
from sqlalchemy import desc, asc
import datetime
import os 
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
        
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"},400)
    
    if "completed_at" not in request_body:
        request_body["completed_at"]= None
        
    # new_task= Task.from_dict(request_body)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
    
    # new_task_result = {"task":{"id":new_task.task_id, 
    #                     "title":new_task.title, 
    #                     "description":new_task.description,
    #                     "is_complete":validate_is_complete()}}
    # return make_response(jsonify(new_task_result),201)
    return {"task":new_task.to_dict()},201
    
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    # tasks = Task.query.all()
    
    # title_query = request.args.get("title")
    sort_query = request.args.get("sort")
    
    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    # def validate_is_complete():
    #     if "completed_at" in tasks_response == None:
    #         return True
    #     else:
    #         return False
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    # for task in tasks:
    #     tasks_response.append(
    #             {
    #         "id":task.task_id,
    #         "title":task.title,
    #         "description":task.description,
    #         "is_complete":validate_is_complete()
    #         })
    return jsonify(tasks_response)
    # return [{"task":tasks.to_dict()}]

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    # task_dict={}
    # def validate_is_complete():
    #     if "completed_at" in task_dict == None:
    #         return True
    #     else:
    #         return False
    # task_dict={"task":
    #     {
    #     "id":task.task_id,
    #     "title":task.title,
    #     "description":task.description,
    #     "is_complete":validate_is_complete()
    #     }
    # }
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()
    if "completed_at" not in request_body:
        request_body["completed_at"]= None

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    # return{"task":
    #     {
    #         "id":task.task_id,
    #         "title":task.title,
    #         "description":task.description,
    #         "is_complete":validate_is_complete()
    #         } }
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()
    
    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}

def slack_bot(text):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_KEY = os.environ.get("SLACK_API_KEY")
    print(SLACK_KEY)
    query_params = {
        "channel": "task-notifications",
        "text": text
    }
    requests.post(PATH, params=query_params, headers={"Authorization":f"Bearer {SLACK_KEY}"})
    
    
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete(task_id):
    task = validate_model(Task,task_id)
    
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    
    slack_bot(f"Someone just completed the task {task.title}completed!")

    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task = validate_model(Task,task_id)
    
    task.completed_at = None
    db.session.commit()
    
    return {"task":task.to_dict()}