# Programmable settlement

Beyond Bitcoin facts, the script engine constrains **what a spend may become**. All opcodes below
are active on the current public testnet.

## Opcodes

Declared in `src/script/script.h`, implemented in `src/script/interpreter.cpp`:

| Opcode | What it does | Status |
|---|---|---|
| `OP_TEMPLATEVERIFY` | commits a spend to a template of its outputs (CTV-style covenant) | `ACTIVE IN CONSENSUS`, `TESTED` |
| `OP_BTCSTATEVERIFY` | asserts a Bitcoin fact — see [Bitcoin-verifiable contracts](bitcoin-verifiable-contracts.md) | `ACTIVE IN CONSENSUS`, `TESTED` |
| `OP_CHECKSIGFROMSTACK` | verifies a signature over an **arbitrary message**, not the spending transaction | `ACTIVE IN CONSENSUS`, `TESTED`, not `DEMONSTRATED` |
| `OP_CAT` | concatenates two stack elements, bounded by the 520-byte element cap | `ACTIVE IN CONSENSUS`, `TESTED`, not `DEMONSTRATED` |
| `OP_CHECKOUTPUTVALUE` | constrains an output's amount | `ACTIVE IN CONSENSUS`, `TESTED`, not `DEMONSTRATED` |
| `OP_CHECKOUTPUTSCRIPT` | constrains an output's script | `ACTIVE IN CONSENSUS`, `TESTED`, not `DEMONSTRATED` |
| `OP_PUSHCURRENTSCRIPT` | pushes the executing script, enabling **recursive** covenants | `ACTIVE IN CONSENSUS`, `TESTED`, not `DEMONSTRATED` |
| `OP_CHECKLOCKTIMEVERIFY` / `OP_CHECKSEQUENCEVERIFY` | absolute and relative timelocks | `ACTIVE IN CONSENSUS` |

`OP_CHECKOUTPUTSCRIPT` together with `OP_PUSHCURRENTSCRIPT` form a **recursive covenant pair**: a
script can require its successor to carry the same rules with new state.

## Hashlocks and timelocks

Hashlocked, timelocked conditional scripts are the basis of cross-chain settlement. Paired-HTLC
flows have run on the testnet against Bitcoin. `TESTED` and demonstrated for that pair.

What is **not** claimed: a general atomicity guarantee. The complete cross-chain state machine,
reorganisation handling and timelock ordering still need formal specification and external review.

## External attestations (DLC) {#external-attestations-dlc}

For anything Bitcoin cannot prove, the engine can consume a signed attestation.
`OP_CHECKSIGFROMSTACK` verifies a signature over an arbitrary message, and the script engine
supports discreet-log-contract shapes **with no new opcode**: two-of-two funding, multi-branch
outcome nodes, an oracle branch where the attestation itself is the private key, and a timelocked
refund.

Status: `AVAILABLE PRIMITIVE`. The script side is covered by tests; **no product exists**, and the
attestation source is entirely outside the protocol. BATHRON checks a signature. It cannot make the
attested statement true, nor contest it.

## Confidentiality

Sapling shielded transfers are available. Values can move without being published.

Limit, stated plainly: the confidentiality of **covenant-bearing** settlement — shielded value
combined with conditional script — is **not demonstrated**. Treat it as an open question, not a
feature.

## Composition

The primitives compose: a covenant can require a Bitcoin fact, a hashlock and a timelock at once;
a recursive covenant can carry state forward. The set of useful compositions has **not** been
inventoried, and this documentation does not claim to have enumerated it.
