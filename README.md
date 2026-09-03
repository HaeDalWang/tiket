# tiket

고객사 기술 티켓 응대 워크스페이스. 코드 저장소가 아니라 **고객 컨텍스트, 근거, 판단 변화, 회신 이력의 저장소**다.

Claude Code, Codex, Hermes, Kiro가 같은 자료와 경계를 사용해 회신 초안을 만들고, 검수·발송·실제 인프라 변경은 사람이 담당한다.

> **처음이라면 [`ONBOARDING.md`](ONBOARDING.md)부터 순서대로 따라간다.** clone부터 첫 합성 티켓까지의 유일한 경로다.

## 구조

```text
ONBOARDING.md        신규 엔지니어 Day 1 경로
CLAUDE.md            에이전트 상세 규칙 정본(영문)
AGENTS.md            Codex/Hermes 공용 진입점(영문)
.kiro/steering/      Kiro 자동 로드 진입점
.kiro/settings/      Kiro MCP 설정(생성물)
.mcp.json            Claude Code MCP 설정(생성물)
.claude/settings.json Claude Code MCP 툴 차단(생성물)
.codex/config.toml   Codex MCP 설정(생성물)
.githooks/           고객 자료 유출·오push 차단 hook
agents/              공통 능력 매핑, 설치 검증, MCP 정본 manifest
customers/           고객사 프로필·티켓·관계 컨텍스트
examples/            공통 upstream의 비식별 재구성 티켓 표본
policy/              대용량 규정의 라우팅·카드·원본 목록
playbooks/           근거 검증, 회신, 인프라 작업, 알려진 함정
handoff/             다른 프로젝트와 PoC 의뢰·결과 handoff
templates/           신규 고객사·티켓 시작점
scripts/             저장소 구조 검증 도구
```

MCP는 clone으로 함께 전달된다. `agents/environment/mcp-manifest.json`이 유일한 정본이고 호스트별 설정 파일은 `scripts/render_agent_configs.py`가 생성한다. 생성물을 직접 수정하면 validator가 실패로 보고한다. AWS 문서 MCP는 `--read-only`와 `--skip-auth`로 문서 조회만 가능하며, 고객 계정 접근은 브로커 경유 skill만 사용한다.

디렉터리와 파일 이름은 ASCII만 사용한다. 파일 **내용**은 한국어로 쓴다. 경로에 한글을 쓰면 macOS·Linux·Git 사이의 Unicode 정규화 차이로 도구가 같은 파일을 다른 이름으로 인식한다.

동료 엔지니어 배포는 공통 upstream을 clone하는 Git-only 방식을 사용한다. 프로젝트 폴더 전체를 압축하거나 파일 복사로 배포하지 않는다.

Alpha 단계에서는 remote가 하나뿐이다. 엔지니어 개인 private 운영 저장소는 회사 승인 대기 중이므로 `customers/CUST-*`는 Git 추적에서 제외되고 로컬에만 보관된다. 공통 저장소로의 push는 `.githooks/pre-push`가 차단한다. clone 직후 `git config core.hooksPath .githooks`로 이 장치를 활성화해야 하며, 미설정 상태는 validator가 실패로 보고한다. 자세한 remote 구성, 경로 소유권, 승인 후 전환 절차는 `DISTRIBUTION.md`를 따른다.

현재 개인 repository의 Git history는 배포하지 않는다. 추후 회사 GitHub의 공통 upstream은 `scripts/export_framework_snapshot.py`로 생성한 clean snapshot의 새 history에서 시작한다.

공통 upstream의 `customers/`에는 운영 고객 기록을 두지 않는다. `examples/`는 실제 workflow를 비식별 reference로 재구성해 구조·lifecycle·회신 스타일을 보여주는 자료이며 활성 고객 상태가 아니다. 실제 업무는 각 엔지니어의 private `origin`에 만든 `customers/CUST-NNN/`에서 진행한다.

에이전트가 읽는 규칙과 라우팅 지시는 가능한 한 영어로 작성한다. 사람이 관리하는 고객 정보, 티켓 내용, 고객 회신은 한국어로 작성한다.

## 티켓이 들어오면

1. `customers/<고객사>/profile.md`를 읽는다.
2. `policy/_routing.md`에서 적용 규정을 찾는다.
3. 고객사의 과거 티켓에서 유사 건을 찾는다.
4. `templates/ticket.md`로 티켓 파일을 만든다.
5. read-only 조사와 공식 근거를 기록한다.
6. 필요하면 `handoff/`를 통해 별도 프로젝트에 PoC를 의뢰한다.
7. 검증된 결과로 회신 초안을 작성한다.
8. 사람이 검수·발송한 뒤 실제 발송문과 고객 반응을 append한다.

## 담당자와 관계성

보안팀/팀장 승인 전에는 tracked 파일에 실제 고객사명과 담당자 이름·연락처를 기록하지 않는다. `CUST-001`, `CONTACT-001` 같은 비식별 reference를 사용하고 실제 연결 정보는 Git에서 제외되는 `.private/customer-map.md`에만 둔다. 관계성 기록은 날짜가 있는 관찰 행동과 대응 방식으로 제한하며 성격이나 인격 평가는 기록하지 않는다.

## 대용량 회사 규정

PDF와 이미지를 매번 프롬프트에 모두 넣지 않는다. `_routing.md` → 관련 정책 카드 → 필요한 추출 구간 → 원본 페이지 순서로 필요한 자료만 읽는다. 원본 파일은 기본적으로 Git에서 제외한다.

정리 전 Raw 파일은 `policy/inbox/`에 그대로 넣는다. 수신함 내용은 기본적으로 Git에서 제외되며, 에이전트가 목록화·OCR·버전 판별·정책 카드 생성을 진행한다.

## PoC 연결

티켓 저장소에는 질문·제약·판단을, PoC 프로젝트에는 코드·실험을 둔다. 결과는 repository/branch/commit, 실행 명령, 실제 결과, 한계가 포함된 결과서로 반환한다.

## 경계

| 위치 | 역할 |
|---|---|
| `tiket` | 고객 응대 컨텍스트·근거·티켓·회신 이력 |
| `~/salt/<고객사>/` 또는 지정 프로젝트 | Terraform 등 실제 코드와 PoC |
| `~/Documents/obsidian/` | 개인 자료, 에이전트 접근 불가 |

## 보안

GitHub는 private 저장소만 사용한다. 그래도 자격증명, 토큰, 세션 값, private key, Terraform state는 절대 커밋하지 않는다. 고객 전달 비용 수치는 FitCloud 정제값만 사용한다.

보안팀/팀장 승인 전에는 고객사명, 담당자 연락처, AWS Account/Payer ID, IP, CIDR 등 고객 보안정보도 commit하지 않는다. 티켓 원문은 비식별화한 뒤 저장한다.

구조 검증은 다음 명령으로 수행한다.

```bash
python3 scripts/validate_workspace.py
```

공통 upstream 배포 후보는 운영 고객 디렉터리 부재까지 확인한다.

```bash
python3 scripts/validate_workspace.py --framework
python3 scripts/test_validate_workspace.py
python3 scripts/test_export_framework_snapshot.py
python3 scripts/check_public_sources.py
```
