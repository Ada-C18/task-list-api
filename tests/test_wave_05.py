import pytest
from app.models.goal import Goal


# @pytest.mark.skip(reason="No way to test this feature yet") - test 1
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet") - test 2
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet") - test 3
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student") - test 4
def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 404
    assert response_body == {"Message": f"Goal 1 not found"}

    # raise Exception("Complete test")


# @pytest.mark.skip(reason="No way to test this feature yet") - test 5
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student") #NOT WORKING - test 6
def test_update_goal(client, one_goal):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Updated Goal Title",
        }
    }
    goal = Goal.query.get(1)
    assert goal.title == "Updated Goal Title"

    # raise Exception("Complete test")



# @pytest.mark.skip(reason="test to be completed by student") # NOT WORKING - test 7
def test_update_goal_not_found(client):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"Message": f"Goal 1 not found"}


# @pytest.mark.skip(reason="No way to test this feature yet")  # NOT WORKING test 8
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 Build a habit of going outside daily successfully deleted'
    }

    # Check that the goal was deleted
    response = client.get("/goals/1")
    response_body = response.get_json()
    assert response.status_code == 404
    assert response_body == {'Message': f"Goal 1 not found"} 

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


# @pytest.mark.skip(reason="test to be completed by student") - test 9
def test_delete_goal_not_found(client):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"Message": f"Goal 1 not found"}
    assert Goal.query.get(1) == None

    # raise Exception("Complete test")



# @pytest.mark.skip(reason="No way to test this feature yet") - test 10
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
