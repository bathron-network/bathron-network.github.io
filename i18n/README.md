# Homepage i18n — one source, versioned catalogues, fail-closed

The homepage exists in one place only: **`index.html`**. It is both the
structure and the English text, and it is the page served at `/`. There is no
second HTML file to keep in sync, because a second file is exactly what drifts.

Every other language is a **catalogue of strings**, not a copy of the page:

```
index.html                    source of truth (structure + English), served at /
i18n/homepage.fr.po           Français      (hand-maintained, versioned)
i18n/homepage.es.po           Español       (hand-maintained, versioned)
i18n/homepage.zh-Hans.po      中文（简体）   (hand-maintained, versioned)
i18n/homepage.hi.po           हिन्दी          (hand-maintained, versioned)
i18n/homepage.ar.po           العربية        (hand-maintained, versioned)

i18n/homepage.pot             extracted template  (generated, NOT versioned)
fr/  es/  zh-hans/  hi/  ar/  index.html per language
                              (generated, NOT versioned)
```

The versioned inputs are `index.html` and the five catalogues — nothing else.
The `.pot` is a pure function of `index.html`, regenerated before every
`msgmerge` and again in CI; committing it would create a second thing to keep in
sync, which is what this design removes. The generated pages are never committed
either, so a language is either current or absent, never quietly stale.

| Language | BCP 47 tag | URL | Direction |
|---|---|---|---|
| English | `en` | `/` | ltr — **source** |
| Français | `fr` | `/fr/` | ltr |
| Español | `es` | `/es/` | ltr |
| 中文（简体） | `zh-Hans` | `/zh-hans/` | ltr |
| हिन्दी | `hi` | `/hi/` | ltr |
| العربية | `ar` | `/ar/` | **rtl** |

The tag and the URL are deliberately distinct: `zh-Hans` is the tag, `/zh-hans/`
is the path. Everything — output paths, catalogue paths, the menu, `hreflang`,
the sitemap check — derives from the `LANGUAGES` table in `i18n.py`.

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
python3 i18n/i18n.py languages       # the language table, as the tool sees it
python3 i18n/i18n.py extract         # refresh homepage.pot from index.html
python3 i18n/i18n.py check   all     # audit every catalogue; non-zero if anything is off
python3 i18n/i18n.py build   all     # generate every page; refuses unless 100 % complete
python3 i18n/i18n.py verify  all     # lang+dir, canonical, og:url, hreflang, menu, HTML balance
python3 i18n/i18n.py compare         # every generated page vs the English skeleton
python3 i18n/i18n.py static-overflow-check   # see the caveat below
python3 i18n/test_i18n.py            # unit tests
bash   i18n/mutation-test.sh         # prove the fail-closed guarantee, in a sandbox
bash   i18n/msgmerge-compat.sh       # OPTIONAL, needs GNU gettext — see below
```

`check`, `build` and `verify` also take a single language code:

```bash
python3 i18n/i18n.py check  ar       # one catalogue
python3 i18n/i18n.py build  zh-Hans  # writes zh-hans/index.html
python3 i18n/i18n.py verify en       # the source page counts for verify
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

For **each** language, `build` refuses to write anything unless every source
string has a non-empty, non-fuzzy translation in that language's catalogue, and
it deletes that language's previous page *before* validating. Since generated
pages are never committed, there is no stale copy anywhere to fall back on. The
page is written to a temporary file in the target directory, fsynced, then moved
into place with `os.replace`, so an interrupted process leaves either the
previous page or none — never half a page.

`build all` builds every language and returns non-zero if **any** of them fails,
so an incomplete catalogue in one language stops the deploy for all of them.
That is deliberate: five languages that disagree about what the site says are
worse than a deploy that did not happen.

Conditions that block a build:

| Condition | Meaning |
|---|---|
| `MISSING` | the English string has no entry in that catalogue |
| `EMPTY` | the entry exists but `msgstr` is empty |
| `FUZZY` | `msgmerge` flagged it — the English changed, the translation did not |
| `OBSOLETE` | the catalogue holds an entry the page no longer contains |
| `CATALOGUE` | the `.po` is malformed, ambiguous, duplicated or for another language |

`mutation-test.sh` proves this by execution: it copies the sources into a
throwaway sandbox and exercises a changed English sentence, an absent catalogue,
a `fuzzy` entry, a duplicated entry and a malformed entry — checking each time
that the build refuses *and* that no generated page survives on disk. It then
asserts, by SHA-256 and by `git status`, that the calling worktree was never
written to. An argument is not a proof; run the test.

> **Scope of the mutation test.** It exercises **French only**, as a
> representative catalogue. The mechanism it proves — fail-closed refusal,
> stale-artifact removal, atomic write — is language-agnostic code shared by all
> five, so proving it once proves it everywhere. What it does *not* do is
> validate the other four catalogues; that is the job of `check all`, `build
> all` and `verify all`, which run over every language on every PR and every
> deploy. Do not read a green mutation test as "the five catalogues are fine".

## Changing English text

Editing one English sentence invalidates that string in **all five**
catalogues, so all five must be updated:

```bash
#  1. edit index.html
python3 i18n/i18n.py extract
for po in i18n/homepage.*.po; do
    msgmerge --update --backup=none "$po" i18n/homepage.pot
done
#  2. the changed entry is now marked #, fuzzy in every catalogue
#  3. fix each msgstr and delete its fuzzy line
python3 i18n/i18n.py check all
```

Until step 3 is done for every language, **nothing** deploys — not just the
language you forgot. That is the point: a page is either current or absent,
never quietly wrong. If you cannot translate a change immediately, the honest
options are to hold the English change or to remove a language from the table;
there is no "publish it stale" path, by design.

## Disambiguation

When one English string needs two different renderings, wrap the element:

```html
<p class="memorable" data-i18n-context="hero">Programmable settlement<br>…</p>
```

That becomes the gettext `msgctxt`. Context is **explicit** on purpose: deriving
it from CSS class names would mark the whole catalogue fuzzy the day someone
renames a class for styling reasons.

### Context metadata — what is actually true

`data-i18n-context` is stripped from every **generated** page, so it never
appears in `fr/`, `es/`, `zh-hans/`, `hi/` or `ar/`; `verify <lang>` fails if it
ever does. The **English page is not generated** — it is `index.html`, served
as-is — so it **keeps the attribute**.

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

Per-language facts — the whole `<html>` tag including `dir`, the canonical URL,
`og:url`, and the language menu — are not prose either. They live in `LANG_CONF` in `i18n.py` and are
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

## Deliberate non-literal renderings

Translations are meant to read naturally, not word by word. Three departures
from the English are intentional and are recorded here so nobody has to guess
whether they are bugs.

**1. "Bitcoin remains the monetary anchor." is not rendered in the paragraph.**
The English section reads: eyebrow *Bitcoin remains the anchor* → heading *The
anchor is Bitcoin, and it stays where it is.* → paragraph opening *Bitcoin
remains the monetary anchor.* Three statements of the same idea in a row. French
condensed it first, and the other four followed.

This is a **kept** condensation, not an oversight. The section still carries the
claim: every language translates the eyebrow as "Bitcoin remains the anchor",
and the paragraph immediately before it is entirely about M0, M1 and monetary
conversion, so "monetary" is not lost in context. Restoring the clause would
reintroduce in five languages the repetition that was removed from one.

If you disagree, the fix is one string per catalogue — the msgid is
`Bitcoin remains the monetary anchor. BATHRON verifies its history…`.

**2. "inventory" becomes "assets" once and "liquidity" once.** English uses
*inventory* twice in the markets paragraph. Every translation renders the first
as assets and the second as available liquidity, because a single literal word
reads like warehouse stock in all five languages. The meaning — a provider
quotes because it holds something, and markets emerge from what is available —
is unchanged.

**3. Arrows point the other way in Arabic.** `→` becomes `←` in the Arabic
catalogue: in right-to-left text, forward is leftward. The five `→` in the other
catalogues and the five `←` in Arabic are checked in the audit, not by a gate.

### What this pass was, and was not

The four new catalogues were written and then re-read against the English for
meaning, not just for protected terms: settlement rendered as the financial term
and never as a legal guarantee; Consensus Operators and Settlement Providers
kept distinct; "one operator, one vote" intact; M0, M1, BATHRON, Bitcoin,
e-mails and URLs untouched; no promise of price, reserve, refund or commercial
outcome introduced; "not from a listing decision" not softened anywhere; the
depth of a Bitcoin confirmation expressed as burial in the chain.

That is an **editorial semantic check**. It is not a native review. No native
speaker of Spanish, Chinese, Hindi or Arabic has read these pages.

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
would mark the CSS entry fuzzy and break every translated build. The generator in this
directory uses only the Python standard library, which is also why the deploy
workflow installs nothing to build the page. `gettext` is installed in CI for
the *test* alone: the fuzzy case must run against real `msgmerge` output rather
than a hand-written imitation of it.

## Scope

The homepage only. The mdBook documentation under `docs/` is English and is not
touched by this system; each translated homepage says so where it links to it.
