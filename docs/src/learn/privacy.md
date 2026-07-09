# Privacy

BATHRON has **private cash at the base layer**: shielded transfers using the Sapling protocol (zero-knowledge proofs), not a mixer bolted on top.

## What is private

- **Amounts and balances** of shielded funds.
- **Linkage**: a shield → unshield hop breaks the on-chain connection between sender and recipient. In the flagship swap, the intermediate value crosses this private hop — so the two Bitcoin transactions at the edges cannot be linked through the middle.

## What is public

- The **total supply** and the monetary invariants — privacy never hides whether the money is sound. Consensus verifies that shielded operations conserve value; it just doesn't see who holds what.
- Settlement transactions (locks, burns, header proofs) are transparent by design: they are the auditable skeleton of the system.

## What we do not claim

BATHRON does not compete with Monero on anonymity-set size, and privacy is not the product — **non-custodial settlement is**. Privacy is what makes settlement commercially usable: no business wants its counterparties, volumes and treasury readable by competitors.

## For builders

Shielded funds are ordinary funds: receive to a shielded address, send with a shielded transaction ([wallet](../build/wallet.md)). Applications can route value through the shielded pool wherever confidentiality matters, and settle transparently where auditability matters.
