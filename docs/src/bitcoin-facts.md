# Contracts on Bitcoin facts

> **Normative source:** [APP-SPEC v1 draft §BTC][pBTC], [§SCR.7][pSCR7], [§0.3, GEN-5][p03]; [N-SPEC v0.7 §8.4][n84].
> This page explains; it does not restate rules or parameter values.

A contract can depend on evidence from Bitcoin that BATHRON nodes check themselves. The important distinction is between proving that a fact exists and assigning a payment to a settlement lock. BTCSTATE supplies the presence test; payment uniqueness belongs to the settlement rules. [APP-SPEC v1 draft §SCR.7, BTCSTATE-2][pSCR7]

## A fact at a reference block

Every application rule in a BATHRON block reads the Bitcoin view designated by that block's reference, `B.ref`. It cannot read beyond that reference or substitute a more recent local view. The reference also obeys the engine's ancestry and time-context rules. [APP-SPEC v1 draft §BTC, BTC-1][pBTC]; [N-SPEC v0.7 §8.4][n84]

BTCSTATE is a generic, non-consuming presence predicate. In its active `TX_CONFIRMED` mode, it checks that a fact exists in the reference view. Several scripts may use the same Bitcoin fact: satisfying a script does not consume that evidence or reserve it for one agreement. Query definitions and formats beyond the adopted rules remain reserved under BTCSTATE-3. [APP-SPEC v1 draft §SCR.7, BTCSTATE-1–BTCSTATE-3][pSCR7]

## What each node checks

The evidence depends on the question. Presence uses the reference's Bitcoin headers, which also carry header facts such as difficulty, and, for transaction evidence, the transaction and its Merkle proof. Authenticating an input additionally requires verified previous-output and witness data. Establishing absence, completeness or the first event requires a verified exhaustive scan of the relevant interval. A presence proof cannot replace that scan. [APP-SPEC v1 draft §BTC, BTC-3][pBTC]

Nodes share the application's Bitcoin view with the engine. Verified coverage is tied to block hashes on a branch, rather than heights alone. A Bitcoin reorganisation therefore invalidates or changes the context of coverage and cached facts. A third-party data source supplies evidence, without becoming an authority; falsified, truncated or reordered Bitcoin blocks fail verification against the headers. [APP-SPEC v1 draft §BTC, BTC-1–BTC-4][pBTC]

## Missing evidence means waiting

An unavailable local provider or unreadable header database produces a local failure or missing-data result. It does not turn a query into a false predicate and make the transaction invalid. Missing coverage proves neither absence nor permission to proceed; it cannot trigger a default refund. [APP-SPEC v1 draft §SCR.7, BTCSTATE-4][pSCR7], [§0.3, GEN-5][p03]

For a builder, the distinction determines the contract mechanism: use a presence predicate when reuse of the fact is acceptable; use §13 when a Bitcoin payment must not resolve multiple settlement locks. That uniqueness applies between §13 locks, without extending to arbitrary scripts. [APP-SPEC v1 draft §SCR.7, BTCSTATE-2][pSCR7], [§13.3][p133]

## See also

[Covenants and timelocks](covenants.md), [BTC/M0 settlement in one hop](settlement.md), and [What others can build](what-you-can-build.md).

[pBTC]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#btc-faits-bitcoin-applicatifs
[pSCR7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr7-btcstate
[p03]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#03-catégories-et-verdicts
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[p133]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#133-paiement
