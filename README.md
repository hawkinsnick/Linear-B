# Linear B Open Control Corpus

## AI research skill

This corpus project includes a vendor-neutral, evidence-first AI research skill in [`ai-skill/`](ai-skill/). The corpus remains the scholarly source of truth; the skill is an interface to it, not a second corpus and not an independent authority.

Researchers using ChatGPT, Claude, Gemini, or another capable model can provide the repository (or its AI-ready bundle) together with [`ai-skill/SKILL.md`](ai-skill/SKILL.md). The skill requires the model to preserve provenance, uncertainty, exclusions, source dependence, rights, and this project's scientific gates. Before substantive use, check [`ai-skill/generated/source-state.json`](ai-skill/generated/source-state.json) and the generated research-bundle index for the corpus commit represented by the AI package.

For questions spanning multiple corpus projects, use the **Combined Corpus Research AI** documented in the Linear A repository under [`combined-ai-skill/`](https://github.com/hawkinsnick/Linear-A/tree/ai-skill-v0.1/combined-ai-skill). It orchestrates the registered individual skills while keeping their evidence models and rights separate. Membership in the combined system does **not** imply linguistic relationship, sign equivalence, chronology, decipherment, or independent replication.

## Reuse and attribution

Current project-original software is licensed under **PolyForm Noncommercial 1.0.0**; current project-owned non-software content is **CC BY-NC 4.0**, subject to [LICENSE-CONTENT.md](LICENSE-CONTENT.md). Earlier material already released under broader irrevocable terms retains any rights previously granted.

**Imported and source-derived material retains its upstream terms.** The
repository as a whole is not covered by an attribution-only data license.
See [rights and licensing](docs/RIGHTS-AND-LICENSING.md) and [NOTICE](NOTICE).

## Current status — 4.9.24

Corrected and field-by-field-audited DAMOS mapping: 5932 records, 5890 nonempty surfaces, 3945 scribe labels and 1305 inventory identifiers. The phonetic smoke samples from the 5890 eligible records and explicitly excludes 42 missing surfaces. Gold calibration and graphical baseline remain blocked.

Family contract 1.2 aligns all five projects with [Phaistos Disc 1.6.0](https://github.com/hawkinsnick/Phaistos-Disc/releases/tag/v1.6.0). The shared readiness report preserves native sampling units, source rights and blocked linguistic controls. It authorizes no pooling or linguistic relationship claim. See [`research/family-readiness-v1.json`](research/family-readiness-v1.json).

The authoritative current gate summary is [`analysis/current-status.json`](analysis/current-status.json). Historical release reports below retain their original versions and claims.

Validate this checkout with:

```sh
python -m pip install -r requirements-validation.txt
python scripts/validate_current_state.py
python scripts/test_current_state.py
```


## Research platform

Observation/gold separation, attribution, blind scoring and representation contracts remain enforced. See the current summary above for completed acquisition and remaining research gates.

### Evidence progress in 4.9.23

Adds a source-ID-preserving EpiDoc importer with synthetic tests for editorial markup, incomplete words, glyphs, numerical and nonphonetic units, alternative annotations, duplicate identifiers and unsafe XML. Published Mycenaean conventions and DAMOS export/import documentation are pinned. No real annotated export or linguistic gold is acquired; 5.0 remains blocked.

The shared family report now targets the Disc [2.0.0-rc.3 prerelease](https://github.com/hawkinsnick/Phaistos-Disc/releases/tag/v2.0.0-rc.3). Final independently reviewed Disc 2.0 remains blocked; compatibility does not confer linguistic equivalence or independent review. Native evidence and this repository’s release version are unchanged.

### Research evidence workbench 1.0

Download the research workbench ZIP, extract it, and open [workbench/evidence.html](workbench/evidence.html). It includes searchable pinned evidence, coverage definitions and unverified inspection-note export. See the [reading and review guide](research/workbench-guide.md). This engineering milestone grants no independent epigraphic acceptance.

The historical replay repair is included in workbench 1.0.1 and all subsequent workbench packages.

### Research workbench 1.1

Download the [research workbench 1.1 package](https://github.com/hawkinsnick/Linear-B/releases/tag/research-workbench-v1.1.0), extract it, and open `workbench/evidence.html`. It adds snapshot-bound inspection collections and includes the immutable release correction tracker. The Disc explorer also presents readable scenario comparisons. This engineering release grants no scientific acceptance.


## Fleet admission

This corpus participates in the Combined Corpus Research AI fleet. Fleet admission requires the repository's component-specific licensing architecture, its individual `ai-skill` research contract and generated bundle, explicit master-registry membership, and passing member/master validation. Third-party material retains its upstream rights.

## Pre-expert validation handoff

See [the handoff](docs/PRE-EXPERT-HANDOFF.md), [source audit](analysis/pre-expert-source-audit.json) and [remaining gates](research/pre-expert-maximum.json). Authenticated source records are materialized locally with retained rights; aggregate engineering checks do not establish expert validation or open scientific gates.


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. The browser is self-contained and searches only the explicitly allowlisted files in `research/browser-sources.json`. Adding a file to the browser requires a rights/provenance check; never recursively ingest repository data or restricted upstream material. Browser display does not establish decipherment, source independence, or expert validation.
