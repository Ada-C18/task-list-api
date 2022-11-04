from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db

goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

"""Goal Routes Start"""
@goal_bp.route("", methods=['POST'])
def create_new_goal():
    response_body = request.get_json()
    
    try:
        new_goal = Goal(
            title=response_body["title"])
    except KeyError:
        return make_response({
        "details": "Invalid data"
    },400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({f"goal":new_goal.goal_dictionfy()}),201)

@goal_bp.route("", methods=['GET'])
def get_all_goals():
    return_list=[]
    match_command = [(key,value) for key,value in request.args.items()]

    if match_command:
        try:
            goals = sort_query_helper(Goal,match_command)
        except ValueError:
            return make_response(jsonify({"warning":"Invalid query sorting parameters"}),400)
    else:
        goals = Goal.query.all()
    
    for goal in goals:
        return_list.append(goal.goal_dictionfy())
    
    return make_response(jsonify(return_list),200)

@goal_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return make_response(jsonify({"goal":goal.goal_dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    response_body = request.get_json()
    goal = validate_model(Goal,goal_id)

    goal.title = response_body["title"]
   
    db.session.commit()

    return make_response(jsonify({f"goal":goal.goal_dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['DELETE'])
def delete_a_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({'details':f'Goal {goal_id} \"{goal.title}\" successfully deleted'}),200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def map_tasks_to_goals(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task,task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"]
    }), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = [task.dictionfy() for task in goal.tasks]
    return_dict = goal.goal_dictionfy()

    return_dict["tasks"] = task_list

    return make_response(jsonify(return_dict),200)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def sort_query_helper(cls,request_dict):
    obj,order = request_dict[0]
    match obj:
        case "sort":
            order_object = cls.title
        case "id_sort":
            order_object = cls.task_id if cls==Task else cls.goal_id #I know there's gonna be a big refactor if I need more than 2 classes to take this but it's what I've got
        case other:
            raise ValueError
    match order:    
        case "desc":
            order_object = order_object.desc()
        case 'asc':
            order_object = order_object.asc()
        case other:
            raise ValueError
    return cls.query.order_by(order_object).all()