# FitCloud Per-Account Cost Split Is Not Available

## Risk

Do not claim that FitCloud `corp/monthly` output can isolate one AWS account unless the active API schema and response have been verified to expose an account dimension.

## Known observation

The currently recorded repository rule states that the relevant `corp/monthly` API family has no `accountId` field. A company with multiple accounts therefore cannot be split by account from that response alone.

## Required behavior

- Use only FitCloud-curated figures in customer-facing material.
- If account-level separation is requested, verify the current FitCloud schema first.
- If still unavailable, offer an approved console filter or direct resource-based investigation rather than fabricating an allocation.
- Never reveal or mention raw AWS billing figures as an alternative.

## Verification before reuse

Record the endpoint, request period, response schema, and observation date in the ticket. Update this trap only through an append-style dated correction if the API changes.
