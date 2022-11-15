from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

goal_bp = Blueprint("goal_bp", __name__, url_prefix = "/goals")

