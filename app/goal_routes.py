from app.models.task import Task
from app.models.goal import Goal
from app.helper_functions import *
from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from datetime import date
import requests
import os
from dotenv import load_dotenv

# Functions are grouped by endpoint, method routing logic (eg GET vs POST) is handled within the function
# I consider this to be DRYer and more RESTful

load_dotenv()

# Blueprints
goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")


# Routes
@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():
    if request.method == "POST":
        goal = Goal.from_dict(request.get_json())
        
        if goal == False:
            return make_response({"details": "Invalid data"}, 400)
        
        db.session.add(goal)
        db.session.commit()
        db.session.refresh(goal)
        goal = goal.to_dict()
        response = {"goal":goal}
        return make_response(response,201)

    elif request.method == "GET":
        goals = Goal.query.all()
        response_body = [goal.to_dict() for goal in goals]
        return make_response(jsonify(response_body), 200)

@goals_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_individual_goal(id):
    goal = validate_id(Goal, id)
    if request.method == "GET":
        return make_response({"goal":goal.to_dict()}, 200)

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)
    
    elif request.method == "PUT":
        goal.title = request.get_json()["title"]
        db.session.commit()

        return make_response({"goal":goal.to_dict()}, 200)

@goals_bp.route("/<id>/tasks", methods=["POST", "GET"])
def goals_and_tasks(id):
    goal = validate_id(Goal, id)
    if request.method == "POST":
        task_ids = request.get_json()["task_ids"]
        for id in task_ids:
            task = validate_id(Task, id)
            task.goal = goal
            db.session.commit()
        return make_response(jsonify({"id":goal.goal_id, "task_ids":task_ids}), 200)
    elif request.method == "GET":
        response = goal.to_dict()
        response["tasks"] = [task.to_dict() for task in goal.tasks]
        return make_response(jsonify(response), 200)

