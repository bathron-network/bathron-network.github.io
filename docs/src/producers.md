# 04 · Producers and tickets

> **Normative source:** [N-SPEC v0.7 §1.4][n14], [§4.1][n41], [§4.7][n47], [§5.3][n53], [§6.6][n66], [§6.7][n67], [§6.9][n69], [§7.1][n71], [§7.4][n74], [§7.6][n76], [§10.1][n101], [§10.3][n103] (in French); [WHY-N §2][w2].
> This page explains; it does not restate rules or parameter values.

A production right carries an entry cost and an obligation to participate. It does not establish independence between participants. Understanding the difference between a registered identity, its tickets and its production role helps explain both the draw and the consequences of misconduct. [N-SPEC v0.7 §4.1][n41], [§5.3][n53], [§6.6][n66], [§7.1][n71]; [WHY-N §2][w2]

## Identity, tickets and selection

A registered identity brings together registered keys and tickets burned on Bitcoin. KEYREG records its keys; admissible ticket burns become eligible after the required maturity and examination. The producer is the role of the identity drawn for a particular slot. Active weight is the number of active tickets, not a count of organizations. [N-SPEC v0.7 §4.1][n41], [§4.2][n42], [§4.7][n47], [§5.3][n53], [§7.1][n71]

A ticket is an entry right, never a guarantee. The burn makes additional identities costly, but does not establish that their owners act independently. A ticket is neither refundable nor transferable. It does not expire merely because it has gone unused; exclusion suspends its active right, while a ban destroys that right. [WHY-N §2][w2]; [N-SPEC v0.7 §1.4, invariants 3–5][n14]

## Participation and reactivation

An identity drawn for a slot must produce. Inactivity is subject to exclusion under the activity rules, density brake and exclusion limits. REACT restores suspended rights after the applicable checks. Adding a ticket does not reactivate an excluded identity or erase its activity record. [N-SPEC v0.7 §6.6][n66], [§6.7][n67], [§4.6][n46]

ROTATE changes production keys under the prescribed authorization rules. It neither reactivates an excluded identity nor removes responsibility for an earlier key generation. Signing reservations and protection against restoring older state prevent a restart or rollback from being treated as permission to sign again. [N-SPEC v0.7 §6.9][n69], [§7.4][n74], [§7.6][n76]

## Equivocation and a permanent ban

Equivocation means signing different headers for the same identity, chain and slot, with each signing key checked in its historical context. The proof must meet the admissibility and maturity rules; receiving an allegation alone does not ban an identity. [N-SPEC v0.7 §10.1][n101], [§10.2][n102], [§10.3][n103]

Proven equivocation bans the identity permanently. There is no slashing: the ticket was spent at entry, not seized. The ban removes participation rights without removing past score. [N-SPEC v0.7 §1.4, invariants 3–4 and 9][n14], [§10.3][n103]

## The role has limits

Production creates no M0 reward. A producer cannot make an invalid operation valid or promote a branch through a signature alone. Fees transfer existing resources, and chain selection follows the published ranking rules. [N-SPEC v0.7 §1.4, invariant 12][n14], [§9.3][n93], [§9.5][n95]

## See also

[The N engine](engine.md), [Burns](burns.md), [Who does what](roles.md), and [Depth and statuses](depth.md).

[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n41]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#41-identité
[n47]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#47-premier-examen
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n66]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#66-exclusions--frein-de-densité-et-plafonds
[n67]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#67-exclusion-et-react
[n69]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#69-rotate
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n74]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#74-réservation-anti-double-signature
[n76]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#76-stockage-anti-rollback-et-restauration
[n101]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#101-preuve-déquivoque
[n103]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#103-ban
[w2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#2-why-n-exists
[n42]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#42-keyreg
[n46]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#46-new-et-add
[n102]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#102-admissibilité-après-rotation
[n93]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#93-score-et-rang
[n95]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#95-sélection-avec-veto-séparé
