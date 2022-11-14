from flask import jsonify, abort, make_response

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_record_by_id(cls, task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        error_message(f"Invalid id {task_id}", 404)

    model = cls.query.get(task_id)
    if model:
        return model

    error_message(f"No model of type {cls.__name__} with id {task_id} found", 404)