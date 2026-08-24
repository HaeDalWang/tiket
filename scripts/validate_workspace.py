#!/usr/bin/env python3
"""Validate the customer-support workspace structure and safety invariants."""

from __future__ import annotations

import re
import sys
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
    "고객/_인덱스.md",
    "회사규정/README.md",
    "회사규정/_라우팅.md",
    "회사규정/카드/_템플릿.md",
    "회사규정/원본_목록.md",
    "회사규정/수신함/README.md",
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
]

ENTRYPOINT_MARKERS = {
    "AGENTS.md": ["CLAUDE.md", "FitCloud", "회사규정/_라우팅.md", "연계/README.md"],
    ".kiro/steering/00-repository-rules.md": [
        "CLAUDE.md",
        "FitCloud",
        "회사규정/_라우팅.md",
        "연계/README.md",
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
