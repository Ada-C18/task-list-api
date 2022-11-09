from flask import make_response, abort

# Helper Functions
def validate_id(class_obj, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details":f"Invalid {class_obj.__name__} id"},400))
    obj = class_obj.query.get(id)
    if not obj:
        abort(make_response({"details":f"{class_obj.__name__} not found"},404))
    else:
        return obj

def mark_truthy_falsy(mark):
    if mark == "mark_complete":
        return True
    elif mark == "mark_incomplete":
        return False

