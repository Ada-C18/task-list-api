from flask import abort, make_response, request

def get_model_from_id(cls,model_id):
    try:
        model_id = int(model_id)
    except ValueError:  
        return abort(make_response({"msg":f"Invalid id for model of type {cls.__name__}: {model_id}"}, 400 ))

    chosen_object = cls.query.get(model_id)
    
    if chosen_object is None:
        if cls.__name__ == "Goal":
            return abort(make_response({"msg": f" Could not find goal item with id : {model_id}"} , 404 ))
        if cls.__name__ == "Task":
            return abort(make_response({"msg": f" Could not find task item with id : {model_id}"} , 404 ))  
            
    return chosen_object 