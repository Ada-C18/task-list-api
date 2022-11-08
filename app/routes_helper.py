from flask import Blueprint, jsonify, request, abort, make_response


def get_one_object_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"Invalid task_id: {obj_id}. ID must be an integer."
        return jsonify({"message": response_str}), 400

    matching_obj = cls.query.get(obj_id)
    
    if matching_obj is None:
        response_str = f"{cls.__name__} with id {obj_id} was not found in the database."
        abort(make_response({"message": response_str}, 404))
    
    return matching_obj