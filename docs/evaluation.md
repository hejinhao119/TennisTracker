# Evaluation

The intended benchmark contains cases for late contact, poor recovery, high error rate with insufficient evidence, contradictory findings, very small samples, and excellent consistency. Each case should provide fixed evidence fixtures and expected grounding behavior.

Metrics will include schema validity, evidence-reference coverage, finding correctness, recommendation relevance, unsupported-claim rate, critic catch rate, latency, and token cost. A single-agent baseline should receive the same evidence context and be evaluated with the same rubric. No benchmark percentages are reported yet because the dataset and runner are not implemented.

The main limitation is that evaluation quality depends on the accuracy and coverage of the upstream CV measurements. Agent scores cannot repair missing or unreliable evidence.