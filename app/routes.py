from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import desc, asc
import datetime as dt
import os
from dotenv import load_dotenv
import requests

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f" {id} is an invalid id"}, 400))

    query_result = Task.query.get(id)
    if not query_result:
        abort(make_response({"message":f" {id} not found"}, 404))

    return query_result


#################CREATE_TASK############


@tasks_bp.route("", methods=["POST"])
def create_tasks():
    #request_body = request.get_json()
    #new_task = Task(title=request_body["title"],description=request_body["description"])
    
    if not 'title' in request.get_json() or not 'description' in request.get_json() :
            return {"details":"Invalid data"},400
    else:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        task_dictionary=new_task.to_dict()
        return {"task":task_dictionary}, 201

##############GET_ALL_TASK####################

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
   #/tasks?sort=desc
    sort_query = request.args.get("sort")
    
    if sort_query=="asc":
        tasks=Task.query.order_by(Task.title)
    elif sort_query=="desc":
        tasks=Task.query.order_by(Task.title.desc())

    else:
        tasks = Task.query.all()
    result_list = [task.to_dict() for task in tasks]
    return   jsonify(result_list), 200




###############Get_one_task######################
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id(id)
    

    return jsonify({"task":task.to_dict()}), 200

################ UPDATE_TASK ########################
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.title=request_body["title"]
    task.description=request_body["description"]
    task.completed_at=None
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200

################# DELETE #################  

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(id)

    db.session.delete(task)

    db.session.commit()
    return  make_response({"details": f"Task {id} \"{task.title}\" successfully deleted"})
    
################# UPDATE-PATCH##################
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_id(id)
    
    date=dt.datetime.utcnow()
    task.completed_at=date
    task.is_completed=True
    db.session.commit()
    send_slack_message(f"Someone just completed the task {task.title}")
    return jsonify({"task":task.from_dict()})

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_icomplete(id):
    task = validate_id(id)
    
    task.completed_at=None
    task.is_completed=False
    
    db.session.commit()
    return jsonify({"task":task.to_dict()})   



#API_KEY=os.environ.get("TOKEN")
#endpoint
#URL="https://slack.com/api/chat.postMessage"
#params
#PARAM={"channel":"task-notifications", "text":"Someone just completed the task My Beautiful Task"}
 # sending post request and saving response as response object
#r = requests.post(URL, data=xml, headers=headers)

#print(r.text)
def send_slack_message(message):
    API_KEY=os.environ.get("TOKEN")
    header={"Authorization":"Bearer"+API_KEY}
    URL="https://slack.com/api/chat.postMessage"
    query_params={"channel":"task-notifications", "text":message}
    response = requests.post(URL, data=query_params, headers=header)
    