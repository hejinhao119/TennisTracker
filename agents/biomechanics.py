from evidence.schemas import EvidenceReport

from .base import AnalysisAgent
from .schemas import AgentFinding, AgentReport


class BiomechanicsAgent(AnalysisAgent):
    name = "BiomechanicsAgent"

    def analyze(self, evidence: EvidenceReport) -> AgentReport:
        item_id = "metric.contact_point.behind_target_ratio"
        try:
            item = evidence.item(item_id)
        except KeyError:
            return AgentReport(self.name, "Biomechanical analysis unavailable.", ( ), ("Insufficient evidence for contact-point analysis.",))
        if item.sample_count < 8:
            return AgentReport(self.name, "Biomechanical analysis is inconclusive.", (), ("Insufficient evidence: fewer than 8 contact samples.",))
        finding = AgentFinding(
            finding_id="biomechanics.late_contact",
            category="contact_point",
            severity="medium" if item.value >= 0.5 else "low",
            claim=f"{item.value:.0%} of valid contact estimates were behind the target zone.",
            confidence=item.measurement_confidence,
            evidence_refs=(item_id,),
        )
        return AgentReport(self.name, "Contact-point geometry was assessed from normalized frame-linked estimates.", (finding,))