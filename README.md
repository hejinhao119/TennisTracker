# TennisTracker: Multimodal Multi-Agent Tennis Coach

TennisTracker is an evidence-grounded coaching prototype combining local computer vision, typed evidence, specialized analysis agents, bounded orchestration, and longitudinal coaching foundations. It is not an LLM chatbot: recommendations must cite validated evidence, preserve uncertainty, and state when the current vision pipeline cannot support a conclusion.

## Current capabilities

- Existing OpenCV frame loading and YOLOv8 pose annotation remain available.
- Normalized `StrokeObservation` and auditable `EvidenceItem` contracts preserve confidence, sample size, provenance, and frame ranges.
- Deterministic evidence aggregation calculates stroke composition and contact-point ratios without an LLM.
- Match, biomechanics, and tactical agents have distinct responsibilities and structured outputs.
- Coach synthesis and a critic run through a bounded orchestration loop.
- A mock LLM provider supports deterministic local tests without paid API calls.
- Streamlit exposes upload, analysis status, limitations, coach output, and an execution trace.
- Dense pose sampling can produce a movement-pattern report with linked frame transitions and a practical shadow-swing drill.
- The report includes the source video, a movement chart, representative frames, and an evidence-linked supporting clip.

## Architecture

```mermaid
flowchart TD
	A[Video] --> B[Existing CV pipeline]
	B --> C[Typed observations]
	C --> D[Evidence layer]
	D --> E[Match agent]
	D --> F[Biomechanics agent]
	D --> G[Tactical agent]
	E --> H[Coach agent]
	F --> H
	G --> H
	H --> I[Critic]
	I -->|approved or bounded retry| J[Coaching report]
```

See [docs/architecture.md](docs/architecture.md), [docs/agent-design.md](docs/agent-design.md), and [docs/failure-modes.md](docs/failure-modes.md).

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run main.py
```

The current entry point reports pose-derived movement evidence with visual support. Stroke type, ball trajectory, court position, and in/out claims remain unavailable until those extractors are implemented.

## Testing

```powershell
python -m pytest tests
```

Tests use deterministic evidence and mock-provider paths. No API keys are required. Provider configuration belongs in environment variables; secrets are never stored in this repository.

## Evaluation and roadmap

The evaluation design and single-agent baseline are documented in [docs/evaluation.md](docs/evaluation.md). Benchmark results are intentionally not claimed until benchmark fixtures and runners exist. Planned work includes structured session persistence, historical comparison, ball/court/stroke extraction, provider adapters, observability, and evidence-linked video frame inspection.

## Limitations

The repository currently has one real tennis recording, duplicated at `data/raw/` and `testing/`. The visual report is therefore a useful prototype, not a cross-video benchmark. Serve biomechanics, tactical direction, error correlation, and performance improvement remain unavailable until their measurements and independent video fixtures are implemented and validated.