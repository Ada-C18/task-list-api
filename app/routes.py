from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

#POST request
@tasks_bp.route("",methods = ['POST'])
def create_task():
    request_body = request.get_json()
    
    new_task = Task(title = request_body['title'],
                    description = request_body['description'],
                    completed_at = request_body["completed_at"])
                        
    
    db.session.add(new_task)
    db.session.commit()

    # task_response = [task.to_dict() for task in new_task]
    return make_response("CREATED", 201)

#Get Tasks: Getting Saved Tasks
@tasks_bp.route("", methods=["GET"])
def get_all_task():

    all_tasks = Task.query.all()

    task_response = [task.to_dict() for task in all_tasks]

    return make_response(jsonify(task_response), 200)


