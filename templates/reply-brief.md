# Reply Brief v2

Select content IDs from the latest Decision Packet v2, then adapt only presentation. Do not restate technical conclusions in free-text brief fields.

```json
{
  "version": 2,
  "audience": {"role_ref": "CONTACT-001", "technical_depth": "standard"},
  "goal": "",
  "decision_ids": ["D1"],
  "fact_ids": ["F1"],
  "hypothesis_ids": [],
  "unknown_ids": ["U1"],
  "customer_action_ids": ["A1"],
  "internal_action_ids": [],
  "prohibited_claim_ids": ["P1"],
  "presentation": {
    "profile": "seungdo-contextual",
    "tone": "formal-korean",
    "structure": "conclusion-first",
    "commands": "on-request"
  },
  "presentation_requirements": [],
  "avoid_topics": []
}
```

## Style precedence

1. Technical accuracy, security, and active company policy
2. Customer profile preferences
3. Team reply rules
4. Operator-local style
5. Agent default style

## Contract rules

- `goal` states the customer's desired resolution behind the literal question, using confirmed context only; it must not invent an unstated motive.
- `audience.technical_depth` controls vocabulary and explanation depth inside the selected profile. It does not select a profile: `presentation.profile` controls information organization and reading flow.
- A detailed technical depth may still use `seungdo-contextual`, and a standard-depth audience may use `technical-detailed` when a reusable reference structure is required. Customer-profile precedence still applies.
- The brief may select only IDs defined by the latest Decision Packet and ticket evidence.
- It must include every hypothesis and blocking unknown referenced by selected decisions and every prohibited claim.
- `presentation_requirements` controls form only; never place a technical conclusion there.
- `presentation.profile` must be `seungdo-contextual` (승도 스타일) or `technical-detailed` (상세 설명형) as defined in `playbooks/reply-style.md`.
- Different agents may vary wording, order, examples, and length while preserving selected IDs and certainty.
- Keep operator-specific preferences outside tracked customer profiles.