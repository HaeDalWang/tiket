---
id: POLICY-OFFBOARD-001
title: Customer offboarding approval and data handling
status: draft
applies_to: [customer-offboarding, partner-transfer, csp-migration, service-termination, access-revocation, data-deletion]
triggers: [offboarding, terminate, migration, partner-change, account-disable, access-remove, data-delete, archive, retention]
source_document: SRC-CUSTOMER-OFFBOARD-001
source_location: "lines 75-215, 315-424, 650-670"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: 2026-05-12
activation_blocker: "CSG Leadership must confirm the current version and set a new review date"
supersedes: ""
---

# Customer offboarding approval and data handling

## Control statement

Treat customer offboarding as a human-controlled, approval-gated transition. Separate partner transfer, CSP migration, and service termination scenarios; define handoff, rollback, data ownership, retention, access revocation, and deletion evidence before any action. Agents prepare and verify artifacts only.

## Scope

- Applies to partner transfer, CSP migration, service termination, access removal, data transfer, archive, and deletion.
- Complements a verified customer contract and `POLICY-DATA-001`; it does not replace them.

## Required behavior

1. Classify the offboarding scenario and confirm the customer-approved schedule.
2. Assign human owners for overall coordination, technical handoff, data management, access revocation, finance, and legal review.
3. Inventory customer data, operational data, technical documents, personal data, credentials, monitoring, and access paths.
4. Prepare rollback and integrity verification before migration or deletion.
5. Require explicit customer approval before customer-data deletion and production-environment deletion.
6. Record deletion approval, execution owner, verification, and history.
7. Apply verified retention/deletion precedence: law/legal obligation → customer-specific contract/SLA/SOW → active standard terms → active Offboarding guide.
8. Remove personal data after the minimum required period and preserve only approved archives.
9. If sources conflict or legal basis is unknown, stop without selecting a period, deleting data, or retaining it indefinitely; obtain legal/human determination.

## Prohibited behavior

- Executing account disablement, environment deletion, snapshot deletion, access revocation, or data transfer from an agent session
- Using the generic timeline or retention table without checking the customer contract
- Deleting customer data without explicit approval
- Treating a role assignment in the guide as permission for an AI agent
- Copying operational contact PII or credentials into policy cards

## Exceptions and escalation

- The guide states that technical information may be stored in `Outline, Git`, while `POLICY-SEC-001` notes a source that lists Teams/company OneDrive as approved sharing platforms. Repository scope requires security-owner resolution.
- Source retention periods differ from the standard terms in some categories. Contract/legal review is required.

## Evidence

- `SRC-CUSTOMER-OFFBOARD-001:82-124` — partner-transfer stages include customer approval, handoff, staged permissions, account disablement, signatures, and a final report.
- `SRC-CUSTOMER-OFFBOARD-001:132-148` — the source classifies retained and immediately deleted data, including tickets, logs, monitoring data, access, and contract records.
- `SRC-CUSTOMER-OFFBOARD-001:170-215` — CSP migration includes risk/rollback planning, data verification, and explicit approval for production deletion.
- `SRC-CUSTOMER-OFFBOARD-001:320-350` — customer approval precedes deletion; the source lists destructive AWS/S3/EBS/RDS/backup/log actions.
- `SRC-CUSTOMER-OFFBOARD-001:374-384` — storage-location table lists technical information under “Outline, Git” and personal information under CRM.
- `SRC-CUSTOMER-OFFBOARD-001:386-423` — immediate access removal, constrained archive, personal-data minimization, and destruction history.
- `SRC-CUSTOMER-OFFBOARD-001:653-662` — roles assign overall coordination, technical handoff, data, access, finance, and legal responsibilities.
- `SRC-CUSTOMER-OFFBOARD-001:667-670` — version 1.0, updated 2026-02-12, next review 2026-05-12, marked approved by Saltware CSG Leadership.

## Change history

- 2026-08-24 — Drafted; overdue review date, contract precedence, retention conflicts, and repository scope require human review.
