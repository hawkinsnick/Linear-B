# Pre-expert validation handoff — Linear-B

This package records a reproducible engineering audit of the exact supplied derivative snapshot. It is not expert validation, independent source confirmation, or a claim of complete surviving inscription coverage. Current disposition: **PRE_EXPERT_HANDOFF_WITH_OPEN_SOURCE_GATES**. Consult `research/pre-expert-maximum.json` for individual unfinished gates.

## Reproduce

From the repository root, supply your authorized local damos-corpus.json snapshot:

```sh
python scripts/build_pre_expert_audit.py /path/to/damos-corpus.json
python scripts/validate_pre_expert_audit.py
python scripts/test_pre_expert_audit.py
```

The importer refuses bytes that differ from the pinned checksum. Outputs under `data/generated/pre-expert/` are deliberately ignored by git and retain CC BY-NC-SA 4.0 source provenance. `records.json` preserves stable source IDs, source fields and exact JSON pointers. The public `analysis/pre-expert-source-audit.json` contains counts, missingness and derivative hashes. These outputs are deterministic and do not read prospective cohorts, predictions, experiment outcomes or gold.

## Reviewer workflow

1. Reproduce the audit and inspect the source-specific representation boundaries.
2. Review local record/source pointers and the canonical source itself for any selected claim.
3. Keep editorial disagreements, source dependencies and missing fields visible.
4. Use `research/linear-a-b-control-interface.json` before cross-script analysis.
5. Record an expert decision as a separate attributed assertion; never overwrite a source witness silently.

## Rights and scope

Repository-original tooling follows the repository software terms. SigLA/DAMOS fields and local derivatives retain upstream rights and attribution. This change publishes no source-record export or primary-edition image. Historical statistical artifacts and their pinned inputs are untouched. Engineering reproducibility does not authorize scoring a sealed experiment.

## Linear B boundaries

5,932 unchanged source document IDs; 5,890 nonempty transcription surfaces; 3,945 scribal labels; 1,305 inventory values. Three short-heading collision groups involve 19 records; four inventory collision groups involve 14 records. These are collision flags, not duplicate or join adjudications. Graphical occurrence identity, coordinates and aligned linguistic gold are absent from this derivative. Editorial text markup is preserved, but structured damage annotation is not manufactured. `identity-register.json` is local. Legitimate aligned annotation acquisition remains external.

## Validation performed

Exact source checksums matched. Record exports and aggregate audits reproduced byte-for-byte on repeat. Current-state, source accounting, AI-bundle and existing Python regression checks passed. Linear B's existing real-source mapping audit and invented-field corruption checks also passed. CI now replays the source audit from the pinned public release asset. Remote CI results are tracked separately from this local validation.
