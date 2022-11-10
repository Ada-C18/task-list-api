from app import db
from app.models.goal import Goal
from flask import Blueprint,jsonify,abort,make_response,request
from sqlalchemy import desc
from sqlalchemy import asc
from datetime import datetime
import os
from dotenv import load_dotenv
import requests


goals_bp=Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("",methods=["GET"])
def handle_goals_data():
    goals_response = []
    title_query=request.args.get("title")

    sort_query=request.args.get("sort")
    if title_query:
        goals=Goal.query.filter_by(title=title_query)
    elif sort_query=="desc":
        goals=Goal.query.order_by(goal.title.desc()).all()
    elif sort_query=="asc":
        goals=Goal.query.order_by(goal.title.asc()).all()
    else:
        goals=Goal.query.all()
    
    for goal in goals:
        
        goals_response.append({
            "id": goal.id,
            "title": goal.title,
            
        })
    return jsonify(goals_response),200

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    goal=Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))
    return goal 


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    
    goal =validate_goal(goal_id)
    return jsonify({'goal':{
        "id": goal.id,
        "title": goal.title,
        
    }})

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal=Goal.from_dictg(request_body)
    except KeyError:
        if "title" not in request_body:
            return make_response({"details": "Invalid data"},400)

    new_goal =Goal.from_dictg(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response(jsonify({"goal":new_goal.to_dictg()}),201)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal":goal.to_dictg()}),200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal= validate_goal(goal_id)

    db.session.delete(goal)

    db.session.commit()
    

    return {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}