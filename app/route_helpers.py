import os, requests
from flask import abort, make_response

key = os.environ.get("SLACK_BOT_TOKEN")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"details":f"No {cls.__name__} with ID {model_id} in database"}, 404))

    return model

def send_slack_message(msg_body):
    payload = {"channel":"task-notifications","text":str(msg_body)}
    header = {'Authorization':str('Bearer ' + key)}
    r = requests.post('https://slack.com/api/chat.postMessage', headers=header, params=payload)
    return r