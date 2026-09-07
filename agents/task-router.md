# Task Router

Classify first, then load only the listed modules. Never load every policy, playbook, ticket, or skill by default.

## Universal

- Customer ticket: record work in `tickets/<ticket-id>.md`. Read `customers/<customer-ref>/profile.md` when one exists; a profile is created only when contract, billing, or access scope is in question.
- Policy: search `policy/_routing.md`; read only matching cards. A `draft` card cannot create a commitment or authorize action.
- Capability: select through `agents/capability-catalog.md`; verify runtime state before use.
- Use official/current evidence for load-bearing claims. Prior replies are history, not proof.
- Reuse confirmed evidence already recorded in the same ticket when claim, target, and source remain applicable and no conflict exists. Re-fetch only for a new claim, missing support, conflict, changed target/version, or explicit freshness requirement.
- Record the ticket in `tickets/<ticket-id>.md` from `templates/ticket-intake.md`. Decide the output first (`playbooks/ticket-outputs.md`), grade every claim `[확인]`/`[추측]`/`[모름]` with a source on each `[확인]`, and pass `## 발송 전 점검` before the draft goes out.

## Route

| Tier | Trigger | Load |
|---|---|---|
| `quick` | General specification or documentation lookup; no live customer state, exact cost, contract, security decision, or mutation | Customer core profile when applicable; capability catalog; official source. Apply the compact checks in `playbooks/evidence-verification.md` sections 0, 2, 4, and 7. |
| `standard` | Customer configuration, troubleshooting, recommendation, or cost optimization without a customer-facing figure | `quick` inputs plus matching policy cards, similar tickets, and the full `playbooks/evidence-verification.md`. |
| `high-risk` | Credentials/PII sharing, exact cost or contract claim, incident, production change, or irreversible action | `standard` inputs plus the relevant specialized playbook. For changes use `playbooks/infra-change-process.md`; for PoC use `handoff/README.md`. Stop at the human approval boundary. |

## Output modules

- Ticket outputs (decide this first): `playbooks/ticket-outputs.md`
- Reply drafting: `playbooks/reply-writing-rules.md`
- Reply presentation profiles: `playbooks/reply-style.md`
- Ticket record and pre-send gate: `templates/ticket-intake.md`
- Customer/profile fields: `templates/customer-profile.md`
- Multi-agent handoff: `agents/compatibility.md`
- Known traps: search `playbooks/pitfalls/`

Load a local skill only when its trigger directly matches the task and it adds procedure not already supplied by these repository modules. Do not load a broad or merely adjacent skill.
