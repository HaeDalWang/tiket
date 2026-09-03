---
example_type: presentation-only
presentation_profile: technical-detailed
source_packet: ../CUST-900/tickets/2026-08-26_Rocky-Linux-RI-SP/current.md
source_evidence: ../CUST-900/tickets/2026-08-26_Rocky-Linux-RI-SP/evidence.md
selected_decision_ids: [D1, D2, D3, D4, D5, D6]
selected_fact_ids: [F1, F2, F3, F4, F5]
selected_hypothesis_ids: [H1]
selected_unknown_ids: [U1, U2, U3, U4]
---

# Rocky Linux RI·Savings Plans 적용 검토 — 상세 설명형 예시

이 문서는 동일 Decision Packet을 `technical-detailed`로 표현한 **presentation-only 표본**이다. 실제 발송문이나 별도 기술 판단이 아니며, 원본 packet·evidence의 ID, certainty, unknown과 prohibited claim을 변경하지 않는다.

## 결론과 적용 범위

Rocky Linux라는 OS 이름 자체는 RI 또는 Savings Plans 적용 제외 조건이 아니다. 다만 개별 인스턴스의 실제 할인 적용 여부는 AMI의 과금 플랫폼과 약정별 일치 조건을 확인한 뒤 확정해야 한다.

현재 고객 계정과 FitCloud는 조회하지 않았으므로, 아래 내용은 공식 사양과 공개 AMI 정보를 기준으로 한 조건부 검토다. 특정 인스턴스의 coverage나 구매 권고로 해석하면 안 된다.

## 할인 방식별 판단 기준

| 구분 | Rocky Linux 관련 결론 | 추가 확인 조건 |
|---|---|---|
| EC2 Reserved Instances | `Platform details`가 `Linux/UNIX`이고 `Usage operation`이 `RunInstances`라면 Linux/UNIX 플랫폼 조건에 해당할 수 있다. | RI 범위에 따라 Region 또는 AZ, instance family·size, tenancy와 platform 일치 여부를 확인한다. |
| Compute Savings Plans | OS 종류 자체가 적용 범위를 제한하지 않는다. | 약정 범위, eligible usage, 현재 coverage를 확인한다. |
| EC2 Instance Savings Plans | OS 종류 자체가 적용 범위를 제한하지 않는다. | 약정한 Region과 instance family 범위, 현재 coverage를 확인한다. |
| Marketplace AMI | EC2 compute 사용량 할인과 판매자 소프트웨어 요금은 별도일 수 있다. | 사용 AMI가 공식 무료 이미지인지 third-party 유료 상품인지 확인한다. |

## 과거 CentOS·RHEL 사례를 그대로 비교할 수 없는 이유

과거 미적용 사례는 당시 AMI의 실제 platform, RI 속성, Region/AZ, family·size, tenancy 또는 Marketplace 상품 여부가 확인되지 않았다. 특히 RHEL은 별도 유료 platform으로 분류될 수 있으므로 Rocky Linux와 이름만으로 같은 조건이라고 단정할 수 없다.

따라서 과거 사례는 `H1` 가설로만 유지하고, 현재 Rocky Linux 인스턴스의 값을 먼저 확인한다.

## 확인된 사실과 미확정 값

### 확인된 사실

- `F1`~`F5`: RI platform 일치 조건, Savings Plans의 OS 유연성, 공개 Rocky Linux AMI의 `Linux/UNIX` 분류, Marketplace 소프트웨어 요금 분리 가능성은 원본 evidence에 기록되어 있다.

### 미확정 값

- `U1`: 대상 인스턴스의 `Platform details`와 `Usage operation`
- `U2`: 사용 AMI의 무료·유료 Marketplace 상품 여부
- `U3`: 대상 인스턴스의 Region, family, size, tenancy
- `U4`: 현재 RI/SP 보유 내역, Payer 공유 범위와 실제 coverage

이 값이 해소되기 전에는 특정 인스턴스의 할인 적용이나 구매 방향을 확정하지 않는다.

## 안전한 확인 순서

1. EC2 콘솔에서 대상 인스턴스의 `Platform details`, `Usage operation`, Region과 instance type을 확인한다.

2. AMI가 Rocky Linux 공식 무료 이미지인지, Marketplace의 third-party 유료 상품인지 확인한다.

3. 현재 보유 RI/SP의 범위와 Payer 공유 조건을 확인한다.

4. 고객에게 제시할 비용·절감 수치는 raw AWS billing이 아니라 FitCloud-curated 근거로 최종 검증한다.

## 근거와 재검증

기술 근거, 관찰일, certainty와 재검증 조건은 [`evidence.md`](../CUST-900/tickets/2026-08-26_Rocky-Linux-RI-SP/evidence.md)를 따른다. 외부 문서 또는 상품 조건이 바뀌었거나 실제 고객 티켓에 재사용할 때는 원본 evidence를 현재 자료로 다시 검증한다.
