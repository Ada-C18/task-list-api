from flask import abort,make_response,request, jsonify
from app.models.task import Task
from app import db

def post_one_model(cls):
    response_body = request.get_json()
    
    try:
        new_model = cls.objectfy(response_body)
    except KeyError:
        return make_response({
        "details": "Invalid data"
    },400)
    db.session.add(new_model)
    db.session.commit()

    class_str = class_str_determinator(cls)

    return make_response(jsonify({class_str:new_model.dictionfy()}),201)

def get_all_models(cls):
    return_list=[]
    match_command = [(key,value) for key,value in request.args.items()]
    specific_title = request.args.get('title')
    
    #currently can query: specific name, order by id or title, all
    if specific_title:
        models = cls.query.filter_by(title=specific_title)
    elif match_command:
        try:
            models = sort_query_helper(cls,match_command)
        except ValueError:
            return make_response(jsonify({"warning":"Invalid query sorting parameters"}),400)
    else:
        models = cls.query.all()
    
    for model in models:
        return_list.append(model.dictionfy())
    
    return make_response(jsonify(return_list),200)

def get_one_model(cls,id):
    model = validate_model(cls,id)
    class_str = class_str_determinator(cls)
    return make_response(jsonify({class_str:model.dictionfy()}),200)

def class_str_determinator(cls):
    return "task" if cls==Task else "goal"

def delete_one_model(cls,id):
    model = validate_model(cls,id)

    db.session.delete(model)
    db.session.commit()

    class_str = class_str_determinator(cls).capitalize()

    return make_response(jsonify({'details':f'{class_str} {id} \"{model.title}\" successfully deleted'}),200)


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def sort_query_helper(cls,request_dict):
    obj,order = request_dict[0]
    match obj:
        case "sort":
            order_object = cls.title
        case "id_sort":
            order_object = cls.task_id if cls==Task else cls.goal_id #I know there's gonna be a big refactor if I need more than 2 classes to take this but it's what I've got
        case other:
            raise ValueError
    match order:    
        case "desc":
            order_object = order_object.desc()
        case 'asc':
            order_object = order_object.asc()
        case other:
            raise ValueError
    return cls.query.order_by(order_object).all()