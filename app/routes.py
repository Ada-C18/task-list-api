from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
#------------------------------------WAVE 1----------------------------------
#Create a Task: Valid Task With null completed_at
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    #Create a Task: Invalid Task With Missing Data
    if  "title" not in request_body or\
        "description" not in request_body:
            abort(make_response({"details": "Invalid data"},400))
  
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    )
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task":{
        "id":new_task.task_id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":False
    }},201)

#Get all Task
@tasks_bp.route("", methods=["Get"])
def get_all_task():
    task_query = request.args.get("sort")
    if task_query =='desc':
        #Sorting Tasks: By Title, Descending
        tasks = Task.query.order_by(Task.title.desc()).all() 
    else:
        #Sorting Tasks: By Title, Ascending
        tasks = Task.query.order_by(Task.title).all() 
    # tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False
        })
    return make_response(jsonify(tasks_response),200)

#Get One Task: One Saved Task
def check_valid_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"invalid task id {task_id}"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"message": f"No id {task_id} task"}, 404))
    return task
    
@tasks_bp.route('/<task_id>', methods =["GET"])
def get_task_by_id(task_id):
    task = check_valid_id(task_id)
    return make_response({"task":{
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":False
    }}, 200)
    
#Update Task
@tasks_bp.route('/<task_id>', methods =["PUT"])
def update_one_task(task_id):
    task = check_valid_id(task_id)
    request_body = request.get_json()
    if "title" not in request_body or\
        "description" not in request_body:
        return jsonify({"message": "Request must include title, description"}), 400
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return make_response({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }},200)
    
#Delete Task: Deleting a Task
@tasks_bp.route('/<task_id>', methods =["DELETE"])
def delete_task(task_id):
    task = check_valid_id(task_id)
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details":f'Task {task_id} "{task.title}" successfully deleted'}),200

#------------------------------------WAVE 3----------------------------------
 #Mark Complete on an Incompleted Task
@tasks_bp.route('/<task_id>/mark_complete', methods =["PATCH"])   
def mark_complete(task_id):
    task = check_valid_id(task_id)
    if task.completed_at is None:
        task.completed_at = datetime.now()

        db.session.commit()
    return make_response({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }},200)
    
#Mark Incomplete on a Completed Task
@tasks_bp.route('/<task_id>/mark_incomplete', methods =["PATCH"])     
def mark_incomplete(task_id):
    task =  check_valid_id(task_id)
    if task.completed_at:
        task.completed_at = None
        
    db.session.commit()
    return make_response({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }},200)
    
#------------------------------------WAVE 4----------------------------------
path = "https://slack.com/api/chat.postMessage"

API_KEY = "Bearer key_token"

@tasks_bp.route('/<task_id>/mark_complete_in_slack', methods =["PATCH"])   
def mark_complete1(task_id):
    task = Task.query.get(task_id)
    if task:
        query_params = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}",
            "format": "json"
        }
    else:
        query_params = {
            "channel": "task-notifications",
            "text": f"No this No. {task_id} task",
            "format": "json"
        }
    headers = {"Authorization": API_KEY}

    response = requests.post(path, data=query_params, headers=headers)

    return(response.json())

#------------------------------------WAVE 5----------------------------------
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Create a Goal: Valid Goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    #Create a Task: Invalid Task With Missing Data
    if  "title" not in request_body:
            abort(make_response({"details": "Invalid data"},400))
  
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":{
        "id":new_goal.goal_id,
        "title":new_goal.title,
    }},201)
    
# Get Goals: Getting Saved Goals
@goals_bp.route("", methods=["GET"])
def get_all_goal():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title":goal.title
        })
    return make_response(jsonify(goals_response),200)

# Get One Goal: One Saved Goal
def check_valid_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"invalid goal id {goal_id}"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return abort(make_response({"message": f"No id {goal_id} goal"}, 404))
    return goal

@goals_bp.route("<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = check_valid_goal_id(goal_id)
    return make_response({"goal":{
        "id":goal.goal_id,
        "title":goal.title,
    }}, 200)
    
#Update Goal
@goals_bp.route('/<goal_id>', methods =["PUT"])
def update_one_goal(goal_id):
    goal = check_valid_goal_id(goal_id)
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"message": "Request must include title"}), 400
    
    goal.title = request_body["title"]
    
    db.session.commit()
    return make_response({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }},200)
    
# Delete Goal: Deleting a Goal
@goals_bp.route('/<goal_id>', methods =["DELETE"])
def delete_goal(goal_id):
    goal = check_valid_goal_id(goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}),200

#------------------------------------WAVE 6----------------------------------
# Sending a List of Task IDs to a Goal
@goals_bp.route('/<goal_id>/tasks', methods =["POST"])
def goal_add_into_task_by_id(goal_id):
    goal = check_valid_goal_id(goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
        db.session.add(task)
        db.session.commit()
    return make_response({
            "id": goal.goal_id,
            "task_ids": request_body["task_ids"]
            }, 200)
# Getting Tasks of One Goal
@goals_bp.route('/<goal_id>/tasks', methods =["GET"])
def get_tasks_one_goal(goal_id):
    goal = check_valid_goal_id(goal_id)
    tasks = Task.query.filter_by(goal_id = int(goal_id)).all()
    tasks_goal_response = []
    
    for task in tasks:
        # if task.goal_id == int(goal_id):
        tasks_goal_response.append({
            "id": task.task_id,
            "goal_id": int(goal_id),
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks":tasks_goal_response
        }),200)
    
@goals_bp.route('/tasks/<task_id>', methods =["GET"])
def get_task_includes_goal_id(task_id):
    task = check_valid_id(task_id)
    return make_response({"task":{
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete":False
        }}, 200)

