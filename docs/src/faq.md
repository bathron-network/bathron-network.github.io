# FAQ

## What problem is BATHRON trying to solve?

Conditional Bitcoin settlement: coordinating a Bitcoin payment with another payment, delivery,
deadline or verifiable event without giving one intermediary unrestricted custody of the funds.

## Is BATHRON a coin offered to users?

No. There is no token sale, premine, treasury, block reward or promised yield. The target client
sends and receives familiar external assets. M0 and M1 are internal accounting states used by
professional providers, and their market value is neither guaranteed nor promoted.

## Who provides the service?

A **Clearing Provider (CP)** gives the client a quote and orchestrates the settlement paths. One
or more **Liquidity Providers (LPs)** supply inventory and pair-specific prices. **Settlement
Operators** run consensus and finality; they do not set commercial prices.

## Why is an internal settlement asset necessary?

BATHRON can verify Bitcoin facts but cannot command Bitcoin to spend. Its contracts therefore
need internal state they can lock and release when a condition is satisfied. M1 carries that
programmable state; M0 accounts for its origin.

## Why destroy Bitcoin?

Verified destruction is the only route by which M0 can be created. It avoids a custodian holding
a redemption reserve, but it is irreversible: the BTC is gone. This is a professional inventory
cost, not a guarantee that M0 or M1 can later be sold for BTC.

## Is M1 pegged to Bitcoin?

No. Consensus enforces only the internal M0↔M1 accounting equality. It does not guarantee an
external price, redemption or liquidity. A provider's realizable value can be heavily discounted
and can fall to zero.

## Is settlement atomic and risk-free today?

No general guarantee is claimed. Individual HTLC and covenant components have run on the
testnet, but the complete state machine, reorganisation handling and timelock ordering still need
formal specification and external review.

## Why confidentiality?

Commercial settlement can expose counterparties, sizes and treasury flows. Sapling can hide
amounts and linkage in the internal leg while consensus still checks conservation. Confidentiality
is a service property, not a retail “private cash” proposition.

## Is this CLS for crypto?

No. Payment-versus-payment is a useful functional analogy, but BATHRON has no central-bank
accounts, regulated settlement membership, equivalent legal finality or systemic track record.

## What exists today?

An experimental testnet with covenant execution, Bitcoin proofs checked in consensus,
confidential internal transfers, paired HTLC demonstrations and fast finality. There is no
mainnet, external safety certification, sustained multi-provider liquidity or proven demand.
