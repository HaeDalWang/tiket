---
ticket_ref: TICKET-EXAMPLE-001
current_revision: v4
updated_at: 2026-08-26 14:26 KST
reuse_policy: current-ticket
---

# Rocky Linux RI/SP 문의 — 근거 레지스트리

동일 ticket에서 claim, target, source가 그대로이고 충돌이 없으면 아래 confirmed evidence를 재사용한다. 새 claim, source 부족, 충돌, target/version 변경, 명시적 freshness 요구가 있을 때만 다시 조회한다.

### v4 재검증 (2026-08-26 14:26 KST)

- [F1] EC2 RI는 실행 중인 On-Demand Instance와 RI의 속성이 일치할 때 적용되는 billing discount이다. Zonal RI는 tenancy, platform, Availability Zone, instance family, instance size가 일치해야 하고, Regional RI의 size flexibility에서도 instance family, tenancy, platform은 일치해야 한다.
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html
  - target: Amazon EC2 Reserved Instance discount application / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F2] AMI billing classification은 `Platform details`와 `Usage operation`으로 확인하며, AWS 공식 표에서 `Linux/UNIX`는 `RunInstances`, `Red Hat Enterprise Linux`는 `RunInstances:0010`으로 구분된다.
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html
  - target: Amazon EC2 AMI billing classification / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F3] Compute Savings Plans는 instance family, size, Region, OS, tenancy와 무관하게 EC2 instance usage에 자동 적용된다.
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: Compute Savings Plans / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F4] EC2 Instance Savings Plans는 선택한 Region과 instance family 범위 안에서 instance size, OS, tenancy와 무관하게 적용된다.
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: EC2 Instance Savings Plans / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F5] AWS Marketplace AMI는 AWS infrastructure charge와 seller software charge가 별도이며, Free model은 추가 software charge가 없고 Paid model은 별도 software charge가 발생할 수 있다.
  - source: https://docs.aws.amazon.com/marketplace/latest/userguide/pricing-ami-products.html
  - target: AWS Marketplace AMI pricing / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [H1] 고객이 과거에 경험한 CentOS/RHEL 계열 RI 미적용은 RHEL의 별도 platform 또는 Region/AZ, family, size, tenancy 등 다른 RI matching condition 불일치였을 수 있다.
  - verify_by: 당시 대상 instance의 `Platform details` / `Usage operation`과 RI의 scope·family·size·tenancy·platform을 대조
  - certainty: hypothesis
- [H2] 대상 Rocky Linux instance의 `Platform details` / `Usage operation`이 `Linux/UNIX` / `RunInstances`일 수 있으나, 실제 값을 확인하지 않았으므로 개별 instance에 대해 확정하지 않는다.
  - verify_by: 고객이 EC2 console의 instance details에서 값을 확인해 회신
  - certainty: hypothesis
- [U1] 대상 Rocky Linux instance의 실제 `Platform details` / `Usage operation` 값은 미확인이며 개별 instance에 대한 Linux/UNIX RI 적용 확정을 막는다.
- [U2] 사용 중인 AMI의 Marketplace pricing model은 미확인이며 seller software charge 잔존 여부 판단을 막는다.
- [U3] 대상 instance의 Region/AZ, family, size, tenancy와 보유 RI/SP, Payer 공유 범위는 미확인이며 실제 coverage 확약과 구매 권고를 막는다.
- [U4] 과거 CentOS/RHEL 사례의 instance·AMI·RI 속성은 미확인이며 미적용 원인 확정을 막는다.

## 조회 이력

- 2026-08-26 14:26 KST — F1~F5를 AWS 공식 문서에서 재검증. 고객 AWS/FitCloud 계정 조회와 비용 실측은 수행하지 않음.

## 재검증 trigger

- AWS 문서 또는 pricing model 변경
- 실제 `Platform details` / `Usage operation` 수신
- 현재 evidence와 상충하는 live behavior
- 새로운 비용 수치·구매 권고·contract claim
