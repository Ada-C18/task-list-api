from app.models.task import Task
from app.models.goal import Goal
from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc, desc
# import datetime
from datetime import date
import requests
import os


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


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

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details": f"{cls.__name__} {id} invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"details": f"{cls.__name__} {id} not found"}, 404))
    
    return model

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
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()
    }, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
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
    task = validate_model(Task, task_id)
    

    db.session.delete(task)
    db.session.commit()


    return make_response(jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"))

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    # request_body = request.get_json()

    # task.title = request_body["title"]
    # task.description = request_body["description"]
    task.completed_at = date.today()

    db.session.commit()

    dict_response = {
            "task": task.to_dict()
                        }
    dict_response["task"]["is_complete"]= True

    message = f"Someone just completed the task {task.title}"
    
    send_slack_message(message)
    
    
    return make_response(jsonify(dict_response),200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    # request_body = request.get_json()
    # request_body["completed_at"] = None
    # try:
    #     isinstance(task.completed_at, datetime.date)
    #     # datetime.datetime)
    # except:
    #     abort(make_response({"details": f"Task {task_id} invalid"}, 400))

    # task.title = request_body["title"]
    # task.description = request_body["description"]
    # task.completed_at = date.today()

    db.session.commit()
    dict_response = {
            "task": task.to_dict()
                        }
    dict_response["task"]["is_complete"]= False
    return make_response(jsonify(dict_response),200)

def send_slack_message(message):
    path = "https://slack.com/api/chat.postMessage"
    header = {
        "Content-type": "application/json",
    "Authorization": os.environ.get("SLACK_API_KEY")}
    
    post_arguments = {
        "channel" :"task-notifications",
        "text": message
    }

    requests.post(path, json=post_arguments, headers=header)
    # response_body = response.json

# goals routes

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
         abort(make_response({"details": "Invalid data"}, 400))
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_response = {"goal": new_goal.to_dict()}

    return make_response(jsonify(goal_response), 201)

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_dict()
    }, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_response = {"goal": goal.to_dict()}
    
    return make_response(jsonify(goal_response), 200)
    
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(details=f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted")) 

