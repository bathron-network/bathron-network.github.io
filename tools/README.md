# Documentation checks

Run `bash tools/docs-check.sh --offline` with the pinned mdBook executable on
PATH. The script installs nothing and makes no network request. It builds all
homepages and the book, then checks the resulting internal links and fragments,
direct redirects, referenced images, sitemap, confidentiality and vocabulary.
Every gate has a sandbox mutation test in `mutation-test.py`; a nominal fixture
must pass before a deliberately broken fixture is accepted as a successful test.
`bash i18n/ci-check.sh` remains the separate translation gate.

## Normative revision

`docs/NSPEC_REF` contains one full git commit hash, with optional comment lines.
TODO-REF and the literal REF are unresolved placeholders, so the source gate
fails even in offline mode. Replace REF in the revision file and every normative
URL after the application source is merged. Remove the TODO comment at that time.

Set `NSPEC_DIR` to a local n-spec git checkout containing that exact commit.
The checker uses `git show` at the pinned commit, never the working tree or a
branch tip. It checks source files, heading anchors, application citation scope,
the presence of the curated application specification and historical wording
exceptions. It never fetches. CI obtains the pinned checkout in a separate step.
External websites other than those normative sources are not probed.

`nspec-oldname-exceptions.txt` scopes each historical wording exception to a
public source section and the page citing it. The homepage entries also apply
to its generated translations. The historical explanation is confined to Who
does what and the editorial guide. The engine settlement chapter is never citable.

## Contextual vocabulary

`vocab-check.py` checks sentences, ignoring code and URL destinations. It checks
English catalogue keys, visible HTML, metadata, alternative text, SVG text,
documentation and both entry-point READMEs. The editorial guide is excluded
because it records prohibited terms as examples. Exceptions in `vocab-allow.txt`
require an exact page, rule, sentence and reason. Citation identifiers that look
like quantities have individually scoped exceptions.

The quantity rule cannot recognize all numbers written in words or parameter
values without units. Human review must inspect every quantity, including these
cases. Translation meaning also requires human review. Automated negation checks
do not establish whether a sentence is true or properly sourced.

## Public confidentiality and metadata

`confidentiality-check.py` scans all tracked files still present, including
catalogues and source code. It also scans untracked, non-ignored files so new
files are checked before staging. Generic patterns detect addresses, personal
paths, unapproved email addresses, numbered host labels, model/tool names and
internal document markers. They cannot identify arbitrary private names or
host aliases. The private-name review runs separately, outside this repository.
No private-name list belongs in this tree.

Each public exception has a file, matched text, complete exact line and reason
in `confidentiality-allow.txt`. Stale exceptions fail. Synthetic forbidden inputs
are assembled only inside temporary mutation fixtures.

For a pull request, set `DOCS_BASE` and `DOCS_HEAD` to full commit hashes and
`DOCS_BRANCH` to its source branch. The metadata check requires the branch to
match `docs/…` and both author and committer to be `BATHRON <dev@bathron.org>`
for every commit in the range. An offline working-tree check without a PR range
reports this check as not run; it does not certify PR metadata.

The PR job has the stable name `docs gates` and no path filter, so branch
protection can require it for every pull request. The deployment workflow calls
the same entry point before site assembly. Actions, Python and mdBook use the
existing pinned versions and digest. Updating those pins requires checking both
workflows together.
