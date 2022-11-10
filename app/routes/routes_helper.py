
from app import db
from datetime import date
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
import requests, os


#Helper function:

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))
    
    matching_task = Task.query.get(task_id)

    if not matching_task:
        response_str = f"Task with id `{task_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task


#helper function goal
def get_one_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response_str = f"Invalid goal_id: `{goal_id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))
    print("goal_id ",goal_id)
    
    matching_goal = Goal.query.get(goal_id)
    
    print("matching_goal ", matching_goal)
    
    if not matching_goal:
        response_str = f"Goal with id `{goal_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_goal





