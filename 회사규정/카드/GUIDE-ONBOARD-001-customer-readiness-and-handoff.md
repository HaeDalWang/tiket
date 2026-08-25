---
id: GUIDE-ONBOARD-001
title: Customer onboarding readiness and handoff
status: draft
applies_to: [customer-onboarding, architecture-baseline, access-readiness, monitoring, handoff]
triggers: [new-customer, onboarding, kickoff, access-setup, monitoring-setup, handoff, operation-start]
source_document: SRC-CUSTOMER-ONBOARD-001
source_location: "lines 70-200, 330-467"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Customer onboarding readiness and handoff

## Control statement

Use the source as a completeness checklist, not blanket authorization to modify a customer account. Before operational handoff, document the current architecture, establish approved access, verify monitoring/backup/ticket paths, record unresolved risk, and obtain the required human confirmations.

## Scope

- Applies to new MSP/customer onboarding and transition from design/build to operations.
- Applies to ticket context, access readiness, documentation, monitoring, backup, escalation, and handoff.
- Does not authorize an agent to create IAM users, modify networks, enable services, configure alarms, or perform any customer-account write.

## Required behavior

1. Capture the current environment and customer-approved architecture baseline.
2. Identify every access or configuration item that requires a human owner and customer approval.
3. Verify least privilege, MFA, and secure credential delivery in the human-controlled implementation plan.
4. Complete SA-to-MSP handoff with architecture intent, known issues, customer requirements, and checklist status.
5. Before declaring onboarding complete, verify access, monitoring, alarms, backup/restore, ticketing, communication, documents, and escalation contacts.
6. Record incomplete items, risk level, owner, and target date.
7. Obtain human approval from the required customer and internal roles.

## Prohibited behavior

- Executing IAM, network, monitoring, security, backup, or billing changes from an agent session
- Treating a blank checklist item as evidence that the control is complete
- Declaring onboarding complete without handoff evidence and human confirmation
- Copying credentials or customer security information into the ticket repository

## Exceptions and escalation

- Customer-specific SOW/SLA and access constraints override the generic checklist.
- Unsupported or high-risk controls require a separate PoC or implementation project through `연계/README.md`.

## Evidence

- `SRC-CUSTOMER-ONBOARD-001:75-98` — architecture review, documentation, and customer review/approval are checklist items.
- `SRC-CUSTOMER-ONBOARD-001:103-137` — IAM, network, CLI, ticket, channel, document, and monitoring access are explicit setup items with assigned roles.
- `SRC-CUSTOMER-ONBOARD-001:339-347` — SA-to-MSP handoff includes design intent, known issues, customer characteristics, and checklist confirmation.
- `SRC-CUSTOMER-ONBOARD-001:352-385` — final verification, document finalization, completion report, customer confirmation, first report/meeting, and retrospective.
- `SRC-CUSTOMER-ONBOARD-001:438-446` — the source contains approval rows for customer, CSR, SA, MSP, and CCoE leadership.
- `SRC-CUSTOMER-ONBOARD-001:466-468` — version 1.0, updated 2026-02-12; next review is after an onboarding retrospective.

## Change history

- 2026-08-24 — Drafted; checklist ownership and current approval status require human review.
