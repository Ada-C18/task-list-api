from app import db
from .models.task import Task
from .models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
import sqlalchemy 



task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


# all task methods
    # Create
@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task" : new_task.to_dict()}, 201)
    
    # Read
@task_bp.route("", methods=["GET"])
def get_all_task():
    
    sort_query = request.args.get("sort")
    if sort_query:
        sort_function = getattr(sqlalchemy, sort_query)
        task_list = Task.query.order_by(sort_function(Task.title))
    else:
        task_list = Task.query.all()
    
    response = []    
    for task in task_list:
        response.append(task.to_dict())
    
    return jsonify(response), 200  



# Individual task methods

    # Read
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    
    task = Task.validate_task_id(task_id)
    
    return {"task" : task.to_dict()}, 200

    # Update
@task_bp.route ("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_task_id(task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task" : task.to_dict()}, 200

@task_bp.route("<task_id>/<marker>", methods=["PATCH"])
def mark_task_status(task_id, marker):
    task = Task.validate_task_id(task_id)
    eval("task." + marker + "()")
    
    db.session.commit()

    return {"task" : task.to_dict()}, 200

    # Delete
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details" : f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)


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
    
    goal = Goal.validate_goal_id(goal_id)
    
    return {"goal" : goal.to_dict()}, 200
@goal_bp.route("", methods = ["GET"])
def get_any_goal():
    goal = Goal.query.get(1)
    return{"goal" : goal.to_dict()}, 200

    # Update
@goal_bp.route ("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.validate_task_id(goal_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal" : goal.to_dict()}, 200

# @goal_bp.route("<goal_id>/<marker>", methods=["PATCH"])
# def mark_goal_status(goal_id, marker):
#     goal = Goal.validate_goal_id(goal_id)
#     eval("goal." + marker + "()")
    
#     db.session.commit()

#     return {"goal" : goal.to_dict()}, 200

    # Delete
# @goal_bp.route("/<goal_id>", methods=["DELETE"])
# def delete_goal(goal_id):
#     goal = Goal.validate_goal_id(goal_id)

#     db.session.delete(goal)
#     db.session.commit()
    
#     return make_response({"details" : f"Task {goal_id} \"{goal.title}\" successfully deleted"}, 200)
