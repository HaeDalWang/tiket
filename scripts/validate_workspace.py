#!/usr/bin/env python3
"""Validate the customer-support workspace structure and safety invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = ".githooks"
# Raw company sources keep the filenames they arrive with. They are never tracked
# and the validator compares them through NFC normalization.
ASCII_PATH_EXEMPT_PREFIXES = ("policy/inbox/",)
# Guard flags that must stay on the AWS MCP proxy command line. --read-only drops
# every tool not annotated readOnlyHint=true; --skip-auth keeps the docs-only
# connection from presenting an AWS credential.
MCP_REQUIRED_PROXY_FLAGS = ("--read-only", "--skip-auth")
# Tools that would bypass the broker-mediated read-only customer boundary.
MCP_FORBIDDEN_TOOLS = (
    "aws___call_aws",
    "aws___run_script",
    "aws___get_presigned_url",
)

REQUIRED_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".githooks/pre-push",
    ".kiro/steering/00-repository-rules.md",
    ".kiro/settings/mcp.json",
    ".mcp.json",
    ".claude/settings.json",
    ".codex/config.toml",
    "agents/environment/mcp-manifest.json",
    "agents/capability-catalog.md",
    "agents/install-verification.md",
    "agents/compatibility.md",
    "agents/runtime-status.md",
    "agents/task-router.md",
    "customers/_index.md",
    "scripts/check_public_sources.py",
    "scripts/export_framework_snapshot.py",
    "scripts/render_agent_configs.py",
    "scripts/test_aws_customer_skill.py",
    "scripts/test_export_framework_snapshot.py",
    "scripts/test_validate_workspace.py",
    "scripts/verify_mcp_servers.py",
    "policy/README.md",
    "policy/_routing.md",
    "policy/cards/_template.md",
    "policy/source-inventory.md",
    "policy/sources.json",
    "policy/inbox/README.md",
    "policy/pending-review.md",
    "playbooks/evidence-verification.md",
    "playbooks/reply-writing-rules.md",
    "playbooks/reply-style.md",
    "playbooks/infra-change-process.md",
    "playbooks/pitfalls/README.md",
    "playbooks/pitfalls/fitcloud-per-account-cost-not-separable.md",
    "playbooks/pitfalls/aurora-snapshot-encryption-unsupported.md",
    "playbooks/pitfalls/ec2-ri-sp-platform-and-marketplace-pricing.md",
    "handoff/README.md",
    "handoff/templates/poc-request.md",
    "handoff/templates/poc-result.md",
    "templates/customer-index.md",
    "templates/customer-profile.md",
]

CANONICAL_MARKERS = [
    "Draft only. Never send email",
    "Never call customer-account write APIs",
    "Customer-account access is read-only and broker-mediated only",
    "Never print or commit credentials",
    "Commit only de-identified customer context",
    "Customer-facing cost figures must be FitCloud-curated",
    "Exa queries must contain public, de-identified technical terms only",
    "agents/task-router.md",
    "customers/<customer-ref>/profile.md",
    "policy/_routing.md",
    "agents/capability-catalog.md",
    "confirmed`, `hypothesis`, and `unknown",
    "appending dated corrections",
    "never subjective judgment",
    "handoff/README.md",
    "Do not commit, push, merge",
]

TASK_ROUTER_MARKERS = [
    "Never load every policy, playbook, ticket, or skill by default",
    "`quick`",
    "`standard`",
    "`high-risk`",
    "Load a local skill only when its trigger directly matches",
    # 0001 에서 Decision Packet / Reply Brief 를 폐기하고 대체한 것들
    "playbooks/ticket-outputs.md",
    "발송 전 점검",
    "Reuse confirmed evidence",
]



REPLY_STYLE_MARKERS = [
    "`seungdo-contextual`",
    "`technical-detailed`",
    "실제로 해결하려는 문제와 잠재된 우려",
    "추가 왕복 없이",
    "고정된 줄 수나 문단 수를 두지 않는다",
    "`ACCOUNT-NNN`",
    "여러 절차를 한 문장이나 한 줄에 압축하지 않는다",
]

TECHNICAL_DETAILED_EXAMPLE_MARKERS = [
    "example_type: presentation-only",
    "presentation_profile: technical-detailed",
    "selected_decision_ids: [D1, D2, D3, D4, D5, D6]",
    "## 결론과 적용 범위",
    "## 할인 방식별 판단 기준",
    "## 확인된 사실과 미확정 값",
    "## 안전한 확인 순서",
    "## 근거와 재검증",
]


ROUTED_MODULE_MARKERS = {
    "policy/_routing.md": ["A `draft` card is a cited review artifact"],
    "playbooks/evidence-verification.md": [
        "confirmed",
        "hypothesis",
        "unknown",
        "Treat the reply as a draft until a human reviews and sends it",
    ],
    "playbooks/reply-writing-rules.md": [
        "Only a human sends email or posts to Zendesk",
        "문장 모양이 아니라 의미를 검증한다",
        "Every definitive statement is supported by a `[확인]` item that carries a source",
        # 0012: 발송 전 관문으로 가는 연결. 끊기면 관문이 고아가 된다.
        "## 발송 전 점검",
        "고객이 문의에서 밝힌 제약 안에서 실행 가능한 답을 준다",
        "고객이 실제로 보는 언어의 UI 명칭을 쓴다",
    ],
    "playbooks/infra-change-process.md": ["Stop at the human gate", "Design rollback first"],
    "handoff/README.md": ["Verify the returned repository, branch, commit, command, and output"],
    "templates/customer-profile.md": ["Never record personality judgments"],
}

ALWAYS_ON_CHAR_BUDGETS = {
    "CLAUDE.md": 4_500,
    "AGENTS.md": 1_800,
    ".kiro/steering/00-repository-rules.md": 1_800,
}
AGENTS_CLAUDE_COMBINED_CHAR_BUDGET = 6_000

# 0013: 아래 안전 문장이 세 진입점에서 조용히 사라진 적이 있다. CLAUDE.md 만 검사가 있어
# AGENTS.md 와 Kiro steering 의 삭제는 발견되지 않았다. 셋 다 고정한다.
ENTRYPOINT_SAFETY_MARKERS = [
    "Never call customer-account write APIs",
    "never send",
]

ENTRYPOINT_MARKERS = {
    "AGENTS.md": [
        "CLAUDE.md", "agents/task-router.md", "FitCloud", "policy/_routing.md",
        "handoff/README.md", "agents/runtime-status.md", *ENTRYPOINT_SAFETY_MARKERS,
    ],
    ".kiro/steering/00-repository-rules.md": [
        "CLAUDE.md",
        "agents/task-router.md",
        "FitCloud",
        "policy/_routing.md",
        "handoff/README.md",
        "agents/runtime-status.md",
        *ENTRYPOINT_SAFETY_MARKERS,
    ],
}

FRONTMATTER_FILES = [
    "policy/cards/_template.md",
    "handoff/templates/poc-request.md",
    "handoff/templates/poc-result.md",
    "templates/customer-profile.md",
]

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt"}
POLICY_STATUSES = {"draft", "active", "superseded", "retired"}
TRACKED_POLICY_PII_PATTERNS = {
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "Korean mobile number": re.compile(r"\b01[016789]-\d{3,4}-\d{4}\b"),
    "12-digit account-like value": re.compile(r"(?<!\d)\d{12}(?!\d)"),
}
TRACKED_CUSTOMER_IDENTIFIER_PATTERNS = {
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone number": re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"),
    "IPv4 address": re.compile(
        r"(?<!\d)(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?:/\d{1,2})?(?!\d)"
    ),
    "12-digit account-like value": re.compile(r"(?<![A-Za-z0-9])\d{12}(?![A-Za-z0-9])"),
}
EXAMPLE_PERSONAL_SIGNATURE_PATTERN = re.compile(
    r"(?m)^(?!\[작성자 소개\]$)[가-힣A-Za-z0-9().&-]{2,30}\s+[가-힣]{2,4}입니다\.?$"
)
DEIDENTIFICATION_SCAN_EXCLUSIONS = {
    "policy/sources.json",
    "policy/source-inventory.md",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_markdown_sources(relative: str, content: str, errors: list[str]) -> None:
    body, separator, sources = content.partition("## Sources")
    cited = {int(value) for value in re.findall(r"\[(\d+)\]", body)}
    listed_values = [
        int(value)
        for value in re.findall(r"^\[(\d+)\]\s+https?://", sources, re.MULTILINE)
    ]
    listed = set(listed_values)
    if cited and not separator:
        fail(errors, f"{relative} cites sources but has no Sources block")
    if len(listed_values) != len(listed):
        fail(errors, f"{relative} has duplicate source IDs")
    if cited - listed:
        fail(errors, f"{relative} has citations missing from Sources: {sorted(cited - listed)}")
    if listed - cited:
        fail(errors, f"{relative} has unused Sources: {sorted(listed - cited)}")


def read_text(relative: str, errors: list[str]) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(errors, f"missing required file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(errors, f"required text file is not UTF-8: {relative}")
        return ""


def gitignored_relatives(candidates: list[Path]) -> set[str]:
    """git 이 무시하는 경로들. 판단은 git 에게 맡긴다.

    무시되는 파일은 공용 저장소에 도달할 수 없으므로 유출 스캔의 대상이 아니다.
    디렉터리 이름을 하드코딩하면(`.private` 처럼) 다음에 추가되는 로컬 전용 경로마다
    같은 오탐이 반복된다 — `tickets/` 가 정확히 그렇게 걸렸다.

    git 을 못 쓰면 빈 집합을 돌려주어 전부 스캔한다(fail closed). 스캔 범위가 넓어
    오탐이 날지언정, 봐야 할 파일을 조용히 건너뛰지는 않는다.
    """
    if not (ROOT / ".git").exists() or not candidates:
        return set()
    relatives = [str(path.relative_to(ROOT)) for path in candidates]
    result = subprocess.run(
        ["git", "check-ignore", "--stdin"],
        cwd=ROOT,
        input="\n".join(relatives),
        capture_output=True,
        text=True,
        check=False,
    )
    # 0 = 일부가 무시됨, 1 = 무시되는 것 없음. 그 외는 git 쪽 문제이므로 전부 스캔한다.
    if result.returncode not in (0, 1):
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def iter_text_files() -> list[Path]:
    candidates: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.relative_to(ROOT).parts:
            continue
        candidates.append(path)
    ignored = gitignored_relatives(candidates)
    return [path for path in candidates if str(path.relative_to(ROOT)) not in ignored]


def validate_policy_cards(errors: list[str]) -> tuple[int, int]:
    inventory = read_text("policy/source-inventory.md", errors)
    routing = read_text("policy/_routing.md", errors)
    manifest_content = read_text("policy/sources.json", errors)
    try:
        manifest = json.loads(manifest_content)
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid policy/sources.json: {exc}")
        manifest = {"sources": []}
    source_entries = manifest.get("sources", [])
    sources_by_id = {entry.get("id"): entry for entry in source_entries if entry.get("id")}
    if len(sources_by_id) != len(source_entries):
        fail(errors, "duplicate or missing source id in policy/sources.json")
    known_sources = set(sources_by_id)
    inventory_sources = set(re.findall(r"`(SRC-[A-Z0-9-]+)`", inventory))
    if inventory_sources != known_sources:
        missing_from_inventory = sorted(known_sources - inventory_sources)
        missing_from_manifest = sorted(inventory_sources - known_sources)
        if missing_from_inventory:
            fail(errors, f"source missing from inventory: {', '.join(missing_from_inventory)}")
        if missing_from_manifest:
            fail(errors, f"source missing from manifest: {', '.join(missing_from_manifest)}")
    seen_ids: dict[str, str] = {}
    cards = sorted((ROOT / "policy/cards").glob("*.md"))
    cards = [card for card in cards if card.name != "_template.md"]

    for card in cards:
        relative = str(card.relative_to(ROOT))
        content = card.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not frontmatter_match:
            fail(errors, f"invalid policy card frontmatter: {relative}")
            continue
        frontmatter = frontmatter_match.group(1)
        id_match = re.search(r"^id:\s*([^#\n]+)", frontmatter, re.MULTILINE)
        status_match = re.search(r"^status:\s*([^#\s]+)", frontmatter, re.MULTILINE)
        if not id_match:
            fail(errors, f"policy card missing id: {relative}")
        else:
            policy_id = id_match.group(1).strip().strip('"\'')
            if policy_id in seen_ids:
                fail(errors, f"duplicate policy id {policy_id}: {seen_ids[policy_id]}, {relative}")
            seen_ids[policy_id] = relative
            if f"`{policy_id}`" not in routing:
                fail(errors, f"policy card not routed: {policy_id} ({relative})")
        if not status_match or status_match.group(1) not in POLICY_STATUSES:
            fail(errors, f"invalid policy card status: {relative}")
            card_status = ""
        else:
            card_status = status_match.group(1)

        if id_match:
            policy_id = id_match.group(1).strip().strip('"\'')
            routing_row = next(
                (line for line in routing.splitlines() if f"| `{policy_id}` |" in line),
                "",
            )
            if routing_row and f"| {card_status} |" not in routing_row:
                fail(errors, f"routing status differs from card status: {policy_id}")

        if card_status == "active":
            required_authority_fields = [
                "source_owner",
                "source_version",
                "applicability",
                "authority_verified_at",
                "approved_by",
                "approved_at",
            ]
            for field in required_authority_fields:
                field_match = re.search(
                    rf"^{field}:\s*([^#\n]*)",
                    frontmatter,
                    re.MULTILINE,
                )
                value = field_match.group(1).strip().strip('"\'') if field_match else ""
                if not value or value.lower() in {"unknown", "tbd", "yyyy-mm-dd"}:
                    fail(errors, f"active policy card missing verified {field}: {relative}")
            review_match = re.search(r"^review_by:\s*([^#\n]*)", frontmatter, re.MULTILINE)
            review_value = review_match.group(1).strip().strip('"\'') if review_match else ""
            try:
                review_date = date.fromisoformat(review_value)
            except ValueError:
                fail(errors, f"active policy card has invalid review_by: {relative}")
            else:
                if review_date < date.today():
                    fail(errors, f"active policy card review date has passed: {relative}")
            blocker_match = re.search(
                r"^activation_blocker:\s*([^#\n]*)",
                frontmatter,
                re.MULTILINE,
            )
            blocker = blocker_match.group(1).strip().strip('"\'') if blocker_match else ""
            if blocker:
                fail(errors, f"active policy card still has activation_blocker: {relative}")

        if card_status == "retired":
            for field in [
                "retired_at",
                "retirement_reason",
                "replacement",
                "approved_by",
                "approved_at",
            ]:
                field_match = re.search(
                    rf"^{field}:\s*([^#\n]*)",
                    frontmatter,
                    re.MULTILINE,
                )
                value = field_match.group(1).strip().strip('"\'') if field_match else ""
                if not value or value.lower() in {"unknown", "tbd", "yyyy-mm-dd"}:
                    fail(errors, f"retired policy card missing {field}: {relative}")

        for source_id in set(
            re.findall(r"SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*\b", content)
        ):
            if source_id not in known_sources:
                fail(errors, f"unknown source id {source_id} in {relative}")

        for source_id, start_text, end_text in re.findall(
            r"(SRC-[A-Z0-9-]+):(\d+)(?:-(\d+))?", content
        ):
            entry = sources_by_id.get(source_id)
            if not entry:
                continue
            start = int(start_text)
            end = int(end_text or start_text)
            if start < 1 or end < start or end > int(entry.get("lines", 0)):
                fail(errors, f"invalid citation range {source_id}:{start}-{end} in {relative}")

        for label, pattern in TRACKED_POLICY_PII_PATTERNS.items():
            if pattern.search(content):
                fail(errors, f"possible {label} copied into tracked policy card: {relative}")

    for reference in re.findall(r"`(cards/[^`]+\.md)`", routing):
        if not (ROOT / "policy" / reference).is_file():
            fail(errors, f"routing references missing card: {reference}")

    if (ROOT / ".git").exists():
        result = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-files", "policy/inbox"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        tracked_raw = [
            line
            for line in result.stdout.splitlines()
            if line and line != "policy/inbox/README.md"
        ]
        if tracked_raw:
            fail(errors, f"raw inbox files are tracked: {', '.join(tracked_raw)}")

    raw_dir = ROOT / "policy/inbox"
    raw_files = sorted(raw_dir.glob("*.txt"))
    raw_by_nfc = {
        unicodedata.normalize("NFC", path.name): path
        for path in raw_files
    }
    verified_sources = 0
    if raw_files:
        expected_names = {
            entry.get("filename_nfc")
            for entry in source_entries
            if entry.get("filename_nfc")
        }
        extra_names = sorted(set(raw_by_nfc) - expected_names)
        if extra_names:
            fail(errors, f"unregistered raw source files: {', '.join(extra_names)}")

    for source_id, entry in sources_by_id.items():
        tracked_relative = entry.get("path")
        if tracked_relative:
            path = (ROOT / tracked_relative).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"manifest tracked source escapes repository: {source_id}")
                continue
            if not path.is_file():
                fail(errors, f"manifest tracked source missing: {source_id} ({tracked_relative})")
                continue
        elif raw_files:
            filename = entry.get("filename_nfc")
            path = raw_by_nfc.get(filename)
            if not path:
                fail(errors, f"manifest source file missing from inbox: {source_id} ({filename})")
                continue
        else:
            continue

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry.get("sha256"):
            fail(errors, f"source hash changed: {source_id} ({path.name})")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count != int(entry.get("lines", 0)):
            fail(
                errors,
                f"source line count changed: {source_id} expected {entry.get('lines')} got {line_count}",
            )
        verified_sources += 1

    return len(cards), verified_sources




def _string_id_list(
    relative: str,
    owner: str,
    value: object,
    pattern: str,
    errors: list[str],
) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(errors, f"{relative} {owner} must be a string list")
        return []
    result = list(value)
    for item in result:
        if not re.fullmatch(pattern, item):
            fail(errors, f"{relative} {owner} has invalid ID: {item}")
    if len(result) != len(set(result)):
        fail(errors, f"{relative} {owner} contains duplicate IDs")
    return result


def validate_deidentified_repository(errors: list[str]) -> None:
    customer_root = ROOT / "customers"
    for path in customer_root.iterdir():
        if path.is_dir() and not re.fullmatch(r"CUST-\d{3,}", path.name):
            fail(errors, f"customer directory is not de-identified: customers/{path.name}")
        if path.is_dir():
            profile = path / "profile.md"
            if not profile.is_file():
                fail(errors, f"customer profile missing: customers/{path.name}/profile.md")
                continue
            profile_content = profile.read_text(encoding="utf-8")
            if not re.search(
                r"^contract_baseline:\s*SRC-FITCLOUD-TERMS-001\s*$",
                profile_content,
                re.MULTILINE,
            ):
                fail(errors, f"customer profile missing standard contract baseline: customers/{path.name}/profile.md")
            if not re.search(r"^contract_exceptions:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing contract_exceptions: customers/{path.name}/profile.md")
            payer_match = re.search(
                r"^payer_model:\s*(standalone|integrated|other|unknown)(?:\s+#.*)?$",
                profile_content,
                re.MULTILINE,
            )
            if not payer_match:
                fail(errors, f"customer profile missing valid payer_model: customers/{path.name}/profile.md")
            if not re.search(r"^payer_verified_at:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing payer_verified_at: customers/{path.name}/profile.md")
            coc_owner_match = re.search(
                r"^coc_owner_ref:\s*(?:\"\"|CONTACT-\d{3,})(?:\s+#.*)?$",
                profile_content,
                re.MULTILINE,
            )
            if not coc_owner_match:
                fail(errors, f"customer profile missing valid coc_owner_ref: customers/{path.name}/profile.md")
            if not re.search(r"^coc_roster_verified_at:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing coc_roster_verified_at: customers/{path.name}/profile.md")

            # 0002 이후 운영 티켓은 로컬 전용 tickets/ 에 있다. customers/ 는 프로필만 둔다.
            ticket_dir = path / "tickets"
            if ticket_dir.is_dir():
                fail(
                    errors,
                    f"tickets moved to the local-only tickets/ directory: "
                    f"{ticket_dir.relative_to(ROOT)}",
                )
    profile_template = read_text("templates/customer-profile.md", errors)
    if "contract_baseline: SRC-FITCLOUD-TERMS-001" not in profile_template:
        fail(errors, "customer profile template missing standard contract baseline")
    if "contract_exceptions:" not in profile_template:
        fail(errors, "customer profile template missing contract_exceptions")
    if not re.search(
        r"^payer_model:\s*unknown(?:\s+#.*)?$",
        profile_template,
        re.MULTILINE,
    ):
        fail(errors, "customer profile template missing default payer_model")
    if "payer_verified_at:" not in profile_template:
        fail(errors, "customer profile template missing payer_verified_at")
    if not re.search(
        r"^coc_owner_ref:\s*\"\"(?:\s+#.*)?$",
        profile_template,
        re.MULTILINE,
    ):
        fail(errors, "customer profile template missing default coc_owner_ref")
    if "coc_roster_verified_at:" not in profile_template:
        fail(errors, "customer profile template missing coc_roster_verified_at")
    for marker in ["법정 보존 근거 reference:", "고객별 보존/삭제 예외:", "법무 확인일:"]:
        if marker not in profile_template:
            fail(errors, f"customer profile template missing retention field: {marker}")
    # 작업 지시서 형식 고정 (0009). 항목 나열로 되돌아가면 티켓을 옮겨 적은 것이 되고,
    # 그럴 거면 실행자는 티켓을 본다 — 실제 피드백으로 한 번 폐기된 형태다.
    intake_template = read_text("templates/ticket-intake.md", errors)
    for marker in [
        "## 작업 지시",
        "[변경]",
        "이 줄만 고치면 아래는 그대로 실행된다",
        "되돌릴 근거",
        "적용됐는지 확인한다",
        "[확인]",
        "[추측]",
        "[모름]",
        # 0010: 출처 없는 [확인] 을 막는 문장. 이게 빠지면 등급이 장식이 된다.
        "출처 없는 [확인] 은 [확인] 이 아니다",
        "확인 방법:",
        "유선으로 처리했으면",
        # 0011: 문서 충돌을 조용히 넘기지 않게 하는 문장
        "공식 문서끼리 충돌하면",
        # 0012: 발송 전 관문. 규칙이 있는데도 안 지켜져서 만든 것이라 항목이 사라지면 안 된다.
        "## 발송 전 점검",
        "고객이 문의에서 밝힌 제약을 답변이 지키는가",
        "콘솔 경로를 고객이 보는 화면 그대로 썼는가",
        "지금 답할 수 있는데 되묻고 있지 않은가",
    ]:
        if marker not in intake_template:
            fail(errors, f"ticket intake template missing marker: {marker}")

    retention_hierarchy = (
        "law/legal obligation → customer-specific contract/SLA/SOW → "
        "active standard terms → active Offboarding guide"
    )
    for relative in [
        "policy/cards/POLICY-DATA-001-contract-termination-data-lifecycle.md",
        "policy/cards/POLICY-OFFBOARD-001-customer-approval-and-data-handling.md",
    ]:
        if retention_hierarchy not in read_text(relative, errors):
            fail(errors, f"retention hierarchy missing from {relative}")

    payer_card = read_text("policy/cards/POLICY-PAYER-001-standalone-payer-scope.md", errors)
    for marker in ["CSR", "COP", "FitCloud"]:
        if marker not in payer_card:
            fail(errors, f"standalone-Payer verification rule missing: {marker}")

    for path in iter_text_files():
        relative = str(path.relative_to(ROOT))
        if relative.startswith("policy/inbox/") or relative in DEIDENTIFICATION_SCAN_EXCLUSIONS:
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in TRACKED_CUSTOMER_IDENTIFIER_PATTERNS.items():
            if pattern.search(content):
                fail(
                    errors,
                    f"possible tracked customer {label}: {relative}; value intentionally not printed",
                )

    if (ROOT / ".git").exists():
        result = subprocess.run(
            ["git", "check-ignore", "-q", ".private/customer-map.md"],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            fail(errors, ".private/customer-map.md is not gitignored")


def validate_ascii_paths(errors: list[str]) -> int:
    """Repository paths must be ASCII.

    Non-ASCII path names are compared as exact strings by this validator, by
    .gitignore, by grep patterns in agent instructions, and by git plumbing. The
    git/filesystem boundary gives no Unicode normalization guarantee, so the same
    file can appear under NFC on one machine and NFD on another: lookups still
    succeed on macOS while directory enumeration silently stops matching. Raw
    company sources under the inbox are exempt because their names come from the
    source system, they are never tracked, and they are NFC-normalized on read.
    """
    checked = 0
    offenders: list[str] = []

    def offending(relative: str) -> bool:
        if relative.startswith(ASCII_PATH_EXEMPT_PREFIXES):
            return False
        return not relative.isascii()

    if (ROOT / ".git").exists():
        listed = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-files", "-z"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        for relative in listed.stdout.split("\0"):
            if not relative:
                continue
            checked += 1
            if offending(relative):
                offenders.append(relative)

    for path in ROOT.rglob("*"):
        relative_parts = path.relative_to(ROOT).parts
        if not relative_parts or relative_parts[0] in {".git", ".private"}:
            continue
        relative = path.relative_to(ROOT).as_posix()
        checked += 1
        if offending(relative):
            offenders.append(relative)

    for relative in sorted(set(offenders)):
        fail(
            errors,
            "non-ASCII repository path; rename it and update every reference: "
            f"{relative}",
        )
    return checked


def validate_mcp_contract(errors: list[str]) -> tuple[int, int]:
    """Project-scoped MCP capability must be declared once and generated for every host.

    The failure this prevents: a capability that works only in the maintainer's
    personal agent profile while the repository documents it as available. Returns
    (server count, host file count).
    """
    relative = "agents/environment/mcp-manifest.json"
    raw = read_text(relative, errors)
    if not raw:
        return 0, 0
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid MCP manifest JSON: {relative} ({exc})")
        return 0, 0

    servers = manifest.get("servers") or []
    if not servers:
        fail(errors, f"MCP manifest declares no server: {relative}")

    declared_capabilities: set[str] = set()
    for server in servers:
        server_id = server.get("id", "<missing id>")
        for field in ("id", "capability", "transport", "authentication", "classification"):
            if not server.get(field):
                fail(errors, f"MCP server missing {field}: {server_id}")
        declared_capabilities.add(server.get("capability", ""))
        if not server.get("allowed_tools"):
            fail(errors, f"MCP server declares no include-only tool list: {server_id}")
        if server.get("required_env"):
            fail(
                errors,
                f"MCP server requires environment values in a shared manifest: {server_id}",
            )
        overlap = set(server.get("allowed_tools") or []) & set(server.get("blocked_tools") or [])
        if overlap:
            fail(
                errors,
                f"MCP server lists the same tool as allowed and blocked: {server_id} "
                f"({', '.join(sorted(overlap))})",
            )
        if server.get("transport") == "stdio":
            if not server.get("pinned_version"):
                fail(errors, f"MCP stdio server is not version pinned: {server_id}")
            args = server.get("args") or []
            for required_flag in MCP_REQUIRED_PROXY_FLAGS:
                if required_flag not in args:
                    fail(
                        errors,
                        f"MCP stdio server missing required guard flag {required_flag}: {server_id}",
                    )
        for tool in MCP_FORBIDDEN_TOOLS:
            if tool in (server.get("allowed_tools") or []):
                fail(errors, f"MCP server allows a customer-account tool: {server_id} ({tool})")

    for capability in ("aws-official-research", "current-web-research"):
        if capability not in declared_capabilities:
            fail(errors, f"MCP manifest does not cover routed capability: {capability}")

    host_files: list[str] = []
    for host in manifest.get("hosts") or []:
        for key in ("config_path", "permissions_path"):
            path = host.get(key)
            if path:
                host_files.append(path)
    for path in host_files:
        if not (ROOT / path).is_file():
            fail(errors, f"generated MCP host config missing: {path}")

    rendered = subprocess.run(
        ["python3", "scripts/render_agent_configs.py", "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if rendered.returncode != 0:
        drifted = [
            line.strip().removeprefix("- out of date: ")
            for line in rendered.stderr.splitlines()
            if line.strip().startswith("- out of date: ")
        ]
        if drifted:
            fail(
                errors,
                "MCP host configs no longer match the manifest "
                f"({', '.join(drifted)}); run: python3 scripts/render_agent_configs.py",
            )
        else:
            fail(errors, "cannot verify MCP host configs against the manifest")

    return len(servers), len(host_files)


def validate_local_only_customer_data(errors: list[str]) -> None:
    """Alpha remote model: operational customer data stays local and unpushed.

    No personal operational remote is approved yet, so the only configured remote is
    the shared framework repository. Two independent guards must be in place:
    the ignore rule (ships with the repository) and the pre-push hook (needs one
    local activation command).
    """
    if not (ROOT / ".git").exists():
        return

    probe = "customers/CUST-001/profile.md"
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", probe],
        cwd=ROOT,
        check=False,
    )
    if ignored.returncode != 0:
        fail(errors, f"operational customer data is not gitignored: {probe}")

    tracked = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-files", "customers/"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    unexpected = [
        line
        for line in tracked.stdout.splitlines()
        if line and line != "customers/_index.md"
    ]
    if unexpected:
        fail(
            errors,
            "operational customer files are tracked and would reach the shared "
            f"repository: {', '.join(unexpected)}",
        )

    configured = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    hooks_path = configured.stdout.strip()
    if hooks_path != HOOKS_DIR:
        fail(
            errors,
            "push guard is inactive; run: git config core.hooksPath "
            f"{HOOKS_DIR}",
        )
        return
    hook = ROOT / HOOKS_DIR / "pre-push"
    if not hook.is_file():
        fail(errors, f"push guard hook is missing: {HOOKS_DIR}/pre-push")
    elif not os.access(hook, os.X_OK):
        fail(
            errors,
            f"push guard hook is not executable; run: chmod +x {HOOKS_DIR}/pre-push",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--framework",
        action="store_true",
        help="fail when operational customer directories exist in the common upstream candidate",
    )
    args = parser.parse_args()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        read_text(relative, errors)

    always_on_contents = {
        relative: read_text(relative, errors) for relative in ALWAYS_ON_CHAR_BUDGETS
    }
    canonical = always_on_contents["CLAUDE.md"]
    for relative, budget in ALWAYS_ON_CHAR_BUDGETS.items():
        length = len(always_on_contents[relative])
        if length > budget:
            fail(errors, f"{relative} exceeds always-on character budget: {length} / {budget}")
    combined_length = len(always_on_contents["AGENTS.md"]) + len(canonical)
    if combined_length > AGENTS_CLAUDE_COMBINED_CHAR_BUDGET:
        fail(
            errors,
            "AGENTS.md + CLAUDE.md exceeds combined always-on character budget: "
            f"{combined_length} / {AGENTS_CLAUDE_COMBINED_CHAR_BUDGET}",
        )
    for marker in CANONICAL_MARKERS:
        if marker not in canonical:
            fail(errors, f"CLAUDE.md missing canonical marker: {marker}")

    task_router = read_text("agents/task-router.md", errors)
    for marker in TASK_ROUTER_MARKERS:
        if marker not in task_router:
            fail(errors, f"task router missing marker: {marker}")

    shared_environment = read_text("agents/shared-agent-environment.md", errors)
    validate_markdown_sources("agents/shared-agent-environment.md", shared_environment, errors)

    for relative, markers in {
    }.items():
        content = read_text(relative, errors)
        for marker in markers:
            if marker not in content:
                fail(errors, f"{relative} missing semantic contract marker: {marker}")

    reply_style = read_text("playbooks/reply-style.md", errors)
    for marker in REPLY_STYLE_MARKERS:
        if marker not in reply_style:
            fail(errors, f"reply style contract missing marker: {marker}")



    for relative, markers in ROUTED_MODULE_MARKERS.items():
        content = read_text(relative, errors)
        for marker in markers:
            if marker not in content:
                fail(errors, f"{relative} missing routed safety marker: {marker}")

    for relative, markers in ENTRYPOINT_MARKERS.items():
        content = read_text(relative, errors)
        for marker in markers:
            if marker not in content:
                fail(errors, f"{relative} missing entrypoint marker: {marker}")

    runtime_status = read_text("agents/runtime-status.md", errors)
    for marker in [
        "`customer-aws-readonly` | enabled",
        "`fitcloud-billing` | enabled",
        "### Evidence provenance",
        "Operator-attested",
        "mcp-proxy-for-aws@1.6.4",
        "aws___search_documentation",
        "aws___read_documentation",
        "aws___list_regions",
        "aws___get_regional_availability",
        "aws___call_aws",
        "aws___run_script",
        "aws___get_tasks",
        "aws___get_presigned_url",
        "aws___retrieve_skill",
        "https://mcp.exa.ai/mcp",
        "web_search_exa",
        "web_fetch_exa",
        "agent_run",
        "web_search_advanced_exa",
        "anonymous",
    ]:
        if marker not in runtime_status:
            fail(errors, f"runtime capability status missing marker: {marker}")

    for relative in FRONTMATTER_FILES:
        content = read_text(relative, errors)
        if not content.startswith("---\n") or "\n---\n" not in content[4:]:
            fail(errors, f"invalid or missing frontmatter fence: {relative}")

    gitignore = read_text(".gitignore", errors)
    for marker in [
        ".private/",
        "policy/raw/",
        "policy/inbox/*",
        "!policy/inbox/README.md",
        "customers/CUST-*",
        "terraform.tfstate",
        "*.kubeconfig",
    ]:
        if marker not in gitignore:
            fail(errors, f".gitignore missing safety rule: {marker}")

    validate_local_only_customer_data(errors)
    mcp_server_count, mcp_host_count = validate_mcp_contract(errors)
    ascii_path_count = validate_ascii_paths(errors)

    plan_files = sorted(path.name for path in ROOT.glob("계획*.md"))
    if plan_files:
        fail(errors, f"obsolete plan files remain: {', '.join(plan_files)}")

    for path in iter_text_files():
        content = path.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                relative = path.relative_to(ROOT)
                fail(errors, f"possible {label} in {relative}; value intentionally not printed")

    policy_card_count, verified_source_count = validate_policy_cards(errors)
    validate_deidentified_repository(errors)
    if args.framework:
        customer_dirs = sorted(path.name for path in (ROOT / "customers").iterdir() if path.is_dir())
        if customer_dirs:
            fail(errors, "framework candidate contains workspace-owned customer directories")
        customer_index = read_text("customers/_index.md", errors)
        clean_customer_index = read_text("templates/customer-index.md", errors)
        if customer_index != clean_customer_index:
            fail(errors, "framework candidate customer index differs from the clean template")

    if errors:
        print("workspace validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("workspace validation: PASS")
    print(f"- required files: {len(REQUIRED_FILES)}")
    print(f"- CLAUDE.md characters: {len(canonical)} / {ALWAYS_ON_CHAR_BUDGETS['CLAUDE.md']}")
    print(
        "- AGENTS.md + CLAUDE.md characters: "
        f"{combined_length} / {AGENTS_CLAUDE_COMBINED_CHAR_BUDGET}"
    )
    print("- entrypoints: AGENTS.md, Kiro steering")
    print("- local-only customer data: gitignored, push guard active")
    print(
        f"- project-scoped MCP: {mcp_server_count} servers, "
        f"{mcp_host_count} host configs generated from the manifest"
    )
    print(f"- ASCII-only paths: {ascii_path_count} checked")
    print(f"- validation mode: {'framework' if args.framework else 'workspace'}")
    print("- templates: frontmatter present")
    print("- shared documentation citation map: consistent")
    print("- ticket outputs: work order / investigation / advisory, pre-send gate pinned")
    print("- obsolete plan files: none")
    print("- credential signature scan: clear")
    print(f"- policy cards: {policy_card_count}, routed with known sources")
    print("- tracked policy PII scan: clear")
    print("- raw inbox tracked files: README.md only")
    print("- tracked customer identifier scan: clear")
    if verified_source_count:
        print(f"- raw source hashes and line counts: {verified_source_count} verified")
    else:
        print("- raw source hashes and line counts: skipped (inbox not present)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
