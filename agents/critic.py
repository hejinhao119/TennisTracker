from .schemas import CoachReport, CriticReport


class CoachCriticAgent:
    name = "CoachCriticAgent"

    def review(self, report: CoachReport) -> CriticReport:
        issues = []
        for recommendation in report.recommendations:
            if not recommendation.evidence_refs:
                issues.append("Recommendation has no evidence references.")
            if recommendation.confidence < 0.5:
                issues.append(f"Recommendation '{recommendation.issue}' has low confidence.")
        return CriticReport(not issues, tuple(issues))