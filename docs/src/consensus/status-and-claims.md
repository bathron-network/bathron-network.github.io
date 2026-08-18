# Status & claims

This is the one page on the site that carries the full caveats. Every other page links here
instead of repeating them, so that the message elsewhere stays readable — and so that a reader
who wants to know exactly what is proven, what is not, and what BATHRON refuses to claim can
find it in one place.

## Where the network is

Three phases, **gated, not scheduled**. Each phase must earn the next — a date would be a
promise the code hasn't made yet.

<svg viewBox="0 0 660 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three gated phases: private testnet, public testnet, mainnet">
  <line x1="70" y1="46" x2="590" y2="46" stroke="#1C222C" stroke-width="2"/>
  <line x1="70" y1="46" x2="330" y2="46" stroke="#D9A441" stroke-width="2" opacity=".55"/>
  <g font-family="ui-monospace,Menlo,monospace">
    <circle cx="70" cy="46" r="8" fill="#3A4150"/>
    <circle cx="330" cy="46" r="9" fill="#D9A441"/>
    <circle cx="590" cy="46" r="8" fill="#0C0F14" stroke="#3A4150" stroke-width="2"/>
    <text x="70" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Private testnet</text>
    <text x="70" y="74" text-anchor="middle" fill="#8A919C" font-size="11">done · surface proven</text>
    <text x="330" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Public testnet</text>
    <text x="330" y="74" text-anchor="middle" fill="#8A919C" font-size="11">now · first builders</text>
    <text x="590" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Mainnet</text>
    <text x="590" y="74" text-anchor="middle" fill="#8A919C" font-size="11">gated · audits + economics</text>
    <text x="200" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: it works, live</text>
    <text x="460" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: open-network safe</text>
  </g>
</svg>

**Done — private testnet.** A multi-node network ran the entire consensus surface live: VRF
finality, the in-consensus Bitcoin header chain, burn → mint, the covenant opcodes, shielded
transfers, a real Bitcoin payment releasing a covenant, and paired HTLCs for a BTC-out leg. The
consensus surface was frozen during this phase; the work was proof, not features — every
primitive exercised on-chain (accept *and* reject paths), adversarial red-teaming, fuzzing of
the money chokepoints, and the code driven to zero legacy and zero dead code. **Its gate was
passed:** full surface proven live, no open monetary or safety issue, a clean launch genesis
rehearsed.

**Now — public testnet.** The current phase. Published genesis and peers, a public block
explorer, the Clearing and Liquidity Provider prototypes, the SDK and runnable examples. The
public testnet is built to differ from mainnet in as few ways as possible: same block rules,
same invariants, same finality math, same M0-origin rule. The differences that remain are the
ones that *must* differ — the Bitcoin network it reads (**testnet4** vs mainnet), the genesis
message and the address identity bytes. The goal of this phase is one thing: the first builders
shipping on the substrate. Disposable-genesis resets remain possible while the network
stabilizes. This is also where the Operator set begins to open — from a project-run set toward
independent Operators; the [open-network hardening](open-network-hardening.md) track exists to
make that safe. **Gate to mainnet:** the hardening items resolved or explicitly bounded, and the
external audits returned.

**Then — mainnet.** Gated, not scheduled — and not planned for any date. Mainnet carries real
value, so it also carries the one rule that never bends: genesis itself is SPV-verified like
every block after it — no special case, no bypass, no premine. Any first internal unit on
mainnet would have to originate from a verified Bitcoin destruction, exactly like the millionth.
The mechanical launch steps (mine and pin the mainnet genesis with a recency proof, flip the
covenant gates to active, ship the non-disposable bootstrap tooling) are written down and mostly
built — execution, not research. The research-shaped prerequisites are the hardening track.

## What runs today

Public testnet, live (measurement network):

- Genesis block 0: `691b0a7e8cb0e7ee159ef7a4fa10d9c6ddb2d5282e5bac7447846459ff54c730`
- Public seed: `57.131.33.151:27171`
- Bitcoin source read by consensus: **Bitcoin testnet4** (mainnet at mainnet)

Demonstrated on testnet:

- covenants — accept **and** reject paths;
- Bitcoin headers and Merkle proofs verified inside consensus;
- burn → M0 → M1;
- shielded transfers;
- `TX_CONFIRMED` releasing a covenant on proof of a Bitcoin payment;
- **paired HTLCs** — an M1 HTLC and a Bitcoin P2WSH HTLC sharing one preimage;
- Clearing and Liquidity Provider prototypes (`pna-lp`, `pna-swap`) exposing quotes over HTTP.

## What is not proven

- No mainnet.
- No external audit yet — in particular, no external audit of the VRF finality path.
- No proven market: no sustained client demand, provider revenue or competitive liquidity.
- The Operator set is project-run. Sybil resistance under open Operator admission is not
  demonstrated; the current set does not demonstrate Byzantine resistance under open
  admission, and does not remove software bugs, key compromise or correlated infrastructure
  failure.
- No value-at-risk bound per finality window.
- No protocol-enforced or independently verified Operator↔provider identity link.
- No productised, externally reviewed cross-chain conditional-settlement flow: paired HTLC
  components have been tested, but general atomicity is not claimed before the full state
  machine is specified and reviewed.

## Open design points (not defects, not features)

- **Sampling regime of finality (`N > E`).** The quorum is `⌈2/3·min(E,N)⌉` and stays fixed
  when more than `E` Operators are eligible, while the VRF-drawn committee size varies around
  `E`. Whether the quorum should track the realised draw, and the fallback when a draw is too
  small, are undecided; no network has reached this regime. → [Open-network hardening](open-network-hardening.md)

## Claims we do not make

You will not read on this site that:

- client funds are guaranteed;
- settlement is atomic in general;
- there is "no counterparty risk";
- M1 has an external par or a peg;
- M1 is "backed by Bitcoin";
- BATHRON is a "CLS for crypto";
- M0 or M1 carry a yield or an expected appreciation;
- BATHRON "supports" this or that chain — any chain with hashlocks and timelocks can be paired
  the same way; that is a capability, not a shipped product.

If a page anywhere on bathron.org contradicts this list, the list wins and the page is wrong.

## One line for the other pages

Every other page — and every README in the `bathron-network` repositories — links here instead of repeating these caveats; where any other public text claims more, this page prevails ([documentation policy](../reference/documentation-policy.md)).

**See also:** [Open-network hardening](open-network-hardening.md) · [Security model](security-model.md) · [Why the consensus is frozen](why-frozen.md)
