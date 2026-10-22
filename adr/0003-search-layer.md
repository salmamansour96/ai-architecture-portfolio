# ADR-0003: Search layer

## Status
Accepted. Evidence is reasoning, not measurement.

## Context
Retrieval needs semantic search from colloquial questions to legal clauses and exact matching of article numbers, amounts and party names. It must stay inside the boundary and enforce tenant filtering. Clause counts are small for every option.

## Decision driver
Hybrid search quality and tenant filtering (P2, P5), not data volume.

## Options considered
| Option | Benefits | Costs and constraints |
| --- | --- | --- |
| A: Elasticsearch BM25 + dense vectors | Hybrid in one system; mature Arabic analyzers; strong tenant, contract-type and clause-type filters | Heavier operations |
| B: Qdrant plus separate BM25 | Simple, fast vector search | Two systems to synchronize for hybrid |
| C: pgvector plus Postgres full-text | One familiar database | Weaker Arabic full-text; more manual hybrid ranking |

## Decision
Choose A, self-hosted.

## Trade-offs we accept
More operational weight than pgvector. Configure Arabic analysis and normalization and test with a retrieval evaluation.

## Revisit when
- Elasticsearch hit rate is not better than a simpler stack on our evaluation set.
- Volume stays too small to justify operational cost.
- The embedding model changes: ingestion and queries must use the same model, so changing it requires re-indexing every contract.
