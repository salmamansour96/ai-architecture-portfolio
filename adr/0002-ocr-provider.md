# ADR-0002: OCR provider

## Status
Accepted. Verification by the spike below is required; no measured results were supplied.

## Context
Many contracts arrive as scans. Broken Arabic letters and lost clause numbers corrupt chunking and citations (P2). Scans contain full contract text, so images must stay inside the boundary (P1).

## Decision driver
P1: no contract image leaves the trust boundary.

## Options considered
| Option | Benefits | Costs and constraints |
| --- | --- | --- |
| A: Local open-source: Tesseract, Surya, EasyOCR | Processing inside boundary | Lower accuracy on poor scans |
| B: Cloud OCR: Google Document AI, Azure | Cloud OCR accuracy | Images leave boundary; violates P1 |
| C: Local OCR plus human review for low-confidence pages | Local processing with review safety net | Manual attention before readiness |

## Decision
Use A with C's safety net. Pages below a confidence threshold, or with unparseable clause numbers, set the contract to needs_review instead of silently indexing bad text. No contract image leaves the boundary.

## Trade-offs we accept
Lower accuracy than the best cloud OCR on poor scans; some contracts need manual attention before becoming ready.

### Verification (spike)
Run on 20 scanned Arabic contracts of mixed quality. Measure character error rate and clause-number accuracy against thresholds written down before testing. The spike checks the decision; it does not make it.

If thresholds are missed, improve inside the boundary first: preprocessing, a different local model, fine-tuning, or a stricter needs_review rule. Cloud OCR requires a new superseding ADR and an explicit ARB exception to P1.

## Revisit when
- The share of needs_review contracts is too high for users.
- A better local Arabic OCR model appears.
