# Known limitations

> **Sources:** [Network status](status.md), [n-spec public README][nsreadme], [WHY-N §1][w1], [§4][w4], [§9][w9], [N-SPEC v0.7 §14.2][n142], [§15.8][n158], [§12.11][n1211], and [APP-SPEC v1 draft status][appstatus].
> This page records the current limits and the conditions still to be met.

## Network and implementation

No public network runs today. The DMM public testnet was shut down on 5 October 2026. A network using N is under construction, with no announced date. [Network status](status.md) is the canonical record of network availability.

There is no public implementation of N. The public Core repository contains legacy DMM software; it does not implement the N specification. [n-spec public README][nsreadme]

## Application and qualification

APP-SPEC v1 is a draft. Gate RA has not been passed, and it authorises no genesis. Byte-level formats and independent generator vectors are still due; reserved or unpublished provisions are not available implementation rules. [APP-SPEC v1 draft status][appstatus]; [application identifier reservations][pid]

Qualification remains open under QR-1…QR-10. These requirements cover real-client measurements, delay assumptions, analytical bounds and proof composition, model exploration, delivery checks, Bitcoin seed grinding, recovery, anchor compatibility and client profiles. The published architecture is a candidate, not a qualified system. [WHY-N §9][w9]

No external audit has been completed. Independent human review is still needed; an external audit is a precondition before any public network carries value. See [How this project is built](how-this-project-is-built.md).

## Initial production and exposure

Producers are managed by the project at startup. In that initial phase, no bound β < 1 on adversarial production weight is defensible: a burn has a cost, but it bounds neither concentration, key rental, corruption, coercion nor attrition. N makes quantitative claims only inside its published domain H_N, which assumes a bound on adversarial weight; this initial arrangement cannot substantiate that assumption. [WHY-N §1][w1]; [n-spec public README][nsreadme]

Real external exposure is zero at bootstrap. Any later exposure limit requires an applicable, published risk bound, and deliveries affected by the same reorganisation must be considered together. [N-SPEC v0.7 §14.2][n142], [§15.8][n158]

## Authenticated origin

Initialisation depends on a signed `BOOTSTRAP` package authenticated by a 3-of-4 release-key threshold. This is weak subjectivity: a new or long-absent node needs a recent authenticated origin before the published registry-agreement claim applies. An origin has no fork-choice power over a synchronised node. [WHY-N §4][w4]; [N-SPEC v0.7 §12.11][n1211]

## Language of the specification

The normative N specification is in French. These English pages explain it; they do not replace the normative text. The application draft is also in French. [n-spec public README][nsreadme]

## See also

[Network status](status.md), [How this project is built](how-this-project-is-built.md), [Where trust lives](trust.md), and [Depth and statuses](depth.md).

[w1]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#1-what-was-abandoned-and-why

[w4]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#4-weak-subjectivity

[w9]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/docs/WHY-N.md#9-qualification-reserves-qr-1--qr-10

[n142]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#142-livraison

[n158]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#158-exposition

[n1211]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/spec/N-SPEC-v0.7.md#1211-politique-release

[nsreadme]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/README.md

[appstatus]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#statut-et-portée

[pid]: https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#id-identifiant-applicatif-application_spec_id
