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
python3 i18n/i18n.py extract     # refresh homepage.pot from index.html
python3 i18n/i18n.py check fr    # audit the catalogue; exit non-zero if anything is off
python3 i18n/i18n.py build fr    # generate fr/index.html; refuses unless 100 % complete
python3 i18n/i18n.py verify fr   # lang, canonical, og:url, hreflang, selector, HTML balance
python3 i18n/i18n.py compare     # EN and FR must share one tag skeleton
python3 i18n/i18n.py overflow    # no fixed width wider than the smallest viewport
python3 i18n/test_i18n.py        # unit tests
bash   i18n/mutation-test.sh     # prove the fail-closed guarantee, in a sandbox
```

Every one of these runs in the deploy workflow, before `_site` is assembled.
A validation that only ever ran on a laptop is not a production guarantee.

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

Link separators in the footer are drawn by CSS, not written as text. A lone
`,` or `and` sitting between two links is untranslatable in isolation and drifts
between languages, so the structure removes the problem instead of asking a
translator to solve it.

## Language and path bounding

`build`, `check` and `verify` validate the language **before** computing any
path and before touching the filesystem. Only languages declared in `LANG_CONF`
are accepted, and only `fr` is generated — English is the source, not an output.
The resolved output path must be exactly `<repo>/fr/index.html` and the
catalogue path exactly `<repo>/i18n/homepage.<lang>.po`; anything else raises.

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
