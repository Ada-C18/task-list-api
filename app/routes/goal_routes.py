from flask import Blueprint, request, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from .task_routes import validate_object, determine_completion
from app.models.task import Task


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
#-------------------------------------------HELPERS----------------------------------

#-------------------------------------------POST----------------------------------
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
        
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()}, 201

@goal_bp.route("/<input_goal_id>/tasks", methods=["POST"])
def send_tasks_to_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)
    request_body = request.get_json()    
    
    for num in request_body["task_ids"]:
        chosen_task = Task.query.get((num))
        chosen_task.goal_id = input_goal_id
    
    db.session.commit()
    print(f"Tasks for goals: {Goal.query.get(1).tasks}")

    return {
        "id": int(input_goal_id),
        "task_ids": request_body["task_ids"]
    }


    

#-------------------------------------------GET----------------------------------
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response  = []
    for goal in goals:
        goal_dict = goal.to_dict()
        response.append(goal_dict)

    return jsonify(response), 200

@goal_bp.route("/<input_goal_id>", methods=["GET"])
def get_one_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)

    return {
        "goal": chosen_goal.to_dict()
}

@goal_bp.route("/<input_goal_id>/tasks", methods=["GET"])
def get_tasks(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)
    
    task_response = []
    for task in chosen_goal.tasks:
        task_dict = task.to_dict_with_goal(determine_completion)
        task_response.append(task_dict)
        
    return {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,
        "tasks": task_response
    }
#-------------------------------------------PUT----------------------------------
@goal_bp.route("/<input_goal_id>", methods=["PUT"])
def update_one_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id) #current goal in db
    request_body = request.get_json() #what client wants to change

    chosen_goal.title = request_body["title"]

    db.session.commit()
    
    return {"goal": chosen_goal.to_dict()}

#-------------------------------------------PATCH----------------------------------

#-------------------------------------------DELETE----------------------------------
@goal_bp.route("/<input_goal_id>", methods=["DELETE"])
def delete_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f"Goal {input_goal_id} \"{chosen_goal.title}\" successfully deleted"
}