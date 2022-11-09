from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, request, make_response
from datetime import datetime
import os, requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#__________________________________________________________________________________________________________
#--------------------------------HELPER FUNCTIONS----------------------------------------------------------
#__________________________________________________________________________________________________________
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def slack_message(task_name):
    
    return f'Someone just completed the task {task_name}'

#____________________________________________________________________________________________________________
#--------------------------------CREATE TASK-----------------------------------------------------------------
#____________________________________________________________________________________________________________
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task= Task.from_dict(request_body)
    except KeyError:
        if "title" not in request_body or "description" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
            
    new_task= Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    dict_task = new_task.to_dict()
    
    return make_response(jsonify({"task":dict_task}), 201)

#__________________________________________________________________________________________________________
#-----------------------------------GET TASK---------------------------------------------------------------
#__________________________________________________________________________________________________________

@tasks_bp.route("", methods=["GET"])
def get_task():
    
    tasks_response= []
    sort_query= request.args.get("sort")
    title_query= request.args.get("title")
    
    if title_query:
        tasks= Task.query.filter_by(title=title_query)
    elif sort_query=="asc":
        tasks= Task.query.order_by(Task.title.asc()).all()  
    elif sort_query=="desc":
        tasks= Task.query.order_by(Task.title.desc()).all()
    else:
        tasks= Task.query.all()
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task= validate_model(Task, task_id)
    dict_task = task.to_dict()
    
    return jsonify({'task':dict_task})

#__________________________________________________________________________________________________________
#--------------------------------UPDATE TASK---------------------------------------------------------------
#__________________________________________________________________________________________________________

@tasks_bp.route("/<task_id>", methods=["PUT"])   
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.update(request_body)
    dict_task = task.to_dict()
    db.session.commit()

    return make_response(jsonify({'task':dict_task}), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])   
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at= datetime.now()
    dict_task = task.to_dict()
    
    db.session.commit()
    
    task_name= dict_task["title"]
    slack_channel= "task-completed"
    slack_token= os.environ.get("SLACK_TOKEN")
    path = 'https://slack.com/api/chat.postMessage'
    LOCATIONIQ_API_KEY = slack_token

    query_params = {
        "key": LOCATIONIQ_API_KEY,
        "format": "json",
        "text": slack_message(task_name),
        "channel": slack_channel
    }
    requests.post(path, params=query_params, headers={
                'Authorization': LOCATIONIQ_API_KEY})
    
    return make_response(jsonify({'task':dict_task}), 200) 

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])   
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at= None
    dict_task = task.to_dict()
    
    db.session.commit()
    return make_response(jsonify({'task':dict_task}), 200)

#_________________________________________________________________________________________________________
#--------------------------------DELETE TASK----------------------------------------
#___________________________________________________________________________________

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
#potential helper function
    dict_task=task.to_dict()
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'details': (f'Task {task_id} "{dict_task["title"]}" successfully deleted')})

####################################################################################
#################################GOAL ROUTE#########################################
####################################################################################
#___________________________________________________________________________________
#--------------------------------CREATE GOAL----------------------------------------
#___________________________________________________________________________________
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal= Goal.from_dict(request_body)
    except KeyError:
        if "title" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
            
    new_goal= Goal.from_dict(request_body)
    
    db.session.add(new_goal)
    db.session.commit()
    dict_goal = new_goal.to_dict()
    
    return make_response(jsonify({"goal":dict_goal}), 201)

#___________________________________________________________________________________
#-----------------------------------GET GOALS---------------------------------------
#___________________________________________________________________________________

@goals_bp.route("", methods=["GET"])
def get_goals():   
    goals_response= []
    title_query= request.args.get("title")
    
    if title_query:
        goals= Goal.query.filter_by(title=title_query)
    else:
        goals= Goal.query.all()
    
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal= validate_model(Goal, goal_id)
    dict_goal = goal.to_dict()
    
    return jsonify({'goal':dict_goal})

#___________________________________________________________________________________
#--------------------------------UPDATE GOAL----------------------------------------
#___________________________________________________________________________________

@goals_bp.route("/<goal_id>", methods=["PUT"])   
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    goal.update(request_body)
    dict_goal = goal.to_dict()
    db.session.commit()

    return make_response(jsonify({'goal':dict_goal}), 200)

#___________________________________________________________________________________
#--------------------------------DELETE GOAL----------------------------------------
#___________________________________________________________________________________

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    dict_goal=goal.to_dict()
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'details': (f'Goal {goal_id} "{dict_goal["title"]}" successfully deleted')})

#___________________________________________________________________________________
#------------------------GOAL-TASK-RELATIONSHIP-------------------------------------
#___________________________________________________________________________________
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goals_tasks(goal_id):
    goal= validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids= request_body["task_ids"]
    goal.tasks= []
    
    for id in task_ids:
        goal.tasks.append(Task.query.get(id))

    db.session.commit()   
    response ={
        "id": goal.goal_id,
        "task_ids": task_ids
    }

    return jsonify(response), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_goals_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    task_id=[] 
    
    for task in goal.tasks:
        task_dict= task.to_dict()
        task_id.append(task_dict)
    response_dict= goal.to_dict()
    response_dict["tasks"]= task_id
    
    return jsonify(response_dict), 200