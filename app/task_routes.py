from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import datetime as dt
import requests



tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
#################################################
#                WAVE 01
#################################################

#validate function 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


#Create a Task: Valid Task With null completed_at
#################
#       new
###############
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()},201

####################
#       original 
####################

# @tasks_bp.route("", methods=["POST"])
# def create_task():
#     request_body = request.get_json()
#     new_task = Task.from_dict(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)
#     return {"task":new_task.to_dict()},201

###########################
#       helper function for get
#########################
# def sort_function():
#     sort_query = request.args.get("sort")
#     if sort_query == "asc":
#         return Task.query.order_by(Task.title.asc())
#     elif sort_query == "desc":
#         return Task.query.order_by(Task.title.desc())
#     else:
#         return Task.query.all()
# ###########################
# #       new function for get w/helper
# #########################

# # Get Tasks: Getting Saved Tasks
# @tasks_bp.route("", methods=["GET"])
# def read_all_tasks():
#     task = sort_function()
#     if task:
#         return task
#     tasks = Task.query.all()

#     tasks_response = []
#     for task in tasks:
#         tasks_response.append(task.to_dict())

#     return jsonify(tasks_response)

#########################
# working original
#########################
# Get Tasks: Getting Saved Tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif title_query: 
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    ###old way???####
    # title_query = request.args.get("title")
    # if title_query:
    #     tasks = Task.query.filter_by(title=title_query)
    # else:
    #     tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)

# Get Tasks: Get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task":task.to_dict()}

# Update Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_book(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}

# Delete Task: Deleting a Task

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_book(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details":f'Task {task.task_id} "{task.title}" successfully deleted'}

########################################
#         PRACTICE  patch tasks/<task_id>mark_complete
########################################
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def updated_incomplete_task_to_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = (dt.date.today())

    db.session.commit()
    return {"task":task.to_dict()}, 200


########################################
#   CORRECT OLD W/O API patch tasks/<task_id>mark_complete
########################################

# Patch Task: Mark Complete on an Incompleted Task
# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def updated_incomplete_task_to_complete(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = (dt.date.today())

#     db.session.commit()
#     return {"task":task.to_dict()}, 200

# Mark Incomplete on a Completed Task
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def updated_complete_task_to_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return {"task":task.to_dict()}, 200