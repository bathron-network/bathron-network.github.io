# Run and observe a node

Independent verification lets a participant inspect settlement without relying solely on a provider's website or an explorer. A BATHRON node validates history, maintains the settlement state and checks the Bitcoin evidence used by the protocol. Running one is distinct from producing blocks or supplying liquidity.

Use the installation, build and configuration instructions accompanying the node source repository. Those instructions describe the operational setup. This page explains what to observe and how to interpret it, without fixing a network endpoint or deployment recipe.

## Separate the views

A node's chain view, finality view, Bitcoin header view and wallet view answer different questions. Reading them together prevents a single height or balance from standing in for the entire settlement process.

| Question | Relevant RPC |
|---|---|
| What BATHRON history does this node hold? | `getblockcount` |
| What settlement state does it validate? | `getstate` |
| What history has finality? | `getfinalitystatus` |
| What Bitcoin header evidence does it hold? | `getbtcheadersstatus` and `getbtcheaderstip` |
| What funds and receipts does this wallet control? | `getwalletstate` |

Use `bathron-cli help <command>` for arguments and returned fields. Reading these views does not require the node to advertise a commercial service.

## Observe an operation through completion

For an agreement, record the funding output and relevant transaction identifiers. Check the transaction contents, inclusion and finality separately. If release uses a Bitcoin predicate, observe the evidence and its eligibility in the accepted header view as well.

An external leg needs its own chain observation. BATHRON finality does not replace that check. A provider can report completion, while an observer independently verifies the evidence that supports the report.

## Use a wallet for the appropriate role

Professional wallets manage M0, M1 receipts, transaction authorization and inventory records. Locking and unlocking are internal accounting operations. They are distinct from acquiring BTC through a provider.

Application users can interact through interfaces organized around their existing assets. Such an interface should still expose the agreement, its authorizations and its recovery responsibilities clearly.

Keep wallet signing authority separate from observation where the operating setup allows it. Give monitoring processes the data they need to follow an agreement and preserve the records required to resume observation after a restart.

## Publish facts, not protocol endorsements

An observer can publish chain data, verified transaction evidence or service observations. It should distinguish direct observations from interpretations and state which chain view supports a conclusion. A reputation judgment remains the observer's or reader's judgment.

See [RPC and transactions](rpc-transactions.md) for commands, [Bitcoin verification](bitcoin-verification.md) for evidence and [Network operators](operators.md) for the separate consensus role.
