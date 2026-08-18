# FAQ

## Do I need permission to create a market?

No. A market on BATHRON exists when someone brings inventory, publishes quotes and finds a
counterparty. There is no listing process, no committee, no fee to the protocol. Nobody can
approve a pair, so nobody can delist it. → [How a market appears](markets/how-a-market-appears.md)

## Who decides which assets can trade?

Nobody. The consensus does not know which pairs exist — it only settles. Any chain that supports
hashlocks and timelocks can be paired against M1 with the same atomic pattern used for native BTC.
That is a capability of the primitives; no pair other than BTC/M1 has been tested or shipped.
→ [Pairing any asset](markets/pairing-any-asset.md)

## Is M1 a coin I should buy?

No. M1 is the settlement unit — the working capital of whoever runs a market. End users settle in
the assets they already hold; market builders and providers settle in M1. Because anyone can create
M1 by destroying bitcoin, destruction is a permanent reference supply route that tends to limit
any premium when it is accessible — there is nothing to speculate up — and nothing guarantees a
floor or any external price. There is no token sale, premine, treasury, block reward or promised yield.
→ [The settlement unit](provides/settlement-unit-m1.md)

## Is M1 pegged to Bitcoin? Is it "backed by Bitcoin"?

No, and no. Consensus enforces the internal 1:1 between M0 and M1. It does not enforce, and the
protocol never promises, an external price. The destroyed bitcoin is gone — there is no reserve and
no redemption desk. What makes native BTC available again is the market: providers holding
inventory on both sides, paired with linked hashlocked legs. → [Bitcoin is the final asset](bitcoin/final-asset.md)

## Why destroy bitcoin at all?

Because it is the only way to create the unit without a keeper. A reserve needs a custodian or a
federation; a destroyed satoshi needs nobody. The BTC is gone, verifiably, and one M0 unit exists
in its place. Irreversible by design — a cost recovered through service revenue, never through
appreciation. → [From destroyed BTC to M1](bitcoin/from-btc-to-m1.md)

## Why not just use an exchange, or a bridge?

An exchange's listing committee is the permission problem itself; a bridge always has a keeper.
BATHRON is custody-free, verifies Bitcoin itself, and is open — and gives up a recoverable vault
in exchange. → [Why not an exchange, a bridge, or a stablecoin](problem/why-not-alternatives.md)

## Does BATHRON hold my BTC?

Never. BATHRON verifies Bitcoin facts and irreversible burns; it cannot move native BTC or trigger
a Bitcoin transaction. Native BTC moves only through Bitcoin-side contracts (hashlocked legs)
between you and a counterparty.

## Who provides the service?

Settlement Providers — participants, not administrators. A Clearing Provider quotes and
orchestrates; a Liquidity Provider holds inventory and prices a pair. Operators run consensus and
finality; they publish facts about themselves and never rank anyone, choose a provider or set a
price. → [Roles](markets/roles.md)

## Is the network permissionless today?

Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator admission
is **not yet open**: the current operator set is project-run while the open-admission threat model
is worked. → [Open-network hardening](consensus/open-network-hardening.md)

## Is settlement atomic and risk-free today?

Not as a general guarantee. Paired-HTLC and covenant components have run on the testnet; the
complete cross-chain state machine, reorganisation handling and timelock ordering still need formal
specification and external review. → [Status & claims](consensus/status-and-claims.md)

## Why is the consensus so small?

On purpose. Anything that can be built above consensus must be built above it — quotes, matching,
reputation, provider choice, fast liveness signals. Every consensus line is decades of maintenance
and attack surface, and a protocol that lists cannot be neutral about listing. The surface is
frozen. → [Why the consensus is frozen](consensus/why-frozen.md)

## Why confidentiality?

Commercial settlement exposes counterparties, sizes and treasury flows. Shielded transfers hide
amounts and linkage on the internal leg while consensus still checks conservation. It is a
property of settlement, not a "private cash" product, and not Monero's anonymity set.
→ [Confidential settlement](markets/confidential-settlement.md)

## Is this CLS for crypto?

No. Payment-versus-payment — one leg if and only if the other — is a useful functional analogy.
BATHRON has no central-bank accounts, no regulated membership, no equivalent legal finality and no
systemic track record.

## What exists today?

A public testnet with covenant execution, Bitcoin headers and proofs checked in consensus (source:
Bitcoin testnet4), confidential internal transfers, paired-HTLC demonstrations, fast finality, and
provider prototypes exposing quotes over HTTP. No mainnet, no external audit, no proven market.
→ [Status & claims](consensus/status-and-claims.md)
