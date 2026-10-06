# BTC/M0 settlement in one hop

> **Normative source:** [APP-SPEC v1 draft §13.1][p131], [§13.2][p132], [§13.3][p133], [§13.4][p134], [§13.5][p135], [§13.6][p136], [§PUB, PUB-2 and PUB-6][pPUB].
> This page explains; it does not restate rules or parameter values.

The Bitcoin payment is the condition observed; M0 is what the BATHRON lock settles. For example, Alice reserves M0 for Bob, released only if the agreed Bitcoin payment is observed under the lock's rules. Otherwise, once the refund conditions are met, resolution sends the reserved M0 to the refund destination. [APP-SPEC v1 draft §13.1][p131], [§13.4][p134]

## Create the agreement

Creating a lock consumes an authorised, unspent transparent M0 output once. The reserved amount leaves the spendable-output set and enters the lock. Its terms identify the beneficiary, refund destination, Bitcoin payment script, required amount and payment window. Changing those terms changes the lock's identity and requires the corresponding authorisation. [APP-SPEC v1 draft §13.2][p132]

An admissible Bitcoin payment carries the lock's marker, pays the exact required script with a sufficient amount and is included within the payment window. The rules select the first admissible payment in Bitcoin order, using verified scan coverage to establish that it is first. Missing coverage means missing data. [APP-SPEC v1 draft §13.3][p133]

## Resolve or refund

Once that payment reaches the required depth in the block's Bitcoin reference, the reserved M0 moves to the beneficiary. Resolution requires no additional native transaction from the beneficiary. A Bitcoin payment never resolves two §13 locks. BTCSTATE, by contrast, remains a reusable presence test, without this payment-use restriction. [APP-SPEC v1 draft §13.1][p131], [§13.3][p133], [§13.4][p134], [§PUB, PUB-6][pPUB]

Refund becomes possible at the specified Bitcoin-height threshold after the payment window, with a complete verified scan establishing that no admissible payment exists. Elapsed time alone is insufficient. Without the scan, resolution waits for data instead of refunding by default. [APP-SPEC v1 draft §13.4][p134]

## Time and responsibility

PUB-2 publishes a time scale of roughly two to four hours for the default delivery depth, and warns of possible waits lasting several hours. This is an order of magnitude, not a completion deadline for an agreement. It accompanies risks including STOP and a revealed secret followed by reorganisation of its claim. [APP-SPEC v1 draft §PUB, PUB-2][pPUB]

The payer waits for lock inclusion and the chosen client policy before paying, then rechecks the conditions after waiting. A late Bitcoin payment can transfer BTC without entitlement to the reserved M0. Resolution remains reorganisable; a Bitcoin payment does not recreate a lock removed from the BATHRON history. [APP-SPEC v1 draft §13.5][p135], [§13.6][p136]

Covenants constrain the BATHRON side of an agreement. They never command a Bitcoin spend: a payer still submits the Bitcoin payment, and BATHRON reads the resulting evidence. Contract composition cannot remove that boundary. [APP-SPEC v1 draft §SCR.5][pSCR5], [§13.3][p133]; [N-SPEC v0.7, preamble, point 3][np]

## See also

[Contracts on Bitcoin facts](bitcoin-facts.md), [Covenants and timelocks](covenants.md), and [Depth and statuses](depth.md).

[p131]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#131-contrat
[p132]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#132-création-objet-0004
[p133]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#133-paiement
[p134]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#134-résolution
[p135]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#135-discipline-du-payeur-politique-client
[p136]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#136-rollback
[pPUB]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#pub-publications-obligatoires
[pSCR5]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr5-ctv
[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
