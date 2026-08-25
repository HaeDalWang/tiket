# Kiro Repository Rules

Before doing any work in this repository, read the root `CLAUDE.md` in full and follow it. Do not duplicate the detailed rules here.

## Non-negotiable boundaries

- Never send customer email or post Zendesk comments. Produce drafts only.
- Customer AWS/FitCloud access is currently blocked while `aws-customer-account-ops` is under developer repair. Do not invoke an existing copy; follow `에이전트/런타임_상태.md`.
- Never modify customer infrastructure, call customer-account write APIs, or run `terraform apply`.
- Never print, copy, or commit credentials, tokens, or session values.
- Until security-team/team-lead approval, commit only de-identified customer context. Use `CUST-NNN`; keep customer names, contacts, Account/Payer IDs, IPs, and CIDRs in gitignored `.private/customer-map.md` only.
- Customer-facing cost figures must come only from FitCloud-curated data. Do not mention raw AWS billing figures.
- Read `고객/<customer-ref>/프로필.md` before working on that customer's ticket.
- Preserve ticket history. Append dated corrections and replies instead of overwriting prior judgment.
- Route company policy through `회사규정/_라우팅.md` and record the applied evidence.
- Select tools by shared capability in `에이전트/기능_카탈로그.md`, not by guessed product-specific names.
- When a PoC is required, follow the request/result handoff contract in `연계/README.md`.

Write agent instructions and metadata in English. Write human-facing ticket content and customer replies in Korean while preserving original technical terms and identifiers.
