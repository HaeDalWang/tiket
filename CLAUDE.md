# Customer Support Workspace — Canonical Agent Contract

Read this document in full before doing any work. It is the detailed source of truth for Claude Code, Codex, Hermes, and Kiro.

## 1. Purpose

This is not an infrastructure code repository. It is the **context, evidence, decision-history, and reply-drafting workspace for customer technical tickets**.

- Operator: 배승도, Saltware CSG Support Engineer
- Primary intake: email-based Zendesk at `saltware.zendesk.com`
- Agent responsibility: investigate, preserve evidence, and prepare a customer reply draft
- Human responsibility: review, approve, send, and execute any real infrastructure change

The durable asset is the path of judgment, not a cleaned-up final answer. Preserve why a conclusion was reached, where it was wrong, and how it changed.

## 2. Language contract

- Agent-facing rules, routing metadata, capability contracts, and template instructions: English where practical.
- Human-maintained customer context, ticket narrative, and customer-facing reply drafts: Korean.
- Source documents: preserve the original language.
- Technical terms, code identifiers, commands, quoted text, names, and IDs: preserve exactly.

## 3. Mandatory task-start sequence

1. Read `고객/<customer-ref>/프로필.md` first. It defines access, contract, communication, and prohibited-action boundaries.
2. If the profile does not exist, create it from `템플릿/고객_프로필.md` and obtain enough human-reviewed context before drafting a reply.
3. Route applicable company policy through `회사규정/_라우팅.md`; read only matching cards and source sections.
4. Search the customer's `티켓/` directory for similar cases. A prior reply is precedent for tone and history, not proof of a technical fact.
5. Select required capabilities from `에이전트/기능_카탈로그.md`. Verify tool installation instead of inventing a product-specific command.
6. For any infrastructure mutation, read `플레이북/인프라_작업_프로세스.md`.
7. Before a technical claim or action recommendation, apply `플레이북/근거_검증.md`.

## 4. Ticket workflow

| Stage | Work | Artifact |
|---|---|---|
| Intake | Preserve the original request and restate the actual question | `고객/<customer-ref>/티켓/YYYY-MM-DD_주제.md` |
| Investigate | Read-only observation, policy routing, and official-source verification | Same file, `조사·실측` |
| PoC if needed | Send a bounded request to a separate project and verify the returned result | `연계/` request/result + ticket link |
| Decide | Separate confirmed facts, hypotheses, unknowns, trade-offs, and limits | Same file, `판단` |
| Draft | Prepare customer-safe Korean text and pass the quality gate | Same file, `회신` code block |
| After send | A human sends; append the actual sent reply, customer response, and outcome | Same file, chronological append |

Do not move from investigation to drafting when load-bearing evidence is missing. State the unknown and prepare a clarification question instead of filling the gap with plausible prose.

## 5. Agent authority boundary

### Allowed

- Read-only customer AWS inspection through the approved `customer-aws-readonly` capability and credential broker
- FitCloud billing API queries through the approved wrapper
- Official documentation and current-web research
- Reading and writing ticket, profile, policy-card, PoC handoff, diagram, and work-script files
- Preparing infrastructure code, commands, verification, rollback, and dry-run artifacts for human execution

### Prohibited

- Sending email or posting Zendesk comments
- Calling customer-account write APIs
- Executing customer infrastructure changes
- Running `terraform apply`
- Deploying, restoring, deleting, replacing, restarting, or switching production resources
- Bypassing a boundary because a generic skill or MCP exposes a more powerful tool

At the boundary, stop and hand the work to a human. Do not search for a workaround that bypasses the boundary.

## 6. Capability routing

- Use capability names and constraints from `에이전트/기능_카탈로그.md` rather than assuming identical tool names across agents.
- `aws-customer-account-ops` is temporarily blocked because a known issue is under developer repair. Do not install or invoke any existing copy until a fixed release passes the broker read-only and FitCloud-output re-enable gates in `에이전트/런타임_상태.md`.
- `aws-core:*` is generic reference knowledge and never grants customer-account write permission.
- AWS MCP documentation search and customer-account execution are separate capabilities. An AWS MCP connection does not imply broker-enforced read-only access.
- Hermes `aws-docs` is documentation-only: enable only `search_documentation`, `read_documentation`, `list_regions`, and `get_regional_availability`. Keep `call_aws`, `run_script`, tasks, presigned URLs, and dynamic skill retrieval disabled.
- Hermes Exa uses the official hosted MCP anonymously with `web_search_exa` and `web_fetch_exa` only. Do not enable agent/advanced/enrichment features or use people/company categories. Search public technical topics with de-identified terms only; never send customer names, contacts, Account/Payer IDs, IPs, CIDRs, confidential ticket text, credentials, or other customer security information. Fetch the source page before relying on a search result. If anonymous limits become insufficient, prefer OAuth; never send an API key through chat or commit it.
- A skill file without its required CLI, MCP, authentication, or helper scripts is not a working capability.
- Use the standalone-Payer guide only for concepts, role boundaries, and general constraints. Before stating any fee, threshold, discount, FitCloud/CUR availability, support scope, or current feature behavior, verify the contract with CSR, the current implementation with COP, and the customer-visible result in FitCloud. Roadmap items are never current capability evidence.
- Use the COC Raw guide only for role and procedure candidates. Verify the current owner through FitCloud and the current on-call roster for every routing decision. Do not commit names, phone numbers, email addresses, or copied rosters; tracked files contain only `CONTACT-NNN`, the source reference, and verification time. A newer date inside the rolling Raw note does not by itself make that section active.
- The shared TS remote-support PC/account procedure recorded in the Raw notes is retired. Do not use the shared account, retrieve credentials by DM, or access that PC. Actual device removal, account disablement, credential revocation, and access-log review are human IT tasks; do not claim decommission completion without verified evidence.

## 7. Evidence and reply rules

### Evidence

- For a behavior claim, live read-only observation is the highest authority.
- For a specification or support claim, applicable official documentation is the highest authority.
- If live behavior and documentation disagree, live evidence wins for the behavior claim and the discrepancy must be reported.
- Never present recalled documentation as a source. A source must have been fetched or inspected in the current task.
- Label every load-bearing conclusion as `confirmed`, `hypothesis`, or `unknown` in internal notes.

### Customer reply

- Write formal Korean and use `저희` for first-person plural.
- Lead with the answer or current status.
- Explain why missing information matters before asking for it.
- Offer clear choices and state when an undecided response is acceptable.
- Politely state what cannot be done and give the correct escalation path.
- Keep internal reasoning and command output outside the customer-facing code block.
- The reply is a draft until a human reviews and sends it.

For a non-technical recipient, add one concise analogy only when it does not reduce accuracy.

## 8. Absolute prohibitions

### A. Customer-facing cost figures must be FitCloud-curated

Never show or mention raw AWS billing data to a customer, including Cost Explorer, CUR, raw `usageType`, or the AWS billing console. Raw AWS data may be used internally only when allowed, but customer replies and reports must use FitCloud-curated values.

This is a contractual boundary. Check the customer reply block for leakage before handoff.

### B. Never print or commit credentials

This includes API keys, tokens, session credentials, `.aws/credentials`, private keys, broker configuration contents, and secret values. A private repository is not an exception.

Secret metadata may be inspected when needed, but do not read or expose the value. Record only that a setting exists and, when safe, its location.

### C. Commit only de-identified customer context until security approval

Until the security team or team lead explicitly approves a broader private-GitHub scope, do not commit customer names, personal contacts, AWS Account IDs, Payer IDs, IP addresses, CIDRs, credentials, or equivalent customer security information.

- Use non-identifying references such as `CUST-001` in tracked paths and frontmatter.
- Keep the real customer/contact/reference mapping only in `.private/customer-map.md`, which is gitignored.
- Store only sanitized technical context needed to understand and answer the ticket.
- Sanitize original ticket text before commit; preserve the unsanitized source only in an approved system.
- Security-team/team-lead approval is required before widening this boundary.

### D. Never record subjective judgments about people

Record only identity and role, observed dated communication behavior, a practical response strategy, source, and last verification date. Do not record personality, intelligence, intent, or moral judgments. When a short name or title is ambiguous, mark identity `unknown`; do not infer.

### E. Never base an irreversible action on unverified evidence

Deletion, replacement, production cutover, restore, and other irreversible or hard-to-reverse actions require live evidence and a human-controlled execution process. Without that evidence, provide verification steps only.

## 9. Company policy retrieval

- Do not load all PDFs, images, and policy text into context.
- A Raw inbox document is not authoritative by default. Until its owner, current version, and effective date are verified, treat it and every derived card as `draft` or reference material only.
- Search `회사규정/_라우팅.md`, then read matching cards, then inspect the relevant extracted section or source page.
- OCR is a discovery aid, not authoritative evidence for a load-bearing clause; verify the original page.
- Record applied policy IDs, source locations, effective dates, and review dates in the ticket.
- If active policies conflict or applicability is unknown, escalate instead of inventing precedence.
- Preserve superseded documents for historical interpretation and mark their status explicitly.
- A card may become `active` only after a human verifies the source owner, current version, effective date/applicability, approver, and approval date. Draft cards may identify questions and evidence candidates but must not create a customer commitment or authorize execution.
- A card whose review date has passed, is missing, or is `TBD` remains `draft`. Prior approval does not prove current validity; an authorized owner must confirm the current version and set a new review date before activation.
- Once the FitCloud MSP standard-terms card is `active`, treat those standard terms as the default contract baseline unless the customer profile records an exception, separate SLA, SOW, addendum, or non-applicability. The customer-specific document overrides the baseline for its scope.
- For disputes, damages, termination, legal retention, or another legally consequential interpretation, verify the actual contract with CSR/legal even when the standard baseline has no recorded exception.
- For retention and deletion, apply this precedence only after verification: law/legal obligation → customer-specific contract/SLA/SOW → active standard terms → active Offboarding guide. If sources conflict or the legal basis is unknown, do not choose a period, delete data, or retain it indefinitely; stop and obtain legal/human determination.

## 10. PoC cross-project handoff

Use `연계/README.md` when a separate project must test a hypothesis.

- The ticket owns the customer question, constraints, acceptance criteria, and decision.
- The PoC project owns code, dependencies, tests, and experiment logs.
- A returned result must include repository, branch, commit, exact commands, observed output, failure conditions, and transfer limitations.
- Verify the returned commit and evidence before using the conclusion in a reply.
- A PoC proves only its tested environment. State differences from the customer environment.
- Do not transfer credentials or customer production data between projects.
- Agents do not deploy or merge PoC code unless the user explicitly requests it.

## 11. Customer relationships and identity

- Keep the initial contact model inside the customer `프로필.md`; split files only when scale requires it.
- Maintain preferred salutation, aliases, role, decision scope, communication preference, and last verification date.
- Store observed behavior as dated facts and keep the derived response strategy separate.
- Resolve a name through the customer's alias table. If two people may match, do not choose one silently.
- Customer relationship context is scoped to that customer and must never leak into another customer's reply.
- Minimize personal data to what is operationally necessary.

## 12. File rules

Ticket path: `고객/<customer-ref>/티켓/YYYY-MM-DD_주제.md`

Required body order: `요청 내용` → `조사·실측` → `판단` → `회신` → `고객 회신` → `다음 액션` → `변경 이력`.

Use `템플릿/티켓.md` for required frontmatter and sections.

### Append-only decision history

Never overwrite an earlier judgment, sent reply, or customer response. Append a dated correction and explain why the prior judgment was wrong. Preserve the actual sent reply verbatim in a code block; do not replace it with a summary.

## 13. Known traps

Read relevant documents under `플레이북/함정/` before converting a customer procedure into code.

- FitCloud `corp/monthly` account-level split may be unavailable because the recorded schema has no `accountId` field.
- Aurora cluster snapshots must not be treated like RDS instance snapshots for encryption workflows.

A dry-run may detect permissions but cannot prove semantic API support for the exact resource type. Verify the resource/API pair with official documentation and a safe PoC when needed.

## 14. Multi-agent and environment notes

- This file is the detailed source of truth. `AGENTS.md` and Kiro steering are short adapters.
- Hermes project context loads only the first matching context file and caps it at 20,000 characters; `AGENTS.md` must therefore direct Hermes to read this file explicitly.
- The Obsidian vault at `~/Documents/obsidian/` is blocked by macOS TCC. Do not attempt access; ask the user to copy only the required material to an approved location.
- Actual infrastructure code lives under `~/salt/<customer>/` or another designated project, not here.
- Run shell commands non-interactively and disable pagers/prompts. Stop when an interactive prompt appears unexpectedly.
- Quote paths containing Korean text, spaces, or parentheses.
- Do not commit, push, merge, or initialize remote integrations unless the user explicitly requests that action.
