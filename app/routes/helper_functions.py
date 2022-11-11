from flask import abort, make_response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid Data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid Data"}, 404))

    return model