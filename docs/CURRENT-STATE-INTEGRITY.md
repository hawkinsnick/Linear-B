# Current-state integrity milestone

Repository version: 4.9.19.

Exact DĀMOS v2 bytes reauthenticated; 5,932 observation records rebuilt and leakage checked. A twice-repeated document-count-only smoke run retained 802 documents with identical dataset hashes. Linguistic gold and graphical sign identities remain missing; calibration is unexecuted and 5.0 is not earned.

The current-state validator parses every committed JSON file, checks schema validity, citation/family metadata, evidence digests, interchange positive/negative fixtures, native committed counts where available, and blocked-claim boundaries. Regression tests deliberately corrupt metadata and restore it. CI runs these checks on pushes and pull requests.

Artifact content versions are independent of the repository release. Unchanged inscription records, historical baselines, protocols and audits retain their content versions. Mutable current metadata (VERSION, citation, current status, family member version, current index/API examples/manifest) follows the repository version. A software validation pass does not certify epigraphic correctness or open a scientific gate.

## Reproduce the real-input smoke run

Obtain the pinned upstream `damos-corpus-v2/damos-corpus.json` locally and run:

```sh
python scripts/run_authenticated_smoke.py /path/to/damos-corpus.json --workdir /tmp/damos-smoke --out /tmp/damos-smoke-summary.json
```

The script verifies exact bytes, rebuilds and leakage-checks the observation export, performs phonetic field preflight, and repeats the document-count-only sampling with seed 20260930. The work directory must be outside the repository. Retained data stays local under upstream rights. Compare the summary with `analysis/authenticated-document-count-smoke.json`. No linguistic gold is consumed or scored.
