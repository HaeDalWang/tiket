#!/usr/bin/env python3
"""Regression tests for the workspace validator's Alpha safety gates."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkspaceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="tiket-validator-test-")
        self.repo = Path(self.tempdir.name) / "repo"
        shutil.copytree(
            ROOT,
            self.repo,
            ignore=shutil.ignore_patterns(".git", ".private", "__pycache__", ".venv"),
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/validate_workspace.py", *args],
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
        )

    def replace_once(self, relative: str, old: str, new: str) -> None:
        path = self.repo / relative
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def assert_rejected(self, result: subprocess.CompletedProcess[str], marker: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(marker, result.stdout)

    def git(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            check=False,
            capture_output=True,
            text=True,
        )

    def init_git(self, activate_hooks: bool = True) -> None:
        """Give the fixture a real repository so the Git-dependent gates run."""
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@invalid")
        self.git("config", "user.name", "test")
        if activate_hooks:
            self.git("config", "core.hooksPath", ".githooks")

    def test_non_ascii_repository_path_is_rejected(self) -> None:
        (self.repo / "templates/한글파일.md").write_text("x\n", encoding="utf-8")
        self.assert_rejected(
            self.run_validator(),
            "non-ASCII repository path",
        )

    def read_manifest(self) -> dict:
        return json.loads(
            (self.repo / "agents/environment/mcp-manifest.json").read_text(encoding="utf-8")
        )

    def write_manifest(self, manifest: dict) -> None:
        (self.repo / "agents/environment/mcp-manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    def test_mcp_host_config_drift_is_rejected(self) -> None:
        self.replace_once(".kiro/settings/mcp.json", '"--read-only",', "")
        self.assert_rejected(
            self.run_validator(),
            "MCP host configs no longer match the manifest",
        )

    def test_mcp_proxy_must_keep_its_guard_flags(self) -> None:
        manifest = self.read_manifest()
        for server in manifest["servers"]:
            if server["transport"] == "stdio":
                server["args"] = [arg for arg in server["args"] if arg != "--read-only"]
        self.write_manifest(manifest)
        subprocess.run(
            ["python3", "scripts/render_agent_configs.py"],
            cwd=self.repo,
            check=True,
            capture_output=True,
        )
        self.assert_rejected(
            self.run_validator(),
            "missing required guard flag --read-only",
        )

    def test_mcp_manifest_cannot_allow_a_customer_account_tool(self) -> None:
        manifest = self.read_manifest()
        manifest["servers"][0]["allowed_tools"].append("aws___call_aws")
        manifest["servers"][0]["blocked_tools"].remove("aws___call_aws")
        self.write_manifest(manifest)
        subprocess.run(
            ["python3", "scripts/render_agent_configs.py"],
            cwd=self.repo,
            check=True,
            capture_output=True,
        )
        self.assert_rejected(
            self.run_validator(),
            "allows a customer-account tool",
        )

    def test_mcp_manifest_must_cover_routed_capabilities(self) -> None:
        manifest = self.read_manifest()
        manifest["servers"] = [
            server for server in manifest["servers"] if server["capability"] != "current-web-research"
        ]
        self.write_manifest(manifest)
        subprocess.run(
            ["python3", "scripts/render_agent_configs.py"],
            cwd=self.repo,
            check=True,
            capture_output=True,
        )
        self.assert_rejected(
            self.run_validator(),
            "does not cover routed capability: current-web-research",
        )

    def test_mcp_manifest_must_not_require_environment_values(self) -> None:
        manifest = self.read_manifest()
        manifest["servers"][0]["required_env"] = ["SOME_API_KEY"]
        self.write_manifest(manifest)
        self.assert_rejected(
            self.run_validator(),
            "requires environment values in a shared manifest",
        )

    def test_generated_mcp_host_config_is_required(self) -> None:
        (self.repo / ".codex/config.toml").unlink()
        self.assert_rejected(
            self.run_validator(),
            "missing required file: .codex/config.toml",
        )

    def test_raw_inbox_source_filenames_stay_exempt(self) -> None:
        """Raw company sources keep their original names without failing the gate."""
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ASCII-only paths:", result.stdout)

    def test_push_guard_must_be_activated(self) -> None:
        self.init_git(activate_hooks=False)
        self.assert_rejected(
            self.run_validator(),
            "push guard is inactive; run: git config core.hooksPath .githooks",
        )

    def test_operational_customer_data_must_be_gitignored(self) -> None:
        self.replace_once(".gitignore", "customers/CUST-*", "# rule removed")
        self.init_git()
        self.assert_rejected(
            self.run_validator(),
            ".gitignore missing safety rule: customers/CUST-*",
        )

    def test_tracked_operational_customer_file_is_rejected(self) -> None:
        customer = self.repo / "customers/CUST-901"
        customer.mkdir()
        shutil.copy2(self.repo / "templates/customer-profile.md", customer / "profile.md")
        self.init_git()
        self.git("add", "-f", "customers/CUST-901/profile.md")
        self.assert_rejected(
            self.run_validator(),
            "operational customer files are tracked",
        )

    def test_push_guard_blocks_operational_customer_data(self) -> None:
        upstream = Path(self.tempdir.name) / "upstream.git"
        self.git("init", "-q", "--bare", str(upstream), cwd=Path(self.tempdir.name))
        self.init_git()
        self.git("remote", "add", "upstream", str(upstream))
        customer = self.repo / "customers/CUST-901"
        customer.mkdir()
        shutil.copy2(self.repo / "templates/customer-profile.md", customer / "profile.md")
        self.git("add", "-A")
        self.git("add", "-f", "customers/CUST-901/profile.md")
        self.git("commit", "-q", "-m", "customer work")

        blocked = subprocess.run(
            ["git", "push", "upstream", "main"],
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "TIKET_ALLOW_UPSTREAM_PUSH": "1"},
        )
        self.assertNotEqual(blocked.returncode, 0, blocked.stderr)
        self.assertIn("customers/CUST-901/profile.md", blocked.stderr)

    def test_push_guard_blocks_shared_repository_without_explicit_override(self) -> None:
        upstream = Path(self.tempdir.name) / "upstream2.git"
        self.git("init", "-q", "--bare", str(upstream), cwd=Path(self.tempdir.name))
        self.init_git()
        self.git("remote", "add", "upstream", str(upstream))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "framework only")

        env = {key: value for key, value in os.environ.items() if key != "TIKET_ALLOW_UPSTREAM_PUSH"}
        blocked = subprocess.run(
            ["git", "push", "upstream", "main"],
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(blocked.returncode, 0, blocked.stderr)
        self.assertIn("개인 운영 저장소가 아직 없습니다", blocked.stderr)

    def test_framework_candidate_passes(self) -> None:
        result = self.run_validator("--framework")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_aws_customer_skill_conformance_runner_is_required(self) -> None:
        (self.repo / "scripts/test_aws_customer_skill.py").unlink()
        self.assert_rejected(
            self.run_validator("--framework"),
            "missing required file: scripts/test_aws_customer_skill.py",
        )

    def test_framework_rejects_operational_customer_directory(self) -> None:
        customer = self.repo / "customers/CUST-901"
        customer.mkdir()
        shutil.copy2(self.repo / "templates/customer-profile.md", customer / "profile.md")
        self.assert_rejected(
            self.run_validator("--framework"),
            "framework candidate contains workspace-owned customer directories",
        )

    def test_framework_rejects_operational_customer_index_entries(self) -> None:
        index = self.repo / "customers/_index.md"
        index.write_text(
            index.read_text(encoding="utf-8")
            + "\n| CUST-901 | customers/CUST-901/profile.md | 1 | 2026-08-31 | local |\n",
            encoding="utf-8",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "framework candidate customer index differs from the clean template",
        )

    def test_example_rejects_operational_ticket_reference(self) -> None:
        self.replace_once(
            "examples/CUST-900/tickets/2026-08-28_Kiro-management-account-change/current.md",
            "TICKET-EXAMPLE-002",
            "TICKET-LOCAL-002",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "example ticket uses operational ticket reference",
        )

    def test_invalid_account_reference_is_rejected(self) -> None:
        self.replace_once(
            "examples/CUST-900/tickets/2026-08-28_Kiro-management-account-change/current.md",
            "account_ref: ACCOUNT-001",
            "account_ref: customer-prod",
        )
        self.assert_rejected(self.run_validator("--framework"), "has invalid account_ref")

    def test_completed_ticket_requires_sent_artifact(self) -> None:
        self.replace_once(
            "examples/CUST-900/tickets/2026-08-28_Kiro-management-account-change/history.md",
            "## 비식별 실제 발송본",
            "## 발송 artifact 누락",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "completed without a preserved de-identified sent artifact",
        )

    def test_history_date_must_cover_latest_event(self) -> None:
        self.replace_once(
            "examples/CUST-900/tickets/2026-08-28_Kiro-management-account-change/history.md",
            "updated_at: 2026-08-31",
            "updated_at: 2026-08-28",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "history updated_at predates its latest event",
        )

    def test_reply_style_contract_markers_are_required(self) -> None:
        self.replace_once(
            "playbooks/reply-style.md",
            "실제로 해결하려는 문제와 잠재된 우려",
            "표면 질문",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "reply style contract missing marker",
        )

    def test_technical_detailed_example_structure_is_required(self) -> None:
        self.replace_once(
            "examples/reply-styles/technical-detailed.md",
            "## 할인 방식별 판단 기준",
            "## 비교",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "technical-detailed example missing marker",
        )

    def test_example_personal_signature_is_rejected(self) -> None:
        self.replace_once(
            "examples/CUST-900/tickets/2026-08-28_Kiro-management-account-change/current.md",
            "[작성자 소개]",
            "가상회사 홍길동입니다.",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "example contains a possible personal signature",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
