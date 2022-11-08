from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.goal import Goal
from app.models.task import Task


goal_bp = Blueprint('goal_bp', __name__, url_prefix='/goals')


@goal_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()

    goal_response = [{"id": goal.goal_id,"title": goal.title}for goal in goals]

    return jsonify(goal_response)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response({"details":"Id not found"}), 404

    return make_response({ "goal":{
        "id": goal.goal_id,
        "title": goal.title,
    }},200)

# @goal_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_one_goal(goal_id):
    
#     goal = Goal.query.get(goal_id)
#     if not goal:
#         return make_response({"details":"Id not found"}), 404

#     return make_response({ "goal":{
#         "id": goal.goal_id,
#         "title": goal.title,
#     }},200)

@goal_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details":"Invalid data"}), 400

    new_goal = Goal(
        title=request_body["title"],
    )
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({ "goal":{
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }},201)


@goal_bp.route("", methods=["POST"])
def post_task_ids_to_goal(goal_id, task_id):

    request_body = request.get_json()

    goal = Goal.query.get(goal_id)
    task = Task.query.all(task_id)

    # if "title" not in request_body:
    #     return make_response({"details":"Invalid data"}), 400

    new_goal = Goal(
        title=request_body["title"],
    )
    task_list = []
    if goal_id:
        task_list.append(task_id)
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({ "goal":{
        "id": new_goal.goal_id,
        "task_ids": new_goal.task_id
    }},201)




@goal_bp.route("/<goal_id>", methods=["PUT"])
def edit_goal(goal_id):

    goal = Goal.query.get(goal_id)

    request_body = request.get_json(goal_id)
    if not goal:

        return make_response({"details":"Id not found"}), 400

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({ "goal":{
        "id": goal.goal_id,
        "title": goal.title
    }},201)


@goal_bp.route("/<goal_id>", methods=["DELETE"])

def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response({"details":"Id not found"}), 404

    db.session.delete(goal)
    db.session.commit()

    return make_response({f"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'}),200

