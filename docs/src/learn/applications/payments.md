# Payments

The base case: move satoshis, privately, final in about a minute.

```text
  Alice ──── shielded transfer ────▶ Bob
             amount hidden
             balances hidden
             final in ~1 min
```

## What you get

- **The unit is the satoshi.** No volatile gas token between you and your money — every unit is backed by provably burned Bitcoin.
- **Privacy by default is available.** Shielded transfers hide amounts and balances; a business can pay suppliers without publishing its treasury.
- **Finality in about a minute**, irreversible — not probabilistic confirmation.

## What it is not

Not a Lightning competitor: no channels, no routing, no liquidity management — but also no per-hop capacity limits and no requirement to be online. A plain on-chain payment, private, final in a minute.

**Primitives:** shielded transfers (Sapling) · BFT finality
