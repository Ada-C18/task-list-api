from flask import Blueprint

#Creating Task Blueprint (instantiating new Blueprint instance)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")