from app import db
from app.models.goal import Goal
from flask import Blueprint,jsonify,abort,make_response,request
from app.models.task import Task

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')
GOAL_ID_PREFIX = '/<goal_id>'

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))
    
    return goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response({"goal":new_goal.to_dict()}, 201)

@goals_bp.route("", methods=["GET"])
def get_goals():
    goal_query = Goal.query
    goals = goal_query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })

    return make_response(jsonify(goals_response), 200)
@goals_bp.route(GOAL_ID_PREFIX, methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    return {"goal": goal.to_dict()}

@goals_bp.route(GOAL_ID_PREFIX,methods=['PUT'])
def update_task(goal_id):
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response("Invalid Request, Goal Must Have Title", 400)

    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)
    
    goal.title = request_body["title"]

    db.session.commit()
    return make_response({"goal":goal.to_dict()}, 200)

@goals_bp.route(GOAL_ID_PREFIX, methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)


@goals_bp.route(GOAL_ID_PREFIX + "/tasks", methods=['GET'])
def read_tasks (goal_id):
    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    return_body = goal.to_dict()
    return_body["tasks"] = [task.to_dict_in_goal() for task in goal.tasks]

    return make_response(jsonify(return_body), 200)


@goals_bp.route(GOAL_ID_PREFIX + "/tasks", methods=['POST'])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    request_body = request.get_json()
    tasks_to_assign = request_body["task_ids"]

    for task_id in tasks_to_assign:
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return_body = {}
    return_body["id"] = goal.goal_id
    return_body["task_ids"] = tasks_to_assign

    return make_response(return_body, 200)