def test_signup_adds_new_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_email_returns_400(client):
    duplicate_email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={duplicate_email}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_uppercase_email_is_accepted_and_persisted(client):
    email = "CASEY.STUDENT@MERGINGTON.EDU"

    response = client.post(f"/activities/Drama%20Club/signup?email={email}")

    assert response.status_code == 200
    payload = client.get("/activities").json()
    assert email in payload["Drama Club"]["participants"]
