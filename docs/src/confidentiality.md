# Private inventory transfers

A provider's inventory and payment sizes reveal commercial information. Publishing every amount can expose a business's capacity, customer activity and negotiating position. Private inventory transfers let participants limit that disclosure while retaining verifiable accounting.

BATHRON provides shielded transfers of M0, its base unit. Cryptographic proofs let nodes verify the transfer rules and conservation without publishing the protected amounts. Confidentiality changes what observers can read; it does not remove validation.

## Define what is protected

A useful privacy description names the transaction and the information it conceals. In a shielded M0 transfer, protected payment details are not published. HTLCs, covenants, lock/unlock and burn operations are transparent, as are M1 receipt transfers and Bitcoin payment evidence.

An application therefore describes confidentiality by operation. It distinguishes private transfer details from publicly verifiable conditions and from information disclosed to the counterparty.

Shielded M0 transfers can move inventory before or after settlement. See [Where trust lives](trust.md#privacy-and-economic-boundaries) for the limits of this protection.

## Follow the whole information path

| Surface | Who can learn information |
|---|---|
| Shielded M0 transfer | Participants retain their payment details; public verification uses proofs |
| Signed quote | The recipient and any service to which it is forwarded can read its terms |
| Conditional leg or M1 receipt transfer | Observers can inspect public amounts and encoded conditions |
| External asset leg | Visibility follows the external chain and transaction format |
| Application records | Access follows the application's storage and disclosure policy |

A relay can see the quotes it carries. A counterparty knows the agreement it accepts. A monitoring service sees the data it receives. These are separate disclosure choices from the transaction's cryptographic privacy.

## Keep accounting and reporting distinct

Consensus verifies conservation. It does not need to publish every participant's balance to do so. Participants still need their own records to distinguish available inventory, committed funds, fees and completed transfers.

A provider can supply evidence of its service history without publishing every customer's details. Applications should state which observations support that history and which details remain private. Reputation is an interpretation of evidence by users or services, not a protocol score.

When designing a confidential flow, trace one payment from quote to receipt. Identify each public field, each party receiving private data and each record retained for recovery. Select the transaction format for each step explicitly.

See [RPC and transactions](rpc-transactions.md) for the separation of transfer families and [Operate a provider](providers.md) for inventory records and operational controls.
