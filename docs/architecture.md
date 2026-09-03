# Architecture

The system separates uncertain video intelligence from reasoning. Vision adapters emit typed observations. The evidence builder validates those observations, normalizes values, aggregates metrics, and attaches provenance and frame references. Agents receive `EvidenceReport`, never arbitrary raw CV dictionaries.

The orchestration is deterministic: three specialists run, the coach synthesizes their structured reports, and the critic validates grounding. Retries are bounded by `max_retries`; ordinary calculations and routing stay in Python. The LLM provider protocol is isolated under `llm/`, with a mock implementation for local development.

```mermaid
flowchart TD
    Video --> Vision[Vision adapters]
    Vision --> Observations[StrokeObservation]
    Observations --> Evidence[EvidenceReport]
    Evidence --> Match[MatchAnalysisAgent]
    Evidence --> Bio[BiomechanicsAgent]
    Evidence --> Tactical[TacticalAnalysisAgent]
    Match --> Coach[CoachAgent]
    Bio --> Coach
    Tactical --> Coach
    Coach --> Critic[CoachCriticAgent]
    Critic --> Report[Structured coaching report]
```

Persistence and longitudinal comparison are intentionally pending until the evidence contract is connected to real session extraction.