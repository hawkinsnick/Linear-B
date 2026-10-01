# Research evidence workbench 1.0

This is an engineering milestone for Linear-B. Existing scientific gates remain in force.

## Open without coding

Download and extract the research workbench release ZIP, then open `workbench/evidence.html` in your browser. Everything shown is embedded locally. Publisher links open external sources only when you choose them. Search the pinned files, select a category, and open a record to inspect its actual source references and rights statements. The index covers current-status evidence; it is not the complete corpus or all historical files.

Metric units and definitions are shown together. Unknown remains unknown. Counts of catalogue entries, conventional phonetic transcriptions, physical objects and source-checked readings are different quantities. Each project remains separate.

## Review and corrections

Use “Record an inspection note” to record an evidence path or stable native ID, a source locator, what you observed and any uncertainty. Download the note before closing the page. Its evidence-index hash identifies the inspected snapshot. Notes are unverified observations and cannot open scientific gates. You can submit a correction through a GitHub issue yourself; no message is sent automatically.

A reviewer may supply a plain written report with stable IDs and source locations. Maintainers can convert a real review into the appropriate structured format while preserving the original report and getting the reviewer’s approval. Reviewers do not need to write code or edit JSON. Expert identity, expertise, independence and permission to publish their review must be checked before attribution.

## Reproduce the build

With Python installed, run `python scripts/evidence_workbench.py` to check committed outputs, or `python scripts/evidence_workbench.py --write` to rebuild them. `python scripts/test_evidence_workbench.py` tests tampering and embedding controls. Browser tests run in GitHub Actions. Hash agreement proves byte identity, not scientific correctness.
