# Run a wallet

The wallet is built into the node for protocol testing. It exposes M0/M1 because developers,
CPs and LPs need to inspect the internal mechanics; it is not a retail wallet or an invitation to
acquire an internal asset. See the [accounting invariants](../reference/invariants.md).

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

Every test unit originates from provably destroyed testnet Bitcoin—there is no mint key, premine
or issuer. A future faucet may **distribute inventory created from prior testnet burns**; it cannot
create units or bypass the invariants. Developers can also test the burn path directly.
