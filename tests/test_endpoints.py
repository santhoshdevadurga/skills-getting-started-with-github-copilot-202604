"""Integration tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Test GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange: TestClient is ready with sample data

        # Act: Call GET /activities
        response = client.get("/activities")

        # Assert: Verify response
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 3
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client):
        # Arrange: TestClient is ready

        # Act: Call GET /activities
        response = client.get("/activities")

        # Assert: Verify activity structure
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_success(self, client):
        # Arrange: Prepare email and activity
        email = "newstudent@mergington.edu"
        activity_name = "Gym Class"

        # Act: Sign up for activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert: Verify success response
        assert response.status_code == 200
        assert f"Signed up {email}" in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client):
        # Arrange: Prepare email and activity
        email = "newstudent@mergington.edu"
        activity_name = "Gym Class"

        # Act: Sign up for activity and verify participant list
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")

        # Assert: Verify participant was added
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        # Arrange: Prepare non-existent activity
        email = "student@mergington.edu"
        activity_name = "NonExistent Activity"

        # Act: Try to sign up for non-existent activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert: Verify 404 error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_registration(self, client):
        # Arrange: Student already registered in Chess Club
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act: Try to sign up again for same activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert: Verify 400 error for duplicate
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Test DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_student_success(self, client):
        # Arrange: Student is registered in Chess Club
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act: Unregister student
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert: Verify success response
        assert response.status_code == 200
        assert f"Unregistered {email}" in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        # Arrange: Student is registered in Chess Club
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act: Unregister student and verify
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        response = client.get("/activities")

        # Assert: Verify participant was removed
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        # Arrange: Prepare non-existent activity
        email = "michael@mergington.edu"
        activity_name = "NonExistent Activity"

        # Act: Try to unregister from non-existent activity
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert: Verify 404 error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_registered(self, client):
        # Arrange: Student not registered in Gym Class
        email = "notregistered@mergington.edu"
        activity_name = "Gym Class"

        # Act: Try to unregister non-registered student
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert: Verify 400 error
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]


class TestRoot:
    """Test GET / endpoint"""

    def test_root_redirects_to_static(self, client):
        # Arrange: TestClient is ready

        # Act: Call GET / with follow_redirects=False to check redirect
        response = client.get("/", follow_redirects=False)

        # Assert: Verify redirect to /static/index.html
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
