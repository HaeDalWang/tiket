---
id: GUIDE-ROLE-001
title: CSG role routing and handoff
status: draft
applies_to: [ticket-routing, escalation, poc, architecture, managed-operations, fitcloud, billing-platform, ai-workload]
triggers: [sa, ts, msp, ai, cop, architecture, poc, incident, runbook, fitcloud, rebilling, billing-error, ai-workload, handoff]
source_document: "SRC-CSG-JD-001 and team-specific JD sources"
source_location: "CSG aggregate lines 5-237; team-specific files lines 3-end"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# CSG role routing and handoff

## Control statement

Route work by the human team's documented purpose while preserving contract and customer ownership. SA owns requirement analysis, architecture, technical validation, and design handoff; TS owns general/project technical support and escalations; MSP owns contracted managed operations and customer lifecycle; AI owns AI/ML architecture and PoC/production-transition support; COP owns FitCloud/Rebilling platform and billing-data system issues. This mapping routes work but does not grant an AI agent authority to execute a human team's write operations.

## Scope

- Applies to ticket assignment suggestions, escalation, cross-team handoff, PoC ownership, and the selection of a separate implementation project.
- Does not establish current staffing, on-call ownership, customer-specific primary/secondary assignment, or approval authority.

## Required behavior

1. Identify the customer support tier and request type before choosing a team.
2. Route architecture, Well-Architected review, technical validation, and design/build handoff to SA.
3. Route general-customer troubleshooting, project technical support, AWS Support escalation, and runbook work to TS.
4. Route contracted MSP incidents, reports, optimization, primary/secondary ownership, and onboarding/offboarding to MSP.
5. Route AI architecture, AI PoC, model/data pipeline, and AI production-transition questions to AI.
6. Route FitCloud/Rebilling, cost allocation, billing-data pipeline, and platform defects to COP.
7. Record the handoff question, evidence, owner, expected result, and receiving repository/team.
8. Verify current ownership in FitCloud/customer profile or with a human; do not infer it from role documents alone.

## Prohibited behavior

- Treating a team JD as customer contract scope
- Executing a human team's account, deployment, billing, support-case, or platform-write action
- Routing solely by a person's name from a stale document
- Assuming individual team files supersede the aggregate CSG document
- Using role evaluation metrics as customer commitments

## Exceptions and escalation

- Team-specific JDs add competency levels and sometimes stronger execution language than the aggregate source. No version/effective-date metadata establishes precedence; resolve conflicts with CSG leadership.
- Customer-specific primary/secondary ownership and contracts override generic role routing.
- COP owns platform billing accuracy while MSP reports cost/resource status through FitCloud; the sources do not define the final owner who approves a customer-facing billing figure. Apply the FitCloud-only repository rule and obtain current COP/MSP confirmation.

## Evidence

- `SRC-CSG-JD-001:5-59` — SA covers business requirements, architecture, PoC/verification, project scope/risk, and handoff.
- `SRC-CSG-JD-001:64-99` — TS covers general/project support, incident/change/problem management, AWS escalation, and runbooks.
- `SRC-CSG-JD-001:104-144` — MSP covers managed operations, SLA incidents, reports, advice, primary/secondary ownership, and onboarding/offboarding.
- `SRC-CSG-JD-001:149-181` — AI covers AI/ML architecture, PoC, production transition, workshops, and operational alignment.
- `SRC-CSG-JD-001:186-217` — COP covers Rebilling, cost allocation, billing data, platform change/incident management, and data separation.
- `SRC-SA-JD-001:3-58`, `SRC-TS-JD-001:3-74`, `SRC-MSP-JD-001:3-84`, `SRC-AI-JD-001:3-68`, `SRC-COP-JD-001:3-66` — team-specific variants add competency and detailed responsibility but provide no explicit version precedence.

## Change history

- 2026-08-24 — Drafted; source precedence and current organizational ownership require human review.
