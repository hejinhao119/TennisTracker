from agents.orchestration import run_coaching_analysis
from agents.critic import CoachCriticAgent
from agents.schemas import CoachRecommendation, CoachReport
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


def test_critic_rejects_unknown_evidence_reference() -> None:
    evidence = build_evidence("session-3", [])
    report = CoachReport(
        "diagnosis",
        (CoachRecommendation(1, "issue", "reason", "drill", "weekly", "3 reps", 0.8, ("missing",)),),
    )

    critic = CoachCriticAgent().review(report, evidence)

    assert not critic.approved
    assert any("missing evidence" in issue for issue in critic.issues)


def test_low_pose_coverage_prioritizes_capture_quality() -> None:
    from evidence.schemas import PoseObservation

    evidence = build_evidence(
        "session-low-coverage",
        [],
        [PoseObservation(0, 1, 0.8), PoseObservation(1, 0, 0.0), PoseObservation(2, 0, 0.0)],
    )
    run = run_coaching_analysis(evidence)

    assert run.biomechanics.findings[0].finding_id == "biomechanics.low_visual_coverage"
    assert run.coach.recommendations[0].drill == "Re-record from a wider, steadier camera position"