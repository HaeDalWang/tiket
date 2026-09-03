---
id: POLICY-SUPPORT-001
title: Contract-dependent service scope and response targets
status: draft
applies_to: [support-scope, ticket-severity, response-time, emergency-support, customer-duty]
triggers: [sla, slt, critical, high, medium, low, response-time, business-hours, emergency, 24x7, support-contract]
source_document: SRC-FITCLOUD-TERMS-001
source_location: "lines 24-89, 127-137, 247-251"
effective_from: 2025-04-02
applicability: "Default baseline after card activation unless the customer profile records an exception, separate SLA/SOW/addendum, or non-applicability"
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Contract-dependent service scope and response targets

## Control statement

After this card becomes `active`, use the standard terms as the default baseline unless the customer profile records an exception, separate SLA/SOW/addendum, or non-applicability. Classify the request by the applicable severity model and distinguish a target (`SLT`) from a compensation-bearing commitment. Legally consequential interpretation still requires actual-contract verification.

## Scope

- Applies to questions about support hours, severity, first-response targets, monitoring, incident response, reports, and emergency support.
- Applies to obligations assigned to the customer or company under the standard terms.
- Does not replace a customer-specific contract, SLA, SOW, or addendum.

## Required behavior

1. Read the customer profile for recorded exceptions, separate SLA/SOW/addendum, or non-applicability before quoting scope or time.
2. Distinguish normal operating hours from separately contracted 24x7 emergency support.
3. Record severity classification and why it applies.
4. Describe response times as targets unless the customer contract states otherwise.
5. Confirm customer prerequisites such as least-privilege access, change notice, payment, and cooperation with security measures.
6. If a security incident is confirmed and the terms apply, route the customer-notification deadline to a human owner; an agent must not send the notification.

## Prohibited behavior

- Promising 24x7 response without confirming the additional contract
- Treating the standard-terms SLT as an unconditional SLA or damages commitment
- Quoting a severity response time without classifying the incident
- Using this card as proof that a specific customer accepted the terms
- Sending customer notification directly

## Exceptions and escalation

- When a customer-specific agreement conflicts with this card, the customer-specific agreement controls after human verification.
- Contract interpretation, damages, termination, and legal disputes require human/legal review.
- FitCloud customer Support Level may define support hours, 24x7 eligibility, severity, and routing independently of the AWS Support Plan. This card remains blocked for those claims until the authoritative Support Level PDF is ingested and reviewed.

## Evidence

- `SRC-FITCLOUD-TERMS-001:24-30` — the terms become effective when the customer enters the service agreement.
- `SRC-FITCLOUD-TERMS-001:37-49` — service scope includes design/build support, monitoring/incident response, ticket support, cost optimization, security, and reports; details are set by a separate SLA.
- `SRC-FITCLOUD-TERMS-001:51-69` — normal hours are weekdays 09:00–18:00 KST; 24x7 emergency support applies only when separately contracted; severity response values are described as targets.
- `SRC-FITCLOUD-TERMS-001:71-89` — customer and company duties include least-privilege access and confidentiality.
- `SRC-FITCLOUD-TERMS-001:127-137` — the source states customer notification within 24 hours after awareness of a security incident.
- `SRC-FITCLOUD-TERMS-001:247-251` — the source states an effective date of 2025-04-02.

## Change history

- 2026-08-24 — Drafted; customer applicability and legal authority require human review.
