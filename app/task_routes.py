from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
from app.goal_routes import validate_model, sort_query_helper
import requests
import os

task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")


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

    return make_response(jsonify({f"task":new_task.dictionfy()}),201)



@task_bp.route("", methods=['GET'])
def get_all_tasks():
    return_list=[]
    
    match_command = [(key,value) for key,value in request.args.items()]
    specific_title = request.args.get('title')
    mCase = specific_title or match_command or "I'm a teapot"
    
    #currently can query: specific name, order by id or title, all
    if specific_title:
        tasks = Task.query.filter_by(title=specific_title)
    elif match_command:
        try:
            tasks = sort_query_helper(Task,match_command)
        except ValueError:
            return make_response(jsonify({"warning":"Invalid query sorting parameters"}),400)
    else:
        tasks = Task.query.all()
    
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

    return make_response(jsonify({f"task":task.dictionfy()}),200)

@task_bp.route("/<task_id>", methods=["PATCH"])
def patch_one_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()

    name_change = patch_helper(task,"title",request_body)
    description_change = patch_helper(task,"description",request_body)
    if not name_change and not description_change:
        return make_response(jsonify({'warning':'Please send valid information: title or description. K thx <3'}),400)
    db.session.commit()

    return make_response(jsonify({f"task":task.dictionfy()}),202)

def patch_helper(object, value, request_body):
    try:
        setattr(object, value, request_body[value])
    except KeyError:
        return None
    return True

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
    slack_call(task.title)
    
    return make_response(jsonify({f"task":task.dictionfy()}),200)

def slack_call(task_title):
    slack_bot_token = os.environ.get('SLACKBOT_API_TOKEN')
    URL = 'https://slack.com/api/chat.postMessage'
    headers = {'Authorization': f'Bearer {slack_bot_token}'}
    params = {
        "channel":'task-notifications',
        'text':f'Someone just completed the task {task_title}'
    }
    requests.put(URL,params=params,headers=headers)
    

@task_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({f"task":task.dictionfy()}),200)



@task_bp.route("/<task_id>", methods=['DELETE'])
def delete_a_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'details':f'Task {task_id} \"{task.title}\" successfully deleted'}),200)


