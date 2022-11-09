from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.goal import Goal
from app.routes.task import get_task_from_id
 


goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal= Goal(title=request_body['title'])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_response()), 201


@goal_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    result = []
    for item in goals:
        result.append(item.to_dict())
    return jsonify(result), 200


@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    chosen_goal = get_goal_from_id(goal_id)
    return jsonify(chosen_goal.to_response()), 200

@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):  
    update_goal = get_goal_from_id(goal_id)
    request_body = request.get_json()   
    try:
        update_goal.title = request_body["title"]  
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    db.session.commit()
    return jsonify(update_goal.to_response()), 200


@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal_to_delete = get_goal_from_id(goal_id)
    db.session.delete(goal_to_delete)
    db.session.commit()
    return jsonify({"details": f"Goal {goal_to_delete.goal_id} \"{goal_to_delete.title}\" successfully deleted"}), 200 

'''
# nested route GET
@goal_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_goal(goal_id):
    goal = get_task_from_id(Goal, goal_id)

    # breakfasts = []
    # for item in menu.breakfast_items:
    #     breakfasts.append(item.to_dict())

    tasks = goal.get_breakfast_list()   
    return jsonify(tasks), 200
'''

# nested route POST
@goal_bp.route('/<goal_id>/tasks', methods=['POST'])
def post_tasks_for_goal(goal_id): 
    # task_items = lists of Task Objects
    # task_ids = list of integers
    
    new_goal = get_goal_from_id(goal_id) 
    request_body = request.get_json() 
    input_task_ids = request_body["task_ids"]
    #new_goal = Goal(task_items=request_body['task_items'])
    task_id_list = []
    for task_id in input_task_ids:
        task_obj = get_task_from_id(task_id)
        # matching
        task_obj.goal_id = new_goal.goal_id
        task_id_list.append(task_obj.task_id)

    
    #db.session.add(new_goal)
    db.session.commit()
    return jsonify({
                "id": new_goal.goal_id, 
                "task_ids": task_id_list
                }), 200


# nested route GET
@goal_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_goal(goal_id):  
    new_goal = get_goal_from_id(goal_id)
    res_tasks = []
    for task in new_goal.tasks:
        res_tasks.append(task.to_dict())
    return jsonify({
            "id": new_goal.goal_id,
            "title":new_goal.title,
            "tasks":res_tasks
                }), 200


'''
       "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": [
            {
                "id": 1,
                "goal_id": 1,
                "title": "Go on my daily walk 🏞",
                "description": "Notice something new every day",
                "is_complete": False
            }
'''


# helper
def get_goal_from_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        # abort: stop looking for unfound; make_response: route decorate 
        return abort(make_response({"msg": f"invalid data type: {goal_id}"}, 400))
    chosen_goal = Goal.query.get(goal_id)
    if chosen_goal is None:
        return abort(make_response("", 404))  
    return chosen_goal   