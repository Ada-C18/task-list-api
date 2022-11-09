from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from dotenv import load_dotenv
import requests
import os



load_dotenv()


bp = Blueprint("task_list", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

@bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    if len(request_body.keys()) < 2:
        return make_response({"details":"Invalid data"},400)

    else:
        new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()


    return make_response({"task":(new_task.to_dict())}, 201)
    

@bp.route("", methods = ["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    completed_at_query = request.args.get("completed_at")
    description_query = request.args.get("description")
    id_query = request.args.get("id")
    sort_query = request.args.get("sort")
    
    

    task_query = Task.query

    if title_query:
        task_query = task_query.filter_by(title=title_query)

    if completed_at_query:
        task_query = task_query.filter_by(completed_at=completed_at_query)

    if description_query:
        task_query = task_query.filter_by(description = description_query)

    if id_query:
        task_query = task_query.filter_by(id= id_query)

    if sort_query == "desc" :
        task_query = Task.query.order_by(Task.title.desc())
    
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title)



    tasks = task_query.all()
    
    all_tasks = [task.to_dict() for task in tasks]

    return jsonify(all_tasks), 200

@bp.route("/<id>", methods = ["GET"])
def read_tasks_by_id(id):
    task = validate_model(Task,id)
    return jsonify({"task":task.to_dict()}), 200

@bp.route("/<id>", methods = ["PUT"])
def update_task_by_id(id):
    updated_task = validate_model(Task,id)
    request_body = request.get_json()

    updated_task.title = request_body["title"]
    updated_task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task":updated_task.to_dict()}), 200


   

@bp.route("/<id>", methods = ["DELETE"])
def delete_task_by_id(id):
    deleted_task = validate_model(Task,id)
    
    db.session.delete(deleted_task)

    db.session.commit()


    return make_response({"details":f'Task {deleted_task.id} \"{deleted_task.title}\" successfully deleted'}), 200

def ada_slack_bot(text):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_KEY = os.environ.get("SLACK_KEY")
    params = {
        "channel": "#task-notifications",
        "text": text
    }

    requests.post(PATH, params=params, headers = {"Authorization": SLACK_KEY})


@bp.route("/<id>/mark_complete", methods = ["PATCH"])
def is_complete(id):
    
    
    updated_task = validate_model(Task,id)

    if updated_task.completed_at == None:
      updated_task.completed_at = datetime.utcnow()
      ada_slack_bot(f"Someone just completed the task {updated_task.id}")
    final_task = updated_task.to_dict()
    final_task["is_complete"] = True

    db.session.commit()

    return jsonify({"task":final_task}), 200

@bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
def is_incomplete(id):
    updated_task = validate_model(Task,id)

    if updated_task.completed_at != None:
      updated_task.completed_at = None
    final_task = updated_task.to_dict()
   
    db.session.commit()

    return jsonify({"task":final_task}), 200


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods =["POST"])
def create_goal():
    request_body = request.get_json()

    if len(request_body.keys()) == 0:
        return make_response({"details":"Invalid data"},400)
    else:
        new_goal = Goal.from_goal_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()


    return make_response({"goal":(new_goal.to_goal_dict())}, 201)

@goal_bp.route("", methods = ["GET"])
def read_all_goals():
    task_query = Goal.query
    goals = task_query.all()
    
    all_goals = [goal.to_goal_dict() for goal in goals]

    return jsonify(all_goals), 200


@goal_bp.route("/<id>", methods = ["GET"])
def read_a_goals(id):
    goal = validate_model(Goal,id)
    return jsonify({"goal":goal.to_goal_dict()}), 200


@goal_bp.route("/<id>", methods = ["PUT"])
def update_a_goal(id):
    
    goal = validate_model(Goal,id)
    request_body = request.get_json()
    
    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":goal.to_goal_dict()}), 200

@goal_bp.route("/<id>", methods = ["DELETE"])
def delete_goal(id):
    deleted_goal = validate_model(Goal, id)

    db.session.delete(deleted_goal)
    db.session.commit()

    return make_response({"details":f'Goal {deleted_goal.id} \"{deleted_goal.title}\" successfully deleted'}), 200

@goal_bp.route("/<id>/tasks", methods = ["POST"])
def goal_task(id):
    goal = validate_model(Goal, id)
    task = Task(goal_id =goal.id, goal = goal )

    request_body = request.get_json()
  

    task.tasks = request_body["task_ids"]

    print(task.goal)
    print(request_body["task_ids"])
    
    print(goal.tasks)
    print(goal.tasks)

    db.session.add(task) 
    db.session.commit()

    return make_response({"id":task.goal_id, "task_ids":task.tasks}, 200 )

    

@goal_bp.route("/<id>/tasks", methods = ["GET"])
def get_task_of_one_goal(id):
    
    goal = validate_model(Goal, id)
    # tasks = Task.query.all()
    # for task in tasks:
    #   if task.goal_id == goal.id:
    #     task_list.append({task})

    # goal.tasks

    #     "id": task.id,
    #     "title": task.title,
    #     "description": task.description,
    # "goal_id": task.goal_id}
    
    
    
    goals =  []
    for task in goal.tasks:
      goals.append(
            {
            "id": task.id,
            "title": task.title,
            }
        )
      goal.tasks.append(task["goals"])
    
      
    db.session.add(goal)
    db.session.commit()
    if goal:
      return make_response({"id": goal.id,"title": goal.title, "tasks":goal.tasks}, 200)
    # else:
    #   return make_response({"id": goal.id,"title": goal.title, "tasks":goal.tasks, "goal_id": goal.id }, 200 )

