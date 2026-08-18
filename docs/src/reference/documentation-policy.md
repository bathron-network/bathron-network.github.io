# Documentation policy

One canonical source, one status page, and a rule for what wins when texts disagree.

## Where things live

| What | Canonical location |
|---|---|
| **Public documentation** — positioning, economics, markets, Bitcoin integration, consensus, security model, status | this site: `bathron-network/bathron-network.github.io`, directory `docs/src/` (rendered at <https://bathron.org/docs/>) |
| **Implementation** — what the software actually does | the code and tests of the repository concerned: [`bathron-core`](https://github.com/bathron-network/bathron-core) (node, consensus, RPC, prototypes under `contrib/`), [`bathron-explorer`](https://github.com/bathron-network/bathron-explorer). `bathron-core` is populated by a **controlled export**: each publication is a flat commit carrying a `.PROVENANCE.txt` (source commit id, exporter version, tree hash) that lets an authorised reviewer reproduce the tree byte for byte. The development repository behind the export is not part of the public record and is not named in public documentation; `bathron-core` is the public reference of the implementation. |
| **Public status** — what runs, what is not proven, what is never claimed | [Status & claims](../consensus/status-and-claims.md) |
| **Editorial rules** — vocabulary, the two-halves permissionless sentence, forbidden claims | `docs/STYLE.md` in the site repository (not rendered) |

## What repository READMEs may contain

A README in any `bathron-network` repository contains **only** what is specific to that
repository: what the software is, how to build, install, configure and run it, its commands, and
warnings proper to that software (experimental status, network it targets, known limitations of
*that component*).

READMEs do **not** restate the protocol's positioning, the security model, the economics of M1,
the atomicity status, the roadmap or the network status. Where a reader needs those, the README
links to the canonical page. Two independent texts explaining the same protocol property is a
defect, not redundancy.

## Precedence

- On **what the software does**: the code and its tests prevail over any prose.
- On **what the protocol claims** — capabilities, guarantees, status: the
  [Status & claims](../consensus/status-and-claims.md) page prevails over every other page, README,
  release note or announcement. If another public text claims more, that text is wrong and is
  corrected; the status page is not softened to match it.
- Reference pages under [Reference](transaction-types.md) describe the current implementation;
  where they lag the code, the code prevails and the page is fixed.

## Historical documents

Documents written for an earlier framing or an earlier network are **archived, not deleted**:
they carry an explicit "archived" banner with the date, state what has since changed, and are
removed from the main navigation. They are not a current reference. Examples on this site: the
[essay](../essay.md) and its [French version](../essai-fr.md); in `bathron-core`, the
signet-era provider prototypes and burn tool under `contrib/`.

## Public claims must be traceable

Every public statement about BATHRON must be attributable either to the code of a
`bathron-network` repository or to a page in `docs/src/`. Public documentation never depends on
private notes, internal rules, local files or unpublished documents; if a claim rests only on
such a source, it is not made.

## Reporting a discrepancy

Open an issue on the site repository for documentation, or on the repository concerned for
implementation. Security-relevant discrepancies go to security@bathron.org first
(see [Security model](../consensus/security-model.md#reporting-a-vulnerability)).
