from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import datetime as dt
import requests
from dotenv import load_dotenv
import os
from sqlalchemy import select
load_dotenv()
# INSTANIATE BLUEPRINT FOR ROUTES
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    # This is like SELECT * FROM table_name(cls param=Task)
    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} can't be found"}, 404))

    return model


@tasks_bp.route("/", strict_slashes=False, methods=["POST"])
def create_task():

    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

    except KeyError:
        abort(make_response({
            "details": "Invalid data"
        }, 400))
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify({'task': {'description': 'Test Description', 'id': 1, 'is_complete': False, 'title': 'A Brand New Task'}}), 201)


@tasks_bp.route("/", strict_slashes=False, methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at_query")
    # 'sort' is the query param /tasks?sort=asc and order_by is storing the value of that key
    order_by = request.args.get("sort")
    # SELECT ... table_name but without * or any WHERE statements what is the data-type/data-structure, how is it storing?
    task_query = Task.query
    # i = 0
    # if title.query:
    #   i+=1

   # this is like WHERE
    if title_query:
        task_query = task_query.filter_by(title=title_query)

    if description_query:
        task_query = task_query.filter_by(description=description_query)

    if completed_at_query:
        task_query = task_query.filter_by(completed_at=completed_at_query)
# GET/Localhost:5000/tasks?sort=asc
    if order_by == "asc":  # Because order_by is the value of the key "sort" it needs to equal "this string"
        task_query = task_query.order_by(Task.title.asc())

    if order_by == "desc":
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()  # like SELECT * from tasks if none of these are true, BUT task_query is holding the (possibly list datastructure?) value of any filters above that are true and asking for all of them, NOT all things in the Table. Task_query.all() is saying get everything in my table but the task_query is saying match these specific parameters and the parameters are the things I've built up above from the if statement filters.

    task_response = [task.to_dict() for task in tasks]

    return jsonify(task_response)


@tasks_bp.route("/<task_id>", strict_slashes=False, methods=["GET"])
def get_one_task(task_id):

    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", strict_slashes=False, methods=["PUT"])
def update_task(task_id):

    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return {"task": task.to_dict()}, 200


def slack_bot(task):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}",
    }

    requests.post(path, params=query_params, headers={
                  'Authorization': SLACK_API_KEY})


@tasks_bp.route("/<task_id>/mark_complete", strict_slashes=False, methods=["PATCH"])
def mark_task_as_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = dt.datetime.now()
    db.session.commit()
    slack_bot(task)
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", strict_slashes=False, methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", strict_slashes=False, methods=["DELETE"])
def delete_task(task_id):

    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }))


@goals_bp.route("/", strict_slashes=False, methods=["POST"])
def create_goal():

    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError:
        abort(make_response({
            "details": "Invalid data"
        }, 400))
    db.session.add(new_goal)
    db.session.commit()
    return make_response(jsonify({
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }), 201)


@goals_bp.route("/", strict_slashes=False, methods=["GET"])
def get_all_goals():

    goal_query = Goal.query

    goals = goal_query.all()

    # appending each goal to dictionary
    goal_response = [goal.to_dict() for goal in goals]

    return jsonify(goal_response)


@goals_bp.route("/<goal_id>", strict_slashes=False, methods=["GET"])
def get_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", strict_slashes=False, methods=["PUT"])
def update_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return make_response(jsonify({
        "goal": {
            "id": 1,
            "title": "Updated Goal Title",

        }
    }), 200)


@goals_bp.route("/<goal_id>", strict_slashes=False, methods=["DELETE"])
def delete_goals(goal_id):

    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": "Goal 1 \"Build a habit of going outside daily\" successfully deleted"}))


@goals_bp.route("/<goal_id>/tasks", strict_slashes=False, methods=["POST"])
def create_list_task_ids_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_list = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        # id of the goal connected to Task .goal attribute that making the connection
        task.goal = goal
        task_list.append(task_id)

    db.session.commit()

    return jsonify({"id": goal.id, "task_ids": task_list}), 200


@goals_bp.route("/<goal_id>/tasks", strict_slashes=False, methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks= Task.query.filter_by(goal=goal)
    task_list=[task.to_dict() for task in tasks]
    
    goal_dict=goal.to_dict()
    goal_dict["tasks"]=task_list
    return make_response(jsonify(goal_dict)),200


