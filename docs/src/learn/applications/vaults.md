# Vaults

Cold storage with **rules instead of promises**: a covenant that makes theft slow and recovery fast.

```text
  vault ──── withdraw ────▶ staging (CSV delay)
    ▲                            │
    │      recovery key,         │  delay elapsed
    │      any time during       ▼
    └────── the delay      destination
```

## How it works

1. Funds sit under a vault covenant. The only permitted spend (`CTV` template) moves them to a **staging** output — never directly out.
2. The staging output enforces a delay (`CSV`). During it, a recovery key can sweep the funds back — this is the theft alarm: a thief must announce the withdrawal on-chain and then wait, in full view.
3. After the delay, funds move to the destination.

Bitcoin has debated exactly this construction for years (it is the canonical CTV use case). Here it runs.

## Variants

Recursion — a covenant that re-creates itself — allows vaults with **standing rules**: rate-limited spending (at most X per period), or a vault that always returns change to itself.

**Primitives:** `CTV` · `CSV` · output introspection (recursion)
