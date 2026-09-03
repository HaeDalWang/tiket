---
id: POLICY-SEC-001
title: Customer security information handling and sharing
status: draft
applies_to: [customer-data, credentials, account-access, file-sharing, external-sharing, security-incident]
triggers: [account-id, payer-id, ip, cidr, access-key, password, token, certificate, private-key, database-access, customer-file, external-share, security-incident]
source_document: SRC-CUSTOMER-SECURITY-001
source_location: "lines 3-284; repository conflict cross-reference SRC-CUSTOMER-OFFBOARD-001 lines 374-384"
effective_from: unknown
reviewed_at: 2026-08-24
reviewed_by: Hermes Agent
review_by: TBD
supersedes: ""
---

# Customer security information handling and sharing

## Control statement

Treat customer account identifiers, network information, credentials, certificates, private keys, and database access details as customer security information. Do not commit or distribute such information through an unapproved platform. Use the approved cross-account access path whenever available, minimize and time-bound any exceptional credential, and remove it immediately after the work.

This card remains `draft` because the source lists Teams and company OneDrive as approved sharing platforms but does not explicitly approve a private GitHub repository. A separate Offboarding source lists `Git` as a storage location for technical information. The repository owner selected the safe interim rule on 2026-08-24: commit only de-identified technical context until the security team or team lead approves a broader scope.

## Scope

- Applies when a ticket, profile, attachment, script, PoC handoff, or reply contains customer security information.
- Applies before sharing customer security information internally or externally.
- Applies when requesting or disposing of temporary customer credentials.
- Does not establish whether this private GitHub repository is an approved storage platform; that question is unresolved.

## Required behavior

1. Classify the information before storing or sharing it.
2. Prefer FitCloud Cross Account for customer resource access.
3. If an exceptional temporary key is required, request least privilege and an explicit validity period.
4. Delete temporary credentials immediately after work and notify the customer when applicable.
5. For approved internal file sharing, limit access to the organization and named recipients.
6. For external sharing, obtain team-lead approval, encrypt the file, separate file and password channels, and retain a sharing record.
7. After the task or project ends, remove local and shared copies according to the approved retention process.
8. On a suspected security incident, immediately escalate to the team lead and security team and request revocation of affected credentials.

## Prohibited behavior

- Personal blog, personal cloud storage, personal note application, public Git repository, or personal messenger storage
- Long-term retention of temporary credentials
- Hardcoding Access Keys in code
- External sharing without prior approval
- Sending an encrypted file and its password through the same email channel
- Copying personal contact details from operational source documents into a policy card unless operationally necessary and approved

## Exceptions and escalation

- Exceptional retention is limited to an agreed project, configuration-support, or incident-response period and requires encryption and a disposal date.
- Private GitHub storage approval is unresolved. Escalate to the security team or team lead before committing customer security information.
- If the customer does not revoke an obsolete key, request again and report to the team lead.

## Evidence

- `SRC-CUSTOMER-SECURITY-001:24-35` — “회사 및 고객사에 대한 보안 정보는 개인이 보관하지 않습니다.” The scope includes Account ID, Payer ID, IP/CIDR, credentials, tokens, certificates, private keys, and database access information.
- `SRC-CUSTOMER-SECURITY-001:41-55` — “다음 플랫폼에 고객 보안 정보 보관을 절대 금지합니다.”
- `SRC-CUSTOMER-SECURITY-001:60-74` — approved team sharing is Microsoft Teams Files or company OneDrive, restricted to internal or named users; external links are prohibited.
- `SRC-CUSTOMER-SECURITY-001:78-96` — “원칙: FitCloud Cross Account 사용”; an exception uses a least-privilege temporary key with a stated duration and immediate disposal.
- `SRC-CUSTOMER-SECURITY-001:147-161` — “2채널 분리 원칙” and “절대 이메일에 암호 포함 금지”.
- `SRC-CUSTOMER-SECURITY-001:181-200` — “원칙: 팀장 사전 승인 필수” for external sharing.
- `SRC-CUSTOMER-SECURITY-001:232-248` — immediate reporting and revocation actions for a security incident.
- `SRC-CUSTOMER-OFFBOARD-001:374-384` — the separate Offboarding guide lists technical information storage as “Outline, Git”, creating an unresolved scope conflict with the approved-platform list above.

## Change history

- 2026-08-24 — Drafted from Raw text; authority and private-GitHub applicability require human review.
- 2026-08-24 — Repository owner selected the de-identified-only interim boundary; broader company-policy approval remains unresolved.
