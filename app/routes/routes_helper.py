from flask import jsonify, abort, make_response

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))


def get_record_by_id(cls, id):
    # handled invalid data types
    try:
        id = int(id)
    except ValueError:
        error_message("Invalid data", 400)

    # check if id exists in db
    model = cls.query.get(id)
    if model: 
        return model 

    if cls.__name__ == "Goal":
        error_message(f"there is no existing goal {id}", 404)

    error_message(f"there is no existing task {id}", 404)
    