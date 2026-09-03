---
ticket_ref: TICKET-EXAMPLE-002
load_policy: on-demand
updated_at: 2026-08-31
---

# 티켓 이력

## 이벤트

### 2026-08-28 KST — 신규 문의 접수 및 초안 작성

- 변경 이유: 원본 AWS 계정의 Kiro 관리 구성을 대상 AWS 계정으로 변경하기 전 지원 경로와 주의사항 검토 요청
- 이전 Decision Packet/Reply Brief: 없음
- 이전 판단 또는 초안: 없음
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: 고객 계정 조회 없이 Kiro 공식 enterprise 문서로 일반 사양만 확인. 실제 identity source, profile Region, 사용자·구독·설정은 미확인.

### 2026-08-28 KST — 회신 초안 v2 개선

- 변경 이유: 권장 절차는 있었으나, 왜 대상 계정에서 새 Profile과 구독을 구성해야 하는지 고객 관점의 설명이 누락됨
- 이전 Decision Packet/Reply Brief: Decision Packet 의미는 유지. Reply Brief v1은 결론 우선, 10줄 안팎, 순서와 링크 제시였으나 권장 이유 문장 요구가 없었음.
- 이전 판단 또는 초안: 초안 v1은 대상 계정 재구성을 권고했으나 Kiro Profile이 AWS 계정·리전에 귀속된다는 이유를 결론 직후 설명하지 않았음
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: F1의 공식 Kiro concepts 근거를 사용해 권고 이유 한 문장을 추가함. 기술 결론과 certainty는 변경 없음.

### 2026-08-28 KST — 기존 IAM Identity Center 사용 정황 추가

- 변경 이유: 운영자가 원본 계정의 IAM Identity Center에 대상 사용자들이 이미 존재한다고 기억함
- 이전 Decision Packet/Reply Brief: 변경 없음
- 이전 판단 또는 초안: Identity Provider 유형이 미확인인 상태로 신규 연결 가능성을 모두 열어둠
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: 운영자 기억이므로 H1 hypothesis로 기록. 대상 계정의 동일 Organization 소속 여부와 IdC organization instance 여부 확인 전에는 기존 사용자를 그대로 재사용할 수 있다고 확정하지 않음.

### 2026-08-28 KST — Cross-account 사용자 구독 지원 구조 확인

- 변경 이유: Kiro member account에서 다른 계정이 관리하는 Identity Center 사용자를 선택할 수 있는지 확인 요청
- 이전 Decision Packet/Reply Brief: D1의 근거에 F8 추가. Reply Brief 의미는 유지.
- 이전 판단 또는 초안: 같은 Organization과 organization instance 조건부로 가능하다고 판단
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: 첨부 화면은 Kiro Profile에 연결된 디렉터리의 사용자 검색 UI임을 보여주지만 디렉터리 범위는 증명하지 못함. Kiro 공식 deployment option F8에서 management account의 IdC와 member account의 Kiro profile·사용자 구독 조합을 명시적으로 확인함.

### 2026-08-28 KST — 계정 간 구독 재할당 공개 사례 확인

- 변경 이유: Kiro Profile 또는 구독의 AWS 계정 간 변경 유즈케이스 요청
- 이전 Decision Packet/Reply Brief: 변경 없음
- 이전 판단 또는 초안: 공식 지원 구조만 확인되어 공개 운영 사례는 미확인
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: GitHub #7747에서 같은 Organization 내 동일 사용자 구독을 새 계정에 활성화하고 기존 구독을 해지한 실제 사례를 확인했으나 Pending/CLI 장애가 발생했고 아직 maintainer 해결 답변이 없음. re:Post에는 중앙 IdC를 사용한 member-account Kiro onboarding 절차가 있음. Profile 자체의 설정·이력 이전 성공 사례는 확인되지 않음.

### 2026-08-28 KST — 공개 장애 사례를 반영한 초안 v3 작성

- 변경 이유: 초안 v2의 절차대로 전환할 경우 GitHub #7747과 같은 Pending/CLI 장애가 발생할 수 있다는 검토 의견 및 번호 항목 가독성 개선 요청
- 이전 Decision Packet/Reply Brief: D1에 F10, D2에 F9를 추가하고 Reply Brief에 공개 사례 및 번호별 줄바꿈 요구를 반영
- 이전 판단 또는 초안: 초안 v2는 대상 계정 재구성 후 Pilot 검증을 권고했으나 실제 장애 사례와 일괄 전환 금지 이유가 회신에 드러나지 않았음
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: 초안 v3은 같은 Organization과 organization instance를 조건으로 기존 사용자 재사용 가능성을 안내하고, Pilot 1명 구독의 Active 상태와 IDE·CLI 로그인을 확인한 후 순차 전환하도록 제한함.

### 2026-08-28 KST — 사용자 문안을 반영한 초안 v4 작성

- 변경 이유: 결론, 공개 장애 사례, 단계별 전환 순서를 고객 관점에서 더 직접적으로 표현하고 번호 항목 사이의 간격을 확보
- 이전 Decision Packet/Reply Brief: 변경 없음
- 이전 판단 또는 초안: 초안 v3은 조건 설명이 앞에 길게 배치되어 실제 권장 절차의 핵심이 상대적으로 약했음
- 실제 발송/고객 회신: 실제 발송 없음
- 근거와 제한: 공식 문서에서 직접 이전 기능이나 별도 migration 절차를 확인하지 못했다는 조사 범위 표현을 사용하고, 기능 부재를 절대 단정하지 않음. 대상 계정에서 기존 Identity Center 사용자가 실제 조회되는지 먼저 확인하며, Pilot 사용자의 Active 상태와 재로그인 후 IDE·CLI 동작을 확인한 다음 기존 구독을 해지하도록 명시함.

### 2026-08-28 KST — 고객 회신 발송

- 변경 이유: 사용자 최종 검토 후 Kiro 관리 계정 변경 사전 검토 회신 발송
- 이전 Decision Packet/Reply Brief: 변경 없음
- 이전 판단 또는 초안: 초안 v4를 기반으로 문장부호와 표현을 자연스럽게 조정
- 실제 발송/고객 회신: 공식 문서에서 Profile 직접 이전 기능·절차가 확인되지 않았음을 먼저 설명하고, GitHub #7747의 Pending 사례를 근거로 Pilot 1명 검증 → 재로그인 및 IDE·CLI 확인 → 기존 구독 해지 → 나머지 순차 전환을 안내함
- 근거와 제한: 실제 발송본의 첫 번째 절차에는 번호 `1.`이 표시되지 않았으나 내용상 1단계임. 고객 응답은 아직 없음.

### 2026-08-28 KST — 회신 스타일 프로필 태깅

- 변경 이유: 공통 Reply Brief에 이름 있는 presentation profile을 도입
- 이전 Decision Packet/Reply Brief: 기술 의미와 선택 ID는 유지하고 `presentation.profile: seungdo-compact`를 추가함. 기존 반복 형식 요구는 공통 스타일 문서로 이동함.
- 이전 판단 또는 초안: 변경 없음
- 실제 발송/고객 회신: 변경 없음
- 근거와 제한: 실제 발송본을 `승도 스타일`의 기준 표본으로 사용하되, 발송문 자체는 수정하지 않음.

### 2026-08-28 KST — 승도 스타일의 길이 기준 교정

- 변경 이유: `compact`와 10줄 안팎이라는 표현이 짧은 회신을 목표로 오해하게 만들 수 있다는 사용자 교정
- 이전 Decision Packet/Reply Brief: 기술 의미와 선택 ID는 유지하고 profile 이름을 `seungdo-contextual`로 변경함.
- 이전 판단 또는 초안: 승도 스타일을 약 10줄의 간결한 회신으로 정의했음
- 실제 발송/고객 회신: 변경 없음
- 근거와 제한: 승도 스타일은 고정 길이가 아니라 고객이 결론·이유·절차를 이해하는 데 필요한 설명량을 티켓 맥락에 맞춰 결정함. 상세 설명형은 장문 여부가 아니라 체계적인 참조 문서가 필요한 경우로 구분함.

### 2026-08-28 KST — 승도 스타일의 해결 목표 기준 보강

- 변경 이유: `왜 필요한가`의 설명보다 고객의 잠재된 고민과 실제 해결 목표를 파악해 후속 의문을 선제적으로 해소하는 것이 핵심이라는 사용자 교정
- 이전 Decision Packet/Reply Brief: 기술 의미, 선택 ID, profile 이름은 변경 없음
- 이전 판단 또는 초안: 고객 이해를 위해 결론의 이유를 필요한 만큼 설명하는 스타일로 정의함
- 실제 발송/고객 회신: 변경 없음
- 근거와 제한: 합리적으로 예상되는 적용 조건·실패 가능성·기존 구성 영향·위험·확인 방법·오류 대응을 선제적으로 포함하되, 확인되지 않은 고객 의도를 단정하거나 무관한 가능성을 모두 나열하지 않도록 정의함.

### 2026-08-31 KST — GitHub 공개 사례 상태 교정

- 변경 이유: Alpha 공유 전 외부 근거의 현재 상태 재검증
- 이전 Decision Packet/Reply Brief: 기술 판단과 선택 ID는 변경 없음
- 이전 판단 또는 초안: 2026-08-28 이력에는 GitHub #7747에 maintainer 해결 답변이 없다고만 기록함
- 실제 발송/고객 회신: 변경 없음
- 근거와 제한: 해결 방법은 제시되지 않았지만, contributor가 2026-08-17 장기 비활성과 최신 재현 정보 부족을 이유로 이슈를 `not_planned` 종료한 사실을 확인함. 공개 장애 사례는 Pilot 권고의 보조 근거로만 유지하며 현재 버전에서도 재현된다고 단정하지 않음.

## 비식별 실제 발송본

아래 block은 실제 발송 문구와 순서를 보존하되, 공통 upstream 공유를 위해 작성자 소개와 고객 account alias만 placeholder/reference로 치환했다. 첫 번째 절차에 번호가 없었던 원문 형식도 그대로 유지한다.

```text
안녕하세요.
[작성자 소개]

확인 결과, AWS 공식 문서에서는 Kiro Profile을 다른 계정으로 직접 이전하는 기능이나 별도 이전 절차가 확인되지 않았습니다.

또한 Kiro GitHub에는 다른 계정으로 구독을 변경한 뒤 신규 구독이 Pending 상태에 머물고 동작하지 않은 사례가 있습니다.
https://github.com/kirodotdev/Kiro/issues/7747

따라서 전체 사용자를 한 번에 전환하기보다 아래 순서로 진행하는 것을 권장드립니다.

대상 계정(`ACCOUNT-002`)의 Kiro 사용자 추가 화면에서 기존 Identity Center 사용자가 조회되는지 확인하고, 조회되는 사용자 1명에게 테스트로 구독을 추가합니다.

2. 신규 구독이 Active인지 확인하고, 해당 사용자가 Kiro에서 로그아웃 후 재로그인하여 IDE·CLI가 정상 동작하는지 확인합니다.

3. 정상 동작을 확인한 후 기존 계정(`ACCOUNT-001`)에서 해당 사용자의 기존 Kiro 구독을 해지합니다.

4. 동일한 방식으로 나머지 사용자를 순차 전환합니다.

진행 중 오류가 발생하거나 Kiro를 사용할 수 없는 경우 메시지로 공유해 주시면 확인을 도와드리겠습니다.

감사합니다.
```

Append only. Never rewrite prior judgment, sent replies, customer responses, packets, briefs, or superseded drafts.
