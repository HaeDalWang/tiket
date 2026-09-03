#!/usr/bin/env python3
"""Render project-scoped MCP configuration for every supported host from one manifest.

The manifest at agents/environment/mcp-manifest.json is the only place a capability
is declared. Host files are generated so that Kiro, Claude Code, and Codex cannot
drift apart, and so the validator can prove they match.

Usage:
    python3 scripts/render_agent_configs.py            # write host files
    python3 scripts/render_agent_configs.py --check    # verify without writing
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "agents/environment/mcp-manifest.json"

GENERATED_NOTE = (
    "Generated from agents/environment/mcp-manifest.json by "
    "scripts/render_agent_configs.py. Do not edit by hand."
)
# JSON has no comment syntax and host schemas may reject unknown top-level keys, so
# the generated marker only appears in the TOML output. Drift is caught by
# scripts/validate_workspace.py instead of by an in-file marker.


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def server_by_id(manifest: dict) -> dict[str, dict]:
    return {server["id"]: server for server in manifest["servers"]}


def render_kiro(manifest: dict) -> str:
    servers: dict[str, dict] = {}
    for server in manifest["servers"]:
        entry: dict[str, object] = {}
        if server["transport"] == "stdio":
            entry["command"] = server["command"]
            entry["args"] = list(server["args"])
        else:
            entry["url"] = server["url"]
        entry["disabled"] = False
        entry["autoApprove"] = list(server["allowed_tools"])
        if server["blocked_tools"]:
            entry["disabledTools"] = list(server["blocked_tools"])
        servers[server["id"]] = entry
    payload = {"mcpServers": servers}
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_claude_mcp(manifest: dict) -> str:
    servers: dict[str, dict] = {}
    for server in manifest["servers"]:
        if server["transport"] == "stdio":
            entry: dict[str, object] = {
                "type": "stdio",
                "command": server["command"],
                "args": list(server["args"]),
            }
        else:
            entry = {"type": "http", "url": server["url"]}
        servers[server["id"]] = entry
    payload = {"mcpServers": servers}
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_claude_settings(manifest: dict) -> str:
    deny: list[str] = []
    for server in manifest["servers"]:
        for tool in server["blocked_tools"]:
            deny.append(f"mcp__{server['id']}__{tool}")
    payload = {
        "enableAllProjectMcpServers": True,
        "enabledMcpjsonServers": [server["id"] for server in manifest["servers"]],
        "permissions": {"deny": deny},
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def toml_array(values: list[str]) -> str:
    return "[" + ", ".join(toml_string(value) for value in values) + "]"


def render_codex(manifest: dict) -> str:
    lines = [f"# {GENERATED_NOTE}", ""]
    for server in manifest["servers"]:
        lines.append(f"[mcp_servers.{server['id']}]")
        if server["transport"] == "stdio":
            lines.append(f"command = {toml_string(server['command'])}")
            lines.append(f"args = {toml_array(list(server['args']))}")
        else:
            lines.append(f"url = {toml_string(server['url'])}")
        lines.append(f"enabled_tools = {toml_array(list(server['allowed_tools']))}")
        if server["blocked_tools"]:
            lines.append(f"disabled_tools = {toml_array(list(server['blocked_tools']))}")
        lines.append("enabled = true")
        lines.append('default_tools_approval_mode = "auto"')
        lines.append("")
    return "\n".join(lines)


RENDERERS = {
    ".kiro/settings/mcp.json": render_kiro,
    ".mcp.json": render_claude_mcp,
    ".claude/settings.json": render_claude_settings,
    ".codex/config.toml": render_codex,
}


def rendered_files(manifest: dict) -> dict[str, str]:
    return {relative: render(manifest) for relative, render in RENDERERS.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()

    try:
        manifest = load_manifest()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"agent config render: FAIL ({exc})", file=sys.stderr)
        return 1

    expected = rendered_files(manifest)
    if args.check:
        drifted = []
        for relative, content in expected.items():
            path = ROOT / relative
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drifted.append(relative)
        if drifted:
            print("agent config render: FAIL (drift)", file=sys.stderr)
            for relative in drifted:
                print(f"- out of date: {relative}", file=sys.stderr)
            print(
                "- run: python3 scripts/render_agent_configs.py",
                file=sys.stderr,
            )
            return 1
        print(f"agent config render: PASS ({len(expected)} host files match the manifest)")
        return 0

    for relative, content in expected.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"agent config render: wrote {len(expected)} host files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
