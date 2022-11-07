from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from datetime import datetime
import requests
import os

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# validate 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# read all tasks
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    # sort_query = request.args.get("sort")

    # if sort_query == "asc":
    #     tasks = Task.query.order_by(Task.title).all()
    # elif sort_query == "desc":
    #     tasks = Task.query.order_by(Task.title.desc()).all()
    # else:
    goals = Goal.query.all()

    # goals_response = [goal.to_dict() for goal in goals]
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
            "id": goal.goal_id,
            "title": goal.title
            }
        )
    return jsonify(goals_response)

# # read one task
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)

    return { "goal": 
        {
        "id": goal.goal_id,
        "title": goal.title
        }
    }
    # completed = None
    # if not task.completed_at:
    #     completed = False
    # else:
    #     completed = True 
    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": completed }
    #     }

# # create new task
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        return abort(make_response({"details": 'Invalid data'}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return { "goal": 
        {
        "id": new_goal.goal_id,
        "title": new_goal.title
        }
    }, 201
    # completed = None
    # if not new_task.completed_at:
    #     completed = False
    # else:
    #     completed = True 
    # return {
    #     "task": {
    #         "id": new_task.task_id,
    #         "title": new_task.title,
    #         "description": new_task.description,
    #         "is_complete": completed }
    #     }, 201

# # update task
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    # task.description = request_body["description"]

    db.session.commit()
    
#     return task.to_dict_one()
#     # completed = None
#     # if not task.completed_at:
#     #     completed = False
#     # else:
#     #     completed = True 
#     # return {
#     #     "task": {
#     #         "id": task.task_id,
#     #         "title": task.title,
#     #         "description": task.description,
#     #         "is_complete": completed }
#     #     }

# # delete task
# @task_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     task = validate_model(Task, task_id)

#     db.session.delete(task)
#     db.session.commit()

#     return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200)

# # mark complete with patch
# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = validate_model(Task, task_id)
#     # request_body = request.get_json()

#     # then the task is updated, so that its completed_at value is the current date, and I get this response:
#     task.completed_at = datetime.now()

#     db.session.commit()

#     # post message to slack
#     url = 'https://slack.com/api/chat.postMessage'
#     params = {
#         "channel": "task-notifications",
#         "text": f"Someone just completed the task {task.title}"
#     }
#     slack_key = os.environ.get("SLACK_KEY")
#     headers = {
#         "Authorization": f"Bearer {slack_key}"
#     }

#     requests.post(url, params=params, headers=headers)

#     return task.to_dict_one()
#     # completed = None
#     # if not task.completed_at:
#     #     completed = False
#     # else:
#     #     completed = True 
#     # return {
#     #     "task": {
#     #         "id": task.task_id,
#     #         "title": task.title,
#     #         "description": task.description,
#     #         "is_complete": completed }
#     #     }

# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_model(Task, task_id)

#     task.completed_at = None

#     db.session.commit()

#     return task.to_dict_one()