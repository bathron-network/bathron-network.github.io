# BATHRON documentation

This repository contains the public explanation of BATHRON and its N engine.
The specification defines rules; these pages explain them through section references.

- [Network status](https://bathron.org/docs/status.html)
- [Documentation](https://bathron.org/docs/overview.html)
- [Normative specification](https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/README.md)
- [Application specification](https://github.com/bathron-network/n-spec/blob/4cfcb8dfcc794a8b25e132a001104ed2a389e4f9/app/APP-SPEC-v1-draft.md#04-vocabulaire-et-identifiants-gelés) (in French)

Edit the book in [docs/src](docs/src/), following [STYLE v3](docs/STYLE.md).
The homepage source is [index.html](index.html); its complete translations are in
[i18n](i18n/README.md). The book is in English.

Build and check locally with the pinned mdBook executable available:

```sh
bash i18n/ci-check.sh
bash tools/docs-check.sh --offline
```

See [the checks guide](tools/README.md) for source verification and publication checks.
The single normative revision is recorded in [docs/NSPEC_REF](docs/NSPEC_REF);
every normative URL uses that revision. The checks reject an unresolved reference.

The deployment workflow runs the same documentation and translation gates as
pull-request validation, before assembling the site. Generated pages are not committed.
