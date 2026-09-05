#!/usr/bin/env python3
"""onboarding.sh 와 onboarding.ps1 이 어긋나지 않는지 검사한다.

두 스크립트는 서로 다른 OS 를 담당하므로 한쪽만 고치고 다른 쪽을 잊기 쉽다.
saltware-csg-skills 에서 install.ps1 이 install.sh 의 파일 목록 두 개를 빠뜨린 채
배포돼 Windows 설치가 통째로 깨진 사고가 있었고, 그걸 잡는 테스트가 없어서
CI 를 그냥 통과했다. 같은 사고를 막는다.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SH = ROOT / "scripts/onboarding.sh"
PS1 = ROOT / "scripts/onboarding.ps1"
FETCH_SH = ROOT / "scripts/fetch-ticket.sh"
FETCH_PS1 = ROOT / "scripts/fetch-ticket.ps1"

BLOCK = re.compile(r"# STEPS-PARITY-START(.*?)# STEPS-PARITY-END", re.S)


def steps(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = BLOCK.search(text)
    if match is None:
        raise AssertionError(f"STEPS-PARITY 블록이 없다: {path.name}")
    return re.findall(r'"([^"]+)"', match.group(1))


class OnboardingParityTests(unittest.TestCase):
    def test_both_scripts_exist(self) -> None:
        for path in (SH, PS1):
            self.assertTrue(path.is_file(), f"없음: {path}")

    def test_step_lists_are_identical_and_ordered(self) -> None:
        """단계 이름과 순서가 같아야 한다. 순서가 다르면 사용자 경험이 갈린다."""
        self.assertEqual(steps(SH), steps(PS1))

    def test_step_count_matches_progress_labels(self) -> None:
        """'[1/4]' 같은 진행 표시가 실제 단계 수와 맞아야 한다."""
        for path in (SH, PS1):
            declared = len(steps(path))
            labels = set(re.findall(r"(\d+)/(\d+)", path.read_text(encoding="utf-8")))
            totals = {int(total) for _, total in labels}
            self.assertIn(
                declared, totals, f"{path.name}: 단계 {declared}개인데 진행 표시는 {totals}"
            )

    def test_both_use_the_same_config_path(self) -> None:
        """설정 경로가 갈리면 OS 를 옮겼을 때 자격증명을 다시 넣어야 한다."""
        for path in (SH, PS1):
            text = path.read_text(encoding="utf-8")
            self.assertIn(".config/saltware", text, f"{path.name}: 공통 설정 경로를 안 쓴다")
            self.assertIn("zendesk.conf", text)

    def test_both_declare_the_same_conf_keys(self) -> None:
        keys = {"ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"}
        for path in (SH, PS1):
            text = path.read_text(encoding="utf-8")
            for key in keys:
                self.assertIn(key, text, f"{path.name}: {key} 누락")

    def test_neither_touches_a_shell_profile(self) -> None:
        """셸 프로필을 건드리면 그 셸을 안 쓰는 사람에게서 조용히 실패한다."""
        for path in (SH, PS1):
            text = path.read_text(encoding="utf-8")
            for profile in (".zshenv", ".zshrc", ".bashrc", ".bash_profile", "$PROFILE"):
                # 주석에서 '안 건드린다'고 설명하는 건 허용, 실제 쓰기는 금지.
                for line in text.splitlines():
                    stripped = line.strip()
                    if profile in stripped and not stripped.startswith("#"):
                        self.fail(f"{path.name}: 셸 프로필 참조: {stripped}")

    def test_token_input_is_hidden_in_both(self) -> None:
        self.assertIn("read -rs", SH.read_text(encoding="utf-8"))
        self.assertIn("-AsSecureString", PS1.read_text(encoding="utf-8"))

    def test_skipping_requires_an_explicit_word(self) -> None:
        """빈 Enter 로 건너뛰게 두면 대부분 그걸 누르고, 나중에 안 된다고 되돌아온다."""
        for path in (SH, PS1):
            text = path.read_text(encoding="utf-8")
            self.assertIn('"skip"', text, f"{path.name}: 명시적 skip 입력이 없다")
            self.assertIn("값이 필요하다", text, f"{path.name}: 빈 입력 재질문이 없다")

    def test_email_prompt_is_not_called_agent_email(self) -> None:
        """이 저장소에서 '에이전트'는 AI 도구다. Zendesk 의 agent(상담원)와 겹치면
        읽는 사람이 자기 이메일을 넣는 자리인지 알 수 없다."""
        for path in (SH, PS1):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("에이전트 이메일", text, f"{path.name}: 모호한 라벨")
            self.assertIn("Zendesk 로그인 이메일", text, f"{path.name}: 명확한 라벨이 없다")

    def test_both_support_a_non_interactive_check_mode(self) -> None:
        self.assertIn("--check", SH.read_text(encoding="utf-8"))
        self.assertIn("$Check", PS1.read_text(encoding="utf-8"))


class FetchTicketParityTests(unittest.TestCase):
    """fetch-ticket 의 .sh 와 .ps1 이 같은 계약을 지키는지 본다."""

    def test_both_scripts_exist(self) -> None:
        for path in (FETCH_SH, FETCH_PS1):
            self.assertTrue(path.is_file(), f"없음: {path}")

    def test_both_read_the_same_conf_file(self) -> None:
        for path in (FETCH_SH, FETCH_PS1):
            text = path.read_text(encoding="utf-8")
            self.assertIn(".config/saltware/zendesk.conf", text, f"{path.name}: conf 경로 불일치")

    def test_both_resolve_the_same_setting_names(self) -> None:
        """우리 이름과 외부 스킬 호환 이름을 양쪽 다 받아야 한다."""
        for path in (FETCH_SH, FETCH_PS1):
            text = path.read_text(encoding="utf-8")
            for key in ("ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"):
                self.assertIn(key, text, f"{path.name}: {key} 누락")
            for legacy in ("Zendesk_SUBDOMAIN", "Zendesk_EMAIL", "Zendesk_API"):
                self.assertIn(legacy, text, f"{path.name}: 호환 이름 {legacy} 누락")

    def test_both_follow_pagination(self) -> None:
        """코멘트 100건이 넘는 스레드가 잘리면 답변이 통째로 틀어진다."""
        for path in (FETCH_SH, FETCH_PS1):
            text = path.read_text(encoding="utf-8")
            self.assertIn("has_more", text, f"{path.name}: cursor 페이지네이션 미처리")
            self.assertIn("next_page", text, f"{path.name}: offset 폴백 미처리")

    def test_both_support_json_output(self) -> None:
        self.assertIn("--json", FETCH_SH.read_text(encoding="utf-8"))
        self.assertIn("$Json", FETCH_PS1.read_text(encoding="utf-8"))

    def test_both_count_inline_body_images_not_just_attachments(self) -> None:
        """Zendesk 는 본문에 붙여넣은 이미지를 attachments 에 안 넣기도 한다.
        attachments 만 세면 이미지 4장짜리 티켓이 '첨부 없음'으로 보인다 —
        읽는 쪽이 자기가 뭘 못 봤는지 모르게 되는 게 이 검사가 막는 것이다."""
        for path in (FETCH_SH, FETCH_PS1):
            text = path.read_text(encoding="utf-8")
            self.assertIn("/attachments/token/", text, f"{path.name}: 본문 이미지 URL 탐지 없음")
            self.assertIn("본문 삽입", text, f"{path.name}: 인라인 개수를 따로 안 알림")

    def test_both_download_images_only_on_demand(self) -> None:
        for path, flag in ((FETCH_SH, "--images"), (FETCH_PS1, "-Images")):
            self.assertIn(flag, path.read_text(encoding="utf-8"), f"{path.name}: {flag} 없음")

    def test_credentials_go_only_to_our_own_zendesk_host(self) -> None:
        """티켓 본문에는 고객사 헬프데스크 URL 이 섞여 있다. 거기로 Authorization 을
        보내면 우리 Zendesk 토큰을 제3자에게 넘기는 것이 된다."""
        sh = FETCH_SH.read_text(encoding="utf-8")
        self.assertIn('grep -q "^https://${HOST}/"', sh, "sh: 호스트 검사 없이 인증 전송")
        ps = FETCH_PS1.read_text(encoding="utf-8")
        self.assertIn('StartsWith("https://$zdHost/")', ps, "ps1: 호스트 검사 없이 인증 전송")

    def test_neither_writes_the_thread_to_disk(self) -> None:
        """원본 스레드에는 실명·계정ID가 들어 있다. 어디에 남길지는 호출자가 정한다."""
        for path in (FETCH_SH, FETCH_PS1):
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for bad in ("Out-File", "Set-Content", "tee "):
                    self.assertNotIn(bad, stripped, f"{path.name}: 디스크 기록: {stripped}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
