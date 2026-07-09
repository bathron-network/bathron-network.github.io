# Inheritance

The problem: pass funds to heirs **without trusting a custodian while alive, and without losing them at death**. A covenant expresses this directly.

```text
  funds ── owner key ─────────▶ spendable any time (normal life)
    │
    ├── heir key + CSV delay ─▶ claimable after N months of inactivity
    │
    └── owner key during delay ▶ sweeps back (proof of life)
```

## How it works

1. The owner spends freely; every spend restarts the clock.
2. If the funds sit untouched for the timeout (`CSV`), the heir's path becomes valid.
3. Refinements compose naturally: multiple heirs with a forced split (`CTV` template), a notary co-signature (`CSFS`) required alongside the heir key, or a staged claim the owner can still veto.

No lawyer holds the key. No exchange decides who inherits. The estate plan is a script, verified by consensus, private in amount.

**Primitives:** `CSV` · `CTV` · `CSFS` · shielded balances
