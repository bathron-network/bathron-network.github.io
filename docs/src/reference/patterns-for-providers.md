# Patterns for providers

Clearing and Liquidity Providers may need standing rules for their M1 inventory: withdrawal
delays, rate limits, approved destinations and recovery paths. Covenants can express those
controls without turning M0/M1 into a retail savings product.

## Inventory controls

| Control | Primitive | Effect |
|---|---|---|
| Staged withdrawal | `CTV` | inventory first moves to a staging output whose next spend is committed to a template |
| Review window | `CSV` | a relative timelock during which a recovery key can return the funds |
| Standing policy | recursive covenants (output introspection) | the policy is preserved on change outputs; periodic limits can be imposed |

A typical withdrawal path: hot key spends inventory to a `CTV`-constrained staging output → the
staging output can only be spent to the approved destination after a `CSV` delay, or back to
the recovery path at any time during that window → change outputs re-create the same covenant.

## Scope

This is an operational-security pattern for professional infrastructure. It does not protect
the external BTC destroyed to acquire inventory and does not make M1 redeemable.

**Primitives:** `CTV` · `CSV` · output introspection

**See also:** [Script & opcodes](opcodes.md) · [Roles](../markets/roles.md)
