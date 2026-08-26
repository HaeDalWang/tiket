# EC2 RI/SP Coverage: Platform Match and Marketplace Software Charges

## Risk

Do not answer "does this OS get RI/SP coverage?" from the distribution name. Two separate mechanisms decide the outcome, and only one of them is about the operating system.

## Known observation

Verified against current AWS documentation on 2026-08-26 (`TICKET-LOCAL-001`).

1. RI coverage depends on the instance's `Platform details`, not the distribution name. Only distributions with a commercial AWS subscription appear as a distinct platform: `Red Hat BYOL Linux`, `Red Hat Enterprise Linux` (and SQL/HA combinations), `SUSE Linux`, `Ubuntu Pro`. Everything else bills as `Linux/UNIX` / `RunInstances`.
2. A zonal RI must match tenancy, platform, Availability Zone, instance family, and size. A regional RI must match instance family, tenancy, and platform, and then gets instance size flexibility. RHEL and SUSE Linux Enterprise Server RIs are excluded from instance size flexibility.
3. Compute Savings Plans and EC2 Instance Savings Plans are OS-agnostic within their documented scope, so the OS name is never the reason a Savings Plan fails to apply.
4. A Marketplace AMI can carry a seller software or support charge that is separate from and additional to the EC2 charge. RI and SP discount the EC2 usage, not the seller charge. A paid support product cannot be used with Reserved Instances at all; the seller-specified price is always paid.
5. The same distribution often exists on Marketplace as both a free vendor-official listing and third-party repackaged paid listings. Rocky Linux is a confirmed example. Coverage expectations differ between the two.

## Required behavior

- Ask for or verify `Platform details` and `Usage operation` before making a definitive RI coverage statement.
- Check whether the AMI is a free official listing or a paid third-party listing before discussing expected savings.
- Separate "RI/SP applies" from "the whole line item drops". Seller software charges remain.
- Treat a customer report of "RI did not apply" as a matching problem to diagnose (platform, family, size, tenancy, scope) or a residual software charge, not as a defect in the discount model.
- Do not state or imply a coverage percentage or amount. Customer-facing figures must be FitCloud-curated.
- Customer-account inspection stays blocked while `aws-customer-account-ops` is under repair. Provide the console path or a read-only CLI query for the customer to run instead.

## Verification before reuse

Record the official documentation URL, the observed date, the `Platform details` / `Usage operation` values obtained, and the Marketplace listing type in the ticket. Append a dated correction if AWS platform values, size-flexibility exclusions, or Marketplace billing behavior change.
