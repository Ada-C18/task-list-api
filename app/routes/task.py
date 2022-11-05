

from app import db
from flask import Blueprint,jsonify,request,abort,make_response
from app.models.task import Task
import os,requests
from datetime import datetime
   


task_bp = Blueprint("task",__name__,url_prefix = "/tasks")

@task_bp.route('',methods =['POST']) 
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title = request_body['title'],
            description = request_body['description'],
            # completed_at = request_body['completed_at']
        )
    except:
        return abort(make_response({"details": "Invalid data"},400))
        
          

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}),201)


@task_bp.route('',methods = ["GET"])
def get_all_tasks():
    query_value = request.args.get("sort")

    if query_value == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif query_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()      
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())

    return make_response(jsonify(response),200) 


@task_bp.route('/<task_id>', methods = ["GET"])
def get_one_task(task_id):

    chosen_task = get_task_from_id(task_id)

    return make_response(jsonify({"task":chosen_task.to_dict()}),200)


@task_bp.route('/<task_id>', methods = ["PUT"])
def update_task(task_id):
    update_task = get_task_from_id(task_id)

    request_body = request.get_json()
    
    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
       
    except KeyError:
        return jsonify({'msg':"Missing needed data"}),400

    db.session.commit()

    return make_response(jsonify({"task": update_task.to_dict()}),200)
    

@task_bp.route('/<task_id>', methods = ["DELETE"])
def delete_one_task(task_id):
    task = get_task_from_id(task_id)

    # request_body = request.get_json()
    
   
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}),200)


def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:  
        return abort(make_response({"msg":f"Invalid data type: {task_id}"}, 400 ))

    chosen_task = Task.query.get(task_id)
    
    if chosen_task is None:
        return abort(make_response({"msg": f" Could not find task item with id : {task_id}"} , 404 ))
            
    return chosen_task    


@task_bp.route('/<task_id>/mark_complete', methods =['PATCH'])
def mark_complete(task_id):
    task= get_task_from_id(task_id)

    task.completed_at = datetime.utcnow()
 
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    slack_api_key = os.environ.get("SLACK_TOKEN")

    request_headers = {"Authorization": f"Bearer {slack_api_key}"}
    request_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"

    }

    requests.post(path, headers=request_headers,json=request_body)

    return jsonify({'task':task.to_dict()}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods =['PATCH'])
def mark_incomplete(task_id):
    task= get_task_from_id(task_id)

    task.completed_at = None
    
    db.session.commit()
    
    return jsonify({'task':task.to_dict()}), 200    





