# from flask import Blueprint, jsonify, request
# from app import db
# from .routes_helper import validate_id, validate_input
# from app.models.goal import Goal
# from app.models.task import Task

# goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# @goal_bp.route("", methods=["POST"])
# def create_new_goal():
#     request_body = request.get_json()

#     validate_input(Goal, request_body)
#     goal = Goal.from_dict(request_body)

#     db.session.add(goal)
#     db.session.commit()

#     return jsonify({"goal": goal.to_dict()}), 201

# @goal_bp.route("", methods=["GET"])
# def get_all_goals():
#     goals = Goal.query.all()

#     all_goals = []
#     for goal in goals:
#         all_goals.append(goal.to_dict())
#     return jsonify(all_goals), 200

# @goal_bp.route("/<goal_id>", methods=["GET"])
# def get_one_goal_by_id(goal_id):
#     goal = validate_id(Goal, goal_id)

#     return jsonify({"goal": goal.to_dict()}), 200

# @goal_bp.route("/<goal_id>", methods=["PUT"])
# def update_one_goal(goal_id):
#     goal = validate_id(Goal, goal_id)
#     request_body = request.get_json()

#     goal.title = request_body["title"]
#     db.session.commit()

#     return jsonify({"goal": goal.to_dict()}), 200

# @goal_bp.route("/<goal_id>", methods=["DELETE"])
# def delete_one_goal(goal_id):
#     goal = validate_id(Goal, goal_id)
    
#     db.session.delete(goal)
#     db.session.commit()

#     return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}

# @goal_bp.route("/<goal_id>/tasks", methods=["POST"])
# def assign_task_to_goal(goal_id):
#     goal = validate_id(Goal, goal_id)
#     request_body = request.get_json()
    
#     tasks = [validate_id(Task, task_id) for task_id in request_body["task_ids"]]
#     for task in tasks:
#         task.goal_id = goal_id
#         db.session.commit()
    
#     # for task_id in task_ids:
#     #     task = validate_id(Task, task_id)
#     #     task.goal_id = goal_id
    
#     response = {
#         "id": int(goal_id), 
#         "task_ids": [task.task_id for task in goal.tasks]
#     }

#     return jsonify(response),200

# @goal_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_tasks_from_goal(goal_id):
#     goal = validate_id(Goal, goal_id)

#     response = {
#         "id": goal.goal_id, 
#         "title": goal.title,
#         "tasks": [task.to_dict_goal_id() for task in goal.tasks] 
#     }

#     return jsonify(response), 200
    