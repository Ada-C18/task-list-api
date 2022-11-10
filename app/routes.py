from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import os, requests
from dotenv import load_dotenv


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# ======== vaildating function ===============================
def validate_model(cls, model_id):
        try:
                model_id = int(model_id)
        except:
                abort(make_response({"message":f"{cls.__name__} {model_id} is invalid."}, 400))
        model = cls.query.get(model_id)
        if not model:
                abort(make_response({"message":f"{cls.__name__} {model_id} does not exist."}, 404))
        return model


#======== TASK ROUTES =========================================
#======== create a task =======================================
@tasks_bp.route("", methods=["POST"])
def create_task():
        request_body = request.get_json()
        try:
                new_task = Task(title=request_body["title"],
                description=request_body["description"])
        except KeyError:
                abort(make_response({"details":f"Invalid data"}, 400))
        else:
                db.session.add(new_task)
                db.session.commit()
        return jsonify({f"task": new_task.to_dict()}), 201

#======== get task(s) ==========================================
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
        title_query = request.args.get("title")
        sort_query = request.args.get("sort")
        id_sort = request.args.get("task_id")
        if sort_query == "asc": 
                tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
                tasks = Task.query.order_by(Task.title.desc()).all()
        elif title_query:
                tasks = Task.query.get(title=title_query)
        elif id_sort:
                tasks = Task.query.order_by(Task.task_id.desc()).all()
        else:
                tasks = Task.query.all()
        task_response = []
        for task in tasks:
                task_response.append(task.to_dict())
        return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
        task = validate_model(Task, task_id)
        return {f"task": task.from_dict()}, 200

#======== upate task ==========================================
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
        task = validate_model(Task, task_id)
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()
        return {f"task": task.to_dict()}, 200

#========= complete, incomplete, post to slack ===============
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_task_incomplete(task_id):
        task = validate_model(Task, task_id)
        task.completed_at = None

        db.session.commit()
        return {f"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_task_complete(task_id):
        task = validate_model(Task, task_id)
        task.completed_at = datetime.now()

        db.session.commit()
        post_message(task)
        return {f"task": task.to_dict()}, 200

def post_message(task):
        KEY = os.environ.get("SLACK_TOKEN")
        # PATH = "https://hooks.slack.com/services/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"
        PATH = "https://slack.com/api/chat.postMessage"
        HEADER = {"Authorization": KEY}
        PARAMS = {"channel": "task-completed","text": f"Someone just completed the task {task}."}
        requests.post(url=PATH, data=PARAMS, headers=HEADER)

#========= delete task ======================================
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
        task = validate_model(Task, task_id)
        task_dict = task.to_dict()

        db.session.delete(task)
        db.session.commit()
        return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200



#======== GOAL ROUTES =========================================
#======== create goal =========================================
@goals_bp.route("", methods=["POST"])
def create_goal():
        request_body = request.get_json()
        try:
                new_goal = Goal(title=request_body["title"])
        except KeyError:
                abort(make_response({"details":f"Invalid data"}, 400))
        else:
                db.session.add(new_goal)
                db.session.commit()
        return jsonify({f"goal": new_goal.to_dict()}), 201

#======== get goal(s) =========================================
@goals_bp.route("", methods=["GET"])
def get_all_goals():
        goals = Goal.query.all()

        goal_response = []
        for goal in goals:
                goal_response.append(goal.to_dict())
        return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
        goal = validate_model(Goal, goal_id)
        return {"goal": goal.to_dict()}, 200

#======== delete goal =========================================
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
        goal = validate_model(Goal, goal_id)
        goal_dict = goal.to_dict()

        db.session.delete(goal)
        db.session.commit()
        return {"details": f'goal {goal_id} "{goal.title}" successfully deleted'}, 200

#======== update goal =========================================
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
        request_body = request.get_json()
        goal = validate_model(Goal, goal_id)
        goal.title = request_body["title"]

        db.session.commit()
        return {"goal": goal.to_dict()}, 200


#======== post tasks to goals ==================================
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
        goal = validate_model(Goal, goal_id)
        request_body = request.get_json()

        task_ids = []
        for task_id in request_body["task_ids"]:
                task = validate_model(Task, task_id)
                goal.tasks.append(task)
                task_ids.append(task_id)
        
        db.session.commit()
        
        return jsonify({"id": goal.goal_id,
                "task_ids" : task_ids}), 200


#======== get specific task with goal id ========================
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
        goal = validate_model(Goal, goal_id)
        tasks_response = [task.goals_dict() for task in goal.tasks]
        
        return jsonify({"id": goal.goal_id,
                "title": goal.title,
                "tasks": tasks_response}), 200