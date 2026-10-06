# 08 · Glossary

> **Normative source:** [N-SPEC v0.7 §4.1][n41], [§5.1][n51], [§7.1][n71], [§9.3][n93], [§10.1][n101], [§12.1][n121], [§12.15][n1215], [§14.5][n145], [§17.3][n173]; [WHY-N §7][w7]; [APP-SPEC v1 draft §0.4][p04], [§13, principle][p13], [§R2P, R2P-1][pR2P].
> This page explains; it does not restate rules or parameter values.

## Production

**Slot** — A position in N's production schedule, assigned to a producer by the draw. [N-SPEC v0.7 §5.1][n51], [§7.1][n71]

**Epoch** — A mechanical interval for the registry and production schedule, with keys and weight fixed within it. [N-SPEC v0.7 §5.1][n51], [§1.4, invariant 8][n14]

**Registry** — The ordered set of active registered identities, their production keys and their ticket weight for an epoch. [N-SPEC v0.7 §5.3][n53]

**Ticket** — An entry right obtained by burning BTC, neither refundable nor transferable; exclusion suspends its active use and a ban destroys its right. [N-SPEC v0.7 §1.4, invariants 3–5][n14]

**Registered identity** — An identity with registered keys and participation rights obtained through Bitcoin ticket burns (formerly called Operator). [N-SPEC v0.7 §4.1][n41], [§4.6][n46]

**Producer** — The registered identity drawn to produce for a slot. [N-SPEC v0.7 §7.1][n71]

**TICKET (NEW/ADD)** — Bitcoin burn forms that add ticket rights; they create no M0 and do not reactivate an excluded identity. [N-SPEC v0.7 §4.4][n44], [§4.6][n46], [§1.4, invariant 1][n14]

**REACT** — Reactivation through an admissible Bitcoin burn tied to an exclusion record; it creates no M0. [N-SPEC v0.7 §6.7][n67], [§1.4, invariant 1][n14]

**KEYREG** — The key registration object used to establish an identity's control and production keys. [N-SPEC v0.7 §4.2][n42]

**ROTATE** — An authorized change of production key that preserves the identity and responsibility for earlier generations. [N-SPEC v0.7 §6.9][n69]

**Seed** — The input derived from Bitcoin and the registry that determines the production draw for an epoch. [N-SPEC v0.7 §5.4][n54]

**Score** — A chain's count of valid production blocks since genesis, used before the public tie-break. [N-SPEC v0.7 §9.3][n93]

**Equivocation** — Different signed headers for the same chain, identity and slot, with each signing key verified in its historical context. [N-SPEC v0.7 §10.1][n101]

**Ban** — Permanent removal of an identity's participation rights after an admissible proof matures; it does not remove past score. [N-SPEC v0.7 §10.3][n103]

**Exclusion** — Suspension of participation rights under the activity rules, distinct from a permanent ban. [N-SPEC v0.7 §6.6][n66], [§6.7][n67]

## Bitcoin and origins

**Reference block (`B.ref`)** — The Bitcoin block designated by an N block as the reference for its Bitcoin context. [N-SPEC v0.7 §8.4][n84]

**H1 detector** — A separate veto using Bitcoin fingerprints; it can delay or halt a decision but never promote a branch. [N-SPEC v0.7 §12.1][n121]

**STOP / deep halt** — A refusal to proceed under N's conflict protections; a deep halt can persist while the conflict remains. [N-SPEC v0.7 §9.5][n95], [§18][n18]

**BOOTSTRAP** — An authenticated origin package for a node without a local origin; it cannot replace an existing local origin. [N-SPEC v0.7 §12.12][n1212]

**RECOVERY** — Exceptional installation of a new origin through explicit acceptance of the exact recovery package and its consequences. [N-SPEC v0.7 §12.14][n1214]

**Weak subjectivity** — Dependence on a recent authenticated origin for a new node, or a returning node that left the reception assumptions, to enter the registry agreement domain. [N-SPEC v0.7 §12.15][n1215]

## Depth and settlement

**Depth** — Progress since an operation's inclusion, assessed under a participant's policy and the published domain. [N-SPEC v0.7 §14.5][n145], [§17.3][n173]

**K(ε) table** — The published relation between depth and a conditional bound on common-prefix failure per cut. [N-SPEC v0.7 §17.3][n173]

**Published domain H_N** — The assumptions within which N makes quantitative claims. [N-SPEC v0.7 §17.1][n171], [§17.2][n172]

**Application status** — A contextual description of an operation's position or condition, using the identifiers in the specification. [N-SPEC v0.7 §14.5][n145]

**Burn** — Irreversible destruction of BTC for an M0, ticket or reactivation purpose; it creates no Bitcoin reserve. [N-SPEC v0.7 §4.4][n44], [§4.9][n49], [§6.7][n67]; [WHY-N §3][w3]

**M0** — The settlement asset, originating only in M0 burns. [APP-SPEC v1 draft §0.4][p04]; [N-SPEC v0.7 §4.9][n49]

## Service labels

**Settlement Provider (SP)** — A service role handling BTC/M0 settlement and choosing its external delivery depth. [APP-SPEC v1 draft §0.4][p04], [§13, principle][p13]; [WHY-N §7][w7]

**Liquidity Provider (LP)** — A service role handling X/M0 and settling with other providers on M0. [APP-SPEC v1 draft §0.4][p04], [§R2P, R2P-1][pR2P]

**Builder** — The descriptive label for whoever creates an application or interface; distinguish its presentation of facts, observations and model results. [N-SPEC v0.7 §16.1][n161]

**User** — The descriptive label for whoever chooses terms and authorizes an operation; distinguish that choice from the external provider's depth policy. [WHY-N §7][w7]

**Observer** — The descriptive label for whoever examines history or reports evidence; the report's category and context matter. [N-SPEC v0.7 §16.1][n161]

## See also

[The N engine](engine.md), [Producers and tickets](producers.md), [Depth and statuses](depth.md), [Burns](burns.md), and [Who does what](roles.md).

[n41]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#41-identité
[n51]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#51-créneaux
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n93]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#93-score-et-rang
[n101]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#101-preuve-déquivoque
[n121]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#121-nature-de-h1
[n1215]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1215-nœuds-nouveaux-ou-de-retour--subjectivité-faible
[n145]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#145-statuts-applicatifs
[n173]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#173-table-kε-du-domaine
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[p04]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés
[p13]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#13-règlement-btcm0-à-un-saut
[pR2P]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n46]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#46-new-et-add
[n44]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#44-sortie-ticket
[n67]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#67-exclusion-et-react
[n42]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#42-keyreg
[n69]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#69-rotate
[n54]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#54-graine
[n103]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#103-ban
[n66]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#66-exclusions--frein-de-densité-et-plafonds
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[n95]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#95-sélection-avec-veto-séparé
[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[n1212]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1212-initialisation-et-pouvoir-nul-du-bootstrap
[n1214]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1214-récupération-exceptionnelle
[n171]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#171-domaine-h_n--principe
[n172]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#172-hypothèses-du-domaine
[n49]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#49-burn-m0-v3
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[n161]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#161-catégories
