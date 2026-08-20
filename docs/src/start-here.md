# Start here — BATHRON in five minutes

**Build contracts around facts Bitcoin can prove.**

BATHRON is an open programmable settlement protocol for markets, instruments and applications
anchored in Bitcoin.

> BATHRON is running an **experimental public testnet**. Application building is open;
> **Consensus-Operator admission is not yet open**.

## The core

Five things, and they compose:

1. **Bitcoin facts, verified in consensus.** A script can assert that difficulty at a Bitcoin
   height was above or below a threshold, that a height was reached, that a median-time-past has
   passed, or that a Bitcoin transaction paying a given script was confirmed deep enough. Every
   node checks it. No designated oracle.
   → [Bitcoin-verifiable contracts](protocol/bitcoin-verifiable-contracts.md)
2. **Programmable settlement.** Covenants — including recursive ones — output constraints,
   hashlocks, timelocks, and signature verification over arbitrary messages.
   → [Programmable settlement](protocol/programmable-settlement.md)
3. **A settlement unit that nobody issues.** M0 exists only against destroyed bitcoin; M1 is its
   transferable receipt. Conservation is enforced in consensus. There is no reserve and no
   redemption.
   → [Bitcoin is the final asset](bitcoin/final-asset.md)
4. **Finality in about a minute**, one Consensus Operator one vote.
   → [Production and finality](consensus/production-and-finality.md)
5. **Confidential transfers.** Values can move without being published.

## Who is who

| Role | Does |
|---|---|
| **Consensus Operators** | produce blocks and take part in finality |
| **Settlement Providers** | build settlement services on top of the protocol |
| **Clearing Providers** | orchestrate settlement conditions and flows |
| **Liquidity Providers** | hold inventory and publish prices |
| **Market / Application Builders** | create interfaces, instruments, markets, software |
| **Users** | choose their application, provider and counterparty |

No role is granted by the protocol except the first, and that one is **not yet open**.

## What can be built

- **Native to Bitcoin facts, no oracle**: difficulty hedges, buried-payment escrows, time-bound
  agreements, prediction instruments over what Bitcoin proves.
- **Programmable settlement**: conditional cross-chain flows, covenant-constrained spends, DLC
  shapes with an external attestation.
- **Markets**: a pair appears because someone quotes it, not because a committee approved it.
- **Needing external components**: anything indexed on a price. BATHRON has **no price oracle, no
  margin engine, no liquidation in consensus**.

The full table, with what each thing depends on:
→ [Application map](build/application-map.md)

## What is true today, and what is not

Anyone can build an application or propose a settlement flow **without a listing committee**.
Native Bitcoin facts require **no designated oracle**. External prices and real-world events still
require **external attestations**.

The protocol supplies settlement primitives; applications supply product logic, liquidity and
interfaces. **Markets are one application of the settlement layer, not the protocol itself.**

The network being aimed at — several independent Consensus Operators, open admission, several
independent providers — is described in
[The target open network](network/open-network-target.md). It is a target, not a description of
today.

→ [Status & claims](consensus/status-and-claims.md) prevails over every other page.
