import datetime, os, requests
from app import db
from app.models.task import Task

from flask import Blueprint, jsonify, make_response, request, abort
from dotenv import load_dotenv



tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({'message':f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get('title')
    sort_query = request.args.get('sort')

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
        
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
        
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
        
    if not title_query and not sort_query:
        tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)



@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if len(request_body) != 2:
        return {"details": "Invalid data"}, 400
    
    new_task= Task(title=request_body['title'], \
        description=request_body['description'])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({'task': new_task.to_dict()}), 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if task.goal_id:
        return jsonify({'task': task.to_dict(goal=True)})

    return jsonify({'task': task.to_dict()})



@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({'task': task.to_dict()})



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}))




def update_community(message):
    load_dotenv()
    URL = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API_KEY")
    query_params = {"channel":"task-notifications", "text":message}
    header = {"Authorization":API_KEY}

    requests.post(URL, data=query_params, headers=header)


@tasks_bp.route("/<task_id>/<command>", methods=["PATCH"])
def update_completed_at(task_id, command):
    task = validate_model(Task, task_id)
    if command == 'mark_incomplete':
        task.completed_at = None
    if command == 'mark_complete':
        task.completed_at = task.completed_at = datetime.datetime.today()
        update_community(f'Someone just completed the task {task.title}')
        
    db.session.commit()
    
    return make_response(jsonify({'task': task.to_dict()}))

