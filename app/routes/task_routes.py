#Does the api have to only work with the following: A completed_at attribute with a null value
#Can it not work on a task that has already been marked complete/doesn't have a null value?
#How do you choose which hellper functions to go in the class module and which to keep on this page
from flask import Blueprint, request, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from operator import itemgetter
from datetime import date
import requests
import os

api_key = os.environ.get("SLACK_API")

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#-------------------------------------------HELPERS----------------------------------
def validate_object(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {obj_id} invalid"}, 400))

    matching_obj = cls.query.get((obj_id))

    if not matching_obj:
        abort(make_response({"message": f"{cls.__name__} {obj_id} not found"}, 404))

    return matching_obj

def determine_completion(task):
    if task.completed_at == None:
        task.completed_at = False
    else:
        task.completed_at = True #task["completed_at"]
    
    return task.completed_at

#-------------------------------------------POST----------------------------------
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    if 'title' not in request_body or\
        'description' not in request_body:
        # 'completed_at' not in request_body: ----- #read-me wave 1 says to put this in but not even the tests request body's have a completed_at 
            return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict(determine_completion)
    }, 201
#-------------------------------------------GET----------------------------------
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sort = request.args.get("sort")
    
    tasks = Task.query.all()

    response = []
    for task in tasks:
        task_info = task.to_dict(determine_completion)
        response.append(task_info)

    if title_sort == "asc":
        response = sorted(response, key=itemgetter("title"))
    elif title_sort == "desc":
        response = sorted(response, key=itemgetter("title"), reverse=True)

    return jsonify(response), 200

@task_bp.route("/<task_id_input>", methods=["GET"])
def get_one_task(task_id_input):
    chosen_task = validate_object(Task, task_id_input)

    task_info = {
        "task": chosen_task.to_dict(determine_completion)
    }

    return jsonify(task_info), 200
# -------------------------------------------PUT----------------------------------
@task_bp.route("/<task_id_input>", methods=["PUT"])
def update_a_task(task_id_input):
    chosen_task = validate_object(Task, task_id_input)

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"message":"Request must include title and description"})

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    # chosen_task.completed_at = request_body["completed_at"]
    
    db.session.commit()

    return {
        "task": chosen_task.to_dict(determine_completion)
    }, 200

# -------------------------------------------PATCH----------------------------------
@task_bp.route("/<task_id_input>/<complete_status>", methods=["PATCH"])
def mark_complete_status(task_id_input, complete_status):
    chosen_task = validate_object(Task, task_id_input)

    request_body = request.get_json()

    if complete_status == "mark_complete":
        chosen_task.completed_at = date.today()
        url = 'https://slack.com/api/chat.postMessage'
        payload = {'channel': 'task-notifications', 'text': f'Someone just completed the task {chosen_task.title}'} #what are we supposed to put again?
        header = {'Authorization': f'Bearer {api_key}'}
        slack_request = requests.post(url, params=payload, headers=header)
    elif complete_status == "mark_incomplete":
        chosen_task.completed_at = None

    db.session.commit()

    return {
    "task": chosen_task.to_dict(determine_completion)
    }

# @task_bp.route("/<task_id_input>/<complete_status>", methods=["PATCH"])
# def mark_incomplete(task_id_input, complete_status):
#     chosen_task = validate_task(task_id_input)
#     print(f"CHOSEN TASK = {chosen_task}")
#     request_body = request.get_json()
#     print(f"REQUEST BODY = {request_body}")
#     # if "title" in request_body:
    # #     new_title = chosen_task.title
    # # if "description" in request_body:
    # #     new_descrip = chosen_task.description
    # if complete_status == "mark_incomplete":
    #     chosen_task.completed_at = Task.completed_at
    # db.session.commit()
    # print(f"DATE!!!!: {chosen_task.completed_at}")

    # return {
    # "task": {
    #     "id": chosen_task.task_id,
    #     "title": chosen_task.title,
    #     "description": chosen_task.description,
    #     "is_complete": False #determine_completion(chosen_task)
    #     }
    # }
# -------------------------------------------DELETE----------------------------------
@task_bp.route("/<task_id_input>", methods=["DELETE"])
def delete_a_task(task_id_input):
    chosen_task = validate_object(Task, task_id_input)

    db.session.delete(chosen_task)
    db.session.commit()

    return {"details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"}

