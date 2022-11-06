from app import db
from app.models.task import Task
from flask import Blueprint,jsonify,abort,make_response,request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route("", methods=["POST"])

def create_task():
    request_body = request.get_json()


    # if "title" not in request_body or "description" not in request_body:
    #     return make_response("Invalid Request, Title & description Can't Be Empty", 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        is_completed = request_body["is_completed"]
    )

    
    db.session.add(new_task)
    db.session.commit()

    
    return make_response(f"Task {new_task.title} has been successfully created!", 201)







@tasks_bp.route('/<task_id>',methods=['PUT'])
def edit_task(task_id):
    task = Task.query.get(task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.is_complete = request_body["is_complete"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response(f"task {task.title} succesfully updated",200)


    






@tasks_bp.route('',methods=['GET'])
def get_task():
    task_query = Task.query

    descripiton_query = request.arg.get("description")
    if descripiton_query:
        task_query = task_query.filter_by(description = descripiton_query)
    else:
        task = Task.query.all()

    title_query = request.arg.get("title")
    if title_query:
        task_query = task_query.filter_by(title = title_query)
    else:
        task = Task.query.all()
    
    is_complete_query = request.arg.get("is_complete")
    if is_complete_query:
        task_query = task_query.filter_by(is_complete = is_complete_query)
    else:
        task = Task.query.all()

    by_id_query = request.arg.get(id)
    if by_id_query:
        by_id_query = by_id_query.filter_by(by_id = by_id_query)
    else:
        task = Task.query.all()

    tasks = task_query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "name": task.name,
            "is_complete": task.is_complete,
            "description": task.description
        })
    if not tasks_response:
        return make_response(jsonify(f"There are no {task_query} tasks"))
    return jsonify(tasks_response)




@tasks_bp.route('/<task_id>',methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task {task.title} succesfully deleted",202)