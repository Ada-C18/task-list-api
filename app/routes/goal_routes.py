from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.routes_helper import *


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Create a new goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()


    try:
        request_body = request.get_json() 
        new_goal = Goal(
            title=request_body["title"]
            )
            
    except KeyError:
        return {"details": "Invalid data"}, 400

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
    
    goals_response = []
    for goal in goals:
        goals_response.append( 
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    
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

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
        }


# Defining Endpoint and Creating Route Function to UPDATE a Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)
    # goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    

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
    goal = get_record_by_id(Goal, goal_id)
    # goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

# ------------------------------- NESTED ROUTES ---------------------------------------------------
# Send a list of tasks IDs to a specific goal (ID)
#   get a list of all tasks with the provided task ids
#   set each task FK with the goal id
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
# 

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def give_task_to_goal(goal_id):
    request_body = request.get_json()
    
    #accessing the list of task_ids
    request_body["task_ids"]
    for id in request_body["task_ids"]:
        
        #gets the task object/dictionary
        #sets task FK to goal ID
        task = Task.query.get(id)
        task.goal_id = int(goal_id)


    db.session.commit()

    return jsonify({
        "id": task.goal_id,
        "task_ids": request_body["task_ids"]
    })

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_with_task(goal_id):
    goal = get_record_by_id(Task, goal_id)
    
    tasks = []

    response_body = jsonify({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks
    })


    # return response_body

    # return goal


    return response_body
