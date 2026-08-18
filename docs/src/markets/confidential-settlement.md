# Confidential settlement

A market cannot work if every participant publishes its counterparties, sizes and inventory to
its competitors. Providers would be front-run on every quote and clients would move the market
against themselves with every large trade. Confidentiality is therefore not a product on
BATHRON; it is a property the settlement state needs so that markets can be built on it at all.

BATHRON uses Sapling proofs for confidential transfers of M1.

## What can be hidden

- amounts and balances in the shielded pool;
- linkage across a shielded transfer — who paid whom, and how much.

## What remains verifiable

- consensus verifies conservation without learning the hidden amounts;
- burns, locks and Bitcoin-header proofs remain transparent where auditability requires it;
- the M0 and M1 accounting invariants remain public (see
  [Accounting invariants](../reference/invariants.md)).

## What it does not cover

Shielding hides the M1 side of a settlement, not the whole workflow. Bitcoin edge transactions,
timing, network metadata and application behaviour may still reveal information; BATHRON does
not claim Monero's anonymity set or a complete privacy guarantee.

In practice, Clearing and Liquidity Providers use the confidential state as back-office
infrastructure — inventory moves and OTC sizes stay private — while end users settle in the
assets they already hold and are never asked to manage "private cash".

**Primitives:** shielded transfers (Sapling) · `shieldsendmany`

**See also:** [Delivery-versus-payment and OTC](patterns/dvp-otc.md) ·
[Run a wallet](../operate/run-a-wallet.md)
