from app import db
from sqlalchemy import sql
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
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }
        if self.goal_id:
            task["goal_id"] = self.goal_id
        return task

    def mark_complete(self, when=None):
        self.completed_at = (
            when
            if type(when) is datetime
            else (None if when is False else sql.func.now())
        )
        if self.completed_at is not None:
            slack_oauth_token = os.environ.get("SLACK_OAUTH_TOKEN")
            slack_channel = "task-notifications"
            completed_message = f"Someone just completed the task {self.title}"
            requests.get(
                "https://slack.com/api/chat.postMessage",
                params={"channel": slack_channel, "text": completed_message},
                headers={"Authorization": f"Bearer {slack_oauth_token}"},
            )
