# Agent Installation and Capability Verification

Use this procedure to verify local installation state. Never print live credential values.

## Installation path contract

| Agent | User skill path |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Hermes | `~/.hermes/skills/` or the active `$HERMES_HOME/skills/` |
| Codex | `~/.agents/skills/` |
| Kiro | `~/.kiro/skills/` |

`aws-customer-account-ops` v1.7.2 is enabled. Run the offline conformance test below after any install or upgrade, and read the current status in `agents/runtime-status.md` before customer work.

Each agent keeps its own copy so it can load `SKILL.md`, but the `csg-login` marker in the single machine-wide `~/.aws/config` decides which copy actually **executes**. One `SKILL_DIR` per machine is structural. `self-update.sh` updates every installed copy in one run; run this drift check after any update that reports a failed agent:

```bash
marker=$(dirname "$(aws configure get profile.csg-login.credential_process 2>/dev/null)")
echo "executes: ${marker:-UNRESOLVED}"
for d in ~/.claude ~/.hermes ~/.agents ~/.kiro ~/.config/opencode ~/.cursor ~/.codeium/windsurf ~/.augment ~/.gemini; do
  p="$d/skills/aws-customer-account-ops"
  [ -d "$p" ] || continue
  printf '%s  %s\n' \
    "$(cat "$p"/get-customer-credentials.sh "$p"/get-sts-token.sh "$p"/fitcloud-api.sh 2>/dev/null | shasum -a 256 | cut -c1-16)" "$p"
done
```

Every listed hash must match, and the marker must resolve into one of the listed directories. A hash that differs from the rest, or a marker resolving outside them, means a stale copy is executing — re-run `self-update.sh` before customer work.

## Safe presence check

```bash
test -f ~/.claude/skills/aws-customer-account-ops/SKILL.md && echo "Claude: installed"
test -f ~/.hermes/skills/aws-customer-account-ops/SKILL.md && echo "Hermes: installed"
test -f ~/.agents/skills/aws-customer-account-ops/SKILL.md && echo "Codex: installed"
test -f ~/.kiro/skills/aws-customer-account-ops/SKILL.md && echo "Kiro: installed"
```

When a Hermes profile is active, resolve its real `$HERMES_HOME` instead of assuming `~/.hermes`.

## `customer-aws-readonly` readiness

Run this readiness check before customer-account work, and again after any skill install or upgrade.

Check the following without exposing values:

1. `bash`, `aws`, `jq`, `python3`, and `curl` are executable.
2. The `bash` resolved from the agent process's `PATH` is Bash 4.3 or newer. That is the syntax floor the skill's shell client actually uses (`local -n` namerefs, `${var,,}`, `;;&`). A separately installed Bash 4.3+ that is not selected by `#!/usr/bin/env bash` does not satisfy it. On macOS, `/bin/bash` 3.2 cannot run the client; configure the agent's `PATH` to select the Homebrew Bash before launching the agent.

   This is a limitation of the externally owned skill, not of this repository. `scripts/test_aws_customer_skill.py` reports it as a warning and exits 0 while marking the customer-account capability unusable in that environment. Ask the skill owner (정지우) for a portability fix rather than working around it per machine.
3. The `csg-login` marker profile exists.
4. Its script path is inside an approved agent skill directory.
5. Check only whether the broker config file exists.
6. Check only whether the FitCloud API key is configured.
7. Run the STS `--check-only` path before any customer AWS request.
8. If expired, perform Slack authentication only with the user's awareness.

Verify the selected Bash without executing the skill. Note that `(( ... ))` arithmetic
must not compare a two-part version as a single number:

```bash
command -v bash
bash -c '(( BASH_VERSINFO[0] > 4 || (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] >= 3) ))' \
  && echo "Bash requirement: pass" \
  || echo "Bash requirement: warn (skill unusable here)"
```

Run this check from the same environment that launches the agent. An interactive terminal and a GUI-launched agent can resolve different `PATH` values.

### Offline skill conformance

After installing the skill, run the repository-owned synthetic test from the workspace root:

```bash
python3 scripts/test_aws_customer_skill.py
```

Use `--skill-dir <path>` when more than one agent copy is installed and a specific copy must be tested. The test uses temporary homes, synthetic tokens, stubbed `curl`, and a stubbed `aws`; it must not contact Slack, FitCloud, the credential broker, or a customer account. It verifies:

- Bash 4.3+ selection and shell syntax
- fail-fast behavior without a login token
- fail-closed behavior without a FitCloud API key
- synthetic FitCloud Bearer forwarding
- the broker `/customer-credentials` path and request scope
- exact five-key `credential_process` output projection
- absence of a local `aws sts assume-role` execution path

A passing offline test is necessary but not sufficient. Broker-side read-only enforcement and the zero-guidance synthetic ticket smoke test are separate gates; see the evidence provenance section of `agents/runtime-status.md` for which of them currently have a recorded artifact.

Read the final line, not just the exit code:

| Final line | Meaning |
|---|---|
| `PASS` | The installed skill copy conforms and the environment can run it. |
| `PASS WITH WARNINGS` | The repository side is fine, but this environment's bash cannot run the skill. Treat `customer-aws-readonly` and `fitcloud-billing` as `blocked` and DM the skill owner. |
| `FAIL` | A local install problem: missing files, wrong skill directory, or a conformance violation. Fix it before customer work. |

Never print:

- `credential_process` output
- API key values
- access key, secret key, or session token
- broker config contents

## Project-scoped MCP readiness

MCP capability ships with the repository. `agents/environment/mcp-manifest.json` is the
only declaration; `.kiro/settings/mcp.json`, `.mcp.json`, `.claude/settings.json`, and
`.codex/config.toml` are generated from it. Hermes keeps its configuration in its own
profile and must be aligned to the same manifest by hand.

```bash
brew install uv                                  # prerequisite for the AWS proxy
python3 scripts/render_agent_configs.py --check   # host configs match the manifest
python3 scripts/verify_mcp_servers.py             # servers reachable and correctly bounded
```

`verify_mcp_servers.py` exits 0 on PASS, 1 when a boundary is violated or a routed tool is
missing, and 2 when the check could not run because `uv` is absent or the endpoint is
unreachable. A transient network failure is not a configuration error; retry before
concluding. The check redirects AWS configuration to a nonexistent path so it can never
invoke the customer credential broker.

Never edit a generated host file directly. The validator rejects drift and prints the
render command. Personal MCP servers belong in user-level configuration
(`~/.kiro/settings/mcp.json` and equivalents), never in the project files.

## `aws-official-research` readiness

- Server: pinned `mcp-proxy-for-aws@1.6.4` against the managed AWS MCP endpoint, from `aws/agent-toolkit-for-aws`.
- Required enabled tools: `aws___search_documentation`, `aws___read_documentation`, `aws___list_regions`, `aws___get_regional_availability`.
- Required disabled tools: `aws___call_aws`, `aws___run_script`, `aws___get_presigned_url`, `aws___get_tasks`, `aws___retrieve_skill`.
- Two enforcement layers, because neither is sufficient alone:
  - `--read-only` on the proxy drops every tool not annotated `readOnlyHint=true`. Observed 2026-09-03: 9 tools without the flag, 6 with it; `call_aws`, `run_script`, and `get_presigned_url` are the three dropped.
  - Host configuration denies the remaining unrouted tools. Codex expresses an exact allow list; Kiro and Claude Code express deny lists, so the proxy flag is what protects against a newly added upstream write tool.
- `--skip-auth` and no AWS credential. Documentation access never grants customer-account execution.
- Do not enable the toolkit's full tool catalog or its generic skill packs to satisfy this capability. Generic AWS knowledge does not expand repository authority, and a larger catalog increases selection noise.

## `current-web-research` readiness

- Server: official hosted Exa MCP at `https://mcp.exa.ai/mcp` in anonymous rate-limited mode. Observed 2026-09-03: `exa-search-server 3.2.1` exposing exactly 2 tools.
- Required enabled tools: `web_search_exa`, `web_fetch_exa`.
- Keep `agent_run`, advanced search, people/company categories, enrichment, and personal-profile lookup unavailable for this workflow.
- Do not send customer names, contacts, Account/Payer IDs, IPs, CIDRs, confidential ticket text, credentials, or other customer security information to Exa.
- Do not treat search highlights as sufficient support for a load-bearing claim; fetch and inspect the source page.
- Anonymous mode needs no API key. If rate limits become insufficient, prefer OAuth and never send an API key through chat.

## Smoke test

Use synthetic, non-customer data when onboarding an agent.

1. It reads repository rules and explains the no-send boundary.
2. It selects a capability from `agents/capability-catalog.md`.
3. It does not invent an unavailable tool name.
4. It rejects an AWS write request and identifies the read-only path.
5. It applies the FitCloud-only rule to a customer cost question.
6. It records evidence and certainty for a technical answer.
7. It routes a PoC through the `handoff/` handoff.

Do not use the agent as the sole investigator for a customer ticket until all checks pass.
