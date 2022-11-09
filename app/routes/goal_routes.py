from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import datetime
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

#CREATE
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

#READ

#UPDATE

#DELETE