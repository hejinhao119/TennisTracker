from evidence.schemas import EvidenceReport

from .schemas import AgentReport, CoachRecommendation, CoachReport


class CoachAgent:
    name = "CoachAgent"

    def synthesize(self, evidence: EvidenceReport, reports: tuple[AgentReport, ...]) -> CoachReport:
        biomechanics = next(report for report in reports if report.agent_name == "BiomechanicsAgent")
        recommendations = []
        for finding in biomechanics.findings:
            if finding.finding_id == "biomechanics.low_visual_coverage":
                drill = "Re-record from a wider, steadier camera position"
                rationale = "The camera supplied usable pose evidence in too few frames to support technical advice. Improve capture quality before changing technique."
            elif finding.finding_id == "biomechanics.inconsistent_movement":
                drill = "Split-step to shadow-swing rhythm drill"
                rationale = "The movement profile contains high-motion bursts and uneven intervals; practice linking preparation, swing, and recovery into one repeatable rhythm."
            elif finding.finding_id == "biomechanics.low_movement_activity":
                drill = "Progressive shadow swings with full range"
                rationale = "The sampled profile shows limited wrist movement; use slow, full-range repetitions before adding speed."
            else:
                drill = "Controlled shadow swings with a deliberate split-step"
                rationale = "The movement profile is relatively steady; reinforce the same preparation and recovery rhythm under controlled repetition."
            recommendations.append(
                CoachRecommendation(
                    priority=1,
                    issue=finding.claim,
                    rationale=("The finding is supported by normalized contact estimates and linked frames." if finding.category == "contact_point" else rationale),
                    drill=("Early unit-turn shadow swings" if finding.category == "contact_point" else drill),
                    frequency="3 sessions/week",
                    volume="3 x 10 repetitions",
                    confidence=finding.confidence,
                    evidence_refs=finding.evidence_refs,
                )
            )
        limitations = tuple(dict.fromkeys(evidence.missing_data + tuple(
            limitation for report in reports for limitation in report.limitations
        )))
        diagnosis = "Prioritize the highest-confidence measurable issue." if recommendations else "No evidence-backed priority can be recommended yet."
        return CoachReport(diagnosis, tuple(recommendations), limitations=limitations)