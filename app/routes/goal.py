from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))

    return goal


def validate_dict_title(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False)):
        abort(make_response({"details": "Invalid data"}, 400))


@bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():
    sort_query = request.args.get("sort")

    goal_query = Goal.query

    if sort_query:
        goal_query = goal_query.order_by(Goal.title.desc()) if sort_query == "desc" else goal_query.order_by(Goal.title.asc())

    goals = goal_query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


@bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    goal_response = {
        "goal": goal.to_dict()
    }
    return jsonify(goal_response)


@bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()
    validate_dict_title(request_body)
    new_goal = Goal.goal_from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response_body), 201)


@bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()
    validate_dict_title(request_body)

    goal.title = request_body["title"]

    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return jsonify(response_body)


@bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    goal_id = goal.goal_id
    goal_title = f"\"{goal.title}\""

    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f"Goal {goal_id} {goal_title} successfully deleted"
    }

    return jsonify(response_body)


# @bp.route("/<id>/mark_complete", methods=["PATCH"])
# def mark_goal_complete(id):
#     goal = validate_goal(id)

#     goal.completed_at = date.today()
#     goal.is_complete = True

#     db.session.commit()

#     send_completed_message(goal)
#     response_body = {"goal": goal.to_dict()}

#     return jsonify(response_body)

# @bp.route("/<id>/mark_incomplete", methods=["PATCH"])
# def mark_goal_incomplete(id):
#     goal = validate_goal(id)

#     goal.completed_at = None
#     goal.is_complete = False

#     db.session.commit()

#     response_body = {"goal": goal.to_dict()}

#     return jsonify(response_body)
