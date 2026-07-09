# Build your first application

An application on BATHRON is not a smart contract in the EVM sense. It is a **covenant**: a script that constrains how value can move, enforced by every node. You compose it from a small set of strong primitives.

## The shape of every application

1. **Lock value under a script.** Funds go to a script hash whose spending conditions you wrote.
2. **State the release conditions.** The script can require signatures, preimages, timeouts (`CSV`/`CLTV`), a forced destination (`CTV`), an oracle signature (`CSFS`) — or **a proven Bitcoin fact** (`TX_CONFIRMED`): *release when this Bitcoin payment is confirmed*.
3. **Anyone can trigger settlement.** When conditions are met, the spend is valid; consensus enforces the outcome. No server, no operator.

## A minimal example — conditional payment on a Bitcoin fact

> *"Pay Bob as soon as Alice's Bitcoin transaction is confirmed; refund me after 24 hours otherwise."*

- One path: proof that the Bitcoin transaction is buried under the in-consensus header chain (`TX_CONFIRMED`) + a `CTV` template that **forces** the payout to Bob.
- Other path: a `CSV` relative timelock returning funds to you.

This one pattern — *a proven Bitcoin fact releases a covenant* — is the engine under [escrow](../learn/applications/escrow.md), [DvP](../learn/applications/dvp.md) and [OTC settlement](../learn/applications/otc.md).

## Tooling

Today the developer surface is the node's [RPC API](../build/api.md) plus the script engine ([opcodes](../reference/opcodes.md)). A higher-level [SDK](../build/sdk.md) is in development and ships with the public testnet.
