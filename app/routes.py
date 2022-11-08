from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from os import abort


task_bp = Blueprint("task_bp", __name__, url_prefix='/tasks')

@task_bp.route("", methods=["POST"])
def create_task():        
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:# or 'completed_at' not in request_body
        return make_response(jsonify({"details":"Invalid data"})),400
    new_task= Task(
        title = request_body['title'],
        description =  request_body['description'],
        
    )
    #completed_at = request_body['completed_at']

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({f"task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
            }})),201


@task_bp.route("", methods=["GET"])
def read_all_tasks():

    task_query = Task.query
    
    task_asc_query = request.args.get("/tasks?sort=asc")
    if task_asc_query:
        task_query = task_query.filter(Task.title.sorted(task_asc_query, key=lambda x: x['title']))
        #tasks = Task.query.sorted(title=task_asc_query,reverse=True)
    
        # task_query = task_query.filter(Planet.name.ilike(f"%{name_query}%"))

    task_desc_query = request.args.get("/tasks?sort=desc")   
    if task_desc_query:
        task_query = task_query.filter(Task.title.sorted(task_desc_query,key=lambda x: x['title'],reverse=True))
    
        return jsonify(task_query)
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            })
    
    # if not tasks_response:
    #     return make_response(jsonify([])),200       
    return jsonify(tasks_response),200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    # if not task:
    #     make_response({"message":f"Task {task_id} not found"}, 404)
        
    return task
    

@task_bp.route('/<task_id>',methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    if task:
        return {"task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                }},200
    return task

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    

    db.session.commit()

    return make_response(jsonify({f"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }})),200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task_id)
    db.session.commit()

    return make_response(f"'details': {task.id} \{task.title}\ successfully deleted"),200 