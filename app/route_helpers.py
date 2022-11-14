
from flask import make_response, abort



def validate_model_id(cls, id):
    cls_name = cls.__name__

    try:
        id = int(id)
    except:
        abort(make_response({"message" : f"{cls_name.lower()} id: {id} is invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message" : f"{cls_name.lower()} {id} not found"}, 404))

    return model