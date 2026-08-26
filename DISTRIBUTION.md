# 배포 및 동기화 원칙

이 문서는 `tiket` 프레임워크를 동료 엔지니어의 독립 워크스페이스에 배포하고 업데이트하는 1차 원칙을 정의한다.

## 잠긴 결정

- 각 엔지니어는 고객·티켓 운영 데이터를 자기 private Git 저장소에서 독립적으로 관리한다.
- 공통 프레임워크 업데이트는 Git remote와 pull/merge만으로 전달한다.
- 프로젝트 폴더 전체 ZIP, GitHub Template 기반 복제, Copier 같은 별도 템플릿 업데이트 도구는 1차 방식으로 사용하지 않는다.
- 모든 워크스페이스는 공통 프레임워크 저장소의 Git 이력을 유지해야 한다.

## 저장소 관계

각 독립 워크스페이스는 remote 두 개를 사용한다.

- `origin`: 엔지니어 개인 또는 담당 범위의 private 운영 저장소
- `upstream`: 공통 프레임워크 저장소

새 워크스페이스는 공통 프레임워크를 clone한 뒤 기존 remote를 `upstream`으로 바꾸고 자기 private 저장소를 `origin`으로 추가한다.

```bash
git clone <framework-repository-url> <workspace-directory>
cd <workspace-directory>
git remote rename origin upstream
git remote add origin <private-workspace-repository-url>
git push -u origin main
```

GitHub의 “Use this template”이나 파일 복사로 시작하면 공통 Git 이력이 유지되지 않으므로 이 방식과 혼용하지 않는다.

## 경로 소유권

Git-only 업데이트가 충돌 없이 작동하려면 공통 프레임워크와 독립 워크스페이스의 수정 범위를 분리해야 한다.

### 공통 프레임워크 소유

다음 파일과 디렉터리의 일반 변경은 공통 저장소에 제안하고, 독립 워크스페이스에서 장기적으로 분기시키지 않는다.

- `AGENTS.md`
- `CLAUDE.md`
- `.kiro/steering/`
- `에이전트/`
- `템플릿/`
- 공통 `플레이북/` 중 `플레이북/함정/`을 제외한 확정 모듈
- `회사규정/카드/`의 모든 정책·가이드 카드
- `회사규정/_라우팅.md`, `회사규정/README.md`, `회사규정/검토_대기.md`
- 카드의 Source ID와 상태를 검증하는 비식별 metadata인 `회사규정/sources.json`, `회사규정/원본_목록.md`
- `scripts/validate_workspace.py`
- 향후 추가되는 공통 개발환경·검증 설정

### 독립 워크스페이스 소유

공통 프레임워크는 다음 운영 자료의 기존 내용을 수정하거나 수집하지 않는다.

- `고객/` 아래의 고객 프로필과 티켓
- `.private/`
- `회사규정/수신함/`의 로컬 원본
- `회사규정/추출본/`
- `플레이북/함정/`
- 실제 고객 식별자·연락처·계정·네트워크 매핑
- 엔지니어 개인 agent 설정과 memory

정책 카드는 source pointer, 적용 범위, 상태, 검토 기한을 보존하되 동료 workspace가 source 원문을 보유하거나 검증했다고 간주하지 않는다. `수신함/`과 `추출본/`이 없는 workspace에서는 source 확인이 필요한 판단을 확정하지 않고 승인된 원문 위치 또는 담당자에게 확인한다.

`플레이북/함정/`의 공통 upstream 포함 여부는 보류한다. 보류 기간에는 각 workspace의 함정을 자동으로 상호 배포하거나 공통 사실로 승격하지 않는다.

## 업데이트 안전 조건

- 업데이트 전에 working tree가 깨끗해야 한다.
- 원격 변경을 검토하지 않은 채 자동 적용하지 않는다.
- 업데이트 후 `python3 scripts/validate_workspace.py`를 실행한다.
- 고객 운영 자료, `.private/`, `회사규정/수신함/`, `회사규정/추출본/`, `플레이북/함정/`이 공통 프레임워크 변경에 포함되지 않았는지 확인한다.
- 공통 파일의 개선은 독립 워크스페이스에만 남기지 않고 upstream에 제안한다.

## 미결정 사항

다음 항목은 아직 잠그지 않았다.

- 엔지니어가 따라갈 upstream 브랜치 또는 release 기준
- 공통 업데이트를 감싸는 검증 스크립트 제공 여부
- `플레이북/함정/`의 공통 upstream 포함 여부와 승격 기준
- 추출본 없는 배포 workspace를 지원하는 validator mode와 source-availability 표시 방식
- 프레임워크 저장소와 현재 운영 저장소의 실제 분리 시점
