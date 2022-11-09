
import os #newly added for wave4
import requests #newly added for wave4
from dotenv import load_dotenv

load_dotenv()

path = 'https://slack.com/api/chat.postMessage'
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
channel = "task_notifications"

#2ND SOLUTION FOR SLACKBOT

def slack_message(text):
    
    query_params = {"channel":channel,
                    "text": text
                    }
    headers = {"Authorization":f"Bearer {SLACK_TOKEN}"}
    
    response = requests.post(path, params=query_params, headers=headers)

    return response