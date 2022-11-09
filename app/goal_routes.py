from app import db
from .models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes import validate_tasks


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goals(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid."}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found."}, 404))
    
    return goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        
        new_goal = Goal(
            title=request_body["title"]
            )
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goal_param = request.args
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goals(goal_id)
    return jsonify({"goal":goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goals(goal_id)
    title = request.json.get("title") 
    
    if not title:
        return jsonify({"details": "Invalid data"}), 400

    goal.title = title
    db.session.commit()
    
    return jsonify(goal.to_dict()), 200
    

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goals(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_goal_belonging_to_tasks(goal_id):
    goal = validate_goals(goal_id)

    request_body = request.get_json()
    task_list = []
    
    for task_id in request_body["task_ids"]:
        task = validate_tasks(task_id)
        task.goal = goal

        task_list.append(task_id)

    db.session.commit()

    return jsonify({
        "id": goal.goal_id,
        "task_ids": task_list
        }), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_goals(goal_id)

    tasks_dict = [task.to_dict() for task in goal.tasks]

    result = goal.to_dict()
    result["tasks"] = tasks_dict

    return jsonify(result), 200

