from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc, desc 
import datetime
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body) 

    db.session.add(new_task)
    db.session.commit()

    task_dict = {}
    task_dict["task"] = {"id":new_task.task_id, "title": new_task.title,"description":new_task.description, "is_complete":bool(new_task.completed_at)}

    return make_response(jsonify(task_dict), 201) 

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if "asc" in sort_query: 
            tasks = Task.query.order_by(Task.title.asc())
        elif "desc" in sort_query: 
            tasks = Task.query.order_by(Task.title.desc()) 
    else: 
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response) 
    

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_model(Task,task_id)

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    if bool(task.goal_id) == True:
        task_with_goal_dict = {}
        task_with_goal_dict["task"] = {"id":task.task_id,"goal_id":task.goal_id,"title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}
        return make_response(jsonify(task_with_goal_dict), 200)

    return make_response(jsonify(task_dict), 200) 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()

    task.update(request_body) 
    db.session.commit()

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    return make_response(jsonify(task_dict), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()
    dict = {"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}

    return make_response(jsonify(dict), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = datetime.datetime.now()

    create_slack_mssg(task) 

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    db.session.commit()

    return make_response(jsonify(task_dict), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = None

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    db.session.commit()

    return make_response(jsonify(task_dict), 200)

##############################################
######## ROUTE TO POST SLACK MESSAGE #########
##############################################

def create_slack_mssg(task_object):

    slack_token = os.environ.get("SLACK_TOKEN")

    message= f"Someone just completed the task {task_object.title}"
    args = {"token":slack_token,
            "channel": "task-notifications",
            "text": message
            }
    response=requests.post("https://slack.com/api/chat.postMessage", data=args) 

    return response.json()


###############################################
############# ROUTES FOR GOAL #################
###############################################

@goals_bp.route("", methods=["POST"])
def create_goals():
    request_body = request.get_json()
    new_goal = Goal.from_dict_goals(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = {}
    goal_dict["goal"] = {"id":new_goal.goal_id, "title": new_goal.title}

    return make_response(jsonify(goal_dict), 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({"id": goal.goal_id, "title": goal.title})

    return (jsonify(goals_response))


@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    return goal.to_dict_goals()

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_a_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    request_body = request.get_json()

    goal.update_goal(request_body) 
    db.session.commit()

    return goal.to_dict_goals()

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()
    delete_dict = {"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}
    return make_response(jsonify(delete_dict))


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_task_to_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.tasks =[] 

    for task_id in request_body["task_ids"]: 
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()

    return make_response(jsonify({"id":goal.goal_id,"task_ids":request_body["task_ids"]})),200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def gets_tasks_of_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    tasks_of_goal =[]  
    
    for task in goal.tasks:
        tasks_of_goal.append(
            {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
            ) 
    return make_response(jsonify({"id":goal.goal_id,"title":goal.title,"tasks":tasks_of_goal})),200 