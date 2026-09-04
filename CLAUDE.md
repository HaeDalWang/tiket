# Customer Support Workspace — Always-On Contract

This repository stores de-identified customer-ticket context, evidence, decisions, and reply drafts. It is not the infrastructure repository. Agents investigate and draft; humans review, send, approve, and execute.

## Absolute boundaries

- Draft only. Never send email, post Zendesk comments, or represent a draft as sent.
- Never call customer-account write APIs, change infrastructure, or run `terraform apply`.
- Customer-account access is read-only and broker-mediated only; confirm capability status in `agents/runtime-status.md` first.
- Never print or commit credentials, tokens, session values, private keys, or secret contents.
- Commit only de-identified customer context until security-team/team-lead approval. Use `CUST-NNN`, `CONTACT-NNN`, and `ACCOUNT-NNN`; keep real mappings only in gitignored `.private/customer-map.md`.
- Customer-facing cost figures must be FitCloud-curated. Never expose or mention raw AWS billing figures.
- Generic skills and MCP tools never expand repository authority. AWS documentation access is not customer-account access.
- Exa queries must contain public, de-identified technical terms only; never send customer-identifying, confidential, account, network, or credential data.
- Do not commit, push, merge, or initialize remote integrations unless the user explicitly requests it.

## Start and route

1. Read `agents/task-router.md` and classify the task as `quick`, `standard`, or `high-risk`.
2. For a customer ticket, record work in `tickets/<ticket-id>.md` from `templates/ticket-intake.md`. `tickets/` is local-only and holds real customer content. Read `customers/<customer-ref>/profile.md` when one exists; create a profile only when contract, billing, or access scope is actually in question, not as a precondition for answering.
3. Search `policy/_routing.md` and load only matching cards. A `draft` card cannot create a commitment or authorize action.
4. Select capabilities through `agents/capability-catalog.md`; verify runtime readiness instead of inventing commands.
5. Load only the router-selected evidence, reply, change, PoC, or trap modules. Load a skill only when its direct trigger matches and repository modules do not already provide the procedure.

## Evidence and records

- Fetch current official evidence for load-bearing technical claims; recalled documentation and prior replies are not proof.
- Separate `confirmed`, `hypothesis`, and `unknown`. Missing load-bearing evidence blocks a definitive reply.
- Preserve ticket history by appending dated corrections, actual sent replies, and customer responses; never overwrite prior judgment.
- Keep internal reasoning, raw tool output, secrets, prohibited billing data, and private mappings outside the customer-facing reply block.
- Record people only by operational identity/role, dated observed behavior, and response strategy; never subjective judgment.
- For PoC work use `handoff/README.md` and verify returned repository, commit, commands, output, and limitations before relying on it.

## Language and environment

- Agent rules and metadata: English where practical. Human-facing ticket content and reply drafts: Korean. Preserve source quotations and technical identifiers exactly.
- Actual Terraform and implementation code lives under `~/salt/<customer>/` or another designated project.
- Run shell commands non-interactively, stop on unexpected prompts, and quote paths containing Korean text, spaces, or parentheses.
- Do not access `~/Documents/obsidian/`; ask the user to copy only required material to an approved location.