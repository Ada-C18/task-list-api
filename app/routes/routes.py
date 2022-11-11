from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task
from datetime import datetime
from app.models.goal import Goal
import os, requests

#VALIDATE ID
def validate_id(class_obj,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{id} is an invalid id"}, 400))
    query_result = class_obj.query.get(id)
    if not query_result:
        abort(make_response({"message":f"{id} not found"}, 404))

    return query_result

#CREATE TASK
task_bp = Blueprint("Task", __name__, url_prefix="/tasks")
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        #TODO later wave will need 'or "completed_at" not in request_body', add above
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_json(request_body)

    # abort(make_response)  
    db.session.add(new_task)
    db.session.commit()
    response_body = {
        "task": new_task.to_dict()
        }
    return make_response(response_body, 201)

# @task_bp.route("", methods=["GET"])
# def read_all_task():
#     tasks_response = []
#     tasks = Task.query.all()
#     for task in tasks:
#         tasks_response.append(task.to_dict())
#     return jsonify(tasks_response)
##GET ALL TASKS AND SORT TASKS BY ASC & DESC

@task_bp.route("", methods=["GET"])
def read_all_task():
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())
    return jsonify(response)

#GET ONE TASK
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)
    response_body = {
        "task": task.to_dict()
    }
    return response_body

#UPDATE TASK
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json() 
    task.title = request_body["title"]
    task.description = request_body["description"]
    # TODO task.completed_at = request_body["completed_at"] #include later
    # task.update(request_body)
    db.session.commit()
    response_body =  {
        "task": task.to_dict()
        }
    return make_response(response_body, 200)

#DELETE ONE TASK
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    task_dict = task.to_dict()

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task_dict["title"]}" successfully deleted'}

#MARK COMPLETE
#MODIFY MARK COMPLETE TO CALL SLACK API
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) #custom endpoint mark task complete
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.utcnow()

    db.session.commit()
    response = {
        "task": task.to_dict()
    }
    slack_key = os.environ.get("SLACKBOT_API_KEY")
    path = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    headers = {
        "authorization":f"Bearer {slack_key}"
    }
    return jsonify(response)


#MARK INCOMPLETE
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    
    db.session.commit()
    response = {
        "task": task.to_dict()
    }

    return jsonify(response)

### GOAL ROUTES
#POST/CREATE A GOAL
goals_bp = Blueprint("Goal", __name__, url_prefix="/goals")
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title=request_body["title"])

    #abort(make_response)  
    db.session.add(new_goal)
    db.session.commit()

    response_body = {
        "goal": new_goal.to_dict()
        }
    return make_response(response_body), 201

## GET ALL GOALS
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = []

    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

#GET ONE GOAL
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_id(Goal, goal_id) #id instead of goal_id
    response_body = {
        "goal": goal.to_dict()
    }
    return response_body

#UPDATE GOAL
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json() 
    goal.title = request_body["title"]

    db.session.commit()
    response_body =  {
        "goal": goal.to_dict()
        }
    return make_response(response_body, 200)

#DELETE ONE GOAL
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    goal_dict = goal.to_dict()

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal_dict["title"]}" successfully deleted'}
