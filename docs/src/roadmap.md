# Roadmap

Three phases, no dates. Each phase gates the next.

## Now — private testnet

The full surface runs live on a multi-node network: consensus with VRF finality, the in-consensus Bitcoin header chain, burn → mint, covenants, shielded transfers, and the flagship flow end-to-end — a real Bitcoin payment releasing a covenant, and an atomic BTC-out swap. The consensus surface is **frozen**: work at this stage is testing, hardening and tooling, not new features.

## Next — public testnet

The network opens: published genesis and peers, public explorer, the Settlement Provider reference implementation, the SDK, and runnable examples. The goal of this phase is a simple one: **the first builders shipping on the substrate.** Disposable-genesis resets remain possible until the network stabilizes.

## Then — mainnet

Gated, not scheduled. Hard prerequisites include external security audits (the VRF finality module foremost), operator-set and collateral economics for an open network, and a launch process where genesis itself is SPV-verified like every block after it — no special cases.

---

The homepage principle applies here too: if this page needs to change often, something is wrong. The substrate is meant to stay small and finished; what should grow is what's built on it.
