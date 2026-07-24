# Roadmap

Three phases, **gated, not scheduled**. Each phase must earn the next — a date would
be a promise the code hasn't made yet. What follows is the honest engineering path,
including the parts that are hard.

<svg viewBox="0 0 660 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three gated phases: private testnet, public testnet, mainnet">
  <line x1="70" y1="46" x2="590" y2="46" stroke="#1C222C" stroke-width="2"/>
  <line x1="70" y1="46" x2="330" y2="46" stroke="#D9A441" stroke-width="2" opacity=".55"/>
  <g font-family="ui-monospace,Menlo,monospace">
    <circle cx="70" cy="46" r="8" fill="#3A4150"/>
    <circle cx="330" cy="46" r="9" fill="#D9A441"/>
    <circle cx="590" cy="46" r="8" fill="#0C0F14" stroke="#3A4150" stroke-width="2"/>
    <text x="70" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Private testnet</text>
    <text x="70" y="74" text-anchor="middle" fill="#8A919C" font-size="11">done · surface proven</text>
    <text x="330" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Public testnet</text>
    <text x="330" y="74" text-anchor="middle" fill="#8A919C" font-size="11">now · first builders</text>
    <text x="590" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Mainnet</text>
    <text x="590" y="74" text-anchor="middle" fill="#8A919C" font-size="11">gated · audits + economics</text>
    <text x="200" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: it works, live</text>
    <text x="460" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: open-network safe</text>
  </g>
</svg>

---

## Done — Private testnet

A multi-node network ran the **entire consensus surface** live: VRF finality, the
in-consensus Bitcoin header chain, burn → mint, the covenant opcodes, shielded
transfers, and the flagship flow end-to-end — a real Bitcoin payment releasing a
covenant, and an atomic BTC-out swap.

The consensus surface was **frozen** during this phase. The work was not new
features — it was proof: every primitive exercised on-chain (accept *and* reject
paths), adversarial red-teaming, fuzzing the money chokepoints, and the tooling that
makes a launch repeatable. The codebase was driven to *zero legacy and zero dead
code*, so what froze is exactly what runs.

**Its gate was passed:** the full surface proven live, no open monetary or safety
issue, a clean launch genesis rehearsed — which is why the next phase exists.

## Now — Public testnet

**This is the current phase.** The network is open: published genesis and peers, a
public block explorer, the **Clearing and Liquidity Provider prototypes**, the SDK,
and runnable examples. The public testnet is deliberately built to differ from
mainnet in as few ways as possible: same block rules, same invariants, same finality
math, same M0-origin rule based on verified BTC destruction. The differences that
remain are the ones that *must* differ — the Bitcoin network it reads (Signet vs
mainnet), the genesis message, and the address identity bytes.

The goal of this phase is a single, unglamorous thing: **the first builders shipping
on the substrate.** Everything else serves that. Disposable-genesis resets remain
possible while the network stabilizes, so early operators and builders can move
without fear of a permanent mistake.

This is also where the operator set begins to open — from a closed, launcher-run set
toward independent operators. That transition is what the *Open-network hardening*
track below exists to make safe.

**Gate to mainnet:** the open-network hardening items resolved or explicitly bounded,
and the external audits returned.

## Then — Mainnet

**Gated, not scheduled — and not planned for any date.** The hard prerequisites are real and named below. Mainnet
carries real value, so it also carries the one rule that never bends: **genesis
itself is SPV-verified like every block after it** — no special case, no bypass, no
premine. Any first internal unit on mainnet would have to originate from a verified Bitcoin
destruction, exactly like the
millionth.

The mechanical launch steps — mine and pin the mainnet genesis with a recency proof,
flip the covenant gates to active, ship the non-disposable mainnet bootstrap tooling —
are written down and mostly built. They are execution, not research. The
research-shaped prerequisites are the hardening track.

---

## Open-network hardening

This is the honest core of the roadmap. The current public-testnet operator set is
**project-controlled**. That does not demonstrate Byzantine resistance under open
admission, and it does not remove software, key-compromise or correlated
infrastructure risk. Opening the operator set to independent parties is a different
threat model; the items below are prerequisites for that transition.

### The one thing that never changes

First, the guarantee that holds in every phase and underpins everything below:

> **The finality committee cannot touch the money.** Finality decides *ordering*,
> never issuance. Every node fully validates every block, so a quorum — even a fully
> captured one — cannot mint a unit, break the [monetary invariants](reference/invariants.md),
> or confirm an invalid transaction. M0 origin remains constrained by verified BTC destruction.

The invariants answer whether an invalid monetary state can be accepted by an honest
full node. The separate open-network question is whether a threshold can censor,
stall or create divergent finalized views. That is what the items below bound.

### The attack surface, stated plainly

With an open operator set and a Byzantine fraction *f*:

- **Liveness.** If roughly ⌈N/3⌉ operators go silent, finality *stalls* — it stops
  advancing until enough honest operators sign again. The chain keeps producing blocks
  (production has its own fallback); it is *irreversibility* that waits. Nothing is
  lost, nothing is forged — settlement simply isn't final yet.
- **Safety.** Only an adversary controlling **≥ the finality threshold across distinct
  eligible operator identities** could sign conflicting histories within a finality
  window. The money cannot be forged either way — but such an adversary *can* censor
  settlement, stall finality, and present **divergent finalized views** to different
  parts of the network. Each honest node's chain-level guard rejects any block that
  would rewrite a height *it* has finalized, from any fork, regardless of chainwork;
  reconciling divergent views across nodes is an operational event, not an automatic one.

The committee draw is **non-grindable**: a per-block ECVRF over each operator's *secret*
key, so an attacker cannot predict or steer which operators will be drawn — which is
what makes adaptive corruption hard. The levers below turn "bounded" into "priced out."

### The work

- **Operator liveness — studied, and deliberately left in consensus as-is.**
  An operator's liveness is inferred from *block production*: a missed, deterministically
  scheduled slot is chain-evident, so eviction rests on evidence every node computes
  identically. It samples each operator about once every N blocks, so a silent failure is
  noticed in roughly 3·N blocks. We investigated replacing this with a
  *finality-participation* signal (detect a dead operator in a handful of blocks) and
  **set it aside**: under the private-VRF committee, "did not sign" is indistinguishable
  from "was not selected," and anchoring a participation view would feed a gossip,
  fork-dependent signal into a consensus parameter — which our eligibility invariant
  forbids. Production-based eviction turns out to be the censorship-optimal choice its
  slower latency is the price of, not a defect. **So the consensus signal stays as it is,
  and the fast "is this operator up right now?" question moves to the market/reputation
  layer — the indexers, wallets and applications that already choose operators — where it
  belongs and carries no consensus risk.**

- **Bounding value-at-risk per finality window.** Because settlement is only reversible
  until it finalizes (~1 minute), the value actually at risk in a worst-case committee
  capture is the value that settles *within one window*. Bounding that — and letting
  high-value settlement **require stronger-than-default finality** (a larger committee
  or more confirmations, chosen by the operators or the application) — turns a
  catastrophic tail into a capped, priced one. It is the strongest lever, and nearly
  free: because the money can't be forged, the only thing left to bound is timing.

- **Committee sizing.** The threshold auto-scales as `⌈2/3 · min(E, N)⌉`, so no constant
  needs retuning as operators join. Setting the committee cap *E* for an open network is
  a security-budget decision — large enough that a random draw statistically yields an
  honest supermajority against an adversary approaching ⅓.

- **Collateral economics.** The chain of costs is explicit: **BTC destruction is what
  creates M0; registering an operator identity requires locking M0 collateral** — M0
  the operator may equally have acquired from a third party rather than burned for.
  The finality threshold is counted over **distinct eligible identities**, so the
  Sybil question is the price of that lock: setting it so that acquiring ≥ the
  threshold of identities costs more than flows through a finality window is the
  economic half of the safety argument, decided at opening. Operating a node carries
  **no guaranteed commercial revenue** — fees are market-driven.

- **External cryptographic audit of the VRF module.** Finality has a single path — the
  ECVRF sortition — so its implementation is the hardest mainnet gate. An internal audit
  has already de-risked it (correctness against known-answer vectors, fixed
  undefined-behavior on malformed proofs, hardened key registration); an **independent
  external audit is a hard, non-negotiable gate** before real value.

- **Separating the producer and the provider.** An operator that both produces blocks
  and also competes as a Clearing or Liquidity Provider could, in principle, order or delay a
  competitor's settlement (an MEV-like edge). The roles are kept **protocol-separable**
  even though they are business-combinable — an open-network design item, not a
  permissioned-launch one.

### No slashing — a deliberate choice, restated

Deterrence is the **up-front cost of acquiring and locking M0 collateral** plus
**proof-of-service bans** (loss of eligibility to produce — an opportunity cost, since
no revenue is guaranteed in the first place), never confiscation. A slashing bug can
destroy honest operators' funds — a catastrophic, irreversible failure mode seen on
other chains — and it buys little the up-front cost and bans don't already provide.
This will not be reconsidered.

---

## Not on the roadmap

Discipline is part of the design, so some things are *deliberately absent* — listing
them matters as much as listing the work:

- **No token, no treasury, no yield, no governance coin.** Security is funded by fees;
  there is nothing to issue and nothing to vote a subsidy for.
- **No protocol rewards or ranking for operators.** The protocol publishes *facts*
  about operators (uptime, age, blocks, service history) and never says one is better —
  [applications choose](learn/settlement-providers.md), the market decides.
- **No changeable origin rule.** One verified destroyed satoshi permits one M0 unit. There is no
  mechanism to change that, and there will not be one.
- **No feature sprawl.** The substrate is meant to stay small and *finished*. What
  should grow is what's built on it, not the kernel.

> If this page has to change often, something has gone wrong. The consensus surface is
> frozen on purpose; the roadmap is mostly a list of proofs to finish and permissions
> to safely remove — not features to add.
