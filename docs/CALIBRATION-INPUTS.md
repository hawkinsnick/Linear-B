# Calibration acquisition checkpoint — 11 October 2026

Known-answer calibration remains unexecuted. No linguistic gold or authoritative graphical baseline was acquired in this checkpoint.

## What the source inspection establishes

Aurora, Nedić, Nesøen and Haug, *Exporting Mycenaean* (2025), DOI [10.5617/dhnbpub.12295](https://doi.org/10.5617/dhnbpub.12295), section 2.2 (printed/PDF p.5) and section 5 (p.7), explicitly distinguish epigraphic EpiDoc export from linguistic annotation. Their described export retains `item.id` and `phys_word.id`, but omits the separately stored morphological/syntactic analyses. The p.5 passage was visually inspected. This is an implementation-at-publication finding, not proof that no later annotation export exists.

The current [online documentation](https://damos.hf.uio.no/about/online/) supplies no aligned annotation package. The [news](https://damos.hf.uio.no/news) records ongoing Pylos edition-variation work. Source inspection details and the original PDF digest are in `research/calibration-source-recheck-2026-10-11.json`; the PDF is not redistributed.

## Required acquisition

Request two linked components: (1) a source-issued observation/EpiDoc snapshot with document and word-occurrence IDs; (2) a separate linguistic annotation export keyed to those IDs, retaining competing analyses, uncertainty, source bibliography and version. A small, explicitly scoped annotated pilot is acceptable for developing alignment, but does not establish whole-corpus calibration. Missing IDs or ambiguous joins remain unresolved; no fuzzy match becomes gold.

Use the existing `research/gold-alignment-contract.json` and `research/gold-access-policy.json`. Acquire and validate package metadata without exposing answer values to the prediction process. Keep annotation payloads outside public observation exports. Freeze the scoring rule and predictions before a recorded gold reveal. Receipt, XML validity and source licensing do not themselves open experiment gates.

## Graphical evidence is a separate acquisition

[LiBER](https://liber.cnr.it/) provides photographs, layouts and critical apparatus. Its current Materials and Terms of use distinguish personal non-profit image use from limited scholarly text reuse; neither establishes a bulk benchmark redistribution grant. Request source-defined sign occurrences, face/line/position, damage and uncertainty, with image rights separately recorded. EpiDoc rendering and conventional phonetic labels are not physical sign certification. A link to CaLiBRA or another photograph is not a verified image baseline.

## Remaining action

`docs/ANNOTATION-EXPORT-REQUEST.md` specifies the exact missing package. It has not been sent; no maintainer reply or permission is asserted. Calibration and degraded-control gates remain blocked. Once evidence is supplied, reconcile IDs and scope, preserve alternatives, and evaluate it under the frozen protocol rather than changing the protocol to fit available answers.

## Executable receipt and routing

Use [private intake instructions](CALIBRATION-INTAKE.md) and `scripts/check_calibration_intake.py` when a source package arrives. This emits exact/ambiguous/unmatched alignment counts from answer-free source IDs and hashes private payloads without parsing answers. It does not change gates or establish certification. Current route checks and source-specific next actions are recorded in `research/source-route-check-2026-10-11.json` and `research/source-action-plan.json`.
