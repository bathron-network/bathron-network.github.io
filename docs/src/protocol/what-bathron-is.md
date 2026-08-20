# What BATHRON is

BATHRON is an **open programmable settlement protocol**. It supplies a settlement unit, a set of
conditions that consensus enforces, and a script engine that can assert facts about the Bitcoin
chain. It does not supply products, liquidity, prices or interfaces — those come from independent
builders on top.

Markets are one application of this layer. They are not the protocol.

## The core, in one list

| Component | What it does |
|---|---|
| **Bitcoin facts in consensus** | Five predicates a script can assert about the Bitcoin chain, verified by every node — no designated oracle |
| **Programmable settlement** | Covenants, output introspection, hashlocks, timelocks, signature verification over arbitrary messages |
| **M0 / M1** | A settlement unit created only against destroyed bitcoin, with conservation enforced in consensus |
| **HU finality** | One round of signatures, counted one Consensus Operator one vote |
| **Confidential transfers** | Sapling shielded values |

Each is documented with its code reference and its limits in
[Bitcoin-verifiable contracts](bitcoin-verifiable-contracts.md) and
[Programmable settlement](programmable-settlement.md).

## What it deliberately is not

- **Not a virtual machine.** The engine is a *script* engine, not Turing-complete. The Bitcoin
  facts it can assert are a **finite list of five**, not an extensible API.
- **Not an exchange.** No matching engine, no order book, no listing committee in consensus.
- **Not an issuer.** M0 exists only against burned bitcoin. There is no reserve and no redemption
  desk — `CheckA5Independent`, `CheckA6P1` and `CheckA7` in `src/state/settlement_logic.cpp`.
- **Not an oracle.** It can *check* an attestation; it cannot produce one or judge its truth.
- **Not a bridge.** Bitcoin moves only through markets, never through a protocol-held reserve.

## Reading the status labels

Every capability in this documentation carries one of four labels. They are not decoration:

- `ACTIVE IN CONSENSUS` — the opcode or rule is enabled on the current public testnet. **This says
  nothing about whether a product uses it.**
- `TESTED` — has a test suite.
- `DEMONSTRATED` — an end-to-end flow has actually been run.
- `AVAILABLE PRIMITIVE` — composable with no consensus change; **no product exists**.
- `TARGET NETWORK` — the architecture being aimed at; **not deployed**.

An active opcode is not a product, and this documentation never uses activation to imply one.

The distinction matters most for the network itself: application building is open today,
**Consensus Operator admission is not**. See [The target open network](../network/open-network-target.md)
and [Status & claims](../consensus/status-and-claims.md), which prevails over any other page.
