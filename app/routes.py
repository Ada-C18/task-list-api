from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task


bp = Blueprint("task_list", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

@bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()


    return make_response({"task":(new_task.to_dict())}, 201)
    

@bp.route("", methods = ["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    color_query = request.args.get("color")
    description_query = request.args.get("description")
    id_query = request.args.get("id")

    task_query = Task.query

    if title_query:
        task_query = task_query.filter_by(title=title_query) 

    if color_query:
        task_query = task_query.filter_by(color=color_query)

    if description_query:
        task_query = task_query.filter_by(description = description_query)

    if id_query:
        task_query = task_query.filter_by(id= id_query)
   
    tasks = task_query.all()
    
    all_tasks = [task.to_dict() for task in tasks]

    return jsonify(all_tasks), 200

@bp.route("/<id>", methods = ["GET"])
def read_tasks_by_id(id):
    task = validate_model(Task,id)
    return jsonify({"task":task.to_dict()}), 200

@bp.route("/<id>", methods = ["PUT"])
def update_task_by_id(id):
    updated_task = validate_model(Task,id)
    request_body = request.get_json()

    updated_task.title = request_body["title"]
    updated_task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task":updated_task.to_dict()}), 200


   

@bp.route("/<id>", methods = ["DELETE"])
def delete_task_by_id(id):
    deleted_task = validate_model(Task,id)
    
    db.session.delete(deleted_task)

    db.session.commit()


    return make_response({"details":f"Task {deleted_task.id}""{deleted_task.description} successfully deleted"}), 200