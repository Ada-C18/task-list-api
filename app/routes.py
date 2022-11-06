from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

#POST request
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if  not len(request_body) == 2:
        return {"details": "Invalid data"}, 400
    
    new_task= Task(title=request_body['title'], 
        description=request_body['description'])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({'task': new_task.to_dict()}), 201)

#Get Tasks: Getting Saved Tasks
@tasks_bp.route("", methods=["GET"])
def get_all_task():

    all_tasks = Task.query.all()

    task_response = [task.to_dict() for task in all_tasks]

    return make_response(jsonify(task_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({'task': task.to_dict()})

#new code because we passed
