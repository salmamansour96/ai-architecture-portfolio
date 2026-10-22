# AI Architecture Portfolio

Coursework and capstone for the AI Architecture Design course. The system used throughout the course is a Contract Review Assistant (working name: Bonod): a bilingual Arabic/English RAG system that answers questions about uploaded contracts with clause and page citations, flags risky clauses, and recommends safer alternatives from a reviewed Clause Library.

| Folder | Contents |
| --- | --- |
| docs/ | One document per session |
| diagrams/ | Architecture diagrams |
| adr/ | Architecture decision records |
| capstone/ | Final document and slides |

## Sessions
### Session 1 - Governance pack

| Deliverable | File |
| --- | --- |
| Governance pack | [Session 1 governance pack](docs/01-governance-pack.md) |
| Diagram | [Governance architecture](diagrams/src/01-governance-architecture.drawio) |
| ADR 0001 | [LLM hosting](adr/0001-llm-hosting.md) |
| ADR 0002 | [OCR provider](adr/0002-ocr-provider.md) |
| ADR 0003 | [Search layer](adr/0003-search-layer.md) |
| Guardrail | [CI guardrail checks](guardrails/check_guardrails.py) |
