from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime as dt
import requests
import os

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")