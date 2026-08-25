# Agent Entry Point

## Required first action

Read the root `CLAUDE.md` in full before doing any work. It is the canonical contract for workflow, authority, evidence, policy routing, PoC handoff, relationship context, reply style, and file rules.

## Repository purpose

This is a customer technical-ticket context and decision-history workspace, not the infrastructure code repository. Actual Terraform and implementation code live under `~/salt/<customer>/` or another designated project.

## Non-negotiable summary

- Produce customer reply drafts only. Never send email or post Zendesk comments.
- Customer AWS/FitCloud inspection is currently blocked while `aws-customer-account-ops` is under developer repair. Do not invoke an existing copy; follow `에이전트/런타임_상태.md`.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Never print, copy, or commit credentials, tokens, session values, or secret contents.
- Until security-team/team-lead approval, commit only de-identified customer context. Use `CUST-NNN`; keep customer names, contacts, Account/Payer IDs, IPs, and CIDRs in gitignored `.private/customer-map.md` only.
- Customer-facing cost figures must be FitCloud-curated. Never show or mention raw AWS billing figures.
- Read `고객/<customer>/프로필.md` before working on that customer.
- Route company policy through `회사규정/_라우팅.md`.
- Select tools through `에이전트/기능_카탈로그.md`; do not invent unavailable product-specific commands.
- Preserve history by appending dated corrections and replies; never overwrite prior judgment.
- Use `연계/README.md` for cross-project PoC work and verify returned evidence before drafting.
- Record people through identity, observed behavior, and response strategy only; never subjective judgment.

## Environment

- Run shell commands non-interactively and disable pagers. Stop on an unexpected prompt.
- Quote paths containing Korean text, spaces, or parentheses.
- Do not access `~/Documents/obsidian/`; macOS TCC blocks it. Ask the user to copy only required material to an approved location.

## Language

Write agent-facing rules and metadata in English. Write human-facing ticket content and customer reply drafts in Korean. Preserve technical identifiers and source quotations exactly.
