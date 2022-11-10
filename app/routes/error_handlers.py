from flask import request
from . import bp_model, tasks, goals

from sqlalchemy.exc import DataError


@tasks.errorhandler(404)
@goals.errorhandler(404)
def handle_not_found(e):
    model, model_name = bp_model(request.blueprint)
    return {"details": f"{model.__name__} not found"}, 404


@tasks.errorhandler(KeyError)
@goals.errorhandler(KeyError)
def handle_invalid_data(e):
    return {"details": "Invalid data"}, 400


@tasks.errorhandler(ValueError)
@goals.errorhandler(ValueError)
def handle_invalid_data(e):
    return {"details": str(e)}, 400


@tasks.errorhandler(DataError)
@goals.errorhandler(DataError)
def handle_invalid_id(e):
    model, model_name = bp_model(request.blueprint)
    return {"details": f"Invalid {model.__name__} id"}, 400
