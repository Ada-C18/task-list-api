from flask import Blueprint, jsonify, make_response, request, abort,Response
from app import db
from app.models import goal
from app.models.goal import Goal


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goal")