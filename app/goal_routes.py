from app import db
from .models.task import Task
from .models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
import sqlalchemy
from .route_helpers import validate_model_id



goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# all goal methods
    # Create
@goal_bp.route("", methods=["POST"])
def create_goal():
    
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal" : new_goal.to_dict()}, 201)
    
    # Read
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    
    sort_query = request.args.get("sort")
    if sort_query:
        sort_function = getattr(sqlalchemy, sort_query)
        goal_list = Goal.query.order_by(sort_function(Goal.title))
    else:
        goal_list = Goal.query.all()
    
    response = []    
    for goal in goal_list:
        response.append(goal.to_dict())
    
    return jsonify(response), 200  



# Individual goal methods

    # Read
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_specific_goal(goal_id): 
    
    goal = validate_model_id(Goal, goal_id)
    
    return {"goal" : goal.to_dict()}, 200
@goal_bp.route("", methods = ["GET"])
def get_any_goal():
    goal = Goal.query.get(1)
    return{"goal" : goal.to_dict()}, 200

    # Update
@goal_bp.route ("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal" : goal.to_dict()}, 200

@goal_bp.route("<goal_id>/<marker>", methods=["PATCH"])
def mark_goal_status(goal_id, marker):
    goal = validate_model_id(Goal, goal_id)
    eval("goal." + marker + "()")
    
    db.session.commit()

    return {"goal" : goal.to_dict()}, 200

    # Delete
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return make_response({"details" : f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)


# Nested route for task assigned to one goal

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    request_body = request.get_json()

    
    for task in request_body["task_ids"]:
        new_task = Task.validate_task_id(task)
        new_task.goal_id = goal_id
        
    db.session.commit()

    return make_response({
        "id" : goal.id,
        "task_ids" : goal.get_task_ids()
    }, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    response_body = goal.to_dict()
    response_body.update({"tasks" : goal.get_tasks()})

    return make_response(response_body, 200)
