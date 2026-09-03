# Aurora Cluster Snapshot Encryption Limitation

## Risk

Do not assume an API that works for an RDS instance snapshot also works for an Aurora DB cluster snapshot.

## Known observation

The recorded incident history states that `CopyDBClusterSnapshot` cannot be used to add encryption to an Aurora cluster snapshot. Encryption is selected when restoring the cluster with the appropriate KMS key option.

## Required behavior

- Confirm the exact engine, resource type, API, and target version in official documentation.
- Validate the procedure in a non-production PoC when the ticket requires implementation confidence.
- Do not present an RDS instance procedure as an Aurora cluster procedure.
- Preserve rollback and service-impact analysis before preparing migration steps.
- Agents may prepare commands and scripts but must not execute the restore or cutover.

## Verification before reuse

Record the official documentation URL, API version/date, PoC environment if used, and observed result in the ticket. Append a dated correction if AWS behavior or support changes.
