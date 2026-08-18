# Security model

A settlement layer is only worth building on if its guarantees are stated precisely — including
their limits. This page separates three kinds of statement:

- **Fact:** enforced by the software and consensus rules today.
- **Design goal:** intended behaviour that is not yet fully implemented or reviewed.
- **Market hypothesis:** an economic or institutional claim that still needs evidence.

## Security in two minutes

1. **Consensus enforces the monetary invariants.** Professionals provide quotes, execution,
   liquidity and client service outside consensus. *(fact + design)*
2. **Operator collateral and public history may create commercial deterrence, but they do not
   replace the BFT assumption.** They prove neither legal identity nor future honesty.
   *(fact + hypothesis)*
3. **A malicious finality threshold cannot create M0 without a verified Bitcoin destruction.**
   It can, however, censor operations, stall finality or create divergent finalized views.
   *(fact)*
4. **Open-set Sybil resistance is not demonstrated.** *(fact + hypothesis)*

## What consensus enforces

Every node validates every block. Finality is added on top of validation; it does not bypass it.

- **A5:** M0 can be created only from Bitcoin destruction verified through SPV.
- **A6:** M0 vaulted for M1 equals the M1 supply; the protocol conversion is 1:1.
- **A9:** the tracked Bitcoin chain must be the real Bitcoin chain — canonical checkpoints and
  a reorg floor below pinned anchors and matured burns.
- **No block subsidy, premine or treasury issuance:** coinbase recycles fees.

A finality threshold cannot sign an invalid issuance into existence. Honest nodes reject a block
that creates M0 without a valid proof, breaks M0↔M1 accounting or contains another invalid
state transition.

This does **not** make ordering and liveness unconditional. A threshold coalition can omit an
operation from blocks it produces, refuse to finalize blocks that include it, stall finality, or
equivocate across a partition.

## The BFT assumption

The finality threshold is:

```text
ceil(2/3 × min(E, N))
```

where `N` is the number of eligible, distinct Operators and `E` is the committee cap. One
Operator identity has one vote.

Safety and liveness rely on the applicable committee remaining below the Byzantine threshold.
Operator history and collateral are commercial signals; they do not change that mathematical
assumption. The assumption also does not remove software bugs, Operator-key compromise,
shared-hosting failures or other correlated failures. Who runs the Operator set today, and what
that does and does not demonstrate, is stated on [Status & claims](status-and-claims.md).

## What a threshold coalition can and cannot do

| Action | Possible? |
|---|---|
| Create M0 without a valid destruction proof | **No** — rejected by full validation |
| Change M0↔M1 accounting | **No** — rejected by consensus |
| Spend a client's key | **No** — the coalition does not possess it |
| Force a Bitcoin transaction | **No** — BATHRON observes Bitcoin; it cannot command it |
| Censor a specific operation | **Yes** — by omission or by withholding finality |
| Push a conditional leg toward its timeout | **Potentially** — censorship plus time can activate a refund path |
| Stall finality | **Yes** |
| Produce conflicting certificates | **Yes, with sufficient equivocation across a partition** |
| Silently replace a height already finalized by a node | **No** — that node rejects conflicting finality |

The residual finality failure is therefore a **split with divergent views**, followed by an
out-of-band social recovery. It is not an automatic rollback silently accepted by nodes that
already finalized the conflicting height.

## Destruction, M0 and Operator collateral

The causal chain is:

```text
Bitcoin destruction  → M0 creation
M0 acquisition       → collateral lock
collateral lock      → operator registration
```

- The destroyed Bitcoin is not held, reserved or redeemable.
- The M0 collateral is locked, not destroyed. Under the current rules it is recoverable by
  spending the collateral output and leaving the Operator set.
- An Operator need not have destroyed the Bitcoin itself; it may acquire M0 from a third party.
- The external acquisition cost therefore depends on future M0 liquidity. It is not a fixed
  protocol price.

The current floor is a launch parameter expressed as 0.01 BTC-equivalent. It is not a
demonstrated Sybil price.

The finality threshold counts **distinct eligible identities**, not an aggregate amount of
collateral. An attacker needs enough M0 to register enough separate identities: about a third
of the committee to stall finality or — combined with a network split — to sign conflicting
certificates (two `⌈2/3·n⌉` quorums always share at least `2q − n` signers), and the full
threshold to control ordering outright. See [Open-network hardening](open-network-hardening.md).

## Design choices

- **ECDSA on secp256k1 only.** No BLS, no aggregated signatures — explicit signatures are
  simpler to audit at these committee sizes, and one round of gossip already reaches finality
  in about a minute regardless of committee size.
- **No slashing.** Deterrence is the up-front cost of acquiring and locking M0 collateral,
  plus a proof-of-service ban that removes an identity from the active set without confiscating
  its M0. Any loss of future fees or service revenue is only a possible commercial opportunity
  cost; those revenues are not proven. The reasoning is restated on
  [Open-network hardening](open-network-hardening.md#no-slashing--a-deliberate-choice-restated).
- **Finality above validation, never instead of it.** This is what makes the table above hold:
  the signers decide ordering; the money is checked by every node.

## Reputation and provider roles

An Operator's registration age and production history are observable facts, but they do not
prove legal identity or future honesty. Provider volume, latency and incident metrics require an
independent indexing methodology and can be manipulated through wash activity or selective
disclosure.

Settlement Operators, Clearing Providers and Liquidity Providers are distinct roles; see
[Roles: Operators, Settlement Providers, users](../markets/roles.md). Choosing or pinning a
provider establishes a service route or endpoint. It does not create a private consensus
committee and does not replace the global finality set. The protocol does not currently prove
that an Operator and a Clearing or Liquidity Provider are the same legal or economic entity.

## Comparison with Bitcoin

Bitcoin and BATHRON close different attack surfaces with different assumptions. Both require
full nodes to reject invalid blocks. Bitcoin orders history through proof of work and
probabilistic depth; BATHRON uses a registered Operator set and BFT finality. BATHRON's residual
finality failure is split and social recovery, while its open-set economic resistance remains
unproven.

For implementation details, continue with [Production and finality](production-and-finality.md),
[Bitcoin facts inside consensus](../bitcoin/facts-in-consensus.md) and
[Accounting invariants](../reference/invariants.md).

## Reporting a vulnerability

Report suspected security issues privately to **security@bathron.org**. Please do not open a
public issue for an unpatched vulnerability. Include enough detail to reproduce; the inbox is
monitored and coordinated disclosure is preferred. The full policy ships as `SECURITY.md` in the
[bathron-core repository](https://github.com/bathron-network/bathron-core/blob/main/SECURITY.md).

## Notes

**Node-local destruction policy.** The `-btcburnsenabled` option is a node-local origination
and relay policy, not a global administrator switch. A node with the option disabled still
accepts a valid block containing a destruction claim produced elsewhere. Pausing new claims
across the network would therefore require coordinated producer behaviour.
