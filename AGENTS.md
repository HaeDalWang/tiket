# Agent Entry Point

Before work, read the root `CLAUDE.md`, then classify the task through `agents/task-router.md`. Load only the routed modules.

## Hard stops

- Draft customer replies only; never send email or post Zendesk comments.
- Customer AWS/FitCloud inspection is read-only and broker-mediated; check `agents/runtime-status.md` before use.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Never expose or commit secrets. Commit only de-identified customer context; keep real mappings in gitignored `.private/customer-map.md`.
- Customer-facing cost figures must be FitCloud-curated; never mention raw AWS billing figures.

For customer work, read the target profile, route policy through `policy/_routing.md`, and select tools through `agents/capability-catalog.md`. Use `handoff/README.md` only when a PoC is required. Human-facing ticket content and reply drafts are Korean; agent rules and metadata are English where practical.