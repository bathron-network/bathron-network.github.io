# Consensus parameters

| Parameter | Value |
|---|---|
| Block interval | 60 seconds |
| Producer selection | deterministic pseudo-random over operator nodes, per block, with fallback slots |
| Finality committee | per-operator ECVRF sortition, redrawn every block |
| Finality threshold | `⌈2/3 · min(E, N)⌉` — `N` = operators at the block, `E` = committee cap (128) |
| Quorum floor | 4 distinct operators minimum to finalize |
| Finality latency | ~1 minute (one signature round) |
| Counting unit | the **operator key** — N masternodes under one operator = 1 vote |
| Signatures | ECDSA / secp256k1 (finality and blocks); RedJubjub inside Sapling |
| Block reward | **0** |
| Coinbase | = transaction fees, exactly |
| Treasury | none |
| Unit of account | the satoshi |
| Supply source | verified Bitcoin burns only |
| Slashing | none — deliberate ([why](../learn/consensus.md#design-choices)) |

## Reading the table

The threshold formula is the part worth internalizing: with few operators (`N ≤ E`) everyone signs and the threshold follows `N`; at scale the VRF samples ~`E` of them. One fixed cap covers a handful of launch operators through hundreds, with no parameter change — and committee size does not affect latency, since collection is a single parallel gossip round.

Once the threshold is met, the block is **irreversible**: a conflicting chain is rejected regardless of its length. Finality overrides chainwork.
