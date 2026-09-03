from evidence.schemas import EvidenceReport

from .base import AnalysisAgent
from .schemas import AgentFinding, AgentReport


class TacticalAnalysisAgent(AnalysisAgent):
    name = "TacticalAnalysisAgent"

    def analyze(self, evidence: EvidenceReport) -> AgentReport:
        if not evidence.strokes:
            return AgentReport(self.name, "Tactical analysis unavailable.", limitations=("No valid stroke sequence was available.",))
        return AgentReport(
            self.name,
            "Tactical sequence analysis is limited to detected shot composition in this pipeline.",
            limitations=("Direction, rally pressure, and court position are not currently measured.",),
        )