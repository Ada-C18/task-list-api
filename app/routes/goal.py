from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("goals_bp", __name__, url_prefix="/goals/", strict_slashes=False)