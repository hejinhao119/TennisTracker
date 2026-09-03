from evidence.schemas import EvidenceReport

from .base import AnalysisAgent
from .schemas import AgentFinding, AgentReport


class BiomechanicsAgent(AnalysisAgent):
    name = "BiomechanicsAgent"

    def analyze(self, evidence: EvidenceReport) -> AgentReport:
        try:
            pose_coverage = evidence.item("metric.pose.detection_rate")
        except KeyError:
            pose_coverage = None
        if pose_coverage is not None and pose_coverage.value < 0.6:
            finding = AgentFinding(
                finding_id="biomechanics.low_visual_coverage",
                category="capture_quality",
                severity="high",
                claim=f"Only {pose_coverage.value:.0%} of sampled frames contained a usable pose detection.",
                confidence=pose_coverage.measurement_confidence,
                evidence_refs=("metric.pose.detection_rate",),
            )
            return AgentReport(
                self.name,
                "Technical coaching is blocked by low visual coverage.",
                (finding,),
                ("Use a wider, steadier camera view with the player fully visible before trusting movement advice.",),
            )
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
            active_ratio = evidence.item("metric.pose.wrist_movement.active_ratio").value
            variability = evidence.item("metric.pose.wrist_movement.variability").value
            if active_ratio < 0.2:
                movement_claim = "Most sampled intervals showed limited right-wrist movement."
                finding_id = "biomechanics.low_movement_activity"
            elif variability >= 0.03:
                movement_claim = "Right-wrist movement varied sharply between sampled intervals, with distinct high-motion bursts."
                finding_id = "biomechanics.inconsistent_movement"
            else:
                movement_claim = "Right-wrist movement was relatively steady across sampled intervals."
                finding_id = "biomechanics.steady_movement"
            finding = AgentFinding(
                finding_id=finding_id,
                category="movement_pattern",
                severity="low",
                claim=f"{movement_claim} Average displacement was {movement.value:.3f} normalized frame units.",
                confidence=movement.measurement_confidence,
                evidence_refs=("metric.pose.right_wrist_displacement", "metric.pose.wrist_movement.variability", "metric.pose.wrist_movement.active_ratio"),
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