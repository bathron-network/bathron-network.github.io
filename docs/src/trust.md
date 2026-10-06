# 02 · Where trust lives

> **Normative source:** [N-SPEC v0.7, preamble][np], [§4.9][n49], [§12.15][n1215], [§17.6][n176], [§18][n18]; [WHY-N §3][w3], [§7][w7]; [ATTACKS §2][a2].
> This page explains; it does not restate rules or parameter values.

Assessing a settlement means identifying its dependencies. Bitcoin evidence, selection of a BATHRON history and a provider's external delivery answer different questions. Inclusion in an N chain does not remove the responsibilities of the party delivering an external asset. [N-SPEC v0.7, preamble][np], [§18][n18]; [WHY-N §7][w7]

## Locate each responsibility

| Layer or role | What to examine |
|---|---|
| Bitcoin | The evidence each node verifies and the Bitcoin reference used for the N block. [N-SPEC v0.7 §8.4][n84], [§11.1][n111] |
| N | Validation of each history and selection of one; its quantitative claims hold only within the published domain. [N-SPEC v0.7 §1.1][n11], [§17.1][n171] |
| Provider | The external value it delivers and the depth it chooses before delivery. [WHY-N §7][w7] |
| Application | Whether its presentation distinguishes explicit facts, local observations and model results. [N-SPEC v0.7 §16.1][n161] |
| User | Whether the stated policy and dependencies suit the operation being considered. [N-SPEC v0.7 §1.1][n11]; [WHY-N §7][w7] |

These are questions to ask of a service, not additional consensus rules. A provider's chosen policy does not change N's validation or chain selection rules. [N-SPEC v0.7 §1.1][n11]

## Bitcoin evidence has a boundary

BATHRON reads Bitcoin; it never commands it. There is no native finality. Inclusion on BATHRON, at any depth, does not move an external asset. N cannot undo an external delivery. The party making that delivery therefore retains a separate responsibility even when the BATHRON operation meets its depth policy. [N-SPEC v0.7, preamble, point 3][np], [§18][n18]; [WHY-N §7][w7]

M0 also has a distinct boundary: a burn irreversibly destroys bitcoin. It creates no recoverable Bitcoin reserve or claim on Bitcoin. Relying on BATHRON therefore includes relying on its consensus and on M0, alongside the dependencies of the external leg. [N-SPEC v0.7 §4.9][n49]; [WHY-N §3][w3], [§7][w7]

## Waiting is part of the model

Wait or stop rather than be wrong. A settlement may wait hours; the network may pause to resolve a conflict. This describes a design choice within the published domain, not an unconditional outcome. Suspensions can occur without an attack. Outside the domain, N makes no quantitative claim, and a departure from the domain need not trigger STOP. [N-SPEC v0.7 §14.4][n144], [§17.6][n176], [§18][n18]; [WHY-N §7][w7], [§8][w8]

## An origin is another dependency

A new node, or a returning node whose reception left the published domain, needs a recent authenticated origin before relying on the registry agreement claim. Exceptional recovery requires explicit acceptance of that origin. Signatures alone do not establish its honesty. [N-SPEC v0.7 §12.14][n1214], [§12.15][n1215], [§18][n18]

Read the published [limits][n18] and [H1 counterexamples][a2] before treating a fingerprint as complete protection against conflicting histories.

## See also

[The N engine](engine.md), [Depth and statuses](depth.md), [Burns](burns.md), and [Who does what](roles.md).

[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
[n49]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#49-burn-m0-v3
[n1215]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1215-nœuds-nouveaux-ou-de-retour--subjectivité-faible
[n176]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#176-comportement-hors-domaine
[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[a2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/ATTACKS.md#2-long-range-and-h1
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[n111]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#111-vue-bitcoin
[n11]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#11-catégories-normatives
[n171]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#171-domaine-h_n--principe
[n161]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#161-catégories
[n144]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#144-suspensions-sans-attaque
[w8]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#8-what-n-guarantees-under-h_n-and-what-it-does-not
[n1214]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1214-récupération-exceptionnelle
