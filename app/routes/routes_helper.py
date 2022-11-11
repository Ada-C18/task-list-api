from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    query_result = cls.query.get(id)

    if not query_result:
        abort(make_response({"details": f"{cls.__name__} {id} Not Found"}, 404))

    return query_result

def validate_input(cls, request_body):
    if cls == Task:
        if "title" not in request_body or "description" not in request_body:
            abort(make_response({"details":"Invalid data"},400))
    elif cls == Goal:
        if "title" not in request_body or "description" in request_body:
            abort(make_response({"details":"Invalid data"},400))