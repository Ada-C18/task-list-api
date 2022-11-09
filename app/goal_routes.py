from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes import validate_id
from app.routes import tasks_bp
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f" {goal_id} is an invalid goal_id"}, 400))

    query_result = Goal.query.get(goal_id)
    if not query_result:
        abort(make_response({"message":f" {goal_id} not found"}, 404))

    return query_result

############### Create GOAL#################
@goals_bp.route("", methods=["POST"])
def create_goals():
    
    if not 'title' in request.get_json()  :
        return {"details":"Invalid data"},400
    else:
    
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        goal_dictionary=new_goal.to_dict()
        return {"goal":goal_dictionary}, 201
    
    
############### Get ALL GOALS###################

@goals_bp.route("", methods=["GET"])
def get_all_goals():
  
    goals = Goal.query.all()
    result_list = [goal.to_dict() for goal in goals]
    return   jsonify(result_list), 200

################ GET ONE GOAL ###################
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal= validate_goal_id(goal_id)
    return jsonify({"goal":goal.to_dict()}), 200

################ UPDATE GOAL ####################
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.title=request_body["title"]
    db.session.commit()
    return jsonify({"goal":goal.to_dict()}), 200
################ DELETE GOAL ##############

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)

    db.session.commit()
    return  make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"})

########################


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_all_taskes_for_one_goal(goal_id):
    
    goal=validate_goal_id(goal_id)
   
    request_body = request.get_json()

    goal.tasks=[]
    #for i in task:
    
    for id in request_body["task_ids"]:
        task=validate_id(id)
        goal.tasks.append(task)    
       
    db.session.add_all(goal.tasks)
    db.session.commit()
    return jsonify({"id":goal.goal_id , "task_ids":request_body["task_ids"]})


###################Getting Task of One Goal############

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])

def read_tasks(goal_id):

    goal = validate_goal_id(goal_id)


    task_response = []
    for task in goal.tasks:

        task_response.append(
            {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete":task.is_complete,
            "goal_id":task.goal_id
            
            }
        )
        
    
    return {"id":goal.goal_id,"title":goal.title,"tasks":task_response}

  ####################################
  
# @tasks_bp.route("/<id>", methods=["GET"])
# def read_one_task(id):
#     task=validate_id(id)
#     if not task.goal_id:
#         return{"task":{"id":task.id,
#                        "title":task.title,
#                        "description":task.description,
#                        "is_complete":task.is_complete
#                        }
#         }
#     else:
#         return{"task":{"id":task.id,
#                        "goal_id":task.goal_id,
#                        "title":task.title,
#                        "description":task.description,
#                        "is_complete":task.is_complete
                       
            
            
#         }
#     }