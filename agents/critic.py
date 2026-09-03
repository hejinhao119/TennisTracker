from evidence.schemas import EvidenceReport

from .schemas import CoachReport, CriticReport


class CoachCriticAgent:
    name = "CoachCriticAgent"

    def review(self, report: CoachReport, evidence: EvidenceReport | None = None) -> CriticReport:
        issues = []
        evidence_ids = {item.evidence_id for item in evidence.items} if evidence else None
        for recommendation in report.recommendations:
            if not recommendation.evidence_refs:
                issues.append("Recommendation has no evidence references.")
            if recommendation.confidence < 0.5:
                issues.append(f"Recommendation '{recommendation.issue}' has low confidence.")
            if evidence_ids is not None:
                missing = set(recommendation.evidence_refs) - evidence_ids
                if missing:
                    issues.append(f"Recommendation references missing evidence: {sorted(missing)}.")
        return CriticReport(not issues, tuple(issues))