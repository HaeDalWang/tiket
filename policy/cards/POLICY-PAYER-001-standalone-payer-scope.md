---
id: POLICY-PAYER-001
title: Standalone Payer scope and escalation
status: draft
applies_to: [standalone-payer, partner-link, billing-visibility, support-scope, payer-transition]
triggers: [standalone-payer, payer, partner-link, fitcloud, cur, rebilling, cost-visibility, integrated-payer, technical-support]
source_document: SRC-STANDALONE-PAYER-001
source_location: "lines 3-147, 149-200, 430-620, 715-764"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Standalone Payer scope and escalation

## Control statement

Use this guide only for standalone-Payer concepts, role boundaries, and general constraints. Before answering a billing, account-management, support, FitCloud, or CUR question, identify the Payer model and verify fees/thresholds/support with CSR, current product behavior with COP, and customer-visible results in FitCloud. Do not promise integrated-Payer capabilities to a standalone-Payer customer.

## Scope

- Applies to standalone Payer onboarding, partner link, support scope, billing visibility, CUR, FitCloud, and transition discussions.
- Does not authorize partner-link, account-transfer, permission, or billing-system changes.

## Required behavior

1. Confirm the customer's Payer model and applicable contract before investigating capability or cost.
2. Record whether account management remains the customer's responsibility.
3. Verify whether technical support, CUR data, FitCloud, and cost visibility are included or separately contracted.
4. Route general/contract questions to CSR, technical/system questions to COP or SA, and exceptions/disputes to CSG leadership.
5. Treat a transition to integrated Payer as a separate approved project with backup, IAM, tagging, recovery, network, contract, and billing considerations.
6. Use only approved FitCloud-curated figures in a customer-facing cost response. Do not copy internal figures or AWS-origin values from this guide.
7. Record the Payer model, verification date, CSR contract reference, COP feature verification, and FitCloud observation in the customer profile or ticket.

## Prohibited behavior

- Assuming FitCloud or Rebilling is available to a standalone-Payer customer
- Quoting the guide's fees, thresholds, targets, or discount claims without current contract/FitCloud verification
- Executing partner invitation, account transfer, IAM, resource migration, or billing configuration
- Using AWS Cost Explorer output in a customer reply
- Treating roadmap items as delivered capabilities
- Treating internal fees, volume thresholds, discount claims, conversion targets, or feature statements as current without CSR/COP/FitCloud verification

## Exceptions and escalation

- The guide contains roadmap and target figures rather than only current controls; these are not customer commitments.
- The source states FitCloud is not provided for the standalone model, while other company systems may expose administrative billing data. Verify the active product and contract rather than resolving this from the guide alone.

## Evidence

- `SRC-STANDALONE-PAYER-001:4-15` — standalone Payer is defined as customer-owned account management with direct AWS payment and a partner link.
- `SRC-STANDALONE-PAYER-001:65-120` — pre-review, leadership approval, limited support, separate technical-support contract, Rebilling/FitCloud constraints, and internal fee statements.
- `SRC-STANDALONE-PAYER-001:149-199` — customer account/security/cost responsibility is separated from Saltware partner-link and optional support.
- `SRC-STANDALONE-PAYER-001:463-551` — transition criteria and process include customer approval, account migration, permission, billing, backup, network, contract, and support changes.
- `SRC-STANDALONE-PAYER-001:553-620` — role and escalation mapping assigns CSR, SA, COP, MSP, and CSG leadership responsibilities.
- `SRC-STANDALONE-PAYER-001:715-764` — roadmap items are separate from current process; source updated 2026-02-20 and reviewed by CSG leadership.

## Change history

- 2026-08-24 — Drafted; active product behavior, customer contract, and fee validity require human verification.
