#!/usr/bin/env python3
"""Regression tests for the workspace validator's Alpha safety gates."""

from __future__ import annotations

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
        customer = self.repo / "고객/CUST-901"
        customer.mkdir()
        shutil.copy2(self.repo / "템플릿/고객_프로필.md", customer / "프로필.md")
        self.assert_rejected(
            self.run_validator("--framework"),
            "framework candidate contains workspace-owned customer directories",
        )

    def test_framework_rejects_operational_customer_index_entries(self) -> None:
        index = self.repo / "고객/_인덱스.md"
        index.write_text(
            index.read_text(encoding="utf-8")
            + "\n| CUST-901 | 고객/CUST-901/프로필.md | 1 | 2026-08-31 | local |\n",
            encoding="utf-8",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "framework candidate customer index differs from the clean template",
        )

    def test_example_rejects_operational_ticket_reference(self) -> None:
        self.replace_once(
            "예시/CUST-900/티켓/2026-08-28_Kiro-management-account-change/current.md",
            "TICKET-EXAMPLE-002",
            "TICKET-LOCAL-002",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "example ticket uses operational ticket reference",
        )

    def test_invalid_account_reference_is_rejected(self) -> None:
        self.replace_once(
            "예시/CUST-900/티켓/2026-08-28_Kiro-management-account-change/current.md",
            "account_ref: ACCOUNT-001",
            "account_ref: customer-prod",
        )
        self.assert_rejected(self.run_validator("--framework"), "has invalid account_ref")

    def test_completed_ticket_requires_sent_artifact(self) -> None:
        self.replace_once(
            "예시/CUST-900/티켓/2026-08-28_Kiro-management-account-change/history.md",
            "## 비식별 실제 발송본",
            "## 발송 artifact 누락",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "completed without a preserved de-identified sent artifact",
        )

    def test_history_date_must_cover_latest_event(self) -> None:
        self.replace_once(
            "예시/CUST-900/티켓/2026-08-28_Kiro-management-account-change/history.md",
            "updated_at: 2026-08-31",
            "updated_at: 2026-08-28",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "history updated_at predates its latest event",
        )

    def test_reply_style_contract_markers_are_required(self) -> None:
        self.replace_once(
            "플레이북/회신_스타일.md",
            "실제로 해결하려는 문제와 잠재된 우려",
            "표면 질문",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "reply style contract missing marker",
        )

    def test_technical_detailed_example_structure_is_required(self) -> None:
        self.replace_once(
            "예시/회신_스타일/technical-detailed.md",
            "## 할인 방식별 판단 기준",
            "## 비교",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "technical-detailed example missing marker",
        )

    def test_example_personal_signature_is_rejected(self) -> None:
        self.replace_once(
            "예시/CUST-900/티켓/2026-08-28_Kiro-management-account-change/current.md",
            "[작성자 소개]",
            "가상회사 홍길동입니다.",
        )
        self.assert_rejected(
            self.run_validator("--framework"),
            "example contains a possible personal signature",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
