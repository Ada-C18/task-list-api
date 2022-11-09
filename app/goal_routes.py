from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app import db


goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
        try:
            model_id=int(model_id)
        except:
            abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
        model =  cls.query.get(model_id)
        if not model:
            abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
        return model
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_data=[goal.to_dict() for goal in goals]

    return jsonify(goals_data)

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return {"goal":goal.to_dict()}

@goal_bp.route("", methods = ["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_goal)
    db.session.commit()
    return {"goal":new_goal.to_dict()}, 201

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    task = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    db.session.commit()
    return {"goal":task.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}),200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def give_tasks_to_a_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
    db.session.commit()
    return make_response({"id": goal.goal_id, "task_ids":request_body["task_ids"]}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_for_a_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_dict = goal.to_dict()
    get_one_task =[task.to_dict() for task in goal.tasks]
    goal_dict["tasks"] = get_one_task
    return goal_dict, 200
    