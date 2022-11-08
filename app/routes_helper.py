from flask import  jsonify, abort, make_response

def get_one_valid_id(cls, task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"invalid task id {task_id}"
        abort(make_response(jsonify({"message":response_str}), 400))
    
    matching_id = cls.query.get(task_id)

    if not matching_id:
        # response_str = f"{cls.__name__} with id `{goal_id}` was not found in the database."
        response_str = f"No id {task_id} task"
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_id