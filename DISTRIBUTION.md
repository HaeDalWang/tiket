# 배포 및 동기화 원칙

이 문서는 `tiket` 프레임워크를 동료 엔지니어의 독립 워크스페이스에 배포하고 업데이트하는 1차 원칙을 정의한다.

## 잠긴 결정

- 공통 프레임워크 업데이트는 Git remote와 pull/merge만으로 전달한다.
- 동료 workspace는 기본적으로 공통 저장소의 `main` 브랜치를 따른다.
- 프로젝트 폴더 전체 ZIP, GitHub Template 기반 복제, Copier 같은 별도 템플릿 업데이트 도구는 1차 방식으로 사용하지 않는다.
- 모든 워크스페이스는 공통 프레임워크 저장소의 Git 이력을 유지해야 한다.
- 고객·티켓 운영 데이터는 엔지니어 개인 소유이며 공통 저장소에 절대 포함되지 않는다.

## Alpha remote 모델

엔지니어 개인 private 운영 저장소는 회사 승인이 필요하며 아직 생성되지 않았다. 승인 전까지 각 워크스페이스는 **remote 하나**만 사용하고 고객 운영 자료는 로컬에만 보관한다.

- `origin`: 공통 private framework repository. clone과 pull 전용이다.
- 개인 운영 remote: **미승인 상태.** 생성하지 않는다.
- `customers/CUST-*`는 `.gitignore`로 Git 추적에서 제외한다. 로컬 파일로만 존재한다.
- 공통 저장소로의 push는 `.githooks/pre-push`가 기본 차단한다.

```bash
git clone <company-private-framework-repository-url> <workspace-directory>
cd <workspace-directory>
git config core.hooksPath .githooks
python3 scripts/validate_workspace.py
```

`core.hooksPath` 설정은 clone으로 전파되지 않는 로컬 config이므로 validator가 미설정 상태를 실패로 보고한다.

### 두 겹 방어의 역할 분리

| 겹 | 수단 | 막는 것 | 우회 |
|---|---|---|---|
| 1 | `.gitignore`의 `customers/CUST-*` | 고객 자료가 commit에 들어가는 것 | `git add -f`로만 가능 |
| 2 | `.githooks/pre-push` | 고객 자료·`.private/`·raw 원본이 push되는 것 | 없음 |
| 2 | `.githooks/pre-push` | 공통 저장소로의 일반 push | maintainer가 `TIKET_ALLOW_UPSTREAM_PUSH=1` 명시 |

1겹은 저장소와 함께 배포되어 설정 없이 적용된다. 2겹은 `core.hooksPath` 활성화가 필요하므로 validator가 이를 강제한다. 고객 자료 유출 차단에는 우회 경로를 두지 않는다.

### 수용한 위험

로컬 전용 보관은 백업과 이력이 없다는 뜻이다. 장비 분실이나 디스크 손상 시 고객 작업 기록이 복구되지 않는다. Alpha에서는 이를 수용하고, 판단 근거가 되는 공식 문서 URL과 결론은 티켓 파일에 반드시 기록해 재구성 가능한 상태로 둔다.

### 개인 저장소 승인 후 전환 절차

회사가 개인 private 운영 저장소를 승인하면 다음 순서로 two-remote 모델로 전환한다. 승인 전에 미리 실행하지 않는다.

```bash
git remote rename origin upstream
git remote add origin <private-workspace-repository-url>
```

1. `.gitignore`에서 `customers/CUST-*` 규칙을 제거한다.
2. `.githooks/pre-push`의 Alpha 정책 차단(공통 저장소 push 차단)을 remote 이름 기준으로 좁힌다. 고객 자료 유출 차단 겹은 유지한다.
3. `git push -u origin main`으로 개인 저장소에 첫 백업을 만든다.
4. `python3 scripts/validate_workspace.py`를 실행하고, 이 문서의 "Alpha remote 모델" 절을 two-remote 모델로 갱신한다.

전환은 공통 저장소 변경을 포함하므로 개별 워크스페이스에서 임의로 수행하지 않고 upstream 변경으로 배포한다.

## 저장소 관계

현재 개인 `tiket` repository는 운영 이력이 있는 staging/private workspace이며 공통 upstream이 아니다. 회사 framework repository는 현재 tree의 허용된 파일만 clean snapshot으로 export해 새 Git history로 시작한다. 시작 전에 공통 private repository에 대한 Git 접근 권한을 준비하고, 자격증명 값을 출력하지 않은 채 `git ls-remote <company-private-framework-repository-url> refs/heads/main`으로 읽기 권한만 확인한다.

GitHub의 “Use this template”이나 파일 복사로 시작하면 공통 Git 이력이 유지되지 않으므로 이 방식과 혼용하지 않는다.

## Alpha onboarding checklist

동료 엔지니어는 clone과 remote 설정만으로 고객 티켓 작업을 시작하지 않는다.

1. `git config core.hooksPath .githooks`로 push guard를 활성화한다. 이 설정은 clone으로 전파되지 않는다.
2. `agents/runtime-status.md`에서 blocked capability와 확인 시점을 읽는다.
3. `agents/install-verification.md`에 따라 사용하는 agent의 Skill·MCP·CLI 준비 상태를 확인한다. MCP는 `python3 scripts/verify_mcp_servers.py`로 실제 연결과 tool 경계를 확인한다.
4. `.private/customer-map.md` 등 로컬 매핑과 `customers/CUST-NNN/`은 로컬에만 생성하고 Git 추적에서 제외됨을 확인한다.
5. `python3 scripts/validate_workspace.py`와 `git diff --check`를 실행한다. 공통 upstream 배포 담당자는 추가로 `python3 scripts/test_validate_workspace.py`, `python3 scripts/test_export_framework_snapshot.py`, `python3 scripts/validate_workspace.py --framework`, `python3 scripts/check_public_sources.py`를 실행한다.
6. 비식별 합성 티켓으로 규칙 발견, no-send 경계, capability 선택, 근거·확실성 기록, 회신 스타일 선택을 smoke test한다.
7. 모든 필수 capability가 ready가 될 때까지 결과를 `unsupported` 또는 `blocked`로 처리하고 우회 도구를 임의로 사용하지 않는다.
8. Alpha 기간에는 모든 고객 회신을 사람이 검토·발송하고, 반복 실패와 교정 내용을 framework 개선 후보로 기록한다.

## Alpha scope and known limitations

- 공통 upstream이 보장하는 것은 entry rules, router, capability contract, templates, validator와 비식별 examples의 동일성이다.
- Skill, CLI, authentication과 agent별 runtime은 clone만으로 설치되지 않는다. 각 workspace가 `agents/install-verification.md`를 실행하고 unavailable capability를 명시해야 한다.
- MCP는 clone으로 전달된다. `agents/environment/mcp-manifest.json`이 정본이고 Kiro·Claude Code·Codex host 설정은 `scripts/render_agent_configs.py`가 생성한다. Hermes는 profile에 저장하므로 같은 manifest로 수동 정렬한다. `uv`는 로컬 전제조건이다.
- `customer-aws-readonly`와 `fitcloud-billing`은 v1.7.2 기준 enabled다. 각 workspace는 사용 전 `python3 scripts/test_aws_customer_skill.py`를 통과시키고 `agents/runtime-status.md`의 근거 등급(observed / operator-attested)을 확인한다.
- 현재 project-scoped Hook은 없다. 실제 반복 실패 표본과 계측 없이 Hook을 기본 활성화하지 않는다. project-scoped MCP manifest는 도입되었다.
- 동료 초대 전 Claude Code, Codex, Hermes, Kiro에 동일한 비식별 합성 티켓을 상세 steering 없이 제공해 no-send, 규칙 발견, 근거 certainty, prohibited claim, 스타일 선택을 비교한다. 미실행 agent는 Alpha 지원 범위에서 `not-verified`로 표시한다.
- Alpha는 사람 검수 전제의 내부 평가 단계이며, 네 agent의 capability parity나 자율 고객 처리를 보장하지 않는다.

## 경로 소유권

Git-only 업데이트가 충돌 없이 작동하려면 공통 프레임워크와 독립 워크스페이스의 수정 범위를 분리해야 한다.

### 공통 프레임워크 소유

다음 파일과 디렉터리의 일반 변경은 공통 저장소에 제안하고, 독립 워크스페이스에서 장기적으로 분기시키지 않는다.

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `DISTRIBUTION.md`
- `.gitignore`
- `.githooks/`
- `.kiro/steering/`
- `agents/`
- MCP 정본 `agents/environment/mcp-manifest.json`과 그로부터 생성되는 `.kiro/settings/mcp.json`, `.mcp.json`, `.claude/settings.json`, `.codex/config.toml`. 생성물은 직접 수정하지 않고 manifest를 고친 뒤 `scripts/render_agent_configs.py`로 다시 생성한다. 개인 MCP 서버는 user-level 설정에 둔다.
- `templates/`
- `examples/`의 비식별 재구성 고객 프로필과 티켓 표본
- 공통 `playbooks/` 전체. `playbooks/pitfalls/`은 standalone proof가 아니라 재검증을 요구하는 shared routing warning이다.
- `policy/cards/`의 모든 정책·가이드 카드
- `policy/_routing.md`, `policy/README.md`, `policy/pending-review.md`
- 카드의 Source ID와 상태를 검증하는 비식별 metadata인 `policy/sources.json`, `policy/source-inventory.md`
- `policy/sources.json`의 `path`로 명시되고 hash·line count가 검증되는 비식별 source excerpt
- `scripts/`
- 향후 추가되는 공통 개발환경·검증 설정

### 독립 워크스페이스 소유

공통 프레임워크는 다음 운영 자료의 기존 내용을 수정하거나 수집하지 않는다.

- `customers/` 아래의 고객 프로필과 티켓
- `.private/`
- `policy/inbox/`의 로컬 원본
- `policy/sources.json`에 등록되지 않은 로컬 추출본
- 실제 고객 식별자·연락처·계정·네트워크 매핑
- 엔지니어 개인 agent 설정과 memory

정책 카드는 source pointer, 적용 범위, 상태, 검토 기한을 보존하되 동료 workspace가 비공개 source 원문을 보유하거나 검증했다고 간주하지 않는다. `sources.json`에 등록된 비식별 excerpt는 validator가 hash와 line count를 검증한다. 그 외 `inbox/` 원본이나 로컬 추출본이 없는 workspace에서는 source 확인이 필요한 판단을 확정하지 않고 승인된 원문 위치 또는 담당자에게 확인한다.

공통 upstream의 `customers/`은 빈 운영 시작점과 인덱스만 제공한다. 실행 가능한 구조·스타일 표본은 `examples/`에 두며, 예시 reference를 실제 고객 reference나 private mapping으로 재사용하지 않는다.

## 업데이트 안전 조건

- 동료 workspace는 기본적으로 `origin/main`을 pull한다. Alpha에서 `origin`은 공통 프레임워크 저장소다.
- 업데이트 전에 working tree가 깨끗해야 한다.
- 원격 변경을 검토하지 않은 채 자동 적용하지 않는다.
- 업데이트 후 `python3 scripts/validate_workspace.py`를 실행한다.
- 공통 upstream commit 전에는 `python3 scripts/validate_workspace.py --framework`를 실행해 운영 `customers/CUST-NNN/`이 포함되지 않았는지 확인한다.
- validator 변경 후에는 `python3 scripts/test_validate_workspace.py`로 정상 후보와 주요 실패 경로를 모두 확인한다.
- Alpha tag 전에는 `python3 scripts/check_public_sources.py`로 공통 문서와 예시 evidence의 public Sources URL을 재확인한다. 일시적인 네트워크 실패는 문서 오류와 구분해 재시도하되, 확인되지 않은 URL을 통과로 간주하지 않는다.
- `examples/`가 아닌 고객 운영 자료, `.private/`, `policy/inbox/`, 미등록 로컬 추출본이 공통 프레임워크 변경에 포함되지 않았는지 확인한다.
- 공통 파일의 개선은 독립 워크스페이스에만 남기지 않고 upstream에 제안한다.

### 회사 GitHub 최초 게시

현재 개인 repository의 `.git` history를 회사 framework repository로 push하지 않는다. 아래 절차는 허용된 현재 파일만 새 디렉터리에 복사하고, 새 `main` index를 만든 뒤 validator와 regression test를 실행한다.

```bash
python3 scripts/test_export_framework_snapshot.py
python3 scripts/export_framework_snapshot.py <clean-export-directory> --init-git
cd <clean-export-directory>
git diff --cached --check
git status --short
git commit -m "feat: initialize tiket internal alpha"
git remote add origin <company-private-framework-repository-url>
git push -u origin main
```

- `git status --short`에는 framework-owned 파일의 최초 추가만 보여야 한다.
- `customers/CUST-*`, `.private/`, raw inbox 내용, 미등록 추출본, 개인 repository의 과거 commit이 포함되면 게시하지 않는다.
- 최초 push 후 remote visibility가 private인지, remote `main` SHA가 local `HEAD`와 일치하는지 읽어 확인한다.
- 회사 repository URL과 접근 정책이 확정되기 전에는 현재 개인 repository를 동료에게 common upstream으로 안내하지 않는다.

### Preview, merge, and rollback

업데이트 전에 maintainer가 공지한 Alpha tag와 commit SHA를 확인한다. 공지되지 않은 `main` 상태를 자동 적용하지 않는다. Alpha에서 공통 프레임워크 remote 이름은 `origin`이며, 개인 저장소 승인 후에는 `upstream`으로 바뀐다.

```bash
git status --short
git fetch origin --tags
git log --oneline --decorate HEAD..origin/main
git diff --stat HEAD...origin/main
git branch backup/pre-upstream-<YYYYMMDD-HHMM>
git merge --no-commit --no-ff origin/main
python3 scripts/validate_workspace.py
git diff --cached --check
git commit -m "chore: merge announced upstream alpha"
```

- 첫 명령의 출력이 비어 있지 않으면 merge를 시작하지 않는다.
- 충돌이나 검증 실패가 commit 전에 발생하면 `git merge --abort`로 되돌린다.
- merge commit은 로컬에만 남는다. Alpha에서는 push하지 않으며 `.githooks/pre-push`가 이를 차단한다.
- merge commit 후 문제가 발견되면 먼저 운영 자료를 별도 보존하고 `git revert -m 1 <merge-commit>`으로 upstream 변경만 되돌린 뒤 다시 검증한다. `git reset --hard`로 workspace 이력을 지우지 않는다.
- 각 초대 가능한 Alpha snapshot은 `alpha-YYYYMMDD.N` tag와 정확한 commit SHA로 공지한다. 회사 GitHub의 branch protection 또는 ruleset 제공 여부는 repository 생성 후 확인해 가능하면 활성화하고, 확인·적용 전에는 tag/SHA 확인과 사람 review를 필수 보완 통제로 사용한다.

## Alpha 배포 smoke test

2026-08-31 KST에 로컬 임시 bare repository를 사용해 다음 흐름을 검증했다.

1. 임시 `upstream`과 서로 다른 두 private `origin`을 생성했다.
2. 각 workspace에 서로 다른 합성 `CUST-NNN` 운영 자료를 commit했다.
3. upstream 소유 파일만 변경해 두 workspace에 merge했다.
4. 양쪽의 workspace 소유 자료 hash가 유지되고 `python3 scripts/validate_workspace.py`가 통과함을 확인했다.
5. 한 workspace에서 upstream 소유 파일을 별도로 수정한 뒤 같은 구간의 upstream 변경을 merge하여 명시적 conflict가 발생함을 확인했다.
6. 운영 `customers/` 기록을 제거하고 `examples/CUST-900/`을 포함한 최종 후보 snapshot으로 다시 실행해, 두 workspace의 local `customers/CUST-NNN/` 자료가 보존되고 양쪽 validator가 통과함을 확인했다.
7. clean exporter가 개인 repository의 commit history 없이 0-commit `main` repository를 만들고, 운영 고객·private/raw 자료를 제외한 상태에서 framework validator와 regression test를 통과함을 확인했다.

이 테스트는 Git remote·경로 소유권 모델의 동작만 검증한다. 실제 동료 onboarding은 고정된 Alpha commit에서 다시 수행하며, agent별 Skill/MCP 설치와 `aws-customer-account-ops` re-enable gate는 별도로 통과해야 한다.

## 미결정 사항

다음 항목은 아직 잠그지 않았다.

- 공통 업데이트를 감싸는 검증 스크립트 제공 여부
- 비공개 원문·로컬 추출본이 없는 배포 workspace의 source-availability 표시 방식
- 각 엔지니어의 private 운영 remote 생성·접근 승인. 회사 승인 대기 중이며, 그때까지는 "Alpha remote 모델"의 단일 remote·로컬 전용 보관을 사용한다.
- 로컬 전용 보관 기간의 고객 작업 백업 수단

공통 Skill, MCP, Hook의 재현성과 비용 검토는 `agents/shared-agent-environment.md`를 따른다. Hook은 표본 없이 기본 활성화하지 않는다.
