# Security model

This page separates three kinds of statement:

- **Fact:** enforced by the software and consensus rules today.
- **Design goal:** intended behaviour that is not yet fully implemented or reviewed.
- **Market hypothesis:** an economic or institutional claim that still needs evidence.

## Security in two minutes

1. **Consensus enforces the monetary invariants.** Professionals provide quotes,
   execution, liquidity and client service outside consensus. *(fact + design)*
2. **Operator collateral and public history may create commercial deterrence, but
   they do not replace the BFT assumption.** They prove neither legal identity nor
   future honesty. *(fact + hypothesis)*
3. **A malicious finality threshold cannot create M0 without a verified Bitcoin
   destruction.** It can, however, censor operations, stall finality or create
   divergent finalized views. *(fact)*
4. **Open-set Sybil resistance is not demonstrated.** The current public-testnet
   operator set is controlled by project infrastructure. *(fact + hypothesis)*

## What consensus enforces

Every node validates every block. Finality is added on top of validation; it does
not bypass it.

- **A5:** M0 can be created only from Bitcoin destruction verified through SPV.
- **A6:** M0 vaulted for M1 equals the M1 supply; the protocol conversion is 1:1.
- **A7/A9:** the tracked Bitcoin chain is constrained by checkpoints and canonical
  chain rules.
- **No block subsidy, premine or treasury issuance:** coinbase recycles fees.

A finality threshold cannot sign an invalid issuance into existence. Honest nodes
reject a block that creates M0 without a valid proof, breaks M0↔M1 accounting or
contains another invalid state transition.

This does **not** make ordering and liveness unconditional. A threshold coalition
can omit an operation from blocks it produces, refuse to finalize blocks that
include it, stall finality, or equivocate across a partition.

## The BFT assumption

The finality threshold is:

```text
ceil(2/3 × min(E, N))
```

where `N` is the number of eligible, distinct operators and `E` is the committee
cap. One operator identity has one vote.

Safety and liveness rely on the applicable committee remaining below the Byzantine
threshold. Operator history and collateral are commercial signals; they do not
change that mathematical assumption.

The current testnet set is **project-controlled**. This does not demonstrate
Byzantine resistance under open admission. It also does not remove software bugs,
operator-key compromise, shared-hosting failures or other correlated failures.

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

The residual finality failure is therefore a **split with divergent views**, followed
by an out-of-band social recovery. It is not an automatic rollback silently accepted
by nodes that already finalized the conflicting height.

## Destruction, M0 and operator collateral

The causal chain is:

```text
Bitcoin destruction  → M0 creation
M0 acquisition       → collateral lock
collateral lock      → operator registration
```

- The destroyed Bitcoin is not held, reserved or redeemable.
- The M0 collateral is locked, not destroyed. Under the current rules it is
  recoverable by spending the collateral output and leaving the operator set.
- An operator need not have destroyed the Bitcoin itself; it may acquire M0 from a
  third party.
- The external acquisition cost therefore depends on future M0 liquidity. It is
  not a fixed protocol price.

The current floor is a launch parameter expressed as 0.01 BTC-equivalent. It is not
a demonstrated Sybil price.

The finality threshold counts **distinct eligible identities**, not an aggregate
amount of collateral. An attacker would need enough M0 to register enough separate
identities to reach the applicable threshold.

There is no slashing. A proof-of-service ban removes an identity from the active
set but does not confiscate its M0. Any loss of future fees or service revenue is
only a possible commercial opportunity cost; those revenues are not proven.

## Reputation and provider roles

An operator's registration age and production history are observable facts, but
they do not prove legal identity or future honesty. Provider volume, latency and
incident metrics require an independent indexing methodology and can be manipulated
through wash activity or selective disclosure.

The three roles remain distinct:

- **Settlement Operator:** consensus and finality.
- **Clearing Provider:** client quote, orchestration, deadlines and service.
- **Liquidity Provider:** inventory and pricing.

Choosing or pinning a provider establishes a service route or endpoint. It does not
create a private consensus committee and does not replace the global finality set.
The protocol does not currently prove that an operator and a Clearing or Liquidity
Provider are the same legal or economic entity.

See [Clearing and Liquidity Providers](settlement-providers.md).

## What remains unproven

- Sybil resistance under open operator admission.
- A value-at-risk bound per finality window.
- An external audit of the VRF finality path.
- A protocol-enforced or independently verified operator↔provider identity link.
- A productised and externally reviewed cross-chain conditional-settlement flow.
- Sustained client demand, provider revenue and competitive liquidity.

## Node-local destruction policy

The `-btcburnsenabled` option is a node-local origination and relay policy, not a
global administrator switch. A node with the option disabled still accepts a valid
block containing a destruction claim produced elsewhere. Pausing new claims across
the network would therefore require coordinated producer behaviour.

## Comparison with Bitcoin

Bitcoin and BATHRON close different attack surfaces with different assumptions.
Both require full nodes to reject invalid blocks. Bitcoin orders history through
proof of work and probabilistic depth; BATHRON uses a registered operator set and
BFT finality. BATHRON's residual finality failure is split and social recovery,
while its open-set economic resistance remains unproven.

For implementation details, continue with [Consensus](consensus.md),
[Bitcoin integration](bitcoin-integration.md) and
[Accounting invariants](../reference/invariants.md).
