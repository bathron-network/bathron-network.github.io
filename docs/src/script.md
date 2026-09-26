# Script reference

BATHRON scripts express conditions for spending outputs. Covenants constrain the resulting transaction; signatures, secrets, Bitcoin evidence and time conditions determine whether a branch is eligible. Applications compose these operations into agreements with explicit funding and recovery paths.

This reference gives their meaning. Exact stack encodings and transaction serialization belong with the implementation's script definitions and accompanying specifications.

## Covenant and data operations

| Operation | Meaning |
|---|---|
| `OP_TEMPLATEVERIFY` | Require the spending transaction to match the committed template |
| `OP_CHECKOUTPUTVALUE` | Check a constraint on an output's amount |
| `OP_CHECKOUTPUTSCRIPT` | Check a constraint on an output's script |
| `OP_PUSHCURRENTSCRIPT` | Place the executing script on the stack for composition |
| `OP_CAT` | Concatenate stack elements within script limits |
| `OP_CHECKSIGFROMSTACK` | Verify a signature over a supplied message |

Output script constraints combined with the executing script support recursive covenants: a successor output can preserve a policy. They carry rules between transactions rather than execute an unbounded loop inside one transaction.

A signature over a supplied message authenticates the agreed signer and message. The application defines the message's meaning, including the event and observation point, so a signature is not interpreted outside its intended agreement.

## Bitcoin predicates

`OP_BTCSTATEVERIFY` evaluates a specified Bitcoin condition against the accepted view.

| Predicate | Condition |
|---|---|
| `BTCSTATE_DIFF_GTE` | Difficulty at the specified height is at or above the threshold |
| `BTCSTATE_DIFF_LT` | Difficulty at the specified height is below the threshold |
| `BTCSTATE_HEIGHT_GTE` | Readable Bitcoin history reaches the required height |
| `BTCSTATE_MTP_GTE` | The specified Bitcoin median time reaches the threshold |
| `BTCSTATE_TX_CONFIRMED` | Proven payment satisfies destination, amount and depth requirements |

These are predicates, not general numerical queries. Chainwork is part of header verification, not an additional script reading. See [Bitcoin verification](bitcoin-verification.md) for the evidence path.

## Secrets and time

A hashlock requires a preimage matching the committed hash. `OP_CHECKLOCKTIMEVERIFY` checks an absolute lock condition; `OP_CHECKSEQUENCEVERIFY` checks a relative one. Their interpretation follows the transaction and script rules, not an interface countdown.

Applications define branch interactions and assign the responsibility for taking an eligible path. See [recovery responsibilities](trust.md#make-recovery-an-action).

## Composition scope

A DLC construction can combine funding, outcome branches, external attestation and timed recovery. A provider policy can combine templates, relative delays and recursive output constraints. The application defines the overall flow and tests the permitted and rejected spends.

Using existing operations does not require a new product category in consensus. Adding a primitive changes the shared validation language and requires specification and review. See [Composable settlement](composition.md) for the conceptual model and [Build an application](build.md) for the design workflow.
