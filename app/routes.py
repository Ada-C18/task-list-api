from app import db
from flask import Blueprint, jsonify, request, abort, make_response, json
from app.models.task import Task
from datetime import datetime
import os
import requests

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model



# new_task = Task.from_dict(request_body)
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({'task': new_task.to_dict()}), 201)



@task_bp.route("", methods=["GET"])
def list_all_tasks():
    task_list = []

    def is_complete():
        if "completed_at" in task_list == None:
            return True
        else:
            return False

    sort_query = request.args.get("sort")
    
    if sort_query:
        if "asc" in sort_query:
            tasks = Task.query.order_by(Task.title)
        elif "desc" in sort_query:
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()   
    
    for task in tasks:
        task_list.append({
            "id": task.task_id, 
            "title": task.title, 
            "description": task.description, 
            "is_complete": is_complete()
            })
    return jsonify(task_list)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    tasks = Task.query.get(task_id)
    
    return {
            "task": {
            "id": task.task_id, 
            "title": task.title, 
            "description": task.description, 
            "is_complete": False
                    }
                    }
        


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}


def slack_bot(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("API_KEY")
    
    query_params = {
        "channel": "#task-notifications",
        "text": message
        }    

    requests.post(PATH, json=query_params, headers={"Authorization": SLACK_API_KEY})




@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at=datetime.now()

    
    db.session.commit()

    slack_bot(f"Someone just completed the task {task.title}")
    
    return make_response(jsonify({'task':Task.to_dict(task)}), 200)



@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at=None
    dict_task =task.to_dict()
        

    db.session.commit()

    return make_response(jsonify({'task': dict_task}), 200)



@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({'task': new_task.to_dict()}), 201)










# ---------------------------------------------------------------------------------------------------------
# def validate_task(id):
#     tasks = Task.query.get(task_id)
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message": f"task {task_id} is invalid"}, 400))
#     for task in tasks:
#         if task.task_id == task_id:
#             return task
#     abort(make_response({"message": f"{task_id} not found"}, 404))   
    
    
    
    
    # @task_bp.route("", methods=["POST"])
# def create_task():
#     request_body = request.get_json()
    
#     new_task = Task.from_dict(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify(f"task: {new_task.title} successfully created"), 201)

    
    
    
    
    # tasks = Task.query.get(task_id)
    # task_id = int(task_id)
    # task = validate_model(Task, task_id)
    # for task in tasks:
    #     if task.task_id == task_id:
    #         return {"task": {
    #             "id": task.task_id,
    #             "title": task.title,
    #             "description": task.description,
    #             "is_complete": task.completed_at
    #         } 
    #         }

    # return {"message":f"task {task_id} not found"}, 404
# {"task": task.to_dict()}

