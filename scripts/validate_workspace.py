#!/usr/bin/env python3
"""Validate the customer-support workspace structure and safety invariants."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".kiro/steering/00-repository-rules.md",
    "에이전트/기능_카탈로그.md",
    "에이전트/설치_검증.md",
    "에이전트/호환성.md",
    "에이전트/런타임_상태.md",
    "에이전트/작업_라우터.md",
    "고객/_인덱스.md",
    "회사규정/README.md",
    "회사규정/_라우팅.md",
    "회사규정/카드/_템플릿.md",
    "회사규정/원본_목록.md",
    "회사규정/sources.json",
    "회사규정/수신함/README.md",
    "회사규정/검토_대기.md",
    "플레이북/근거_검증.md",
    "플레이북/회신_작성_규칙.md",
    "플레이북/인프라_작업_프로세스.md",
    "플레이북/함정/README.md",
    "플레이북/함정/fitcloud-계정별-비용-분리불가.md",
    "플레이북/함정/aurora-스냅샷-암호화-불가.md",
    "연계/README.md",
    "연계/템플릿/PoC_의뢰서.md",
    "연계/템플릿/PoC_결과서.md",
    "템플릿/고객_프로필.md",
    "템플릿/티켓.md",
    "템플릿/티켓_근거.md",
    "템플릿/티켓_이력.md",
    "템플릿/결정_패킷.md",
    "템플릿/회신_브리프.md",
]

CANONICAL_MARKERS = [
    "Draft only. Never send email",
    "Never call customer-account write APIs",
    "aws-customer-account-ops` is temporarily blocked",
    "Never print or commit credentials",
    "Commit only de-identified customer context",
    "Customer-facing cost figures must be FitCloud-curated",
    "Exa queries must contain public, de-identified technical terms only",
    "에이전트/작업_라우터.md",
    "고객/<customer-ref>/프로필.md",
    "회사규정/_라우팅.md",
    "에이전트/기능_카탈로그.md",
    "confirmed`, `hypothesis`, and `unknown",
    "appending dated corrections",
    "never subjective judgment",
    "연계/README.md",
    "Do not commit, push, merge",
]

TASK_ROUTER_MARKERS = [
    "Never load every policy, playbook, ticket, or skill by default",
    "`quick`",
    "`standard`",
    "`high-risk`",
    "Load a local skill only when its trigger directly matches",
    "Decision Packet",
    "Reply Brief",
    "Do not read `history.md` unless",
    "Reuse confirmed evidence",
]

DECISION_PACKET_TEMPLATE_MARKERS = [
    "Decision Packet v2",
    '"version": 2',
    '"id": "D1"',
    '"decisions"',
    '"fact_ids"',
    '"hypothesis_ids"',
    '"unknown_ids"',
    '"actions"',
    '"prohibited_claims"',
    "Absence from an example list is not confirmation",
]

REPLY_BRIEF_TEMPLATE_MARKERS = [
    "Reply Brief v2",
    '"version": 2',
    '"decision_ids"',
    '"fact_ids"',
    '"hypothesis_ids"',
    '"unknown_ids"',
    '"customer_action_ids"',
    '"prohibited_claim_ids"',
    '"presentation_requirements"',
    "Style precedence",
]

DECISION_PACKET_V2_CHAR_BUDGET = 5_000
REPLY_BRIEF_V2_CHAR_BUDGET = 1_800
CURRENT_TICKET_CHAR_BUDGET = 14_000
EVIDENCE_TICKET_CHAR_BUDGET = 10_000

ROUTED_MODULE_MARKERS = {
    "회사규정/_라우팅.md": ["A `draft` card is a cited review artifact"],
    "플레이북/근거_검증.md": [
        "confirmed",
        "hypothesis",
        "unknown",
        "Treat the reply as a draft until a human reviews and sends it",
    ],
    "플레이북/회신_작성_규칙.md": [
        "Only a human sends email or posts to Zendesk",
        "Validate meaning, not sentence shape",
        "Every definitive statement is supported by a `confirmed` Decision Packet item",
    ],
    "플레이북/인프라_작업_프로세스.md": ["Stop at the human gate", "Design rollback first"],
    "연계/README.md": ["Verify the returned repository, branch, commit, command, and output"],
    "템플릿/티켓.md": ["Never rewrite prior judgment"],
    "템플릿/고객_프로필.md": ["Never record personality judgments"],
    "템플릿/티켓_근거.md": ["reuse_policy: current-ticket", "Re-fetch only"],
    "템플릿/티켓_이력.md": ["load_policy: on-demand", "Append only"],
}

ALWAYS_ON_CHAR_BUDGETS = {
    "CLAUDE.md": 4_500,
    "AGENTS.md": 1_800,
    ".kiro/steering/00-repository-rules.md": 1_800,
}
AGENTS_CLAUDE_COMBINED_CHAR_BUDGET = 6_000

ENTRYPOINT_MARKERS = {
    "AGENTS.md": ["CLAUDE.md", "에이전트/작업_라우터.md", "FitCloud", "회사규정/_라우팅.md", "연계/README.md", "에이전트/런타임_상태.md"],
    ".kiro/steering/00-repository-rules.md": [
        "CLAUDE.md",
        "에이전트/작업_라우터.md",
        "FitCloud",
        "회사규정/_라우팅.md",
        "연계/README.md",
        "에이전트/런타임_상태.md",
    ],
}

FRONTMATTER_FILES = [
    "회사규정/카드/_템플릿.md",
    "연계/템플릿/PoC_의뢰서.md",
    "연계/템플릿/PoC_결과서.md",
    "템플릿/고객_프로필.md",
    "템플릿/티켓.md",
    "템플릿/티켓_근거.md",
    "템플릿/티켓_이력.md",
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
DEIDENTIFICATION_SCAN_EXCLUSIONS = {
    "회사규정/sources.json",
    "회사규정/원본_목록.md",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


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


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative_parts = path.relative_to(ROOT).parts
        if ".git" in relative_parts or ".private" in relative_parts:
            continue
        files.append(path)
    return files


def validate_policy_cards(errors: list[str]) -> tuple[int, int]:
    inventory = read_text("회사규정/원본_목록.md", errors)
    routing = read_text("회사규정/_라우팅.md", errors)
    manifest_content = read_text("회사규정/sources.json", errors)
    try:
        manifest = json.loads(manifest_content)
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid 회사규정/sources.json: {exc}")
        manifest = {"sources": []}
    source_entries = manifest.get("sources", [])
    sources_by_id = {entry.get("id"): entry for entry in source_entries if entry.get("id")}
    if len(sources_by_id) != len(source_entries):
        fail(errors, "duplicate or missing source id in 회사규정/sources.json")
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
    cards = sorted((ROOT / "회사규정/카드").glob("*.md"))
    cards = [card for card in cards if card.name != "_템플릿.md"]

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

    for reference in re.findall(r"`(카드/[^`]+\.md)`", routing):
        if not (ROOT / "회사규정" / reference).is_file():
            fail(errors, f"routing references missing card: {reference}")

    if (ROOT / ".git").is_dir():
        result = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-files", "회사규정/수신함"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        tracked_raw = [
            line
            for line in result.stdout.splitlines()
            if line and line != "회사규정/수신함/README.md"
        ]
        if tracked_raw:
            fail(errors, f"raw inbox files are tracked: {', '.join(tracked_raw)}")

    raw_dir = ROOT / "회사규정/수신함"
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


def _decision_contract_sections(
    relative: str,
    ticket_content: str,
    errors: list[str],
) -> tuple[str, str] | None:
    packet_match = re.search(r"^## 결정 패킷\s*$", ticket_content, re.MULTILINE)
    brief_match = re.search(r"^## 회신 브리프\s*$", ticket_content, re.MULTILINE)
    reply_match = re.search(r"^## 회신\s*$", ticket_content, re.MULTILINE)
    packet_start = packet_match.start() if packet_match else -1
    brief_start = brief_match.start() if brief_match else -1
    reply_start = reply_match.start() if reply_match else -1
    if min(packet_start, brief_start, reply_start) < 0:
        fail(errors, f"decision-packet ticket missing required section: {relative}")
        return None
    if not packet_start < brief_start < reply_start:
        fail(errors, f"decision-packet ticket sections out of order: {relative}")
        return None
    return (
        ticket_content[packet_start:brief_start],
        ticket_content[brief_start:reply_start],
    )


def _validate_decision_packet_v1(
    relative: str,
    packet_section: str,
    brief_section: str,
    errors: list[str],
) -> None:
    for marker in [
        "version: 1",
        "tier:",
        "question:",
        "decisions:",
        "facts:",
        "hypotheses:",
        "unknowns:",
        "policy_ids:",
        "customer_actions:",
        "internal_actions:",
        "must_not_claim:",
    ]:
        if marker not in packet_section:
            fail(errors, f"{relative} decision packet missing field: {marker}")
    for marker in [
        "version: 1",
        "audience:",
        "goal:",
        "fact_ids:",
        "hypothesis_ids:",
        "unknown_ids:",
        "must_include:",
        "avoid:",
    ]:
        if marker not in brief_section:
            fail(errors, f"{relative} reply brief missing field: {marker}")


def _latest_v2_json(
    relative: str,
    label: str,
    section: str,
    errors: list[str],
) -> tuple[dict[str, object], str] | None:
    blocks = re.findall(r"```json\s*\n(.*?)\n```", section, re.DOTALL)
    for raw in reversed(blocks):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, f"{relative} latest {label} JSON is invalid: {exc}")
            return None
        if isinstance(parsed, dict) and parsed.get("version") == 2:
            return parsed, raw
    fail(errors, f"{relative} missing {label} v2 JSON block")
    return None


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


def _defined_evidence_ids(ticket_content: str, prefix: str) -> set[str]:
    bracketed = set(re.findall(rf"\[({prefix}\d+)\]", ticket_content))
    legacy = set(re.findall(rf"\bid:\s*({prefix}\d+)\b", ticket_content))
    return bracketed | legacy


def _validate_decision_packet_v2(
    relative: str,
    ticket_content: str,
    evidence_content: str,
    packet_section: str,
    brief_section: str,
    errors: list[str],
) -> None:
    packet_result = _latest_v2_json(relative, "Decision Packet", packet_section, errors)
    brief_result = _latest_v2_json(relative, "Reply Brief", brief_section, errors)
    if not packet_result or not brief_result:
        return
    packet, packet_raw = packet_result
    brief, brief_raw = brief_result
    if len(packet_raw) > DECISION_PACKET_V2_CHAR_BUDGET:
        fail(errors, f"{relative} Decision Packet v2 exceeds character budget")
    if len(brief_raw) > REPLY_BRIEF_V2_CHAR_BUDGET:
        fail(errors, f"{relative} Reply Brief v2 exceeds character budget")

    for key in ["tier", "question", "decisions", "policy_ids", "actions", "prohibited_claims"]:
        if key not in packet:
            fail(errors, f"{relative} Decision Packet v2 missing key: {key}")
    if packet.get("tier") not in {"quick", "standard", "high-risk"}:
        fail(errors, f"{relative} Decision Packet v2 has invalid tier")
    if not isinstance(packet.get("question"), str) or not packet.get("question"):
        fail(errors, f"{relative} Decision Packet v2 has empty question")

    evidence_ids = {
        prefix: _defined_evidence_ids(ticket_content + "\n" + evidence_content, prefix)
        for prefix in ["F", "H", "U"]
    }
    decisions_value = packet.get("decisions")
    if not isinstance(decisions_value, list) or not decisions_value:
        fail(errors, f"{relative} Decision Packet v2 decisions must be a non-empty list")
        decisions_value = []
    decisions: dict[str, dict[str, object]] = {}
    for index, value in enumerate(decisions_value, 1):
        owner = f"decision[{index}]"
        if not isinstance(value, dict):
            fail(errors, f"{relative} {owner} must be an object")
            continue
        decision_id = value.get("id")
        if not isinstance(decision_id, str) or not re.fullmatch(r"D\d+", decision_id):
            fail(errors, f"{relative} {owner} has invalid id")
            continue
        if decision_id in decisions:
            fail(errors, f"{relative} duplicate decision ID: {decision_id}")
        decisions[decision_id] = value
        for key in ["item", "result", "certainty", "conditions", "fact_ids", "hypothesis_ids", "unknown_ids"]:
            if key not in value:
                fail(errors, f"{relative} {decision_id} missing key: {key}")
        result = value.get("result")
        certainty = value.get("certainty")
        if not isinstance(value.get("item"), str) or not value.get("item"):
            fail(errors, f"{relative} {decision_id} has empty item")
        if result not in {"yes", "no", "conditional", "unknown"}:
            fail(errors, f"{relative} {decision_id} has invalid result")
        if certainty not in {"confirmed", "hypothesis", "unknown"}:
            fail(errors, f"{relative} {decision_id} has invalid certainty")
        conditions = value.get("conditions")
        if not isinstance(conditions, list) or any(not isinstance(item, str) for item in conditions):
            fail(errors, f"{relative} {decision_id} conditions must be a string list")
            conditions = []
        refs = {
            "F": _string_id_list(relative, f"{decision_id}.fact_ids", value.get("fact_ids"), r"F\d+", errors),
            "H": _string_id_list(relative, f"{decision_id}.hypothesis_ids", value.get("hypothesis_ids"), r"H\d+", errors),
            "U": _string_id_list(relative, f"{decision_id}.unknown_ids", value.get("unknown_ids"), r"U\d+", errors),
        }
        for prefix, ids in refs.items():
            for ref in ids:
                if ref not in evidence_ids[prefix]:
                    fail(errors, f"{relative} {decision_id} references undefined evidence ID: {ref}")
        if certainty == "confirmed" and refs["H"]:
            fail(errors, f"{relative} confirmed {decision_id} must not reference hypotheses")
        if certainty == "hypothesis" and not refs["H"]:
            fail(errors, f"{relative} hypothesis {decision_id} requires an H ID")
        if result == "unknown" and not refs["U"]:
            fail(errors, f"{relative} unknown {decision_id} requires a U ID")
        if result == "conditional" and not conditions:
            fail(errors, f"{relative} conditional {decision_id} requires conditions")

    policy_ids = packet.get("policy_ids")
    if not isinstance(policy_ids, list) or any(
        not isinstance(item, str) or not re.fullmatch(r"(?:POLICY|GUIDE)-[A-Z0-9-]+", item)
        for item in policy_ids
    ):
        fail(errors, f"{relative} Decision Packet v2 policy_ids is invalid")

    actions = packet.get("actions")
    if not isinstance(actions, dict):
        fail(errors, f"{relative} Decision Packet v2 actions must be an object")
        actions = {}
    action_ids: dict[str, set[str]] = {"customer": set(), "internal": set()}
    for kind, pattern in [("customer", r"A\d+"), ("internal", r"I\d+")]:
        values = actions.get(kind, [])
        if not isinstance(values, list):
            fail(errors, f"{relative} actions.{kind} must be a list")
            values = []
        for value in values:
            if not isinstance(value, dict) or not re.fullmatch(pattern, str(value.get("id", ""))):
                fail(errors, f"{relative} actions.{kind} has invalid item")
                continue
            action_id = str(value["id"])
            if action_id in action_ids[kind]:
                fail(errors, f"{relative} duplicate action ID: {action_id}")
            action_ids[kind].add(action_id)
            if not isinstance(value.get("action"), str) or not value.get("action"):
                fail(errors, f"{relative} {action_id} has empty action")

    prohibited_value = packet.get("prohibited_claims")
    if not isinstance(prohibited_value, list):
        fail(errors, f"{relative} prohibited_claims must be a list")
        prohibited_value = []
    prohibited_ids: set[str] = set()
    for value in prohibited_value:
        if not isinstance(value, dict) or not re.fullmatch(r"P\d+", str(value.get("id", ""))):
            fail(errors, f"{relative} prohibited_claims has invalid item")
            continue
        claim_id = str(value["id"])
        if claim_id in prohibited_ids:
            fail(errors, f"{relative} duplicate prohibited claim ID: {claim_id}")
        prohibited_ids.add(claim_id)
        if not isinstance(value.get("claim"), str) or not value.get("claim"):
            fail(errors, f"{relative} {claim_id} has empty claim")

    for key in [
        "audience",
        "goal",
        "decision_ids",
        "fact_ids",
        "hypothesis_ids",
        "unknown_ids",
        "customer_action_ids",
        "internal_action_ids",
        "prohibited_claim_ids",
        "presentation",
        "presentation_requirements",
        "avoid_topics",
    ]:
        if key not in brief:
            fail(errors, f"{relative} Reply Brief v2 missing key: {key}")
    for legacy_key in ["must_include", "optional", "avoid"]:
        if legacy_key in brief:
            fail(errors, f"{relative} Reply Brief v2 uses legacy free-text key: {legacy_key}")
    decision_ids = _string_id_list(relative, "brief.decision_ids", brief.get("decision_ids"), r"D\d+", errors)
    if not decision_ids:
        fail(errors, f"{relative} Reply Brief v2 must select at least one decision")
    brief_refs = {
        "F": _string_id_list(relative, "brief.fact_ids", brief.get("fact_ids"), r"F\d+", errors),
        "H": _string_id_list(relative, "brief.hypothesis_ids", brief.get("hypothesis_ids"), r"H\d+", errors),
        "U": _string_id_list(relative, "brief.unknown_ids", brief.get("unknown_ids"), r"U\d+", errors),
    }
    for decision_id in decision_ids:
        if decision_id not in decisions:
            fail(errors, f"{relative} Reply Brief references undefined decision ID: {decision_id}")
    for prefix, ids in brief_refs.items():
        for ref in ids:
            if ref not in evidence_ids[prefix]:
                fail(errors, f"{relative} Reply Brief references undefined evidence ID: {ref}")

    selected = [decisions[item] for item in decision_ids if item in decisions]
    selected_refs: dict[str, set[str]] = {"F": set(), "H": set(), "U": set()}
    for item in selected:
        for prefix, key in [("F", "fact_ids"), ("H", "hypothesis_ids"), ("U", "unknown_ids")]:
            values = item.get(key)
            if isinstance(values, list):
                selected_refs[prefix].update(
                    value for value in values if isinstance(value, str)
                )
    for prefix, label in [("F", "facts"), ("H", "hypotheses"), ("U", "unknowns")]:
        if not set(brief_refs[prefix]).issubset(selected_refs[prefix]):
            fail(errors, f"{relative} Reply Brief selects {label} outside selected decisions")
    for prefix, label in [("H", "hypotheses"), ("U", "blocking unknowns")]:
        if not selected_refs[prefix].issubset(set(brief_refs[prefix])):
            fail(errors, f"{relative} Reply Brief omits selected decision {label}")

    customer_action_ids = _string_id_list(
        relative, "brief.customer_action_ids", brief.get("customer_action_ids"), r"A\d+", errors
    )
    internal_action_ids = _string_id_list(
        relative, "brief.internal_action_ids", brief.get("internal_action_ids"), r"I\d+", errors
    )
    prohibited_claim_ids = _string_id_list(
        relative, "brief.prohibited_claim_ids", brief.get("prohibited_claim_ids"), r"P\d+", errors
    )
    for ref in customer_action_ids:
        if ref not in action_ids["customer"]:
            fail(errors, f"{relative} Reply Brief references undefined customer action: {ref}")
    for ref in internal_action_ids:
        if ref not in action_ids["internal"]:
            fail(errors, f"{relative} Reply Brief references undefined internal action: {ref}")
    if not prohibited_ids.issubset(set(prohibited_claim_ids)):
        fail(errors, f"{relative} Reply Brief omits prohibited claims")

    audience = brief.get("audience")
    if not isinstance(audience, dict) or audience.get("technical_depth") not in {
        "concise",
        "standard",
        "detailed",
    }:
        fail(errors, f"{relative} Reply Brief v2 has invalid audience")
    presentation = brief.get("presentation")
    if not isinstance(presentation, dict) or presentation.get("commands") not in {
        "none",
        "on-request",
        "inline",
    }:
        fail(errors, f"{relative} Reply Brief v2 has invalid presentation")
    for key in ["presentation_requirements", "avoid_topics"]:
        values = brief.get(key)
        if not isinstance(values, list) or any(
            not isinstance(item, str) for item in values
        ):
            fail(errors, f"{relative} Reply Brief v2 {key} must be a string list")

    body, separator, sources = ticket_content.partition("## Sources")
    cited = {int(value) for value in re.findall(r"\[(\d+)\]", body)}
    listed = {
        int(value)
        for value in re.findall(r"^\[(\d+)\]\s+https?://", sources, re.MULTILINE)
    }
    if cited - listed:
        fail(errors, f"{relative} has citations missing from Sources: {sorted(cited - listed)}")
    if separator and listed - cited:
        fail(errors, f"{relative} has unused Sources: {sorted(listed - cited)}")


def validate_decision_packet_ticket(
    relative: str,
    ticket_content: str,
    errors: list[str],
    evidence_content: str = "",
) -> None:
    version_match = re.search(
        r"^decision_packet_version:\s*(\d+)\s*$",
        ticket_content,
        re.MULTILINE,
    )
    if not version_match:
        return
    version = int(version_match.group(1))
    sections = _decision_contract_sections(relative, ticket_content, errors)
    if not sections:
        return
    packet_section, brief_section = sections
    if version == 1:
        _validate_decision_packet_v1(relative, packet_section, brief_section, errors)
    elif version == 2:
        _validate_decision_packet_v2(
            relative,
            ticket_content,
            evidence_content,
            packet_section,
            brief_section,
            errors,
        )
    else:
        fail(errors, f"{relative} has unsupported decision_packet_version: {version}")


def validate_deidentified_repository(errors: list[str]) -> None:
    customer_root = ROOT / "고객"
    for path in customer_root.iterdir():
        if path.is_dir() and not re.fullmatch(r"CUST-\d{3,}", path.name):
            fail(errors, f"customer directory is not de-identified: 고객/{path.name}")
        if path.is_dir():
            profile = path / "프로필.md"
            if not profile.is_file():
                fail(errors, f"customer profile missing: 고객/{path.name}/프로필.md")
                continue
            profile_content = profile.read_text(encoding="utf-8")
            if not re.search(
                r"^contract_baseline:\s*SRC-FITCLOUD-TERMS-001\s*$",
                profile_content,
                re.MULTILINE,
            ):
                fail(errors, f"customer profile missing standard contract baseline: 고객/{path.name}/프로필.md")
            if not re.search(r"^contract_exceptions:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing contract_exceptions: 고객/{path.name}/프로필.md")
            payer_match = re.search(
                r"^payer_model:\s*(standalone|integrated|other|unknown)(?:\s+#.*)?$",
                profile_content,
                re.MULTILINE,
            )
            if not payer_match:
                fail(errors, f"customer profile missing valid payer_model: 고객/{path.name}/프로필.md")
            if not re.search(r"^payer_verified_at:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing payer_verified_at: 고객/{path.name}/프로필.md")
            coc_owner_match = re.search(
                r"^coc_owner_ref:\s*(?:\"\"|CONTACT-\d{3,})(?:\s+#.*)?$",
                profile_content,
                re.MULTILINE,
            )
            if not coc_owner_match:
                fail(errors, f"customer profile missing valid coc_owner_ref: 고객/{path.name}/프로필.md")
            if not re.search(r"^coc_roster_verified_at:\s*.*$", profile_content, re.MULTILINE):
                fail(errors, f"customer profile missing coc_roster_verified_at: 고객/{path.name}/프로필.md")

            ticket_dir = path / "티켓"
            if ticket_dir.is_dir():
                legacy_tickets = sorted(ticket_dir.glob("*.md"))
                for legacy in legacy_tickets:
                    fail(errors, f"legacy monolithic ticket remains: {legacy.relative_to(ROOT)}")
                for case_dir in sorted(item for item in ticket_dir.iterdir() if item.is_dir()):
                    required = {
                        "current": case_dir / "current.md",
                        "evidence": case_dir / "evidence.md",
                        "history": case_dir / "history.md",
                    }
                    missing = [name for name, item in required.items() if not item.is_file()]
                    if missing:
                        fail(
                            errors,
                            f"ticket directory missing {', '.join(missing)}: {case_dir.relative_to(ROOT)}",
                        )
                        continue
                    current_content = required["current"].read_text(encoding="utf-8")
                    evidence_content = required["evidence"].read_text(encoding="utf-8")
                    history_content = required["history"].read_text(encoding="utf-8")
                    relative = str(required["current"].relative_to(ROOT))
                    if len(current_content) > CURRENT_TICKET_CHAR_BUDGET:
                        fail(errors, f"current ticket exceeds character budget: {relative}")
                    if len(evidence_content) > EVIDENCE_TICKET_CHAR_BUDGET:
                        fail(errors, f"ticket evidence exceeds character budget: {required['evidence'].relative_to(ROOT)}")
                    for marker in [
                        "decision_packet_version: 2",
                        "current_revision:",
                        "evidence_file: evidence.md",
                        "history_file: history.md",
                        "## 현재 상태",
                        "## 파일 연결",
                    ]:
                        if marker not in current_content:
                            fail(errors, f"{relative} missing current-state marker: {marker}")
                    if re.search(r"초안 v\d+.*대체됨", current_content):
                        fail(errors, f"current ticket contains superseded draft history: {relative}")
                    for marker in ["reuse_policy: current-ticket", "## 재검증 trigger"]:
                        if marker not in evidence_content:
                            fail(errors, f"{required['evidence'].relative_to(ROOT)} missing reuse marker: {marker}")
                    if "load_policy: on-demand" not in history_content:
                        fail(errors, f"{required['history'].relative_to(ROOT)} missing on-demand load policy")
                    archive_hash_match = re.search(
                        r"^archived_source_sha256:\s*([0-9a-f]{64})\s*$",
                        history_content,
                        re.MULTILINE,
                    )
                    archive_marker = "## Archived monolithic snapshot through v4\n\n"
                    if archive_hash_match:
                        if archive_marker not in history_content:
                            fail(errors, f"{required['history'].relative_to(ROOT)} missing archive marker")
                        else:
                            archived = history_content.split(archive_marker, 1)[1]
                            digest = hashlib.sha256(archived.encode("utf-8")).hexdigest()
                            if digest != archive_hash_match.group(1):
                                fail(errors, f"archived ticket snapshot hash changed: {required['history'].relative_to(ROOT)}")
                    validate_decision_packet_ticket(
                        relative,
                        current_content,
                        errors,
                        evidence_content=evidence_content,
                    )

    profile_template = read_text("템플릿/고객_프로필.md", errors)
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

    ticket_template = read_text("템플릿/티켓.md", errors)
    for marker in [
        "decision_packet_version: 2",
        "current_revision:",
        "evidence_file: evidence.md",
        "history_file: history.md",
        "## 현재 상태",
        "## 파일 연결",
    ]:
        if marker not in ticket_template:
            fail(errors, f"current ticket template missing marker: {marker}")
    evidence_template = read_text("템플릿/티켓_근거.md", errors)
    for marker in ["reuse_policy: current-ticket", "[F1]", "[H1]", "[U1]", "reverify_when:"]:
        if marker not in evidence_template:
            fail(errors, f"ticket evidence template missing marker: {marker}")
    history_template = read_text("템플릿/티켓_이력.md", errors)
    for marker in ["load_policy: on-demand", "Append only", "실제 발송/고객 회신"]:
        if marker not in history_template:
            fail(errors, f"ticket history template missing marker: {marker}")

    retention_hierarchy = (
        "law/legal obligation → customer-specific contract/SLA/SOW → "
        "active standard terms → active Offboarding guide"
    )
    for relative in [
        "회사규정/카드/POLICY-DATA-001-contract-termination-data-lifecycle.md",
        "회사규정/카드/POLICY-OFFBOARD-001-customer-approval-and-data-handling.md",
    ]:
        if retention_hierarchy not in read_text(relative, errors):
            fail(errors, f"retention hierarchy missing from {relative}")

    payer_card = read_text("회사규정/카드/POLICY-PAYER-001-standalone-payer-scope.md", errors)
    for marker in ["CSR", "COP", "FitCloud"]:
        if marker not in payer_card:
            fail(errors, f"standalone-Payer verification rule missing: {marker}")

    for path in iter_text_files():
        relative = str(path.relative_to(ROOT))
        if relative.startswith("회사규정/수신함/") or relative in DEIDENTIFICATION_SCAN_EXCLUSIONS:
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in TRACKED_CUSTOMER_IDENTIFIER_PATTERNS.items():
            if pattern.search(content):
                fail(
                    errors,
                    f"possible tracked customer {label}: {relative}; value intentionally not printed",
                )

    if (ROOT / ".git").is_dir():
        result = subprocess.run(
            ["git", "check-ignore", "-q", ".private/customer-map.md"],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            fail(errors, ".private/customer-map.md is not gitignored")


def main() -> int:
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

    task_router = read_text("에이전트/작업_라우터.md", errors)
    for marker in TASK_ROUTER_MARKERS:
        if marker not in task_router:
            fail(errors, f"task router missing marker: {marker}")

    for relative, markers in {
        "템플릿/결정_패킷.md": DECISION_PACKET_TEMPLATE_MARKERS,
        "템플릿/회신_브리프.md": REPLY_BRIEF_TEMPLATE_MARKERS,
    }.items():
        content = read_text(relative, errors)
        for marker in markers:
            if marker not in content:
                fail(errors, f"{relative} missing semantic contract marker: {marker}")

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

    runtime_status = read_text("에이전트/런타임_상태.md", errors)
    for marker in [
        "`customer-aws-readonly` | blocked",
        "`fitcloud-billing` | blocked",
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
        "회사규정/원본/",
        "회사규정/수신함/*",
        "!회사규정/수신함/README.md",
        "terraform.tfstate",
        "*.kubeconfig",
    ]:
        if marker not in gitignore:
            fail(errors, f".gitignore missing safety rule: {marker}")

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
    print("- templates: frontmatter present")
    print(
        "- decision contract: v1 compatible; v2 JSON graph checks enabled "
        f"(packet {DECISION_PACKET_V2_CHAR_BUDGET}, brief {REPLY_BRIEF_V2_CHAR_BUDGET} chars)"
    )
    print(
        "- ticket storage: current/evidence/history selective load "
        f"(current {CURRENT_TICKET_CHAR_BUDGET}, evidence {EVIDENCE_TICKET_CHAR_BUDGET} chars)"
    )
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
