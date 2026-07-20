# Provider inventory controls

CPs and LPs may need standing rules for internal inventory: withdrawal delays, rate limits,
approved destinations and recovery paths. Covenants can express those controls without turning
M0/M1 into a retail savings product.

A withdrawal can first move inventory to a staging output constrained by CTV. CSV then enforces a
review window during which a recovery key can return the funds. Recursive covenants can preserve
the policy for change outputs or impose periodic limits.

This is an operational-security pattern for professional infrastructure. It does not protect the
external BTC destroyed to acquire inventory and does not make M1 redeemable.

**Primitives:** CTV · CSV · output introspection
