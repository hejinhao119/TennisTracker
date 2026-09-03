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
            try:
                movement = evidence.item("metric.pose.right_wrist_displacement")
            except KeyError:
                return AgentReport(self.name, "Biomechanical analysis unavailable.", (), ("Insufficient evidence for contact-point or movement analysis.",))
            if movement.sample_count < 8:
                return AgentReport(self.name, "Movement analysis is inconclusive.", (), ("Insufficient evidence: fewer than 8 consecutive wrist measurements.",))
            finding = AgentFinding(
                finding_id="biomechanics.wrist_movement",
                category="movement_pattern",
                severity="low",
                claim=f"Average right-wrist displacement between sampled frames was {movement.value:.3f} normalized frame units.",
                confidence=movement.measurement_confidence,
                evidence_refs=("metric.pose.right_wrist_displacement",),
            )
            return AgentReport(self.name, "Upper-limb movement was measured from linked pose keypoints; this is not a stroke classification.", (finding,), ("A wider camera angle and faster sampling are needed for stroke timing.",))
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