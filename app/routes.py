from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{cls} {id} is an invalid id"}, 400))

    query_result = Task.query.get(id)

    if not query_result:
        abort(make_response({"message": f"{cls}{id} is an invalid id"}), 404)

    return query_result

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task} has been created", 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
    
    results_list = [t.to_dict() for t in tasks]
    
    return jsonify(results_list), 200

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id(Task, id)

    return jsonify(task.to_dict()), 200
    
@tasks_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    task = validate_id(Task, id)
    
    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return make_response(jsonify(f"task {id} sucessfully updated"))

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_cat(id):
    task = validate_id(Task, id)

    db.session.delete(task)

    db.session.commit()

    return make_response(jsonify(f"task {id} successfully deleted"))

