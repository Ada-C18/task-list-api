import requests 
import os 

class SlackClient():
    def post_message_to_my_channel(self, notification_message):
        access_token=os.environ.get("SLACK_BOT_ACCESS_TOKEN")
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {access_token}'})

        query= { 'channel': 'my-task-notifications', 'text': f'{notification_message}' }
        session.get('https://slack.com/api/chat.postMessage', params=query)