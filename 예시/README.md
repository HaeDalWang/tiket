# 비식별 티켓 예시

이 디렉터리는 실제 support workflow에서 식별자와 운영 소유권을 제거해 재구성한 공통 upstream의 비식별 참조 자료다. 완전한 합성 기록이라고 주장하지 않으며 활성 고객 운영 기록도 아니다. `CUST-900`, `ACCOUNT-NNN`, `CONTACT-NNN`, `TICKET-EXAMPLE-NNN`은 예시 전용 reference다.

날짜, 판단 변경, 발송 상태와 비식별 발송문은 ticket lifecycle·append-only·freshness 검증을 재현하기 위해 유지한다. 이는 해당 고객이 현재 존재하거나 티켓이 활성 상태라는 의미가 아니다. 각 예시는 `example_provenance: de-identified-reconstruction`과 `operational_owner: none`을 명시한다.

## 포함 표본

- `CUST-900/티켓/2026-08-26_Rocky-Linux-RI-SP/`
  - 복합 조건을 고객의 질문 흐름에 맞춰 설명하는 `seungdo-contextual` 표본
  - `current.md`, `evidence.md`, `history.md` 분리와 archived snapshot hash 검증 표본
- `CUST-900/티켓/2026-08-28_Kiro-management-account-change/`
  - 고객의 실제 해결 목표와 후속 의문을 선제 해소하는 `seungdo-contextual` 표본
  - 공개 사례를 보조 근거로 사용하고 Pilot → 검증 → 기존 구성 정리 → 순차 확대하는 표본
- `회신_스타일/technical-detailed.md`
  - Rocky Linux Decision Packet의 기술 의미를 바꾸지 않고 다수 엔지니어가 재검토할 수 있는 문서형으로 배열한 presentation-only 표본

## 사용 규칙

- 신규 운영 티켓은 이 디렉터리를 직접 수정하거나 그대로 복제하지 않는다. `템플릿/고객_프로필.md`와 `템플릿/티켓.md`로 `고객/CUST-NNN/` 아래에 생성한다.
- 예시의 날짜·상태·공개 사례는 표본에 기록된 관찰 시점 기준이다. 현재 고객 판단의 근거로 재사용하려면 공식 자료와 외부 사례를 다시 확인한다.
- 실제 고객명, 계정 alias, 연락처, Account ID, IP/CIDR 또는 private mapping을 예시에 추가하지 않는다.
- 예시 개선은 공통 upstream에 제안한다. 각 workspace의 운영 기록은 `고객/`에만 둔다.
