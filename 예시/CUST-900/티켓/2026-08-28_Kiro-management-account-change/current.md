---
title: Kiro 관리 Account 변경 사전 검토
customer_ref: CUST-900
example_provenance: de-identified-reconstruction
operational_owner: none
account_ref: ACCOUNT-001
target_account_ref: ACCOUNT-002
date: 2026-08-28
status: 회신완료
source_ref: TICKET-EXAMPLE-002
tags: [티켓, Kiro, 계정변경]
policy_ids: []
poc_id: ""
decision_packet_version: 2
current_revision: v4
evidence_file: evidence.md
history_file: history.md
---

# Kiro 관리 Account 변경 사전 검토

## 요청 내용

### 고객이 실제로 묻는 것

- 기존 AWS 계정에서 관리 중인 Kiro 구성을 새 AWS 계정으로 옮길 때 단순 재설정하면 되는지, 별도 이전 방법과 주의사항이 있는지 확인 요청

### 비식별 원문

- 원본 계정에서 사용 중인 Kiro 관리 구성을 이미 Kiro를 활성화한 대상 계정으로 변경하고자 함
- 작업 전 권장 절차, 대안 및 주의사항 안내 요청

## 현재 상태

- 작업 tier: standard
- 최신 evidence 확인일: 2026-08-31
- 최신 실제 발송: 2026-08-28 KST
- 적용 정책: 없음 (`policy_ids: []`)
- 차단 capability: 고객 AWS 리소스 조회 미사용; 공식 Kiro 문서만으로 일반 사양 검토

## 결정 패킷

```json
{
  "version": 2,
  "tier": "standard",
  "question": "기존 AWS 계정의 Kiro 관리 구성을 다른 AWS 계정으로 변경할 때 지원 경로와 주의사항은 무엇인가?",
  "decisions": [
    {
      "id": "D1",
      "item": "Kiro profile은 AWS 계정과 리전에 귀속되므로 대상 계정에서 별도 profile과 구독을 구성한다.",
      "result": "yes",
      "certainty": "confirmed",
      "conditions": [],
      "fact_ids": ["F1", "F2", "F8", "F10"],
      "hypothesis_ids": [],
      "unknown_ids": []
    },
    {
      "id": "D2",
      "item": "대상 profile에 identity, 사용자·그룹·tier 및 관리 설정을 재구성한 뒤 pilot 로그인을 검증하고 원본 구독을 해지한다.",
      "result": "conditional",
      "certainty": "confirmed",
      "conditions": ["현재 identity source와 profile 설정을 먼저 목록화", "대상 계정에서 pilot 사용자 검증 완료"],
      "fact_ids": ["F2", "F3", "F5", "F6", "F7", "F9"],
      "hypothesis_ids": [],
      "unknown_ids": ["U1", "U2"]
    },
    {
      "id": "D3",
      "item": "원본과 대상 profile에 같은 사용자를 동시에 구독한 기간에는 이중 과금될 수 있으므로 중복 기간을 최소화한다.",
      "result": "yes",
      "certainty": "confirmed",
      "conditions": [],
      "fact_ids": ["F4"],
      "hypothesis_ids": [],
      "unknown_ids": []
    }
  ],
  "policy_ids": [],
  "actions": {
    "customer": [
      {"id": "A1", "action": "현재 identity source, Kiro profile Region, 구독 사용자·그룹·tier와 주요 Settings를 확인한다."},
      {"id": "A2", "action": "대상 계정에서 재구성 후 pilot 사용자 로그인을 검증하고 원본 구독을 해지한다."}
    ],
    "internal": [
      {"id": "I1", "action": "고객이 identity source와 Organization 관계를 회신하면 해당 방식의 상세 체크리스트를 제공한다."}
    ]
  },
  "prohibited_claims": [
    {"id": "P1", "claim": "기존 Kiro profile과 설정·구독이 대상 계정으로 자동 이전된다."},
    {"id": "P2", "claim": "중복 구독 기간에도 추가 과금이 없다."}
  ]
}
```

## 회신 브리프

```json
{
  "version": 2,
  "audience": {"role_ref": "CONTACT-001", "technical_depth": "standard"},
  "goal": "Kiro 관리 계정 변경의 권장 절차와 핵심 주의사항을 짧게 안내",
  "decision_ids": ["D1", "D2", "D3"],
  "fact_ids": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"],
  "hypothesis_ids": [],
  "unknown_ids": ["U1", "U2"],
  "customer_action_ids": ["A1", "A2"],
  "internal_action_ids": [],
  "prohibited_claim_ids": ["P1", "P2"],
  "presentation": {
    "profile": "seungdo-contextual",
    "tone": "formal-korean",
    "structure": "conclusion-first",
    "commands": "on-request"
  },
  "presentation_requirements": ["공식 문서 링크와 공개 사례 링크를 단독 줄로 표시"],
  "avoid_topics": ["고객 계정 리소스 조회 결과처럼 표현", "내부 capability 상태"]
}
```

## 현재 판단

- Kiro profile 자체를 계정 간 이동하는 것이 아니라 대상 계정에서 profile, subscriptions, identity 연결 및 profile settings를 재구성하는 방식이 적합함
- 대상 profile 검증 전 원본 profile 또는 구독을 먼저 삭제하지 않음
- 동일 사용자의 profile 간 중복 구독과 월 중 해지 과금 조건을 사전 안내함
- 동일 Organization 내 계정 간 구독 재할당 후 신규 구독이 Pending에 머물고 CLI가 실패한 공개 사례가 있으므로 일괄 전환하지 않고 Pilot 1명으로 검증함

## 회신

### 현재 비식별 reference rendering

실제 발송 artifact는 `history.md`의 `비식별 실제 발송본`에 보존한다. 이 rendering은 저장소 공유를 위해 작성자 소개와 고객 계정 alias만 비식별 reference로 치환했다.

```text
안녕하세요.
[작성자 소개]

확인 결과, AWS 공식 문서에서는 Kiro Profile을 다른 계정으로 직접 이전하는 기능이나 별도 이전 절차가 확인되지 않았습니다.

또한 Kiro GitHub에는 다른 계정으로 구독을 변경한 뒤 신규 구독이 Pending 상태에 머물고 동작하지 않은 사례가 있습니다.
https://github.com/kirodotdev/Kiro/issues/7747

따라서 전체 사용자를 한 번에 전환하기보다 아래 순서로 진행하는 것을 권장드립니다.

1. 대상 계정(`ACCOUNT-002`)의 Kiro 사용자 추가 화면에서 기존 Identity Center 사용자가 조회되는지 확인하고, 조회되는 사용자 1명에게 테스트로 구독을 추가합니다.

2. 신규 구독이 Active인지 확인하고, 해당 사용자가 Kiro에서 로그아웃 후 재로그인하여 IDE·CLI가 정상 동작하는지 확인합니다.

3. 정상 동작을 확인한 후 기존 계정(`ACCOUNT-001`)에서 해당 사용자의 기존 Kiro 구독을 해지합니다.

4. 동일한 방식으로 나머지 사용자를 순차 전환합니다.

진행 중 오류가 발생하거나 Kiro를 사용할 수 없는 경우 메시지로 공유해 주시면 확인을 도와드리겠습니다.

감사합니다.
```

## 고객 회신

- 2026-08-28 KST 회신 발송 완료. 비식별 실제 발송본은 `history.md`에 보존함.

## 다음 액션

- [x] 사용자 검토 후 회신 발송
- [ ] 고객이 identity source와 AWS Organizations 관계를 제공하면 상세 절차 보완

## 파일 연결

- 근거: `evidence.md`
- 이력: `history.md` — on-demand only
