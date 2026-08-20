# The target open network

This page describes what BATHRON is **being built toward**. It is `TARGET NETWORK`: with the
exception explicitly marked below, none of it is deployed today.

[Status & claims](../consensus/status-and-claims.md) prevails over this page for anything about
the present.

## What the target network looks like

- A **public, open network**.
- **Several independent Consensus Operators**, none of whom chooses markets, providers or assets.
- **Open Consensus-Operator admission**, once the Sybil model and the economic conditions are
  validated.
- **Several independent Settlement Providers**, several Clearing Providers, several Liquidity
  Providers.
- **Several competing applications and interfaces.**
- **No listing committee. No protocol-imposed matching engine. No privileged provider.**
- Several providers may serve the **same** instrument or market.
- A provider may **disappear without removing** the protocol or the instrument.
- Users choose their application, their provider and their counterparty.

## What is true today

Application building is already open: anyone can build an application or propose a settlement flow
without a listing committee, and nothing in consensus registers or approves one.

**Consensus-Operator admission is not open.** The current operator set is run by the project while
the open-admission threat model is worked out. That is the single largest gap between today and the
target, and it is deliberate.

## The invariants that will not change

Whatever admission mechanism is eventually chosen, these hold:

1. **One Consensus Operator, one vote.** Sybil resistance is counted per operator identity, never
   per node or per masternode.
2. **No operator chooses what settles.** Operators order and finalise; they do not curate.
3. **No privileged provider.** The protocol publishes facts about identities; it never ranks them.
4. **Admission opens only when the cost of acquiring a threatening share is understood and
   acceptable** — not when the code merely permits it.

## Open design points

The **exact admission mechanism is `OPEN DESIGN`.** It is not decided, and this documentation will
not pretend otherwise. What is settled is the goal and the invariants above; what is not settled is
how identities are admitted, priced and bounded.

Related open points, none of them defects:

- how the expected committee size should be set for an open network;
- how the value at risk within a finality window should be bounded;
- what economic sizing makes a one-third share prohibitively expensive.

See [Open-network hardening](../consensus/open-network-hardening.md) for the arithmetic that
constrains any answer.
