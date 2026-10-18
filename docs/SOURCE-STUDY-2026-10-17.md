# Source study and specialist handoff — 17 October 2026

The 25-record Pylos pilot plus published example 4307 were checked against 26 public DĀMOS AJAX responses. Returned IDs and four historical metadata fields agree with the registered derivative. This establishes documentary consistency only: no physical-word identifiers, linked linguistic analyses, same-snapshot crosswalk or certified graphical baseline was acquired. All competing display headings and source uncertainty are retained.

The public application defines the `ajaxitem/{id}/` route. The allowlisted projection excludes transcription content, images, comments and legends. DĀMOS content remains CC BY-NC-SA 4.0; original project licensing does not replace upstream conditions. Official `/news` returns successfully; an earlier failed `/news/` route does not establish that the news service is unavailable. Source timestamp fields are not corpus version identifiers.

The source paper's PDF pages 5 (§2.2) and 7 (§5) explain the separate linked linguistic layer and its delivery limitations. The request below is prepared, not sent; a successful homepage or metadata request is not annotation delivery.

### Bounded delivery request (unsent)

Please provide, for the 26 source record IDs in `research/damos-live-pilot-2026-10-17.json`, a versioned, same-snapshot extract containing the source observations, `phys_word` identifiers and links to all available `ling_words` analyses. Please preserve alternative analyses, incomplete or missing annotation, editorial uncertainty, and stable item/word crosswalks. Include the snapshot/version, extraction scope, field definitions, component-specific reuse terms, attribution and any image exclusions. We will retain the current derivative separately until ID and content alignment is demonstrated. No calibration or held-out labels are requested or exposed by this packet.

Official contact route: Federico Aurora's University of Oslo staff profile and the DĀMOS contact address documented in the source receipt. No outreach has occurred.

## Reproduction and review

`python scripts/source_study.py --check` replays the study, evidence-profile bindings, prepared packet and draft response. `python scripts/source_study.py --verify-sources /path/to/local-source-directory` additionally checks acquired source bytes against the receipts; source payloads are intentionally not bundled. `python -m unittest discover -s scripts -p test_source_study.py` checks drift and false scientific promotion.

`research/source-study-2026-10-17.json` is the attributed source register; `review/source-study-packet.json` contains evidence-bound questions and exact locators; `review/source-study-response.json` is an unfilled native review form; `analysis/source-study-audit.json` records the replay. Use the evidence query's `source-study` collection for the exact study ID in the register. A prepared packet, a structural validation or source authorship is not an independent specialist review. Reviewer identity and assessment remain empty. No acceptance, calibration execution or message sending occurred.


Subsequent work: [reviewer walkthrough and practice example](REVIEWER-WALKTHROUGH.md). The historical source study above remains scoped to its original evidence and access receipts.
