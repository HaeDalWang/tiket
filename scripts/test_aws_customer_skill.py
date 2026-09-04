#!/usr/bin/env python3
"""Offline conformance tests for an installed aws-customer-account-ops skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

SKILL_NAME = "aws-customer-account-ops"
SYNTHETIC_ACCOUNT_ID = "123456" + "789012"
REQUIRED_FILES = (
    "SKILL.md",
    "get-sts-token.sh",
    "get-customer-credentials.sh",
    "fitcloud-api.sh",
    "self-update.sh",
)
# Syntax floor actually used by the skill's shell client, not a policy preference:
#   local -n (nameref)  -> 4.3
#   ${var,,}            -> 4.0
#   ;;& in case         -> 4.0
# macOS ships /bin/bash 3.2 and will not ship a newer one. The skill is owned by
# saltware-csg-skills, so this repository reports the gap instead of failing on it.
SKILL_BASH_FLOOR = (4, 3)
SKILL_OWNER = "정지우"


def probe_bash() -> tuple[str, tuple[int, ...] | None]:
    """Resolve bash the way the skill does (`#!/usr/bin/env bash`) and read its version."""
    binary = shutil.which("bash") or ""
    if not binary:
        return "", None
    result = subprocess.run(
        [binary, "-c", 'printf "%s %s" "${BASH_VERSINFO[0]}" "${BASH_VERSINFO[1]}"'],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return binary, None
    try:
        return binary, tuple(int(value) for value in result.stdout.split())
    except ValueError:
        return binary, None


def discover_skill_dir(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    home = Path.home()
    candidates = (
        home / ".hermes/skills" / SKILL_NAME,
        home / ".claude/skills" / SKILL_NAME,
        home / ".agents/skills" / SKILL_NAME,
        home / ".kiro/skills" / SKILL_NAME,
    )
    for candidate in candidates:
        if (candidate / "SKILL.md").is_file():
            return candidate.resolve()
    raise FileNotFoundError("installed aws-customer-account-ops skill not found")


class AwsCustomerSkillConformanceTests(unittest.TestCase):
    skill_dir: Path
    bash_bin: str
    bash_version: tuple[int, ...] | None

    @classmethod
    def configure(cls, skill_dir: Path) -> None:
        cls.skill_dir = skill_dir
        cls.bash_bin, cls.bash_version = probe_bash()

    @classmethod
    def setUpClass(cls) -> None:
        """Auto-configure for `python -m unittest discover`, which never calls main().

        main() calls configure() explicitly with the parsed --skill-dir before
        building the suite; this only fills in the gap when nothing configured
        it first, so an explicit main() call always wins.
        """
        if not hasattr(cls, "skill_dir"):
            try:
                cls.configure(discover_skill_dir(None))
            except FileNotFoundError as exc:
                raise unittest.SkipTest(str(exc))

    @classmethod
    def bash_meets_floor(cls) -> bool:
        return bool(cls.bash_bin) and cls.bash_version is not None and cls.bash_version >= SKILL_BASH_FLOOR

    def require_supported_bash(self) -> None:
        """Skip instead of fail: an unsupported bash is a skill-side limitation."""
        if not self.bash_meets_floor():
            self.skipTest("environment bash is below the skill's syntax floor")

    def script(self, name: str) -> Path:
        return self.skill_dir / name

    def isolated_env(self, home: Path, bin_dir: Path) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(home),
                "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}",
                "SALTWARE_DISABLE_UPDATE": "1",
                "SALTWARE_AGENT": "hermes",
            }
        )
        env.pop("FITCLOUD_API_KEY", None)
        return env

    def write_executable(self, path: Path, content: str) -> None:
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        path.chmod(0o755)

    def test_required_files_exist(self) -> None:
        missing = [name for name in REQUIRED_FILES if not self.script(name).is_file()]
        self.assertEqual(missing, [], f"missing required skill files: {missing}")

    def test_selected_bash_is_supported_by_the_skill(self) -> None:
        self.assertTrue(self.bash_bin, "bash is not available in the agent PATH")
        self.assertIsNotNone(self.bash_version, f"cannot read bash version: {self.bash_bin}")
        self.require_supported_bash()

    def test_shell_scripts_parse_with_selected_bash(self) -> None:
        self.require_supported_bash()
        for script in sorted(self.skill_dir.glob("*.sh")):
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [self.bash_bin, "-n", str(script)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_customer_client_has_no_local_assume_role_command(self) -> None:
        source = self.script("get-customer-credentials.sh").read_text(encoding="utf-8")
        command = re.compile(r"^[^#\n]*\baws\s+sts\s+assume-role\b", re.MULTILINE)
        self.assertIsNone(command.search(source), "customer client must not run local sts assume-role")
        self.assertIn("/customer-credentials", source)

    def test_missing_login_token_fails_fast_without_network(self) -> None:
        self.require_supported_bash()
        with tempfile.TemporaryDirectory(prefix="tiket-aws-skill-no-login-") as tempdir:
            root = Path(tempdir)
            home = root / "home"
            bin_dir = root / "bin"
            home.mkdir()
            bin_dir.mkdir()
            curl_log = root / "curl.log"
            self.write_executable(
                bin_dir / "curl",
                f"""
                #!/usr/bin/env bash
                printf 'called\n' >> {str(curl_log)!r}
                exit 99
                """,
            )
            env = self.isolated_env(home, bin_dir)
            started = time.monotonic()
            result = subprocess.run(
                [self.bash_bin, str(self.script("get-customer-credentials.sh")), "--account-id", SYNTHETIC_ACCOUNT_ID],
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=2,
            )
            elapsed = time.monotonic() - started
            self.assertNotEqual(result.returncode, 0)
            self.assertLess(elapsed, 2)
            self.assertIn("로그인이 필요합니다", result.stderr)
            self.assertFalse(curl_log.exists(), "missing-token path attempted a network call")

    def test_fitcloud_missing_key_fails_without_network(self) -> None:
        self.require_supported_bash()
        with tempfile.TemporaryDirectory(prefix="tiket-fitcloud-no-key-") as tempdir:
            root = Path(tempdir)
            home = root / "home"
            bin_dir = root / "bin"
            home.mkdir()
            bin_dir.mkdir()
            curl_log = root / "curl.log"
            self.write_executable(
                bin_dir / "curl",
                f"""
                #!/usr/bin/env bash
                printf 'called\n' >> {str(curl_log)!r}
                exit 99
                """,
            )
            result = subprocess.run(
                [self.bash_bin, str(self.script("fitcloud-api.sh")), "GET", "/api/synthetic"],
                env=self.isolated_env(home, bin_dir),
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FITCLOUD_API_KEY", result.stderr)
            self.assertFalse(curl_log.exists(), "missing-key path attempted a network call")

    def test_fitcloud_wrapper_passes_synthetic_bearer(self) -> None:
        self.require_supported_bash()
        with tempfile.TemporaryDirectory(prefix="tiket-fitcloud-header-") as tempdir:
            root = Path(tempdir)
            home = root / "home"
            bin_dir = root / "bin"
            home.mkdir()
            bin_dir.mkdir()
            curl_log = root / "curl.log"
            self.write_executable(
                bin_dir / "curl",
                f"""
                #!/usr/bin/env bash
                printf '%s\n' "$@" > {str(curl_log)!r}
                printf '{{"body":[]}}\n'
                """,
            )
            env = self.isolated_env(home, bin_dir)
            env["FITCLOUD_API_KEY"] = "synthetic-fitcloud-key"
            result = subprocess.run(
                [self.bash_bin, str(self.script("fitcloud-api.sh")), "GET", "/api/synthetic"],
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            invocation = curl_log.read_text(encoding="utf-8")
            self.assertIn("Authorization: Bearer synthetic-fitcloud-key", invocation)
            self.assertIn("https://aws.fitcloud.co.kr/api/synthetic", invocation)

    def test_customer_client_projects_synthetic_broker_response(self) -> None:
        self.require_supported_bash()
        with tempfile.TemporaryDirectory(prefix="tiket-customer-broker-") as tempdir:
            root = Path(tempdir)
            home = root / "home"
            bin_dir = root / "bin"
            config_dir = home / ".config/saltware"
            cache_dir = home / ".cache/saltware"
            config_dir.mkdir(parents=True)
            cache_dir.mkdir(parents=True)
            bin_dir.mkdir()

            (config_dir / "credential-broker.conf").write_text(
                "API_URL=https://broker.invalid/Prod/v1/credentials\n",
                encoding="utf-8",
            )
            (cache_dir / "sts-token.json").write_text(
                json.dumps(
                    {
                        "Version": 1,
                        "Expiration": "2099-01-01T00:00:00Z",
                        "SlackAccessToken": "synthetic-login-token",
                        "SlackUserId": "U-SYNTHETIC",
                    }
                ),
                encoding="utf-8",
            )

            curl_log = root / "curl.log"
            aws_log = root / "aws.log"
            self.write_executable(
                bin_dir / "curl",
                f"""
                #!/usr/bin/env bash
                printf '%s\n' "$@" > {str(curl_log)!r}
                out=''
                while (($#)); do
                    if [[ "$1" == '-o' ]]; then out="$2"; shift 2; else shift; fi
                done
                printf '%s' '{{"AccessKeyId":"synthetic-access","SecretAccessKey":"synthetic-secret","SessionToken":"synthetic-session","Expiration":"2099-01-01T00:00:00Z","BrokerVersion":"synthetic"}}' > "$out"
                printf '200'
                """,
            )
            self.write_executable(
                bin_dir / "aws",
                f"""
                #!/usr/bin/env bash
                printf '%s\n' "$@" >> {str(aws_log)!r}
                exit 99
                """,
            )

            result = subprocess.run(
                [self.bash_bin, str(self.script("get-customer-credentials.sh")), "--account-id", SYNTHETIC_ACCOUNT_ID],
                env=self.isolated_env(home, bin_dir),
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(
                set(payload),
                {"Version", "AccessKeyId", "SecretAccessKey", "SessionToken", "Expiration"},
            )
            self.assertEqual(payload["Version"], 1)
            invocation = curl_log.read_text(encoding="utf-8")
            self.assertIn("https://broker.invalid/Prod/v1/customer-credentials", invocation)
            self.assertIn("Authorization: Bearer synthetic-login-token", invocation)
            self.assertIn(f'"accountId":"{SYNTHETIC_ACCOUNT_ID}"', invocation)
            self.assertIn('"agent":"hermes"', invocation)
            self.assertFalse(aws_log.exists(), "customer client attempted a local AWS command")


def bash_warning_lines(binary: str, version: tuple[int, ...] | None, skipped: int) -> list[str]:
    floor = ".".join(str(part) for part in SKILL_BASH_FLOOR)
    if not binary:
        found = "bash not found in PATH"
    elif version is None:
        found = f"{binary} (version unreadable)"
    else:
        found = f"{binary} is bash {'.'.join(str(part) for part in version)}"
    return [
        f"- WARN: {found}; the skill's shell client needs bash {floor} or newer",
        f"- WARN: {skipped} skill checks were skipped. 이 환경에서 고객 AWS 조회 도구는 동작하지 않습니다.",
        "- 저장소 문제가 아닙니다. 스킬이 bash 4.3 전용 문법(local -n, ${var,,}, ;;&)을 사용합니다.",
        f"- 조치: {SKILL_OWNER}에게 DM 하세요. 스킬 쪽 수정이 필요합니다.",
        "- 임시로 쓰려면 에이전트를 실행하는 환경의 PATH에서 Homebrew bash가 먼저 선택되게 하세요.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", help="installed skill directory; otherwise search supported agent paths")
    args = parser.parse_args()

    try:
        skill_dir = discover_skill_dir(args.skill_dir)
    except FileNotFoundError as exc:
        print(f"aws customer skill conformance: FAIL ({exc})")
        return 1

    AwsCustomerSkillConformanceTests.configure(skill_dir)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AwsCustomerSkillConformanceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        print(f"aws customer skill conformance: FAIL ({skill_dir})")
        return 1

    if AwsCustomerSkillConformanceTests.bash_meets_floor():
        print(f"aws customer skill conformance: PASS ({skill_dir})")
        return 0

    print(f"aws customer skill conformance: PASS WITH WARNINGS ({skill_dir})")
    for line in bash_warning_lines(
        AwsCustomerSkillConformanceTests.bash_bin,
        AwsCustomerSkillConformanceTests.bash_version,
        len(result.skipped),
    ):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
