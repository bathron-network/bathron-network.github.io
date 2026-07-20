# Confidential settlement state

Privacy is not the product. It is a property needed when settlement participants should not
publish counterparties, amounts and inventory to competitors.

BATHRON uses Sapling proofs for confidential internal transfers.

## What can be hidden

- amounts and balances in the shielded pool;
- linkage across a shielded transfer.

## What remains verifiable

- consensus verifies conservation without learning the hidden amounts;
- burns, locks and Bitcoin-header proofs remain transparent where auditability requires it;
- the M0 and M1 accounting invariants remain public.

Shielding does not make the entire cross-chain workflow anonymous. Bitcoin edge transactions,
timing, network metadata and application behaviour may still reveal information. BATHRON does not
claim Monero's anonymity set or a complete privacy guarantee.

In the target service, CPs and LPs use the confidential state as back-office infrastructure. A
retail client is not asked to acquire or manage “private cash.”
