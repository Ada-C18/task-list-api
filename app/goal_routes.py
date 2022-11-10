from flask import abort, Blueprint, jsonify, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes import validate_model
from app import db


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    '''
    POST method - allows client to post goals to the goals record
    '''
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        return make_response({"details": "Invalid data"}, 400)
    
    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response_body), 201)


@goals_bp.route("", methods=["GET"])
def view_all_goals():
    '''
    GET method - allows client to view all goals
    allows client to sort goals alphabetically by title, in ascending and descending order
    '''
    sorted_query = request.args.get("sort")
    if sorted_query:
        if sorted_query == "asc":
            all_goals = Goal.query.order_by(Goal.title.asc()).all()
        
        elif sorted_query == "desc":
            all_goals = Goal.query.order_by(Goal.title.desc()).all()

    else:
        all_goals = Goal.query.all()

    request_body = []
    for goal in all_goals:
        request_body.append(goal.to_dict())

    return jsonify(request_body), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def view_one_goal(goal_id):
    '''
    GET method - allows client to view one goal by ID
    '''
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    '''
    PUT method - allows user to update one goal record
    '''
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    '''
    DELETE method - allows user to remove specified goal record
    '''
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}


#### GOALS -< TASKS ####

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    '''
    POST method - return task IDs for one goal
    '''
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal = goal
        task.goal_id = goal_id

        db.session.commit()


    return jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def view_one_goal_tasks(goal_id):
    '''
    GET method - allows client to view one goals tasks by ID
    '''
    goal = validate_model(Goal, goal_id)
    tasks = goal.get_task_list()

    dict = goal.to_dict()
    dict["tasks"] = tasks

    return dict