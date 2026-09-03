from collections import Counter
from statistics import fmean

from .schemas import EvidenceItem, EvidenceReport, PoseObservation, StrokeObservation


def _reliability(sample_count: int, confidence: float) -> str:
    if sample_count >= 20 and confidence >= 0.75:
        return "high"
    if sample_count >= 8 and confidence >= 0.55:
        return "medium"
    return "low"


def build_evidence(
    session_id: str,
    strokes: list[StrokeObservation],
    pose_observations: list[PoseObservation] | None = None,
) -> EvidenceReport:
    """Validate vision observations and expose only aggregate, traceable metrics."""
    items: list[EvidenceItem] = []
    pose_observations = pose_observations or []
    by_type = Counter(stroke.stroke_type for stroke in strokes)
    total = len(strokes)

    for stroke_type, count in sorted(by_type.items()):
        confidence = fmean(
            stroke.confidence for stroke in strokes if stroke.stroke_type == stroke_type
        )
        items.append(
            EvidenceItem(
                evidence_id=f"metric.stroke_share.{stroke_type}",
                metric="stroke_share",
                value=count / total if total else 0.0,
                unit="ratio",
                source="vision.stroke_observations",
                measurement_confidence=confidence,
                sample_count=count,
                reliability=_reliability(count, confidence),
                frame_refs=tuple(
                    (stroke.frame_start, stroke.frame_end)
                    for stroke in strokes
                    if stroke.stroke_type == stroke_type
                ),
            )
        )

    contact_samples = [stroke for stroke in strokes if stroke.contact_point_x is not None]
    if contact_samples:
        behind_target = [stroke for stroke in contact_samples if stroke.contact_point_x < 0.5]
        confidence = fmean(stroke.confidence for stroke in contact_samples)
        items.append(
            EvidenceItem(
                evidence_id="metric.contact_point.behind_target_ratio",
                metric="contact_point.behind_target_ratio",
                value=len(behind_target) / len(contact_samples),
                unit="ratio",
                source="vision.contact_point_estimator",
                measurement_confidence=confidence,
                sample_count=len(contact_samples),
                reliability=_reliability(len(contact_samples), confidence),
                frame_refs=tuple(
                    (stroke.frame_start, stroke.frame_end) for stroke in behind_target
                ),
            )
        )

    if pose_observations:
        detected = [observation for observation in pose_observations if observation.person_count > 0]
        confidence = fmean(observation.confidence for observation in pose_observations)
        items.append(
            EvidenceItem(
                evidence_id="metric.pose.detection_rate",
                metric="pose.detection_rate",
                value=len(detected) / len(pose_observations),
                unit="ratio",
                source="vision.pose_estimator",
                measurement_confidence=confidence,
                sample_count=len(pose_observations),
                reliability=_reliability(len(pose_observations), confidence),
                frame_refs=tuple((observation.frame_index, observation.frame_index) for observation in detected),
            )
        )

    missing_data = []
    if not strokes:
        missing_data.append("No valid strokes were detected")
    if not contact_samples:
        missing_data.append("Contact-point estimates are unavailable")

    return EvidenceReport(
        session_id=session_id,
        strokes=tuple(strokes),
        items=tuple(items),
        pose_observations=tuple(pose_observations),
        missing_data=tuple(missing_data),
    )