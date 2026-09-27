# Contracts on Bitcoin facts

Some agreements concern Bitcoin itself: mining difficulty, a reached height or a confirmed payment. Requiring an outside reporter for those observations adds a role that the underlying evidence can replace. BATHRON lets contracts use Bitcoin facts verified by every node.

The commercial agreement still belongs to its participants. They choose the observation point, funding and payouts. Consensus evaluates the encoded condition, without pricing the agreement or selecting its users.

## A difficulty threshold contract

Consider two parties who agree on a distribution depending on Bitcoin difficulty at height H. One branch pays the agreed destination if difficulty is at or above threshold D. The other handles difficulty below D. Funding and output constraints bind the amounts and recipients.

The contract observes difficulty, not a miner's revenue. Revenue also depends on factors outside that predicate. Participants choose the instrument because its defined exposure is useful to them, rather than treating the predicate as a complete model of a mining business.

Difficulty predicates return pass or fail. A stepped payoff can combine several threshold branches. A linear payout requires an explicit construction; it is not implied by a single comparison. More branches also mean more contract data to review.

## A payment releases another payment

Alice and Bob can require proof of a Bitcoin payment before a BATHRON output is released. The agreement specifies the Bitcoin destination script, minimum amount and required depth. Evidence ties the relevant transaction to the accepted header view.

A covenant fixes where the released value goes. Additional authorization or a recovery path can complete the agreement. The Bitcoin predicate supplies the evidence for one condition; it does not arrange the entire operation.

This pattern links a BATHRON payment to evidence of the specified Bitcoin payment. Physical goods need a different evidence source.

## Height and time conditions

A contract can require a Bitcoin height or median-time threshold. These observations are distinct from the local machine's clock and from BATHRON transaction timelocks. Builders name the clock used by each condition so participants understand when evidence becomes usable.

Readable history follows the protocol's accepted Bitcoin view and depth rules. Applications distinguish a newly observed event from an event eligible for the agreed predicate.

## Keep the evidence boundary visible

Comparisons at separate heights can test predefined threshold combinations. They do not calculate an arbitrary difference or percentage change between the two difficulties; such a payoff needs an explicit construction. Cumulative chainwork, although used to verify headers, is not a script predicate. A conversion rate or an event on another chain needs an external attestation or a separate application mechanism.

See [Bitcoin facts in contracts](bitcoin-facts.md) for the predicate families, [Bitcoin verification](bitcoin-verification.md) for proofs, and [Script reference](script.md) for names. Show the human agreement beside those exact conditions before asking participants to fund it.
