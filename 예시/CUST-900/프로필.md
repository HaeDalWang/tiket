---
customer_ref: CUST-900
example_provenance: de-identified-reconstruction
operational_owner: none
contract_baseline: SRC-FITCLOUD-TERMS-001
contract_exceptions: []
payer_model: unknown
payer_verified_at: ""
coc_owner_ref: ""
coc_roster_verified_at: ""
updated_at: 2026-08-26
review_by: 2026-11-26
---

# CUST-900

## 계약 범위 / 담당 영역

- 기술 문의 접수 채널: Zendesk email
- 현재 확인된 문의 범위: AWS 기술·비용 최적화 관련 일반 문의
- 실제 지원 계약 범위: 미확인

## 계약 기준 및 예외

- 기본 약관: `SRC-FITCLOUD-TERMS-001` (active 전환 후 default baseline)
- 별도 SLA/SOW/addendum: 미확인
- 적용 제외 조항: 미확인
- 예외 적용 범위: 미확인
- 예외 근거 reference: 미확인
- 실제 계약 확인일: 미확인
- 법정 보존 근거 reference: 미확인
- 고객별 보존/삭제 예외: 미확인
- 법무 확인일: 미확인

## Payer / FitCloud 현재 상태

- Payer model: `unknown`
- CSR 계약 확인 reference: 미확인
- COP 기능 확인 reference: 미확인
- FitCloud 실측 reference: 미확인
- 비용·임계값·할인 검증일: 미확인
- FitCloud/CUR 제공 여부 검증일: 미확인
- roadmap와 현재 기능 구분 메모: 검증 전 고객 확약 금지

## COC / On-call 현재 라우팅

- 현재 담당자 reference: 미확인
- FitCloud owner source reference: 미확인
- On-call roster source reference: 미확인
- 최종 확인일시: 미확인
- Raw 절차와 live 절차 차이: 미확인

## 제약사항 — 티켓 작업 전 필수 확인

- 접근 불가 영역: 고객 AWS/FitCloud 조회는 `aws-customer-account-ops` 재승인 전 차단
- 승인 필요 작업: 실제 계약·할인 구매 권고·비용 수치 확약
- 금지 사항: 고객 계정 write API, 인프라 변경, raw AWS billing의 고객 노출
- 고객 계정 조회 방식: 현재 사용 불가; 일반 사양은 AWS 공식 문서로만 검증
- 비용 자료 기준: 고객 노출 비용 수치는 FitCloud-curated 자료만 허용

## 환경

| 항목 | 값 | 출처 | 확인일 | 재확인 시점 |
|---|---|---|---|---|
| 문의 대상 계정 | `ACCOUNT-001` | `TICKET-EXAMPLE-001` | 2026-08-26 | 실제 계정 확인이 필요한 티켓 |
| 문의 대상 OS | Rocky Linux를 사용하는 EC2 인스턴스 일부 | `TICKET-EXAMPLE-001` | 2026-08-26 | AMI/product code 확인이 필요한 경우 |

## 고객 고유 용어

| 용어 | 의미 | 출처 | 확인일 |
|---|---|---|---|
| 관리 계정 | `ACCOUNT-001` | `TICKET-EXAMPLE-001` | 2026-08-26 |

## 담당자 및 호칭

### CONTACT-001

- 소속/역할(비식별): 고객 IT 운영 책임자
- 권장 호칭(개인 이름 제외): 부장님
- 로컬 매핑 reference: `.private/customer-map.md`
- 담당·의사결정 범위: IT 운영 문의 및 비용 최적화 검토
- 선호 채널: Zendesk email
- 응답 형식 선호: 현재 미확인
- 최종 확인일: 2026-08-26
- 근거: `TICKET-EXAMPLE-001`

#### 관찰된 커뮤니케이션

- 2026-08-26: Rocky Linux EC2의 RI 및 Savings Plans 할인 적용 여부를 구체적으로 질문함.

#### 대응 방식

- RI와 Savings Plans를 분리해 결론과 예외 조건을 먼저 설명하고, 실제 구매 전 확인할 항목을 짧게 제시한다.

## 이름·별칭 연결표

| 비식별 표현 | 연결 대상 | 확신 | 근거 |
|---|---|---|---|
| 문의 발신자 | CONTACT-001 | confirmed | `.private/customer-map.md` |

## 주요 결정 이력

| 날짜 | 결정 | 배경·근거 | 상태 |
|---|---|---|---|
| 2026-08-26 | 고객 계정 조회 없이 AWS 공식 문서로 RI/SP 적용 사양을 검증 | customer AWS capability가 blocked이며 일반 사양 문의임 | current |

## 자료 위치

- 실제 인프라 코드: 미확인
- 고객 제공 자료: Zendesk `TICKET-EXAMPLE-001`
- 관련 회사 규정: `POLICY-SEC-001`

## 알려진 이슈 및 반복 패턴

- 고객은 과거 Red Hat/CentOS 계열 인스턴스에서 Linux/Unix RI 할인 적용이 기대와 달랐던 경험을 언급함. 원인은 아직 확인되지 않았으며 추정하지 않는다.

## 변경 이력

- 2026-08-26 — 최초 티켓 접수에 따라 비식별 최소 프로필 생성
