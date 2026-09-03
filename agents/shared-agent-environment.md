# Shared Agent Environment

`as_of: 2026-08-31 KST`

This document defines the proposed distribution boundary for project-scoped Skills, MCP capabilities, and Hooks across Hermes, Claude Code, Codex, and Kiro. It records an assessment and rollout gate; it does not authorize credentials, customer-account access, or automatic customer communication.

## Locked operating direction

- Teammate workspaces follow `upstream/main`.
- Operational backlog creation is deferred while real ticket samples accumulate.
- `playbooks/pitfalls/` is shared curated knowledge whose entries act as routing warnings and always require ticket-specific re-verification; they are not standalone proof.
- The next environment priority is consistent project-scoped capability, not identical personal agent installations.
- Hook adoption requires measured benefit or a deterministic safety requirement.

## Observed baseline

- The repository has no project-scoped Skill directory for any supported agent.
- The repository has no committed MCP manifest or product-specific MCP adapter.
- The repository has no Hook configuration or shared Hook implementation.
- The current Hermes profile has 95 enabled Skills, mixing personal, bundled, and support-related capabilities.
- The current Hermes profile has no configured Hook.
- The current Hermes profile exposes only six selected MCP tools: four AWS documentation tools and two Exa research tools.
- The root entrypoints are already bounded: the validator caps `CLAUDE.md`, `AGENTS.md`, and Kiro steering and enforces selective routing. Kiro also supports conditional steering inclusion when specialized guidance should not load on every interaction.[13]

The present state gives agents consistent rules but does not reproduce actual capability after clone.

## Portability boundary

All four target agents support the open Agent Skills format and progressive disclosure.[2][6]
Their automatic project directories differ: Hermes and Codex can discover repository Skills under `.agents/skills/`, while Claude Code uses `.claude/skills/` and Kiro uses `.kiro/skills/`.[9][14]

Use this layout:

```text
.agents/skills/                 canonical project Skill source
.claude/skills/                 generated Claude Code copies
.kiro/skills/                   generated Kiro copies
agents/환경/mcp-manifest.yaml  secret-free capability manifest
scripts/agent-environment/      render, install, verify, and Hook scripts
.claude/settings.json           Claude Hook adapter
.codex/hooks.json               Codex Hook adapter
.kiro/hooks/                    Kiro Hook adapters
```

Do not maintain three independent Skill implementations. A deterministic sync script must copy the canonical Skill into product directories and the workspace validator must reject drift. Copies are preferred over Git symlinks so clones remain portable across operating systems and Git configurations.

Hermes project Skill discovery requires explicit repository trust. Onboarding must run `hermes skills trust` for the workspace rather than silently modifying global trust state.

## Do not duplicate the ticket workflow as a Skill

Do not add a `tiket-ticket-workflow` Skill. The workflow is already divided across repository contracts:

- `agents/task-router.md` classifies the task and controls selective loading.
- `playbooks/evidence-verification.md` implements the portable `answer-quality-gate` capability.
- Claude Code maps that capability to its existing `seonbi` Skill.
- Hermes, Codex, and Kiro apply the same repository playbook directly.
- Decision Packet v2 and Reply Brief v2 normalize semantics before prose.

This is an intentional capability mapping, not a missing shared Skill. A host-specific Skill name does not need to be identical when the repository capability contract and output semantics are the same. Add a new Skill only when repeated samples reveal a procedure that is not already supplied by the router, playbooks, templates, or an existing approved Skill.

## MCP distribution

MCP is the shared external-capability boundary, but configuration syntax and trust are host-specific. Claude Code supports project-scoped `.mcp.json`; Codex supports project-scoped `.codex/config.toml`; Kiro supports workspace MCP configuration; Hermes stores native MCP configuration in its profile.[10][12][15]

Maintain one secret-free manifest that explicitly declares:

- capability ID and server name
- pinned package version or remote URL
- allowed transport
- exact include-only tool list
- required environment-variable names, never values
- read/write classification
- authentication mode
- smoke test
- blocked or unavailable state

Generate or install host adapters from that manifest. Never commit OAuth tokens, API keys, headers containing credentials, or local callback state.

The existing six-tool include-only MCP boundary is good. Do not add an entire server tool catalog when a routed capability needs only a small subset. Larger or poorly described MCP tool catalogs increase selection noise; Kiro explicitly warns that very large tool descriptions can affect agent performance.[15]

## Hook portability

Hermes and Claude Code expose lifecycle Hooks, including command-based interception around tool use or turn completion.[1][5]
Codex and Kiro expose comparable lifecycle events, but all four hosts differ in event payloads, matcher names, trust mechanisms, and configuration locations.[7][11]

Therefore:

- Put deterministic logic in shared scripts under `scripts/agent-environment/hooks/`.
- Keep product-specific files as thin event and payload adapters.
- Never encode business policy separately in four Hook configurations.
- Never log prompts, customer text, tool inputs, tool outputs, identifiers, credentials, or source documents.
- Treat Hook trust as local human state; a cloned repository must not grant itself execution trust.

## Performance and token assessment

Hooks do not inherently reduce token cost. They help only when deterministic work replaces an avoidable model/tool loop, prevents a known failure, or keeps irrelevant context out of the prompt. Hooks also add process latency, and prompt- or agent-based Hooks can add another model call.[5][7][11]

| Candidate | Expected effect | Decision |
|---|---|---|
| Silent final validator; return output only on failure | May prevent a failed completion and one correction turn | Pilot after baseline |
| Pre-tool guard for prohibited sends, customer-account writes, and `terraform apply` | Strong deterministic safety; may avoid correction loops | Design after common script contract |
| Run full validator after every file edit | Repeated process cost and noisy feedback | Reject |
| Inject router or policy text on every prompt | Repeats input tokens and may reduce prompt-cache stability | Reject |
| LLM/prompt Hook for routine classification | Adds model cost and is not portable because Codex currently executes command handlers only | Reject |
| Metadata-only Stop Hook for measurements | Provides evidence without model-visible content | Pilot candidate |

For Hermes specifically, Skills are already progressively disclosed, while their metadata index is part of the stable prompt. Official documentation describes the default Skill index as roughly 3,000 tokens and advises cache-stable prompt construction.[2][3][4] The current 94-Skill personal catalog is therefore a more credible immediate token target than adding a Hook.

A dedicated `tiket` Hermes profile should eventually load only the project core pack and genuinely required support Skills. This must not delete or alter the user's personal default profile. Claude Code and Codex also disclose Skill metadata before loading full Skill bodies, so concise descriptions and a small project pack matter across hosts.[6][8][9]

## Measurement gate

Preserve zero-guidance testing. Use the same de-identified raw ticket intake and no steering prompt for baseline and candidate runs.

Record only numeric or categorical metadata:

- host and model
- input, cached-input, and output tokens when exposed
- wall-clock duration
- model-call and tool-call counts
- files and modules loaded by count, not customer-bearing path text
- validator result and correction-turn count
- safety violation attempts
- human review outcome

Do not record prompt bodies, customer content, model output, tool payloads, or credentials in Hook telemetry.

Do not claim savings from one successful run. Promote a Hook only after repeated paired samples show one of:

- fewer correction turns
- fewer irrelevant file/tool loads
- lower uncached input tokens
- lower total token use without quality regression
- a deterministic safety block that justifies neutral or higher cost

## Recommended rollout order

1. Record the existing capability-to-host mapping in a secret-free environment manifest.
2. Add deterministic cross-host presence and readiness verification; verify `seonbi` for Claude Code and the repository playbook path for the other hosts.
3. Add the MCP contract to the same manifest and compare it to actual host configuration.
4. Accumulate zero-guidance baseline samples with no Hook and no new ticket workflow Skill.
5. Promote a new shared Skill only after samples show a repeated procedural gap.
6. Pilot one silent, metadata-only measurement Hook.
7. Pilot final validation only if baseline runs commonly omit or fail validation.
8. Add pre-tool safety guards only after payload adapters are tested on every supported host.

Do not deploy several Hooks together; that would prevent attribution of any performance or cost change.

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
[3] https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
[4] https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
[5] https://code.claude.com/docs/en/hooks
[6] https://code.claude.com/docs/en/skills
[7] https://developers.openai.com/codex/hooks
[8] https://developers.openai.com/codex/concepts/customization
[9] https://developers.openai.com/codex/skills
[10] https://developers.openai.com/codex/mcp
[11] https://kiro.dev/docs/hooks
[12] https://kiro.dev/docs/how-kiro-works
[13] https://kiro.dev/docs/steering
[14] https://kiro.dev/docs/skills
[15] https://kiro.dev/docs/mcp
