# Company Policy Knowledge Base

This directory stores routing metadata and normalized policy cards. It must not inject every company document into the model context.

## Retrieval flow

1. Classify the current ticket by customer, service, action, data type, and risk.
2. Search `_라우팅.md` for matching triggers.
3. Read only the matching cards in `카드/`.
4. Open the relevant extracted section or original page only when the card is insufficient.
5. Record applied policy IDs, source pages, and effective dates in the ticket.
6. If two active policies conflict, stop and escalate to a human.

## Language contract

- Routing metadata, agent instructions, and normalized control statements: English where practical.
- Original company documents: preserve their source language without rewriting.
- Human-facing ticket notes and customer replies: Korean.
- Technical identifiers and quotations: preserve exactly.

## Storage layers

- `_라우팅.md`: compact policy index loaded for routing.
- `카드/`: short, reviewed policy cards with scope and source pointers.
- `추출본/`: searchable OCR/text derivatives when approved for this repository.
- `원본_목록.md`: source inventory and storage pointer.
- `원본/`: local source documents; gitignored by default. Use an approved document system or Git LFS only after an explicit decision.

## Ingestion rules

- Never treat OCR output as authoritative without checking the source page for a load-bearing clause.
- Every card must identify source document, page/section, effective date, status, and review date.
- A superseded policy remains in history but must be marked `superseded` and linked to its replacement.
- Never store credentials or unrestricted raw operational logs with policy sources.
