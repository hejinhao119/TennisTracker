from evidence.schemas import EvidenceReport

from .base import AnalysisAgent
from .schemas import AgentFinding, AgentReport


class MatchAnalysisAgent(AnalysisAgent):
    name = "MatchAnalysisAgent"

    def analyze(self, evidence: EvidenceReport) -> AgentReport:
        if not evidence.strokes:
            return AgentReport(self.name, "Match-level analysis unavailable.", limitations=evidence.missing_data)
        findings = []
        for item in evidence.items:
            if item.metric == "stroke_share":
                findings.append(
                    AgentFinding(
                        finding_id=f"match.{item.evidence_id}",
                        category="match_composition",
                        severity="low",
                        claim=f"{item.value:.0%} of detected strokes were {item.evidence_id.rsplit('.', 1)[-1]}.",
                        confidence=item.measurement_confidence,
                        evidence_refs=(item.evidence_id,),
                    )
                )
        return AgentReport(self.name, "Objective stroke composition was calculated from valid detections.", tuple(findings))