# BATHRON editorial style — v4

Not rendered on the site; public in this repository.

This guide applies to the documentation, homepage, metadata and image text. Explain the reader's decision before introducing the mechanism. Use the same terms for the same responsibilities throughout.

## Sources and scope

PUB-1 adds two factual transparency pages: Known limitations and How this project is built.
They use a **Sources** block, separating public specification evidence from project-owner statements.
Known limitations may summarise the canonical network status, the dated shutdown, open qualification
in WHY-N §9, and the bootstrap signature threshold. How this project is built may identify the AI
models used and the commitment to publish bootstrap key holders. The homepage adds only the requested
network-status sentence and links beneath the hero buttons, using an existing CSS class.
Exact-line and exact-sentence exceptions in the check lists document these narrow permissions;
the general vocabulary and confidentiality rules still apply elsewhere.

1. **Keep each source in its role.** N-SPEC defines engine rules. The application specification defines its application scope. Network status belongs to the canonical Status page. Documentation explains the sources through conceptual summaries with section references. Do not duplicate parameter values, depth tables, measurements, qualification results, dates or network conditions.
2. **Identify the source at the top.** Each explanatory page starts with the source block below. Use a single pinned revision of n-spec for every normative link. That revision must contain all cited documents. An unresolved reference or an absent public source prevents publication.
3. **Link to Network status.** The documentation theme, homepage and repository entry points link to the canonical page. Do not repeat its contents in prose, metadata or images. Do not add another status paragraph to individual documentation pages.
4. **Write in the present tense.** Describe the documented rules and their boundaries. Keep schedules, release plans and development announcements out of these pages.
5. **Give each concept a home.** Explain production in Producers and tickets, chain selection in The N engine, delivery depth in Depth and statuses, burns in Burns, and service responsibilities in Who does what. Other pages summarize and link.
6. **Stay within public source scope.** Cite N-SPEC v0.7, WHY-N §§1–8 and ATTACKS for the engine and its boundaries. For Capabilities, cite the adopted parts of APP-SPEC v1 draft §BTC, §SCR, §13, §R2P, §OBJ.3 rule OBJ-10 and §PUB, as well as §0.3 rule GEN-5; retain §0.4 and §ID rule ID-1. Burns may also cite §IMP.1, §IMP.4 and §OBJ.2 for eligible import and existing M0 transfers. Cite the precise subsection where one exists. Explain reserved details as reserved, never as available functionality; difficulty markets are compatible by design (header facts verified by each node, plus covenants), without an oracle, and the exact difficulty query format is not yet published (BTCSTATE-3). Present recursive covenants and DLCs as outside the documented baseline, with the SCR-2/CTV-1 basis explicit. Every construction is a third-party example that distinguishes protocol primitives from builder responsibilities. The word “oracle” is permitted only to explain a dependency external to the protocol, chosen by a builder; it must never describe Bitcoin evidence verification. The homepage keeps its presentation: source comments cite the corrected agreement, and its links lead to the explanatory pages.
7. **State limits with evidence.** Refer readers to [N-SPEC v0.7 §18][n18] and [ATTACKS][attacks] for limitations. Explain consequences relevant to the reader without reproducing vulnerability details or research results. Keep a domain qualification beside any conditional claim. Never turn a halt mechanism into an assurance that every conflict is detected.
8. **Use a predictable structure.** Title, source block, a paragraph explaining why the topic matters, body, then See also. Use sentence case. Explanatory pages contain 350–600 words; the glossary may extend to 900 and needs no opening rationale.
9. **Use restrained language.** Write declarative sentences and short paragraphs. Prefer concrete responsibilities to slogans. Avoid superlatives, promotional adjectives, unsupported comparisons and universal promises. Distinguish a rule, a local observation and a model result.
10. **Keep illustrations subordinate to the text.** Use small SVG illustrations and the existing theme palette. An image must not add a mechanism absent from the prose. Apply the same source and terminology rules to labels, captions and alternative text. Do not put parameter values or status statements in images. Remove an illustration that no longer explains a retained section.

Use this source block, replacing the references with links to the sections that support the page:

> **Normative source:** N-SPEC v0.7 §x.y; WHY-N §n; APP-SPEC v1 draft §x, where applicable.
> This page explains; it does not restate rules or parameter values.

Put a section citation immediately after the claim or paragraph it supports. The opening source block does not substitute for claim-level references. Keep public document locations in links, not in reader-facing explanations.

## Vocabulary

| Use | Avoid in prose | Meaning and boundary |
|---|---|---|
| **M0, the settlement asset** | M1, pivot, settlement pivot, currency, money, coin, token, backed by Bitcoin, peg, par, buy/invest in M0, numéraire, yield, APY | Describe its Bitcoin origin without implying backing, a price floor or a financial return. [APP-SPEC v1 draft §0.4][p04]; [N-SPEC v0.7 §4.9][n49] |
| **BTC/M0, X/M0** | Historical asset pairs; apply the M0 vocabulary above | The asset-pair notation of the application reference. [APP-SPEC v1 draft §0.4][p04] |
| **Registered identity** | Operator except for the single glossary mention; masternode, validator as a role, stake, staking | The identity associated with registered keys and ticket rights. [N-SPEC v0.7 §4.1][n41], [§4.6][n46] |
| **Producer** | Committee, quorum, vote, voting except in sourced negations; apply the identity vocabulary above | The registered identity drawn for a production slot. [N-SPEC v0.7 §7.1][n71] |
| **Ticket** | Stake, staking, refundable deposit; slashing except in the required negation | An entry right, neither refundable nor transferable. [N-SPEC v0.7 §1.4, invariants 3–4][n14] |
| **Settlement Provider (SP), Liquidity Provider (LP)** | Clearing Provider, member, administrator, identity required, market maker chosen by the protocol | Service responsibilities, distinct from block production; identify the party choosing delivery depth. [APP-SPEC v1 draft §0.4][p04], [§R2P, R2P-1][pR2P]; [WHY-N §7][w7] |
| **Settlement, settles, asset conversion, conversion rate, asset pair, settlement inventory, inventory movement** | Swap, exchange, trade, trading, exchange rate, trading pair, DEX, DLP, liquidity pool; message exchange and key exchange remain ordinary technical expressions | Use these terms consistently for services and asset movements. |
| **Inclusion, depth, status, stable under your policy** | Final, finality, finalized except in negation; confirmed as an absolute, safe, guaranteed except in negation, instant, real-time | Keep the policy and domain visible. Do not turn these into unconditional assurance labels. [N-SPEC v0.7 §14.5][n145], [§17.3][n173] |
| **Burn** | Reserve, redeem, redeemable or a claim on Bitcoin except in negation; mint, issuance | Irreversible destruction, with no reserve and no claim on Bitcoin. [N-SPEC v0.7 §4.9][n49]; [WHY-N §3][w3] |
| **Bitcoin facts, reference block** | Oracle as a protocol service; feed, latest Bitcoin tip | Evidence checked in the block's designated Bitcoin context. [N-SPEC v0.7 §8.4][n84] |
| **STOP, RECOVERY** | Never be wrong without the published-domain qualification; unstoppable, 100% uptime | Preserve technical spelling and distinguish a halt from explicit acceptance of a new origin. [N-SPEC v0.7 §12.1][n121], [§12.14][n1214] |

Use only the current role names. The glossary keeps one historical mention: *formerly called Operator*. This is the only permitted use of the former role name in reader-facing copy. Do not call a producer's ticket a recoverable deposit. Do not apply financial promotion language to M0 or promise universal protection to participants.

Keep fixed technical identifiers unchanged when explaining an identifier is in scope. Explain settlement-lock identifiers only when needed; do not reproduce payloads or parameter values. “Covenant-linked parent contract” describes the construction; never describe M0 as a pivot. Link to the application status definitions without translating or reproducing their list.

## Required wording

These formulations are fixed for this set of pages. Preserve their adjoining source references and qualifications.

**Producers and tickets**

> A ticket is an entry right, never a guarantee.

[WHY-N §2][w2]; [N-SPEC v0.7 §1.4, invariants 3–4][n14]

> Proven equivocation bans the identity permanently. There is no slashing: the ticket was spent at entry, not seized.

[N-SPEC v0.7 §10.1][n101], [§10.3][n103]. Explain proof admissibility and maturity immediately before this statement.

**The N engine**

> One producer per slot, drawn from burned tickets with a Bitcoin-derived seed. No committee, no quorum, no vote, no finality gadget.

[WHY-N §2][w2]; [N-SPEC v0.7 §5.3][n53], [§5.4][n54], [§7.1][n71]

**Depth and statuses**

> There is no native finality. N offers inclusion and depth. Each participant chooses a depth from the published table, within the published domain. Outside it, N makes no quantitative claim.

[N-SPEC v0.7 §1.4, invariant 18][n14], [§17.3][n173], [§17.6][n176]

**BATHRON in five minutes; Where trust lives**

> There is no native finality.

[N-SPEC v0.7 §1.4, invariant 18][n14], [§18][n18]. Include this sentence once on each page and link to Depth and statuses.

**Depth and statuses; Where trust lives**

> Wait or stop rather than be wrong. A settlement may wait hours; the network may pause to resolve a conflict.

[N-SPEC v0.7 §14.4][n144], [§18][n18]; [WHY-N §7][w7], [§8][w8]. Follow it with the domain qualification and the absence of a universal conflict-detection claim.

**Burns**

> New M0 comes only from eligible burns imported under the rules.
> Using M0 does not require burning BTC.
> Every M0 unit comes from burned bitcoin. A burn creates no reserve and no claim on Bitcoin.

[APP-SPEC v1 draft §IMP.1][pIMP1], [§IMP.4][pIMP4], [§OBJ.2][pOBJ2]; [N-SPEC v0.7 §4.9][n49]; [WHY-N §3][w3]. Put use of existing M0 before its origin; distinguish M0, TICKET and REACT burns.

**Where trust lives**

> BATHRON reads Bitcoin; it never commands it.

[N-SPEC v0.7, preamble, point 3][np]

**Who does what**

> N-SPEC v0.7 keeps a historical application wording that was never adopted for any network. APP-SPEC v1 makes M0 the only settlement asset; its §13 differs from N-SPEC v0.7 §13 only in the asset.

[APP-SPEC v1 draft §13, principle][p13], [§ID, ID-1][pID]. Keep the reader-facing explanation on this page only, at the first mention of BTC/M0. Do not spell out the historical asset identifier or link to the engine's settlement chapter. The historical wording does not describe an earlier name for M0.

> Independent liquidity providers settle with each other on M0, without trusting one another. The specifications define no order book and no pool.

[APP-SPEC v1 draft §R2P, R2P-1][pR2P] supports settlement without mutual trust; the absence of an order book or pool summarizes the specifications, not an explicit rule in R2P-1. Keep this statement within the service-role explanation and retain the delivery-depth dependency.

## Editorial checks

Check entire sentences and their context. Negative statements about consensus mechanisms and the entry-right qualification must remain readable. Do not remove them merely because a term appears in a search result. Treat technical identifiers separately from prose. Check rendered text separately from link destinations: a word in a source URL is not an editorial use. This guide may name prohibited terms to explain the restrictions. On the homepage, retain the exact sourced sentence “N selects one producer per slot from burned tickets, without a vote.” as the sole exception to the page restriction on consensus negations.

Read every quantity, including quantities written in words and values without units. Section numbers, versions and page numbering identify references; they are not parameters. The singular producer per slot and the qualitative possibility of waiting hours explain the model. They do not authorize copying slot durations, burn amounts, maturities, depths or performance claims. The sole additional exception is PUB-2’s approximate two-to-four-hour scale on the settlement page, explicitly sourced and never presented as a deadline.

Check all visible text, metadata, source links, internal links, captions and alternative text. Match the page title and social title exactly to the homepage hero. Use the same approved description in page and social metadata. Keep the Network status link as navigation, without an accompanying network-state claim.

[n18]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#18-limites
[attacks]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/ATTACKS.md
[p04]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés
[n49]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#49-burn-m0-v3
[n41]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#41-identité
[n46]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#46-new-et-add
[n71]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#71-tirage
[n14]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#14-invariants
[pR2P]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants
[w7]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#7-why-sps-and-lps-choose-their-own-depth
[n145]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#145-statuts-applicatifs
[n173]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#173-table-kε-du-domaine
[w3]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#3-the-property-split
[n84]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#84-repère-bitcoin
[n121]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#121-nature-de-h1
[n1214]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1214-récupération-exceptionnelle
[w2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#2-why-n-exists
[n101]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#101-preuve-déquivoque
[n103]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#103-ban
[n53]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#53-registre-actif
[n54]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#54-graine
[n176]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#176-comportement-hors-domaine
[n144]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#144-suspensions-sans-attaque
[w8]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#8-what-n-guarantees-under-h_n-and-what-it-does-not
[np]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#préambule
[p13]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#13-règlement-btcm0-à-un-saut
[pID]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#id-identifiant-applicatif-application_spec_id
[pIMP1]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#imp1-source-unique
[pIMP4]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#imp4-matérialisation
[pOBJ2]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#obj2-transaction-applicative-application_transaction
