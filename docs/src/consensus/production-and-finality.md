# Production and finality

A settlement is only useful once it cannot be undone. BATHRON's consensus therefore answers two
questions separately — who makes the next block, and when that block becomes irreversible — and
keeps both answers deliberately simple, so that a market builder can reason about *when a
settlement is final* without reading the source.

Two separate layers, deliberately kept apart:

| Layer | Question it answers | Property |
|---|---|---|
| **Production** | who makes the next block | liveness |
| **Finality** | when is a block irreversible | safety |

## Operator selection

The parties who produce blocks and sign finality are **Settlement Operators** — network
identities collateralised with M0. Because M0 can originate only from verified BTC destruction,
Sybil resistance has an up-front acquisition cost paid before a single block is signed. One
Operator can run several nodes but counts **once**: the unit of consensus is the Operator key,
not the machine. **One Operator, one vote.**

> *Naming note:* in the node's RPC surface and source these identities keep their lineage
> name, **masternode** (`protx`, `getactivemnstatus`). The public model — what an Operator
> *is* — is the Settlement Operator. Commercial Clearing and Liquidity Provider roles are
> separate. → [Roles](../markets/roles.md)

## Block production

A deterministic pseudo-random draw designates each block's producer — every node computes the
same result from the previous block hash, with no communication and no mining. One block every
**60 seconds**. If the designated producer is absent, a fallback schedule lets the next in line
produce: the chain never stalls on a missing node. Because the designation is deterministic, a
block signed by the wrong Operator is rejected by every node.

## Finality

Finality comes from a **per-Operator committee, redrawn at every block by verifiable random
function (ECVRF)**. Each selected Operator publishes a VRF proof with its signature; everyone
verifies the draw. The committee input is public, but the output depends on each Operator's
secret key — so nobody, including the block producer, can predict or grind the committee.

The threshold is `⌈2/3 · min(E, N)⌉` where `N` is the eligible Operator count at the block and `E` a fixed committee
cap — the same rule scales from a handful of Operators to hundreds without retuning. One round
of signatures, **~1 minute** to irreversibility. Once final, a block cannot be reorganised —
finality overrides the longest chain, whatever the chainwork.

## State transition

Finality sits **on top of** full block validation, never instead of it. Every node fully
validates every transaction; a quorum — even a hypothetically malicious one — cannot mint value,
break the [accounting invariants](../reference/invariants.md), or confirm an invalid transaction.
What the signers control is ordering, never the money.

## Script engine

Bitcoin Script, extended with the covenant opcodes Bitcoin has debated for a decade —
templates, introspection, oracle signatures, Bitcoin-fact verification.
→ [Script & opcodes](../reference/opcodes.md)

## Block subsidy and internal-unit origin

There is no block subsidy: `block_reward = 0`, no treasury and no premine. Coinbase pays
exactly the block's fees. Separately, M0 can be created only from verified BTC destructions
under A5. That creation path is not a reward or discretionary issuance
([From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)).

## Where the rest is

The design choices behind these mechanisms (signature scheme, why there is no slashing) and
what a threshold coalition can and cannot do are on the [security model](security-model.md);
the work of opening the Operator set is on [Open-network hardening](open-network-hardening.md);
the current status of the network is on [Status & claims](status-and-claims.md).

**Primitives:** deterministic producer draw · ECVRF finality committee · `⌈2/3 · min(E, N)⌉` · `block_reward = 0`
**Reference:** [Consensus parameters](../reference/consensus-parameters.md)
