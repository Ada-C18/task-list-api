from flask import make_response, abort
import os
import requests

# Helper Functions
def validate_id(class_obj, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details":f"Invalid {class_obj.__name__} id"},400))
    obj = class_obj.query.get(id)
    if not obj:
        abort(make_response({"details":f"{class_obj.__name__} not found"},404))
    else:
        return obj

def mark_truthy_falsy(mark):
    if mark == "mark_complete":
        return True
    elif mark == "mark_incomplete":
        return False

def slack_send_new_task(task):
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    PARAMS = {"channel":"task-notifications",
              "text":f"New Task: {task.title} {task.task_id}"
             }
    HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    requests.post(url = SLACK_URL, headers=HEADERS, params=PARAMS)

def slack_send_completed_task(task):
    # connect to Slack API to send a message to the task-notifications channel
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    PARAMS = {"channel":"task-notifications",
                "text":f"Someone just completed the task {task.title}"
                }
    HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    requests.post(url = SLACK_URL, headers=HEADERS, params=PARAMS)

def slack_get_channel_history():
    SLACK_URL = "https://slack.com/api/conversations.history"
    PARAMS = {"channel":"C04AJDQ14M6"
                }
    HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    r = requests.get(url = SLACK_URL, headers=HEADERS, params=PARAMS)
    return(r)

def slack_get_message(task):
    history = slack_get_channel_history()
    
    for message_info in history.json()["messages"]:
        if message_info["text"] == f"New Task: {task.title} {task.task_id}":
            ts = message_info["ts"]
            return ts

def slack_add_check(task):
    message_ts = slack_get_message(task)
    SLACK_URL = "https://slack.com/api/reactions.add"
    PARAMS = {"channel":"C04AJDQ14M6", "name":"white_check_mark", "timestamp":message_ts}
    HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    r = requests.get(url = SLACK_URL, headers=HEADERS, params=PARAMS)
    
