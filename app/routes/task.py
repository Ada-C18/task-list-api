from flask import Blueprint, json, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import date 
import requests

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()   
    #print(request_body)
    try:
        new_task= Task(title=request_body['title'],
                    description=request_body['description'],
                    #completed_at=request_body['completed_at']
                    completed_at=request_body.get('completed_at') # ".get" vs "[]" return None instead of error
                    )
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 
    #print(request_body)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_response()), 201

'''
# GET route with query param, option 1
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    result = []
    for item in tasks:
        result.append(item.to_dict()) 
    #tasks is List - why I can't sort when placing them after   
    sort_query = request.args.get("sort") #sort is the key
    # for ascending sorting
    if sort_query == "asc":
        result = sorted(result, key=lambda t:t['title'])
    # for descending sorting
    elif sort_query == "desc":
        result = sorted(result, key=lambda t:t['title'], reverse=True)
    return jsonify(result), 200
'''

# GET route with query param, option 2: order_by query function 
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    list_of_task_objects = []
    sort_query = request.args.get("sort") 
    # for ascending sorting
    if sort_query == "asc":
        list_of_task_objects = Task.query.order_by(Task.title.asc()).all()             
    # for descending sorting
    else:
        list_of_task_objects = Task.query.order_by(Task.title.desc()).all() 
    #result at this point is list of object
    result = []  
    for item in list_of_task_objects:
        result.append(item.to_dict())
    return jsonify(result), 200


# GET route for one task
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify(chosen_task.to_response()), 200

# PUT route for one task
@task_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):  
    update_task = get_task_from_id(task_id)
    request_body = request.get_json()   
    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
        update_task.is_complete = request_body.get('completed_at')   
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    db.session.commit()
    return jsonify(update_task.to_response()), 200


#/tasks/1/mark_complete and added API
path = "https://slack.com/api/chat.postMessage"
API_KEY = "Bearer xoxb-3831949166102-4330548743939-M7VwemzW4oIcUOjzx0JLQ9El"

@task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_task_slack(task_id):
    mark_complete_task = get_task_from_id(task_id)
    mark_complete_task.completed_at = date.today() 
    if mark_complete_task:
        query_params = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {mark_complete_task.title}",
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
    db.session.commit()
    return jsonify(mark_complete_task.to_response()), 200


'''
#/tasks/1/mark_complete
@task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_task(task_id):  
    mark_complete_task = get_task_from_id(task_id)
    mark_complete_task.completed_at = date.today()    
    db.session.commit()
    return jsonify(mark_complete_task.to_response()), 200
'''


#/tasks/1/mark_incomplete
@task_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete_task(task_id):  
    mark_incomplete_task = get_task_from_id(task_id)
    mark_incomplete_task.completed_at = None    
    db.session.commit()
    return jsonify(mark_incomplete_task.to_response()), 200



# DELETE route for one task
@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({"details": f"Task {task_to_delete.task_id} \"{task_to_delete.title}\" successfully deleted"}), 200    

# helper
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        # abort: stop looking for unfound; make_response: route decorate 
        return abort(make_response({"msg": f"invalid data type: {task_id}"}, 400))
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        return abort(make_response("", 404))  
    return chosen_task
