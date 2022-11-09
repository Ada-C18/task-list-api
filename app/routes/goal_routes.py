
from flask import Blueprint, jsonify, request, make_response, abort
from app import db 
from app.models.goal import Goal
from app.models.task import Task
from .routes_helper import validate
from sqlalchemy import func




goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")




@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"},400)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    response = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response)), 201 
   
    

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals= Goal.query.all()

    goal_response = [goal.to_dict() for goal in goals]

  
    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate(Goal,goal_id)

    return {"goal" : goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate(Goal,goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
   

    db.session.commit()

    response = {"goal": goal.to_dict()}
    

  
    return make_response(jsonify(response)), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def get_tasks_for_goal(goal_id):
    goal = validate(Goal, goal_id)

    request_body = request.get_json()
    for tasks_for_goal in request_body["task_ids"]:
        task = validate (Task, tasks_for_goal) 
        goal.tasks.append(task) 

   
    db.session.commit()
  

    task_ids_list = [task.task_id for task in goal.tasks]

    tasks_response = {"id": goal.goal_id, "task_ids":task_ids_list}
    return jsonify(tasks_response), 200



# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_tasks_from_goal(goal_id):
#     goal_
#     goal.to_dict






