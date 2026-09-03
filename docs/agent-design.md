# Agent design

| Agent | Input | Responsibility | Failure behavior |
| --- | --- | --- | --- |
| `MatchAnalysisAgent` | aggregate evidence | shot composition and match-level counts | reports unavailable when no strokes exist |
| `BiomechanicsAgent` | contact and pose evidence | measurable technical patterns | says insufficient evidence below eight contact samples |
| `TacticalAnalysisAgent` | stroke sequence evidence | describes available tactical signals | lists unmeasured direction, pressure, and court position |
| `CoachAgent` | specialist reports plus evidence | prioritizes grounded drills | emits no recommendation without supported findings |
| `CoachCriticAgent` | coach report | rejects missing references and low-confidence recommendations | returns structured issues; orchestration has a retry cap |

Reports are typed dataclasses with explicit evidence references. The UI exposes summaries and provenance, not hidden chain-of-thought.