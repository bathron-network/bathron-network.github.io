# Roadmap

Three phases, **gated, not scheduled**. Each phase must earn the next — a date would
be a promise the code hasn't made yet. What follows is the honest engineering path,
including the parts that are hard.

<svg viewBox="0 0 660 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three gated phases: private testnet, public testnet, mainnet">
  <line x1="70" y1="46" x2="590" y2="46" stroke="#1C222C" stroke-width="2"/>
  <line x1="70" y1="46" x2="210" y2="46" stroke="#D9A441" stroke-width="2" opacity=".55"/>
  <g font-family="ui-monospace,Menlo,monospace">
    <circle cx="70" cy="46" r="9" fill="#D9A441"/>
    <circle cx="330" cy="46" r="8" fill="#0C0F14" stroke="#3A4150" stroke-width="2"/>
    <circle cx="590" cy="46" r="8" fill="#0C0F14" stroke="#3A4150" stroke-width="2"/>
    <text x="70" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Private testnet</text>
    <text x="70" y="74" text-anchor="middle" fill="#8A919C" font-size="11">now · frozen surface</text>
    <text x="330" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Public testnet</text>
    <text x="330" y="74" text-anchor="middle" fill="#8A919C" font-size="11">next · first builders</text>
    <text x="590" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Mainnet</text>
    <text x="590" y="74" text-anchor="middle" fill="#8A919C" font-size="11">gated · audits + economics</text>
    <text x="200" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: it works, live</text>
    <text x="460" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: open-network safe</text>
  </g>
</svg>

---

## Now — Private testnet

A multi-node network runs the **entire consensus surface** live: VRF finality, the
in-consensus Bitcoin header chain, burn → mint, the covenant opcodes, shielded
transfers, and the flagship flow end-to-end — a real Bitcoin payment releasing a
covenant, and an atomic BTC-out swap.

The consensus surface is **frozen**. Work at this stage is not new features — it is
proof: every primitive exercised on-chain (accept *and* reject paths), adversarial
red-teaming, fuzzing the money chokepoints, and the tooling that makes a launch
repeatable. The codebase has been driven to *zero legacy and zero dead code*, so what
freezes is exactly what runs.

**What "close to mainnet" means here.** The private testnet is deliberately built to
differ from mainnet in as few ways as possible: same block rules, same invariants,
same finality math, same burn-backed issuance. The differences that remain are the
ones that *must* differ — the Bitcoin network it reads (Signet vs mainnet), the
genesis message, and the address identity bytes. Everything else is the launch code.

**Gate to the next phase:** the full surface proven live, no open monetary or safety
issue, a clean launch genesis rehearsed.

## Next — Public testnet

The network opens. Published genesis and peers, a public block explorer, the
**Clearing and Liquidity Provider prototypes**, the SDK, and runnable examples.

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

**Gated, not scheduled.** The hard prerequisites are real and named below. Mainnet
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

This is the honest core of the roadmap. Today's network is **permissioned**: the
maintainer runs the operators, so there is no adversary holding a fraction of them,
and the system is sound for that phase. Opening the operator set to untrusted parties
is a different threat model — and these are the items that close the gap. **None of
them is a bug in the running system;** each is a prerequisite for *removing the
permission*.

### The one thing that never changes

First, the guarantee that holds in every phase and underpins everything below:

> **The finality committee cannot touch the money.** Finality decides *ordering*,
> never issuance. Every node fully validates every block, so a quorum — even a fully
> captured one — cannot mint a unit, break the [monetary invariants](reference/invariants.md),
> or confirm an invalid transaction. All value is burned Bitcoin, verified by SPV.

So the open-network question is never "can someone steal the money" — the invariants
answer that. It is narrower and honest: **can someone disrupt or reorder *settlement*
before it finalizes.** That is what the items below bound.

### The attack surface, stated plainly

With an open operator set and a Byzantine fraction *f*:

- **Liveness.** If roughly ⌈N/3⌉ operators go silent, finality *stalls* — it stops
  advancing until enough honest operators sign again. The chain keeps producing blocks
  (production has its own fallback); it is *irreversibility* that waits. Nothing is
  lost, nothing is forged — settlement simply isn't final yet.
- **Safety.** Only an adversary controlling **≥ the finality threshold** could sign two
  conflicting histories (equivocate) within a finality window — and even then the money
  is safe, so the damage is bounded to *re-ordering unfinalized settlement*. The
  chain-level guard already rejects any block that would rewrite an *already-finalized*
  height, from any fork, regardless of chainwork.

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

- **Collateral economics.** Each operator identity is bought by **burning real Bitcoin**
  up front — a Sybil cost paid in advance, not a refundable stake. Pricing it so that
  acquiring ≥ the finality threshold costs more than flows through a finality window is
  the economic half of the safety argument, decided at opening.

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

Deterrence is the **up-front burned-BTC collateral** plus **proof-of-service bans**
(loss of future fees), never confiscation. A slashing bug can destroy honest operators'
funds — a catastrophic, irreversible failure mode seen on other chains — and it buys
little the burn cost and bans don't already provide. This will not be reconsidered.

---

## Not on the roadmap

Discipline is part of the design, so some things are *deliberately absent* — listing
them matters as much as listing the work:

- **No token, no treasury, no yield, no governance coin.** Security is funded by fees;
  there is nothing to issue and nothing to vote a subsidy for.
- **No protocol rewards or ranking for operators.** The protocol publishes *facts*
  about operators (uptime, age, blocks, service history) and never says one is better —
  [applications choose](learn/settlement-providers.md), the market decides.
- **No new monetary policy.** One burned satoshi, one unit, forever. There is no
  mechanism to change that, and there will not be one.
- **No feature sprawl.** The substrate is meant to stay small and *finished*. What
  should grow is what's built on it, not the kernel.

> If this page has to change often, something has gone wrong. The consensus surface is
> frozen on purpose; the roadmap is mostly a list of proofs to finish and permissions
> to safely remove — not features to add.
