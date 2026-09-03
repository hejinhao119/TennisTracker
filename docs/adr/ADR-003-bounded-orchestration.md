# ADR-003: Bound critic retries

Critic revision is capped by a retry budget. A bounded loop prevents cost and latency runaway and makes failure behavior testable. A rejected final report remains explicitly rejected rather than looping indefinitely.