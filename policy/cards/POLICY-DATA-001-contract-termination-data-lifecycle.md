---
id: POLICY-DATA-001
title: Contract termination and customer data lifecycle
status: draft
applies_to: [contract-termination, customer-offboarding, data-transfer, data-deletion, retention]
triggers: [termination, offboarding, migration, data-transfer, delete, retention, access-revocation, destruction-certificate]
source_document: SRC-FITCLOUD-TERMS-001
source_location: "lines 142-180"
effective_from: 2025-04-02
applicability: "Default baseline after card activation unless the customer profile records an exception, separate SLA/SOW/addendum, or non-applicability; actual contract verification required for termination and legal retention"
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Contract termination and customer data lifecycle

## Control statement

After this card becomes `active`, use the standard terms as the default baseline unless the customer profile records an exception. Treat contract termination as a controlled data-transfer, access-revocation, retention, and deletion process. Do not execute any transfer or deletion from this workspace. Prepare evidence and a human-controlled plan, and verify the actual contract with CSR/legal before using a termination or legal-retention deadline.

## Scope

- Applies to customer offboarding, data migration, access removal, retained operational data, and deletion requests.
- Applies only after confirming the standard terms or an equivalent customer agreement governs the customer.

## Required behavior

1. Confirm the termination date, written notice, customer request, and applicable contract.
2. Identify customer-owned data separately from company-generated operational data.
3. Record the requested destination and human approval for transfer.
4. Prepare access revocation and deletion verification; do not execute it.
5. Verify and apply retention/deletion precedence: law/legal obligation → customer-specific contract/SLA/SOW → active standard terms → active Offboarding guide.
6. Encrypt retained data and restrict it to the stated purpose.
7. Record expiry and destruction evidence for each retained category.
8. If sources conflict or legal basis is unknown, do not select a period or propose deletion; obtain CSR/legal determination.

## Prohibited behavior

- Deleting customer data without confirmed approval and contract basis
- Treating the standard 15-business-day or 30-day period as universal
- Retaining operational data for an undefined future need
- Executing offboarding, access revocation, migration, or deletion from an agent session

## Exceptions and escalation

- Legal retention requirements and a customer deletion request may conflict; escalate to legal/human review.
- If the customer-specific agreement sets different periods, apply that agreement after verification.

## Evidence

- `SRC-FITCLOUD-TERMS-001:155-163` — requested data transfer is targeted within 15 business days; access is revoked after transfer; absent a request, deletion follows 30 days with final notice.
- `SRC-FITCLOUD-TERMS-001:165-180` — the source lists conditional retention periods, encryption, purpose limitation, customer deletion request, expiry destruction, and optional destruction confirmation.

## Change history

- 2026-08-24 — Drafted; applicability and legal interpretation require human review.
