from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort


goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({'message':f'goal {id} invalid'}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({'message':f'Goal {id} not found'}, 404))

    return goal

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    all_goals = Goal.query.all()
    goal_response = [goal.to_dict() for goal in all_goals]

    return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<id>", methods=["GET"])
def handle_goal(id):
    goal = validate_goal(id)

    return {"goal": {
    "id": goal.id,
    "title": goal.title}
}

@goals_bp.route("", methods=["POST"])

def create_goal():
    request_body = request.get_json()

    # guard clause
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    new_goal= Goal(
        title=request_body['title']
       )
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({'goal': new_goal.to_dict()}), 201)


@goals_bp.route("/<id>", methods=["PUT"])
def edit_goal(id):
    
    goal = validate_goal(id)
    request_body = request.get_json()

    goal.title=request_body["title"]
    

    db.session.commit()

    return make_response(jsonify({'goal': goal.to_dict()}), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    
    db.session.delete(goal)
    db.session.commit()
    response_body = {"details": f'Goal {goal.id}"{goal.title}" successfully deleted'}

    #return {"details": f'Goal {goal.id}"{goal.title}" successfully deleted'}, 200
    return make_response(jsonify({"details": f"Goal {goal.id} {goal.title} successfully deleted"}))


# one to many(trial and error)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_id_to_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    tasks = [validate_task(task_id) for task_id in task_ids]
   
    for task in tasks:
        task.goal_id = goal.id

    # db.session.add(task) #Not needed?
    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": task_ids,
    })

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)

    
    tasks = [Task.to_dict(task) for task in goal.tasks]

    response_body = jsonify({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks
    })
    # print(response_body["tasks"])
    
    return jsonify({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks
    })