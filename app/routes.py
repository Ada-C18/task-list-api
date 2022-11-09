from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import datetime as dt
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Helper Functions 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
        
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def slack_bot_msg(task_title):

    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    my_headers = {'Authorization' : 'Bearer '+SLACK_TOKEN}
    query_params ={
        "channel": "task-notifications",
        "text": (f"Someone just completed the task {task_title}.")
    }

    requests.post(PATH, params=query_params, headers=my_headers)


#Task routes
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param=request.args.get("sort")
    if sort_param == "asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks=Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }), 200
    return jsonify(tasks_response),200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    if not task.goal_id:
        return task.response_dict(), 200
    else:
                return jsonify({
            "task": {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }}), 200
        

@tasks_bp.route("", methods=["POST"])
def create_task():  
    request_body = request.get_json()      
    if ("title" not in request_body) or ("description" not in request_body):
        return jsonify({
            "details": "Invalid data"
        }), 400
    else:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        return new_task.response_dict(), 201
    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return task.response_dict(), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }), 200)



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = (dt.date.today())
    db.session.commit()
    slack_bot_msg(task.title)
    return task.response_dict(), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = (None)
    db.session.commit()
    return task.response_dict(), 200

#Goal Routes
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals=Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
            }), 200
    return jsonify(goals_response),200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
            }}), 200

@goals_bp.route("", methods=["POST"])
def create_goal():  
    request_body = request.get_json()      
    if ("title" not in request_body):
        return jsonify({
            "details": "Invalid data"
        }), 400
    else:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }}), 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify ({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.tasks =[]
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()
    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        })), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
                "id": task.task_id,
                "goal_id": goal.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }), 200
    return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response}), 200