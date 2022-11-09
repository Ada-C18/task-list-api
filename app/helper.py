from flask import abort, make_response
import requests
import os
# from app.models.task import Task

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def post_slack(task):
    url = 'https://slack.com/api/chat.postMessage'
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_key = os.environ.get("SLACK_KEY")
    headers = {
        "Authorization": f"Bearer {slack_key}"
    }

    requests.post(url, params=params, headers=headers)