from flask import abort, make_response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"Invalid {cls.__name__}: `{model_id}`. ID must be an integer"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} with id `{model_id}` was not found in the database."}, 404))
    return model