from app import db
from flask import Blueprint, jsonify, abort, make_response, request

#Parent 
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)
