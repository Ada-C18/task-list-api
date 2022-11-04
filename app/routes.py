from flask import Blueprint, request, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from operator import itemgetter
from datetime import date

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#-------------------------------------------HELPERS----------------------------------
def validate_task(task_id_input):
    try:
        task_id_input = int(task_id_input)
    except:
        abort(make_response({"message": f"Task {task_id_input} invalid"}, 400))

    task = Task.query.get((task_id_input))

    if not task:
        abort(make_response({"message": f"Task {task_id_input} not found"}, 404))

    return task

def determine_completion(task):
    if task.completed_at == None:
        task.completed_at = False
    else:
        task.completed_at = True #task["completed_at"]
    
    return task.completed_at

def task_dict(task, determine_completion):
    return {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": determine_completion(task)
            
        }
    
#-------------------------------------------POST----------------------------------
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    print(F"LOOK HERE! {request_body}.")

    if 'title' not in request_body or\
        'description' not in request_body:
        # 'completed_at' not in request_body: ----- #read-me wave 1 says to put this in but not even the tests request body's have a completed_at 
            return {"details": "Invalid data"}, 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        # completed_at=request_body["is_complete"]
    )
    
    db.session.add(new_task)
    db.session.commit()


    return {
        "task": task_dict(new_task, determine_completion)
    }, 201
#-------------------------------------------GET----------------------------------
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    # request_body = request.get_json()
    title_sort = request.args.get("sort")

    # if title_sort is None:
    #     tasks = Task.query.all()
    # elif title_sort == "asc":
    #     tasks = sorted(tasks, key=itemgetter("title"))
    # elif title_sort == "desc":
    #     tasks = sorted(tasks, key=itemgetter("title", reverse=True))
    
    tasks = Task.query.all()


    response = []
    for task in tasks:
        task_info = task_dict(task, determine_completion)
        response.append(task_info)

    if title_sort == "asc":
        response = sorted(response, key=itemgetter("title"))
    elif title_sort == "desc":
        response = sorted(response, key=itemgetter("title"), reverse=True)

    return jsonify(response), 200

@task_bp.route("/<task_id_input>", methods=["GET"])
def get_one_task(task_id_input):
    chosen_task = validate_task(task_id_input)

    task_info = {
        "task": task_dict(chosen_task, determine_completion)
    }

    return jsonify(task_info), 200
# -------------------------------------------PUT----------------------------------
@task_bp.route("/<task_id_input>", methods=["PUT"])
def update_a_task(task_id_input):
    chosen_task = validate_task(task_id_input)

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"message":"Request must include title and description"})

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    # chosen_task.completed_at = request_body["completed_at"]
    
    db.session.commit()

    return {
        "task": task_dict(chosen_task, determine_completion)
    }, 200

# -------------------------------------------PATCH----------------------------------
@task_bp.route("/<task_id_input>/<complete_status>", methods=["PATCH"])
def mark_complete_status(task_id_input, complete_status):
    chosen_task = validate_task(task_id_input)

    request_body = request.get_json()

    # if "title" in request_body:
    #     new_title = chosen_task.title
    # if "description" in request_body:
    #     new_descrip = chosen_task.description
    if complete_status == "mark_complete":
        chosen_task.completed_at = date.today()
    elif complete_status == "mark_incomplete":
        chosen_task.completed_at = None
    db.session.commit()
    # print(f"DATE!!!!: {chosen_task.completed_at}")

    return {
    "task": task_dict(chosen_task, determine_completion)
    }

# @task_bp.route("/<task_id_input>/<complete_status>", methods=["PATCH"])
# def mark_incomplete(task_id_input, complete_status):
#     chosen_task = validate_task(task_id_input)
#     print(f"CHOSEN TASK = {chosen_task}")
#     request_body = request.get_json()
#     print(f"REQUEST BODY = {request_body}")
#     # if "title" in request_body:
    # #     new_title = chosen_task.title
    # # if "description" in request_body:
    # #     new_descrip = chosen_task.description
    # if complete_status == "mark_incomplete":
    #     chosen_task.completed_at = Task.completed_at
    # db.session.commit()
    # print(f"DATE!!!!: {chosen_task.completed_at}")

    # return {
    # "task": {
    #     "id": chosen_task.task_id,
    #     "title": chosen_task.title,
    #     "description": chosen_task.description,
    #     "is_complete": False #determine_completion(chosen_task)
    #     }
    # }
# -------------------------------------------DELETE----------------------------------
@task_bp.route("/<task_id_input>", methods=["DELETE"])
def delete_a_task(task_id_input):
    chosen_task = validate_task(task_id_input)

    db.session.delete(chosen_task)
    db.session.commit()

    return {"details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"}

