# Customer Reply Rules

## 순서

1. 산출물을 먼저 정한다 — `playbooks/ticket-outputs.md` (작업 지시서 / 조사 결과+답변 / 답변+출처).
2. `tickets/<번호>.md` 의 `## 확인한 것` 을 근거로 쓴다. `[확인]` 항목만 확정 서술에 쓴다.
3. 표현 프로파일을 고른다 — `playbooks/reply-style.md`.
4. 초안을 쓴 뒤 **`## 발송 전 점검` 을 통과시킨다.** 이 관문은 형식이 아니라 실제로
   나갔던 실패에서 뽑은 항목이다.

에이전트마다 문장·순서·길이는 달라도 된다. 질문, 결론, 확실성, 사실, 미확인, 다음 행동은
같아야 한다. 문장 모양이 아니라 의미를 검증한다.

`[추측]` 을 `[확인]` 처럼 서술하지 않는다. `[모름]` 을 조용히 빼지 않는다.

## Language and tone

- Write customer-facing drafts in formal Korean.
- Use `저희` for first-person plural.
- Lead with the answer or current status, then supporting detail.
- Default to `seungdo-contextual` (승도 스타일). Its length follows the ticket's complexity and the explanation needed for customer understanding. Select `technical-detailed` (상세 설명형) when a systematic reference-style response is required.
- Before drafting, identify the customer's likely desired resolution behind the literal question. Include relevant confirmed conditions, risks, and next steps that prevent predictable follow-up questions, without inventing unstated facts or dumping unrelated possibilities.
- Before asking a clarification question, explain why the missing information blocks the answer.
- Offer choices when possible and state when an undecided answer is acceptable.
- Preserve technical terms, commands, product names, and identifiers exactly.
- **콘솔 화면을 안내할 때는 고객이 실제로 보는 언어의 UI 명칭을 쓴다.** 한국어 콘솔을 쓰는
  고객에게 영문 메뉴 경로를 주면 화면에서 찾지 못한다. 필요하면 `결제 및 비용 관리(Billing
  and Cost Management)` 처럼 병기한다. 여러 단계를 클릭해야 하는 안내는 스크린샷이 텍스트
  경로보다 빠른 경우가 많다.
- **고객이 문의에서 밝힌 제약 안에서 실행 가능한 답을 준다.** 권한·환경·일정 제약을 고객이
  이미 적었는데 그것을 무시한 경로를 안내하면, 답을 준 것이 아니라 왕복을 만든 것이다.

## Separation

- Internal investigation stays outside the customer reply code block.
- The customer reply contains no secret location, credential material, raw command dump, unsupported assertion, or prohibited raw AWS billing information.
- A draft is not a sent reply. Only a human sends email or posts to Zendesk.

## Evidence and certainty

- Apply `playbooks/evidence-verification.md` before drafting.
- Convert internal evidence into concise customer-safe reasoning.
- Do not use a prior reply as proof of a technical fact.
- If the answer is unknown, state what must be checked or ask for the missing information.

## Relationship context

- Use the preferred salutation and response format recorded in the customer profile.
- Do not infer identity from a short name when the alias map is ambiguous.
- Adapt detail level from observed communication behavior, not a personality judgment.

Style precedence is: technical accuracy/security/active policy → customer profile → team rules → operator-local preference → agent default.

## Final checks

`tickets/<번호>.md` 의 `## 발송 전 점검` 을 채운 뒤 아래를 함께 본다.

- The reply answers the actual question.
- Every definitive statement is supported by a `[확인]` item that carries a source.
- No hypothesis was promoted and no blocking unknown was omitted.
- The next action and owner are clear.
- The reply does not imply that an unexecuted change or unverified PoC has completed.
- Cost figures follow the FitCloud-only rule.
- The code block can be copied without exposing internal notes.
