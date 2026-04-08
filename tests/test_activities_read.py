from src.app import activities


REQUIRED_ACTIVITY_KEYS = {
    "description",
    "schedule",
    "max_participants",
    "participants",
}


def test_get_activities_returns_seeded_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == len(activities)
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_get_activities_contract_for_each_activity(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()

    for activity_name, details in payload.items():
        assert isinstance(activity_name, str)
        assert REQUIRED_ACTIVITY_KEYS.issubset(details.keys())
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)
