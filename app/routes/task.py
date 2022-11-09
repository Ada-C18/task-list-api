from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import date
import os #newly added for wave4
import requests #newly added for wave4
from app.models.goal import Goal
from app import SLACK_URL
from app.routes.slack_bot import slack_message


# goal_bp = Blueprint("goal",__name__,url_prefix="/goals")
task_bp = Blueprint("task", __name__, url_prefix="/tasks")

########################## WAVE 1 ##########################
#HELPER FUNCTIONS
def get_model_from_id(cls,model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message":f"data type {model_id} is invalid"},400))

    chosen_object = cls.query.get(model_id)
    
    if chosen_object is None:
        abort(make_response({"message":f"Could not find {cls.__name__} item with id: {model_id}"},404))

    return chosen_object

def get_all_objects(cls):    
    '''source: https://riptutorial.com/sqlalchemy/example/12146/order-by'''
    
    title_query_sort = request.args.get("sort")
    if title_query_sort == "asc":
        objects = cls.query.order_by(cls.title.asc())
    elif title_query_sort == "desc":
        objects = cls.query.order_by(cls.title.desc())    
    else:
        objects = cls.query.all()
    
    result = []
    
    for object in objects:
        result.append(object.to_dict())
    return result

def update_one_object(cls, model_id):
    update_object = get_model_from_id(cls,model_id)
    request_body = request.get_json()

    if cls == Task:
        update_object.title = request_body["title"]
        update_object.description = request_body["description"]
    elif cls == Goal:
        update_object.title = request_body["title"]
    return update_object

##END ROUTES
@task_bp.route('', methods=['GET'])
def get_all_tasks():    
    result = get_all_objects(Task)
    return jsonify(result), 200

##End route to get one task
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_model_from_id(Task,task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
        
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}),400

    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_dict()}), 201

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):    
    try:        
        update_task = update_one_object(Task, task_id)        
    except KeyError:
        return jsonify({"details": "Invalid data"}),400
                
    db.session.commit()
    return jsonify({"task":update_task.to_dict()}),200
    
@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_model_from_id(Task,task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return jsonify({"details":f"Task {task_id} \"{task_to_delete.title}\" successfully deleted"}), 200

########################## WAVE 3 ##########################
@task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_one_task(task_id):
    chosen_task = get_model_from_id(Task,task_id)      
    chosen_task.completed_at = date.today()    
    db.session.commit()
        
    slack_message("Someone just completed the task {chosen_task.title}")

    return jsonify({"task":chosen_task.to_dict()}), 200

# #2ND SOLUTION FOR SLACKBOT USING BUILT-IN WEBHOOKS FEATURES
# @task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
# def mark_complete_one_task(task_id):
    
#     chosen_task = get_model_from_id(Task,task_id)      
#     chosen_task.completed_at = date.today()    
#     db.session.commit()
    
#     # SLACK_URL = os.environ.get("SLACK_URL") #This is now under app.__init__.py

#     data = '{"text":"%s"}' % f"Someone just completed the task {chosen_task.title}"
    
#     requests.post(SLACK_URL, data)        
    
#     return jsonify({"task":chosen_task.to_dict()}), 200


@task_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete_one_task(task_id):
    chosen_task = get_model_from_id(Task,task_id)
    chosen_task.completed_at = None
    db.session.commit()
    
    
    return jsonify({"task":chosen_task.to_dict()}), 200
    
# ########################## WAVE 5 ##########################
# @goal_bp.route('', methods=["GET"])
# def get_all_goals():
#     result = get_all_objects(Goal)
#     return jsonify(result), 200

# @goal_bp.route('/<goal_id>', methods=["GET"])
# def get_one_goal(goal_id):
#     chosen_goal = get_model_from_id(Goal,goal_id)
#     return jsonify({"goal":chosen_goal.to_dict()}), 200

# @goal_bp.route('', methods=["POST"])
# def create_one_goal():
#     request_body = request.get_json()    
#     try:
#         new_goal = Goal.from_dict(request_body)
#     except KeyError:
#         return jsonify({"details": "Invalid data"}),400
    
#     db.session.add(new_goal)
#     db.session.commit()
#     return jsonify({"goal":new_goal.to_dict()}), 201

# @goal_bp.route('/<goal_id>', methods=["PUT"])
# def update_one_goal(goal_id):
#     try:
#         update_goal = update_one_object(Goal,goal_id)
#     except KeyError:
#         return jsonify({"details": "Invalid data"}),400
    
#     db.session.commit()
#     return jsonify({"goal":update_goal.to_dict()}),200

# @goal_bp.route('/<goal_id>', methods=["DELETE"])
# def delete_one_goal(goal_id):
#     goal_to_delete = get_model_from_id(Goal,goal_id)
    
#     db.session.delete(goal_to_delete)
#     db.session.commit()
#     return jsonify({"details":f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted"}), 200


# @goal_bp.route('<goal_id>/tasks', methods=["POST"])
# def create_task_id_to_goal(goal_id):
#     goal = get_model_from_id(Goal,goal_id)
#     request_body = request.get_json()

#     task_list =[]
#     for task_id in request_body["task_ids"]:
#         task = get_model_from_id(Task, task_id)
#         # if task:
#         task.goal_id = goal.goal_id
#         task_list.append(task.task_id)
    
#     db.session.commit()

#     return jsonify({"id":goal.goal_id, "task_ids": task_list}), 200

# @goal_bp.route('<goal_id>/tasks', methods =["GET"])
# def get_tasks_from_goal_id(goal_id):
#     goal = get_model_from_id(Goal, goal_id)
#     tasks = goal.get_task_list()
    
#     return jsonify(goal.to_dict_task_id()), 200
    
