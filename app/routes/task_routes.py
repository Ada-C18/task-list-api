from app import db
from pathlib import Path
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.routes_helper import get_record_by_id
from datetime import date
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#Creating Task Blueprint (instantiating new Blueprint instance)
#use it to group routes(endpoints) that start with /tasks
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# Defining Endpoint and Creating Route Function to CREATE a task
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    
    try:
        request_body = request.get_json() #This method "Pythonifies" the JSON HTTP request body by converting it to a Python dictionary
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
            )
    # if missing atribute title, description, or completed_at
    # KeyError
    except KeyError:
        return {"details": "Invalid data"}, 400

    #communicating to the db to collect and commit the changes made in this function
    #saying we want the database to add new_task
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
        }, 201

# Defining Endpoint and Creating Route Function to GET(read) All Tasks
# Task.query.all() is SQLAlchemy syntax that tells Task to query for all() tasks. 
#       This method returns a list of instances of task
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    tasks = Task.query.all() #Not sure if we need this

    # helps the client to search by title and sort
    tasks_sort = request.args.get("sort")
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )

    
    # call the filter from the test ex. asc & desc
    if tasks_sort == "asc":
        sorted_tasks = sorted(tasks_response, key=lambda x: x['title'])
        return jsonify(sorted_tasks)
    elif tasks_sort == "desc":
        reverse_tasks = sorted(tasks_response, key=lambda x: x['title'],reverse=True)
        return jsonify(reverse_tasks)
    else:
        return jsonify(tasks_response)
    

# ------------------- refactored and moved to routes_helper -------------------------------------------
#Creating helper function validate_task to handle errors for get a task by id
# Checks for valid data type (int)
# Checks that id provided exists in records
# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"details": "Invalid data"}, 400))

#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"details":f"there is no existing task {task_id}"}, 404))
        
#     return task
# ------------------- ^^ refactored and moved to routes_helper ^^ -------------------------------------------


# Defining Endpoint and Creating Route Function to GET(read) One Task
#Refactored to define task as return value of helper function validate_task
    #else task = Task.query.get(task_id) how task is defined validate_task without helper function
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_record_by_id(Task, task_id)
    # task = validate_goal(task_id)

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
        }
        } 

  
    if task.goal_id == None:
        pass
    else:
        response["task"]["goal_id"] = task.goal_id
    
    return response



# Defining Endpoint and Creating Route Function to UPDATE a Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_record_by_id(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
        }

# Defining Endpoint and Creating Route Function to DELETE a Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_record_by_id(Task, task_id)
    # task = validate_task(task_id) #old version without refactoring

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }


# create helper to post slack message
def slack_request(title):  
    URL = "https://slack.com/api/chat.postMessage"

    payload={"channel":"slack-bot-test-channel",
            "text": f"Someone just completed the task {title}"}

    headers = {
    "Authorization": os.environ.get('SLACK_TOKEN')
    }

    return requests.post(URL, data=payload, headers=headers) 


# Define Endpoint and Create Route Function to PATCH a Task
# Make complete endpoint variable dyanmic to check if mark_complete or mark_incomplete
# create variable to store value of "is_complete" key
# if mark_complete
    # update completed_at to today's date
    # set is_compelete variable to True
# if mark_incomplete 
    # update completed_at to None
    # set is_compelete variable to False
# Return task_response

@tasks_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def patch_task_complete(task_id,complete):
    task = get_record_by_id(Task, task_id)
    # task = validate_task(task_id)


    if complete == "mark_complete":
        task.completed_at = date.today()
        is_complete = True
        

    elif complete == "mark_incomplete":
        task.completed_at = None
        is_complete = False
        

    db.session.commit()
    task_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
        }

    if is_complete == True:
        slack_request(task.title)

    return make_response(task_response, 200)



