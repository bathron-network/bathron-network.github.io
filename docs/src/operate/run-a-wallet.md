# Run a wallet

End users settle in the assets they already hold; market builders and providers settle in M1.
The wallet described here is for the second group: it is built into the node, exposes M0/M1
and the settlement operations directly, and is what a provider or developer uses to hold
inventory, fund covenants and inspect the settlement state. It is not a retail wallet or an
invitation to acquire an internal asset — see the
[accounting invariants](../reference/invariants.md).

Everything is reachable over RPC with `bathron-cli` or any JSON-RPC client. Amounts are
**satoshis** — the unit of account everywhere.

## Addresses

```bash
bathron-cli -testnet getnewaddress          # transparent address
bathron-cli -testnet getnewshieldaddress    # shielded address (private)
```

Transparent addresses are visible on chain; shielded addresses hide amounts and balances and
are how providers keep inventory and OTC sizes confidential
(see [Confidential settlement](../markets/confidential-settlement.md)).

## Sending

```bash
# transparent
bathron-cli -testnet sendmany "" '{"<address>": 10000}'

# shielded — amounts and balances hidden
bathron-cli -testnet shieldsendmany "<from>" '[{"address":"<shield-addr>","amount":10000}]'
```

## Inspecting

```bash
bathron-cli -testnet getwalletstate true    # full balance breakdown, including settlement receipts
```

## Settlement operations

The vault/receipt mechanics behind the settlement state are exposed directly:

```bash
bathron-cli -testnet lock 100000       # vault M0, receive an M1 receipt (1:1, free)
bathron-cli -testnet unlock 100000     # redeem the receipt back to M0 (1:1, free)
bathron-cli -testnet transfer_m1 <outpoint> <address>   # transfer a receipt
```

Most applications never call these directly — the SDK and provider flows wrap them — but they
are ordinary RPCs, not privileged operations.

## Getting funds

Every test unit originates from provably destroyed testnet Bitcoin — there is no mint key,
premine or issuer. A future faucet may **distribute inventory created from prior testnet
burns**; it cannot create units or bypass the invariants. Developers can also test the burn
path directly (see [From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)).

**See also:** [RPC API](../build/api.md) · [Create your first market](create-your-first-market.md)
