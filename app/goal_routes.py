from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify, make_response, abort
from sqlalchemy import desc
from datetime import datetime
import requests
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# goals
@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()
    goals_list = []

    for goal in goals:
        goals_list.append(
            
            {"id": goal.goal_id, "title": goal.title}
        )
        
        # return jsonify(goals_list),200
    return jsonify(goals_list)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    validate_goal = validate_model(Goal, goal_id)

    goal = Goal.query.get(goal_id)
    if goal:
        return {
            "goal": goal.to_dict_goal()
        }, 200
    else:
        # return make_response(jsonify(None))
        return []

# @authors_bp.route("", methods=["POST"])
# def create_author():
#     request_body = request.get_json()
#     new_author = Author(name=request_body["name"],)

#     db.session.add(new_author)
#     db.session.commit()

#     return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

# @authors_bp.route("", methods=["GET"])
# def read_all_authors():
    
#     authors = Author.query.all()

#     authors_response = []
#     for author in authors:
#         authors_response.append(
#             {
#                 "name": author.name
#             }
#         )
#     return jsonify(authors_response)

# @authors_bp.route("/<author_id>/books", methods=["POST"])
# def create_book(author_id):

#     author = validate_model(Author, author_id)

#     request_body = request.get_json()
#     new_book = Book(
#         title=request_body["title"],
#         description=request_body["description"],
#         author=author
#     )
#     db.session.add(new_book)
#     db.session.commit()
#     return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

# @authors_bp.route("/<author_id>/books", methods=["GET"])
# def read_books(author_id):

#     author = validate_model(Author, author_id)

#     books_response = []
#     for book in author.books:
#         books_response.append(
#             {
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#             }
#         )
#     return jsonify(books_response)

