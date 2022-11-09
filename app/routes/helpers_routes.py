from flask import jsonify, abort, make_response
from dotenv import load_dotenv
import os
import requests


def validate_obj(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"Invalid ID: {obj_id}. ID must be an integer"
        abort(make_response(jsonify({"message": response_str}), 400))

    obj = cls.query.get(obj_id)

    if not obj:
        response_str = f"{cls.__name__} with id {obj_id} was not found."
        abort(make_response(jsonify({"message": response_str}), 404))

    return obj


# INTEGRATE SLACK API
def send_slack_message(message):
    try:
        PATH = "https://slack.com/api/chat.postMessage"
        API_KEY = os.environ.get("SLACK_API_KEY")

        headers = {"Authorization": API_KEY}

        post_body = {
            "channel": "task-notifications",
            "text": message
        }

        requests.post(
            PATH, params=post_body, headers=headers)
    except:
        print(f"Message to Slack failed")
