
from flask import Blueprint, jsonify, request, make_response
from app import db 
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import datetime
import os
import requests
from .routes_helper import validate 



tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"},400)
         
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    
    response = {"task": new_task.to_dict()}

    return jsonify(response), 201 
   

@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():

    title_query = request.args.get("sort")
    
    if title_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))       
    elif title_query == "asc": 
        tasks = Task.query.order_by(asc(Task.title))
    else:
        tasks = Task.query.all()

    task_response = [task.to_dict() for task in tasks]

    return jsonify(task_response), 200



@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate(Task,task_id)

    if task.goal_id is not None:
        return {"task": task.to_dict(include_join = True)}, 200
       
    return {"task" : task.to_dict()}, 200
  

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {"task": task.to_dict()}
    

  
    return jsonify(response), 200



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) 
def update_task_is_complete(task_id):
    task = validate(Task,task_id)
    

    task.completed_at=datetime.utcnow() 
   
    response = {"task": task.to_dict()}
    
 
    db.session.commit()

   
    SLACK_TOKEN =os.environ.get('SLACK_API_KEY')
    requests.post("https://slack.com/api/chat.postMessage", json = {"channel": "task-notifications", "text": f"Someone just completed the task {task.title}"}, headers = {"Authorization": SLACK_TOKEN})

    if task.completed_at:
        return jsonify(response), 200
    
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) 
def mark_incomplete(task_id):
    task = validate(Task,task_id)

  
    task.completed_at = None


    response = {"task": task.to_dict()}
   
    db.session.commit()
       
    return jsonify(response), 200



    
    
    
    

    



