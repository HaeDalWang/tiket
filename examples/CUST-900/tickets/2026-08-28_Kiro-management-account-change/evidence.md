---
ticket_ref: TICKET-EXAMPLE-002
updated_at: 2026-08-31
reuse_policy: current-ticket
---

# 근거 레지스트리

## 확인된 사실

- [F1] Kiro profile은 특정 AWS 계정과 리전의 조합에 대응하며, 해당 profile이 enterprise 사용자 대상 관리 설정과 구독을 정의한다.[1]
  - source: https://kiro.dev/docs/enterprise/concepts
  - target: Kiro enterprise profile account/Region ownership
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro profile transfer 기능 또는 account binding 정책 변경 시

- [F2] 새 AWS 계정에서 Kiro profile을 생성하고 IdP의 사용자·그룹을 선택해 구독 tier를 할당할 수 있다.[2]
  - source: https://kiro.dev/docs/enterprise/subscribe
  - target: destination Kiro profile and subscriptions
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro enterprise onboarding 절차 변경 시

- [F3] Kiro profile에는 암호화 키, 코드 참조, 사용량 대시보드, 사용자 활동 보고서, prompt logging, MCP, Web Tools, overages 등의 관리 설정이 존재한다.[5]
  - source: https://kiro.dev/docs/enterprise/settings
  - target: profile-specific administrative settings
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro settings 항목 변경 시

- [F4] 동일 사용자를 서로 다른 Kiro profile에 중복 구독하면 각 profile에서 별도 과금된다. 중도 해지는 해당 월 전액이 청구되고 다음 달 초부터 취소가 적용된다.[4]
  - source: https://kiro.dev/docs/enterprise/billing
  - target: overlapping source/destination subscriptions
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro enterprise billing 정책 변경 시

- [F5] Kiro profile을 삭제하면 연결된 구독이 자동 취소되며, 개별 사용자 비활성화만으로는 구독이 취소되지 않는다.[3]
  - source: https://kiro.dev/docs/enterprise/subscription-management
  - target: source profile and subscription cleanup
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: subscription cancellation 동작 변경 시

- [F6] IAM Identity Center 방식은 지원 리전의 IdC instance와 대상 사용자 identity가 필요하다.[6]
  - source: https://kiro.dev/docs/enterprise/identity-provider/iam-identity-center
  - target: IAM Identity Center prerequisite
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro IdC 연결 요구사항 변경 시

- [F7] Okta 또는 Microsoft Entra ID를 직접 연결한 경우 새 profile에 맞춰 SCIM endpoint/token과 provisioning을 다시 구성해야 한다. 기존 profile 삭제 후 같은 IdP application으로 새 profile을 만들면 group membership이 자동 동기화되지 않아 전체 재-provisioning이 필요하다.[7][8]
  - source: https://kiro.dev/docs/enterprise/identity-provider/okta
  - source: https://kiro.dev/docs/enterprise/identity-provider/microsoft-entra
  - target: direct external IdP reprovisioning
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: external IdP migration/provisioning 기능 변경 시

- [F8] Kiro의 공식 deployment option은 AWS Organizations management account에서 IAM Identity Center를 활성화하고, member account에서 Kiro profile을 생성하여 사용자를 구독하는 구성을 지원한다.[9]
  - source: https://kiro.dev/docs/enterprise/deployment-options
  - target: organization Identity Center with member-account Kiro profile
  - observed_at: 2026-08-28 KST
  - evidence_tier: official-doc
  - certainty: confirmed
  - reverify_when: Kiro multi-account deployment option 변경 시

- [F9] Kiro 공식 GitHub 이슈 #7747에는 같은 AWS Organization 내에서 동일 사용자의 구독을 다른 AWS 계정에 활성화하고 기존 계정 구독을 해지한 실제 사례가 보고되어 있다. 새 구독이 Pending 상태에 머물고 Kiro CLI가 실패했으며, 기존 계정 구독을 복원하면 다시 동작했다. 이 이슈는 해결 방법이 확인된 것이 아니라 2026-08-17 장기 비활성과 최신 재현 정보 부족을 이유로 `not_planned` 종료됐다.[10]
  - source: https://github.com/kirodotdev/Kiro/issues/7747
  - target: same-user cross-account subscription reassignment case
  - observed_at: 2026-08-31 KST
  - evidence_tier: public-case
  - certainty: reported
  - reverify_when: 최신 버전 재현 사례, 후속 이슈 또는 공식 해결 안내 추가 시

- [F10] AWS re:Post의 cross-account AssumeRole 구성 가이드는 organization management account의 Identity Center를 사용하면서 member account에서 Kiro Enterprise를 활성화하는 절차를 설명한다.[11]
  - source: https://repost.aws/articles/AR275kg6NETeqZ0Ju445zpfw/how-do-i-set-up-aws-kiro-enterprise-subscription-when-using-a-cross-account-iam-assumerole-architecture
  - target: member-account Kiro onboarding with central Identity Center
  - observed_at: 2026-08-28 KST
  - evidence_tier: aws-repost-article
  - certainty: confirmed
  - reverify_when: re:Post article or Kiro onboarding model 변경 시

## 가설

- [H1] 원본 계정에서 IAM Identity Center를 사용 중이며 대상 사용자들이 이미 해당 identity store에 존재한다는 운영자 기억
  - verify_by: IAM Identity Center instance type이 organization instance인지와 대상 계정이 같은 AWS Organization의 member account인지 확인
  - certainty: hypothesis

## 미확인

- [U1] 현재 Kiro profile의 Identity Center 연결, profile Region, 구독 사용자·그룹·tier, profile별 관리 설정
  - blocks: 고객 환경에 맞춘 상세 실행 순서와 누락 없는 설정 목록

- [U2] 대상 계정이 같은 AWS Organization의 member account인지와 현재 IAM Identity Center가 organization instance인지 여부
  - blocks: 기존 identity를 그대로 선택할 수 있는지 또는 새 IdC/사용자 동기화가 필요한지 판단

- [U3] 조사 범위에서는 Kiro Profile 자체와 그 관리 설정·이력을 다른 AWS 계정으로 그대로 이전한 성공 사례는 확인되지 않음. 확인된 공개 사례는 동일 사용자의 구독을 새 계정에서 재할당하고 기존 구독을 해지한 사례임.
  - blocks: profile 데이터·설정의 자동 승계를 전제로 한 안내

## 조회 이력

- 2026-08-28 — Kiro 공식 enterprise 문서에서 profile 귀속, 신규 profile·구독 생성, 관리 설정, 구독 해지 및 중복 과금 조건 확인

## 재검증 trigger

- Kiro가 profile의 AWS 계정 간 직접 transfer 기능을 제공하는 경우
- Kiro profile, subscription 또는 billing 정책이 변경되는 경우
- 고객의 실제 identity source와 AWS Organizations 구성이 현재 판단과 충돌하는 경우

## Sources

[1] https://kiro.dev/docs/enterprise/concepts
[2] https://kiro.dev/docs/enterprise/subscribe
[3] https://kiro.dev/docs/enterprise/subscription-management
[4] https://kiro.dev/docs/enterprise/billing
[5] https://kiro.dev/docs/enterprise/settings
[6] https://kiro.dev/docs/enterprise/identity-provider/iam-identity-center
[7] https://kiro.dev/docs/enterprise/identity-provider/okta
[8] https://kiro.dev/docs/enterprise/identity-provider/microsoft-entra
[9] https://kiro.dev/docs/enterprise/deployment-options
[10] https://github.com/kirodotdev/Kiro/issues/7747
[11] https://repost.aws/articles/AR275kg6NETeqZ0Ju445zpfw/how-do-i-set-up-aws-kiro-enterprise-subscription-when-using-a-cross-account-iam-assumerole-architecture
