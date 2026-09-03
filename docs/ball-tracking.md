# Ball tracking status

The current ball adapter is intentionally a baseline. It searches for small, circular yellow/green candidates in HSV space and records normalized image coordinates with a shape-based confidence. The evidence layer aggregates candidate coverage and frame-to-frame image displacement.

This is useful for pipeline wiring and failure visibility, but it is not sufficient for customer-facing ball speed, bounce, or in/out calls. Those require a trained tiny-object detector such as a TrackNet-family model, temporal filtering, court calibration, and a labeled tennis validation set. The [ArtLabss tennis-tracking project](https://github.com/ArtLabss/tennis-tracking) is a useful reference for separating ball, player, court, and bounce subsystems.

The UI labels this signal as a candidate trajectory and does not use it to generate technical coaching claims yet.