# Prepared Linear B inputs and corpus growth

The full authenticated DAMOS v2 observation side is now materialized and validated: 5,932 source document records, 5,890 nonempty transliteration surfaces and 42 missing/empty surfaces. This is a real source-derived input package, not a synthetic calibration result. Its observation hash is `4959cab13a11c53172d0d857344466e3434482175fdb4b92301ba27fefe28d5c`.

Run `python scripts/prepare_calibration_inputs.py /path/to/damos-corpus.json --output /path/outside/repos/linear-b-inputs`. Supply the exact snapshot identified in `research/damos-observation-field-map-v1.json`. The command refuses wrong bytes, output inside the repo and overwriting an existing package; it validates every mapped field and the blind field policy before completion.

The package provides observations, a document-identity index, field coverage, component attribution and checksums. The derivative does not supply source word IDs. Missing source IDs stay missing; invented ordinals or fuzzy lexical matches do not become linguistic gold. Transliterations are deciphered phonetic representations, not certified graphical sign occurrences.

## Remaining calibration inputs

1. A source-issued document/word-ID crosswalk aligned to an observation snapshot.
2. A linked linguistic annotation payload, retaining competing analyses and source lineage.
3. A source-certified graphical occurrence layer with face/line/position, uncertainty and separate component/image permissions.

The existing private intake checker handles these inputs when supplied. Freeze scoring rules and predictions before a recorded gold reveal. No experiment gate is opened by materializing observations. The current alternative-source audit is `research/calibration-acquisition-2026-10-12.json`: generated lexicons, lexical-cognate benchmarks and older CSV copies are not substitutes for occurrence annotations.

## Mega corpus before independent review

Corpus materialization and lawful coverage growth proceed independently of the blocked calibration experiments. The master `Linear-A/corpus-factory/build_mega_corpus.py` integrates the declared views of all 18 language repositories, retains component terms and supplies native reading/apparatus context. Restricted A/B payloads remain local. Read `Linear-A/corpus-factory/MEGA-CORPUS.md` for construction, verification and query instructions. Existing reference assertions can be inspected and compared before independent acceptance; they remain attributed, uncertain where applicable and distinct from accepted readings.

Do not request final expert acceptance merely because an engineering milestone is green. Finish the largest lawful source-bound evidence package and its machine reconciliation first. Missing source delivery must remain explicit, because corpus growth cannot invent inaccessible records or annotation answers.
