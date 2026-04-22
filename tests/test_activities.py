"""Unit tests for activity data operations"""
import pytest


class TestActivityStructure:
    """Test activity data structure and operations"""

    def test_activity_has_required_fields(self, sample_activities):
        # Arrange: Get a test activity
        activity = sample_activities["Chess Club"]

        # Act & Assert: Verify all required fields exist
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_activity_max_participants_is_positive(self, sample_activities):
        # Arrange: Check all activities

        # Act & Assert: Verify max_participants is positive
        for activity in sample_activities.values():
            assert activity["max_participants"] > 0

    def test_activity_participants_is_list(self, sample_activities):
        # Arrange: Check all activities

        # Act & Assert: Verify participants is a list
        for activity in sample_activities.values():
            assert isinstance(activity["participants"], list)


class TestParticipantOperations:
    """Test participant addition and removal"""

    def test_add_participant_to_activity(self, sample_activities):
        # Arrange: Get activity and new email
        activity = sample_activities["Gym Class"]
        email = "newstudent@mergington.edu"
        initial_count = len(activity["participants"])

        # Act: Add participant
        activity["participants"].append(email)

        # Assert: Verify participant was added
        assert len(activity["participants"]) == initial_count + 1
        assert email in activity["participants"]

    def test_remove_participant_from_activity(self, sample_activities):
        # Arrange: Get activity with participant
        activity = sample_activities["Chess Club"]
        email = "michael@mergington.edu"
        initial_count = len(activity["participants"])

        # Act: Remove participant
        activity["participants"].remove(email)

        # Assert: Verify participant was removed
        assert len(activity["participants"]) == initial_count - 1
        assert email not in activity["participants"]

    def test_check_participant_exists(self, sample_activities):
        # Arrange: Get activity with participant
        activity = sample_activities["Chess Club"]

        # Act & Assert: Check if participant exists
        assert "michael@mergington.edu" in activity["participants"]
        assert "nonexistent@mergington.edu" not in activity["participants"]


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_activity_with_no_participants(self, sample_activities):
        # Arrange: Get activity with empty participants
        activity = sample_activities["Gym Class"]

        # Act & Assert: Verify empty list
        assert len(activity["participants"]) == 0
        assert activity["participants"] == []

    def test_duplicate_participant_in_list_check(self, sample_activities):
        # Arrange: Activity with participants
        activity = sample_activities["Chess Club"]
        email = "michael@mergington.edu"

        # Act: Check if email is in list
        is_registered = email in activity["participants"]

        # Assert: Verify email is found once
        assert is_registered
        assert activity["participants"].count(email) == 1

    def test_activity_spots_remaining(self, sample_activities):
        # Arrange: Get activity details
        activity = sample_activities["Chess Club"]
        max_participants = activity["max_participants"]
        current_participants = len(activity["participants"])

        # Act: Calculate remaining spots
        spots_remaining = max_participants - current_participants

        # Assert: Verify calculation
        assert spots_remaining >= 0
        assert spots_remaining == max_participants - current_participants
