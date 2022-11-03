from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#helper function to validate task id
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message":f"data type {task_id} is invalid"},400))

    chosen_task = Task.query.get(task_id)
    
    if chosen_task is None:
        abort(make_response({"message":f"Could not find task item with id: {task_id}"},404))

    return chosen_task

##End route to get all tasks
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    title_query_value = request.args.get("title")
    if title_query_value is not None:
        tasks = Task.query.filter_by(title=title_query_value)
    
    else:
        tasks = Task.query.all()
    
    result = []
    
    for task in tasks:
        result.append(task.to_dict())
    
    return jsonify(result), 200

##End route to get one task
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    
    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    # completed_at=request_body['completed_at']
                    )
    
    attributes = ["title","description"]
    
    try:
        new_task.title = request_body["title"]
        new_task.description = request_body["description"]
    except KeyError:
        # return jsonify({"details": "Invalid data"}),400
        for attribute in attributes:
            if attribute not in request_body:
                return jsonify({"details": "Invalid data"}),400
    
    
    db.session.add(new_task)
    db.session.commit()
    # return jsonify({"task":{"id":new_task.task_id,"title":new_task.title,"description":new_task.description,"is_complete":False}}), 201
    return jsonify({"task":new_task.to_dict()}), 201

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    update_task = get_task_from_id(task_id)
    request_body = request.get_json()
    
    task_attributes = ["title","description"]
    response_message = ""
    
    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        # return jsonify({"details": "Invalid data"}),400
        for attribute in task_attributes:
            
            if attribute not in request_body:
                response_message += attribute +", "
        return jsonify({"message": f"Task #{task_id} missing {response_message[:-2]}"}),400
    

    
    db.session.commit()
    return jsonify({"task":update_task.to_dict()}),200
    

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return jsonify({"details":f"Task {task_id} \"{task_to_delete.title}\" successfully deleted"})
    