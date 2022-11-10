from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal) # track this object
    db.session.commit() # any changes that are pending commit those changes as data written in SQL
    return make_response(jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title,
        }
    }), 201)


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title
            }
        )

    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)
    return make_response(jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_model = get_validate_model(Goal, goal_id)

    request_body = request.get_json()

    if not goal_model: 
        return make_response({"message":f"Goal {goal_model} not found"}, 404)  

    goal_model.title = request_body["title"]

    db.session.commit()

    return make_response({
        "goal": {
            "id": goal_model.goal_id,
            "title": goal_model.title
        }
    }, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    task = get_validate_model(Goal, goal_id)

    goal_model = Goal.query.get(goal_id)

    if not goal_model: 
        return make_response({"message":f"Task {goal_id} not found"}, 404)  

    db.session.delete(goal_model)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal_model.title}" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def sending_list_of_task_ids_to_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    goal.tasks = []
    for task_id in task_ids:
        goal.tasks.append(Task.query.get(task_id))
    
    db.session.commit() # any changes that are pending commit those changes as data written in SQL

    return make_response(jsonify({
            "id": goal.goal_id,
            "task_ids": task_ids
    }), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_list_of_tasks_by_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)
    print('HELLO!!!!!!!')
    tasks_list = []
    for task in goal.tasks:
        # task_dict = {}
        # task_dict["id"] = task.task_id
        # task_dict["title"] = task.title
        # task_dict["description"] = task.description
        # task_dict["is_complete"] = False
        # tasks_list.append(task_dict)
        tasks_list.append(
            {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
        
    # db.session.commit() # any changes that are pending commit those changes as data written in SQL

    return make_response(jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_list
        }), 200)
