import os
import requests
from app.models.task import Task


def sendSlackNotification(title):
    url = 'https://slack.com/api/chat.postMessage'
    header = {
        'Authorization': os.environ.get(
            "SLACK_AUTH_TOCKEN"),
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }
    guery = {"channel": "task-notifications",
             "text": f"Someone just completed the task {title}"}
    return requests.post(url=url, headers=header, params=guery)
