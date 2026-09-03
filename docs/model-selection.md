# Model selection and performance plan

## What the current results say

The current generic YOLOv8 pose baseline is useful for wiring and visualization, but it does not identify tennis strokes, ball contact, court coordinates, or tactical outcomes. Independent testing showed that 4K footage can still have poor pose coverage, while a 1080p training clip can be much more usable. Resolution alone is not a quality metric.

## Candidates

- [Ultralytics](https://github.com/ultralytics/ultralytics): easiest migration and supports tracking, but the current project uses a small generic pose checkpoint. Review AGPL/commercial licensing before shipping a customer product.
- [RTMPose/MMPose](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose): the strongest practical next candidate for top-down pose, with documented model sizes, ONNXRuntime/MMDeploy deployment, and tracking examples. Benchmark RTMPose-m and RTMPose-l rather than assuming the largest model wins.
- [ViTPose](https://github.com/ViTAE-Transformer/ViTPose): accuracy-oriented generic pose models with stronger COCO results, but heavier installation and inference costs. Keep it as an offline accuracy benchmark until latency is measured.
- [ArtLabss tennis-tracking](https://github.com/ArtLabss/tennis-tracking): reference architecture for court lines, players, TrackNet-style ball tracking, and bounce classification. It is an older project with documented speed and camera limitations, so reuse ideas rather than treating it as production-ready.

## Recommended architecture

Use a two-stage, tennis-specific pipeline:

1. Camera quality gate: resolution, blur, exposure, player visibility, pose coverage, keypoint confidence.
2. Player detector plus temporal tracker: one stable player identity, not an independent per-frame argmax.
3. Pose estimator: RTMPose benchmarked against the existing YOLO baseline.
4. Tennis event models: ball detector/tracker, court homography, stroke-phase classifier, and bounce/outcome classifier.
5. Deterministic biomechanics: calculate angles, velocities, timing, and recovery from validated trajectories.
6. Agents: explain only those measurements and link every claim to frames.

## Acceptance gates

Do not enable a customer-facing technical recommendation unless the held-out clip meets the configured pose coverage and keypoint-confidence gates. Model selection requires a labeled validation set with per-event precision, recall, and temporal localization error. Report measured results; do not use COCO scores as a substitute for tennis accuracy.

## License and operations

Ultralytics currently offers AGPL-3.0 and an enterprise option. MMPose is Apache 2.0. License choice matters for a commercial product. Keep model adapters behind a stable interface so a licensed or hosted model can be substituted without changing the evidence and coaching layers.