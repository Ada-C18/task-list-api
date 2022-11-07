from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os  
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goals(goal_id):
    try:
        goal_id = int(goal_id )
    except:
        abort(make_response({"message":f"{goal_id } invalid"}, 400))

    goal = Goal.query.get(goal_id )

    if not goal:
        abort(make_response({"message":f"goal{goal_id} not found"}, 404))
    
    return goal
