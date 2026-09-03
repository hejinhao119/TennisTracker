from collections import Counter
from statistics import fmean, pstdev

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
        keypoint_confidence = fmean(observation.keypoint_confidence for observation in pose_observations)
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
        items.append(
            EvidenceItem(
                evidence_id="metric.pose.keypoint_confidence",
                metric="pose.keypoint_confidence",
                value=keypoint_confidence,
                unit="ratio",
                source="vision.pose_estimator.keypoints",
                measurement_confidence=confidence,
                sample_count=len(pose_observations),
                reliability=_reliability(len(pose_observations), keypoint_confidence),
                frame_refs=tuple((observation.frame_index, observation.frame_index) for observation in detected),
            )
        )

        wrist_pairs = []
        for previous, current in zip(pose_observations, pose_observations[1:]):
            if len(previous.keypoints) <= 10 or len(current.keypoints) <= 10:
                continue
            previous_wrist = previous.keypoints[10]
            current_wrist = current.keypoints[10]
            displacement = ((current_wrist[0] - previous_wrist[0]) ** 2 + (current_wrist[1] - previous_wrist[1]) ** 2) ** 0.5
            wrist_pairs.append((displacement, previous.frame_index, current.frame_index))
        if wrist_pairs:
            confidence = fmean(observation.confidence for observation in pose_observations)
            displacements = [pair[0] for pair in wrist_pairs]
            active_pairs = [pair for pair in displacements if pair >= 0.05]
            items.append(
                EvidenceItem(
                    evidence_id="metric.pose.right_wrist_displacement",
                    metric="pose.right_wrist_displacement",
                    value=fmean(pair[0] for pair in wrist_pairs),
                    unit="normalized_frame_distance",
                    source="vision.pose_estimator.keypoints",
                    measurement_confidence=confidence,
                    sample_count=len(wrist_pairs),
                    reliability=_reliability(len(wrist_pairs), confidence),
                    frame_refs=tuple((pair[1], pair[2]) for pair in wrist_pairs),
                )
            )
            profile_metrics = (
                ("mean", fmean(displacements)),
                ("variability", pstdev(displacements) if len(displacements) > 1 else 0.0),
                ("active_ratio", len(active_pairs) / len(displacements)),
                ("peak", max(displacements)),
            )
            for metric_suffix, value in profile_metrics:
                items.append(
                    EvidenceItem(
                        evidence_id=f"metric.pose.wrist_movement.{metric_suffix}",
                        metric=f"pose.wrist_movement.{metric_suffix}",
                        value=value,
                        unit="normalized_frame_distance" if metric_suffix != "active_ratio" else "ratio",
                        source="vision.pose_estimator.keypoints",
                        measurement_confidence=confidence,
                        sample_count=len(displacements),
                        reliability=_reliability(len(displacements), confidence),
                        frame_refs=tuple((pair[1], pair[2]) for pair in wrist_pairs),
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