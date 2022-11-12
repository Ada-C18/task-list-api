from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
    
        try:
            task = Task(title = request_body['title'], description = request_body['description'])
        except KeyError:
            invalid_dict = {"details": "Invalid data"}
            return make_response(jsonify(invalid_dict),400)

        db.session.add(task)
        db.session.commit()

        response_body = {"task": task.to_dict()}

        return make_response(jsonify(response_body), 201)

    elif request.method == "GET":
        sort_by_query = request.args.get('sort')

        tasks = Task.query.all()
        response_body = []

        if sort_by_query == 'asc':
            tasks = Task.query.order_by(Task.title)
        elif sort_by_query == 'desc':
            tasks = Task.query.order_by(desc(Task.title))
        
        for task in tasks:
            response_body.append(task.to_dict())

        return make_response(jsonify(response_body), 200)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])

def handle_task(task_id):
    if request.method == "GET":
        task = validate_model_id(Task, task_id)
        #task = Task.query.get(task_to_get)

        return make_response(jsonify({"task": task.to_dict()}), 200)

    elif request.method == "PUT":
        task = validate_model_id(Task, task_id)
        #task = Task.query.get(task_to_edit)

        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()

        return make_response(jsonify({"task": task.to_dict()}), 200)

    elif request.method == "DELETE":
        task = validate_model_id(Task, task_id)
        #task = Task.query.get(task_to_delete)
        
        db.session.delete(task)
        db.session.commit()

        return make_response({"details": f'Task {task.task_id} ' f'"{task.title}"' ' successfully deleted'}, 200)

def validate_model_id(cls,task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"message":f"{cls.__name__} id {task_id} is invalid"},400))
    
    chosen_object = cls.query.get(task_id)
    
    if chosen_object is None:
        return abort(make_response({"message":f"{cls.__name__} {task_id} not found"}, 404))
    
    return chosen_object

# #def check_for_missing_info(task_id):
#     task = validate_model_id(Task, task_id)

#     if "title" not in task:
#         return make_response("Missing title", 400)

#     if "description" not in task:
#         return make_response("Missing description", 400)

#     if "completed_at" not in task:
#         return make_response("Missing completed_at value", 400)