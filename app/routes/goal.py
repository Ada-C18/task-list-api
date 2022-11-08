
from app import db
from flask import Blueprint,jsonify,request,abort,make_response
from app.models.goal import Goal
from app.models.task import Task
import os,requests
from .helper_function import get_model_from_id

goal_bp = Blueprint("goal",__name__,url_prefix = "/goals")

@goal_bp.route('',methods =['POST']) 
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal( title = request_body['title'])
            
    except:
        return abort(make_response({"details": "Invalid data"},400))
        
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}),201


@goal_bp.route('',methods = ["GET"])
def get_all_tasks():
    
    goals = Goal.query.all()

    response = []
    for goal in goals:
        response.append(goal.to_dict())

    return make_response(jsonify(response),200) 


@goal_bp.route('/<goal_id>', methods = ["GET"])
def get_one_goal(goal_id):

    chosen_goal = get_model_from_id(Goal,goal_id)

    return make_response(jsonify({"goal":chosen_goal.to_dict()}),200)   


@goal_bp.route('/<goal_id>', methods = ["PUT"])
def update_goal(goal_id):
    update_goal = get_model_from_id(Goal,goal_id)

    request_body = request.get_json()
    
    try:
        update_goal.title = request_body["title"]
       
    except KeyError:
        return jsonify({'msg':"Missing needed data"}),400

    db.session.commit()

    return make_response(jsonify({"goal": update_goal.to_dict()}),200)
    

@goal_bp.route('/<goal_id>', methods = ["DELETE"])
def delete_one_goal(goal_id):
    goal = get_model_from_id(Goal,goal_id)
   
    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}),200)


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = get_model_from_id(Goal,goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = get_model_from_id(Task,task_id)
        task.goal_id = goal_id
        task.goal = goal
    
    # db.session.add(task)
    db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids":request_body["task_ids"]}),200


@goal_bp.route('/<goal_id>/tasks',methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = get_model_from_id(Goal,goal_id)
    
    task_list = []
    for task in goal.tasks:
        task_list.append(task.to_dict())

    goal_dict = goal.to_dict()  
    goal_dict['tasks'] = task_list  

    return make_response(jsonify(goal_dict),200) 