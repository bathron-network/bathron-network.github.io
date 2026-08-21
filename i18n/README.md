# Homepage i18n — one source, versioned catalogue, fail-closed

The homepage exists in one place only: **`index.html`**. It is both the structure
and the English text, and it is the page served at `/`. There is no second HTML
file to keep in sync, because a second file is exactly what drifts.

French is a **catalogue of strings**, not a copy of the page:

```
index.html                 source of truth (structure + English)
i18n/homepage.fr.po        French catalogue     (hand-maintained, versioned)
i18n/homepage.pot          extracted template   (generated, NOT versioned)
fr/index.html              generated artifact   (generated, NOT versioned)
```

Only two files are versioned inputs. The `.pot` is a pure function of
`index.html`, regenerated before every `msgmerge` and again in CI; committing it
would create a second thing to keep in sync, which is what this design removes.

## Commands

```bash
bash   i18n/ci-check.sh          # ALL the gates, in order — what CI runs
```

That script is the single definition of "the i18n gates". Both workflows call
it, so the checks guarding a pull request and the checks guarding a publication
cannot drift apart. It needs Python 3 and git; it installs nothing, downloads
nothing and reads no secret.

Individually:

```bash
python3 i18n/i18n.py extract     # refresh homepage.pot from index.html
python3 i18n/i18n.py check fr    # audit the catalogue; exit non-zero if anything is off
python3 i18n/i18n.py build fr    # generate fr/index.html; refuses unless 100 % complete
python3 i18n/i18n.py verify fr   # lang, canonical, og:url, hreflang, selector, HTML balance
python3 i18n/i18n.py compare     # EN and FR must share one tag skeleton
python3 i18n/i18n.py static-overflow-check   # see the caveat below
python3 i18n/test_i18n.py        # unit tests
bash   i18n/mutation-test.sh     # prove the fail-closed guarantee, in a sandbox
bash   i18n/msgmerge-compat.sh   # OPTIONAL, needs GNU gettext — see below
```

### `static-overflow-check` is not a rendering check

It scans the markup for fixed pixel widths wider than the smallest supported
viewport. It does not lay the page out, does not resolve the cascade, and cannot
see a long unbreakable word, a wide flex item or an oversized image. A clean
result means *no fixed width certain to overflow was found* — never *the page
renders correctly*. Looking at the page in a browser at desktop and mobile
widths remains a **local editorial step**, and screenshots taken that way are
review material, not evidence produced by CI.

### `msgmerge-compat.sh` is optional and off the deployment path

The fail-closed guarantee is proven by `mutation-test.sh`, which injects the
`#, fuzzy` flag deterministically and therefore needs Python only. Publishing
the site must not depend on the Ubuntu archives being reachable, so **nothing on
the deploy path runs `apt-get`**.

`msgmerge-compat.sh` answers a separate, narrower question — does the strict PO
reader still understand what a *real* `msgmerge --update` writes? It runs
locally on demand, and in CI as a **non-blocking** job that cannot stop a pull
request or a publication. It exits `77` when gettext is absent.

## Workflows

| Workflow | Trigger | Permissions | Deploys |
|---|---|---|---|
| `.github/workflows/i18n-check.yml` | every `pull_request` | `contents: read` only | never |
| `.github/workflows/deploy.yml` | `push` to `main` | `contents: read`, `pages: write`, `id-token: write` | yes |

Both run `bash i18n/ci-check.sh`. The PR workflow requests no Pages permission,
no `id-token`, reads no secret and uploads no artifact — it exists purely to
judge a branch by the same gates that will later guard `main`.

### Why the PR workflow has no `paths:` filter

A check that is *skipped* for some pull requests cannot safely be made
required: GitHub reports a skipped required check as pending, and the branch
never becomes mergeable. So the job runs on **every** pull request under one
stable name — `i18n gates` — and decides internally whether any i18n file
changed. When none did, it says so and succeeds without running anything. The
check can be made required without stalling unrelated pull requests.

Making it required is a repository setting and is **not** applied here.

### Pinning

Every action is pinned by commit SHA — no mobile tags anywhere. Each SHA was
confirmed through `GET /repos/<owner>/<repo>/git/ref/tags/<tag>`, which returns
the commit a tag points at:

| Action | Tag | Commit |
|---|---|---|
| `actions/checkout` | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` |
| `actions/setup-python` | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| `actions/upload-pages-artifact` | v3.0.1 | `56afc609e74202658d3ffba0e8f6dda462b719fa` |
| `actions/deploy-pages` | v4.0.5 | `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` |

Each is the newest release of the major line already in use, so pinning changed
no behaviour. Python is pinned to 3.12.14 and **asserted at runtime**, so a
silent interpreter drift fails the job instead of passing unnoticed.

## Portability, and one lesson

The shell scripts run on the Bash 3.2 that macOS ships as `/bin/bash`, as well
as on Bash 5. No associative arrays, no `mapfile`, no `${var^^}`, and no
`sha256sum` — a stock macOS has none of those. Hashing goes through Python,
which is already a hard dependency.

This matters because it went wrong. An earlier `mutation-test.sh` used
`declare -A`. On Bash 3.2 that fails, the guarded-file comparisons then never
ran, and the script still printed `MUTATION TEST: PASS` and exited 0 — a test
that reported success precisely because it had not run.

Two defences now make that impossible:

- **`die()` on any harness error** — hashing, sandbox creation, copying, a
  missing anchor — exits 3 with `FAIL (harness error)`, never PASS.
- **Completeness counters.** The script counts the steps and assertions it
  actually executed and refuses to print PASS unless both reach their expected
  totals. `die()` cannot catch a check that silently does not run; the counter
  can, and a regression test injects exactly that fault to prove it.

`BATHRON_MUTATION_TEST_FAULT` injects failures at five points — `manifest`,
`sandbox`, `copy`, `guard`, `skipguard` — and `test_i18n.py` asserts that each
one exits non-zero and never prints PASS, on top of a static scan that fails the
suite if a Bash 4-only construct or `sha256sum` reappears in any script.

### Sandbox bounding

The sandbox is created as `${TMPDIR:-/tmp}/bathron-i18n-mutation.XXXXXX` — a
template both GNU and BSD `mktemp` handle — and a marker file is written inside
it. Cleanup removes **only** the exact path `mktemp` returned, and only if it
still matches that template *and* still carries the marker. A directory that
matches the prefix but was not created by this run is left alone; a test plants
exactly such a decoy and asserts it survives.

## The guarantee

`build` refuses to write anything unless **every** source string has a non-empty,
non-fuzzy translation, and it deletes any previous `fr/index.html` *before*
validating. Since the artifact is never committed, there is no stale copy
anywhere to fall back on. The page is written to a temporary file in the target
directory, fsynced, then moved into place with `os.replace`, so an interrupted
process leaves either the previous page or none — never half a page.

Conditions that block a build:

| Condition | Meaning |
|---|---|
| `MISSING` | the English string has no entry in the catalogue |
| `EMPTY` | the entry exists but `msgstr` is empty |
| `FUZZY` | `msgmerge` flagged it — the English changed, the French did not |
| `OBSOLETE` | the catalogue holds an entry the page no longer contains |
| `CATALOGUE` | the `.po` is malformed, ambiguous, duplicated or for another language |

`mutation-test.sh` proves this by execution: it copies the sources into a
throwaway sandbox and exercises a changed English sentence, an absent catalogue,
a `fuzzy` entry produced by real `msgmerge`, a duplicated entry and a malformed
entry — checking each time that the build refuses *and* that no French page
survives on disk. It then asserts, by SHA-256 and by `git status`, that the
calling worktree was never written to. An argument is not a proof; run the test.

## Changing English text

```bash
#  1. edit index.html
python3 i18n/i18n.py extract
msgmerge --update --backup=none i18n/homepage.fr.po i18n/homepage.pot
#  2. the changed entry is now marked #, fuzzy
#  3. fix the msgstr, delete the fuzzy line
python3 i18n/i18n.py check fr
```

Until step 3 is done, `/fr/` cannot be deployed. That is the point: the French
page is either current or absent, never quietly wrong.

## Disambiguation

When one English string needs two different French renderings, wrap the element:

```html
<p class="memorable" data-i18n-context="hero">Programmable settlement<br>…</p>
```

That becomes the gettext `msgctxt`. Context is **explicit** on purpose: deriving
it from CSS class names would mark the whole catalogue fuzzy the day someone
renames a class for styling reasons.

### Context metadata — what is actually true

`data-i18n-context` is stripped from every **generated** page, so it never
appears in `fr/index.html`; `verify fr` fails if it ever does. The **English
page is not generated** — it is `index.html`, served as-is — so it **keeps the
attribute**.

That is a deliberate choice between two models:

1. *Serve `index.html` directly and let the attribute stay.* `data-*` is valid
   HTML5 and inert: no styling, no script, no behaviour, a handful of bytes.
2. *Generate an English publication copy with the attribute removed.* Cleaner
   output, but it makes English an artifact too, adds a build step that can
   fail, and means the file a reader edits is no longer the file that ships.

Model 1 was chosen: keeping the served English page identical to the source file
is worth more than removing an inert attribute. The attribute also documents
itself where the translator will actually look. Should the page ever grow many
contexts, model 2 remains available without changing the catalogue.

## What is not translatable

`<style>` and `<script>` contents are never extracted. Among attributes, only
prose is: `img/@alt`, `a/@title`, and the `<meta>` tags carrying real sentences
(`description`, `og:title`, `og:description`, `twitter:title`,
`twitter:description`). `viewport`, `og:image`, `twitter:card` and friends are
structural and stay out of the catalogue.

Per-language facts — `<html lang>`, the canonical URL, `og:url`, and the EN/FR
selector — are not prose either. They live in `LANG_CONF` in `i18n.py` and are
applied by count-checked substitution: if one of them stops matching exactly
once, the build fails rather than emitting a page with a wrong canonical or no
language selector.

### The language menu

Six languages are published: English `/`, Français `/fr/`, Español `/es/`,
中文（简体）`/zh-hans/`, हिन्दी `/hi/`, العربية `/ar/`. The BCP 47 tag and the URL
are deliberately separate — `zh-Hans` is the tag, `/zh-hans/` is the path.

The menu is a native `<details>`, no JavaScript:

```html
<nav class="langsel" aria-label="Language selection">
  <details class="langmenu">
    <summary><svg …globe…/><span class="lm-current">English</span><svg …chevron…/></summary>
    <ul class="lm-list">
      <li><span class="lm-item lm-on" aria-current="page" lang="en">…EN…English</span></li>
      <li><a class="lm-item" href="/fr/" lang="fr" hreflang="fr">…FR…Français</a></li>
      …
    </ul>
  </details>
</nav>
```

It opens on click and on Enter/Space, because that is what `<summary>` does. A
language switcher that needs a script is a switcher that can fail.

The active language is a `<span>` carrying `aria-current="page"` — never a link
— and is **filled** rather than tinted, so it reads without relying on hue. The
badges (`EN`, `FR`, `ES`, `简`, `हि`, `ع`) are `aria-hidden` decoration: the
native name is always written out, and no flag ever carries meaning on its own.
The globe and chevron are inline SVG rather than emoji, whose rendering depends
on the system font.

`selector_html()` builds the whole `<nav>` from the table, so it is not prose
and never reaches a catalogue: "Français" is Français in every language. The
`langsel` class is in `SKIP_CLASSES`, which keeps the extractor out of that
subtree entirely.

### Right-to-left

Arabic is served as `<html lang="ar" dir="rtl">`; every other language carries
no `dir` at all. The layout needed almost nothing for this: the page uses
centred text, flex and grid, with no physical `left`/`right` anywhere. The one
rule that mattered is the dropdown panel, which uses `inset-inline-end: 0` so it
hangs off the correct edge in both directions.

`verify` checks the exact `<html>` tag per language, so a missing or stray
`dir` fails the build.

## Adding a language

The machinery is extensible; publishing is deliberate. A language appears in
the menu only once its catalogue is complete, because the menu is generated
from the same table the build uses — there is no way to list a language that
does not build.

1. **Declare it** in `LANGUAGES` in `i18n/i18n.py`: `code` (BCP 47), `name`
   (native), `path` (public URL), `out` (output directory, lowercase), `dir`,
   `badge`, `label` (the localised accessible name of the menu).
2. **Create the catalogue** `i18n/homepage.<code>.po` with a `Language:` header
   matching the code, and translate every string. Nothing else is accepted:
   a missing, empty, fuzzy, duplicated or malformed entry blocks the build.
3. **`python3 i18n/i18n.py check <code>`** until it reports zero problems.
4. **`python3 i18n/i18n.py build <code>`** to generate the page.
5. **Add the output directory to `.gitignore`** — generated pages are never
   committed — and add the URL to `sitemap.xml`. The `hreflang` set and the
   menu update themselves from the table.
6. **Run `bash i18n/ci-check.sh`.** The language ships only when every gate
   passes; `verify` will refuse a page whose menu, canonical, `hreflang` or
   `dir` disagrees with the table.

Do not add an empty catalogue for a language you are not ready to publish. A
declared language with no catalogue fails `check` and `build`, which is the
intended behaviour — but it also fails the whole deploy, so declare and
translate in the same change.

## Language and path bounding

`build`, `check` and `verify` validate the language **before** computing any
path and before touching the filesystem. The regex is a shape check only; what
actually authorises a language is membership in `LANGUAGES` — an allowlist,
never a pattern, so a well-formed BCP 47 tag nobody declared is refused like any
other unknown string. English is the source, not an output. Output and
catalogue directory names come from the **table**, never from the argument, so
a caller cannot steer the path even if validation were somehow bypassed.

`python3 i18n/i18n.py build ../../x` therefore fails before a single file is
opened, created or removed. The unit tests assert this with spies on `open`,
`os.remove`, `os.makedirs`, `os.replace` and `tempfile.mkstemp`, and with a
sentinel file outside the repository whose size, mtime and contents must be
unchanged.

## The strict PO reader

The reader is deliberately unforgiving, because a silently overwritten entry is
a silently wrong page. It rejects: duplicate `(msgctxt, msgid)` pairs; repeated
`msgid`/`msgstr`/`msgctxt` within one entry; `msgctxt` after `msgid`; `msgid`
after `msgstr`; a continuation string with nothing above it; any unrecognised
non-comment line; invalid or dangling escapes; entries missing a `msgid` or a
`msgstr`; a missing or duplicated header; obsolete `#~` blocks; flags attached
to no entry; and a catalogue whose `Language:` header does not match the
requested language. Nothing is ever written into a dictionary key twice.

If this parser ever needs to grow beyond the homepage, replace it with a mature
library pinned by version *and* hash rather than loosening it.

## Why not po4a

po4a was evaluated first and rejected on evidence, not taste. With the version
packaged for this machine (`po4a 0.73`), its xhtml module:

- rejects `<!doctype html>` in lowercase — valid HTML5 — with a parse error;
- reformats the document, reflowing the `<style>` block (65 lines → 55) so the
  round-trip diverges by 216 lines;
- puts **the entire CSS block into the catalogue as one `msgid`**.

That last one is fatal here: under a 100 %-or-nothing rule, changing a colour
would mark the CSS entry fuzzy and break the French build. The generator in this
directory uses only the Python standard library, which is also why the deploy
workflow installs nothing to build the page. `gettext` is installed in CI for
the *test* alone: the fuzzy case must run against real `msgmerge` output rather
than a hand-written imitation of it.

## Scope

The homepage only. The mdBook documentation under `docs/` is English and is not
touched by this system; the French homepage says so where it links to it.
