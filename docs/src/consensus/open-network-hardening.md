# Open-network hardening

> Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator
> admission is **not yet open**: the current operator set is project-run while the
> open-admission threat model is worked.

This page is the work that separates the two halves of that sentence. Opening the Operator set
to independent parties is a different threat model from a project-run set: it must hold against
a Byzantine fraction of Operators, key compromise and correlated infrastructure failure. The
items below are the prerequisites for that transition — the honest core of what remains before
mainnet. Where the network stands against them is on [Status & claims](status-and-claims.md).

## The one thing that never changes

First, the guarantee that holds in every phase and underpins everything below:

> **The finality committee cannot touch the money.** Finality decides *ordering*, never
> issuance. Every node fully validates every block, so a quorum — even a fully captured one —
> cannot mint a unit, break the [accounting invariants](../reference/invariants.md), or confirm
> an invalid transaction. M0 origin remains constrained by verified BTC destruction.

The invariants answer whether an invalid monetary state can be accepted by an honest full node.
The separate open-network question is whether a threshold can censor, stall or create divergent
finalized views. That is what the items below bound.

## The attack surface, stated plainly

With an open Operator set and a Byzantine fraction *f*:

- **Liveness.** If roughly ⌈N/3⌉ Operators go silent, finality *stalls* — it stops advancing
  until enough honest Operators sign again. The chain keeps producing blocks (production has
  its own fallback); it is *irreversibility* that waits. Nothing is lost, nothing is forged —
  settlement simply isn't final yet.
- **Safety.** With a threshold `q = ⌈2/3·n⌉`, two conflicting finality certificates must share
  at least `2q − n` signers — **about a third of the committee, not two thirds**. So an adversary
  holding roughly ⌈N/3⌉ distinct identities *and* a network split can present **divergent
  finalized views** to different parts of the network; at the full threshold it controls
  ordering outright. (Example: `n = 4`, `q = 3` — certificates `{A,B,C}` and `{A,B,D}` need only
  two equivocating identities.) The money cannot be forged in either case — such an adversary
  can censor settlement, stall finality and equivocate, never mint. Each honest node's
  chain-level guard rejects any block that would rewrite a height *it* has finalized, from any
  fork, regardless of chainwork; reconciling divergent views across nodes is an operational
  event, not an automatic one.

Put together: **liveness and safety both degrade at about one third of the identities; full
control of ordering needs two thirds.** The economic sizing below is against the one-third
figure, not the threshold.

The committee draw is **non-grindable**: a per-block ECVRF over each Operator's *secret* key, so
an attacker cannot predict or steer which Operators will be drawn — which is what makes adaptive
corruption hard. The levers below turn "bounded" into "priced out."

## The work

- **Bounding value-at-risk until detection and halt.** Because the money cannot be forged, what a
  captured committee can damage is *ordering* — and only for as long as the capture lasts and
  applications keep accepting its finality. The bound to aim for is therefore the **cumulative
  value exposed between the start of a capture and the moment settlement halts** (divergent
  views become detectable, wallets and applications stop accepting), not merely the throughput
  of one ~1-minute window: a persistent coalition can attack successive heights, and "more
  confirmations" does not help if the same compromised identities finalize every block. The
  levers that do work are a cap on value settled per window (so the exposure per unit of
  detection time is bounded), a **larger committee** for high-value settlement (a statistical
  gain, chosen by the Operators or the application), and fast out-of-band detection of divergent
  finality. This turns a catastrophic tail into a capped, priced one — provided the halt is
  real, which is an application-layer obligation as much as a consensus one.

- **Committee sizing.** The threshold auto-scales as `⌈2/3 · min(E, N)⌉`, so no constant needs
  retuning as Operators join. Setting the committee cap *E* for an open network is a
  security-budget decision — large enough that a random draw statistically yields an honest
  supermajority against an adversary approaching ⅓.

- **Collateral economics.** The chain of costs is explicit: **BTC destruction is what creates
  M0; registering an Operator identity requires locking M0 collateral** — M0 the Operator may
  equally have acquired from a third party rather than burned for. Finality is counted over
  **distinct eligible identities**, so the Sybil question is the price of that lock — sized
  against the **one-third figure** above (enough identities to stall or, with a split, to
  equivocate), not against the full threshold: acquiring that many identities must cost more
  than the value exposed until a capture is detected and settlement halts. This is the economic
  half of the safety argument, decided at opening.
  Operating a node carries **no guaranteed commercial revenue** — fees are market-driven.

- **External cryptographic audit of the VRF module.** Finality has a single path — the ECVRF
  sortition — so its implementation is the hardest mainnet gate. An internal audit has already
  de-risked it (correctness against known-answer vectors, fixed undefined-behavior on malformed
  proofs, hardened key registration); an **independent external audit is a hard, non-negotiable
  gate** before real value.

- **Separating the producer and the provider.** An Operator that both produces blocks and also
  competes as a Clearing or Liquidity Provider could, in principle, order or delay a
  competitor's settlement (an MEV-like edge). The roles are kept **protocol-separable** even
  though they are business-combinable — an open-network design item, not a permissioned-launch
  one.

- **Operator liveness — studied, and deliberately left in consensus as-is.** The short version:
  the consensus signal stays slow and chain-evident, and the fast "is this Operator up right
  now?" question moves to the market layer. Details below.

<details>
<summary>Operator liveness: why the fast signal stays out of consensus</summary>

An Operator's liveness is inferred from *block production*: a missed, deterministically
scheduled slot is chain-evident, so eviction rests on evidence every node computes identically.
It samples each Operator about once every N blocks, so a silent failure is noticed in roughly
3·N blocks.

We investigated replacing this with a *finality-participation* signal (detect a dead Operator in
a handful of blocks) and **set it aside**: under the private-VRF committee, "did not sign" is
indistinguishable from "was not selected," and anchoring a participation view would feed a
gossip, fork-dependent signal into a consensus parameter — which our eligibility invariant
forbids. Production-based eviction turns out to be the censorship-optimal choice its slower
latency is the price of, not a defect.

**So the consensus signal stays as it is, and the fast "is this Operator up right now?" question
moves to the market/reputation layer — the indexers, wallets and applications that already
choose Operators — where it belongs and carries no consensus risk.** This is the
[consensus freeze rule](why-frozen.md) applied to a live question.

</details>

## No slashing — a deliberate choice, restated

Deterrence is the **up-front cost of acquiring and locking M0 collateral** plus
**proof-of-service bans** (loss of eligibility to produce — an opportunity cost, since no revenue
is guaranteed in the first place), never confiscation. A slashing bug can destroy honest
Operators' funds — a catastrophic, irreversible failure mode seen on other chains — and it buys
little the up-front cost and bans don't already provide. This will not be reconsidered.

**See also:** [Security model](security-model.md) · [Production and finality](production-and-finality.md) · [Why the consensus is frozen](why-frozen.md)
