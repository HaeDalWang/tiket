# Kiro Repository Entry Point

Read root `CLAUDE.md`, then route the task through `agents/task-router.md`. Load only matched modules.

## Hard stops

- Draft only; never send customer email or post Zendesk comments.
- Customer AWS/FitCloud inspection is read-only and broker-mediated; check `agents/runtime-status.md` before use.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Never expose or commit secrets. Commit only de-identified customer context; keep real mappings in `.private/customer-map.md`.
- Customer-facing cost figures must be FitCloud-curated; never mention raw AWS billing figures.

For customer work, read the profile, route policy through `policy/_routing.md`, and select capabilities through `agents/capability-catalog.md`. Use `handoff/README.md` only for a routed PoC. Human-facing ticket content and drafts are Korean.