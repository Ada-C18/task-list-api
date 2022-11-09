from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
load_dotenv()


bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message" : f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message" : f"{cls.__name__} {model_id} not found"}, 404))

    return model



@bp.route("", methods=["POST"])
def create_a_task():
    try: 
        request_body = request.get_json()

        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify({
                "task": Task.to_dict(new_task)})), 201
    except:
        abort(make_response({"details": "Invalid data"}, 400))   

@goal_bp.route("", methods=["POST"])
def create_a_goal():
    try: 
        request_body = request.get_json()

        new_goal = Goal.from_dict(request_body)
        db.session.add(new_goal)
        db.session.commit()

        return make_response(jsonify({
                "goal": Goal.to_dict(new_goal)})), 201
    except:
        abort(make_response({"details": "Invalid data"}, 400))



@bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    sort_query = request.args.get("sort")
    if sort_query=="desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.order_by(Task.title.asc())
    
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)



@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)







@bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(jsonify({
        "task": Task.to_dict(task)})), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(jsonify({
        "goal": Goal.to_dict(goal)})), 200


@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({
        "task": Task.to_dict(task)})), 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    goal.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({
        "goal": Goal.to_dict(goal)})), 200

@bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details" : f"Task {task_id} \"{task.title}\" successfully deleted"}))


@goal_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
        "details" : f"Goal {goal_id} \"{goal.title}\" successfully deleted"}))


def use_slack_bot(task):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("API_KEY")
    
    query_params = {
        "channel": "#task-notifications",
        "text" : f"Someone just completed the task {task.title}"
        }

    requests.post(PATH, params=query_params, headers={
        "Authorization": SLACK_API_KEY
    })

@bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incompleted_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()
    use_slack_bot(task)
    return {"task":task.to_dict()}, 200

    




@bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_completed_task(task_id):
    try:
        task = validate_model(Task, task_id)
        task.completed_at = None

        db.session.commit()

        return make_response(jsonify({
            "task": Task.to_dict(task)}))
    except:
        abort(make_response({"message" : f"task {task_id} not found"}, 404))

@bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_completed_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    task.is_complete = True
    task_dict = task.to_dict()

    db.session.commit()

    return make_response(jsonify({
        "task": task_dict}))

@bp.route("<task_id>/mark_incomplete", methods=["PATCH"])

def mark_incomplete_on_incompleted_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({
        "task": Task.to_dict(task)}))


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_list_of_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.tasks = []

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)


    # db.session.add()
    db.session.commit()

    return make_response(jsonify({
        "id" : goal.goal_id,
        "task_ids" : request_body["task_ids"]
    })), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])

def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    all_tasks = []

    tasks = goal.tasks

    for task in tasks:
        all_tasks.append({
            "id" : task.task_id,
            "goal_id" : task.goal_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : task.is_complete
        })

    return jsonify({
        "id" : goal.goal_id,
        "title" : goal.title,
        "tasks" : all_tasks
    }), 200





