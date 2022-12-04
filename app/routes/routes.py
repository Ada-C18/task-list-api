# from flask import Blueprint, jsonify, request, abort, make_response
# from app import db
# from app.models.task import Task
# from app.models.goal import Goal
# from datetime import datetime
# import requests
# import os

# task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message":f"Invalid {cls.__name__}: `{model_id}`. ID must be an integer"}, 400))
    
#     model = cls.query.get(model_id)
#     if not model:
#         abort(make_response({"message":f"{cls.__name__} with id `{model_id}` was not found in the database."}, 404))
#     return model


# @task_bp.route("", methods=["POST"])
# def add_task():
#     request_body = request.get_json()
    
#     if "title" not in request_body or \
#         "description" not in request_body:
#             return jsonify({"details": "Invalid data"}), 400

#     new_task = Task.from_dict(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     task_dict = Task.to_dict(new_task)
    
#     return jsonify({"task": task_dict}), 201


# @task_bp.route("", methods=["GET"])
# def get_all_tasks():
#     sort_param = request.args.get("sort")
    
#     tasks = Task.query.all()

#     response = []
#     for task in tasks:
#         task_dict = Task.to_dict(task)
#         response.append(task_dict)
    
#     if sort_param == "asc":
#         response = sorted(response, key=lambda task: task['title'])
#     elif sort_param == "desc":
#         response = sorted(response, key=lambda task: task['title'], reverse=True)

#     return jsonify(response), 200



# @task_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
#     selected_task = validate_model(Task, task_id)

#     task_dict = Task.to_dict(selected_task)

#     return jsonify({"task": task_dict}), 200

# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     selected_task = validate_model(Task, task_id)
    
#     selected_task.completed_at = datetime.today()
#     db.session.add(selected_task)
#     db.session.commit()

#     task_dict = Task.to_dict(selected_task)

#     slack_path = "https://slack.com/api/chat.postMessage"
#     SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
#     headers = {
#         "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
#     }
#     paramaters = {
#         "channel": "task-notifications",
#         "text": f"Someone just completed the task {selected_task.title}"
#     }
    
#     requests.get(url=slack_path, headers=headers, params=paramaters)

#     return jsonify({"task": task_dict}), 200

# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_task_incomplete(task_id):
#     selected_task = validate_model(Task, task_id)

#     selected_task.completed_at = None

#     db.session.add(selected_task)
#     db.session.commit()

#     task_dict = Task.to_dict(selected_task)

#     return jsonify({"task": task_dict}), 200

# @task_bp.route("<task_id>", methods=["PUT"])
# def update_one_task(task_id):
#     selected_task = validate_model(Task, task_id)
    
#     request_body = request.get_json()

#     if "title" not in request_body or \
#         "description" not in request_body:
#             return jsonify({"message": "Request must include title and description"}), 400

#     selected_task.title = request_body["title"]
#     selected_task.description = request_body["description"]

#     db.session.commit()
    
#     task_dict = Task.to_dict(selected_task)
#     return jsonify({"task": task_dict}), 200

# @task_bp.route("/<task_id>", methods=["DELETE"])
# def delete_one_task(task_id):
#     selected_task = validate_model(Task, task_id)

#     db.session.delete(selected_task)
#     db.session.commit()

#     return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200

# goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# @goals_bp.route("", methods=["POST"])
# def create_goal():
#     request_body = request.get_json()
#     if "title" not in request_body:
#         return jsonify({"details": "Invalid data"}), 400
    
#     new_goal = Goal.from_dict(request_body)

#     db.session.add(new_goal)
#     db.session.commit()

#     goal_dict = Goal.to_dict(new_goal)

#     return jsonify({"goal": goal_dict}), 201


# @goals_bp.route("", methods=["GET"])
# def get_all_goals():
#     goals = Goal.query.all()

#     response = []

#     for goal in goals:
#         goal_dict = {
#             "id": goal.goal_id,
#             "title": goal.title
#         }
#         response.append(goal_dict)
    
#     return jsonify(response), 200

# @goals_bp.route("/<goal_id>", methods=["GET"])
# def get_one_goal(goal_id):
#     selected_goal = validate_model(Goal, goal_id)

#     goal_dict = Goal.to_dict(selected_goal)

#     return jsonify({"goal": goal_dict}), 200

# @goals_bp.route("/<goal_id>", methods=["PUT"])
# def update_goal(goal_id):
#     selected_goal = validate_model(Goal, goal_id)

#     request_body = request.get_json()

#     if "title" not in request_body:
#         return jsonify({"message": "Request must include title and description"}), 400

#     selected_goal.title = request_body["title"]

#     db.session.commit()
    
#     goal_dict = Goal.to_dict(selected_goal)
#     return jsonify({"goal": goal_dict}), 200

# @goals_bp.route("/<goal_id>", methods=["DELETE"])
# def delete_one_goal(goal_id):
#     selected_goal = validate_model(Goal, goal_id)

#     db.session.delete(selected_goal)
#     db.session.commit()

#     return jsonify({"details": f'Goal {goal_id} "{selected_goal.title}" successfully deleted'}), 200

# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def send_goal_ids_to_task(goal_id):
#     selected_goal = validate_model(Goal, goal_id)
#     request_body = request.get_json()
    
    
#     for task_id in request_body["task_ids"]:
#         valid_task = validate_model(Task, task_id)
#         valid_task.goals = selected_goal
#         db.session.commit()
    
#     task_id_list = [task.task_id for task in selected_goal.tasks]
    
#     response_body = {
#         "id": selected_goal.goal_id,
#         "task_ids": task_id_list
#     }
#     return jsonify(response_body), 200

# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_tasks_of_one_goal(goal_id):
#     selected_goal = validate_model(Goal, goal_id)

#     task_list = []
#     for task in selected_goal.tasks:
#         task_list.append(Task.to_dict(task))
    
#     goal_dict = {
#         "id": selected_goal.goal_id,
#         "title": selected_goal.title,
#         "tasks": task_list
#     }

#     return jsonify(goal_dict), 200