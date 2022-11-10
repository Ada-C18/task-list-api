import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
    ]


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]

def test_get_tasks_id_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?id_sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False}
    ]


def test_get_tasks_by_name(client, three_tasks):
    # Act
    response = client.get("/tasks?title=Water the garden 🌷")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
    ]

def test_get_tasks_id_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?id_sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
        
    ]

def test_get_tasks_bad_query(client, three_tasks):
    # Act
    response = client.get("/tasks?im=teapot")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert 'warning' in response_body
    assert response_body['warning'] == "Invalid query sorting parameters"

#Goal query tests#
def test_get_goals_bad_query(client, two_goals):
    # Act
    response = client.get("/goals?im=teapot")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert 'warning' in response_body
    assert response_body['warning'] == "Invalid query sorting parameters"

def test_get_goals_bad_query(client, two_goals):
    # Act
    response = client.get("/goals?sort=teapot")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert 'warning' in response_body
    assert response_body['warning'] == "Invalid query sorting parameters"

def test_get_goals_query_asc(client, two_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 2,
            "title": 'Toss an apple at a doctor'}
        
    ]
def test_get_goals_query_desc(client, two_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 2,
            "title": 'Toss an apple at a doctor'},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"}
    ]
def test_get_goals_id_query_asc(client, two_goals):
    # Act
    response = client.get("/goals?id_sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 2,
            "title": 'Toss an apple at a doctor'}
        
    ]
def test_get_goals_id_query_desc(client, two_goals):
    # Act
    response = client.get("/goals?id_sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 2,
            "title": 'Toss an apple at a doctor'},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"}
    ]