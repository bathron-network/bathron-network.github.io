# bathron.org

This repository is the **canonical source for the public BATHRON documentation**.
<https://bathron.org/docs/> is its generated mdBook rendering.

- Documentation source: [`docs/src/`](docs/src/) (edit here; nothing is hand-copied from other repos)
- Landing page: [`index.html`](index.html)
- Rendered docs: <https://bathron.org/docs/>

## Editing the docs

The docs are an [mdBook](https://rust-lang.github.io/mdBook/) (`mdbook v0.4.52`). The table of
contents is [`docs/src/SUMMARY.md`](docs/src/SUMMARY.md). To preview locally:

```bash
cd docs
mdbook serve   # or: mdbook build
```

GitHub Actions builds `docs/` and deploys it to GitHub Pages on every push to `main`
([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)); there is no manual copy step.

## Related repositories

- Node, build files and short README: <https://github.com/bathron-network/bathron-core>
- Private development (source of truth, not public): `BATHRON-V2`

One notion has one canonical page here; other pages link to it rather than duplicating text.
Do not maintain a second public documentation corpus elsewhere.
