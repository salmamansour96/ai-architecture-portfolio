# Session 2: Use-Case Flow View

**Use case:** risky-clause recommendation. A user opens a contract, and for each risky clause the system shows a safer alternative from the reviewed Clause Library, as a proposal for review with a lawyer disclaimer (P3, P4).

**Diagram:** `diagrams/src/02-usecase-flow.drawio` (PNG: `diagrams/02-usecase-flow.png`)

## Mapping to the high-level architecture

| High-level component | In this system |
|---|---|
| Channels + API Gateway | API Gateway (authN/authZ, `tenant_id` from token) |
| E-commerce service + operational DB | Contract Service + operational DB (ownership, status) |
| CDC > Kafka > Flink | Queue + Ingestion Worker |
| Airflow + CDP | Airflow batch jobs (recompute when the Clause Library changes) |
| Feature store + vector DB | Elasticsearch (BM25 + vectors + precomputed recommendations) |
| Recommendation engine | Risk scoring + Clause Library lookup |
| WhatsApp | Not used |

## Two paths

- **Background (B1-B9):** upload, ingestion, embedding and indexing, then risk scoring and library lookup for **both parties**, with top-K recommendations stored per clause and party. Airflow recomputes affected contracts when the library changes.
- **Real-time (R1-R7):** auth, ownership check on the operational DB, one read of precomputed recommendations from Elasticsearch, then the response with the disclaimer.

## Options compared

| | A: Precompute at ingestion | B: Real-time (search + rerank + LLM per open) |
|---|---|---|
| Latency | One read | Several chained steps, including an LLM call |
| Cost | GPU once per contract | GPU on every open |
| Load on operational DB | One light read (ownership) | Same, plus more queries |
| Freshness | Stale until recomputed | Always current |

**Decision: A.** It wins on latency, cost, and load on the operational DB. A contract does not change after upload, and scoring both parties in advance means we do not need the user's role at compute time. The trade-off is staleness when the Clause Library changes. The Airflow job covers that, and a real-time fallback (async, with a loading state) covers a miss or a stale entry.

## Over-engineering check

- **Not needed:** CDC > Kafka > Flink (an upload is an explicit event, so a queue is enough), CDP (no behavior profile), WhatsApp (at most an optional "contract ready" ping).
- **Missing from the high-level view:** Object Storage for original files, and local OCR, LLM and reranker serving.

## Latency budget (real-time path)

Assumed targets, to be measured. P95 target: 800 ms.

| Hop | Budget |
|---|---|
| Gateway + auth | 50 ms |
| Ownership check (operational DB) | 30 ms |
| Elasticsearch read | 100 ms |
| Assemble + disclaimer | 50 ms |
| Network + UI | 200 ms |
| **Total** | **430 ms** (370 ms headroom) |
