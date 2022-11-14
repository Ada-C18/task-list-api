from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.helper_routes import get_one_obj_or_abort

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
#--------------------------------POST-------------------------------
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(title = request_body["title"])
    

    db.session.add(new_goal)
    db.session.commit()


    return jsonify({"goal": new_goal.to_dict()}), 201

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_a_task_to_goal(goal_id):
    request_body = request.get_json()
  
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    list_of_chosen_tasks = [get_one_obj_or_abort(Task, task_id) for task_id in request_body["task_ids"]] 
    # for task_id in request_body["task_ids"]:
    #     chosen_task = get_one_obj_or_abort(Task, task_id)
    #     list_of_chosen_tasks.append(chosen_task)

    chosen_goal.tasks = list_of_chosen_tasks

    db.session.commit()

    return jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200


#--------------------------------GET-------------------------------
@goal_bp.route("", methods=["GET"])
def get_all_saved_goals():
    goals = Goal.query.all()

    response = []
    for goal in goals:
        goal_dict = {
                "id": goal.goal_id,
                "title": goal.title,
            }
        response.append(goal_dict)
    
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_saved_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    goal = {"id": chosen_goal.goal_id, "title": chosen_goal.title}
    return jsonify({"goal": goal}), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    #tasks = Task.query.filter_by(goal_id=goal_id)
    list_of_tasks = [task.to_dict() for task in chosen_goal.tasks]
    #list_of_tasks = [task.to_dict() for task in tasks]
    # list_of_tasks = []
    # for task in tasks:
    #     task_dict = {
    #         "id": task.id,
    #         "title": task.title,
    #         "description": task.description,
    #         "goal_id": int(goal_id),
    #         "is_complete": task.is_complete

    #     }
        # list_of_tasks.append(task_dict)

    chosen_goal_dict = {
    "id":chosen_goal.goal_id,
    "title":chosen_goal.title,
    "tasks": list_of_tasks
    }

    return jsonify(chosen_goal_dict), 200

#--------------------------------PUT-------------------------------
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    request_body = request.get_json()
    
    chosen_goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": chosen_goal.to_dict()}), 200

#---------------------------------------DELETE------------------------------------------------
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_task(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'}), 200



