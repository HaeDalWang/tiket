---
id: POLICY-REMOTE-001
title: Retired TS shared remote-support access procedure
status: retired
applies_to: [remote-support, shared-account, credential-delivery, support-pc]
triggers: [remote-pc, remote-support, shared-account, password-dm, pin-dm]
source_document: SRC-TS-NOTES-001
source_location: "lines 19-27"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: N/A
approved_by: repository owner
approved_at: 2026-08-24
retired_at: 2026-08-24
retirement_reason: "The procedure is rarely used and the remote-support PC/account is to be decommissioned"
replacement: "No replacement approved; use a separately reviewed support path"
activation_blocker: "Retired procedures must never become active"
supersedes: ""
---

# Retired TS shared remote-support access procedure

## Control statement

The shared TS remote-support PC/account procedure described in the Raw notes is retired. It is not an approved access path for a human or agent. Do not use the shared account, request or retrieve its password/PIN by DM, or connect to the referenced device.

## Required behavior

1. Reject any task that depends on this retired access path.
2. Ask for a separately reviewed and individually attributable support path when remote access is required.
3. Leave actual device decommissioning, account disablement, credential revocation, and access-log review to human IT owners.
4. Record verified decommission evidence before marking the underlying device/account removed.
5. Preserve the Raw note only as historical decision evidence; never copy its IP, account, credential-delivery contacts, or other access details into tracked files.

## Prohibited behavior

- Connecting to the retired remote-support PC
- Using a shared account from the Raw note
- Requesting password or PIN through DM
- Copying access details into a ticket, profile, policy card, prompt, or repository file
- Claiming the device/account was removed without human IT evidence
- Reactivating this card

## Decommission handoff for human IT

- Identify the physical/virtual device and owner in the approved inventory.
- Disable the shared account and revoke associated credentials.
- Remove remote-access software or authorization.
- Review recent access logs and preserve required audit evidence.
- Wipe or dispose of the device through the approved asset process.
- Update the current TS/IT runbook and record completion evidence outside this agent's authority.

## Evidence

- `SRC-TS-NOTES-001:19-27` — the Raw note describes a remote-support PC, a shared account, credential retrieval by DM, and pre/post access notification. Sensitive values and identities are intentionally not reproduced.
- Repository-owner decision on 2026-08-24 — the procedure is rarely used and should be retired with human IT decommissioning.

## Change history

- 2026-08-24 — Created directly as `retired`; no active period is recognized in this repository.
