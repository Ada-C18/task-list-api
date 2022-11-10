from datetime import datetime
from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
import requests, os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# helper function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task id: {task_id} must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task:
        abort(make_response(jsonify({"message": f"The {task_id} is not found"}), 404))

    return matching_task



# Create a Task: Valid Task With null completed_at
@task_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()

    # If add "is_complete" not in respnse_body
    # in postman it return 500. 
    # Haven't solve the problem, so I take out that line
    if "title" not in response_body or\
       "description" not in response_body:
       # "is_complete" not in respnse_body
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = response_body["title"],
        description = response_body["description"],
        # completed_at = response_body["is_complete"]
    )
       
    db.session.add(new_task)
    db.session.commit()

    # using the class method in task.py 
    return jsonify({"task":new_task.return_body()}), 201


# Get Tasks: Getting Saved Tasks, sorting by ascending/descending
@task_bp.route("", methods=["GET"])
def read_task():
    # tasks = Task.query.all()
    
    # read_task_result = []
    # # for task in tasks:
    # #     read_task_result.append(task.return_body())
    # read_task_result = [task.return_body() for task in tasks]
    # return jsonify(read_task_result), 200
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    response = [task.return_body() for task in tasks]
    return jsonify(response), 200   



# Get One Task: One Saved Task
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    chosen_task = validate_task(task_id)

    return jsonify({"task":chosen_task.return_body()}), 200


# Update Task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # after update the task, it becomes to the last one
    # id order: 2341
    chosen_task = validate_task(task_id)
    request_body = request.get_json()

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200

    

# Deleting a Task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    # mistakes in the return sentence trapped me for some time 
    return jsonify({"details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'}), 200

  
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_update(task_id):
    chosen_task = validate_task(task_id)
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = datetime.now()
    db.session.commit()
    
    PATH = "https://slack.com/api/chat.postMessage"
    
    SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")

    # the query parameters come from the 
    query_params = {
        "token": SLACKBOT_TOKEN,
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url=PATH, data=query_params, headers={"Authorization": SLACKBOT_TOKEN})
    # using json=query_params connot connect to the slack
    # POST: to submit data to be processed to the server.
    
    return jsonify({"task":chosen_task.return_body()}), 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_update(task_id):
    chosen_task = validate_task(task_id)
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = None
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200
    

# helper function to check the value of completed_at
# def check_complete_status(goal_id, result):
#     chosen_task = validate_task(goal_id)
#     task = Task.query.get(goal_id)
#     if task is None:
#         return make_response("The task was not found", 404)
#     task.complete_at = result
#     db.session.commit()
#     return jsonify({"task":chosen_task.return_body()}), 200




# ===============================================================
# Goal Routes

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response_str = f"Invalid task id: {goal_id} must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_goal = Goal.query.get(goal_id)

    if not matching_goal:
        abort(make_response(jsonify({"message": f"The {goal_id} is not found"}), 404))

    return matching_goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    response_body = request.get_json()

    if "title" not in response_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(
        title = response_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.return_body()}), 201


# Get Goals: Getting Saved Goals
@goal_bp.route("", methods=["GET"])
def read_goal():
    goals = Goal.query.all()
    response = [goal.return_body() for goal in goals]
    return jsonify(response), 200   


#Get One Goal: One Saved Goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    chosen_goal= validate_goal(goal_id)
    return jsonify({"goal":chosen_goal.return_body()}), 200


# Update Goal
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # after update the task, it becomes to the last one
    # id order: 2341
    chosen_task = validate_task(task_id)
    request_body = request.get_json()

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200