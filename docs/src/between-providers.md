# Settlement between providers on M0

> **Normative source:** [APP-SPEC v1 draft §R2P][pR2P], [§OBJ.3, OBJ-10][pOBJ], [§SCR.1][pSCR1], [§SCR.2][pSCR2], [§SCR.3][pSCR3], [§SCR.5][pSCR5].
> This page explains; it does not restate rules or parameter values.

Independent liquidity providers can settle with each other on M0 without mutual trust in the settlement mechanism. BATHRON does not need to know the other chains for this M0 leg. Providers still choose monitoring, margins and delivery depth under the availability and reorganisation assumptions of their contracts. [APP-SPEC v1 draft §R2P, R2P-1 and R2P-3][pR2P]

## One settlement inventory

M0 is the common settlement asset for the interchain leg. In a provider construction, one M0 inventory can connect a provider to all the pairs it serves, instead of requiring a different BATHRON settlement asset for each pair. This is a consequence of the common-asset model, not a promise that counterparties or liquidity exist for every pair. [APP-SPEC v1 draft §R2P, R2P-1][pR2P]

## Generic scripts, including three secrets

Preimage claims, refunds after a delay, three-secret hash time locked contracts (HTLC3S) and a covenant-linked parent contract are generic scripts on M0. They have no dedicated consensus transaction rule. Hashlocks supply the preimage condition; timelocks constrain spending paths; CTV constrains the transaction that spends the output. The constructor supplies the arrangement of secrets, participants and transactions. [APP-SPEC v1 draft §OBJ.3, OBJ-10][pOBJ], [§SCR.1][pSCR1], [§SCR.5][pSCR5]

The R2P construction uses a parent covenant to constrain a child contract. The child's refund path combines an absolute deadline in N slots with a relative delay in N links. The parent's claim template commits to the child's full output script, including every required refund branch, so a claimant cannot omit that delay. [APP-SPEC v1 draft §R2P, R2P-2][pR2P]

The relative delay begins with the child's inclusion on the examined branch. An absolute deadline alone would not establish this interval after creation. The template's delays and deadlines belong to the construction and its margin analysis; R2P does not choose their values. [APP-SPEC v1 draft §SCR.3, CSV-1][pSCR3], [§R2P, R2P-2 and R2P-5][pR2P]

## What the interval does not provide

On the examined branch, the relative delay keeps the child's refund path closed for the required links after inclusion. It does not establish an equal interval after the beneficiary discovers the child. A branch revealed late can already contain both the child and its refund. The provider's published policy must address monitoring, margins and required depth. [APP-SPEC v1 draft §R2P, R2P-3][pR2P]

There is also no script upper bound on claim height: a late claim is no longer rejected by a separate HTLC consensus rule. Constructors must reason about the available claim and refund paths instead of assuming expiry removes the claim path. These generic scripts do not replace the distinct Bitcoin-payment lock of §13. [APP-SPEC v1 draft §R2P, R2P-1][pR2P], [§OBJ.3, OBJ-10][pOBJ], [§13.1][p131]

## See also

[What others can build](what-you-can-build.md), [Covenants and timelocks](covenants.md), and [Who does what](roles.md).

[pR2P]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants
[pOBJ]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#obj3-anciens-types-refusés-et-numéros-réservés
[pSCR1]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr1-socle-actif-au-genesis
[pSCR2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr2-échéances-absolues-en-créneaux-n-cltv
[pSCR3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr3-délais-relatifs-en-liens-n-csv
[pSCR5]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr5-ctv
[p131]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#131-contrat
