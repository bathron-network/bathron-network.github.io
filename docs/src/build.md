# Build an application

Building an application means turning an agreement into a complete sequence of permitted actions. BATHRON supplies the settlement primitives. The builder supplies the terms, interface, transaction construction and services that make those primitives usable.

Start with one agreement that can be explained without code. For example: Alice commits a payment to Bob, a specified Bitcoin payment permits release, and a timed path allows recovery under agreed conditions.

## Describe every transition

Write down funding, release and recovery as separate transitions. For each one, identify the input being spent, the required evidence, the authorization, the destination and any timing condition.

| Design question | Concrete answer to record |
|---|---|
| What is committed? | Asset, amount and funding output |
| What permits release? | Exact predicate, secret or signed message |
| Where does value go? | Recipient and constrained output form |
| What permits recovery? | Eligible branch, clock and required signer |
| Who acts? | Software or person responsible for submission and observation |

Keep the human agreement and this transition description together. They should describe the same rights.

## Choose evidence and primitives

Use [Bitcoin facts in contracts](bitcoin-facts.md) for facts that Bitcoin proves. For other observations, name an external attestation source and define the exact message. A signature authenticates that source; the application remains responsible for explaining what the statement means.

Combine authorization, covenants and timelocks to express the branches. Use recursive output constraints when a successor must preserve a standing policy. The [Script reference](script.md) is a vocabulary for this work, not a substitute for designing the agreement.

## Construct and inspect transactions

Use the node's RPC help for command arguments and the source repository's accompanying build and configuration instructions for local setup. The public application model does not require a particular interface framework.

Inspect each transaction before signing: input selection, amounts, output scripts, fees and branch data. Retain the information required to reconstruct recovery. An RPC response acknowledging submission is distinct from inclusion and finality.

Exercise both accepted and rejected paths. Include wrong evidence, incorrect destinations, premature recovery, repeated submission and restart during observation. For external assets, review the other chain's flow separately and then the complete coordination between them.

## Give users an agreement they can understand

Show what the user sends, receives, authorizes and must monitor. Explain when funds are committed and what action remains available afterward. A countdown identifies its clock and condition.

Applications using existing primitives do not change consensus. A new primitive requires specification and review. For operational integrations, continue with [RPC and transactions](rpc-transactions.md), [Operate a provider](providers.md) and [Run and observe a node](node.md).
