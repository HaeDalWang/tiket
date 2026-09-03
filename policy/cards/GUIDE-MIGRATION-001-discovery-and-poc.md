---
id: GUIDE-MIGRATION-001
title: Migration discovery and PoC decision intake
status: draft
applies_to: [migration, discovery-meeting, assessment, poc, scope-definition, expectation-setting]
triggers: [migration, first-meeting, discovery, assessment, poc, rehost, replatform, refactor, retire, retain]
source_document: SRC-MIGRATION-MEETING-001
source_location: "lines 3-180, 187-300"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Migration discovery and PoC decision intake

## Control statement

Use an initial migration discussion to understand the customer's current state, goals, constraints, decision process, and the next validated step. Do not promise architecture, timeline, support coverage, savings, or migration feasibility before assessment and PoC evidence.

## Scope

- Applies to first migration meetings, discovery tickets, assessment requests, and PoC handoff preparation.
- Does not replace a migration assessment, SOW, architecture review, contract, or implementation plan.

## Required behavior

1. Identify industry/regulatory context, decision makers, business goals, and internal team roles.
2. Capture infrastructure, application dependencies, operations/DR, current cost awareness, contract expiry, and migration timing.
3. Ask what must move, by when, and to what target level; separate quick wins from transformation.
4. Label migration strategy as an option pending assessment rather than a commitment.
5. Agree on the next step, required customer information, schedule, NDA/contract form, and owners.
6. Convert a technical uncertainty into a bounded PoC request through `handoff/README.md`.
7. Record decision, owner, due date, and unresolved risk in the ticket.

## Prohibited behavior

- Promising feasibility, delivery date, savings, 24x7 support, or a migration approach before evidence and contract verification
- Treating a first meeting as approval to access or modify the customer environment
- Copying a generic reference architecture into the customer answer without verifying dependencies
- Sending the follow-up email directly from an agent session

## Exceptions and escalation

- The source lists “24x7 기술 지원” as partner value, while `POLICY-SUPPORT-001` says emergency support requires a separate contract. Verify the customer contract before using that statement.
- Program and pricing eligibility require current CSR/AWS verification.

## Evidence

- `SRC-MIGRATION-MEETING-001:8-10` — success is agreement on the next step, not a proposal request.
- `SRC-MIGRATION-MEETING-001:15-52` — internal readiness covers regulatory context, decision structure, goals, roles, and partner positioning.
- `SRC-MIGRATION-MEETING-001:57-108` — discovery covers infrastructure, applications, operations, costs/contracts, target scope/timing, and warns against overpromising.
- `SRC-MIGRATION-MEETING-001:130-154` — next-step agreement includes assessment, required data, timeline, milestones, NDA, and PoC/full-migration contract form.
- `SRC-MIGRATION-MEETING-001:159-194` — follow-up captures goals, actions/owners/deadlines, internal alignment, and initial risk.
- `SRC-MIGRATION-MEETING-001:230-275` — question template and 6R reference support discovery but do not prove the selected strategy.
- `SRC-MIGRATION-MEETING-001:299-300` — source updated 2026-02-10 and attributed to SA Team.

## Change history

- 2026-08-24 — Drafted; contract promises and current program eligibility require human verification.
