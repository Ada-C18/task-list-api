from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db
from datetime import datetime
from app.helper_functions import validate_model, post_one_model, get_one_model, get_all_models, delete_one_model, slack_call, patch_helper


task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")


#Note: this has both the routes for task and goal

"""Routes for Task"""
@task_bp.route("", methods=['POST'])
def make_new_task():
    return post_one_model(Task)


@task_bp.route("", methods=['GET'])
def get_all_tasks():
    return get_all_models(Task)
    """
    This is the previous code used that is common between tasks and goals

    return_list=[]
    
    match_command = [(key,value) for key,value in request.args.items()]
    specific_title = request.args.get('title')
    
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
    
    return make_response(jsonify(return_list),200)"""


@task_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    return get_one_model(Task,task_id)


@task_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id):
    response_body = request.get_json()
    task = validate_model(Task,task_id)
    try:
        task.title = response_body["title"]
        task.description = response_body["description"]
    except KeyError:
        return make_response(jsonify({'warning':'Enter both title and description or use patch method'}),400)

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
    

@task_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({f"task":task.dictionfy()}),200)



@task_bp.route("/<task_id>", methods=['DELETE'])
def delete_a_task(task_id):
    return delete_one_model(Task,task_id)
