import string
from app import db
from app.models.task import Task
from flask import Blueprint,jsonify,abort,make_response,request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

def validate_task(task_id):

    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))
    
    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
    )

    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task":new_task.to_dict()}, 201)

@tasks_bp.route('/<task_id>',methods=['PUT'])
def update_task(task_id):
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request, Title & Description Can't Be Empty", 400)

    task = validate_task(task_id)
    task = Task.query.get(task_id)
    
    task.title = request_body["title"]
    # task.is_complete = request_body["is_complete"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response({"task":task.to_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
# GET /task/id
def handle_task(task_id):
    # Query our db to grab the task that has the id we want:
    task = validate_task(task_id)
    task = Task.query.get(task_id)

    return {"task":{
                "id": task.task_id,
                "title": task.title,
                "is_complete": task.is_complete,
                "description": task.description}
            }


@tasks_bp.route('',methods=['GET'])
def get_task():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query:
        task_response = []
        tasks = task_query.all()
        for task in tasks:
            task_response.append(task.to_dict())

        task_titles = []

        for task in task_response:
            for key, value in task.items():
                if key == "title":
                    task_titles.append(value)

        response_body = []
        if sort_query == "asc":
            sorted_tasks = sorted(task_titles)
            while len(response_body) < len(task_titles):
                for task in task_response:
                    if len(sorted_tasks) == 0:
                        break
                    if task["title"] == sorted_tasks[0]:
                        response_body.append(task)
                        sorted_tasks.pop(0)
            return make_response(jsonify(response_body), 200)

        if sort_query == "desc":
            sorted_tasks = sorted(task_titles, reverse=True)
            while len(response_body) < len(task_titles):
                for task in task_response:
                    if len(sorted_tasks) == 0:
                        break
                    if task["title"] == sorted_tasks[0]:
                        response_body.append(task)
                        sorted_tasks.pop(0)
            return make_response(jsonify(response_body), 200)

    descripiton_query = request.args.get("description")
    if descripiton_query:
        task_query = task_query.filter_by(description = descripiton_query)

    title_query = request.args.get("title")
    if title_query:
        task_query = task_query.filter_by(name = title_query)
    
    is_complete_query = request.args.get("is_complete")
    if is_complete_query:
        task_query = task_query.filter_by(is_complete = is_complete_query)

    tasks = task_query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "is_complete": task.is_complete,
            "description": task.description
        })

    return jsonify(tasks_response)

@tasks_bp.route('/<task_id>',methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200)