---
id: POLICY-INCIDENT-001
title: COC support eligibility and notification routing
status: draft
applies_to: [incoming-call, incident, after-hours, monitoring-alert, security-request, ticket-assignment, aws-case]
triggers: [coc, 24x7, phone, critical, alarm, guardduty, phd, tam-req, after-hours, ticket-assignment, aws-case]
source_document: SRC-COC-GUIDE-001
source_location: "lines 116-175, 219-238"
effective_from: mixed
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# COC support eligibility and notification routing

## Control statement

Classify the customer's contracted support level, business-hours status, request type, and severity before selecting a response route. Treat Raw roles/procedures as candidates only and verify the current owner through FitCloud plus the current on-call roster on every routing decision. Agents may prepare routing notes and customer reply drafts, but must not copy contact details, make calls, send email, assign tickets, open AWS cases, or post Slack/Zendesk messages.

## Scope

- Applies to incoming calls, monitoring alarms, incidents, after-hours requests, PHD/AWS health, security-related AWS requests, ticket assignment, and AWS Case assistance.
- Applies only after current contract/support eligibility and current owner lists are verified.

## Required behavior

1. Verify customer identity, company, and the relevant AWS account using a minimal identifier appropriate to the approved process.
2. Confirm the support tier and whether 24x7/emergency coverage is contracted.
3. Classify business-hours versus after-hours handling and incident versus general inquiry.
4. Route MSP/major-customer incidents through current primary/secondary ownership and escalation roles.
5. Route non-contracted or general after-hours requests to the approved CSR/sales path unless a human has authorized emergency handling.
6. Record ticket history for security-related AWS requests and major incident communications.
7. When ownership or severity is unclear, escalate rather than selecting a named person from this source.
8. Record only the de-identified owner reference, FitCloud/on-call source reference, and verification time in tracked files.

## Prohibited behavior

- Copying personal phone numbers or stale person lists from the Raw source into tracked files
- Calling, emailing, posting Slack, assigning Zendesk tickets, or opening AWS Cases from an agent session
- Promising a 15-minute callback or 24x7 response before confirming applicability
- Treating embedded dated notes as a coherent current version
- Treating the most recently dated Raw subsection or roster as active without live FitCloud/on-call verification
- Disclosing full account identifiers when the approved script requires only a minimal check

## Exceptions and escalation

- The source contains mixed effective dates and person-specific rosters. Current FitCloud assignment, customer profile, and live on-call roster must override the Raw list.
- Alarm-level and GuardDuty routing may be customer-specific; check the customer agreement/comment before applying.
- Do not infer FitCloud customer Support Level from the AWS Support Plan. Support Level routing remains pending ingestion of the authoritative FitCloud Support Level PDF.

## Evidence

- `SRC-COC-GUIDE-001:116-133` — call handling differentiates MSP incidents, business-hours inquiries, general customers, and after-hours routing; the script asks for company/name and the last four digits of an account ID.
- `SRC-COC-GUIDE-001:134-149` — monitoring propagation distinguishes production incidents, alarm levels, MSP/major-customer escalation, and non-contracted support.
- `SRC-COC-GUIDE-001:157-167` — GuardDuty/PHD handling requires content review and customer-specific or severity-aware routing.
- `SRC-COC-GUIDE-001:169-175` — AWS TAM security requests require customer communication, history in a ticket, and internal status sharing.
- `SRC-COC-GUIDE-001:219-230` — ticket assignment differs by MSP/general status, business hours, workload, and CSR decision.
- `SRC-COC-GUIDE-001:232-238` — PLS AWS Case assistance distinguishes business hours, MSP incidents, non-MSP accounts, and additional customer emergency requests.

## Change history

- 2026-08-24 — Drafted without personal contact details; current roster, contract applicability, and mixed-date procedures require human review.
