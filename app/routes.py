from flask import Blueprint
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__,url_prefix="/tasks")


# Helper function
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {task_id}"}, 200))


    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find the task with id: {task_id}"}, 404))
    
    return chosen_task


@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return abort(make_response({"details": "Invalid data"}, 400))

    new_task= Task(title=request_body["title"],
                description=request_body["description"]

    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():

    sort_query_value = request.args.get('sort')
    if sort_query_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all() 
    else:
    # title_query_value is not None:
        tasks = Task.query.order_by(Task.title.asc()).all()
    # else:
    # tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append(task.to_dict())
    
    return jsonify(result), 200

# @tasks_bp.route('/task?sort=asc', methods=['GET'])
# def get_taks_asc():
#     tasks = Task.query.order_by(Task.title.asc()).all()

#     result = []

#     for task in tasks:
#         result.append(task.to_dict())
    
#     return jsonify(result), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):

    chosen_task = get_task_from_id(task_id)

    return jsonify({"task":chosen_task.to_dict()}), 200

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    update_task = get_task_from_id(task_id)

    request_body = request.get_json()

    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]

    except KeyError:
        return jsonify ({"msg": f"Missing attributes"}), 400

    db.session.commit()
    return jsonify({"task":update_task.to_dict()})

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)

    title_task_to_delete= get_task_from_id(task_id).to_dict()["title"]

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{title_task_to_delete}" successfully deleted'}), 200
        



