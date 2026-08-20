# Application map

What can be built, and what each thing actually depends on. The labels are defined in
[What BATHRON is](../protocol/what-bathron-is.md#reading-the-status-labels).

`Needs external components` and `Requires consensus change` are not soft warnings — they mean the
thing does not work today without that dependency.

## A. Native contracts on Bitcoin facts

No oracle. The facts come from Bitcoin headers carried in consensus.

| Application | Status | Depends on |
|---|---|---|
| Difficulty above/below a threshold | `AVAILABLE PRIMITIVE` | — |
| Buried-height conditions | `AVAILABLE PRIMITIVE` | — |
| Median-time-past conditions | `AVAILABLE PRIMITIVE` | — |
| Confirmed Bitcoin payment (amount, script, depth) | `AVAILABLE PRIMITIVE` | no dedicated test suite yet |
| Binary and barrier instruments | `AVAILABLE PRIMITIVE` | — |
| Mining-difficulty hedges | `AVAILABLE PRIMITIVE` | product logic, counterparty |
| Payments conditioned on verifiable Bitcoin events | `AVAILABLE PRIMITIVE` | — |
| Cumulative-work conditions | **Requires consensus change** | no such query exists |
| Linear (non-stepped) payoff on difficulty | **Requires consensus change** | predicates only, no value read |

## B. Programmable settlement

| Application | Status | Depends on |
|---|---|---|
| Covenants, output constraints | `ACTIVE IN CONSENSUS`, `TESTED` | — |
| Recursive covenants | `ACTIVE IN CONSENSUS`, `TESTED` | no end-to-end demonstration |
| Hashlocks and timelocks | `ACTIVE IN CONSENSUS` | — |
| Conditional cross-chain settlement | `TESTED` / demonstrated against Bitcoin | no general atomicity guarantee |
| DLC with external attestation | `AVAILABLE PRIMITIVE` | **external oracle**, product logic |
| Confidential transfers | `ACTIVE IN CONSENSUS` | — |
| Confidential **covenants** | `UNKNOWN` | not demonstrated |

## C. Markets

| Application | Status | Depends on |
|---|---|---|
| Market with no listing committee | `TESTED` / demonstrated | application, liquidity |
| Several providers on one pair | `AVAILABLE PRIMITIVE` | providers |
| Off-chain quotes, on-chain settlement | `TESTED` | provider infrastructure |

No guarantee of liquidity, of price, or of general atomicity is offered. **No market is proven
today**; the network is an experimental testnet.

## D. Applications needing external components

**These are not native.** BATHRON has **no price oracle, no margin engine and no liquidation in
consensus.**

| Application | Status | Missing |
|---|---|---|
| Synthetic USD | **Needs external components** | price attestation, collateral, margin, liquidation |
| Price-indexed assets | **Needs external components** | same |
| Margin, liquidation, application collateral | **Needs external components** | entirely application-layer |

A note worth stating plainly: an instrument indexed on **Bitcoin difficulty** is more native and
more verifiable than a synthetic USD. The first settles on a predicate every node checks in
consensus; the second on a signature the protocol can verify but never judge.
