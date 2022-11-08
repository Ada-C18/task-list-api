from app.models.task import Task

def test_get_non_int_id(client):
    pass
    # Act
    response = client.get("/goals/tacocat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert response_body["message"] == "Invalid Goal_id: tacocat must be an integer" 

def test_get_goals_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "A New goal title"},
        {
            "id": 2,
            "title": "Even newer goal title"},
        {
            "id": 3,
            "title": "The newest goal of all"}
    ]


def test_get_goals_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "The newest goal of all"},
        {
            "id": 2,
            "title": "Even newer goal title"},
        {
            "id": 1,
            "title": "A New goal title"}]