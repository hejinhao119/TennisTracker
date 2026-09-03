from evidence.schemas import EvidenceReport

from .schemas import AgentReport, CoachRecommendation, CoachReport


class CoachAgent:
    name = "CoachAgent"

    def synthesize(self, evidence: EvidenceReport, reports: tuple[AgentReport, ...]) -> CoachReport:
        biomechanics = next(report for report in reports if report.agent_name == "BiomechanicsAgent")
        recommendations = []
        for finding in biomechanics.findings:
            recommendations.append(
                CoachRecommendation(
                    priority=1,
                    issue=finding.claim,
                    rationale="The finding is supported by normalized contact estimates and linked frames.",
                    drill="Early unit-turn shadow swings",
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