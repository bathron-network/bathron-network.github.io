# RPC API

The node speaks Bitcoin-style JSON-RPC. Familiar calls (`getblockcount`, `getrawtransaction`, `sendrawtransaction`…) work as expected; this page lists what is BATHRON-specific.

## State and consensus

| RPC | Returns |
|---|---|
| `getstate` | global settlement state + live check of the monetary invariants |
| `getfinalitystatus` | finality height, lag, average delay |
| `getactivemnstatus` | this node's masternode status |

## Bitcoin integration

| RPC | Returns |
|---|---|
| `getbtcheadersstatus` | the in-consensus Bitcoin header chain (tip, work, sync) |
| `getbtcheaderstip` | tip of the header database |
| `submitburnclaim` | submit an SPV proof of a Bitcoin burn |

## Settlement

| RPC | Action |
|---|---|
| `lock <amount>` | vault M0 → M1 receipt (1:1) |
| `unlock <amount>` | M1 receipt → M0 (1:1) |
| `transfer_m1 <outpoint> <addr>` | transfer a receipt |
| `getwalletstate true` | balances including receipts |

## Privacy

| RPC | Action |
|---|---|
| `getnewshieldaddress` | new shielded address |
| `shieldsendmany` | shielded payment |

Full per-command help is available from the node itself: `bathron-cli help <command>`.
