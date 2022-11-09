from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.routes_helper import *
from flask import Blueprint, jsonify, abort, make_response, request


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Create a new goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal.from_dict(request_body)
    # ------------ ^^ refactored ^^ ------------------------------

    # try:
    #     request_body = request.get_json() 
    #     new_goal = Goal(
    #         title=request_body["title"]
    #         )
            
    # except KeyError:
    #     return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title,
        }
        }, 201

#Get All goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()
    
    # goals_response = []
    # for goal in goals:
    #     goals_response.append( 
    #         {
    #             "id": goal.goal_id,
    #             "title": goal.title,
    #         }
    #     )
    
    #------------------ ^^ refactored ^^ ---------------------------- 
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

# #helper function to validate goal 
# def validate_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         abort(make_response({"details": "Invalid data"}, 400))

#     goal = Goal.query.get(goal_id)

#     if not goal:
#         abort(make_response({"details":f"there is no existing goal {goal_id}"}, 404))
        
#     return goal

#Get One goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)
    # goal = validate_goal(goal_id)

    # return {
    #     "goal": {
    #         "id": goal.goal_id,
    #         "title": goal.title,
    #     }
    #     }

# ---------------- ^^refactored return statement^^ --------------------
    return goal.to_dict(), 200

# Defining Endpoint and Creating Route Function to UPDATE a Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    # goal = validate_goal(goal_id)

    request_body = request.get_json()

    # goal.title = request_body["title"]
    goal.update(request_body)

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
        }


#Defining Endpoint and Creating Route Function to DELETE a goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

# ------------------------------- Nested Routes ---------------------------------------------------
#Create a task by a specific goal
