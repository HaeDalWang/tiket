# Reply Style Profiles

Named profiles control presentation only. They never change Decision Packet IDs, evidence certainty, unknowns, prohibited claims, or required actions.

## Selection

- Use `seungdo-contextual` (**승도 스타일**) by default.
- Use `technical-detailed` (**상세 설명형**) when the output must serve as a systematic reference, comparison, diagnostic note, or reusable technical explanation for multiple readers.
- Customer-profile requirements and active policy override either profile.
- Record the selected name in `Reply Brief.presentation.profile`. Do not blend profiles without stating ticket-specific exceptions in `presentation_requirements`.
- `audience.technical_depth` changes vocabulary and explanation depth within a profile; it does not select the profile. Choose `technical-detailed` for reusable document structure, not merely because the topic is technical or the answer is long.

## `seungdo-contextual` — 승도 스타일

목표는 고객의 표면 질문 뒤에 있는 **실제로 해결하려는 문제와 잠재된 우려**를 파악하고, 합리적으로 예상되는 다음 의문까지 해소하여 고객이 추가 왕복 없이 실행할 수 있도록 하는 것이다. 이상적인 결과는 고객이 별도 질문 없이 조치한 뒤 `감사합니다`로 대화를 끝낼 수 있는 회신이다. 짧게 쓰는 것 자체가 목표는 아니다.

### 기본 흐름

1. 인사와 작성자 소개를 짧게 분리한다.
2. 고객의 문장에 적힌 질문과 실제로 해결하려는 목표를 구분한다. 추정이 필요한 경우 단정하지 말고 확인된 맥락과 일반적으로 예상되는 후속 의문만 다룬다.
3. `확인 결과`로 결론 또는 현재 확인 범위를 먼저 제시한다.
4. 고객이 결론을 받아들여 실행하는 데 필요한 설명을 제공한다. 공식 근거·공개 사례, 작동 원리·배경·조건 중 필요한 것을 선택한다.
5. 회신을 읽은 고객이 바로 물을 가능성이 높은 질문을 점검한다. 적용 조건, 실패 가능성, 기존 구성의 유지 여부, 비용·중단 위험, 되돌리기, 확인 방법, 오류 발생 시 조치 중 해당되는 내용을 선제적으로 포함한다.
6. 고객이 실행할 절차가 있으면 위험을 줄이는 순서로 작성한다. 조회·Pilot·검증을 먼저 하고, 해지·삭제·전체 확대는 뒤에 둔다.
7. 번호 절차는 항목마다 별도 줄에 쓰고 항목 사이를 띄운다.
8. 오류 또는 미확정 상황에서 고객이 무엇을 공유하면 되는지 안내한 뒤 짧게 마무리한다.

### 길이와 표현

- 고정된 줄 수나 문단 수를 두지 않는다. 티켓의 성격, 기술 난이도, 오해 가능성, 고객의 현재 이해 수준에 따라 짧아지거나 충분히 길어질 수 있다.
- 간단한 질문을 불필요하게 늘이지 않되, 길이를 줄이기 위해 판단 이유나 이해에 필요한 기술 설명을 삭제하지 않는다.
- 절차와 효과만 나열하지 않는다. 고객이 실행 전에 가질 합리적인 의문이 남는다면 근거, 기술적 설명, 조건 또는 실패 시 대응을 함께 제공한다.
- 모든 가능성을 백과사전처럼 나열하지 않는다. 고객의 실제 해결 목표와 연결되고 후속 질문을 줄이는 내용만 선제적으로 포함한다.
- tracked 티켓과 초안에서는 `ACCOUNT-NNN` 등 비식별 reference를 사용한다. 사람이 실제 발송할 때만 gitignored private mapping을 확인해 고객이 이해하는 계정 alias로 치환하며, 실제 alias를 저장소에 다시 기록하지 않는다. 제품명과 공개 화면명은 정확히 유지한다.
- 조사 범위에서 기능이나 사례를 찾지 못했다면 `확인되지 않았습니다`라고 쓰고 `없습니다`라고 절대 단정하지 않는다.
- 확인되지 않은 가설을 배경 설명으로 길게 늘이지 않는다. 답을 막는 조건만 고객 행동과 연결해 적는다.
- 여러 절차를 한 문장이나 한 줄에 압축하지 않는다.

### 구조 예시

```text
안녕하세요
[작성자 소개]

확인 결과, [결론 또는 공식 문서상 확인 범위]
[권고 이유 또는 공개 사례]
[근거 링크]

[고객이 다음으로 궁금해할 적용 조건·위험·기존 구성 영향]

따라서 아래 순서로 진행하는 것을 권장드립니다

1. [가장 작은 범위에서 조회 또는 Pilot]

2. [상태와 실제 사용 검증]

3. [검증 후 기존 구성 정리]

4. [나머지 범위로 순차 확대]

진행 중 [오류/미확정 정보]를 공유해 주시면 확인을 도와드리겠습니다
감사합니다
```

## `technical-detailed` — 상세 설명형

목표는 복잡한 기술 판단의 **조건, 작동 원리, 예외, 검증 방법**을 고객이 재검토할 수 있을 정도로 설명하는 것이다.

승도 스타일의 단순한 장문 버전이 아니다. 승도 스타일은 고객의 현재 질문과 이해 흐름을 따라 필요한 만큼 설명하는 대화형 회신이고, 상세 설명형은 여러 독자가 다시 참조할 수 있도록 정보를 체계적으로 배열한 문서형 회신이다.

### 사용 조건

- 여러 서비스·과금·보안 조건을 표나 항목으로 체계적으로 비교해야 한다.
- 여러 담당자에게 공유되거나 이후 재검토할 기준 문서가 필요하다.
- 장애 분석, 설계 검토, 운영 절차처럼 전제·진단·예외·검증을 빠짐없이 구조화해야 한다.
- 고객이 문서형 상세 설명을 명시적으로 요청했다.

### 기본 흐름

1. 첫 문단에서 결론과 적용 범위를 요약한다.
2. 전제와 아직 확인되지 않은 값을 분리한다.
3. 주제별 제목, bullet 또는 표로 조건과 이유를 설명한다.
4. 각 주요 결론에는 `왜`를 붙이고 공식 근거와 관찰 사실을 구분한다.
5. 위험·예외·되돌리기 조건과 고객의 확인 항목을 정리한다.
6. 마지막에 다음 행동과 근거 링크를 모은다.

### 길이와 표현

- 고정된 줄 수는 두지 않지만 같은 결론이나 주의사항을 반복하지 않는다.
- 상세함을 원문·명령·내부 조사 로그의 덤프로 대체하지 않는다.
- 긴 문단보다 제목, 표, bullet을 사용해 훑어볼 수 있게 한다.
- 결론을 뒤로 미루지 않는다. 상세형도 항상 요약을 먼저 둔다.

## Reply Brief usage

```json
"presentation": {
  "profile": "seungdo-contextual",
  "tone": "formal-korean",
  "structure": "conclusion-first",
  "commands": "on-request"
}
```

Use `presentation_requirements` only for ticket-specific form requirements, such as separating RI and Savings Plans or including a comparison table. Do not duplicate the selected profile's standing rules there.
