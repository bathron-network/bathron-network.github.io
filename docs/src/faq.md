# FAQ

## Why burn Bitcoin?

Because it is the only way to back a unit with Bitcoin **trustlessly**. A bridge needs custodians; a federation needs trust; a burn needs neither — it is irreversible, verifiable by SPV, and requires no one's permission or honesty. One burned satoshi backs one unit, forever, with no issuer to default.

## Why not Ethereum?

Bridged BTC on Ethereum is custodial (a wrapper someone can freeze or lose), there is no base-layer privacy, and you price everything through a volatile gas token. BATHRON's unit *is* the satoshi, backing is burned BTC with no bridge, and private cash is built in.

## Why not Liquid?

Liquid is a **federation**: a fixed set of functionaries custodies the peg and can censor. BATHRON has no federation — Bitcoin facts are verified by SPV inside consensus, and the return to native BTC is an open market, not a multisig.

## Why no token?

Because nothing needs one. Fees are paid in satoshis, security is funded by fees (`block_reward = 0`), there is no treasury and no premine. A token would add a speculation layer and a conflict of interest — and remove nothing.

## Why Settlement Providers?

Because the protocol cannot move native BTC — nobody can, trustlessly, from another chain. So the design refuses to fake it: native liquidity comes from an open market of providers competing on fees, settling atomically, custodying nothing. → [Settlement Providers](learn/settlement-providers.md)

## Why private?

Settlement is commercially unusable if competitors can read your counterparties, sizes and treasury. Privacy here is a **property of good settlement**, not an ideology — amounts are shielded; the monetary invariants stay publicly verifiable.

## Can I become a Settlement Provider?

Yes — that is the intended path, and there is no whitelist. The reference implementation publishes with the public testnet; [contact us](mailto:contact@bathron.org) to be early.

## Can I run a validator?

Yes. Validators are masternodes backed by burned-BTC collateral. On the current private testnet the operator set is closed; it opens progressively with the public testnet. → [Consensus](learn/consensus.md)

## Is it experimental?

**Yes.** Private testnet running, public testnet next, no mainnet. The consensus surface is frozen before any mainnet, and external audits gate the launch. We would rather under-promise here and let the running system speak.
