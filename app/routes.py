from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def new_task():

    request_body = request.get_json()
    if 'title' not in request_body or 'description' \
not in request_body or 'completed_at' not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
  
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        is_complete = new_task.completed_at !=  None
        return make_response({"task": {"id": new_task.task_id, "title": new_task.title, "description": new_task.description, "is_complete": is_complete}}, 201)
                                    
@tasks_bp.route("", methods=["GET"])
def all_tasks():
    title_query = request.args.get('title')
    order_by_query = request.args.get('sort')
    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif order_by_query == 'asc':
        tasks = Task.query.order_by(Task.title).all()

    elif order_by_query == 'desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.order_by(Task.title).all()
    
    task_response = []
    for task in tasks:
        is_complete = task.completed_at != None
        task_response.append({'id': task.task_id, 'title': task.title, 'description': task.description,'is_complete': is_complete})
    
    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def one_task(task_id):
    task = Task.query.get(task_id)
    if task == None:
        abort(404) 
    is_complete = task.completed_at != None
    if request.method == "GET":
        if task.goal_id:
            return make_response({"task": {"id": task.task_id,"title": task.title, "description": task.description, "goal_id": task.goal_id, "is_complete": is_complete}}, 200)
        else:
            return make_response({"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}, 200)
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = task.completed_at

        db.session.commit()

        return make_response({"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}, 200)

    elif request.method == "PATCH":
        form_data = request.get_json()
        if "title" in form_data:
            task.title = form_data["title"]
        if "description" in form_data:
            task.description = form_data["description"]
        
        db.session.commit()
        return make_response({"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}, 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({'details':f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
        
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_complete(task_id):

    time_stamp = datetime.now()
    task = Task.query.get(task_id)
    if task == None:
        abort(404) 
    else:
        task.completed_at = time_stamp
    db.session.commit()
    is_complete = task.completed_at != None
    
    try:
        header= {"Authorization"}
        post_body = requests.post(header)
    except TypeError:
        pass
    return make_response({"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_not_complete(task_id):
    task = Task.query.get(task_id)
    if task == None:
        abort(404) 
    else:
        task.completed_at = None
    db.session.commit()
    is_complete = task.completed_at != None
    return make_response({"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}, 200)  

@goals_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    if 'title' not in request_body :
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()
        return make_response({"goal": {"id": new_goal.goal_id, "title": new_goal.title}}, 201)

@goals_bp.route("", methods=["GET"])
def all_goals():
    title_query = request.args.get('title')
    order_by_query = request.args.get('sort')
    if title_query:
        goals = Goal.query.filter_by(title = title_query)
    elif order_by_query == 'asc':
        goals = Goal.query.order_by(Goal.title).all()
    elif order_by_query == 'desc':   
        goals = Goal.query.order_by(desc(Goal.title)).all()
    else:
        goals = Goal.query.order_by(Goal.title).all()
    
    goal_response = []
    for goal in goals:
        goal_response.append({'id': goal.goal_id, 'title': goal.title})
    return jsonify(goal_response), 200    

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def one_goal(goal_id):
    goal = Goal.query.get(goal_id) 
    if goal == None:
        abort(404) 
    if request.method == "GET":
        return make_response({"goal": {"id": goal.goal_id, "title": goal.title}}, 200)
    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()

        return make_response({"goal": {"id": goal.goal_id, "title": goal.title}}, 200)
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({'details': 
        f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST", "GET"]) 
def task_and_goal(goal_id):
    request_body = request.get_json()
    tasks = Task.query.all()
    goal = Goal.query.get(goal_id) 
    if goal == None:
        abort(404) 
    if request.method == "POST":
        for task in tasks:
            if task.task_id in request_body["task_ids"]:
                task.goal_id = int(goal_id)
            db.session.commit()
        return make_response({"id": int(goal_id), "task_ids": request_body["task_ids"]}, 200)   
    elif request.method == "GET":
        goals_tasks = Goal.query.get(goal_id).tasks
        
        task_response = []
        for task in goals_tasks:
            is_complete = task.completed_at != None
            task_response.append({'id': task.task_id,
'goal_id': task.goal_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete})
    
        return make_response({"id": goal.goal_id, "title": goal.title, "tasks": task_response}, 200)
