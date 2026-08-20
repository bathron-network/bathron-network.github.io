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

Four quantities must be kept apart, because the arithmetic below depends on which one is meant.
The definitions follow the implementation (`HuActiveFinalityThreshold`, `IsVrfSelected` in
`src/state/quorum.cpp`), not a textbook:

| Quantity | Meaning |
|---|---|
| **N** — eligible set | distinct Operator identities eligible at a given block |
| **E** — expected committee size | a fixed parameter (128 on mainnet and testnet). It is a *target*, not a hard cap: when `N > E` the realised size varies around it and can exceed it |
| **q** — quorum | signatures needed for a finality certificate: **`q = ⌈2/3 · min(E, N)⌉`** — computed from the *eligible* count, never from how many were actually drawn |
| **m** — drawn committee | who may sign that block: while `N ≤ E`, **everyone** (`m = N`, deterministic); when `N > E`, each Operator is drawn with probability `E/N`, so `m` is a random variable with mean `E` |
| **max(0, 2q − m)** — intersection | the minimum number of signers two *different* certificates for the same height must share (pigeonhole over the `m` who may sign) |

Below the Sybil floor (`nHuQuorumSize` = 4 distinct Operators, mainnet and testnet alike) the
threshold is *unreachable*: a network with fewer eligible Operators keeps producing blocks and
never finalizes.

### Regime 1 — everyone signs (`N ≤ E`; every deployment up to 128 Operators)

Here `m = N` exactly and `q = ⌈2N/3⌉`, so the arithmetic is exact:

- **Liveness.** If more than `N − q` Operators — roughly a third — go silent, finality *stalls*:
  it stops advancing until enough honest Operators sign again. The chain keeps producing blocks
  (production has its own fallback); it is *irreversibility* that waits. Nothing is lost, nothing
  is forged — settlement simply isn't final yet.
- **Safety.** Two conflicting certificates must share at least `2q − N` signers — **about a third,
  not two thirds** — and those shared signers are, by construction, equivocating. So an adversary
  holding roughly a third of the identities *and* a network split can present **divergent
  finalized views** to different parts of the network; at the full quorum it controls ordering
  (and censorship) outright. The money cannot be forged in either case — such an adversary can
  censor settlement, stall finality and equivocate, never mint. Each honest node's chain-level
  guard rejects any block that would rewrite a height *it* has finalized, from any fork,
  regardless of chainwork; reconciling divergent views across nodes is an operational event, not
  an automatic one.

Worked examples (`q = ⌈2N/3⌉`, minimum equivocators `= 2q − N`):

| eligible `N` (= drawn) | quorum `q` | stall needs (`N − q + 1` silent) | two conflicting certificates need |
|---|---|---|---|
| 4 (the floor) | 3 | 2 | **2** equivocators — `{A,B,C}` and `{A,B,D}` |
| 8 | 6 | 3 | **4** equivocators |
| 128 (= E, still everyone) | 86 | 43 | 44 equivocators |

Put together: **liveness and safety both degrade at about one third of the identities; full
control of ordering needs two thirds.** The economic sizing below is against the one-third
figure, never against the quorum.

### Regime 2 — sampling (`N > E`; not reached by any network to date)

The quorum stays fixed at `q = ⌈2E/3⌉` (86 at `E = 128`) while the drawn committee `m` varies
around `E` from block to block. Consequences that the exact arithmetic above no longer captures:

- the intersection of two certificates is `max(0, 2q − m)`, so the number of equivocators needed
  **shrinks when the draw is large** (`m = 128 → 44`; `m = 140 → 32`) — an **oversized** draw
  with `m ≥ 2q` (172 at `E = 128`; astronomically unlikely but not excluded by the rules) would
  in principle allow two disjoint certificates with no equivocator at all;
- liveness needs `q` live signers among the `m` drawn — an **undersized** draw makes a stall more
  likely, and a draw with `m < q` cannot finalize that block at all (no re-draw is defined);
- an adversary's share of the drawn committee is a random variable around its share of `N`,
  which is what committee sizing (below) is about.

How this regime should be bounded — whether the quorum should track the realised draw, and what
the fallback is when a draw is too small — is an **open design point**, not a documented property.
The examples above are stated only for regime 1. → [Status & claims](status-and-claims.md)

The committee draw is **non-grindable**: a per-block ECVRF over each Operator's *secret* key, so
an attacker cannot predict or steer which Operators will be drawn — which is what makes adaptive
corruption hard. The levers below turn "bounded" into "priced out."

## The work

- **Bounding value-at-risk until detection and halt.** Because the money cannot be forged, what a
  captured committee can damage is *ordering* — and only for as long as the capture lasts and
  applications keep accepting its finality. The bound to aim for is therefore the **cumulative
  value exposed between the start of a capture and the end of operational recovery** —
  detection of divergent views, wallets and applications halting acceptance, and the
  out-of-band reconciliation that follows — not merely the throughput of one ~1-minute window: a persistent coalition can attack successive heights, and "more
  confirmations" does not help if the same compromised identities finalize every block. The
  levers that do work are a cap on value settled per window (so the exposure per unit of
  detection time is bounded), a **larger committee** for high-value settlement (a statistical
  gain — it lowers the probability that a random draw hands the adversary a third, under the
  explicit assumptions that the adversary's identities are a minority of the eligible set and
  that the draw is unbiased; it does nothing against a majority), and fast out-of-band detection
  of divergent finality. This turns a catastrophic tail into a capped, priced one — provided the halt is
  real, which is an application-layer obligation as much as a consensus one.

- **Committee sizing.** The threshold auto-scales as `⌈2/3 · min(E, N)⌉`, so no constant needs
  retuning as Operators join. Setting the expected committee size *E* for an open network is a
  security-budget decision — large enough that a random draw statistically yields an honest
  supermajority against an adversary approaching ⅓ *of the eligible set*. Under the explicit
  assumptions above (minority adversary, unbiased draw), the probability that a committee of
  size `E` contains ≥ ⌈E/3⌉ adversarial identities falls exponentially in `E`; a larger cap buys
  resistance, it does not buy certainty, and in the sampling regime it interacts with the
  `2q − m` intersection described above (open design point).

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
  sortition — so its implementation is the hardest mainnet gate. What is publicly checkable today
  is the code and its tests in `bathron-core` — the vendored ECVRF module and
  `src/test/vrf_tests.cpp`, which exercises it against known-answer vectors. **No external
  cryptographic audit has been performed**, and an independent one is a hard, non-negotiable gate
  before real value.

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
