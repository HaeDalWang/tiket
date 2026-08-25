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
]

CANONICAL_MARKERS = [
    "Customer-facing cost figures must be FitCloud-curated",
    "Never print or commit credentials",
    "PoC cross-project handoff",
    "Company policy retrieval",
    "Customer relationships and identity",
    "Append-only decision history",
    "Commit only de-identified customer context until security approval",
    "standard terms as the default contract baseline",
    "law/legal obligation → customer-specific contract/SLA/SOW → active standard terms → active Offboarding guide",
    "Use the standalone-Payer guide only for concepts, role boundaries, and general constraints",
    "Roadmap items are never current capability evidence",
    "Use the COC Raw guide only for role and procedure candidates",
    "A card whose review date has passed, is missing, or is `TBD` remains `draft`",
    "The shared TS remote-support PC/account procedure recorded in the Raw notes is retired",
    "aws-customer-account-ops` is temporarily blocked",
    "Hermes `aws-docs` is documentation-only",
    "Hermes Exa uses the official hosted MCP anonymously",
    "web_search_exa` and `web_fetch_exa` only",
]

ENTRYPOINT_MARKERS = {
    "AGENTS.md": ["CLAUDE.md", "FitCloud", "회사규정/_라우팅.md", "연계/README.md", "에이전트/런타임_상태.md"],
    ".kiro/steering/00-repository-rules.md": [
        "CLAUDE.md",
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

        for source_id in set(re.findall(r"SRC-[A-Z0-9-]+", content)):
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
        expected_names = {entry.get("filename_nfc") for entry in source_entries}
        extra_names = sorted(set(raw_by_nfc) - expected_names)
        if extra_names:
            fail(errors, f"unregistered raw source files: {', '.join(extra_names)}")
        for source_id, entry in sources_by_id.items():
            filename = entry.get("filename_nfc")
            path = raw_by_nfc.get(filename)
            if not path:
                fail(errors, f"manifest source file missing from inbox: {source_id} ({filename})")
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != entry.get("sha256"):
                fail(errors, f"source hash changed: {source_id} ({filename})")
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count != int(entry.get("lines", 0)):
                fail(
                    errors,
                    f"source line count changed: {source_id} expected {entry.get('lines')} got {line_count}",
                )
            verified_sources += 1

    return len(cards), verified_sources


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
        "Payer model / 확인일:",
        "CSR 계약 확인 reference:",
        "COP 현재 기능 확인 reference:",
        "FitCloud 실측 reference:",
    ]:
        if marker not in ticket_template:
            fail(errors, f"ticket template missing Payer verification field: {marker}")
    for marker in [
        "COC owner reference / 확인일시:",
        "FitCloud owner source reference:",
        "On-call roster source reference:",
    ]:
        if marker not in ticket_template:
            fail(errors, f"ticket template missing COC verification field: {marker}")
    for marker in ["보존/삭제 근거:", "보존/삭제 conflict 상태:", "CSR/법무 확인 reference:"]:
        if marker not in ticket_template:
            fail(errors, f"ticket template missing retention field: {marker}")

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

    canonical = read_text("CLAUDE.md", errors)
    if len(canonical) > 20_000:
        fail(errors, f"CLAUDE.md exceeds the 20,000-character context limit: {len(canonical)}")
    for marker in CANONICAL_MARKERS:
        if marker not in canonical:
            fail(errors, f"CLAUDE.md missing canonical marker: {marker}")

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
    print(f"- CLAUDE.md characters: {len(canonical)} / 20000")
    print("- entrypoints: AGENTS.md, Kiro steering")
    print("- templates: frontmatter present")
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
