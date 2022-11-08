from app import db
from app.models.goal import Goal
from .route_helpers import validate_model, send_slack_message
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")
