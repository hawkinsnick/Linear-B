# Linear B Open Control Corpus

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
