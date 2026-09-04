#!/usr/bin/env bash
#
# onboarding.sh — macOS / Linux 온보딩. Windows 는 onboarding.ps1 을 쓴다.
#
# 셸 프로필(~/.zshenv, ~/.bashrc 등)을 건드리지 않는다. 사용자가 어떤 셸을 쓰는지
# 알 수 없기 때문이다. 자격증명은 ~/.config/saltware/*.conf 에 저장하고, 이 저장소의
# 스크립트가 그 파일을 직접 읽는다. saltware-csg-skills install.sh 와 같은 규약이다.
#
# 사용:
#   bash scripts/onboarding.sh            대화형 (자격증명 입력 포함)
#   bash scripts/onboarding.sh --check    확인만 (입력 없음, CI·에이전트용)

set -uo pipefail

# STEPS-PARITY-START
STEP_NAMES=(
  "required-tools"
  "push-guard"
  "zendesk-credentials"
  "workspace-validation"
)
# STEPS-PARITY-END

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF_DIR="$HOME/.config/saltware"
ZENDESK_CONF="$CONF_DIR/zendesk.conf"
CHECK_ONLY=0
[ "${1:-}" = "--check" ] && CHECK_ONLY=1

fail_count=0
ok()   { printf '  \033[32mOK\033[0m    %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; fail_count=$((fail_count + 1)); }
skip() { printf '  \033[33m건너뜀\033[0m %s\n' "$1"; }
step() { printf '\n[%s] %s\n' "$1" "$2"; }

# ── 1. required-tools ────────────────────────────────────────────────────────
step 1/4 "필수 도구"
for bin in git python3 curl jq; do
  if command -v "$bin" >/dev/null 2>&1; then
    ok "$bin"
  else
    bad "$bin 없음 — macOS: brew install $bin"
  fi
done

# ── 2. push-guard ────────────────────────────────────────────────────────────
# 고객 자료가 공용 저장소로 나가는 걸 막는 hook. 활성화는 로컬에서 한 번 해야 한다.
step 2/4 "push guard"
current_hooks=$(git -C "$ROOT" config --get core.hooksPath 2>/dev/null || true)
if [ "$current_hooks" = ".githooks" ]; then
  ok "core.hooksPath = .githooks"
elif [ "$CHECK_ONLY" -eq 1 ]; then
  bad "core.hooksPath 미설정 — 해결: git config core.hooksPath .githooks"
else
  if git -C "$ROOT" config core.hooksPath .githooks; then
    ok "core.hooksPath 를 .githooks 로 설정했다"
  else
    bad "core.hooksPath 설정 실패"
  fi
fi
if [ -x "$ROOT/.githooks/pre-push" ]; then
  ok "pre-push hook 실행 가능"
else
  bad "pre-push hook 이 없거나 실행 권한 없음 — chmod +x .githooks/pre-push"
fi

# ── 3. zendesk-credentials ───────────────────────────────────────────────────
step 3/4 "Zendesk 자격증명"
conf_has() { [ -f "$ZENDESK_CONF" ] && grep -qE "^$1=" "$ZENDESK_CONF" 2>/dev/null; }

if conf_has ZENDESK_SUBDOMAIN && conf_has ZENDESK_EMAIL && conf_has ZENDESK_API_TOKEN; then
  ok "설정됨: ~/.config/saltware/zendesk.conf (값은 출력하지 않는다)"
elif [ "$CHECK_ONLY" -eq 1 ]; then
  bad "미설정 — 해결: bash scripts/onboarding.sh"
elif [ ! -t 0 ]; then
  # 토큰을 파이프나 인자로 받으면 히스토리·로그에 남는다.
  bad "터미널에서 직접 실행해야 자격증명을 입력받을 수 있다"
else
  echo
  echo "  Zendesk API 토큰이 필요하다. 아직 없으면 먼저 발급받는다:"
  echo "    Zendesk 관리센터 → 앱 및 통합 → API → Zendesk API → 토큰 추가"
  echo "  건너뛰려면 그냥 Enter 를 누른다."
  echo
  printf "  서브도메인 (예: saltware): "; read -r zd_sub
  if [ -z "$zd_sub" ]; then
    skip "자격증명 설정을 건너뛰었다. 나중에 다시 실행하면 된다."
  else
    printf "  에이전트 이메일: "; read -r zd_email
    printf "  API 토큰 (화면에 안 보인다): "; read -rs zd_token; echo

    if [ -z "$zd_email" ] || [ -z "$zd_token" ]; then
      bad "이메일 또는 토큰이 비었다. 저장하지 않았다."
    else
      case "$zd_sub" in
        *.zendesk.com) zd_host="$zd_sub" ;;
        *)             zd_host="${zd_sub}.zendesk.com" ;;
      esac
      printf "  확인 중: https://%s ...\n" "$zd_host"
      resp=$(curl -sS -m 20 -w $'\n%{http_code}' \
        -u "${zd_email}/token:${zd_token}" \
        "https://${zd_host}/api/v2/users/me.json" 2>/dev/null)
      code="${resp##*$'\n'}"; body="${resp%$'\n'*}"

      if [ "$code" = "200" ]; then
        who=$(printf '%s' "$body" | jq -r '.user | "\(.name) (\(.role))"' 2>/dev/null || echo "?")
        mkdir -p "$CONF_DIR" && chmod 700 "$CONF_DIR" 2>/dev/null
        old_umask=$(umask); umask 077
        cat > "$ZENDESK_CONF" << EOF
# tiket Zendesk credentials. 이 파일 내용을 채팅·이슈·PR 에 붙여넣지 않는다.
# 다시 설정하려면: bash scripts/onboarding.sh
ZENDESK_SUBDOMAIN=${zd_sub}
ZENDESK_EMAIL=${zd_email}
ZENDESK_API_TOKEN=${zd_token}
EOF
        umask "$old_umask"; chmod 600 "$ZENDESK_CONF"
        ok "인증 성공 ($who) — ~/.config/saltware/zendesk.conf 에 저장 (권한 600)"
      elif [ "$code" = "401" ] || [ "$code" = "403" ]; then
        bad "인증 거부 (HTTP $code). 이메일 또는 토큰이 맞지 않는다. 저장하지 않았다."
      else
        bad "Zendesk 응답 HTTP ${code:-없음}. 서브도메인과 네트워크를 확인한다. 저장하지 않았다."
      fi
    fi
  fi
fi

# ── 4. workspace-validation ──────────────────────────────────────────────────
step 4/4 "저장소 검증"
if command -v python3 >/dev/null 2>&1; then
  if out=$(cd "$ROOT" && python3 scripts/validate_workspace.py 2>&1); then
    ok "$(printf '%s' "$out" | head -1)"
  else
    bad "$(printf '%s' "$out" | head -3)"
  fi
else
  bad "python3 이 없어 검증을 건너뛰었다"
fi

# ── 결과 ─────────────────────────────────────────────────────────────────────
echo
if [ "$fail_count" -eq 0 ]; then
  printf '\033[32m온보딩 완료.\033[0m 다음: ONBOARDING.md 의 "연습해보기"\n'
  exit 0
fi
printf '\033[31m%d개 항목이 남았다.\033[0m 위 FAIL 줄의 해결 방법을 따른 뒤 다시 실행한다.\n' "$fail_count"
exit 1
