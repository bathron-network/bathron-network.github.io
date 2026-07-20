# Consensus

Two separate layers, deliberately kept apart:

| Layer | Question it answers | Property |
|---|---|---|
| **Production** | who makes the next block | liveness |
| **Finality** | when is a block irreversible | safety |

## Operator selection

Validators are **Settlement Operators**—network identities collateralised with M0. Because M0
can originate only from verified BTC destruction, Sybil resistance has an up-front acquisition cost paid
before a single block is signed. One operator can run several nodes but counts
**once**: the unit of consensus is the operator key, not the machine.

> *Naming note:* in the node's RPC surface and source these identities keep their
> lineage name, **masternode** (`protx`, `getactivemnstatus`). The public model —
> what an operator *is*—is the Settlement Operator. Commercial CP/LP roles are separate.
> → [Clearing and Liquidity Providers](settlement-providers.md)

## Block production

A deterministic pseudo-random draw designates each block's producer — every node computes the same result from the previous block hash, with no communication and no mining. One block every **60 seconds**. If the designated producer is absent, a fallback schedule lets the next in line produce: the chain never stalls on a missing node.

## Finality

Finality comes from a **per-operator committee, redrawn at every block by verifiable random function (ECVRF)**. Each selected operator publishes a VRF proof with its signature; everyone verifies the draw. The committee input is public, but the output depends on each operator's secret key — so nobody, including the block producer, can predict or grind the committee.

The threshold is `⌈2/3 · min(E, N)⌉` where `N` is the operator count and `E` a fixed committee cap — the same rule scales from a handful of operators to hundreds without retuning. One round of signatures, **~1 minute** to irreversibility. Once final, a block cannot be reorganized — finality overrides the longest chain.

## State transition

Finality sits **on top of** full block validation, never instead of it. Every node fully validates every transaction; a quorum — even a hypothetically malicious one — cannot mint value, break the [monetary invariants](../reference/invariants.md), or confirm an invalid transaction. What the signers control is ordering, never the money.

## Script engine

Bitcoin Script, extended with the covenant opcodes Bitcoin has debated for a decade — templates, introspection, oracle signatures, Bitcoin-fact verification. → [Script & opcodes](../reference/opcodes.md)

## Block subsidy and internal-unit origin

There is no block subsidy: `block_reward = 0`, no treasury and no premine. Coinbase pays exactly
the block's fees. Separately, M0 can be created only from verified BTC destructions under A5.
That creation path is not a reward or discretionary issuance.

## Design choices

- **ECDSA on secp256k1 only.** No BLS, no aggregated signatures — explicit signatures are simpler to audit at these committee sizes.
- **No slashing.** Deliberate: a slashing bug can destroy honest operators' funds. Deterrence is the burned-BTC collateral (paid up front) plus proof-of-service bans (loss of future fees).

## Threat model, honestly

The network is **permissioned today** — the launcher runs the operators, so no
adversary holds a fraction of them, and the system is sound as-is. Opening the
operator set is a different threat model, and the guarantee that matters most survives
it: because finality sits *on top of* full validation, a captured committee could at
worst stall or re-order **unfinalized** settlement — it can never mint value or break
the invariants. Making the open-network transition safe (finality-participation
liveness, value-at-risk bounds, committee sizing, the external VRF audit) is the
[roadmap](../roadmap.md)'s open-network hardening track — named work, not hidden risk.
