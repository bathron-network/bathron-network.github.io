# Script & opcodes

The script engine is Bitcoin Script plus the programmability Bitcoin has debated for a decade without activating. The additions:

| Opcode | Bitcoin status | What it does |
|---|---|---|
| `OP_TEMPLATEVERIFY` (CTV) | BIP 119 — proposed, not activated | commit to the spending transaction's template (up to 64 outputs): the covenant **forces** where funds go |
| `OP_BTCSTATEVERIFY` + `TX_CONFIRMED` | none | verify a **Bitcoin fact** in script — a payment's confirmation (Merkle proof vs the in-consensus header chain), difficulty, height, median time |
| `OP_CHECKSIGFROMSTACK` (CSFS) | proposed | verify a signature over arbitrary data — oracle attestations on-chain |
| `OP_CAT` | disabled since 2010 (BIP 347 proposed) | concatenation (520-byte cap) — the glue for structured commitments |
| `OP_CHECKSEQUENCEVERIFY` (CSV) | active on Bitcoin | relative timelocks (BIP 68/112 semantics) |
| `OP_CHECKLOCKTIMEVERIFY` (CLTV) | active on Bitcoin | absolute timelocks |
| Output introspection (`OP_OUTPUTVALUE`, `OP_OUTPUTSCRIPT`) | none | a script can read its spending transaction's outputs — enabling **recursive covenants** (state-carrying contracts that re-create themselves) |

## What is deliberately absent

- **No general-purpose VM.** No gas market, no unbounded loops — scripts terminate, costs are predictable, and the validation surface stays auditable.
- **No Taproot/Schnorr.** ECDSA on secp256k1 throughout; simplicity over signature aggregation at current scales.

## The composition rule

Every application in [Learn → Applications](../learn/applications.md) is a composition of this table — nothing else. If a use case can't be expressed here, the answer is a better composition, not a new opcode: the surface is frozen before mainnet.
