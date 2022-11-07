from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os  
import requests


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")