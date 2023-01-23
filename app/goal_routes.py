from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_complete_request(request_body):
    try:
        if request_body["title"]:
            return request_body

    except:
        abort(make_response({"details": "Invalid data"}, 400))


def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    valid_data = validate_complete_request(request_body)
    new_goal = Goal.from_dict(valid_data)

    db.session.add(new_goal)
    db.session.commit()

    goal_response = {
        "goal": new_goal.to_dict()
    }
    return make_response(jsonify(goal_response), 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals_sort_asc():
    goal_query = Goal.query.all()
    title_query = request.args.get("title")
    if title_query:
        goal_query = Goal.query.filter_by(title=title_query)

    goals = goal_query

    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def goal_update_entire_entry(goal_id):
    goal = validate_model_id(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response((goal_response), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def goal_delete(goal_id):
    goal = validate_model_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal.id} "{goal.title}" successfully deleted'}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model_id(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()

    goal_response = {
        "id": goal.id,
        "task_ids": request_body["task_ids"]
    }
    

    return make_response(jsonify(goal_response), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_with_tasks(goal_id):
    goal = validate_model_id(Goal, goal_id)

    tasks = []
    for task in goal.tasks:
        tasks.append(
        {
            "id": task.id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    )

    goal_response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }

    return make_response(jsonify(goal_response), 200)

@goals_bp.route("<goal_id>/tasks/<task_id>", methods=["GET"])
def get_one_task(goal_id, task_id):
    goal = validate_model_id(Goal, goal_id)
    task = validate_model_id(Task, task_id)

    task_response = []
    for task in goal.tasks:
        task_response.append(
            {
                "task": {
                    "id": task.id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False
                }
            }
        )

    return make_response(jsonify(task_response), 200)
