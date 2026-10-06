# 01 · BATHRON in five minutes

> **Normative source:** [N-SPEC v0.7, preamble][np], [§1.4][n14], [§7.1][n71], [§8.4][n84] (in French); [WHY-N §3][w3], [§7][w7]; [APP-SPEC v1 draft §0.4][p04] (in French).
> This page explains; it does not restate rules or parameter values.

BATHRON is a settlement network with its own chain, separate from Bitcoin and rooted in it. [N-SPEC v0.7, preamble][np]; [WHY-N §3][w3]

A settlement needs a way to distinguish valid operations from the history in which they appear. BATHRON separates those questions. Bitcoin establishes the origins of resources. Objects carry provenance and conservation obligations. N, the consensus engine, selects a history when valid evolutions become incompatible. Selecting a history does not itself establish conservation; that also depends on the application rules. [WHY-N §3][w3]

## What Bitcoin contributes

Bitcoin supplies roots, verified facts, time and randomness. Each node checks Bitcoin data in the context of the Bitcoin reference block designated by an N block. A producer cannot substitute a personal account of what happened on Bitcoin. N reads Bitcoin without changing its rules. [N-SPEC v0.7, preamble, point 3][np], [§8.4][n84], [§11.1][n111]

## How N chooses a history

One producer is selected for each slot from the active ticket registry, using a seed derived from Bitcoin. There is no committee, no quorum and no vote. N ranks valid chains by their production blocks and uses a public tie-break independent of block content. It selects a chain; it does not merge incompatible blocks. [N-SPEC v0.7 §5.3][n53], [§5.4][n54], [§7.1][n71], [§9.3][n93], [§1.4, invariant 17][n14]; [WHY-N §2][w2]

## M0 and burned bitcoin

M0 is the settlement asset. Its origin is burned bitcoin. An M0 burn creates M0; a ticket burn gives production weight to a registered identity. Reactivation restores suspended participation rights. Ticket and reactivation burns create no M0. Fees transfer existing M0, and there is no block reward. A burn leaves no Bitcoin reserve that can be reclaimed. [APP-SPEC v1 draft §0.4][p04]; [N-SPEC v0.7 §1.4, invariants 1–4 and 12][n14], [§4.9][n49], [§6.7][n67]; [WHY-N §3][w3]

## Depth is a decision

There is no native finality. Inclusion starts a depth assessment. The participant delivering value outside BATHRON chooses a depth from the published table, within the published domain: the network, clock and adversary assumptions under which N's quantitative claims hold. Settlement may take hours, and conflicts may stop progress. Outside that domain, N makes no quantitative claim. [WHY-N §7][w7], [§8][w8]; [N-SPEC v0.7 §1.4, invariant 18][n14], [§17.1][n171], [§17.2][n172], [§17.6][n176], [§18][n18]

## Who takes responsibility

Producers are registered identities selected to produce blocks. Settlement Providers handle BTC/M0; Liquidity Providers handle X/M0, where X is another asset. Providers choose their delivery depth. Builders create interfaces, users choose terms, and observers examine evidence: these are responsibilities around a service, distinct from the production role. [N-SPEC v0.7 §4.1][n41], [§7.1][n71]; [APP-SPEC v1 draft §0.4][p04], [§13, principle][p13]; [WHY-N §7][w7]

## See also

[The N engine](engine.md), [Producers and tickets](producers.md), [Depth and statuses](depth.md), [Burns](burns.md), [Who does what](roles.md), and [Where trust lives](trust.md).

[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[p04]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés
[n111]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#111-vue-bitcoin
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n54]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#54-graine
[n93]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#93-score-et-rang
[w2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#2-why-n-exists
[n49]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#49-burn-m0-v3
[n67]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#67-exclusion-et-react
[w8]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#8-what-n-guarantees-under-h_n-and-what-it-does-not
[n176]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#176-comportement-hors-domaine
[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[n41]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#41-identité
[p13]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#13-règlement-btcm0-à-un-saut
[n171]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#171-domaine-h_n--principe
[n172]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#172-hypothèses-du-domaine
