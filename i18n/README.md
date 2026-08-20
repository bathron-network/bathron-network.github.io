# Homepage i18n — one source, versioned catalogues, fail-closed

The homepage exists in one place only: **`index.html`**. It is both the structure
and the English text, and it is the page served at `/`. There is no second HTML
file to keep in sync, because a second file is exactly what drifts.

French is a **catalogue of strings**, not a copy of the page:

```
index.html                 source of truth (structure + English)
i18n/homepage.pot          extracted template   (generated — never edit)
i18n/homepage.fr.po        French catalogue     (hand-maintained, versioned)
fr/index.html              generated artifact   (NOT versioned — see .gitignore)
```

## Commands

```bash
python3 i18n/i18n.py extract     # refresh homepage.pot from index.html
python3 i18n/i18n.py check fr    # audit the catalogue; exit 1 if anything is off
python3 i18n/i18n.py build fr    # generate fr/index.html; refuses if not 100 %
bash   i18n/mutation-test.sh     # prove the guarantee still holds
```

## The guarantee

`build` refuses to write anything unless **every** source string has a non-empty,
non-fuzzy translation. And it deletes any previous `fr/index.html` *before*
validating, so a failed build cannot leave yesterday's page behind. Since the
artifact is never committed, there is no stale copy anywhere to fall back on.

Four conditions block a build:

| Condition | Meaning |
|---|---|
| `MISSING` | the English string has no entry in the catalogue |
| `EMPTY` | the entry exists but `msgstr` is empty |
| `FUZZY` | `msgmerge` flagged it — the English changed, the French did not |
| `OBSOLETE` | the catalogue holds an entry the page no longer contains |

`mutation-test.sh` proves this by execution: it changes an English sentence,
shows the build failing and the French page disappearing, shows a `fuzzy` entry
failing too, then translates it and shows the build succeeding — and restores
the tree. An argument is not a proof; run the test.

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

That becomes the gettext `msgctxt`. The attribute is build metadata and is
stripped from every generated page. Context is **explicit** on purpose: deriving
it from CSS class names would mark the whole catalogue fuzzy the day someone
renames a class for styling reasons.

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

## Why not po4a

po4a was evaluated first and rejected on evidence, not taste. With the version
packaged for this machine (`po4a 0.73`), its xhtml module:

- rejects `<!doctype html>` in lowercase — valid HTML5 — with a parse error;
- reformats the document, reflowing the `<style>` block (65 lines → 55) so the
  round-trip diverges by 216 lines;
- puts **the entire CSS block into the catalogue as one `msgid`**.

That last one is fatal here: under a 100 %-or-nothing rule, changing a colour
would mark the CSS entry fuzzy and break the French build. The generator in this
directory uses only the Python standard library and pulls in no external tool,
which is also why the deploy workflow needs no new package.

## Scope

The homepage only. The mdBook documentation under `docs/` is English and is not
touched by this system.
