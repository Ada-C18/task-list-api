from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f" {id} is an invalid id"}, 400))

    query_result = Task.query.get(id)
    if not query_result:
        abort(make_response({"message":f" {id} not found"}, 404))

    return query_result





#################CREATE_TASK############


@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    task_dictionary=new_task.to_dict()
   
    return {"task":task_dictionary}, 201

##############GET_ALL_TASK####################
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    completed_param=request.args.get("completed_at")

    if title_param:
        tasks = Task.query.filter_by(title=title_param)
    elif description_param:
        tasks = Task.query.filter_by(description=description_param)
    elif completed_param:
        tasks=Task.query.filter_by(completed_at=completed_param)
    else:
        tasks = Task.query.all()

    result_list = [task.to_dict() for task in tasks]

    return   jsonify(result_list), 200

###############Get_one_task######################
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id(id)
    

    return jsonify({"task":task.to_dict()}), 200

################ UPDATE_TASK ########################
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.title=request_body["title"]
    task.description=request_body["description"]
    task.completed_at=None
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200

################# DELETE #################  

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(id)

    db.session.delete(task)

    db.session.commit()
    return  make_response({"details": f"Task {id} \"{task.title}\" successfully deleted"}), 200
    