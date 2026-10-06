# Homepage translations

The English source is `index.html`. The language table `LANGUAGES` in
`i18n.py` defines the published languages, paths, menus and text direction.
The five complete catalogues are French, Spanish, Simplified Chinese, Hindi and
Arabic. The documentation book remains in English; every homepage says so.
Normative specifications linked from the homepage are identified as French.

## Editing and checking

```sh
python3 i18n/i18n.py extract
python3 i18n/i18n.py check all
python3 i18n/i18n.py build all
python3 i18n/i18n.py verify all
bash i18n/ci-check.sh
```

The generated template and language directories are ignored by git. A missing,
empty, fuzzy, obsolete, duplicate or malformed entry blocks generation and removes
a stale output page. An English change requires matching translations in the same
change. There is no partial-language fallback. The catalogue parser validates its
language header and rejects unknown languages before touching output paths.

Only visible text and prose attributes are translated. CSS, scripts, destinations,
canonical URLs, alternate links and the language selector are structural.
`data-i18n-context` distinguishes otherwise identical strings; it is removed from
generated pages. English remains the canonical, directly served source.

## Meaning and terminology

Preserve M0, BATHRON, Bitcoin, N, SP, LP and specification identifiers. M0 is an
*actif de règlement* in French, an *activo de liquidación* in Spanish, a
*结算资产* in Chinese, a *निपटान परिसंपत्ति* in Hindi and an *أصل للتسوية* in Arabic.
A registered identity and the producer role are distinct from service providers.
In French use *identité enregistrée*, *producteur*, *prestataire de règlement*
and *fournisseur de liquidité*. Keep BTC/M0 and X/M0 unchanged and explain X as
another asset. Consult [STYLE](../docs/STYLE.md) for the shared terminology.

Translate the whole claim, including negation, source, domain qualification and
responsibility for choosing depth. A burn creates no reserve and no claim on
Bitcoin. Waiting or stopping is conditional on the published domain; STOP need
not occur outside it. Do not introduce a price, repayment promise or assurance.
Do not add a network-state statement; link to Network status instead.

All catalogues were translated against the same English copy. Editorial review
is distinct from native-speaker review, which these automated checks cannot provide.
The vocabulary gate checks English catalogue keys; translations need human review.

## Direction and layout

Arabic uses `dir="rtl"`. The other languages use the normal left-to-right layout.
The selector uses native language names and a native details element. Logical CSS
properties place its dropdown on the appropriate side in both directions.
Structural checks verify direction, canonical links, alternate links and menus;
the static overflow check does not replace visual review in a browser.

## Adding a language

Declare the language and output path in `LANGUAGES`, add a complete catalogue,
ignore its generated page and regenerate the sitemap with `tools/gen-sitemap.py`.
Run both documentation and translation gates. An undeclared language or incomplete
catalogue is rejected. The menu is derived from the same table as generation.

## CI and pinned tools

`ci-check.sh` runs unit tests, sandbox mutation tests, catalogue checks, generation,
structural checks, skeleton comparison, static overflow checks and git cleanliness.
It uses Bash and the Python standard library, with no installation or download.
`msgmerge-compat.sh` checks compatibility with GNU gettext separately; it is optional
and returns a skip code when gettext is absent. It is outside the deployment gates.

The workflows pin actions by full commit SHA. The Pages upload action is
`actions/upload-pages-artifact` at `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`
(the v4.0.0 release). Python and mdBook versions and the mdBook archive digest
are pinned in the workflows. Keep those pins aligned when updating them.
