import json
import datetime
from os import abort

from flask import Blueprint, abort, jsonify, make_response, request
from sqlalchemy import asc, desc

from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=['POST'])
def created_task():
    response_body = request.get_json()

    if "title" not in response_body or "description" not in response_body:
        return {"details": "Invalid data"}, 400
    
    created_task = Task(title=response_body["title"],
                description=response_body["description"])

    
    db.session.add(created_task)
    db.session.commit()
    
    return make_response(jsonify({"task": created_task.build_task_dict()})), 201


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route('', methods=['GET'])
def query_all():
    
    sort_query = request.args.get("sort")
    
    query_lists = []
    
       
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)



    if sort_query== "desc":
        query_tasks = Task.query.order_by(Task.title.desc())


    elif sort_query == "asc":
        query_tasks = Task.query.order_by(Task.title.asc())

    else:
        query_tasks = Task.query.all()

    for query in query_tasks:
        query_lists.append(query.build_task_dict())

    return jsonify(query_lists), 200



@tasks_bp.route('/<task_id>', methods=['GET'])
def one_saved_task(task_id):
    task_validate = validate_task_id(task_id)
    
    # task = Task.query.get(task_id)
    if task_id == None:
        return "The task ID submitted, does not exist: error code 404"
    else:    
        return {"task": task_validate.build_task_dict()}


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_tasks(task_id):
    
    validate_id = validate_task_id(task_id)

    response_body = request.get_json()
    
    validate_id.title = response_body["title"]
    validate_id.description = response_body["description"]
    # validate_id.completed_at = response_body["completed_at"]

    db.session.commit()

    return jsonify({"task": validate_id.build_task_dict()}),200
    

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    test_task = validate_task_id(task_id)
    result_notice = {"details": f'Task {task_id} "{test_task.title}" successfully deleted'}

    db.session.delete(test_task)
    db.session.commit()

    return make_response(result_notice, 200)

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_on_incomplete_task(task_id):
    test_task = validate_task_id(task_id)
    test_task.completed_at = datetime.datetime.today()
    test_task.is_complete = True
    db.session.commit()
    print(test_task.completed_at)

    return make_response({"task": {
            "id": test_task.task_id,
            "title": test_task.title, 
            "description":test_task.description, 
            "is_complete": test_task.is_complete}}), 200

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete_on_complete_task(task_id):
    test_task = validate_task_id(task_id)
    test_task.completed_at = None
    test_task.is_complete = False
    db.session.commit()

    return make_response({"task": {
            "id": test_task.task_id,
            "title": test_task.title, 
            "description":test_task.description, 
            "is_complete": test_task.is_complete}}), 200