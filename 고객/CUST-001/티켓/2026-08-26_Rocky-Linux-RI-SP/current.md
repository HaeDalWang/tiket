---
title: Rocky Linux EC2의 RI 및 Savings Plans 적용 문의
customer_ref: CUST-001
account_ref: ACCOUNT-001
date: 2026-08-26
status: 초안작성
source_ref: TICKET-LOCAL-001
tags: [티켓, EC2, Rocky-Linux, Reserved-Instances, Savings-Plans]
policy_ids: [POLICY-SEC-001, POLICY-PAYER-001, POLICY-COST-ESC-001]
poc_id: ""
decision_packet_version: 2
current_revision: v4
evidence_file: evidence.md
history_file: history.md
---

# Rocky Linux EC2의 RI 및 Savings Plans 적용 문의

## 요청 내용

### 고객이 실제로 묻는 것

`ACCOUNT-001`에서 Rocky Linux를 사용하는 EC2 인스턴스가 EC2 Reserved Instances(RI) 또는 Savings Plans(SP) 할인 적용 대상인지 확인해 달라는 요청이다. 고객은 과거 CentOS 또는 Red Hat 계열에서 `Linux/UNIX` RI가 예상대로 적용되지 않았던 경험을 언급했다.

### 원문

> 안녕하세요 [MASKED:customer] [MASKED:contact]입니다.
>
> [ACCOUNT-001] 계정에 몇몇 인스턴스에 Rocky Linux 를 사용 중인게 있는데
> RI 나 SP 에 적용이 되는지 확인차 문의드렸습니다.
>
> 기존에 CentOS나 Redhat 계열 리눅스의 경우 기본 Linux/Unix 플랫폼으로 선택하면 적용이 안되었던 경우가 있었던거 같아서 확인차 문의드립니다.
>
> 확인부탁드리겠습니다.
> 감사합니다.
>
> [MASKED:signature]

## 현재 상태

- 작업 tier: `standard`
- 최신 revision: `v4` (2026-08-26 14:26 KST)
- 최신 evidence: `evidence.md`의 F1~F5, H1~H2, U1~U4
- 최신 실제 발송: 1차 접수 회신 완료 — 원문은 `history.md`
- 적용 정책: `POLICY-SEC-001`, `POLICY-PAYER-001`, `POLICY-COST-ESC-001`
- CSR handoff: 미실행; 사람이 Slack `@csr` 게시 후 시각 기록
- 차단 capability: `customer-aws-readonly`, `fitcloud-billing`

## 결정 패킷

### v2 (current)

```json
{
  "version": 2,
  "tier": "standard",
  "question": "ACCOUNT-001의 Rocky Linux EC2 instance에 EC2 RI 또는 Savings Plans 할인을 적용할 수 있는가",
  "decisions": [
    {
      "id": "D1",
      "item": "Rocky Linux라는 OS 자체가 Savings Plans 적용을 배제하는가",
      "result": "no",
      "certainty": "confirmed",
      "conditions": [],
      "fact_ids": ["F3", "F4"],
      "hypothesis_ids": [],
      "unknown_ids": []
    },
    {
      "id": "D2",
      "item": "Linux/UNIX RI 적용 가능 여부",
      "result": "conditional",
      "certainty": "confirmed",
      "conditions": [
        "대상 instance의 Platform details / Usage operation이 Linux/UNIX / RunInstances일 것",
        "RI scope에 따른 Region/AZ, family, size, tenancy, platform matching condition을 충족할 것"
      ],
      "fact_ids": ["F1", "F2"],
      "hypothesis_ids": [],
      "unknown_ids": ["U1", "U3"]
    },
    {
      "id": "D3",
      "item": "Compute Savings Plans에서 Rocky Linux 사용이 제한 조건인가",
      "result": "no",
      "certainty": "confirmed",
      "conditions": ["Compute Savings Plans의 EC2 적용 범위일 것"],
      "fact_ids": ["F3"],
      "hypothesis_ids": [],
      "unknown_ids": []
    },
    {
      "id": "D4",
      "item": "EC2 Instance Savings Plans 적용 가능 여부",
      "result": "conditional",
      "certainty": "confirmed",
      "conditions": ["약정한 Region과 instance family 범위 안일 것"],
      "fact_ids": ["F4"],
      "hypothesis_ids": [],
      "unknown_ids": ["U3"]
    },
    {
      "id": "D5",
      "item": "과거 CentOS/RHEL 계열 RI 미적용 원인",
      "result": "unknown",
      "certainty": "hypothesis",
      "conditions": ["당시 instance와 RI의 platform 및 기타 matching condition 대조 필요"],
      "fact_ids": ["F1", "F2"],
      "hypothesis_ids": ["H1"],
      "unknown_ids": ["U4"]
    },
    {
      "id": "D6",
      "item": "Marketplace seller software charge가 별도로 남을 수 있는가",
      "result": "conditional",
      "certainty": "confirmed",
      "conditions": ["Paid Marketplace AMI를 사용하는 경우"],
      "fact_ids": ["F3", "F4", "F5"],
      "hypothesis_ids": [],
      "unknown_ids": ["U2"]
    }
  ],
  "policy_ids": ["POLICY-SEC-001", "POLICY-PAYER-001", "POLICY-COST-ESC-001"],
  "actions": {
    "customer": [
      {"id": "A1", "action": "대상 instance의 Platform details / Usage operation을 확인해 회신"},
      {"id": "A2", "action": "대상 instance의 Region과 instance type을 회신"},
      {"id": "A3", "action": "Marketplace AMI인 경우 Free/Paid product 여부를 확인"}
    ],
    "internal": [
      {"id": "I1", "action": "사람이 최종 검토 후 Zendesk email 발송"},
      {"id": "I2", "action": "POLICY-COST-ESC-001에 따라 사람이 Slack @csr handoff 게시 후 시각 기록"}
    ]
  },
  "prohibited_claims": [
    {"id": "P1", "claim": "실제 Platform details와 matching condition 확인 전에 대상 instance의 RI 적용을 확정"},
    {"id": "P2", "claim": "FitCloud-curated 근거 없이 구체적 절감 금액, 절감률, 비용 수치를 제시"},
    {"id": "P3", "claim": "과거 CentOS/RHEL 미적용 원인을 확정"},
    {"id": "P4", "claim": "현재 보유 약정과 Payer 공유 범위 확인 전에 특정 RI/SP 구매나 coverage를 확약"},
    {"id": "P5", "claim": "고객 AWS/FitCloud 계정을 실측한 것처럼 표현"}
  ]
}
```

## 회신 브리프

### v2 (current)

```json
{
  "version": 2,
  "audience": {"role_ref": "CONTACT-001", "technical_depth": "standard"},
  "goal": "Rocky Linux 자체는 RI/SP 제외 사유가 아니라는 결론과 개별 instance 확정 조건을 간결히 전달한다",
  "decision_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
  "fact_ids": ["F1", "F2", "F3", "F4", "F5"],
  "hypothesis_ids": ["H1"],
  "unknown_ids": ["U1", "U2", "U3", "U4"],
  "customer_action_ids": ["A1", "A2", "A3"],
  "internal_action_ids": [],
  "prohibited_claim_ids": ["P1", "P2", "P3", "P4", "P5"],
  "presentation": {
    "tone": "formal-korean",
    "structure": "conclusion-first",
    "commands": "none"
  },
  "presentation_requirements": [
    "RI와 Savings Plans를 별도 항목으로 구분",
    "과거 CentOS/RHEL 사례는 가능성으로만 설명",
    "확인 요청 값은 한 문단으로 정리"
  ],
  "avoid_topics": [
    "구체적 비용 수치와 절감률",
    "특정 RI/SP 구매 권고",
    "고객 계정을 실측한 것처럼 보이는 표현"
  ]
}
```

## 현재 판단

- 최신 의미 계약은 위 Decision Packet v2이다. 이 section은 새로운 기술적 의미를 추가하지 않는다.
- 대상 instance의 실제 RI 적용과 구매 권고는 U1/U3가 해소되기 전까지 확정하지 않는다.

## 회신

### 현재 초안 v4 (검수 대기)

```text
안녕하세요, 부장님.

문의주신 Rocky Linux 인스턴스의 RI 및 Savings Plans 적용 여부를 확인하여 안내드립니다.

결론부터 말씀드리면, Rocky Linux라는 운영체제 자체는 RI나 Savings Plans 적용을 막는 조건이 아닙니다. 다만 개별 인스턴스에 실제로 적용되는지는 AMI의 과금 플랫폼과 RI/SP의 적용 조건을 함께 확인해야 합니다.

- RI: 대상 인스턴스의 `Platform details`가 `Linux/UNIX`(`Usage operation: RunInstances`)로 표시되면 `Linux/UNIX` RI의 플랫폼 조건에 해당합니다. 이와 함께 RI의 범위에 따라 Region/가용 영역, 인스턴스 패밀리·사이즈, tenancy 등의 일치 여부를 확인해야 합니다.
- Savings Plans: Compute Savings Plans는 운영체제와 무관하게 EC2 사용량에 적용됩니다. EC2 Instance Savings Plans도 약정한 Region과 인스턴스 패밀리 범위 안에서는 운영체제와 무관하게 적용됩니다.

말씀하신 과거 CentOS/RHEL 계열 사례는 RHEL이 `Red Hat Enterprise Linux`라는 별도 플랫폼으로 구분되었거나, 다른 RI 일치 조건이 충족되지 않았을 가능성이 있습니다. 다만 당시 정보를 확인하지 않은 상태에서 정확한 원인을 단정하기는 어렵습니다.

또한 AWS Marketplace의 유료 AMI를 사용 중인 경우에는 EC2 사용료와 별도인 판매자 소프트웨어 요금이 남을 수 있으므로 해당 상품의 요금 유형도 함께 확인이 필요합니다.

정확한 확인을 위해 EC2 콘솔에서 대상 인스턴스의 `Platform details`, `Usage operation`, Region, 인스턴스 타입을 확인하여 회신 부탁드립니다. Marketplace AMI인 경우 Free/Paid 상품 여부도 함께 알려주시면, 해당 값을 기준으로 적용 조건을 최종 안내드리겠습니다.

감사합니다.
```

## 고객 회신

- 아직 추가 고객 회신 없음

## 다음 액션

- [ ] 고객에게 대상 인스턴스의 `Platform details` / `Usage operation` 값 요청 (회신 초안 v4에 포함)
- [ ] 사용 중인 Rocky Linux AMI가 공식 무료 목록인지 third-party 유료 목록인지 확인
- [ ] 대상 인스턴스의 Region, family, size, tenancy 확인
- [ ] 기존 RI/SP 및 Payer 공유 범위 확인
- [ ] 확인 결과에 따라 조건부 문구를 확정 문구로 갱신
- [ ] 사람이 최종 검토 후 Zendesk email로 발송 (에이전트 발송 금지)
- [ ] `POLICY-COST-ESC-001`에 따라 사람이 Slack `@csr` handoff 게시 후 시각 기록 (RI/SP 문의는 비용 문의 범주)
- [ ] 함정 문서 참조: `플레이북/함정/ec2-ri-sp-플랫폼과-마켓플레이스-요금.md`

---

## 파일 연결

- 근거: `evidence.md`
- 전체 이력: `history.md` — on-demand only
