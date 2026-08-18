# Glossary

Two lines per term, in the order a new reader meets them.

**Settlement** — the moment both legs of a trade move, or neither does. The only thing BATHRON's
consensus performs. → [Settlement guarantees](../provides/settlement-guarantees.md)

**Market / pair** — `X/M1`: exists when someone brings inventory and publishes quotes; nobody
approves it and nobody can revoke it. → [How a market appears](../markets/how-a-market-appears.md)

**M1** — the settlement unit (numéraire) of the network; M0 vaulted 1:1. Held by market builders
and providers as working capital; not a coin sold to end users. → [The settlement unit](../provides/settlement-unit-m1.md)

**M0** — the base accounting unit, created only when bitcoin has been provably destroyed and the
proof verified in consensus (invariant A5). → [From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)

**Burn / destruction** — sending bitcoin to a provably unspendable output on Bitcoin. One-way; the
BTC is not held for redemption. → [Bitcoin is the final asset](../bitcoin/final-asset.md)

**Numéraire** — a common unit every pair settles through, so N assets need N pairs instead of N².

**Operator (Settlement Operator)** — a consensus identity collateralised with M0: produces blocks,
signs finality, publishes facts about itself. One operator, one vote. Called *masternode* in the
RPC and source. → [Roles](../markets/roles.md)

**Settlement Provider (SP)** — umbrella term for the commercial participants: Clearing Providers
and Liquidity Providers. Participants, never administrators.

**Clearing Provider (CP)** — quotes a client, orchestrates the legs, enforces deadlines, offers an
SLA; paid by explicit fees.

**Liquidity Provider (LP)** — holds inventory in a pair and prices it; paid by the spread; bears
capital and market risk.

**Quote** — a signed off-chain message: pair, bid, ask, size, expiry. Never seen by consensus.
→ [Quotes live off-chain](../markets/quotes-off-chain.md)

**Covenant** — a script constraining how value may move (a forced destination, a timeout, a
condition). Not a smart contract in the EVM sense. → [The infrastructure](../provides/infrastructure.md)

**HTLC** — hashed timelocked contract: pays on a revealed secret, refunds after a deadline. Two
of them, one per chain, keyed to the same secret, form an atomic pair. → [Native BTC ⇄ M1](../markets/native-btc-pair.md)

**Bitcoin facts / SPV** — Bitcoin block headers carried and verified inside BATHRON's consensus;
a Merkle proof then proves a Bitcoin transaction is confirmed, for every node, without an oracle.
→ [Bitcoin facts inside consensus](../bitcoin/facts-in-consensus.md)

**`TX_CONFIRMED`** — the script check "this Bitcoin payment is confirmed under enough work"; the
engine under DvP and escrow.

**`CTV`, `CSFS`, `CSV`/`CLTV`, `OP_CAT`, introspection** — the covenant opcodes: forced template,
oracle signature, timelocks, concatenation, reading the spending transaction. → [Script & opcodes](opcodes.md)

**Finality** — a block is irreversible after one round of operator signatures (~1 minute), by an
ECVRF-drawn committee with threshold ⌈2/3·min(E,N)⌉; finality overrides the longest chain.
→ [Production and finality](../consensus/production-and-finality.md)

**Invariants A5 / A6** — A5: M0 total equals BTC provably destroyed. A6: vaulted M0 equals M1
supply. Enforced by every node; a finality quorum cannot break them. → [Accounting invariants](invariants.md)

**Consensus freeze** — the rule that any addition to consensus must prove it enables something
impossible to build cleanly above; all future value is built above. → [Why the consensus is frozen](../consensus/why-frozen.md)

**Open admission** — the state in which anyone may register as an operator. Not yet reached: the
current operator set is project-run. → [Status & claims](../consensus/status-and-claims.md)
