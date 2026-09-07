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
  "agents"
  "push-guard"
  "mcp"
  "customer-skill"
  "zendesk-credentials"
  "workspace-validation"
)
# STEPS-PARITY-END

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# saltware-csg-skills 는 별도 저장소다. 저장소 안에 사본을 두지 않는 이유는
# design/decisions/0014 참조 — EXTERNAL_ID 하드코딩, 버전 드리프트, 외부 소유.
SKILL_REPO_URL="git@haedalwang:fitcloud/saltware-csg-skills.git"
SKILL_REPO_CANDIDATES=(
  "${SALTWARE_CSG_SKILLS:-}"
  "$HOME/opensource/saltware-csg-skills"
  "$HOME/saltware-csg-skills"
  "$HOME/work/saltware-csg-skills"
)
# 에이전트 이름 → 스킬 설치 경로. install.sh 의 테이블과 같은 규약.
AGENT_NAMES=(claude-code opencode kiro cursor windsurf augment codex gemini hermes)
AGENT_HOMES=(
  "$HOME/.claude" "$HOME/.config/opencode" "$HOME/.kiro" "$HOME/.cursor"
  "$HOME/.codeium/windsurf" "$HOME/.augment" "$HOME/.agents" "$HOME/.gemini" "$HOME/.hermes"
)

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
step 1/7 "필수 도구"
for bin in git python3 curl jq; do
  if command -v "$bin" >/dev/null 2>&1; then
    ok "$bin"
  else
    bad "$bin 없음 — macOS: brew install $bin"
  fi
done

# ── 2. agents ────────────────────────────────────────────────────────────────
step 2/7 "설치된 에이전트"
detected_agents=()
for i in "${!AGENT_NAMES[@]}"; do
  if [ -d "${AGENT_HOMES[$i]}" ]; then
    detected_agents+=("${AGENT_NAMES[$i]}")
    skill_dir="${AGENT_HOMES[$i]}/skills/aws-customer-account-ops"
    if [ -f "$skill_dir/SKILL.md" ]; then
      ok "${AGENT_NAMES[$i]}  (고객 조회 스킬 있음)"
    else
      ok "${AGENT_NAMES[$i]}"
    fi
  fi
done
if [ "${#detected_agents[@]}" -eq 0 ]; then
  bad "감지된 에이전트 없음 — Claude Code·Codex·Kiro·Hermes 중 하나는 설치돼 있어야 한다"
fi

# ── 2. push-guard ────────────────────────────────────────────────────────────
# 고객 자료가 공용 저장소로 나가는 걸 막는 hook. 활성화는 로컬에서 한 번 해야 한다.
step 3/7 "push guard"
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

# ── 4. mcp ───────────────────────────────────────────────────────────────────
# MCP 설정 파일은 clone 으로 따라온다. 확인할 것은 "실제로 붙는가" 뿐이다.
step 4/7 "MCP 연결"
for host in .mcp.json .claude/settings.json .codex/config.toml .kiro/settings/mcp.json; do
  [ -f "$ROOT/$host" ] || bad "MCP 설정 누락: $host — python3 scripts/render_agent_configs.py 로 생성"
done
if command -v python3 >/dev/null 2>&1; then
  mcp_out=$(cd "$ROOT" && python3 scripts/verify_mcp_servers.py 2>&1)
  mcp_rc=$?
  mcp_last=$(printf '%s' "$mcp_out" | tail -1)
  case "$mcp_rc" in
    0) ok "$mcp_last" ;;
    2) skip "$mcp_last" ;;   # 전제 조건 미비·네트워크 — 경계 위반이 아니다
    *) bad "$mcp_last" ;;
  esac
fi
if [ -d "$HOME/.hermes" ]; then
  skip "Hermes 는 MCP 설정을 저장소 밖 프로필에 둔다. agents/environment/mcp-manifest.json 에 맞춰 직접 정렬한다"
fi

# ── 5. customer-skill ────────────────────────────────────────────────────────
# 스킬은 별도 저장소(saltware-csg-skills)가 소유한다. 여기서는 찾아주고 안내만 한다.
step 5/7 "고객 AWS 조회 스킬"
marker_path=$(aws configure get profile.csg-login.credential_process 2>/dev/null || true)
if [ -n "$marker_path" ] && [ -f "$marker_path" ]; then
  ok "설치됨 — 실행 경로: $(dirname "$marker_path" | sed "s|$HOME|~|")"
  # 사본이 갈라졌는지 본다. self-update 가 부분 실패하면 여기서 드러난다.
  hashes=$(for h in "${AGENT_HOMES[@]}"; do
    d="$h/skills/aws-customer-account-ops"
    [ -d "$d" ] || continue
    hasher=$(command -v sha256sum || echo "shasum -a 256")
    cat "$d"/get-customer-credentials.sh "$d"/get-sts-token.sh "$d"/fitcloud-api.sh 2>/dev/null | $hasher | cut -c1-16
  done | sort -u | grep -c .)
  if [ "${hashes:-0}" -le 1 ]; then
    ok "사본 일치"
  else
    bad "사본이 갈라졌다 (${hashes}종) — saltware-csg-skills 에서 ./install.sh --all 재실행"
  fi
else
  skill_repo=""
  for cand in "${SKILL_REPO_CANDIDATES[@]}"; do
    [ -n "$cand" ] && [ -f "$cand/install.sh" ] && { skill_repo="$cand"; break; }
  done
  if [ -z "$skill_repo" ]; then
    bad "스킬 미설치, 소스 저장소도 없음"
    printf "        해결: 저장소를 clone 한 뒤 설치한다 (접근 권한은 담당자에게 요청)\n"
    printf "          git clone %s ~/opensource/saltware-csg-skills\n" "$SKILL_REPO_URL"
    printf "          bash ~/opensource/saltware-csg-skills/install.sh\n"
  else
    bad "스킬 미설치 — 소스는 $(printf '%s' "$skill_repo" | sed "s|$HOME|~|") 에 있다"
    printf "        해결: bash %s/install.sh\n" "$(printf '%s' "$skill_repo" | sed "s|$HOME|~|")"
    if [ "$CHECK_ONLY" -eq 0 ]; then
      printf "\n        감지된 에이전트 (install.sh --status):\n"
      (cd "$skill_repo" && bash install.sh --status 2>&1 | sed 's/^/          /' | head -20) || true
    fi
  fi
fi

# ── 3. zendesk-credentials ───────────────────────────────────────────────────
step 6/7 "Zendesk 자격증명"
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
  echo "  Zendesk 토큰을 등록한다. 티켓을 번호로 가져오려면 필요하다."
  echo "  토큰 발급: Zendesk 관리센터 → 앱 및 통합 → API → Zendesk API → 토큰 추가"
  echo

  # 빈 입력은 건너뛰기가 아니다. 건너뛰려면 skip 을 직접 입력해야 한다 —
  # 필수 단계에 쉬운 탈출구를 두면 대부분 그걸 누르고, 나중에 안 된다고 되돌아온다.
  ask_required() {  # ask_required <라벨> <힌트>; 값은 stdout, skip 이면 빈 값 + 리턴 1
    local label="$1" hint="$2" value="" attempt=0
    while [ "$attempt" -lt 3 ]; do
      attempt=$((attempt + 1))
      printf "  %s%s: " "$label" "$hint" >&2
      read -r value
      [ "$value" = "skip" ] && return 1
      [ -n "$value" ] && { printf '%s' "$value"; return 0; }
      printf "    값이 필요하다. 지금 등록할 수 없으면 skip 을 입력한다.\n" >&2
    done
    return 1
  }

  if ! zd_sub=$(ask_required "Zendesk 서브도메인" " (예: saltware)"); then
    skip "토큰 등록을 건너뛰었다. 티켓 조회는 아직 안 된다."
    skip "나중에 다시 실행: bash scripts/onboarding.sh"
  else
    # 'Zendesk 로그인 이메일'로 적는다. 이 저장소에서 '에이전트'는 AI 도구를 뜻하므로
    # Zendesk 쪽 agent(상담원)와 겹쳐 읽는 사람이 자기 이메일인지 헷갈린다.
    if ! zd_email=$(ask_required "Zendesk 로그인 이메일" " (본인 계정)"); then
      skip "토큰 등록을 건너뛰었다. 나중에 다시 실행: bash scripts/onboarding.sh"
    else
      printf "  API 토큰 (화면에 안 보인다): "
      read -rs zd_token; echo

      if [ -z "$zd_token" ]; then
        bad "토큰이 비었다. 저장하지 않았다. 다시 실행: bash scripts/onboarding.sh"
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
fi

# ── 4. workspace-validation ──────────────────────────────────────────────────
step 7/7 "저장소 검증"
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
