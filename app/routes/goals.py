from flask import request, jsonify
from app import db
from app.models.goal import Goal
from . import goals


@goals.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@goals.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    request_body = request.get_json()
    goal.add_tasks(request_body["task_ids"])
    db.session.commit()
    return {"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}, 200


@goals.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return goal.to_dict(tasks=True), 200
