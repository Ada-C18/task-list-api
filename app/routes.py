from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@task_list_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False 
            }
        )
    return jsonify(tasks_response)


@task_list_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task": task.to_dict()})


@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if len(request_body) != 2:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task.from_dict(request_body)
    

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return jsonify({"task": task.to_dict()}), 200
    


@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200





# @task_list_bp.route("", methods=["GET"])   
# def get_all_tasks():
#     title_param = request.args.get("title")
#     description_param = request.args.get("description")
    
#     if title_param:
#         tasks = Task.query.filter_by(title=title_param)
#     elif description_param:
#         tasks = Task.query.filter_by(description=description_param)
#     else:
#         tasks = Task.query.all()
        
#     results_list = [task.to_dict() for task in tasks]
#     return jsonify(results_list), 200


    # (title=request_body["title"],
    #                 description=request_body["description"],
    #                 completed_at=request_body["completed_at"])

    # db.session.add(new_task)
    # db.session.commit()

    # return make_response(f"Book {new_task.title} successfully created", 200)