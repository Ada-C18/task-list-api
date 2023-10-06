from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.routes_helper import *


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Create a new goal
@goals_bp.route("", methods=["POST"])
def create_goal():

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
    
    goals_response = [ goal.to_dict() for goal in goals ]

    # goals_response = []
    # for goal in goals:
    #     goals_response.append( 
    #         {
    #             "id": goal.goal_id,
    #             "title": goal.title,
    #         }
    #     )
    
    return jsonify(goals_response)


#Get One goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    return {
        "goal": goal.to_dict()
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
        id = int(id)
        #gets the task object/dictionary
        task = Task.query.get(id)
        task.goal_id = goal_id
        print(task.goal_id)

    db.session.commit()

    return jsonify({
        "id": task.goal_id,
        "task_ids": request_body["task_ids"]
    })


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_with_task(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    #create a brand new list
    #add dict version of each task instance via goal.tasks
    task_list = []
    # iterate over goal.tasks
    for task in goal.tasks:
        if goal_id:

    # append each task dict to goal_list
            task_list.append({
                "id": task.task_id,
                "goal_id":int(goal_id),
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })
        else:
            task_list.append({
                "id": task.task_id,
                "goal_id": int(goal_id),
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })
    
    response_body = jsonify({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": task_list
    })

    return response_body