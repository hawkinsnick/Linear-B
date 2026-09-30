# Linear B Open Control Corpus

## Current status — 4.9.21

Corrected and field-by-field-audited DAMOS mapping: 5932 records, 5890 nonempty surfaces, 3945 scribe labels and 1305 inventory identifiers. The phonetic smoke samples from the 5890 eligible records and explicitly excludes 42 missing surfaces. Gold calibration and graphical baseline remain blocked.

Family contract 1.1 adds [Phaistos Disc](https://github.com/hawkinsnick/Phaistos-Disc) as a fifth member with its own native evidence and blocked transcription gate. Membership authorizes no pooled analysis or linguistic relationship claim. See [`research/family-extension-1.1.md`](research/family-extension-1.1.md).

The authoritative current gate summary is [`analysis/current-status.json`](analysis/current-status.json). Historical release reports below retain their original versions and claims.

Validate this checkout with:

```sh
python -m pip install -r requirements-validation.txt
python scripts/validate_current_state.py
python scripts/test_current_state.py
```


## Research platform

Observation/gold separation, attribution, blind scoring and representation contracts remain enforced. See the current summary above for completed acquisition and remaining research gates.
