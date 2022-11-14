from flask import Blueprint, abort, jsonify, make_response, request
from app.models.goal_model import Goal
from app.models.task_model import Task
from .helper import get_goal_by_id, get_task_by_id
from app import db

goal_bp = Blueprint('goal_bp', __name__, url_prefix='/goals')

# take a goal and return it as a dictionary
def json_details(goal):
    return {"goal": {
                "id": goal.goal_id,
                "title": goal.title,
            }
        }

# return all goals as json
@goal_bp.route("", methods=["GET"])
def get_goal():
    goals = Goal.query.all()
    response = [{"id": goal.goal_id, "title": goal.title} for goal in goals]
    
    return jsonify(response), 200

# return one goal by id
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_goal_by_id(Goal, goal_id)
    return json_details(goal), 200

# create a new goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()        
    
    try:
        new_goal = Goal(title = request_body["title"])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return json_details(new_goal), 201

# delete a goal by id
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_goal_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200

# update a goal by id
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal = get_goal_by_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return json_details(goal), 200

# add a list of tasks to a goal
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = get_goal_by_id(Goal, goal_id)
    request_body = request.get_json()

    task_goal_id_list = []
    task_to_connect = request_body["task_ids"]
    for task_id in task_to_connect:
        task = get_task_by_id(Task, task_id)
        task.goal_id = goal.goal_id
        task_goal_id_list.append(task_id)
        db.session.commit()
    
    return {
        "id": goal.goal_id,
        "task_ids": task_goal_id_list
    }, 200

# get tasks for one goal
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_and_tasks(goal_id):
    goal = get_goal_by_id(Goal, goal_id)
    
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]
    return goal_dict, 200