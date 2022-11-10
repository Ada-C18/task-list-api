from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import requests



goal_bp = Blueprint("goal_bp", __name__, url_prefix='/goals')

@goal_bp.route("", methods=["POST"])
def create_goal():        
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details":"Invalid data"})),400
    new_goal= Goal(
        title = request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {
                "id": new_goal.goal_id,
                "title": new_goal.title
            }},201

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
            })
    
    return jsonify(goals_response),200

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify(dict(details=f"There is no existing goal {goal_id}")), 404))

    return goal


@goal_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal":{
            "goal_id": goal.goal_id,
            "title": goal.title
            }},200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return make_response(jsonify({f"goal": {
                "id": goal.goal_id,
                "title": goal.title,
            }})),200


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }            

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_list_of_tasks(goal_id): 
    
    request_body = request.get_json()
    task_list = request_body["task_ids"]
    for task_id in task_list:
        task= Task.query.get(task_id)
        task.goal_id = goal_id

    db.session.commit()

    return {
            "id": task.goal_id,
            "task_ids": task_list
            },200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_and_task(goal_id):
    goal = validate_goal(goal_id)
    
    task_list = [] 
    for task in goal.tasks:
            task_list.append({
                "id": task.task_id,
                "goal_id": goal.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })   
        
    response_body= jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    })
        
    return response_body,200            
