from flask import request, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal

from . import tasks
from . import goals


def bp_model(bp_name):
    model = {"tasks": Task, "goals": Goal}.get(bp_name, None)
    return model, bp_name[:-1]


@tasks.route("", methods=["GET"])
@goals.route("", methods=["GET"])
def get_all_items():
    model, _ = bp_model(request.blueprint)

    by = request.args.get("by")
    by = getattr(model, by) if by in ("title", "task_id", "goal_id") else model.title
    sort = request.args.get("sort")
    order_by = getattr(by, sort)() if sort in ("asc", "desc") else None

    title = request.args.get("title")
    filter = model.title.like(f"%{title}%") if title else None

    query = model.query
    query = query.filter(filter) if title else query
    query = query.order_by(order_by) if sort else query

    return jsonify([t.to_dict() for t in query.all()])


@tasks.route("/<item_id>", methods=["GET"])
@goals.route("/<item_id>", methods=["GET"])
def get_item(item_id):
    model, model_name = bp_model(request.blueprint)
    item = model.query.get_or_404(item_id)
    return {model_name: item.to_dict()}


@tasks.route("/<item_id>", methods=["PUT"])
@goals.route("/<item_id>", methods=["PUT"])
def put_item(item_id):
    model, model_name = bp_model(request.blueprint)
    form_data = request.get_json()
    item = model.query.get_or_404(item_id)
    item.update(**form_data)
    db.session.commit()
    return {model_name: model.to_dict()}


@tasks.route("/<item_id>", methods=["DELETE"])
@goals.route("/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    model, model_name = bp_model(request.blueprint)
    item = model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {
        "details": f'{model.__name__} {item_id} "{item.title}" successfully deleted'
    }
