from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import datetime
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")