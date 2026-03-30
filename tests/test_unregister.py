
def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_when_participant_missing(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422