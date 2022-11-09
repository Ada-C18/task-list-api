from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
import pytest


def test_get_tasks_for_specific_invalid_goal(client):
    # Act
    response = client.get("/goals/abc/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details":f"Invalid {Goal.__name__} id"}

    assert Goal.query.all() == []



def test_get_tasks_for_specific_goal_no_goal(client):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details":f"{Goal.__name__} not found"}


def test_create_task_with_date(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "datetime": "07/12/99"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": True
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert isinstance(new_task.completed_at, datetime)
    assert new_task.completed_at.strftime('%m/%d/%y') == '07/12/99'


def test_create_task_with_invalid_date(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "datetime": "0a/12/99"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details":f"datetime invalid, needs to be in form 'm/d/yy'"}
    