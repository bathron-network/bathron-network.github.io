# Why the consensus is frozen

Most protocols promise features. BATHRON promises the opposite: the consensus — the small set
of rules every node enforces — is frozen, and everything of value is meant to grow *above* it.
This matters to anyone building a market here, because it is what makes the ground stable: the
rules a market settles under will not shift because a feature became fashionable.

## The rule

The freeze is not a mood; it is a written rule with a burden of proof:

> **Any addition to consensus must demonstrate that it enables something impossible to obtain
> cleanly in a higher layer. Failing that, it is rejected.**

Three things follow from how the rule is phrased:

- **The burden is on the addition, never on the absence.** Nobody has to justify *not* adding
  something. The proposal has to prove that markets, wallets, indexers or applications
  genuinely cannot do the job.
- **The test is about a concrete, current need — never a "future possibility".** A hard fork
  for a proven need is preferable to consensus surface kept around for a hypothetical one.
- **The price of a consensus line is understood up front.** Every line of consensus is decades
  of maintenance, a format that can never change again, and an attack surface every node
  carries forever.

TCP/IP is a fair analogy: the protocol stayed small and dull, and the web grew on top of it.
Nobody asks TCP to add a shopping cart.

## What lives above consensus

Because of the rule, the things people usually expect a protocol to grow are placed in the layer
above, where they can evolve, compete and be replaced without touching the rules:

- **Markets and quotes** — a pair exists because someone brings inventory and publishes a
  price; the protocol only settles ([How a market appears](../markets/how-a-market-appears.md)).
- **Applications** — escrow, delivery-versus-payment, hedging, fixed-term positions are
  compositions of covenants, HTLCs, timelocks and Bitcoin facts, not protocol features.
- **Reputation and provider choice** — the protocol publishes facts about Operators (age,
  blocks produced, service history) and never says one is better; wallets and indexers rank,
  the market decides.
- **Fast liveness signals** — "is this Operator up *right now*?" is answered by indexers and
  applications, not by consensus. Consensus keeps only the slow, chain-evident signal (block
  production), because a fast gossip signal fed into consensus would let a network adversary
  change who counts toward finality. That decision was studied and settled
  ([Open-network hardening](open-network-hardening.md)).

The same discipline already rejected proposals that sounded reasonable — for instance a
consensus-level link between an Operator and a service identity, which turned out to be an
ordinary signed attestation any wallet can verify off-chain.

## Not on the roadmap

Discipline is part of the design, so some things are *deliberately absent* — listing them
matters as much as listing the work:

- **No token, no treasury, no yield, no governance coin.** Security is funded by fees; there is
  nothing to issue and nothing to vote a subsidy for.
- **No protocol rewards or ranking for Operators.** The protocol publishes *facts* about
  Operators and never says one is better — [applications choose](../markets/roles.md), the
  market decides.
- **No changeable origin rule.** One verified destroyed satoshi permits one M0 unit. There is
  no mechanism to change that, and there will not be one.
- **No feature sprawl.** The substrate is meant to stay small and *finished*. What should grow
  is what is built on it, not the kernel.
- **No slashing.** Deterrence is the up-front cost of acquiring and locking M0 collateral plus
  proof-of-service bans, never confiscation. A slashing bug can destroy honest Operators' funds
  — a catastrophic, irreversible failure seen on other chains — and it buys little the up-front
  cost and bans do not already provide. This is a deliberate choice and will not be reconsidered.

## What "frozen" does not mean

Frozen does not mean nothing ever changes. A demonstrable bug or vulnerability is fixed. The
open-network hardening work — auditing the finality path, sizing committees, pricing collateral
— is a list of proofs to finish and permissions to safely remove, not features to add. It means
the *shape* of consensus is finished, and the site describing it should rarely need to change:

> If this page has to change often, something has gone wrong. The currently deployed surface is
> intentionally narrow, and any consensus change requires an explicit protocol and governance
> decision; the roadmap is mostly a list of proofs to finish and permissions to safely remove
> — not features to add.

**See also:** [What BATHRON deliberately does not do](../provides/what-it-does-not-do.md) · [Production and finality](production-and-finality.md) · [Status & claims](status-and-claims.md)
