from app.models.goal import Goal
from app.models.task import Task
import pytest


def test_get_tasks_sorted_id_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc&by=task_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷",
        },
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧",
        },
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭",
        },
    ]


def test_get_tasks_sorted_id_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&by=task_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False,
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False,
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False,
        },
    ]


def test_get_tasks_invalid_sort(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asdf")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷",
        },
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧",
        },
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭",
        },
    ]


def test_filter_tasks_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?title=forgotten")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧",
        },
    ]


def test_sort_goals_by_title(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
        },
    ]


def test_create_task_invalid_completed_at(client):
    # Act
    response = client.post(
        "/tasks",
        json={"description": "Test Description", "completed_at": "this is not a date"},
    )
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {"details": "Invalid data"}
    assert Task.query.all() == []


def test_update_task_invalid_completed_at(client, one_task):
    # Act
    response = client.put(
        "/tasks/1",
        json={
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "completed_at": "this is not a date",
        },
    )
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["details"] == "Invalid isoformat string: 'this is not a date'"

    task = Task.query.get(1)
    assert task.title != "Updated Task Title"
    assert task.description != "Updated Test Description"
    assert task.completed_at == None


def test_get_invalid_task_id(client, one_task):
    # Act
    response = client.get("/tasks/asdf")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid Task id"}


def test_get_invalid_goal_id(client, one_goal):
    # Act
    response = client.get("/goals/asdf")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid Goal id"}
