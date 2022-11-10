from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc #(used in read_all_tasks for sorting)
import requests
import os 
# from slackclient import SlackClient #Alternate method 3 (below to call external api)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
# slack_client = SlackClient(SLACK_TOKEN) #Alternate method 3


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#CREATE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("", methods=["POST"])
def create_task():
        request_body = request.get_json()

        try:
            new_task = Task.from_dict(request_body)
        except KeyError:
            return jsonify ({"details": "Invalid data"}), 400
        
        db.session.add(new_task)
        db.session.commit()
        if new_task.goal_id:
            return jsonify({"task": new_task.to_dict_incl_goal_id()}), 201
        return jsonify({"task": new_task.to_dict()}), 201

#READ Routes (Wave 1: CRUD routes)
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    #(Wave 2: Query param: sort)
    if "sort"in request.args or "SORT" in request.args:
        sort_query_val = request.args.get("sort") if "sort"in request.args else \
            request.args.get("SORT") 

        if sort_query_val.lower() == "asc":
            tasks = Task.query.order_by(Task.title).all()

        elif sort_query_val.lower() == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all() 
            # Source: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending

        else:
            return jsonify({"msg": f"Invalid query value: {sort_query_val}"}), 400

    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    # for task in tasks:
    #     tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def read_task_by_id(task_id): 
    task = validate_model(Task, task_id)
    if task.goal_id is None:
        return jsonify({"task":task.to_dict()}), 200
    return jsonify({"task":task.to_dict_incl_goal_id()}), 200

#Helper function for use in READ route: read_task_by_id and UPDATE route: update_task
def validate_model(cls, id):
    try:
        model_id = int(id)
    except:
        abort(make_response(jsonify({"msg":f"invalid id: {model_id}"}), 400))
    
    chosen_object = cls.query.get(model_id)

    if not chosen_object:
        abort(make_response(jsonify({"msg": f"No {cls.__name__.lower()} found with given id: {model_id}"}), 404))

    return chosen_object

#UPDATE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    if len(request_body) > 2 and request_body["completed_at"]:
        task.completed_at = request_body["completed_at"]

    db.session.commit()

    return jsonify({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False if task.completed_at is None else True
        }}), 200
        
#UPDATE Routes (Wave 3: PATCH Routes)
@tasks_bp.route("/<task_id>/<mark>", methods=["PATCH"])
def update_task_mark_complete_or_incomplete(task_id, mark):
    task = validate_model(Task, task_id)
    
    if mark == "mark_complete":
        task.completed_at = datetime.utcnow().date()
        #Source: https://stackoverflow.com/questions/27587127/how-to-convert-datetime-date-today-to-utc-time
        
        
        channel = "text-notifications"
        message = f"Someone just completed the task {task.title}"
        access_token = SLACK_TOKEN
        my_headers = {'Authorization' : f'Bearer {access_token}'}
        
        #Method 1:
        response = requests.post(f'https://slack.com/api/chat.postMessage', 
            data={"channel": channel,"text": message},
            headers=my_headers,json=True)
        
        #Alternate Method 2:
        #response = requests.post(f'https://slack.com/api/chat.postMessage?channel={channel}&text={message}&pretty=1', headers=my_headers)
        #Source: https://www.nylas.com/blog/use-python-requests-module-rest-apis/
        
        #Alternate Method 3: 
        # channel_id = "C04A2GQ53NF" 
        # send_message(channel_id=channel_id, message=message)
        #Source: https://realpython.com/getting-started-with-the-slack-api-using-python-and-flask/
    
    elif mark == "mark_incomplete":
        task.completed_at = None
    
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

# DELETE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200

#Helper Function to call slack api (Alternate Method 3)
# def send_message(channel_id, message):
#     slack_client.api_call(
#         "chat.postMessage",
#         channel=channel_id,
#         text=message,
#     )
#Source: https://api.slack.com/methods/chat.postMessage/code

