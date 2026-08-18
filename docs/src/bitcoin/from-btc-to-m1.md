# From destroyed BTC to M1

A settlement protocol needs a unit that its own consensus can lock, release and account for.
Bitcoin cannot be that unit — BATHRON cannot command Bitcoin to spend — so an internal one is
required. The question this page answers is where that unit comes from, who brings it into
existence and why the answer is deliberately narrow: only from Bitcoin that has been provably
destroyed.

## Why an internal unit is required at all

Covenants, timelocks and hashlocks need an asset the BATHRON consensus can lock and release.
M1 carries that programmable settlement state. M0 records where the inventory came from: a
one-way origin in verified BTC destruction.

```text
BTC --irreversible, SPV-proven destruction--> M0 --lock 1:1--> M1
```

Two consensus rules pin this down. In plain words:

- **A5 — provenance.** One destroyed satoshi permits one M0 unit; nothing else does. There is
  no block subsidy, no premine, no treasury and no issuer. Even the very first unit at genesis
  came from a verified destruction, exactly like every later one.
- **A6 — accounting equality.** The M0 vaulted for M1 equals the M1 in circulation. Lock and
  unlock are 1:1 protocol operations, so unvaulted M1 cannot exist.

Both rules are checked by every full node on every block; a finality quorum cannot sign its way
around them. The formal statement is in [Accounting invariants](../reference/invariants.md).

## What a destruction looks like

Bitcoin is sent to a provably unspendable output — a script that can never be satisfied — with a
small `OP_RETURN` naming the BATHRON destination that will receive the M0. Any node can then
verify, against the Bitcoin header chain it maintains in consensus, that the transaction was
included under sufficient work; after a maturity delay the M0 becomes claimable. The exact
format, the unspendable script and the maturity constants are in the
[SPV reference](../reference/spv.md#burn-format-bcs-v10).

The BTC is not held for redemption. It is destroyed. That is what makes M0 an inventory unit
rather than a deposit receipt.

## Who does this

Nobody has to touch M0 to use BATHRON:

> End users settle in the assets they already hold; market builders and providers settle in M1.

The destruction route is a professional inventory-acquisition path — for Liquidity Providers
who want inventory to quote a pair, for market builders who need a settlement float, and for
anyone who wants to register as an Operator (registration requires locking M0 as collateral):

```text
Bitcoin destruction  → M0 creation
M0 acquisition       → inventory, or collateral lock
collateral lock      → operator registration
```

Two properties matter for whoever takes this route:

- **It is an irreversible cost.** The BTC is gone; the M0 is inventory. That cost is recovered,
  if at all, through the service built on it — spreads on a pair, clearing fees, settlement —
  not through any protocol payment, subsidy or expected appreciation of the unit.
- **Destroying Bitcoin yourself is not required.** M0 already in existence can be acquired from
  a third party. The rule is only that *every* M0 unit, whoever holds it now, traces back to a
  verified destruction. An Operator's collateral is locked, not destroyed, and is recoverable by
  leaving the operator set.

## What this buys

Because the origin rule is a single, verifiable, one-way path, three questions that plague
other designs simply do not arise: there is no reserve to audit or lose, no issuer to trust or
pressure, and no rule to vote on — one satoshi, one M0 unit, and there is no mechanism to change
that. What M1 is worth in Bitcoin on a given day is then a market question, answered by
[providers quoting the native pair](../markets/native-btc-pair.md), never by the protocol.

**See also:** [Bitcoin is the final asset](final-asset.md) · [Bitcoin facts inside consensus](facts-in-consensus.md) · [The settlement unit: M1](../provides/settlement-unit-m1.md)
