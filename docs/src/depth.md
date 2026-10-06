# 05 · Depth and statuses

> **Normative source:** [N-SPEC v0.7 §14.1][n141], [§14.2][n142], [§14.4][n144], [§14.5][n145], [§16.1][n161], [§17.1][n171], [§17.3][n173], [§17.6][n176], [§18][n18] (in French); [WHY-N §7][w7], [§8][w8].
> This page explains; it does not restate rules or parameter values.

An included operation and a decision to deliver value are different things. Inclusion records where the operation appears. Depth informs a participant's policy for acting on it. The party delivering value outside BATHRON carries the residual risk and chooses the required depth. [WHY-N §7][w7]

## Choose depth within a domain

There is no native finality. N offers inclusion and depth. Each participant chooses a depth from the published table, within the published domain. Outside it, N makes no quantitative claim. [N-SPEC v0.7 §1.4, invariant 18][n14], [§17.3][n173], [§17.6][n176]

The [published K(ε) table][n173] relates depth to a conditional risk bound for a particular cut in history. It is not a universal delivery policy. Read it together with the [domain assumptions][n172] and the [delivery policy][n142]. Copying a depth into an interface without its assumptions would remove the context in which the bound applies. [N-SPEC v0.7 §17.3][n173]

SPs and LPs can require a greater depth to target a smaller residual risk within that domain. The choice belongs to the party exposed by an external delivery, alongside its exposure policy. A provider's decision does not replace the protocol's rules. [WHY-N §7][w7]

## Read a status with its context

Use the application status identifiers defined in [N-SPEC v0.7 §14.5][n145]. They distinguish stages such as inclusion, depth assessment, reorganisation and waiting. After reinclusion, depth and stability assessment start from the new inclusion. A previously reached depth does not carry across to that new position. [N-SPEC v0.7 §14.5][n145]

The API separates **O**, an objective function of explicit data; **L**, a local observation; and **M**, a model result. These categories make the basis of a report visible. An interface should retain the relevant chain, origin and policy context instead of collapsing them into an unconditional assurance flag. [N-SPEC v0.7 §16.1][n161]

## Waiting and suspension

Wait or stop rather than be wrong. A settlement may wait hours; the network may pause to resolve a conflict. This describes the design within its assumptions, not a promise that every conflict will be detected. Delivery can be suspended without an attack, and chain progress alone does not establish that a delivery policy is satisfied. [WHY-N §7][w7], [§8][w8]; [N-SPEC v0.7 §14.2][n142], [§14.4][n144], [§18][n18]

## Outside the published domain

The table does not provide a quantitative claim outside H_N. Existing halt and recovery rules still apply, but leaving the domain need not trigger STOP. A long wait does not repair missing assumptions. The [published limits][n18] define what the model does not establish. [N-SPEC v0.7 §17.6][n176]

## See also

[Where trust lives](trust.md), [The N engine](engine.md), [Who does what](roles.md), and [Glossary](glossary.md).

[n141]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#141-densité
[n142]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#142-livraison
[n144]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#144-suspensions-sans-attaque
[n145]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#145-statuts-applicatifs
[n161]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#161-catégories
[n171]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#171-domaine-h_n--principe
[n173]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#173-table-kε-du-domaine
[n176]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#176-comportement-hors-domaine
[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[w8]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#8-what-n-guarantees-under-h_n-and-what-it-does-not
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[n172]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#172-hypothèses-du-domaine
