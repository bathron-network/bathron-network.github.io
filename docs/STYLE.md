# bathron.org — editorial style guide (refonte 2026-08)

This file governs every page on bathron.org and /docs/. It is not published (not in `src/`).

## The one rule

**Every page answers "what problem" before "how".** A page that only contains "how" belongs in
part V (Consensus), VI (Build) or VII (Reference) — never earlier. Before publishing a page, ask:
*does this describe the problem BATHRON solves, or only the way it solves it?*

## The message (must survive any single page)

BATHRON is an **open settlement protocol**. It owns no market and no exchange, and never decides
which assets may trade. It provides three things only: a common settlement unit (**M1**), a
consensus that guarantees settlements, and an infrastructure any market can be built on.
**Markets belong to whoever builds them. Bitcoin remains the final asset.**

Five-minute test — a new reader must be able to say:
> "BATHRON is an open settlement infrastructure where anyone can create a market without
> permission, while Bitcoin remains the ultimate settlement asset."

## Vocabulary (fixed)

| Term | Meaning | Never |
|---|---|---|
| **Operator** (Settlement Operator) | consensus role: produces blocks, signs finality, publishes facts | "masternode" in prose (RPC/source keep the lineage name — say so once, in the consensus page) |
| **Settlement Provider (SP)** | umbrella for the commercial roles below; a participant, never an administrator | "member", "administrator", "validator" |
| **Clearing Provider (CP)** | quotes, orchestrates legs, deadlines, SLA | — |
| **Liquidity Provider (LP)** | holds inventory, prices a pair, earns the spread | "market maker chosen by the protocol" |
| **M1** | the settlement unit / numéraire; created 1:1 from M0, which comes only from verified BTC destruction | "coin", "token", "buy M1", "invest" |
| **M0** | the vaulted origin unit behind M1 | — |
| **market / pair** | `X/M1` — exists when someone brings inventory and quotes; the protocol never validates it | "listed", "supported pair" |
| **settle / settlement** | what consensus does; the only thing it does | "trade on BATHRON", "BATHRON exchange" |
| **covenant** | a script constraining how value moves | "smart contract" (EVM sense) |
| **Bitcoin facts** | headers/proofs verified inside consensus (SPV) | "oracle" |

Audience sentence, reuse verbatim when the M1 question comes up:
> End users settle in the assets they already hold; market builders and providers settle in M1.

## The permissionless sentence (reuse verbatim; never one half without the other)

> Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator
> admission is **not yet open**: the current operator set is project-run while the
> open-admission threat model is worked.

## Status facts (2026-08)

- Public testnet live (measurement network). Genesis block 0 = `691b0a7e8cb0e7ee159ef7a4fa10d9c6ddb2d5282e5bac7447846459ff54c730`. Public seed `57.131.33.151:27171`.
- Bitcoin source read by consensus: **Bitcoin testnet4** (mainnet at mainnet). Say "testnet4", not "signet".
- No mainnet. No external audit yet. No proven market. Operator set closed.
- Demonstrated on testnet: covenants (accept & reject paths), Bitcoin headers + Merkle proofs in consensus, burn → M0 → M1, shielded transfers, `TX_CONFIRMED` releasing a covenant, **paired HTLCs** (M1 HTLC + Bitcoin P2WSH HTLC, same preimage), CP/LP prototypes (`pna-lp`, `pna-swap`) exposing quotes over HTTP.

## Forbidden claims (unchanged from the 2026-07 canon; put them ONLY on "Status & claims" as a public list)

client funds guaranteed · general atomicity · "no counterparty risk" · external par / peg for M1 ·
"backed by Bitcoin" · "CLS for crypto" · yield or expected appreciation of M0/M1 · "supports DOGE/PIVX/…"
(say: *any chain with hashlocks and timelocks can be paired the same way — capability, not a shipped product*).

## Hedges: one page only

The honest caveats (not atomic yet, project-run operators, no mainnet, no audit) live on **Status &
claims** and nowhere else in full. Other pages link there in one line: *see [Status & claims](...)*.
Do not repeat the caveat paragraph on every page — it drowns the message.

## Tone

Plain, declarative, short paragraphs. No marketing adjectives (revolutionary, unique, seamless).
Analogies allowed: Internet/HTTP/apps · "Bitcoin doesn't decide who may hold BTC; BATHRON doesn't
decide which markets may exist" · a market today is a lease from a landlord, here it is land with no
owner · numéraire = pivot language (N pairs, not N²) · PvP/DvP principle (never "CLS").
Diagrams: inline SVG or `text` blocks, same palette as the site (`#D9A441` gold, `#0C0F14` panel,
`#1C222C` line, `#E8EBF0` ink, `#8A919C` muted). Keep them small.

## Structure

Every page: `# Title` → one-paragraph "why this matters" → body → optional `**Primitives:**` /
`**See also:**` line. Headings in sentence case. Reference pages (part VII) are exempt from the
"why" paragraph.
