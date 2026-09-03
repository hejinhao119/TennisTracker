from .models import MetricComparison, SessionMetric


def compare_metric(previous: SessionMetric, current: SessionMetric, min_samples: int = 8) -> MetricComparison:
    """Compare metrics only when both measurements have enough reliable samples."""
    if previous.metric != current.metric:
        raise ValueError("metrics must match")
    change = current.value - previous.value
    meaningful = (
        previous.sample_count >= min_samples
        and current.sample_count >= min_samples
        and previous.confidence >= 0.55
        and current.confidence >= 0.55
    )
    reason = "Meaningful comparison" if meaningful else "Insufficient sample size or measurement confidence"
    return MetricComparison(previous.metric, previous.value, current.value, change, meaningful, reason)