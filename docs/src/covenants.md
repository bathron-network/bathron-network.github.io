# Covenants and timelocks

> **Normative source:** [APP-SPEC v1 draft §SCR.1][pSCR1], [§SCR.2][pSCR2], [§SCR.3][pSCR3], [§SCR.4][pSCR4], [§SCR.5][pSCR5], [§SCR.7][pSCR7].
> This page explains; it does not restate rules or parameter values.

A builder needs to distinguish constraints on an M0 spend from conditions about Bitcoin and from deadlines. The adopted script baseline combines hashes, comparisons, multisig and hashlocks with covenants, timelocks and Bitcoin presence checks. Its active set and its reserved details have different scopes. [APP-SPEC v1 draft §SCR.1, SCR-1][pSCR1], [§SCR.7][pSCR7]

## Constrain the BATHRON spend

The active covenant is `OP_TEMPLATEVERIFY`, limited to CTV-1. Its template commits to the transaction version, type, absolute lock, input count, relative delays and outputs. It also commits to the current input index and to the chain and application identifiers in the template's hash domain. These commitments constrain the transaction that spends the M0 output. [APP-SPEC v1 draft §SCR.5, CTV-1][pSCR5]

This form requires an empty Sapling bundle. It does not describe a confidential covenant construction. The exact template hash remains reserved; a richer commitment alone does not qualify an extension, and v1 defines no such extension. Builders must preserve those limits when describing a proposed contract. [APP-SPEC v1 draft §SCR.5, CTV-1–CTV-3][pSCR5]

## Two different clocks

CLTV expresses an absolute deadline in N slots. Slots follow time, whereas chain height can advance more slowly when production is sparse. The absolute-lock field, bounds and operand semantics remain reserved in the draft. The adopted unit does not supply those missing formats. [APP-SPEC v1 draft §SCR.2][pSCR2]

CSV expresses a relative delay in N links, counted from the block containing the spent output to the block containing its spend, on the branch being examined. The count is recalculated for each branch. Time-based CSV is refused, and relative delays are never counted in slots. CSV qualification remains a requirement; encoding and operand details are reserved. [APP-SPEC v1 draft §SCR.3][pSCR3]

Neither clock ensures that a participant observes a transaction or obtains inclusion before an external deadline. Censorship, unavailability and reorganisation remain relevant. A validity bound is not a delivery commitment, and the Bitcoin-height rules for §13 remain separate. [APP-SPEC v1 draft §SCR.4, SCR-5][pSCR4]

## Active and reserved capabilities

The adopted baseline marks CLTV, qualified CSV, the restricted CTV form and BTCSTATE as active. Signature-opcode decisions remain reserved. CSFS, CAT and the output-inspection opcodes listed in SCR-2 are inactive; executing them fails the script. Their activation requires an application revision. [APP-SPEC v1 draft §SCR.1, SCR-1–SCR-2][pSCR1]

Accordingly, recursive covenants and discreet log contracts (DLCs) are not capabilities offered by this documented baseline today. This is a scope limit inferred from the inactive CSFS/CAT set and restricted CTV form, rather than an additional script rule. [APP-SPEC v1 draft §SCR.1, SCR-2][pSCR1], [§SCR.5, CTV-1][pSCR5]

## See also

[Contracts on Bitcoin facts](bitcoin-facts.md), [Settlement between providers on M0](between-providers.md), and [What others can build](what-you-can-build.md).

[pSCR1]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr1-socle-actif-au-genesis
[pSCR2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr2-échéances-absolues-en-créneaux-n-cltv
[pSCR3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr3-délais-relatifs-en-liens-n-csv
[pSCR4]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr4-limites-publiées-des-délais
[pSCR5]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr5-ctv
[pSCR7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#scr7-btcstate
