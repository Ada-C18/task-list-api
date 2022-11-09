import datetime, os, requests
from .routes import validate_model
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from dotenv import load_dotenv

load_dotenv()

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')



@goals_bp.route("", methods=["GET"])
def read_all_goals():
    title_query = request.args.get('title')

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
        
    if not title_query:
        goals = Goal.query.all()
    goals_response = [goal.goal_to_dict() for goal in goals]
    return jsonify(goals_response)


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not request_body:
        return {"details": "Invalid data"}, 400
    new_goal= Goal(title=request_body['title'])

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({'goal': new_goal.goal_to_dict()}), 201)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({'goal': goal.goal_to_dict()})

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({'goal': goal.goal_to_dict()})


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}))

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_ids(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.tasks = [Task.query.get(task_id) for task_id in request_body['task_ids']]

    db.session.commit()
    return make_response(jsonify({'id': goal.goal_id, 'task_ids': [ task.task_id for task in goal.tasks]}))


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_ids(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    

    db.session.commit()
    return make_response(jsonify(goal.goal_to_dict(tasks=True)))


@goals_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task_info(task_id):

    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    db.session.commit()
    return make_response(jsonify({'task': task.to_dict(goal=True)}))