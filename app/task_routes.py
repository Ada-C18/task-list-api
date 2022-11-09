import datetime, logging, os
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import abort, Blueprint, jsonify, make_response, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id, action):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"Could not {action} {cls.__name__} \'{model_id}\' as it is invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"Could not {action} {cls.__name__} {model_id} as it was not found"}, 404))
    
    return model


def return_goal_from_goal_title(goal_title):
    goal = Goal.query.filter(Goal.title==goal_title).first()
    if goal is None:
        new_goal = Goal.from_dict({"title":goal_title})
        
        db.session.add(new_goal)
        db.session.commit()
        return new_goal
    else:
        return goal




@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id, "get")
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort") 
    if sort_query == "asc":
        sort_method = Task.title.asc()
    elif sort_query == "desc":
        sort_method = Task.title.desc()
    else:
        sort_method = None
    
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query).order_by(sort_method).all()
    else:
        tasks = Task.query.order_by(sort_method).all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def post_a_task():
    request_body = request.get_json()

    try:
        goal_response = return_goal_from_goal_title(request_body["goal"])
    except:
        goal_response = None
    
    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            goal=goal_response
        )

        db.session.add(new_task)
        db.session.commit()
    
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task_to_update = validate_model(Task, task_id, "update")
    request_body = request.get_json()
    if "goal" in request_body:
        goal_response = return_goal_from_goal_title(request_body["goal"])
    else:
        goal_response = None

    try:
        task_to_update.title = request_body["title"]
        task_to_update.description = request_body["description"]
        task_to_update.goal = goal_response
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400

    db.session.commit()
    return jsonify({"task": task_to_update.to_dict()}), 200
    
@tasks_bp.route("/<task_id>", methods=["PATCH"])
def add_goal_to_task(task_id):
    task_to_update = validate_model(Task, task_id, "update")
    request_body = request.get_json()

    try:
        goal_to_update = validate_model(Goal, request_body["goal"], "update")
        task_to_update.goal = goal_to_update
    except:
        return jsonify({"msg": "Missing goal data"}), 400

    db.session.commit()
    return jsonify({"task": task_to_update.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_model(Task, task_id, "delete")

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f"Task {task_to_delete.task_id} \"{task_to_delete.title}\" successfully deleted"}), 200

client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
logger = logging.getLogger(__name__)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_one_task_as_completed(task_id):
    task_to_mark_complete = validate_model(Task, task_id, "mark complete")

    task_to_mark_complete.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    # if not task_to_mark_complete.completed_at:
    #     task_to_mark_complete.completed_at = datetime.datetime.utcnow()
    #     db.session.commit()
    # else:
    #     return jsonify({"message": f"Task <{task_to_mark_complete.title.title()}> has already been completed"}), 200

    try:
        result = client.chat_postMessage(
            channel="C0495RTF6LV",
            text=f"Someone just completed the task <{task_to_mark_complete.title.title()}> on {task_to_mark_complete.completed_at:%m-%d-%Y}"
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posing message: {e}")

    return jsonify({"task": task_to_mark_complete.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_as_incompleted(task_id):
    task_to_mark_incomplete = validate_model(Task, task_id, "mark incomplete")

    task_to_mark_incomplete.completed_at = None
    db.session.commit()
    return jsonify({"task": task_to_mark_incomplete.to_dict()}), 200 
