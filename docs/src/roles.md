# 07 · Who does what

> **Normative source:** [N-SPEC v0.7 §4.1][n41], [§7.1][n71], [§10.3][n103]; [WHY-N §2][w2], [§7][w7]; [APP-SPEC v1 draft §0.4][p04], [§ID, ID-1][pID], [§13, principle and rules 13-1–13-2][p13], [§R2P, R2P-1][pR2P].
> This page explains; it does not restate rules or parameter values.

Producing a block and delivering an external asset carry different responsibilities. A registered identity participates in the production draw. A provider chooses when to deliver outside value under its own depth policy. Keeping those roles distinct helps a user understand what a service offer actually covers. [N-SPEC v0.7 §4.1][n41], [§7.1][n71]; [WHY-N §7][w7]

## Production and services

A **producer** is a registered identity drawn to produce in a slot. Its active tickets determine its production weight. This role concerns the N engine, not approval of a commercial service. [N-SPEC v0.7 §5.3][n53], [§7.1][n71]

A **Settlement Provider (SP)** handles **BTC/M0** settlement. N-SPEC v0.7 keeps a historical application wording that was never adopted for any network. APP-SPEC v1 makes M0 the only settlement asset; its §13 differs from N-SPEC v0.7 §13 only in the asset. [APP-SPEC v1 draft §0.4][p04], [§13, principle and rules 13-1–13-2][p13], [§ID, ID-1][pID]

A **Liquidity Provider (LP)** handles **X/M0**, where X denotes the external asset. Independent liquidity providers settle with each other on M0, without trusting one another. The specifications define no order book and no pool. [APP-SPEC v1 draft §0.4][p04], [§R2P, R2P-1][pR2P]

SP and LP are service roles outside consensus. Neither role requires a registered identity or participation in block production. No provider is vetted by the protocol. These roles describe responsibility for settlement services, not a separate form of production authority. [N-SPEC v0.7 §4.1][n41], [§7.1][n71]; [APP-SPEC v1 draft §13, 13-1][p13]; [WHY-N §7][w7]

## Other responsibilities

Use these labels to distinguish responsibilities around a service:

| Role | Question it answers |
|---|---|
| Builder | Who creates the application or interface and explains its policy? |
| User | Who chooses the terms and authorizes the operation? |
| Observer | Who examines history or reports evidence? |

These are descriptive labels, not extra consensus roles. For each report, distinguish explicit data, local observations and model results. For each delivery, identify the party carrying the external exposure. [N-SPEC v0.7 §1.1][n11], [§16.1][n161]; [WHY-N §7][w7]

## Depth belongs to the exposed party

The provider delivering outside value chooses its depth within the published domain. Inclusion alone does not determine that decision. The depth table supplies a conditional risk bound; the provider supplies the policy for its exposure. [WHY-N §7][w7]; [N-SPEC v0.7 §17.3][n173]

## Read an offer as an offer

A quote is an offer from a provider, not an official protocol price. [WHY-N §2][w2], [§7][w7]

Neither service role is a listing authority. Reputation is an interpretation of evidence, not a production right. A single organization may perform several roles; assess each responsibility separately. [N-SPEC v0.7 §4.1][n41]; [WHY-N §7][w7]

Protocol accountability for proven equivocation is a permanent ban of the registered identity under the proof rules. It does not evaluate a provider's service quality. [N-SPEC v0.7 §10.1][n101], [§10.3][n103]

## See also

[Producers and tickets](producers.md), [Depth and statuses](depth.md), [The N engine](engine.md), and [Where trust lives](trust.md).

[n41]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#41-identité
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n103]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#103-ban
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[p04]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés
[pID]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#id-identifiant-applicatif-application_spec_id
[p13]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#13-règlement-btcm0-à-un-saut
[pR2P]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n11]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#11-catégories-normatives
[n161]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#161-catégories
[n173]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#173-table-kε-du-domaine
[n101]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#101-preuve-déquivoque
[w2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#2-why-n-exists
