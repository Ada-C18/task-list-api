from flask import  jsonify, abort, make_response

def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    
    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        abort(make_response(jsonify({"details": "Invalid data"}), 404))
    return matching_obj