# ADR-001: Introduce an evidence layer

We place validation, normalization, aggregation, confidence, provenance, and frame references between vision and agents. This prevents every agent from interpreting raw model output differently and makes recommendations auditable. The tradeoff is an additional contract to maintain, accepted because traceability and uncertainty are core product requirements.