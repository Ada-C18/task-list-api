from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from .task_routes import validate_model
import requests
import os


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if (("title") not in request_body):
        return make_response({"title": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    
    goal_response = Goal.query.get(1)
    return make_response({"goal": goal_response.to_dict()}, 201)