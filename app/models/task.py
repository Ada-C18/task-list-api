from app import db
from datetime import datetime
import requests
import os


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task = {
            "id" : self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id:
            task["goal_id"] = self.goal_id

        return task

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]

    def mark_complete(self, completion_time=None):
        if completion_time is not False:
            self.completed_at = datetime.utcnow()
        else:
            self.completed_at = None

        if self.completed_at is not None:
            SLACKBOT_OAUTH_TOKEN = os.environ.get("SLACKBOT_OAUTH_TOKEN")
            slack_channel = "task-notifications"
            message = f"Someone just completed the task {self.title}"
            requests.get(
                "https://slack.com/api/chat.postMessage",
                params={"channel": slack_channel, "text": message},
                headers = {"Authorization": f"Bearer {SLACKBOT_OAUTH_TOKEN}"}
            )

    @classmethod
    def from_dict(cls, task_data):
        return cls(title=task_data["title"], description=task_data["description"])