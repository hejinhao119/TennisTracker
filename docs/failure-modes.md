# Failure modes and mitigations

- Incorrect or missing CV detections: preserve per-observation confidence and report missing evidence; do not treat predictions as ground truth.
- Small samples: attach sample counts and low reliability; biomechanics requires a minimum sample before making a finding.
- Unsupported biomechanics or tactics: agents list unavailable measurements instead of inferring them.
- Malformed model output: provider responses are isolated behind a structured contract; production adapters should validate and retry parsing before orchestration accepts them.
- Agent disagreement: the coach report has explicit agreement and contradiction fields; future revisions should populate them from specialist findings.
- LLM timeout or provider outage: the mock provider keeps local tests runnable; production UI should surface provider failure as a failed run.
- Runaway loops: orchestration stops after the configured retry budget.