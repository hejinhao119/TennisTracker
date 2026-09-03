from memory.models import UserFeedback
from memory.repository import SessionRepository


def test_user_feedback_round_trip(tmp_path) -> None:
    repository = SessionRepository(tmp_path / "sessions.db")
    feedback = UserFeedback("session-1", "coach_report", "Yes")

    repository.save_feedback(feedback)

    assert repository.get_feedback("coach_report") == [feedback]