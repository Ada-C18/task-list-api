from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os

task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")
goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

#Note: this has both the routes for task and goal

"""Routes for Task"""
@task_bp.route("", methods=['POST'])
def make_new_task():
    response_body = request.get_json()
    
    try:
        new_task = Task(
            title=response_body["title"],
            description=response_body["description"])
    except KeyError:
        return make_response({
        "details": "Invalid data"
    },400)
   
    db.session.add(new_task)
    db.session.commit()

    return make_response({f"task":new_task.dictionfy()},201)



@task_bp.route("", methods=['GET'])
def get_all_tasks():
    return_list=[]
    
    sort_query = request.args.get("sort")
    
    if sort_query=="desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.title.asc()).all()
    
    for task in tasks:
        return_list.append(task.dictionfy())
    
    return make_response(jsonify(return_list),200)


@task_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    return make_response(jsonify({"task":task.dictionfy()}),200)


@task_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id):
    response_body = request.get_json()
    task = validate_model(Task,task_id)

    task.title = response_body["title"]
    task.description = response_body["description"]

    db.session.commit()

    return make_response({f"task":task.dictionfy()},200)

@task_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_as_complete(task_id):
    """
    Please note, I'm commenting out the slack bot section as while it does work,
    it is also continuously crashing my Slack with each pytest and I'd rather not have it do that.
    """
    task = validate_model(Task,task_id)

    task.completed_at = datetime.now()

    db.session.commit()
    
    #this is the slack bot section
    slack_bot_token = os.environ.get('SLACKBOT_API_TOKEN')
    headers = {'Authorization': f'Bearer {slack_bot_token}'}
    requests.put(f'https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}',headers=headers)
    
    return make_response({f"task":task.dictionfy()},200)

@task_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = None

    db.session.commit()

    return make_response({f"task":task.dictionfy()},200)



@task_bp.route("/<task_id>", methods=['DELETE'])
def delete_a_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details':f'Task {task_id} \"{task.title}\" successfully deleted'},200)


"""Goal Routes Start"""
@goal_bp.route("", methods=['POST'])
def create_new_goal():
    response_body = request.get_json()
    
    try:
        new_goal = Goal(
            title=response_body["title"])
    except KeyError:
        return make_response({
        "details": "Invalid data"
    },400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({f"goal":new_goal.goal_dictionfy()},201)

@goal_bp.route("", methods=['GET'])
def get_all_goals():
    return_list=[]
    
    sort_query = request.args.get("sort")
   
    if sort_query=="desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.order_by(Goal.title.asc()).all()
    
    for goal in goals:
        return_list.append(goal.goal_dictionfy())
    
    return make_response(jsonify(return_list),200)

@goal_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return make_response(jsonify({"goal":goal.goal_dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    response_body = request.get_json()
    goal = validate_model(Goal,goal_id)

    goal.title = response_body["title"]
   
    db.session.commit()

    return make_response({f"goal":goal.goal_dictionfy()},200)

@goal_bp.route("/<goal_id>", methods=['DELETE'])
def delete_a_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details':f'Goal {goal_id} \"{goal.title}\" successfully deleted'},200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_book(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task,task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"]
    }), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return_dict = {
        "id":goal.goal_id,
        "title":goal.title,
        "tasks":[]
    }

    for task in goal.tasks:
        return_dict["tasks"].append(task.dictionfy())

    return make_response(jsonify(return_dict),200)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model