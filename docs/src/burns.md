# 06 · Burns: M0, tickets, reactivation

> **Normative source:** [N-SPEC v0.7, preamble][np], [§1.4][n14], [§4.4][n44], [§4.6][n46], [§4.9][n49], [§6.7][n67], [§12.1][n121], [§12.2][n122]; [WHY-N §3][w3]; [APP-SPEC v1 draft §0.4][p04].
> This page explains; it does not restate rules or parameter values.

Burns have different purposes. Creating settlement inventory, obtaining production weight and restoring suspended rights are distinct effects. Distinguishing them avoids treating a ticket as spendable M0 or a burn as a deposit that can be withdrawn. [N-SPEC v0.7 §1.4, invariants 1–4][n14], [§4.6][n46], [§4.9][n49], [§6.7][n67]

## Different burns, different effects

| Burn | Effect |
|---|---|
| M0 burn | Creates M0, the settlement asset. [N-SPEC v0.7 §4.9][n49]; [APP-SPEC v1 draft §0.4][p04] |
| TICKET, with NEW or ADD | Adds ticket rights to a registered identity, subject to admission and activity rules. It creates no M0. [N-SPEC v0.7 §4.6][n46], [§1.4, invariant 1][n14] |
| REACT | Restores suspended participation rights under the reactivation rules. It creates no M0. [N-SPEC v0.7 §6.7][n67], [§1.4, invariant 1][n14] |

NEW and ADD express different intentions but grant the same kind of ticket right. An ADD does not itself reactivate an excluded identity. A REACT concerns the identity's exclusion record; it is not another source of settlement inventory. [N-SPEC v0.7 §4.6][n46], [§6.7][n67]

## M0 has a Bitcoin origin

Every M0 unit comes from burned bitcoin. A burn creates no reserve and no claim on Bitcoin. The destroyed bitcoin cannot be recovered by returning M0. The provenance describes where M0 comes from; it does not create a promise to return BTC. [N-SPEC v0.7 §4.9][n49]; [WHY-N §3][w3]

The supply of M0 is the sum of M0 burns. There is no premine, issuer or block reward. Fees transfer existing M0 rather than create it. Conservation remains an application obligation within each history; N's choice of history does not establish it by itself. [N-SPEC v0.7, preamble][np], [§1.4, invariants 2 and 12][n14]; [WHY-N §3][w3]

## A ticket remains an entry cost

Ticket rights are neither refundable nor transferable. They remain acquired until a ban, while exclusion suspends their active use. Inactivity does not turn a ticket into M0, and reactivation does not recover the bitcoin spent at entry. [N-SPEC v0.7 §1.4, invariants 1–4][n14], [§6.7][n67]

## Fingerprints are a separate use

Admissible burns can also carry fingerprints for H1. A fingerprint may contribute to a wait or STOP; it cannot promote a branch or add score. This detector role is distinct from creating M0 or obtaining participation rights. [N-SPEC v0.7 §12.1][n121], [§12.2][n122]

An M0 burn's optional reference does not control M0 creation. An absent, unknown or losing reference does not block creation from an otherwise admissible M0 burn. Its use as a fingerprint has separate conditions. [N-SPEC v0.7 §4.9][n49]

## See also

[Producers and tickets](producers.md), [The N engine](engine.md), [Where trust lives](trust.md), and [Glossary](glossary.md).

[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n44]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#44-sortie-ticket
[n46]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#46-new-et-add
[n49]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#49-burn-m0-v3
[n67]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#67-exclusion-et-react
[n121]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#121-nature-de-h1
[n122]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#122-empreintes-admissibles
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[p04]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés
