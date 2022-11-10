from flask import  jsonify, abort, make_response

def get_one_obj_or_abort(cls, obj_id):
    validate_id(obj_id, 'ID')
    matching_obj = cls.query.get(obj_id)
    return matching_obj

def validate_id(id, str):
    try:
        id = int(id)
    except ValueError:
        response_str = f"Invalid {str}: `{id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))
    
