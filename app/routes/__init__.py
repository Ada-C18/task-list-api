from flask import Blueprint

tasks = Blueprint("tasks", "tasks", url_prefix="/tasks")
goals = Blueprint("goals", "goals", url_prefix="/goals")

from .tasks import *
from .goals import *
from .routes import *
from .error_handlers import *
