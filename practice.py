import requests
import os
from dotenv import load_dotenv

load_dotenv()
def slack_send_message(task):
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    PARAMS = {"channel":"task-notifications",
            "text":f"Someone just completed the task {task.to_dict()['title']}",}
    HEADERS ={
            "Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"
            }
    r = requests.post(url = SLACK_URL, headers= HEADERS, params=PARAMS)
    print(r)