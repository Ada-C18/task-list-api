from app.models.task import Task
from app.models.goal import Goal
from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from datetime import date
import requests
import os
from dotenv import load_dotenv


load_dotenv()


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")


@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():

    if request.method == "POST":
        task = Task.from_dict(request.get_json())
        
        if task == False:
            return make_response({"details": "Invalid data"}, 400)
        
        db.session.add(task)
        db.session.commit()

        db.session.refresh(task)
        task = task.to_dict()
        response = {"task":task}
        return make_response(response,201)

    elif request.method == "GET":
        sort = request.args.get("sort")
        if sort == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
            
        else:
            tasks = Task.query.all()
        response_body = [task.to_dict() for task in tasks]
        return make_response(jsonify(response_body), 200)

def validate_id(class_obj, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details":"invalid id"},400))
    obj = class_obj.query.get(id)
    if not obj:
        abort(make_response({"details":f"{class_obj.__name__} not found"},404))
    else:
        return obj

@tasks_bp.route("/<id>", methods=["GET","DELETE","PUT"])
def handle_individual_task(id):
    task = validate_id(Task, id)
    if request.method == "GET":
        return make_response({"task":task.to_dict()}, 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
    
    elif request.method == "PUT":
        new_task = request.get_json()
        task.description = new_task["description"]
        task.title= new_task["title"]
        db.session.commit()

        return make_response({"task":task.to_dict()}, 200)


def mark_reducer(mark):
    if mark == "mark_complete":
        return True
    elif mark == "mark_incomplete":
        return False

@tasks_bp.route("/<id>/<mark>", methods=["PATCH"])
def mark_task(id, mark):
    task = validate_id(Task, id)
    mark = mark_reducer(mark)
    if mark == True:
        if task.completed_at == None:
            SLACK_URL = "https://slack.com/api/chat.postMessage"
            PARAMS = {"channel":"task-notifications",
                    "text":f"Someone just completed the task {task.to_dict()['title']}"
                    }
            HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
            r = requests.post(url = SLACK_URL, headers=HEADERS, params=PARAMS,)
        task.completed_at = date.today()
        db.session.commit()
        return make_response({"task":task.to_dict()},200)
    elif mark == False:
        task.completed_at = None
        db.session.commit()
        return make_response({"task":task.to_dict()},200)


@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():
    if request.method == "POST":
        goal = Goal.from_dict(request.get_json())
        
        if goal == False:
            return make_response({"details": "Invalid data"}, 400)
        
        db.session.add(goal)
        db.session.commit()

        db.session.refresh(goal)
        goal = goal.to_dict()
        response = {"goal":goal}
        return make_response(response,201)

    elif request.method == "GET":
        goals = Goal.query.all()
        response_body = [goal.to_dict() for goal in goals]
        return make_response(jsonify(response_body), 200)

@goals_bp.route("/<id>", methods=["POST", "GET", "PUT", "DELETE"])
def handle_individual_goal(id):
    goal = validate_id(Goal, id)
    if request.method == "GET":
        return make_response({"goal":goal.to_dict()}, 200)

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)
    
    elif request.method == "PUT":
        new_goal = request.get_json()
        goal.title= new_goal["title"]
        db.session.commit()

        return make_response({"goal":goal.to_dict()}, 200)

@goals_bp.route("/<id>/tasks", methods=["POST", "GET", "PUT", "DELETE"])
def goals_tasks(id):
    goal = validate_id(Goal, id)
    if request.method == "POST":
        task_ids = request.get_json()["task_ids"]
        for id in task_ids:
            task = validate_id(Task, id)
            task.goal = goal
            db.session.commit()
        return make_response(jsonify({"id":goal.goal_id, "task_ids":task_ids}), 200)
    elif request.method == "GET":
        response = goal.to_dict()
        response["tasks"] = [task.to_dict() for task in goal.tasks]
        return make_response(jsonify(response), 200)

