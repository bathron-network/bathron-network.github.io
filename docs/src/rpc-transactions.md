# RPC and transactions

The node exposes a Bitcoin-style JSON-RPC interface. RPC calls inspect state, construct operations or submit transactions. Consensus evaluates the resulting transactions independently of the application that invokes the call.

Use `bathron-cli help <command>` for exact arguments and response fields. The tables below group commands by purpose; they are not shell recipes or a replacement for command help.

## Inspection and submission

| RPC | Purpose |
|---|---|
| `getblockcount` | Inspect the node's BATHRON chain height |
| `getrawtransaction` | Inspect a transaction |
| `sendrawtransaction` | Submit a serialized transaction |
| `getstate` | Inspect settlement state and monetary invariant checks |
| `getfinalitystatus` | Inspect finality information |
| `getbtcheadersstatus` | Inspect the accepted Bitcoin header view |
| `getbtcheaderstip` | Inspect its tip |
| `getwalletstate` | Inspect wallet balances and receipts |

## Operations that change state

`submitburnclaim` submits Bitcoin destruction evidence. `lock` vaults M0 and creates the corresponding M1 receipt. `unlock` consumes a receipt and releases M0. `transfer_m1` transfers a receipt.

For shielded M0 transfers, `getnewshieldaddress` creates a shielded address and `shieldsendmany` constructs a shielded payment. Select commands according to the asset representation and transaction family involved, rather than treating every balance as interchangeable.

## Transaction families

| Type | Role in validation |
|---|---|
| `NORMAL` | Ordinary transparent or shielded payment |
| `TX_LOCK` | M0 vaulting and corresponding M1 creation |
| `TX_UNLOCK` | M1 consumption and corresponding M0 release |
| `TX_TRANSFER_M1` | Receipt transfer |
| `TX_BURN_CLAIM` | Submission of Bitcoin destruction evidence |
| `TX_MINT_M0BTC` | M0 creation against an eligible verified claim |
| `TX_BTC_HEADERS` | Submission of Bitcoin headers |
| HTLC family | Creation, claim and refund of hashlocked, timed settlement |

M1 receipts are spent through the settlement transaction families that understand their accounting. Shielded M0 payments use the ordinary transfer family; see [Private inventory transfers](confidentiality.md) for disclosure by operation.

## Interpret responses correctly

Submission, inclusion and finality are separate observations. A successful RPC submission does not itself establish completed settlement. Inspect the relevant transaction and resulting state, and track any external leg independently.

Applications preserve identifiers and expected outputs so retries and restarts can be reconciled against chain evidence. Before requesting a state-changing operation, inspect amounts, destination scripts, selected inputs and the intended branch.

See [Monetary invariants](invariants.md) for accounting, [Script reference](script.md) for spending conditions and [Run and observe a node](node.md) for interpreting node views.
