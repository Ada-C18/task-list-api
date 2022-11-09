from flask import Blueprint, jsonify, abort, request, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task




goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# VALIDATE FUNCTION

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))
    
    return obj

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body: 
        return make_response({"details": "Invalid data"
    }, 400)

    new_goal = Goal(
        title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.goal_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goal_list = []
    goals = Goal.query.all()

    for goal in goals:
        goal_list.append(goal.goal_dict())
    
    return jsonify(goal_list)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    return {"goal": goal.goal_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.goal_dict()}), 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_to_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    request_body = request.get_json()
    task_ids = []
    

    for task_id in request_body["task_ids"]:
        task = validate_id(Task, task_id)
        goal.tasks.append(task)
        task_ids.append(task_id)

    db.session.commit()
    
    return {"id": goal.goal_id,
            "task_ids" : task_ids}


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goals(goal_id): 
    goal = validate_id(Goal, goal_id)

    response_body = []
    for task in goal.tasks:
        response_body.append(task.task_dict())

        
    return {"id": goal.goal_id,
        "title": goal.title,
        "tasks": response_body}
    


