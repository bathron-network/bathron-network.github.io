# Run a wallet

The wallet is built into the node — there is no separate wallet binary. As a user you **send and hold satoshis**; the internal M0/M1 mechanics are an implementation detail ([how the money works](../reference/invariants.md)).

## Addresses

```bash
bathron-cli -testnet getnewaddress          # transparent address
bathron-cli -testnet getnewshieldaddress    # shielded address (private)
```

## Sending

```bash
# transparent
bathron-cli -testnet sendmany "" '{"<address>": 10000}'

# shielded — amounts and balances hidden
bathron-cli -testnet shieldsendmany "<from>" '[{"address":"<shield-addr>","amount":10000}]'
```

## Inspecting

```bash
bathron-cli -testnet getwalletstate true    # balances, including settlement receipts
```

## Getting funds

Every circulating unit originates from provably burned Bitcoin — there is no faucet key, no premine, no issuer. On the public testnet, funds come from burning testnet BTC ([Bitcoin integration](../learn/bitcoin-integration.md)) or receiving them from someone who did.
