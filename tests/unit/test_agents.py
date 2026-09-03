from agents.orchestration import run_coaching_analysis
from evidence.builder import build_evidence
from evidence.schemas import StrokeObservation


def test_orchestration_is_bounded_and_grounded() -> None:
    strokes = [
        StrokeObservation(f"s{i}", float(i), "forehand", 0.8, i * 10, i * 10 + 2, contact_point_x=0.4)
        for i in range(8)
    ]
    run = run_coaching_analysis(build_evidence("session-1", strokes))

    assert run.attempts <= 3
    assert run.critic.approved
    assert run.coach.recommendations[0].evidence_refs == (
        "metric.contact_point.behind_target_ratio",
    )


def test_biomechanics_does_not_overclaim_small_sample() -> None:
    strokes = [StrokeObservation("s1", 1.0, "forehand", 0.9, 1, 2, contact_point_x=0.4)]
    run = run_coaching_analysis(build_evidence("session-2", strokes))

    assert not run.coach.recommendations
    assert any("fewer than 8" in item for item in run.biomechanics.limitations)