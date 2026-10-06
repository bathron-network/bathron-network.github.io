# 03 · The N engine

> **Normative source:** [N-SPEC v0.7 §1.1][n11], [§1.4][n14], [§5.3][n53], [§5.4][n54], [§7.1][n71], [§9.3][n93], [§9.5][n95], [§12.1][n121], [§12.15][n1215], [§18][n18] (in French); [WHY-N §2][w2], [§3][w3], [§4][w4].
> This page explains; it does not restate rules or parameter values.

Valid operations can belong to incompatible histories. N answers which history to follow. It does not make an invalid operation valid or replace the application's conservation obligations. This distinction separates validation from chain selection. [N-SPEC v0.7 §1.1][n11], [§9.5][n95]; [WHY-N §3][w3]

## Production without voting

One producer per slot, drawn from burned tickets with a Bitcoin-derived seed. No committee, no quorum, no vote, no finality gadget. A registered identity's active tickets determine its weight in the draw. Selection identifies the producer for that slot; an absent producer has no replacement. [WHY-N §2][w2]; [N-SPEC v0.7 §5.3][n53], [§5.4][n54], [§7.1][n71]

Slots belong to epochs. The epoch registry and seed determine the production schedule mechanically. The seed uses Bitcoin and the registry; block content and producer signatures do not enter it. [N-SPEC v0.7 §5.1][n51], [§5.4][n54]

## Validation before selection

A signature does not excuse a broken rule. Nodes validate candidate histories before applying selection and local adoption rules. Historical validity and local permission to adopt a branch are distinct: a node can refuse adoption without declaring that branch historically invalid. [N-SPEC v0.7 §1.1][n11], [§9.5][n95]

The score counts valid production blocks since genesis. At equal score, a public tie-break independent of block content ranks the competing histories. A signature, checkpoint or arrival order adds no preference. N selects a chain; it does not merge blocks from incompatible histories. [N-SPEC v0.7 §9.3][n93], [§1.4, invariant 17][n14]

## Bitcoin supplies context, not an instruction to switch

Bitcoin supplies roots, verified facts, time and randomness. Each N block designates a Bitcoin reference; Bitcoin reorganisations have their own handling in N. [N-SPEC v0.7, preamble][np], [§5.4][n54], [§8.4][n84], [§11][n11doc]

Bitcoin fingerprints can trigger STOP. They never promote a branch. The H1 detector can leave the base decision unchanged, delay it or halt it. It cannot change a chain's score or select a replacement. [N-SPEC v0.7 §12.1][n121]

## Origins and limits

A new node, or a returning node that left the reception assumptions, needs a recent authenticated origin to enter the registry agreement domain. A node with a local origin does not replace it merely by receiving a bootstrap package. Exceptional recovery requires explicit acceptance. [N-SPEC v0.7 §12.12][n1212], [§12.14][n1214], [§12.15][n1215]

The quantitative claims depend on the [published domain H_N][n172]. Outside it, N makes no quantitative claim. H1 is not complete long-range protection, and a deep halt can persist while a conflict remains. Read the [limits][n18] and [published counterexamples][a2]. [N-SPEC v0.7 §17.6][n176]

## See also

[Producers and tickets](producers.md), [Depth and statuses](depth.md), [Where trust lives](trust.md), and [Glossary](glossary.md).

[n11]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#11-catégories-normatives
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n54]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#54-graine
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n93]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#93-score-et-rang
[n95]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#95-sélection-avec-veto-séparé
[n121]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#121-nature-de-h1
[n1215]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1215-nœuds-nouveaux-ou-de-retour--subjectivité-faible
[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[w2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#2-why-n-exists
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[w4]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#4-weak-subjectivity
[n51]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#51-créneaux
[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[n11doc]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#11-réorganisations-bitcoin
[n1212]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1212-initialisation-et-pouvoir-nul-du-bootstrap
[n1214]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1214-récupération-exceptionnelle
[n172]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#172-hypothèses-du-domaine
[a2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/ATTACKS.md#2-long-range-and-h1
[n176]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#176-comportement-hors-domaine
