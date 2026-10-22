# Session 1 — Governance pack

## Purpose
Govern Bonod, a bilingual Arabic/English Contract Review Assistant using RAG.
Protect confidential contracts while grounding answers and reviewed alternatives in traceable sources.

## Principles
| Principle | Rule | Business goal | Verification |
| --- | --- | --- | --- |
| P1 Confidential and untrusted | Self-host LLM, OCR and search; contract text never leaves the boundary or enters logs, analytics or unscoped caches. Delimit text as data, never instructions. | Client trust, PDPL compliance, injection protection. | No outbound calls; CI log and delimiter checks; injection test set. |
| P2 Grounded or silent | Answer from retrieved text with clause/page citations; if unsupported, say the contract does not mention it. | Reduce legal risk. | Citation accuracy and faithfulness thresholds; CI citation rule. |
| P3 Library-only recommendations | Retrieve alternatives from the reviewed Clause Library; never invent clauses. | Legally reviewed wording. | Require source_clause_id; block recommendations without it. |
| P4 Human oversight | Legal-position changes are proposals with lawyer-review disclaimer; never apply automatically. Flag rule-score/LLM-judge disagreement as “needs human review”. | Legal accountability. | Explicit user confirmation before modification; flag and count disagreements. |
| P5 Least privilege | Authenticate/authorize every request; retrieve only owned/shared contracts. Force tenant_id from server-side auth token, never request body; admins cannot access text. | Trust, PDPL compliance, no cross-tenant leaks. | Cross-tenant test; CI tenant-filter check on every search. |

## ADR summary
| ADR | Decision | Status | Driver |
| --- | --- | --- | --- |
| [0001](../adr/0001-llm-hosting.md) | Self-hosted open-source LLM | Accepted | P1 |
| [0002](../adr/0002-ocr-provider.md) | Local open-source OCR; low-confidence pages need review | Accepted (verification by spike required; no results supplied) | P1 |
| [0003](../adr/0003-search-layer.md) | Self-hosted Elasticsearch hybrid: BM25 + dense vectors | Accepted | P2, P5 |

Evidence for 0001 and 0003 is reasoning, not measurement. Faithfulness evaluation would change 0001; retrieval hit-rate evaluation would change 0003. OCR verification uses the specified spike, without claiming an unreported result.

## ARB checklist
Thresholds are set before testing and written down. Questions below require evidence, not assumed passes.

| ID | Question | Principle |
| --- | --- | --- |
| **Security** | | |
| S1 | Every request authenticated/authorized before retrieval; admins denied contract text? | P5 |
| S2 | Every search tenant filter built server-side? | P5 |
| S3 | Cross-tenant test passed? | P5 |
| S4 | Contract text delimited as data; injection test set passed? | P1 |
| **Privacy (PDPL)** | | |
| D1 | Contract text stays inside boundary; no outbound calls? | P1 |
| D2 | Lawful basis and user consent for personal-data processing documented? | P1 |
| D3 | Storage location and retention period defined? | P1 |
| D4 | User can delete contract and all chunks, embeddings, caches and feedback? | P1, P5 |
| D5 | No contract text in logs, analytics or error reports? | P1 |
| **Evals** | | |
| E1 | Citation accuracy/faithfulness meet thresholds on 30–50 questions, including correct unanswerable abstention? | P2 |
| E2 | Every recommendation has library source_clause_id? | P3 |
| E3 | Expert risk-score agreement and alternative relevance measured on 20 risky clauses? | P3, P4 |
| E4 | OCR spike on 20 scanned Arabic contracts meets clause-number accuracy threshold? | P2 |
| **Cost** | | |
| C1 | Monthly GPU/hosting cost and cost per contract estimated and measured? | ADR-0001 |
| C2 | File-size, page and per-user query limits in place? | P5 |
| **Human oversight** | | |
| H1 | Recommendations are proposals with disclaimer; no modification without user confirmation? | P4 |
| H2 | Rule-vs-LLM disagreements flagged and counted? | P4 |
| H3 | Lawyers review library entries; users can report wrong answers? | P3, P4 |

D2 and D3 need confirmation by someone with PDPL legal expertise. **Production triggers:** the board blocks release if any of S2, S3, D1, D5, E1, E2 or H1 is “no”.

## Business metrics
**Targets to validate in a pilot, not measured results**

| Principle | Business metric | Target |
| --- | --- | --- |
| P1 | Outbound/leak incidents | 0 |
| P2 | Answers with material error in weekly lawyer-reviewed sample of 20 | Below 2% |
| P3 | Recommendations accepted by lawyer without material edits | At least 70% |
| P4 | High-risk clauses reaching human review | 100% |
| P5 | Cross-tenant test leaks | 0 |

Headline value metrics: risky-clause recall against an expert baseline (prefer recall over precision); review time versus manual review (measure the manual baseline first); cost per contract. Guardrail metrics: abstain rate (zero is suspicious), human-review flag rate, and error-report rate.

## CI guardrail
[Static checks](../guardrails/check_guardrails.py) run on pull requests. The supplied prompt and search stub demonstrate the required patterns; they are not a production implementation.

| Check | Looks for | Principle |
| --- | --- | --- |
| Citation rule | Every prompt template contains {{CITATION_RULE}} and {{ABSTAIN_RULE}}. | P2 |
| Contract text safety | {{CONTRACT_TEXT}} inside contract_text tags; instruction treats it as data, never instructions; no logger/print receives contract_text, chunk_text or ocr_text. | P1 |
| Tenant filter | Only services/search.py imports Elasticsearch; search_chunks(user, query) builds filter from user.tenant_id. | P5 |

This static check does not prove model obedience: evals do that. A cross-tenant integration test is still required. Static pattern checks cannot prove runtime authorization, complete data-flow safety or tenant isolation.

## Diagram
[Editable draw.io architecture](../diagrams/src/01-governance-architecture.drawio) · [PNG export](../diagrams/01-governance-architecture.png)
