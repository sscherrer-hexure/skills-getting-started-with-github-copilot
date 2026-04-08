def test_unregister_removes_existing_participant(client):
    email = "daniel@mergington.edu"

    response = client.delete(f"/activities/Chess%20Club/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown%20Club/unregister?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess%20Club/unregister?email=ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in activity"}


def test_unregister_then_signup_same_email_works(client):
    email = "lucas@mergington.edu"

    remove_response = client.delete(f"/activities/Drama%20Club/unregister?email={email}")
    add_response = client.post(f"/activities/Drama%20Club/signup?email={email}")

    assert remove_response.status_code == 200
    assert add_response.status_code == 200

    payload = client.get("/activities").json()
    participants = payload["Drama Club"]["participants"]
    assert participants.count(email) == 1
