from app import db
from flask import abort, Blueprint, jsonify, make_response, request
from app.models.goal import Goal
from app.models.task import Task



goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

#==============================
#       HELPER FUNCTIONS
#==============================
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model: 
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


#==============================
#         CREATE GOAL
#==============================
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal.new_instance_from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_response = {"goal": new_goal.create_dict()}

    return make_response(jsonify(goal_response), 201)

#==============================
#      CREATE GOAL TASKS
#==============================
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal = goal
    db.session.commit()

    goal_response = {"id": goal.goal_id,
                        "task_ids": request_body["task_ids"]}

    return make_response(jsonify(goal_response), 200)

#==============================
#        READ ALL GOALS
#==============================
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")

    if sort_query=="asc":
        goals=Goal.query.order_by(Goal.title.asc())
    elif sort_query=="desc":
        goals=Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
        
    goals_response = [goal.create_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200)

#==============================
#        READ ONE GOAL
#==============================
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_response = {"goal": goal.create_dict()}
    return make_response(jsonify(goal_response), 200)

#==============================
#         UPDATE GOAL
#==============================
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()

    goal_response = {"goal": goal.create_dict()}
    return make_response(jsonify(goal_response), 200)

#==============================
#         DELETE GOAL
#==============================
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    goal_response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
    return make_response(jsonify(goal_response), 200)