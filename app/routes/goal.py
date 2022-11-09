from flask import Blueprint, jsonify, request, abort, make_response
from app.models.goal import Goal
from app import db
from .task import get_task_from_id

goal_bp = Blueprint("goal", __name__, url_prefix = "/goals")

# Helper function
def get_goal_from_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"message" : f"{goal_id} is invalid"}, 400))

    chosen_goal = Goal.query.get(goal_id)
    
    if chosen_goal is None:
        return abort(make_response({'msg': f' Could not find goal item with id : {goal_id}'}, 404))
     
    return chosen_goal


@goal_bp.route('', methods= ['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body['title'])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal':new_goal.to_dict()}), 201


@goal_bp.route('', methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response = []
    for goal in goals:    
        response.append(goal.to_dict())
    
    return make_response(jsonify(response), 200)


@goal_bp.route('/<goal_id>', methods= ["GET"])
def get_one_goal(goal_id):
    
    chosen_goal = get_goal_from_id(goal_id)

    return make_response(jsonify({'goal':chosen_goal.to_dict()}),200)


@goal_bp.route('/<goal_id>', methods= ['PUT'])
def update_one_goal(goal_id):

    update_goal= get_goal_from_id(goal_id)

    request_body = request.get_json()
    try: 
        update_goal.title = request_body["title"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400
        
    db.session.commit()
    return jsonify({'goal':update_goal.to_dict()}), 200


@goal_bp.route('/<goal_id>', methods= ['DELETE'])
def delete_one_goal(goal_id):

    goal_to_delete = get_goal_from_id(goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({
             "details": f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'
            }), 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def sending_tasks_to_goal(goal_id):

    goal = get_goal_from_id(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = get_task_from_id(task_id)
        task.goal_id = goal_id
        db.session.add(task)
        db.session.commit()

    return make_response(jsonify({"id":goal.goal_id, "task_ids":request_body["task_ids"]}), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    
    goal = get_goal_from_id(goal_id)
    tasks_list=[]
    for task in goal.tasks:
        tasks_list.append(task.to_dict())
        
    goal_dict = goal.to_dict()
    goal_dict['tasks']=tasks_list
    
    
    return jsonify(goal_dict), 200
    
    

