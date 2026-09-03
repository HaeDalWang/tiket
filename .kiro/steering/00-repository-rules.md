# Kiro Repository Entry Point

Read root `CLAUDE.md`, then route the task through `에이전트/작업_라우터.md`. Load only matched modules.

## Hard stops

- Draft only; never send customer email or post Zendesk comments.
- Customer AWS/FitCloud inspection is read-only and broker-mediated; check `에이전트/런타임_상태.md` before use.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Never expose or commit secrets. Commit only de-identified customer context; keep real mappings in `.private/customer-map.md`.
- Customer-facing cost figures must be FitCloud-curated; never mention raw AWS billing figures.

For customer work, read the profile, route policy through `회사규정/_라우팅.md`, and select capabilities through `에이전트/기능_카탈로그.md`. Use `연계/README.md` only for a routed PoC. Human-facing ticket content and drafts are Korean.