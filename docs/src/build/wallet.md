# Wallet

The wallet lives in the node; everything is reachable over RPC with `bathron-cli` or any JSON-RPC client.

## Addresses and balances

```bash
bathron-cli -testnet getnewaddress            # transparent
bathron-cli -testnet getnewshieldaddress      # shielded
bathron-cli -testnet getwalletstate true      # full balance breakdown
```

## Payments

```bash
# transparent payment
bathron-cli -testnet sendmany "" '{"<address>": 25000}'

# shielded payment — amount and balances hidden
bathron-cli -testnet shieldsendmany "<from>" '[{"address":"<shield-addr>","amount":25000}]'
```

Amounts are **satoshis** — the unit of account everywhere.

## Settlement operations

The vault/receipt mechanics behind the settlement state ([invariants](../reference/invariants.md)) are exposed directly:

```bash
bathron-cli -testnet lock 100000       # vault M0, receive an M1 receipt (1:1, free)
bathron-cli -testnet unlock 100000     # redeem the receipt back to M0 (1:1, free)
bathron-cli -testnet transfer_m1 <outpoint> <address>   # transfer a receipt
```

Most applications never call these directly — the SDK and SP flows wrap them — but they are ordinary RPCs, not privileged operations.
