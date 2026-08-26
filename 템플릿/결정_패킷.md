# Decision Packet v2

Create this internal JSON contract before a new or revised customer reply. Evidence claims and source URLs stay in the ticket's investigation sections under stable `[F#]`, `[H#]`, and `[U#]` IDs; do not copy them into the packet.

```json
{
  "version": 2,
  "tier": "standard",
  "question": "",
  "decisions": [
    {
      "id": "D1",
      "item": "",
      "result": "conditional",
      "certainty": "confirmed",
      "conditions": [],
      "fact_ids": ["F1"],
      "hypothesis_ids": [],
      "unknown_ids": ["U1"]
    }
  ],
  "policy_ids": [],
  "actions": {
    "customer": [{"id": "A1", "action": ""}],
    "internal": [{"id": "I1", "action": ""}]
  },
  "prohibited_claims": [{"id": "P1", "claim": ""}]
}
```

## Contract rules

- IDs are stable within a ticket: decisions `D#`, facts `F#`, hypotheses `H#`, unknowns `U#`, customer actions `A#`, internal actions `I#`, prohibited claims `P#`.
- `confirmed` decisions may reference facts and blocking unknowns, but not hypotheses.
- `hypothesis` certainty requires at least one `H#`; `unknown` results require at least one `U#`; `conditional` results require explicit conditions.
- Absence from an example list is not confirmation.
- Direct source URLs and observation times belong with `[F#]` evidence, not in this packet.
- Preserve prior packet revisions. Append the latest v2 JSON block when semantics change.