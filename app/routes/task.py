from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db


task_bp = Blueprint("task", __name__, url_prefix = "/tasks")

@task_bp.route('', methods= ['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body['title'], 
                        description=request_body['description'])
                    # completed_at=request_body['completed_at'])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201



@task_bp.route('', methods=["GET"])
def get_all_tasks():
    title_query_value = request.args.get("title") 
    # It's better to check for None rather than check for falsey, in case we are checking for value equal to 0 or False.
    if title_query_value is not None: 
        tasks = Task.query.filter_by(title = title_query_value)
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:    
        response.append(task.to_dict())

    return jsonify(response), 200



