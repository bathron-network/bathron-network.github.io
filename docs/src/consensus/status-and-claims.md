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
    <text x="70" y="74" text-anchor="middle" fill="#8A919C" font-size="11">done · scoped surface exercised</text>
    <text x="330" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Public testnet</text>
    <text x="330" y="74" text-anchor="middle" fill="#8A919C" font-size="11">now · first builders</text>
    <text x="590" y="24" text-anchor="middle" fill="#E8EBF0" font-size="12" font-weight="600">Mainnet</text>
    <text x="590" y="74" text-anchor="middle" fill="#8A919C" font-size="11">gated · audits + economics</text>
    <text x="200" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: ran live, in scope</text>
    <text x="460" y="106" text-anchor="middle" fill="#5B626E" font-size="10">gate: open-network safe</text>
  </g>
</svg>

**Done — private testnet.** A multi-node network exercised the consensus surfaces then in scope: VRF
finality, the in-consensus Bitcoin header chain, burn → mint, the covenant opcodes, shielded
transfers, a real Bitcoin payment releasing a covenant, and paired HTLCs for a BTC-out leg. The
consensus surface was frozen during this phase; the work was proof, not features — the primitives then in scope exercised on-chain (accept *and* reject paths), adversarial red-teaming, fuzzing of
the money chokepoints, and dead code removed where it was found. **Its gate was passed** on the evidence available at the time: the surfaces then in scope were exercised live, with no monetary or safety issue open against them **that this work had identified** — an absence of findings, not a proof of absence, and no external audit was involved — with a clean launch genesis
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

## How to read the five labels

This documentation labels every capability. The labels are load-bearing, and the first one is the one most easily misread: an opcode being active in consensus does **not** mean a product uses it.

| Label | Means |
|---|---|
| `ACTIVE IN CONSENSUS` | the opcode or rule is enabled on this testnet — **not a statement about any product** |
| `TESTED` | has a test suite |
| `DEMONSTRATED` | an end-to-end flow has actually been run |
| `AVAILABLE PRIMITIVE` | composable with no consensus change — **no product exists** |
| `TARGET NETWORK` | the architecture being aimed at — **not deployed** |

**Active primitives.** The covenant, introspection and Bitcoin-fact opcodes are active in
consensus on this testnet: `OP_BTCSTATEVERIFY`, `OP_TEMPLATEVERIFY`, `OP_CHECKSIGFROMSTACK`,
`OP_CAT`, `OP_CHECKOUTPUTVALUE`, `OP_CHECKOUTPUTSCRIPT`, `OP_PUSHCURRENTSCRIPT`, plus the two
timelock opcodes. Declared in `src/script/script.h`, implemented in `src/script/interpreter.cpp`.

**Demonstrations.** Paired-HTLC settlement against Bitcoin, covenant accept **and** reject paths.

**Products that do not exist.** No price oracle, no margin engine, no liquidation in consensus, no
synthetic asset, no built market. An active opcode is not a product.

**Target network, not deployed.** Open Consensus-Operator admission, several independent operators
and providers — see [The target open network](../network/open-network-target.md). The exact
admission mechanism is **`OPEN DESIGN`**: not decided.

**Known coverage gaps.** `BTCSTATE_TX_CONFIRMED` has no dedicated test suite. `OP_CAT`,
`OP_CHECKSIGFROMSTACK` and the two output-introspection opcodes have unit tests but no end-to-end
demonstration. The confidentiality of covenant-bearing settlement is not demonstrated.

## Current public testnet

Live (measurement network):

- Genesis block 0: `691b0a7e8cb0e7ee159ef7a4fa10d9c6ddb2d5282e5bac7447846459ff54c730`
- Public seed: `57.131.33.151:27171`
- Bitcoin source read by consensus: **Bitcoin testnet4** (mainnet at mainnet)

Exercised on this network:

- covenants — accept **and** reject paths;
- Bitcoin headers and Merkle proofs verified inside consensus;
- burn → M0 → M1;
- shielded transfers;
- **paired HTLCs** — an M1 HTLC and a Bitcoin P2WSH HTLC sharing one preimage. Components are
  covered by public test suites; **no reproducible artifact of an end-to-end run is published**.

## Historical demonstrations

Runs from **earlier networks**, kept for the record. They were real; the network they ran against
is **not** the one live today, and nothing here should be read as describing current behaviour.

- The Clearing and Liquidity Provider prototypes (`pna-lp`, `pna-swap`) exposed quotes over HTTP.
  They are **decommissioned**: their application state belonged to a superseded network and the
  services are **not running**. Their HTTP APIs are not available, and no endpoint should be
  treated as callable.

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
