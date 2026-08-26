# Agent Entry Point

Before work, read the root `CLAUDE.md`, then classify the task through `에이전트/작업_라우터.md`. Load only the routed modules.

## Hard stops

- Draft customer replies only; never send email or post Zendesk comments.
- Customer AWS/FitCloud inspection is blocked while `aws-customer-account-ops` is under repair; follow `에이전트/런타임_상태.md`.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Never expose or commit secrets. Commit only de-identified customer context; keep real mappings in gitignored `.private/customer-map.md`.
- Customer-facing cost figures must be FitCloud-curated; never mention raw AWS billing figures.

For customer work, read the target profile, route policy through `회사규정/_라우팅.md`, and select tools through `에이전트/기능_카탈로그.md`. Use `연계/README.md` only when a PoC is required. Human-facing ticket content and reply drafts are Korean; agent rules and metadata are English where practical.