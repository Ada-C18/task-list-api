from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

##################################################     
#           WAVE 1, part 2: VALIDATE TASK ID  
##################################################
def validate_task_id(id):
    #confirm id is type int
    try:
        id= int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    task = Task.query.get(id)

    #confirm id is in db
    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return task
    
################################################ 
#       WAVE 1, part 3: VALIDATE INPUT REQUESTS  
# ##############################################
def validate_request(request_body):
    try:
        if request_body['title'] and request_body['description']:
            return request_body
    except KeyError as error:
        abort(make_response({"details":"Invalid data"}, 400))

######################  WAVE 1, PART 1: CRUD ######################

#########################################
#            CREATE RESOURCE
##########################################
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    #the next line would create dependency with VALIDATE_REQUEST function
    new_task = validate_request(request_body)
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    task={"task":new_task.to_dict()}

    return task, 201

    

################################
#       GET ALL RESOURCES
################################
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    if request.args.get("sort")=='asc':
        tasks = Task.query.order_by(Task.title).all()
    elif request.args.get("sort")=='desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = []  #returns empty list if no tasks

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response), 200

########################################
#       Get One Task: One Saved Task
########################################
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_task_id(id)
    saved_task={"task":task.to_dict()}

    return saved_task,200


##################################
#       Update Task  
# ################################
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task_id(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    updated_task={"task":task.to_dict()}

    return updated_task,200


#######################################   
#           Delete Task
#######################################
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task_id(id)
    title=str(task.title)
    description=str(task.description)
    #message='Task '+str(id)+" "+title+" "+description+" successfully deleted"
    message=f'Task {id} {title} successfully deleted'
    deleted_task={}
    deleted_task["details"]=message

    db.session.delete(task)
    db.session.commit()


    return deleted_task, 200



######################################   
#   FLASK SHUTDOWN ROUTE 
# #####################################
@tasks_bp.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."

####################################################

#                WAVE 3

#####################################################

#############   COMPLETE_TASK: PATCH    ################
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def completed_task(id):
    task = validate_task_id(id)

    #request_body = request.get_json()
    
    #if not task.completed_at:
    task.completed_at = datetime.utcnow()

    db.session.commit()

    completed_task={"task":task.to_dict()}
    completed_task["task"]["is_complete"] = True

    return completed_task,200

#######################################
#       INCOMPLETE TASK - PATCH
#######################################

"""""
Thee functionality I need is.....
    if /mark_complete ....do this
    elif /mark_incomplete .... do that
It looks like this /mark_incomplete function is overwriting previous PATCH function..
#   
# Debugger does not seem to be working...

# how to solve? 
#  possible solution: flask app endpoint <function name>
#
"""

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_task_id(id)

    # request_body = request.get_json()
    
    # if task.completed_at:
    task.completed_at = None

    db.session.commit()

    incomplete_task={"task":task.to_dict()}
    incomplete_task["task"]["is_complete"] = False

    return incomplete_task,200

##################################
#       General error handling
###################################
#@app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html', pic=pic), 404

# @app.errorhandler(400)
# def bad_request():
#     """Bad request."""
#     return make_response(
#         render_template("400.html"),
#         400
#     )


# @app.errorhandler(500)
# def server_error():
#     """Internal server error."""
#     return make_response(
#         render_template("500.html"),
#         500
#     )
