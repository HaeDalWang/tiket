#!/usr/bin/env bash
#
# fetch-ticket.sh — Zendesk 티켓 번호로 메타 + 전체 코멘트 스레드를 가져온다.
#
# 자격증명은 ~/.config/saltware/zendesk.conf 에서 읽는다 (scripts/onboarding.sh 가 저장).
# 셸 프로필이나 환경변수에 의존하지 않으므로 zsh / bash / fish 어디서든 같게 동작한다.
# 환경변수가 설정돼 있으면 그쪽이 우선한다 (CI·일회성 실행용).
#
# 사용:
#   bash scripts/fetch-ticket.sh <티켓번호>                 사람이 읽는 형식
#   bash scripts/fetch-ticket.sh <티켓번호> --json          원본 JSON
#   bash scripts/fetch-ticket.sh <티켓번호> --images <디렉터리>  본문 이미지 내려받기
#
# 출력은 stdout 으로만 흘린다. 파일로 저장하지 않는다 — 어디에 남길지는 호출자가 정한다.

set -euo pipefail

CONF="$HOME/.config/saltware/zendesk.conf"

conf_value() {
    [ -f "$CONF" ] || return 0
    grep -E "^$1=" "$CONF" 2>/dev/null | head -1 | cut -d'=' -f2- || true
}

TICKET_ID="${1:-}"
MODE="${2:-text}"
IMAGE_DIR=""
if [ "${2:-}" = "--images" ]; then
    MODE="text"
    IMAGE_DIR="${3:-}"
    [ -n "$IMAGE_DIR" ] || { echo "--images 에는 저장할 디렉터리가 필요하다." >&2; exit 1; }
fi

if [[ -z "$TICKET_ID" || ! "$TICKET_ID" =~ ^[0-9]+$ ]]; then
    echo "사용법: $0 <티켓번호> [--json]" >&2
    echo "  티켓번호는 숫자만." >&2
    exit 1
fi
if [[ -n "${2:-}" && "$2" != "--json" && "$2" != "--images" ]]; then
    echo "알 수 없는 옵션: $2 (--json, --images 만 지원)" >&2
    exit 1
fi

for bin in curl jq; do
    command -v "$bin" >/dev/null 2>&1 || { echo "필요한 도구 없음: $bin" >&2; exit 1; }
done

# 우선순위: 우리 환경변수 → 외부 스킬 호환 이름 → conf 파일
ZD_SUB="${ZENDESK_SUBDOMAIN:-${Zendesk_SUBDOMAIN:-$(conf_value ZENDESK_SUBDOMAIN)}}"
ZD_EMAIL="${ZENDESK_EMAIL:-${Zendesk_EMAIL:-$(conf_value ZENDESK_EMAIL)}}"
ZD_TOKEN="${ZENDESK_API_TOKEN:-${Zendesk_API:-$(conf_value ZENDESK_API_TOKEN)}}"

missing=()
[ -n "$ZD_SUB" ]   || missing+=("ZENDESK_SUBDOMAIN")
[ -n "$ZD_EMAIL" ] || missing+=("ZENDESK_EMAIL")
[ -n "$ZD_TOKEN" ] || missing+=("ZENDESK_API_TOKEN")
if [ ${#missing[@]} -gt 0 ]; then
    echo "Zendesk 자격증명 없음: ${missing[*]}" >&2
    echo "해결: bash scripts/onboarding.sh 를 실행해 토큰을 등록한다." >&2
    exit 1
fi

case "$ZD_SUB" in
    *.zendesk.com) HOST="$ZD_SUB" ;;
    *)             HOST="${ZD_SUB}.zendesk.com" ;;
esac
AUTH="${ZD_EMAIL}/token:${ZD_TOKEN}"
BASE="https://${HOST}/api/v2"

zd() {  # 단건 조회. 2xx 아니면 시끄럽게 죽는다.
    local path="$1" out code
    out=$(curl -sS -m 30 -w $'\n%{http_code}' -u "$AUTH" "${BASE}${path}")
    code="${out##*$'\n'}"; out="${out%$'\n'*}"
    if [[ "$code" -lt 200 || "$code" -ge 300 ]]; then
        echo "Zendesk API ${path} → HTTP ${code}" >&2
        [ "$code" = "401" ] && echo "인증 거부. 토큰을 다시 등록한다: bash scripts/onboarding.sh" >&2
        [ "$code" = "404" ] && echo "티켓을 찾을 수 없다. 번호와 서브도메인을 확인한다." >&2
        exit 1
    fi
    printf '%s' "$out"
}

zd_all() {  # 페이지네이션 끝까지. 코멘트 100건 넘는 스레드가 잘리지 않게 한다.
    local url="${BASE}$1" key="$2" acc='[]' body code page
    while [[ -n "$url" && "$url" != "null" ]]; do
        body=$(curl -sS -m 30 -w $'\n%{http_code}' -u "$AUTH" "$url")
        code="${body##*$'\n'}"; body="${body%$'\n'*}"
        if [[ "$code" -lt 200 || "$code" -ge 300 ]]; then
            echo "Zendesk API $1 → HTTP ${code}" >&2; exit 1
        fi
        page=$(printf '%s' "$body" | jq --arg k "$key" '.[$k] // []')
        acc=$(jq -n --argjson a "$acc" --argjson p "$page" '$a + $p')
        # cursor 방식(meta.has_more) 우선, 없으면 offset 방식(next_page)으로 폴백.
        url=$(printf '%s' "$body" | jq -r '
            if (.meta.has_more == true) then (.links.next // empty)
            else (.next_page // empty) end')
    done
    jq -n --argjson a "$acc" --arg k "$key" '{($k): $a}'
}

TICKET_JSON=$(zd "/tickets/${TICKET_ID}.json")
COMMENTS_JSON=$(zd_all "/tickets/${TICKET_ID}/comments.json?sort_order=asc" "comments")

if [[ "$MODE" == "--json" ]]; then
    jq -n --argjson t "$TICKET_JSON" --argjson c "$COMMENTS_JSON" \
       '{ticket: $t.ticket, comments: $c.comments}'
    exit 0
fi

AIDS=$(echo "$COMMENTS_JSON" | jq -r '[.comments[].author_id] | unique | join(",")')
USERS_JSON=$(zd "/users/show_many.json?ids=${AIDS}")

echo "════════════════════════════════════════════════════════════"
echo "$TICKET_JSON" | jq -r '.ticket |
  "TICKET #\(.id)  [\(.status)]\n" +
  "제목   : \(.subject)\n" +
  "생성   : \(.created_at)   업데이트: \(.updated_at)\n" +
  "우선순위: \(.priority // "-")   유형: \(.type // "-")"'
echo "링크   : https://${HOST}/agent/tickets/${TICKET_ID}"
echo "════════════════════════════════════════════════════════════"
echo ""

echo "$COMMENTS_JSON" | jq -r --argjson users "$USERS_JSON" '
  ($users.users | map({key: (.id|tostring), value: {name, role}}) | from_entries) as $u
  | .comments[]
  | ($u[(.author_id|tostring)] // {name:"(알 수 없음)", role:"?"}) as $a
  | "──────────────────────────────────────────────\n" +
    "[\(.created_at)] \($a.name) (\($a.role))" +
    (if .public then "  · 공개" else "  · 내부 메모" end) + "\n" +
    "──────────────────────────────────────────────\n" +
    .body +
    (if (.attachments | length) > 0 then
       "\n\n첨부: " +
       ([.attachments[] | "\(.file_name) (\(((.size // 0)/1024)|floor)KB)"] | join(", "))
     else "" end) + "\n"'

# 첨부는 본문 텍스트에 안 들어온다. 존재만 알리고 내용 확인은 사람에게 넘긴다.
#
# Zendesk 는 본문에 붙여넣은 이미지를 attachments 배열에 안 넣고 본문 마크다운 링크로만
# 남기는 경우가 있다. attachments 만 세면 이미지가 4장 있어도 "첨부 없음"으로 보이고,
# 읽는 쪽은 자기가 뭘 못 봤는지조차 모른 채 답변을 쓰게 된다. 둘 다 센다.
ATTACH_N=$(echo "$COMMENTS_JSON" | jq '[.comments[].attachments[]?] | length')
INLINE_URLS=$(echo "$COMMENTS_JSON" | jq -r '.comments[].body | scan("https://[^)[:space:]]+/attachments/token/[^)[:space:]]+")' | sort -u)
INLINE_N=$(printf '%s' "$INLINE_URLS" | grep -c . || true)
TOTAL_IMG=$((ATTACH_N + INLINE_N))

if [ -n "$IMAGE_DIR" ] && [ "$INLINE_N" -gt 0 ]; then
    mkdir -p "$IMAGE_DIR"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "본문 이미지 ${INLINE_N}건 내려받기 → ${IMAGE_DIR}"
    i=0
    while IFS= read -r url; do
        [ -n "$url" ] || continue
        i=$((i + 1))
        # 자격증명은 우리 Zendesk 호스트에만 보낸다. 고객사 헬프데스크 등 다른 호스트로
        # Authorization 헤더를 흘리면 우리 토큰을 제3자에게 넘기는 것이 된다.
        if printf '%s' "$url" | grep -q "^https://${HOST}/"; then
            curl -sS -L -u "$AUTH" -o "${IMAGE_DIR}/img${i}.png" "$url" || true
        else
            curl -sS -L -o "${IMAGE_DIR}/img${i}.png" "$url" || true
        fi
        if [ -s "${IMAGE_DIR}/img${i}.png" ]; then
            echo "  img${i}.png  ←  $(printf '%s' "$url" | cut -c1-60)..."
        else
            echo "  img${i}.png  실패  ←  $(printf '%s' "$url" | cut -c1-60)..."
        fi
    done <<< "$INLINE_URLS"
    echo "════════════════════════════════════════════════════════════"
elif [ "$TOTAL_IMG" -gt 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "※ 이미지 ${TOTAL_IMG}건 (첨부 ${ATTACH_N} · 본문 삽입 ${INLINE_N})."
    echo "  내용은 위 텍스트에 없다. 답변에 그 정보가 필요하면 추측하지 말고 받아서 본다:"
    echo "    bash scripts/fetch-ticket.sh ${TICKET_ID} --images <저장할디렉터리>"
    echo "════════════════════════════════════════════════════════════"
fi
