from datetime import datetime
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.routes_helper import validate_model, validate_input_data, error_message
from flask import Blueprint, jsonify, make_response, request, abort

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

# read one goal (GET)
@goals_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = validate_model(Goal, id)

    return jsonify({"goal": goal.to_dict()}), 200


@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(id):
    goal = validate_model(Goal, id)
    tasks = [Task.to_dict(task) for task in goal.tasks]

    return make_response({"id": goal.id, "title": goal.title, "tasks": tasks})
     
    
# read all goals (GET)
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)


# create a goal (POST) 
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = validate_input_data(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    request_body = request.get_json()
    goal = validate_model(Goal, id)
    
    task_ids = request_body["task_ids"]

    ####### updating goal.tasks ########
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()
    ###################################

    ######## updating task.goal_id ########
    # task_list = [Task.query.get(task) for task in task_ids]

    # for task in task_list:
    #     task.goal_id = goal.id
    #     db.session.add(task)
    #     db.session.commit()
    
    ###################################

    return make_response({"id": goal.id, "task_ids": task_ids}, 200)


# replace a goal (PUT)
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()
    
    response = {"goal": goal.to_dict()}
    return response


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)

    # saves title before being deleted 
    title = goal.title

    db.session.delete(goal)
    db.session.commit()

    return(make_response({"details": f"Goal {id} \"{title}\" successfully deleted"}), 200)


    
