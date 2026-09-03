# ADR-002: Use structured agent outputs

Agents return typed reports instead of prose-only responses. This enables validation, UI rendering, evidence-reference checks, and deterministic tests. It constrains expressive output, but reliability matters more than unconstrained summaries.