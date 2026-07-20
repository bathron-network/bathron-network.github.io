# Conditional escrow

The target is an escrow-like BTC service without giving an agent unrestricted custody.

A CP quotes an execution path and a timeout path in the client's familiar assets. LP inventory
funds the conditional internal leg. A proven event can release the settlement; if it does not
occur, the external commitment must follow the specified refund path.

```text
client BTC commitment -> quoted condition
                             | condition proven
                             v
                    CP/LP internal covenant -> recipient leg
                             |
                             +-- timeout -> client refund path
```

Possible conditions include a confirmed Bitcoin payment (`TX_CONFIRMED`) or a designated
signature (`CSFS`). CTV can constrain internal outputs and CSV can enforce a timeout.

“No agent can take the principal” remains a design target, not a current general guarantee. It
depends on the complete two-chain state machine, timelock ordering, reorganisation handling and
wallet verification being formally specified and reviewed.

**Primitives:** TX_CONFIRMED · CTV · CSV · CSFS
