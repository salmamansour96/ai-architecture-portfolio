# ADR-0001: LLM hosting

## Status
Accepted. Evidence is reasoning, not measurement.

## Context
Contracts are confidential. Answers must support Arabic and citations. PDPL limits where personal data can go.

## Decision driver
P1: contract text stays inside the trust boundary.

## Options considered
| Option | Benefits | Costs and constraints |
| --- | --- | --- |
| A: Commercial API | Best Arabic quality; no GPU operations | Text leaves boundary; vendor dependency; per-token cost |
| B: Self-hosted open-source, such as Qwen, Llama or Jais | Data stays inside; predictable cost; full logging control | GPU and operations; weaker Arabic and long-context quality |
| C: API with zero-retention contract | Better quality than B | Data still leaves; compliance depends on trust, which P1 disallows |

## Decision
Choose B. Select the exact model by evaluating candidates on our own evaluation set.

## Trade-offs we accept
Lower Arabic and reasoning quality, offset by strict grounding (P2), retrieval quality and the reviewed Clause Library (P3). GPU cost and operational load remain.

## Revisit when
- A vendor offers in-region hosting with a legally binding no-retention agreement that passes PDPL review.
- Open-source models fail the faithfulness threshold.
- Volume is too low to justify GPU cost.
