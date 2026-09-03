---
id: GUIDE-FITCLOUD-001
title: FitCloud cost-data freshness limitations
status: draft
applies_to: [fitcloud, billing-data, data-freshness, delayed-update, month-end]
triggers: [fitcloud-delay, cur-update, billing-period, data-time, stale-cost, month-end, queue]
source_document: SRC-COP-QA-001
source_location: "lines 4-16"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# FitCloud cost-data freshness limitations

## Control statement

Do not interpret the time shown in FitCloud as proof that all source billing data through that time has been processed. When investigating apparent delay, distinguish AWS source-data delivery, the source data's own coverage time, and FitCloud processing/queue time. Re-verify current platform behavior before using this draft guidance.

## Scope

- Applies to questions about delayed FitCloud cost reflection, CUR update time, processing time, and increasing month-end latency.
- Does not authorize use or disclosure of raw AWS billing values in a customer reply.

## Required behavior

1. Record the requested billing period and the exact FitCloud observation time.
2. Confirm the latest available FitCloud-curated data before quoting customer figures.
3. Distinguish source delivery, data coverage, queue wait, and processing completion.
4. If current behavior is needed, route a platform verification question to COP and record the live result.
5. Explain uncertainty without promising a fixed refresh interval that has not been verified.

## Prohibited behavior

- Treating a displayed timestamp as complete source coverage
- Quoting raw AWS/CUR figures to a customer
- Claiming a fixed daily delivery count or queue architecture as current without live verification
- Copying customer names, account IDs, or support-plan examples from the Raw Q&A

## Exceptions and escalation

- Platform implementation may have changed since this undated Q&A. Live FitCloud behavior and current COP confirmation outrank this card.

## Evidence

- `SRC-COP-QA-001:4-16` — the source says CUR delivery is periodic, delivered data may lag its delivery time, Payer jobs may queue sequentially, and month-end volume can increase delay.

## Change history

- 2026-08-24 — Drafted from Q&A; current implementation and authority require COP review.
