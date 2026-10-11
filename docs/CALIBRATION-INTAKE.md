# Private calibration package intake

No source-issued gold or certified graphical baseline has been acquired. This checker makes exact alignment and payload integrity review executable when a source package arrives. It does not execute calibration, certify a maintainer's authority, approve rights or reveal answers.

Keep source files, manifest and receipt outside the repository. Run:

```bash
python scripts/check_calibration_intake.py /private/package/manifest.json --out /private/intake-receipt.json
```

The manifest has `format: linear-b-calibration-intake-v1`, an explicit `scope` of `pilot` or `corpus`, and these fields:

| Field | Required content |
|---|---|
| `source` | `authority`, `locator`, `snapshot`, `rights_basis`, `lineage`; statements to review, not self-certifying approval |
| `observation_payload` | Relative `path` inside package and exact `sha256` of source-issued observation bytes |
| `annotation_payload` | Relative `path` inside package and exact `sha256` of private annotation bytes |
| `observation_units` | Answer-free records containing only `document_id`, `source_unit_id`, `source_locator` |
| `gold_unit_index` | Answer-free records containing only `document_id`, `source_unit_id`, `analysis_group_id`, `analysis_id`, `source_locator` |
| Optional `graphical_baseline` | `authority`, `snapshot`, `locator`, `data_rights_basis`, `image_rights_basis`, `payload` with path/digest, and `occurrences` |
| Graphical occurrence | `document_id`, `source_unit_id`, `occurrence_id`, `face`, `line`, `position`, `source_locator`, `damage`, `uncertainty`, all source-stated |

Use source-assigned identity, never IDs invented from tokenizing a transliteration. Each distinct answer unit is a document/unit pair. Several analyses in one source analysis group remain alternatives; several groups for an otherwise matching unit are reported as ambiguous. Duplicate observations and duplicate analyses fail. Exact, ambiguous and unmatched counts are reported, with zero manual overrides. Missing graphical evidence stays absent; conventional spelling does not create occurrences.

The checker hashes payload bytes without interpreting their answers. It checks the supplied metadata index, not whether that index faithfully describes the payload: source review must verify this before experiment admission. The byte digests bind receipt to files but do not establish scientific correctness. A graphical metadata receipt is not graphical certification. The checker never writes experiment gates, the scoring rule or predictions, and refuses receipt output inside the repository or overwriting any existing file.

After receipt: verify source authority, component rights, index/payload fidelity, source-lineage independence and target coverage. A pilot remains a pilot. Resolve or explicitly exclude unmatched/ambiguous units under a preregistered policy. The frozen blind protocol still requires observation leakage checks, scoring and prediction artifacts frozen before a recorded authorized reveal. Keep answer payloads outside public observation exports and prediction-process access.

Run `python scripts/test_calibration_intake.py` for synthetic hostile-input checks. These fixtures are software tests, not ancient evidence or a known-answer result.
