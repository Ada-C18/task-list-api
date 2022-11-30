from flask import abort, make_response, jsonify

def validate_model(cls, model_id):
    try:
        model_id = int(model_id) 
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)
    
    if not model:
        response = f"{cls.__name__} #{model_id} was not found"
        abort(make_response({"message": response}, 404))
        
    return model