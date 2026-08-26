---
ticket_ref: TICKET-LOCAL-001
load_policy: on-demand
archived_at: 2026-08-26
archived_source_path: 고객/CUST-001/티켓/2026-08-26_Rocky-Linux-RI-SP-적용문의.md
archived_source_sha256: 1fd2c34bfd07fe71ccbe893174b17c6d987757ec6f0d7dd86248df1b5064fe19
---

# Rocky Linux RI/SP 문의 — 전체 이력

이 파일은 기본 context로 읽지 않는다. 판단 변경 이유, 이전 packet/brief/draft, 실제 발송, 고객 회신 또는 분쟁 확인이 필요할 때만 읽는다.

## Archived monolithic snapshot through v4

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

## 조사·실측

### 적용 컨텍스트

- 고객 프로필: `고객/CUST-001/프로필.md`
- 유사 티켓: 없음
- 적용 회사 규정: `POLICY-SEC-001` (draft; 비식별화 경계만 적용), `POLICY-PAYER-001` (draft; Payer/계약 확인 필요사항 식별에만 사용), `POLICY-COST-ESC-001` (active; RI/SP·할인 문의이므로 CSR handoff 대상)
- CSR handoff 상태: 미실행. `POLICY-COST-ESC-001`에 따라 사람이 Slack에서 `@csr` handoff를 게시해야 하며, 에이전트는 게시하지 않는다. handoff 시각·응답·에스컬레이션은 확정 후 append한다.
- 사용한 공통 능력: `aws-official-research`, `answer-quality-gate`
- Payer model / 확인일: `unknown` / 미확인
- CSR 계약 확인 reference: 미확인
- COP 현재 기능 확인 reference: 미확인
- FitCloud 실측 reference: 미확인
- COC owner reference / 확인일시: 해당 없음
- FitCloud owner source reference: 해당 없음
- On-call roster source reference: 해당 없음
- 보존/삭제 근거: 미확인
- 보존/삭제 conflict 상태: 해당 없음
- CSR/법무 확인 reference: 해당 없음

### 확인된 사실

- EC2 RI는 `Linux/UNIX`, `SUSE Linux`, `Red Hat Enterprise Linux` 등을 서로 다른 platform으로 취급한다. RI가 적용되려면 RI의 platform과 인스턴스를 시작한 AMI의 platform이 일치해야 한다. Linux AMI는 일반 `Linux/UNIX`인지 `SUSE Linux` 같은 특정 값인지 `Platform details`를 확인해야 한다.[1]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-concepts-buying.html
  - target: Amazon EC2 Reserved Instances / current documentation
  - observed_at: 2026-08-26 09:11 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- AMI의 과금 분류는 `Platform details`와 `Usage operation`으로 확인할 수 있다. 공식 예시에서 `Linux/UNIX`는 `RunInstances`, `Red Hat Enterprise Linux`는 `RunInstances:0010`으로 구분된다.[3]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html
  - target: Amazon EC2 AMI billing classification / current documentation
  - observed_at: 2026-08-26 09:11 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- Compute Savings Plans는 EC2 instance family, size, Region, OS, tenancy와 무관하게 적격 EC2 사용량에 적용된다.[2]
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: Compute Savings Plans / current documentation
  - observed_at: 2026-08-26 09:11 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- EC2 Instance Savings Plans는 선택한 Region과 instance family 범위 안에서 size, OS, tenancy와 무관하게 적용된다.[2]
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: EC2 Instance Savings Plans / current documentation
  - observed_at: 2026-08-26 09:11 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- AWS Marketplace AMI의 요금은 AWS infrastructure charge와 seller-defined software charge로 구분된다. Free 제품은 별도 software charge가 없지만 Paid 제품은 별도 software charge가 존재할 수 있다.[4]
  - source: https://docs.aws.amazon.com/marketplace/latest/userguide/pricing-ami-products.html
  - target: AWS Marketplace AMI pricing / current documentation
  - observed_at: 2026-08-26 09:11 KST
  - evidence_tier: official-doc
  - certainty: confirmed

- 공식 `Platform details` / `Usage operation` 예시 표에 별도 플랫폼으로 등재된 Linux 계열은 `Red Hat BYOL Linux`, `Red Hat Enterprise Linux`(및 SQL/HA 조합), `SUSE Linux`, `Ubuntu Pro`뿐이다. Rocky Linux 등 별도 상용 subscription이 없는 배포판에 해당하는 항목은 없고, 일반 Linux AMI 예시는 `Linux/UNIX` / `RunInstances`다.[3][5]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html , https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/view-billing-info.html
  - target: AMI billing information fields / Finding AMI billing and usage details / current documentation
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- RI 할인은 running On-Demand instance에 적용되는 billing discount이며, zonal RI는 tenancy·platform·AZ·instance family·instance size가 모두 일치해야 한다. regional RI는 instance size flexibility를 제공하지만 이때도 반드시 일치해야 하는 속성은 instance family, tenancy, platform이다. 또한 RHEL과 SUSE Linux Enterprise Server RI는 instance size flexibility 대상이 아니다.[6]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html
  - target: How Reserved Instance discounts are applied / current documentation
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- AWS Marketplace의 유료 support product는 RI와 함께 사용할 수 없고, seller가 지정한 가격을 항상 지불한다. 공식 문구: "You can't use a support product with Reserved Instances. You always pay the price that's specified by the seller of the support product."[7]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-paid-amis-support.html
  - target: Use paid support for supported AWS Marketplace offerings / current documentation
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- Marketplace AMI 사용 시 AWS 서비스 요금은 software 구매 비용과 별개다. 공식 문구: "Charges for using Amazon EC2 and other services from AWS are separate and in addition to what you pay to purchase AWS Marketplace software products." 또한 instance type 변경 시 "your Amazon EC2 infrastructure will be billed according to your signed savings plan. However, the AMI license from AWS Marketplace will automatically change to hourly pricing."[8]
  - source: https://aws.amazon.com/marketplace/help/201550560
  - target: AMI subscriptions in AWS Marketplace / current documentation
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- Rocky Linux 프로젝트가 판매자로 등록한 공식 Marketplace 목록(예: Rocky Linux 8 (Official), 판매자 `Rocky Linux`)은 software 요금이 없다. 목록 문구: "This product is available free of charge. ... Additional AWS infrastructure costs may apply." Marketplace 메타데이터의 Operating system 값은 `OtherLinux <version>`으로 표시된다.
  - source: https://aws.amazon.com/marketplace/pp/prodview-2otariyxb3mqu
  - target: Rocky Linux 8 (Official) AWS Marketplace listing / observed 2026-08-26
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: vendor-listing
  - certainty: confirmed
- 반면 Marketplace에는 동일한 Rocky Linux를 재포장한 third-party 유료 목록이 다수 존재한다. 확인된 예: seller support 요금이 명시된 `Rocky Linux 9 Minimal`, usage-based pricing이 명시된 `Rocky Linux 8 supported by Apollo` / `Rocky Linux 9 (ARM) supported by Apollo`, 유료 지원이 포함된 `Rocky Linux 8 (Official) Supported Fifty Clouds`, free trial 후 usage-based로 전환되는 `Rocky Linux 10 Security Hardened`.
  - source: https://aws.amazon.com/marketplace/pp/prodview-g7eliviybmfpk , https://aws.amazon.com/marketplace/pp/prodview-l6cwimqa4op7i , https://aws.amazon.com/marketplace/pp/prodview-qqxr5cp34oys6 , https://aws.amazon.com/marketplace/pp/prodview-efbo6tpghkriu
  - target: third-party Rocky Linux Marketplace listings / observed 2026-08-26
  - observed_at: 2026-08-26 09:45 KST
  - evidence_tier: vendor-listing
  - certainty: confirmed

### 가설

- 가설: 고객이 과거 CentOS/Red Hat 계열에서 `Linux/UNIX` RI 적용 실패를 경험한 원인은 대상이 RHEL 유료 AMI였고 `Platform details`가 `Red Hat Enterprise Linux`(`RunInstances:0010`)여서 `Linux/UNIX` RI의 platform 조건과 불일치했을 가능성이 가장 높다. 부수적으로 RHEL RI는 instance size flexibility 대상이 아니므로 size가 다르면 regional RI로도 커버되지 않는다.
  - 근거 방향: `Platform details` 표에 `Red Hat Enterprise Linux`가 별도 platform으로 존재하고[3], RI는 platform 일치가 필수이며 RHEL은 size flexibility 제외 목록에 있다[6].
  - 확인 또는 기각 방법: 당시 대상 AMI의 `Platform details`와 구매한 RI의 platform·size를 대조한다. 근거 없이 원인을 단정하는 문구는 고객 회신에 넣지 않고 "가능성이 높은 원인" 수준으로만 언급한다.
- 가설: Rocky Linux 공식 AMI의 `Platform details`는 `Linux/UNIX`, `Usage operation`은 `RunInstances`다.
  - 근거 방향: Rocky Linux는 별도 상용 Linux subscription이 아니고 공식 Marketplace 목록에 software 요금이 없으며, 공식 platform 목록에 Rocky 전용 항목이 없다.
  - 확인 또는 기각 방법: 대상 instance/AMI에서 `PlatformDetails`, `UsageOperation`을 직접 확인한다. 현재 고객 계정 조회가 blocked이므로 고객이 콘솔 또는 read-only CLI로 확인하거나, capability 복구 후 저희가 확인한다.
  - certainty: hypothesis (strong)

### 미확인 / 고객에게 필요한 정보

- 대상 Rocky Linux 인스턴스가 사용한 AMI의 실제 `Platform details`
- AMI의 `Usage operation` 및 AWS Marketplace product 여부
- Marketplace product인 경우 Free/BYOL/Paid pricing model
- 적용하려는 할인 유형: EC2 RI, Compute Savings Plans, EC2 Instance Savings Plans
- RI인 경우 Region/AZ scope, instance type/family, tenancy, platform
- EC2 Instance Savings Plans인 경우 Region과 instance family
- 고객 Payer model과 할인 공유 범위

### 실행한 조회와 결과

- `aws___search_documentation`: RI platform 일치 조건, Savings Plans OS 유연성, AMI billing field, Marketplace 요금 구조 검색 성공
- `aws___read_documentation`: 공식 문서 네 페이지 원문 읽기 성공
- 2026-08-26 09:45 KST 추가 조회: `apply_ri.html`, `view-billing-info.html`, `using-paid-amis-support.html`, Marketplace buyer guide, Savings Plans FAQ 원문 확인 성공
- 공개 Marketplace 목록 조회: Rocky Linux 공식 목록(무료)과 third-party 유료 재포장 목록 존재를 확인함. 고객 식별 정보 없이 공개 기술 용어로만 조회함.
- 고객 AWS 계정 조회: 실행하지 않음 (`customer-aws-readonly` blocked)
- AWS/FitCloud 비용 실측: 실행하지 않음; 고객 회신에 비용 수치 없음

### v4 재검증 (2026-08-26 14:26 KST)

- [F1] EC2 RI는 실행 중인 On-Demand Instance와 RI의 속성이 일치할 때 적용되는 billing discount이다. Zonal RI는 tenancy, platform, Availability Zone, instance family, instance size가 일치해야 하고, Regional RI의 size flexibility에서도 instance family, tenancy, platform은 일치해야 한다.[6]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html
  - target: Amazon EC2 Reserved Instance discount application / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F2] AMI billing classification은 `Platform details`와 `Usage operation`으로 확인하며, AWS 공식 표에서 `Linux/UNIX`는 `RunInstances`, `Red Hat Enterprise Linux`는 `RunInstances:0010`으로 구분된다.[3]
  - source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html
  - target: Amazon EC2 AMI billing classification / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F3] Compute Savings Plans는 instance family, size, Region, OS, tenancy와 무관하게 EC2 instance usage에 자동 적용된다.[2]
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: Compute Savings Plans / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F4] EC2 Instance Savings Plans는 선택한 Region과 instance family 범위 안에서 instance size, OS, tenancy와 무관하게 적용된다.[2]
  - source: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
  - target: EC2 Instance Savings Plans / current documentation
  - observed_at: 2026-08-26 14:26 KST
  - evidence_tier: official-doc
  - certainty: confirmed
- [F5] AWS Marketplace AMI는 AWS infrastructure charge와 seller software charge가 별도이며, Free model은 추가 software charge가 없고 Paid model은 별도 software charge가 발생할 수 있다.[4]
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

### PoC 연계

- 필요 여부: 없음
- 의뢰서: 해당 없음
- 결과서: 해당 없음
- repository/branch/commit: 해당 없음
- 검증 상태: 공식 문서 검증으로 충분

## 결정 패킷

### v1 (2026-08-26 09:45 KST)

```yaml
version: 1
tier: standard
question: "ACCOUNT-001의 Rocky Linux EC2 인스턴스가 EC2 RI 또는 Savings Plans 할인 적용 대상인가"
decisions:
  - item: "Rocky Linux라는 OS 자체가 RI/SP 적용을 배제하는가"
    result: no
    certainty: confirmed
    conditions: []
    fact_ids: [F1, F5]
  - item: "Compute Savings Plans 적용 가능 여부"
    result: yes
    certainty: confirmed
    conditions: ["적격 EC2 사용량일 것"]
    fact_ids: [F3]
  - item: "EC2 Instance Savings Plans 적용 가능 여부"
    result: yes
    certainty: confirmed
    conditions: ["약정한 Region 및 instance family 범위 내일 것"]
    fact_ids: [F4]
  - item: "EC2 Reserved Instances 적용 가능 여부"
    result: conditional
    certainty: confirmed
    conditions:
      - "대상 인스턴스의 Platform details가 Linux/UNIX (Usage operation: RunInstances)일 것"
      - "zonal RI는 tenancy, platform, AZ, family, size 전부 일치"
      - "regional RI는 family, tenancy, platform 일치 (size flexibility 적용)"
    fact_ids: [F1, F2, F6]
  - item: "Marketplace 유료 Rocky Linux 이미지의 software/support 요금이 RI/SP로 할인되는가"
    result: no
    certainty: confirmed
    conditions: ["third-party 유료 목록을 사용 중인 경우에 한해 발생"]
    fact_ids: [F7, F8, F9, F10]
  - item: "과거 CentOS/RHEL 계열에서 Linux/Unix RI가 적용되지 않은 원인"
    result: unknown
    certainty: hypothesis
    conditions: ["당시 대상 AMI의 Platform details와 구매 RI의 platform/size 대조 필요"]
    fact_ids: [F2, F6]
  - item: "대상 인스턴스 개별 확정 및 구매 권고"
    result: unknown
    certainty: unknown
    conditions: ["Platform details/Usage operation, Region, family, tenancy, 기존 RI/SP 및 Payer 공유 범위 확인 필요"]
    fact_ids: []
facts:
  - id: F1
    claim: "EC2 RI는 Linux/UNIX, SUSE Linux, Red Hat Enterprise Linux 등을 서로 다른 platform으로 취급하며, RI platform과 인스턴스 AMI의 platform이 일치해야 적용된다"
    sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-concepts-buying.html"]
    observed_at: "2026-08-26 09:11 KST"
  - id: F2
    claim: "AMI 과금 분류는 Platform details와 Usage operation으로 확인하며, Linux/UNIX는 RunInstances, Red Hat Enterprise Linux는 RunInstances:0010이다"
    sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html"]
    observed_at: "2026-08-26 09:11 KST"
  - id: F3
    claim: "Compute Savings Plans는 instance family, size, Region, OS, tenancy와 무관하게 적격 EC2 사용량에 적용된다"
    sources: ["https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html"]
    observed_at: "2026-08-26 09:11 KST"
  - id: F4
    claim: "EC2 Instance Savings Plans는 선택한 Region과 instance family 범위 안에서 size, OS, tenancy와 무관하게 적용된다"
    sources: ["https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html"]
    observed_at: "2026-08-26 09:11 KST"
  - id: F5
    claim: "공식 Platform details 예시 표에 별도 platform으로 등재된 Linux 계열은 Red Hat BYOL Linux, Red Hat Enterprise Linux(및 SQL/HA 조합), SUSE Linux, Ubuntu Pro뿐이며 Rocky Linux 전용 항목은 없다"
    sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/view-billing-info.html"]
    observed_at: "2026-08-26 09:45 KST"
  - id: F6
    claim: "zonal RI는 tenancy/platform/AZ/family/size 전부 일치가 필요하고, regional RI는 family/tenancy/platform 일치가 필수이며, RHEL과 SUSE Linux Enterprise Server RI는 instance size flexibility 대상이 아니다"
    sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html"]
    observed_at: "2026-08-26 09:45 KST"
  - id: F7
    claim: "AWS Marketplace 유료 support product는 RI와 함께 사용할 수 없고 seller가 지정한 가격을 항상 지불한다"
    sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-paid-amis-support.html"]
    observed_at: "2026-08-26 09:45 KST"
  - id: F8
    claim: "Marketplace software 구매 비용은 EC2 등 AWS 서비스 요금과 별개이며, instance type 변경 시 EC2 인프라는 savings plan으로 과금되지만 Marketplace AMI license는 hourly pricing으로 전환된다"
    sources: ["https://aws.amazon.com/marketplace/help/201550560"]
    observed_at: "2026-08-26 09:45 KST"
  - id: F9
    claim: "Rocky Linux 프로젝트가 판매자인 공식 Marketplace 목록은 software 요금이 없고 AWS 인프라 요금만 발생한다"
    sources: ["https://aws.amazon.com/marketplace/pp/prodview-2otariyxb3mqu"]
    observed_at: "2026-08-26 09:45 KST"
  - id: F10
    claim: "Marketplace에는 동일한 Rocky Linux를 재포장한 third-party 유료 목록이 다수 존재한다"
    sources: ["https://aws.amazon.com/marketplace/pp/prodview-g7eliviybmfpk", "https://aws.amazon.com/marketplace/pp/prodview-l6cwimqa4op7i", "https://aws.amazon.com/marketplace/pp/prodview-qqxr5cp34oys6", "https://aws.amazon.com/marketplace/pp/prodview-efbo6tpghkriu"]
    observed_at: "2026-08-26 09:45 KST"
hypotheses:
  - id: H1
    claim: "과거 CentOS/RHEL 계열 RI 미적용의 원인은 대상이 RHEL 유료 AMI(Platform details: Red Hat Enterprise Linux)여서 Linux/UNIX RI와 platform이 불일치했고, RHEL RI는 size flexibility 제외 대상이었기 때문일 가능성이 높다"
    verify_by: "당시 대상 AMI의 Platform details와 구매한 RI의 platform/size를 대조"
  - id: H2
    claim: "Rocky Linux 공식 AMI의 Platform details는 Linux/UNIX, Usage operation은 RunInstances다"
    verify_by: "대상 instance/AMI에서 PlatformDetails, UsageOperation을 직접 확인 (고객 자체 확인 또는 capability 복구 후 저희가 확인)"
unknowns:
  - id: U1
    question: "대상 Rocky Linux 인스턴스의 실제 Platform details / Usage operation 값"
    blocks: "개별 인스턴스에 대한 RI 적용 확정"
  - id: U2
    question: "사용 중인 AMI가 공식 무료 목록인지 third-party 유료 목록인지"
    blocks: "실제 절감 폭 및 software 요금 잔존 여부 판단"
  - id: U3
    question: "대상 인스턴스의 Region, family, size, tenancy 및 기존 RI/SP 보유 현황, Payer 공유 범위"
    blocks: "RI/SP 유형 선택 권고 및 coverage 확약"
policy_ids: [POLICY-SEC-001, POLICY-PAYER-001, POLICY-COST-ESC-001]
customer_actions:
  - "대상 인스턴스의 Platform details / Usage operation 확인 후 회신"
  - "대상 인스턴스의 Region, instance type 공유"
  - "사용 중인 Rocky Linux AMI의 Marketplace 목록 종류 확인"
internal_actions:
  - "사람이 최종 검토 후 Zendesk email 발송 (에이전트 발송 금지)"
  - "POLICY-COST-ESC-001에 따라 사람이 Slack @csr handoff 게시 후 시각 기록"
  - "고객 회신 수신 시 조건부 문구를 확정 문구로 갱신"
must_not_claim:
  - "대상 인스턴스가 실제로 RI/SP 적용 대상임을 확정 (Platform details 미확인)"
  - "구체적 절감 금액, 절감률, 비용 수치 (FitCloud-curated 자료 외 금지)"
  - "과거 CentOS/RHEL 미적용 원인의 확정 (H1은 가설)"
  - "특정 RI/SP 구매 권고 및 coverage 확약"
```

### v2 (2026-08-26 14:26 KST)

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

### v1 (2026-08-26 09:45 KST)

```yaml
version: 1
audience:
  role: "고객 IT 운영 책임자 (CONTACT-001)"
  technical_depth: standard
goal: "Rocky Linux의 RI/SP 적용 가능 여부를 결론부터 전달하고, 개별 인스턴스 확정에 필요한 값을 고객이 직접 확인해 회신하도록 유도한다"
tone: formal-korean
structure: conclusion-first
fact_ids: [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10]
hypothesis_ids: [H1]
unknown_ids: [U1, U2, U3]
must_include:
  - "Rocky Linux는 RI/SP 모두 적용 가능하다는 결론"
  - "RI 판단 기준은 배포판 이름이 아니라 Platform details 값"
  - "Compute SP와 EC2 Instance SP의 OS 무관 적용"
  - "Marketplace 유료 이미지의 software/support 요금은 RI/SP로 할인되지 않음"
  - "Platform details / Usage operation 확인 방법과 고객 회신 요청"
optional:
  - "과거 CentOS/RHEL 사례의 유력한 원인 (H1, 확정 아님으로 명시)"
  - "zonal / regional RI 일치 조건 구분"
avoid:
  - "비용 수치, 절감률, 구매 권고"
  - "고객 계정 실측을 수행한 듯한 표현"
  - "H1을 확정으로 서술"
commands: on-request
salutation_ref: "고객/CUST-001/프로필.md#CONTACT-001"
```

### v2 (2026-08-26 14:26 KST)

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

## 판단

- Rocky Linux라는 OS 이름 자체가 RI/SP 할인 적용을 배제하지 않는다. Rocky Linux는 AWS의 별도 상용 Linux platform(RHEL/SUSE/Ubuntu Pro)이 아니므로, 공식 무료 AMI 기준으로는 `Linux/UNIX` 과금 플랫폼으로 취급되는 것이 정상 동작이다. 단, 개별 instance 확정은 `Platform details` 확인 후에만 가능하다.
- **EC2 RI:** `Platform details`가 `Linux/UNIX`이면 `Linux/UNIX` RI가 적용된다. zonal RI는 tenancy·platform·AZ·family·size가 모두 일치해야 하고, regional RI는 family·tenancy·platform만 일치하면 size flexibility가 적용된다.[6]
- **Compute Savings Plans:** OS·family·size·Region·tenancy와 무관하게 적격 EC2 사용량에 적용되므로 Rocky Linux 사용 자체는 적용 장애가 아니다.[2]
- **EC2 Instance Savings Plans:** 선택한 Region 및 instance family 안에서 size·OS·tenancy와 무관하게 적용된다.[2]
- **핵심 분기 — 어떤 Rocky Linux AMI인가.** Marketplace에는 (a) Rocky Linux 프로젝트의 공식 무료 목록과 (b) 유료 지원·재포장 third-party 목록이 함께 존재한다. (b)를 사용 중이면 EC2 인프라 요금과 별도로 seller software/support 요금이 발생하고, 이 요금은 RI/SP로 할인되지 않는다. 특히 유료 support product는 RI와 함께 사용할 수 없고 seller 지정 가격을 그대로 지불한다.[7][8] 즉 "RI를 샀는데 예상만큼 안 줄었다"는 체감은 platform 불일치가 아니라 software 요금 잔존 때문일 수도 있다.
- **과거 CentOS/RHEL 경험의 유력한 원인:** RHEL 유료 AMI는 `Platform details`가 `Red Hat Enterprise Linux`(`RunInstances:0010`)여서 `Linux/UNIX` RI와 platform이 불일치한다. 또한 RHEL RI는 instance size flexibility 제외 대상이다.[3][6] 다만 당시 실제 구성 확인 전이므로 회신에서는 확정이 아니라 유력한 원인으로만 안내한다.
- 확인 방법은 콘솔 `Instances` 또는 `AMIs` → **Details** 탭의 `Platform details` / `Usage operation`이며, read-only CLI는 `describe-instances` 또는 `describe-images`다.[5]
- 구매 권고나 실제 coverage 확약은 Payer model, 현재 사용량, 기존 commitment, AMI billing field 확인 전에는 하지 않는다. 고객 회신에 비용 수치는 넣지 않는다.

## 회신

### 발송 완료 — 1차 접수 회신 (2026-08-26 09:08, 사람 발송)

```text
안녕하세요.
솔트웨어 배승도입니다

확인하고 회신드리겠습니다

감사합니다
```

### 초안 v4 (2026-08-26 14:26 KST, 검수 대기)

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

### 초안 v3 (2026-08-26, 대체됨)

```text
안녕하세요, 부장님.

문의주신 Rocky Linux 인스턴스의 RI/SP 적용 여부, 확인하여 회신드립니다.

결론부터 말씀드리면 Rocky Linux는 RI와 Savings Plans 모두 적용 대상입니다. Rocky Linux는 RHEL이나 SUSE처럼 AWS가 별도 과금 플랫폼으로 구분하는 유료 배포판이 아니어서, 공식 이미지 기준으로는 기본 Linux/UNIX 플랫폼으로 과금됩니다.

1. Savings Plans — 제약 없음

Compute Savings Plans는 운영체제, 인스턴스 패밀리, 사이즈, 리전, 테넌시와 무관하게 적격 EC2 사용량에 적용됩니다. EC2 Instance Savings Plans도 약정하신 리전과 인스턴스 패밀리 범위 안에서는 사이즈와 운영체제에 무관하게 적용됩니다. 따라서 Rocky Linux 사용 자체는 SP 적용에 아무런 제약이 되지 않습니다.

2. Reserved Instances — Platform details 값이 기준

RI는 플랫폼이 일치해야 적용되며, 판단 기준은 배포판 이름이 아니라 해당 인스턴스의 Platform details 값입니다.

- Platform details가 Linux/UNIX (Usage operation: RunInstances)로 표시되면 Linux/Unix RI가 정상 적용됩니다.
- 가용 영역을 지정하는 Zonal RI는 테넌시, 플랫폼, 가용 영역, 인스턴스 패밀리, 사이즈가 모두 일치해야 합니다.
- 리전 단위 Regional RI는 패밀리, 테넌시, 플랫폼만 일치하면 사이즈는 유연하게 적용됩니다.

3. 말씀하신 CentOS/RHEL 사례에 대하여

당시 대상이 RHEL 유료 이미지였을 가능성이 높습니다. RHEL 이미지는 Platform details가 Red Hat Enterprise Linux (Usage operation: RunInstances:0010)로 별도 플랫폼으로 구분되어, Linux/Unix로 구매한 RI와는 플랫폼이 일치하지 않습니다. 여기에 더해 RHEL RI는 사이즈 유연성(instance size flexibility) 적용 제외 대상이라, 사이즈가 다르면 리전 RI로도 커버되지 않습니다. 다만 당시 구성을 확인하기 전이므로 확정은 아니며, 필요하시면 함께 점검해 드리겠습니다.

4. 한 가지 확인이 필요한 부분 — 어떤 Rocky Linux 이미지인지

AWS Marketplace에는 Rocky Linux 프로젝트가 제공하는 공식 무료 이미지와, 서드파티가 유료 지원을 붙여 재배포한 이미지가 함께 등록되어 있습니다.

- 공식 무료 이미지: 소프트웨어 요금이 없고 EC2 인프라 요금만 발생하므로, RI/SP 할인이 사용 요금에 그대로 반영됩니다.
- 서드파티 유료 이미지: EC2 인프라 요금과 별도로 판매자의 소프트웨어·지원 요금이 발생합니다. 이 요금은 RI나 SP로 할인되지 않으며, 유료 지원 제품의 경우 RI와 함께 사용할 수 없고 판매자가 정한 금액을 그대로 부담하게 됩니다.

즉 서드파티 유료 이미지를 사용 중이시라면, RI/SP를 적용하더라도 소프트웨어 요금은 그대로 남아 기대만큼 절감되지 않는 것처럼 보일 수 있습니다.

5. 확인 방법

대상 인스턴스에서 아래 값을 확인해 주시면 적용 여부를 확정해 드릴 수 있습니다.

- 콘솔: EC2 > 인스턴스 > 대상 인스턴스 선택 > 세부 정보 탭 > Platform details, Usage operation
- CLI(조회 전용):

  aws ec2 describe-instances \
      --instance-ids i-1234567890abcdef0 \
      --query "Reservations[].Instances[].{PlatformDetails:PlatformDetails,UsageOperation:UsageOperation}"

값이 Linux/UNIX / RunInstances로 나오면 Linux/Unix RI와 Savings Plans 모두 적용 가능한 상태입니다.

위 값과 함께 대상 인스턴스의 리전, 인스턴스 타입을 알려주시면, 기존 RI/SP 보유 현황과 함께 검토하여 어떤 방식이 적합할지 회신드리겠습니다.

감사합니다.
```

### 초안 v2 (2026-08-26, 대체됨)

```text
안녕하세요, 부장님.

솔트웨어 배승도입니다. 문의주신 Rocky Linux 인스턴스의 RI/SP 적용 여부 확인 결과 안내드립니다.

결론부터 말씀드리면, Rocky Linux는 RI와 Savings Plans 모두 적용 가능합니다. RHEL이나 SUSE처럼 AWS에서 별도 과금 플랫폼으로 구분되는 유료 배포판이 아니기 때문에, 공식 Rocky Linux 이미지 기준으로는 기본 Linux/UNIX 플랫폼으로 과금됩니다.

1. Savings Plans

Compute Savings Plans는 운영체제, 인스턴스 패밀리, 사이즈, 리전, 테넌시와 무관하게 적격 EC2 사용량에 적용됩니다. EC2 Instance Savings Plans도 약정한 리전과 인스턴스 패밀리 범위 안에서는 사이즈와 운영체제에 무관하게 적용됩니다. 따라서 Rocky Linux 사용은 SP 적용에 아무런 제약이 되지 않습니다.

2. Reserved Instances

RI는 플랫폼이 일치해야 적용되며, 판단 기준은 배포판 이름이 아니라 해당 인스턴스의 Platform details 값입니다.

- Platform details가 Linux/UNIX (Usage operation: RunInstances)로 표시되면 Linux/Unix RI가 정상 적용됩니다.
- 가용 영역을 지정한 Zonal RI는 테넌시, 플랫폼, 가용 영역, 인스턴스 패밀리, 사이즈가 모두 일치해야 합니다.
- 리전 단위 Regional RI는 패밀리, 테넌시, 플랫폼만 일치하면 사이즈는 유연하게 적용됩니다.

3. 과거 CentOS/RHEL 건에서 적용이 안 되었던 이유

말씀하신 사례는 대상 인스턴스가 RHEL 유료 이미지였을 가능성이 높습니다. RHEL 이미지는 Platform details가 Red Hat Enterprise Linux (Usage operation: RunInstances:0010)로 별도 플랫폼으로 구분되어, Linux/Unix로 구매한 RI와는 플랫폼이 일치하지 않습니다. 추가로 RHEL RI는 사이즈 유연성(instance size flexibility) 적용 제외 대상이라 사이즈가 다르면 리전 RI로도 커버되지 않습니다. 당시 구성은 확인 전이므로 확정은 아니며, 필요하시면 함께 점검해 드리겠습니다.

4. 한 가지 확인이 필요한 부분

AWS Marketplace에는 Rocky Linux 프로젝트가 제공하는 공식 무료 이미지와, 서드파티가 유료 지원을 붙여 재배포한 이미지가 함께 등록되어 있습니다.

- 공식 무료 이미지: 소프트웨어 요금이 없고 EC2 인프라 요금만 발생하므로, RI/SP 할인이 사용 요금 전체에 반영됩니다.
- 서드파티 유료 이미지: EC2 인프라 요금과 별도로 판매자 소프트웨어/지원 요금이 발생합니다. 이 요금은 RI나 SP로 할인되지 않으며, 유료 지원 제품의 경우 RI와 함께 사용할 수 없고 판매자가 정한 금액을 그대로 부담하게 됩니다.

즉 서드파티 유료 이미지를 사용 중이라면 RI/SP를 적용해도 소프트웨어 요금은 그대로 남아, 기대만큼 절감되지 않는 것처럼 보일 수 있습니다.

5. 확인 방법

대상 인스턴스에서 아래 값을 확인해 주시면 적용 여부를 확정해 드릴 수 있습니다.

- 콘솔: EC2 > 인스턴스 > 대상 인스턴스 선택 > 세부 정보 탭 > 인스턴스 세부 정보 > Platform details, Usage operation
- CLI(조회 전용):

  aws ec2 describe-instances \
      --instance-ids i-1234567890abcdef0 \
      --query "Reservations[].Instances[].{PlatformDetails:PlatformDetails,UsageOperation:UsageOperation}"

값이 Linux/UNIX / RunInstances로 나오면 Linux/Unix RI 및 Savings Plans 모두 적용 가능한 상태입니다.

해당 값과 대상 인스턴스의 리전, 인스턴스 타입을 알려주시면, 기존 RI/SP 보유 현황과 함께 검토하여 어떤 방식이 적합한지 회신드리겠습니다.

감사합니다.
```

### 초안 v1 (2026-08-26, 대체됨)

```text
안녕하세요, 부장님.

문의주신 Rocky Linux 기반 EC2 인스턴스도 RI 및 Savings Plans 적용 대상이 될 수 있습니다.

다만 적용 기준은 Rocky Linux라는 운영체제 명칭 자체가 아니라, 해당 인스턴스가 사용한 AMI의 과금 플랫폼 정보입니다.

- EC2 RI: AMI의 `Platform details`가 `Linux/UNIX`이고, RI의 Region 또는 가용 영역, 인스턴스 유형·패밀리, tenancy 등 다른 조건도 일치하면 `Linux/UNIX` RI 할인이 적용됩니다.
- Compute Savings Plans: 운영체제와 무관하게 적격 EC2 사용량에 적용되므로 Rocky Linux 사용 여부는 적용에 영향을 주지 않습니다.
- EC2 Instance Savings Plans: 선택한 Region과 인스턴스 패밀리 범위 안에서는 운영체제와 무관하게 적용됩니다.

따라서 대상 Rocky Linux AMI의 `Platform details`가 `Linux/UNIX`로 표시된다면 Linux/UNIX RI 적용을 검토할 수 있습니다. 반면 `Red Hat Enterprise Linux`처럼 별도 플랫폼으로 표시되는 AMI는 동일한 Linux/UNIX RI와 일치하지 않습니다.

또한 AWS Marketplace에서 제공되는 AMI 중 유료 제품은 EC2 인프라 사용료와 별도의 소프트웨어 요금이 발생할 수 있으므로, 해당 AMI의 Marketplace 요금 유형도 함께 확인해야 합니다.

대상 인스턴스의 AMI `Platform details`와 사용 중인 인스턴스 패밀리·Region을 확인한 뒤, 실제 RI 또는 Savings Plans 적용 조건을 최종 확인하여 안내드리겠습니다.

감사합니다.
```

## 고객 회신

- 아직 회신하지 않음

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

## 변경 이력

### 2026-08-26 14:26 KST — 공식 문서 재검증 및 회신 초안 v4

- AWS 공식 문서에서 RI의 zonal/regional matching condition, AMI의 `Platform details` / `Usage operation`, Compute Savings Plans와 EC2 Instance Savings Plans의 OS 유연성, Marketplace AMI의 infrastructure/software charge 분리를 재검증함.
- 고객 AWS/FitCloud 계정 조회는 실행하지 않았고, 비용 수치나 구매 권고를 회신에 포함하지 않음.
- 안정적인 `[F1]`∼`[F5]`, `[H1]`∼`[H2]`, `[U1]`∼`[U4]` ID를 조사·실측에 등록하고 Decision Packet v2와 Reply Brief v2를 추가함.
- v3의 “Rocky Linux는 RI와 Savings Plans 모두 적용 대상” 표현을, “Rocky Linux 자체는 제외 조건이 아니며 개별 RI 적용은 실제 platform·matching condition 확인 필요”로 조정해 미확인 상태를 확정하지 않도록 함.
- 과거 CentOS/RHEL 사례는 원인을 확정하지 않고 platform 또는 기타 matching condition 불일치 가능성으로만 유지함.
- 초안 v4를 검수 대기 상태로 추가하고 v3를 대체 표시함. 발송과 Slack `@csr` handoff는 사람이 수행해야 함.

### 2026-08-26 — 최초 기록

- 신규 고객을 `CUST-001`로 비식별 등록하고 문의를 `TICKET-LOCAL-001`로 기록함.
- AWS 공식 문서 MCP로 RI platform 일치 조건, Savings Plans OS 유연성, AMI billing field, Marketplace 요금 구조를 확인함.
- 고객 계정의 실제 AMI 속성은 확인되지 않아 회신을 조건부 초안으로 유지함.

### 2026-08-26 10:55 KST — 결정 패킷·회신 브리프 보강 및 회신 초안 v3

- 라우터가 요구하는 `결정 패킷`(v1)과 `회신 브리프`(v1)를 티켓에 명시적으로 기록함. 기존 `확인된 사실`을 `F1`~`F10`, 가설을 `H1`~`H2`, 미확인을 `U1`~`U3`로 ID화하고 `must_not_claim`을 고정함. 기술적 판단 내용은 v2 시점과 동일하며 표현만 구조화함.
- 사람이 2026-08-26 09:08에 발송한 1차 접수 회신을 `## 회신`에 사실대로 기록함.
- 회신 초안 v3 작성. 동일 메일 스레드의 후속 회신이므로 중복 자기소개를 제거하고, 각 항목에 결론을 앞세우는 소제목을 붙여 가독성을 높임. 새로운 기술적 주장이나 확약은 추가하지 않았고, v2의 사실·가설·조건은 그대로 유지함. 초안 v2는 대체 표시로 보존함.
- 발송과 Slack `@csr` handoff는 여전히 사람이 수행한다.

### 2026-08-26 09:45 KST — 근거 보강 및 회신 초안 v2

- 추가 확인: `apply_ri.html`의 zonal/regional RI 일치 속성과 RHEL/SUSE의 instance size flexibility 제외, `view-billing-info.html`의 확인 절차와 read-only CLI, `using-paid-amis-support.html`의 "You can't use a support product with Reserved Instances", Marketplace buyer guide의 EC2 요금과 software 요금 분리 문구.
- 공개 Marketplace 목록 확인으로 Rocky Linux 공식 무료 목록과 third-party 유료 재포장 목록이 병존함을 확인하고, 이를 회신의 핵심 확인 항목으로 승격함.
- 과거 CentOS/RHEL 미적용 경험의 유력한 원인을 `Red Hat Enterprise Linux` platform 불일치 + RHEL RI의 size flexibility 제외로 정리함. 당시 구성 미확인 상태이므로 확정이 아닌 "가능성 높음"으로만 회신에 포함함.
- 판단을 v1의 "적용될 수 있음"에서 "Rocky Linux는 RI/SP 모두 적용 가능, 단 개별 인스턴스는 `Platform details` 확인 필요"로 조정함. 초안 v1은 대체 표시로 보존함.
- 고객 계정 조회는 여전히 실행하지 않음. 대신 고객이 직접 실행할 수 있는 read-only 확인 절차를 회신에 포함함.
- 반복 함정으로 `플레이북/함정/ec2-ri-sp-플랫폼과-마켓플레이스-요금.md`를 신규 등록함.
- 병행 세션에서 `POLICY-COST-ESC-001` (active)이 신설되어 RI/SP 문의가 CSR handoff 대상임을 확인하고 티켓에 반영함. Slack 게시는 사람이 수행한다.

## Sources

[1] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-concepts-buying.html — Buy Reserved Instances for Amazon EC2
[2] https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html — Savings Plans types
[3] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html — AMI billing information fields
[4] https://docs.aws.amazon.com/marketplace/latest/userguide/pricing-ami-products.html — AMI product pricing for AWS Marketplace
[5] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/view-billing-info.html — Finding AMI billing and usage details
[6] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html — How Reserved Instance discounts are applied
[7] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-paid-amis-support.html — Use paid support for supported AWS Marketplace offerings
[8] https://aws.amazon.com/marketplace/help/201550560 — AMI subscriptions in AWS Marketplace
