# What others can build

> **Normative source:** [APP-SPEC v1 draft §OBJ.3, OBJ-10][pOBJ], [§R2P][pR2P], [§BTC][pBTC], [§SCR.1][pSCR1], [§SCR.5][pSCR5], [§SCR.7][pSCR7], [§PUB][pPUB].
> This page explains; it does not restate rules or parameter values.

These are examples of third-party constructions, not services supplied by BATHRON. Each separates the protocol's documented primitives from the terms, software and dependencies a builder would supply. The examples illustrate composition; they add no protocol rule. [APP-SPEC v1 draft §OBJ.3, OBJ-10][pOBJ], [§SCR.1][pSCR1]

## Settlement between liquidity providers

**Protocol:** generic M0 scripts support preimage claims, refunds after a delay, HTLC3S with three secrets and a covenant-linked parent/child construction. **Builder:** arrange the secrets and counterparties, fund M0 inventory and publish monitoring, depth and margin policies. The child's relative refund delay applies from inclusion on the examined branch, not from discovery by its beneficiary. [APP-SPEC v1 draft §OBJ.3, OBJ-10][pOBJ], [§R2P, R2P-2–R2P-3][pR2P]

## Conditional payment or escrow

**Protocol:** hashlocks, multisig and timelocks provide script conditions for M0 spends. **Builder:** define release and refund paths, choose participants and write the dispute process. In an escrow construction, an arbitrator is a key in a multisig arrangement; the builder decides when that key is needed. This is a proposed use of multisig, without any protocol role for an arbitrator or verification of a real-world dispute. [APP-SPEC v1 draft §SCR.1][pSCR1], [§SCR.2][pSCR2], [§SCR.3][pSCR3]

## A difficulty market

**Protocol:** difficulty is a header fact in the presence class, verified by each node against the headers of the block's Bitcoin reference, and a covenant can constrain the M0 side of the contract. Difficulty markets are therefore compatible by design, without an oracle. The exact format of difficulty queries is not yet published: BTCSTATE-3 is reserved. **Builder:** define the contract, outcome, counterparties and funding, and use the query format once it is published. [APP-SPEC v1 draft §BTC, BTC-3][pBTC], [§SCR.5, CTV-1][pSCR5], [§SCR.7, BTCSTATE-3][pSCR7]

## Risk hedging

**Protocol:** M0 scripts provide conditional spending and time constraints. **Builder:** define the exposure, payoff, funding, counterparties and evidence for the condition. A difficulty-based hedge shares the unpublished query format noted above; other proposed hedges need conditions that the documented primitives support. This example does not imply that BATHRON prices, underwrites or covers a loss. [APP-SPEC v1 draft §SCR.1][pSCR1], [§SCR.7, BTCSTATE-3][pSCR7], [§OBJ.3, OBJ-10][pOBJ]

## BTCUSD/USDBTC instruments

**Protocol:** the available primitives constrain M0 settlement; BTC/USD price is not a Bitcoin fact. **Builder:** define the instrument's terms and supply an oracle external to the protocol, chosen by the builder and adding its own trust dependency. This requirement follows from the scope of Bitcoin facts; it is not a specified price service or a native DLC capability. [APP-SPEC v1 draft §BTC][pBTC], [§SCR.1, SCR-2][pSCR1]

For any of these constructions, deadlines do not ensure observation or inclusion before an external expiry. Builders must account for reorganisation, revealed secrets and possible waits lasting hours when explaining their service. [APP-SPEC v1 draft §SCR.4][pSCR4], [§PUB, PUB-2][pPUB]

## See also

[Settlement between providers on M0](between-providers.md), [Contracts on Bitcoin facts](bitcoin-facts.md), and [BTC/M0 settlement in one hop](settlement.md).

[pOBJ]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#obj3-anciens-types-refusés-et-numéros-réservés
[pR2P]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants
[pBTC]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#btc-faits-bitcoin-applicatifs
[pSCR1]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr1-socle-actif-au-genesis
[pSCR5]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr5-ctv
[pSCR7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr7-btcstate
[pPUB]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#pub-publications-obligatoires
[pSCR2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr2-échéances-absolues-en-créneaux-n-cltv
[pSCR3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr3-délais-relatifs-en-liens-n-csv
[pSCR4]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr4-limites-publiées-des-délais
