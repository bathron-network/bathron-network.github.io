# What you can build

Builders need a way to express an agreement without making the base protocol understand their entire business. BATHRON supplies programmable settlement, a common unit and verifiable Bitcoin facts. Independent applications combine them with interfaces, services and any external evidence their users require.

The following examples describe constructions, not a catalogue of products supplied by BATHRON. Their common foundation is a set of explicit spending conditions.

## A map of applications

| Application | Settlement building blocks | Responsibilities outside consensus |
|---|---|---|
| Cross-chain settlement | Hashlocks, timelocks and constrained outputs | Quotes, inventory, external chain execution and monitoring |
| Conditional payment | Authorization, covenant and evidence predicate | Agreement terms and transaction submission |
| Escrow | Release branches and timed recovery | Evidence collection and any human arbitration |
| Difficulty contract | Bitcoin difficulty predicates and fixed outcome branches | Pricing, funding and selection of observation points |
| Provider inventory policy | Recursive covenants, approved destinations and delays | Key management, review and recovery monitoring |
| USDBTC construction | Conditional payouts and external attestation | Economic terms, price observation and provider services |

A builder chooses primitives from the agreement's requirements. The presence of an opcode does not supply a usable product by itself.

## Start from the fact being settled

For a difficulty contract, Bitcoin supplies the relevant fact. Every node checks the predicate at the agreed observation height. A dollar price requires an external source because it is not contained in Bitcoin history.

For an asset conversion involving X, the application also needs a valid execution process on X's chain. BATHRON settles its own leg. The external leg remains a provider and application responsibility, even when the two use a shared secret.

This distinction helps users compare agreements. They can see which conditions are independently verified and which rely on a named service or attestation.

## Build a complete lifecycle

An application defines funding, successful settlement and recovery. It explains who acts at each stage, what evidence they keep and how eligibility is observed.

Interfaces make this lifecycle understandable. A user should be able to identify the asset sent, the asset received, the applicable fees, the counterparty and the recovery conditions before signing.

New applications can reuse existing primitives without changing consensus. A genuinely new primitive has a different scope: it needs a specification and review of the rules every node validates.

## USDBTC

USDBTC is an imaginable third-party construction for exchanging risk between a stable-value-and-yield objective and leveraged BTC exposure.
A builder can combine covenants with an external price oracle and provider services.
The builder defines the funding, payoff and source of any return; no economic mechanism is prescribed here.
It is an application idea, not a BATHRON product or a promise of stability or yield.

Explore [Settlement across chains](cross-chain.md), [Conditional payments and escrow](escrow.md) and [Contracts on Bitcoin facts](bitcoin-contracts.md). Then use [Build an application](build.md) to translate one agreement into a transaction flow.
