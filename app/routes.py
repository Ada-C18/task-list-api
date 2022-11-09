from flask import Blueprint, jsonify, request, abort, make_response
from sqlalchemy import desc
from app import db
from app.models.task import Task
from app.models.helper import get_one_obj_or_abort
from datetime import datetime
from app.slackClient import SlackClient
from app.models.goal import Goal

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
slackClient = SlackClient()

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_request_dict(request_body)
    if new_task.title is None or new_task.description is None:
        response_str = f"Invalid data"
        abort(make_response(jsonify({"details":response_str}), 400))

    db.session.add(new_task)
    db.session.commit()

    task_dict = new_task.to_response_dict()
    response_body = {
        "task": task_dict
    }

    response = make_response(jsonify(response_body), 201)
    return response

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_type = request.args.get("sort")

    if sort_type is None: 
        tasks = Task.query.all() 
    elif sort_type == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    elif sort_type == "asc":
        tasks = Task.query.order_by(Task.title).all()

    response = [task.to_response_dict() for task in tasks]
    
    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    task_dict = chosen_task.to_response_dict()
    response_body = {
        "task": task_dict
    }

    return make_response(jsonify(response_body), 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_with_new_vals(task_id):

    chosen_task = get_one_obj_or_abort(Task, task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
    "description" not in request_body:
        return jsonify({"message":"Request must include title and description."}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    db.session.commit()

    task_dict = chosen_task.to_response_dict()
    response_body = {
        "task": task_dict
    }

    return make_response(jsonify(response_body), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{chosen_task.title}\" successfully deleted"}), 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    current_date = datetime.now()

    chosen_task.completed_at = current_date
    db.session.commit()

    message=f"Someone just completed the task {chosen_task.title}"
    slackClient.post_message_to_my_channel(message)

    task_dict = chosen_task.to_response_dict()
    response_body = {
        "task": task_dict
    }

    response = make_response(jsonify(response_body), 200)
    return response

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    chosen_task.completed_at = None
    db.session.commit()

    # message = f"Someone just marked the task {chosen_task.title} incomplete"
    # slackClient.post_message_to_my_channel(message)

    task_dict = chosen_task.to_response_dict()
    response_body = {
        "task": task_dict
    }

    response = make_response(jsonify(response_body), 200)
    return response

# goal

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    new_goal = Goal.from_request_dict(request_body)

    if new_goal.title is None:
        response_str = f"Invalid data"
        abort(make_response(jsonify({"details":response_str}), 400))

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = new_goal.to_response_dict()
    response_body = {
        "goal": goal_dict
    }

    response = make_response(jsonify(response_body), 201)
    return response

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    name_param = request.args.get("title")

    if name_param is None:
        goals = Goal.query.all()
    else:
        goals = Goal.query.filter_by(title=name_param)

    response = [goal.to_response_dict() for goal in goals]

    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    goal_dict = chosen_goal.to_response_dict()
    response_body = {
        "goal": goal_dict
    }

    return make_response(jsonify(response_body), 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_with_new_vals(goal_id):

    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"message":"Request must include title."}), 400

    chosen_goal.title = request_body["title"]

    db.session.commit()

    goal_dict = chosen_goal.to_response_dict()
    response_body = {
        "goal": goal_dict
    }

    return make_response(jsonify(response_body), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_task = get_one_obj_or_abort(Goal, goal_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal_id} \"{chosen_task.title}\" successfully deleted"}), 200)

# @goal_bp.route("/<goal_id>/task", methods=["POST"])
# def post_task_belonging_to_a_goal(goal_id):
#     parent_goal = get_one_obj_or_abort(Goal, goal_id)

#     request_body = request.get_json()

#     new_task = Task.from_request_dict(request_body)
#     new_task.goal = parent_goal

#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify({f"{new_task.task_id}"}), 201



# @goal_bp.route("/<goal_id>/task", methods=["GET"])
# def get_all_tasks_belonging_to_a_goal(goal_id):
#     goal = get_one_obj_or_abort(Goal, goal_id)

#     tasks_response = [task.to_response_dict() for task in goal.tasks]

#     return jsonify(tasks_response), 200





