# 구조 해설 — 각 디렉터리가 언제 로드되고 어떻게 쌓이는가

README 는 이 저장소가 **무엇인지** 설명한다. 이 문서는 **어떻게 동작하는지** 설명한다.
`playbooks/`, `policy/`, `handoff/`, `customers/` 가 각각 언제 에이전트 컨텍스트에 들어가고
누가 무엇을 채우는지가 궁금하면 여기를 읽는다.

---

## 큰 원칙 — 기본은 "안 읽는다"

`agents/task-router.md` 첫 줄이 규칙 전부다.

> Classify first, then load only the listed modules.
> **Never load every policy, playbook, ticket, or skill by default.**

이 저장소는 정책 카드 14개, 플레이북 5개, 함정 카드 4개를 갖고 있다. 전부 읽으면
티켓 하나 답하기 전에 수만 자를 소비한다. 그래서 **모든 디렉터리는 기본 비활성**이고,
라우터가 지목한 것만 로드된다.

디렉터리는 두 부류다.

| 부류 | 성격 | 해당 |
|---|---|---|
| **읽는 것** | 에이전트가 조건부로 로드하는 규칙·지식 | `agents/` `policy/` `playbooks/` `templates/` |
| **쌓는 것** | 작업하면서 채워지는 기록 | `tickets/` `customers/` `handoff/` |

---

## 티켓 하나가 지나가는 경로

```
티켓 번호
   │
   ├─ agents/task-router.md ─────── 항상 읽음. 등급(quick/standard/high-risk) 판정
   │
   ├─ playbooks/ticket-outputs.md ─ 항상 읽음. 산출물 3종 중 무엇을 만들지 결정
   │
   ├─ policy/_routing.md ────────── 항상 읽음(색인만). 매칭된 카드만 추가 로드
   │
   ├─ customers/<ref>/profile.md ── 있을 때만. 계약·청구·접근 범위가 걸릴 때만 생성
   │
   ├─ playbooks/pitfalls/ ───────── 주제가 걸릴 때만
   │
   └─ tickets/<번호>.md ─────────── 결과를 여기에 쓴다 (로컬 전용)
```

---

## `agents/` — 에이전트가 무엇을 할 수 있는지

**항상 읽는 것은 `task-router.md` 하나뿐이다.** 나머지는 필요할 때만.

| 파일 | 언제 읽히나 | 누가 갱신하나 |
|---|---|---|
| `task-router.md` | **항상.** 진입점이 여기로 보낸다 | 워크플로우가 바뀔 때 사람이 |
| `capability-catalog.md` | 도구를 고를 때 | capability 가 추가·차단될 때 |
| `runtime-status.md` | 도구가 지금 쓸 수 있는지 확인할 때 | 설치·검증 후 사람이 |
| `install-verification.md` | 온보딩·설치 문제 때 | 설치 절차가 바뀔 때 |
| `compatibility.md` | 다른 에이전트에 인계할 때 | 드물게 |
| `environment/mcp-manifest.json` | **읽히지 않음.** 도구가 읽는다 | `render_agent_configs.py` 가 여기서 호스트 설정 4개를 생성 |

`runtime-status.md` 는 **관측 기록이지 정책이 아니다.** "이 capability 를 써도 되나"는
`capability-catalog.md` 가 정하고, "지금 실제로 되나"는 `runtime-status.md` 가 답한다.
둘이 어긋나면 실측이 이긴다.

---

## `policy/` — 회사 규정을 통째로 넣지 않기 위한 구조

핵심은 **색인과 본문의 분리**다.

```
policy/
├── _routing.md        ← 항상 읽는 색인. 15줄짜리 표 하나
├── cards/             ← 매칭된 것만 읽는 본문 (카드 14개 + _template)
├── sources.json       ← 원본 파일의 SHA-256·줄수 매니페스트
├── excerpts/          ← 승인된 OCR 추출본
├── inbox/             ← 정리 전 원본 투입구 (gitignored)
├── raw/               ← 원본 문서 (gitignored)
└── pending-review.md  ← draft → active 승격에 필요한 사람 결정
```

### 읽는 순서

1. `_routing.md` 의 **trigger terms** 로 매칭
2. 매칭된 **카드만** 읽는다
3. 카드로 부족할 때만 `excerpts/` 나 원본 페이지를 연다
4. 적용한 정책 ID·출처 페이지·발효일을 티켓에 기록

### 쌓이는 방식

```
사람이 원본 PDF 를 policy/inbox/ 에 넣는다   (gitignored — 원본은 저장소에 안 올라감)
        ↓
에이전트가 목록화·OCR·버전 판별
        ↓
정책 카드 초안 작성 → cards/ 에 status: draft 로 추가
        ↓
_routing.md 에 행 추가 (검토 후에만)
        ↓
사람이 검토 → status: active 승격, pending-review.md 에서 제거
```

### 지금 상태에서 중요한 것

**카드 14개 중 `active` 는 1개뿐이고 12개가 `draft`, 1개가 `retired` 다.**

> `draft` 카드는 약속을 만들거나 조치를 승인할 수 없다. (`task-router.md`)

즉 대부분의 정책 카드는 **배경 참고용**이며, 고객에게 "규정상 이렇습니다"라고 말하는
근거로 쓸 수 없다. 이건 결함이 아니라 의도적인 게이트다 — 사람 검토를 거치지 않은 규정을
고객 약속으로 바꾸지 않기 위해서다.

---

## `playbooks/` — 절차 지식

정책이 "무엇이 허용되나"라면 플레이북은 "어떻게 하나"다.

| 파일 | 언제 | 성격 |
|---|---|---|
| `ticket-outputs.md` | **티켓마다 항상** | 산출물 3종의 형식. 가장 먼저 읽는다 |
| `reply-writing-rules.md` | 회신 초안을 쓸 때 | 언어·분리·최종 점검 |
| `reply-style.md` | 회신 초안을 쓸 때 | 표현 프로파일 2종 |
| `evidence-verification.md` | `quick` 은 일부, `standard` 이상은 전체 | 근거 검증 절차 |
| `infra-change-process.md` | **`high-risk` 변경 작업일 때만** | 사람 승인 경계 |
| `pitfalls/` | 해당 주제가 걸릴 때만 | 알려진 함정 |

### `pitfalls/` 가 쌓이는 방식 — 이게 판례의 원형이다

함정 카드는 **케이스가 아니라 일반화된 패턴**만 담는다. 그래서 태생적으로 비식별이고,
고객 맥락 없이 재사용된다.

```
티켓에서 "이거 다음에도 또 걸리겠다" 싶은 것이 나옴
        ↓
사람이 판단: 이게 일반화되나?  ← 자동 집계가 아니다
        ↓
pitfalls/ 에 카드 작성 — 위험 / 관측 / 필수 행동 / 재사용 전 검증
        ↓
pitfalls/README.md 표에 trigger 추가
```

현재 4개. 예를 들어 `savings-plans-inventory-is-in-fitcloud.md` 는 **공식 문서를 충실히
따르면 오히려 틀리는** 경우를 기록한 것이다 — AWS 문서는 콘솔 경로를 안내하지만
우리 고객사 대부분은 그 화면을 못 본다.

---

## `templates/` — 빈 양식

| 파일 | 무엇을 만드나 |
|---|---|
| `ticket-intake.md` | `tickets/<번호>.md` 의 원본. **발송 전 점검 6항목이 여기 있다** |
| `customer-profile.md` | `customers/<ref>/profile.md` 의 원본 |
| `customer-index.md` | `customers/_index.md` 의 원본 |

`ticket-intake.md` 는 단순 양식이 아니라 **강제 장치**다. `validate_workspace.py` 가
`## 작업 지시`, `[변경]`, `출처 없는 [확인] 은 [확인] 이 아니다`, `## 발송 전 점검` 같은
문구를 검사하므로, 형식을 되돌리면 빌드가 깨진다.

---

## `customers/` — 프로필만, 필요할 때만

**티켓은 여기 없다.** 예전에는 `customers/<ref>/tickets/` 에 3파일로 쌓았지만
지금은 `tickets/` 로 옮겼다.

| 무엇 | 언제 만드나 |
|---|---|
| `profile.md` | **계약·청구·접근 범위가 실제로 걸릴 때만** |

프로필에는 `contract_baseline`, `contract_exceptions`, `payer_model`, `payer_verified_at`,
`coc_owner_ref` 같은 필드가 있고 validator 가 이를 검사한다. 비용·계약 답변 전에 필요한
정보이지, 티켓을 열기 위한 전제가 아니다.

**clone 직후엔 비어 있다.** `_index.md` 하나만 있다.
`customers/CUST-*` 는 gitignore + pre-push 로 저장소 밖으로 못 나간다.

---

## `tickets/` — 실제 작업 기록

| 성격 | 내용 |
|---|---|
| 파일 | 티켓 하나 = `tickets/<번호>.md` 하나 |
| 내용 | **실명 그대로.** 마스킹하지 않는다 |
| Git | gitignore + pre-push 이중 차단. `git add -f` 로도 push 가 막힌다 |
| 동기화 | 없음. 엔지니어별 로컬 |

실명을 그대로 쓰는 이유는 이 디렉터리가 **저장소 밖으로 나갈 수 없기 때문**이다.
비식별은 "항상, 미리"가 아니라 "밖으로 낼 때, 한 번" 하는 것으로 옮겼다.

**백업이 없다.** 노트북을 잃으면 같이 사라진다. 개인 저장소가 승인되면 바뀐다.

---

## `handoff/` — 코드가 필요할 때 나가는 문

티켓 저장소는 코드를 담지 않는다. 실험·구현이 필요하면 다른 프로젝트로 넘긴다.

```
tiket          질문·제약·가설·수용 기준·판단 이력
PoC 프로젝트    코드·의존성·테스트·실험 로그
돌아오는 것     검증된 commit, 실행 명령, 실제 결과, 한계, 회신 가능한 결론
```

상태 흐름: `requested → running → blocked | completed → adopted | rejected`

| 파일 | 용도 |
|---|---|
| `templates/poc-request.md` | 의뢰서 |
| `templates/poc-result.md` | 결과서 |

**PoC 저장소를 통째로 복사해 오지 않는다.** 세션 기록을 인계 산출물로 쓰지도 않는다.
결과서에 적힌 repository·branch·commit·명령·출력을 **직접 확인한 뒤** 회신에 쓴다.

---

## `scripts/` — 도구

| 스크립트 | 언제 |
|---|---|
| `onboarding.sh` / `.ps1` | 최초 1회. 도구 확인 → push guard → Zendesk → 검증 |
| `fetch-ticket.sh` / `.ps1` | 티켓마다. 스레드·이미지 가져오기 |
| `validate_workspace.py` | 커밋 전. 구조·보안 경계 |
| `render_agent_configs.py` | MCP 매니페스트를 고칠 때 |
| `verify_mcp_servers.py` | MCP 연결 확인 |
| `export_framework_snapshot.py` | 공용 저장소로 배포할 때 |

`export_framework_snapshot.py` 는 **allowlist 방식**이다. 분류되지 않은 새 파일이 있으면
조용히 포함되는 게 아니라 **실패한다.** 새 디렉터리를 만들면 분류를 등록해야 한다.

---

## `design/` — 프레임워크가 아니다

이 프레임워크를 **왜 이렇게 만들었는지**의 기록이다. 티켓 처리에 쓰이지 않고
배포본에도 안 들어간다(`workspace-owned` 로 분류됨).

| 위치 | 내용 |
|---|---|
| `decisions/` | 갈림길마다 하나. 정한 것 · 왜 · **버린 선택지** · 근거 |
| `research/` | 실측. 방법·표본 수·한계를 같이 적는다 |
| `open-questions.md` | 아직 안 정한 것 |

**결정이 실측과 어긋나면 실측이 이긴다.** 실제로 `0005`(A/B/C 분류)가 65건 실측 뒤
개정됐다.

---

## 안전장치가 어디에 박혀 있나

규칙은 문서에만 있으면 지켜지지 않는다. 그래서 세 겹으로 둔다.

| 층 | 무엇 | 실패하면 |
|---|---|---|
| 문서 | `CLAUDE.md`, 라우터, 플레이북 | 사람이 읽고 따름 |
| **검증기** | `validate_workspace.py` 의 마커 검사 | **커밋 전 FAIL** |
| **훅** | `.githooks/pre-push` | **push 차단, 우회 불가** |

검증기가 고정하는 것은 문구 그 자체다. 예를 들어 `## 발송 전 점검` 의 항목 문구가
사라지면 빌드가 깨진다. 실제로 세 진입점에서 안전 문장 하나가 조용히 사라진 적이 있고,
검사가 있던 `CLAUDE.md` 만 잡히고 나머지 둘은 넘어갔다. 지금은 셋 다 고정돼 있다.

---

## 새 엔지니어가 자주 묻는 것

**Q. 정책 카드를 다 읽어야 하나?**
아니다. `_routing.md` 에서 매칭된 것만. 전부 읽으면 라우터의 존재 이유가 사라진다.

**Q. `draft` 카드를 근거로 답해도 되나?**
안 된다. 배경 참고까지다. 고객 약속이나 조치 승인에 쓸 수 없다.

**Q. 고객 프로필을 먼저 만들어야 하나?**
아니다. 계약·청구·접근 범위가 실제로 걸릴 때만 만든다. 예전에는 선행 필수였는데
그게 시작 자체를 막는 원인이라 바꿨다.

**Q. 내 티켓 기록이 다른 사람에게 보이나?**
안 보인다. `tickets/` 는 로컬 전용이고 동기화되지 않는다.

**Q. 함정 카드는 자동으로 쌓이나?**
아니다. 사람이 "이건 일반화된다"고 판단해서 쓴다. 그 판단이 카드의 값어치다.

**Q. 왜 이렇게 정했는지 알고 싶다.**
`design/decisions/` 를 본다. 버린 선택지와 그 이유가 같이 적혀 있다.
