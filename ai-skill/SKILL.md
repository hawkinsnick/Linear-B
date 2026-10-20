---
name: linear-b-research
description: Evidence-first AI research skill for the Linear B corpus.
version: 0.3.1
---

## Load and validate this repository-bound skill

Use this file as the canonical individual skill. Load the complete matching
repository checkout or give the AI access to its files; this Markdown file alone
contains instructions, not the corpus. Do not claim that supplying a GitHub URL
installs a skill or makes private/local files available to an AI platform.
Resolve the paths below from the repository root. With Python 3.10+ available,
run `python scripts/validate_ai_skill.py` before describing this skill as
operational on the supplied checkout. Read `docs/AI-SKILL-VALIDATION.md` for the
exact workflow, examples, dependencies, validation scope and limitations.
If execution or source access is unavailable, say which step was not run and
make no fresh validation claim. Preserve all native source/rights restrictions.

Discover exact IDs with `python scripts/evidence_query.py --coverage` and
`python scripts/evidence_query.py --list COLLECTION`. Retrieve evidence with
`python scripts/evidence_query.py --record ID --collection COLLECTION`;
use `python scripts/research_delivery.py --dossier ID --collection COLLECTION`
for its evidence-only answer frame. Return the exact source path/hash/pointer,
attribution, uncertainty and native evidence unit. A missing ID means absent
from the selected view; never invent a replacement or infer global absence.


# Linear B Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization, computational derivation, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, or rights.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Corpus-specific caution
Deciphered Mycenaean Greek: distinguish primary transcription, normalized forms, linguistic interpretation, restorations, and editorial uncertainty; do not transfer Linear B values to other scripts without explicit evidence.

## Default research response
Give the direct answer, followed as relevant by Evidence; Evidentiary status; Uncertainty/limitations; Reproducibility; Rights/attribution.

## Synchronization
Read `ai-skill/generated/source-state.json` before substantive work. It records the corpus commit from which the AI-facing package was synchronized. Generated files are rebuildable views; canonical corpus files govern if a discrepancy is found.

## Academic-scrutiny gates
- Linear B is deciphered Mycenaean Greek, but transcription, graphical sign identity, normalization and interpretation remain distinct layers.
- Do not transfer Linear B values automatically to another script.
- Calibration and reference-annotation status follow canonical current status.
- Preserve source mapping qualifications, exclusions and upstream rights.

## Pre-expert source audit routing
Read `research/pre-expert-maximum.json`, `analysis/pre-expert-source-audit.json` and `docs/PRE-EXPERT-HANDOFF.md` before readiness or coverage claims. Record-level authenticated exports are generated locally under ignored directories; committed aggregate counts do not mean canonical records are publicly bundled. Use source JSON pointers and unchanged source IDs. Do not infer physical-object equivalence from headings, joins or inventory collisions. Read `research/linear-a-b-control-interface.json` before comparing representations. A local engineering pass does not establish independent source verification, linguistic calibration or expert validation.


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. The browser is self-contained and searches only the explicitly allowlisted files in `research/browser-sources.json`. Adding a file to the browser requires a rights/provenance check; never recursively ingest repository data or restricted upstream material. Browser display does not establish decipherment, source independence, or expert validation.


## Fleet EpiDoc and identity graph gates
Read `analysis/epidoc-interoperability-audit.json` and `research/identity-graph.json`. The repository has an EpiDoc import engineering path, but fleet EpiDoc conformance remains open until a real authenticated source export, structured mapping coverage, loss manifest, validation and round-trip tests exist. DĀMOS/source document identifiers must not be promoted to physical tablet identities by string equality. Scribal attribution and transliteration remain assertion/representation layers, not object or graphical-occurrence identity.

## Current-summary authority
Read the native current-status and residual-gate files before using README summaries. The marked current README block is generated by `scripts/build_current_summary.py --check`; historical sections are not current admission or calibration evidence. Report a mismatch and use the native authority.

For calibration acquisition, load `research/calibration-source-recheck-2026-10-11.json` and `docs/CALIBRATION-INPUTS.md`. The described DĀMOS EpiDoc export retains linking IDs but excludes linguistic analyses; do not classify epigraphic XML, documentation examples or transliteration as acquired linguistic gold. Preserve the separate graphical baseline requirement and the prediction-before-reveal policy.

## Source-specific stopping policy

Read `research/source-action-plan.json` and `docs/SOURCE-ACTION-PLAN.md` before proposing evidence growth or calling the corpus rights-only. Report access, permission for the intended use, source delivery, factual reconciliation and human adjudication separately. A failed endpoint or dated search is not global exhaustion. Preserve completed native crosswalks and identify their remaining edges; no metadata plan certifies a reading or physical identity.

For acquired calibration packages, follow `docs/CALIBRATION-INTAKE.md`. The private checker validates supplied identity indices and payload digests only. Its receipt does not authorize gold reveal, establish source rights or certify a graphical baseline; keep answers outside the prediction process.

## Enforced assertion, dependency and bundle integrity

Read `docs/AI-INTEGRITY.md` and the required `research/cross-corpus-dependencies.json` before source counts or cross-corpus analysis. Use qualified assertion views when provided; original source literals must travel with their reconciliation, uncertainty and identity context. The dependency register does not certify physical identity or linguistic affinity. Shared catalogue references and duplicated digital sources are not independent witnesses. Missing links mean unknown, not independent. `scripts/check_cross_corpus_dependencies.py` screens declared record selections and rejects pooled physical/witness counts and phonetic transfer. Native AI bundle validation checks the dependency projection and local evidence hashes. Bundle publication validates the exact source parent and never rebases or force-pushes the validated artifact. Software and packaging checks do not establish expert or model-behavior acceptance.

## Mega corpus before final independent acceptance

Use `Linear-A/corpus-factory/MEGA-CORPUS.md`, `build_mega_corpus.py` and `query_mega_corpus.py` to materialize and inspect native corpus views across all 18 members. The initial package has 9,116 view rows, including private authenticated A/B source records; it is not 9,116 unique inscriptions or a globally complete corpus. Original source fields, uncertainty, apparatus context and component terms travel with the rows. Native corpora remain authoritative. Preserve restricted payloads locally; do not infer a combined redistribution license, physical identity or independent witnesses. Continue lawful native coverage growth before final expert acceptance.

Linear B's `analysis/calibration-prepared-inputs-2026-10-12.json` reports real prepared observations: 5,932 documents, 5,890 nonempty transliteration surfaces and 42 missing/empty ones. Source word-ID crosswalks, linked linguistic annotations and source-certified graphical occurrences remain missing. `docs/CALIBRATION-PREPARED-INPUTS.md` and `research/calibration-acquisition-2026-10-12.json` distinguish preparation from gold delivery. Corpus expansion can continue while calibration is blocked. Do not replace occurrence gold with generated lexical analyses or expose the mixed mega-corpus interpretation layers to a blinded run.

## Source delivery checkpoint

Read `research/source-access-delivery-2026-10-12.json` and `docs/SOURCE-DELIVERY-REQUESTS.md` when planning source acquisition. Preserve contact-verification and routing uncertainty. Distinguish drafted requests from sent correspondence and explicit permissions. Log edition/version, IDs, coverage and rights per delivered component before reconciliation. Do not admit an inaccessible edition, invented word-ID join or photograph as certified gold; no scientific gate is closed by this checkpoint.

## Available source evidence

Read `docs/KN-FP13-CONCORDANCE.md` when querying the expanded source layer. Preserve native sampling units, unresolved source classifications, replica/derivative dependence and component rights. Source rectangles, facsimile ordinals and table rows are not automatically ancient objects, certified glyphs or independent witnesses.

## Private pre-reveal byte binding
Read `docs/CALIBRATION-FREEZE-2026-10-14.md` and `research/calibration-recheck-2026-10-14.json`. Use `scripts/freeze_calibration_run.py` only on private aligned packages outside the repository. Retain competing analyses and reject ambiguous/unmatched scope, altered digests and file aliases. A freeze receipt hashes sealed answers without parsing them; it grants no reveal, source authority, rights acceptance, valid scoring or calibration. Synthetic tests are engineering fixtures, never gold. Current public-route availability is not linked annotation delivery or certified graphical geometry. Keep all native calibration and scientific gates blocked until their actual prerequisites are satisfied.

## Published DAMOS identifier example — 14 October 2026

Read `research/damos-published-id-example-2026-10-14.json` and `docs/DAMOS-PUBLISHED-ID-EXAMPLE.md`. The inspected 2025 appendix provides one published item ID and seven ID-bearing units: five lexical words, one logogram, one numeral. These are publication-local identifiers, not a delivered same-snapshot crosswalk, linked linguistic gold or certified graphical evidence. Never align by text or ordinal, convert all seven to lexical words, or infer current source delivery from a paper example. Calibration remains unexecuted; delivery requests remain unsent. Component rights stay separate.

## Corpus-native evidence and alternatives

Read `docs/EVIDENCE-AND-ALTERNATIVES.md`, `research/evidence-query-profile.json` and `analysis/evidence-query-coverage.json` for evidence or competing-reading questions. Use `scripts/evidence_query.py` with exact native IDs and an explicit collection when ambiguous. Preserve `native_record`, every uncertainty/editorial mark, source attribution, locator, inspection status and rights. Cite artifact path, JSON pointer and SHA-256; hashes certify bytes only. Treat explicitly linked records as declared ID associations, not physical certification or independent witnesses. Context resources have corpus-level scope and are not automatically about the queried record. Distinguish a named source reading from a legacy queue label, uninspected bibliographic lead, count convention or hypothesis. Do not infer a count of collated alternative pairs or independent witnesses from searchable rows; those metrics remain unknown. Report the native units and scope of each view separately, and defer to the corpus-specific limits. No new readings, expert acceptance or decipherment follows from this interface.

## Bounded attribution review (2026-10-15)

Read `docs/ATTRIBUTION-REVIEW.md` and `research/attribution-review.json` before describing a dispute or source comparison. Run `python scripts/attribution_review.py --case ID` with the referenced evidence available. Preserve complete native evidence and distinguish reading, interpretation, classification, count, identity and representation questions. This checkpoint reviews pinned repository packets; it does not repeat their primary consultation or grant independent review. Inherit the exact author/publication, locator, consultation limits and dependence from each pointer; missing fields remain unknown. Use the case-specific remaining work. Do not count register entries or apparatus notes as fully attributed pairs, physical objects or independent witnesses.

Two documentary controls: the published DAMOS example is not the live observation snapshot, and the Cambridge cast is not a second ancient witness. No native alternative apparatus is supplied by these packets.

## Research delivery, evidence answers and feedback

Read `docs/RESEARCH-DELIVERY.md` and verify `analysis/research-delivery.json`
with `python scripts/research_delivery.py --check` before using delivery claims.
Use `--dossier ID --collection COLLECTION` for exact evidence-bound answers;
preserve the complete native payload, citations, categories and limitations.
Use `--search TEXT` for source-record retrieval. Do not convert file pointers
into missing primary-edition citations, catalogue rows into unique objects,
source dependence into independent confirmation, or review forms into acceptance.
Prepare bounded review drafts with `--review-template`; validate submissions with
`--validate-review`, then require native human-maintainer acceptance. Treat delivery
and deterministic answer tests as engineering checks, not empirical LLM validation
or completion of scholarly/source-permission work. Local packaging grants no new
redistribution rights. Label any model-generated analysis separately and cite it.

## Specialist task pilot

Read `docs/RESEARCH-TASK-PILOT.md`, `research/task-pilot.json` and `analysis/task-pilot-example.json` for the 25-record Pylos retrieval pilot. Reproduce full local results with `scripts/task_pilot.py`; public receipts omit transcription payloads. Report literal Unicode matches and whole-record marker-screen counts separately, never as secure readings, names or people. Hand labels are source assertions. Numeric document IDs, source JSON pointers and code-point spans are not source word IDs, physical identities or edition lines. Require admitted linguistic evidence and separate identity assertions before prosopographical claims; keep interpretation outside blinded calibration. Retain upstream CC BY-NC-SA terms and local-only result defaults. No named scholar participation, endorsement or independent review is established by the pilot.


## Source study and review handoff (2026-10-17)

Route source-study questions through `docs/SOURCE-STUDY-2026-10-17.md`, `research/source-study-2026-10-17.json` and the native evidence-query `source-study` collection. Preserve source attribution, exact locators, reuse terms and uncertainty. The prepared `review/source-study-packet.json` and draft response do not establish specialist participation or acceptance. No canonical readings or calibration results are added by this study.


For the source follow-up and reviewer exercise, read `docs/REVIEWER-WALKTHROUGH.md` and `research/review-exercise-2026-10-18.json`; retrieve its exact native target. Preserve the source register’s actual access level and all remaining gates. Treat `review/teaching-example.json` as a simulated project exercise with no reviewer, never a completed human assessment. Require the native blank response and independent source consultation for a real submission.

## Source page and structure check (2026-10-18)

Read `docs/DAMOS-SUPPLIED-STRUCTURE-2026-10-18.md` and `research/damos-supplied-structure-2026-10-18.json`; query `damos-supplied-structure` for the exact bounded outcome. Preserve the difference between source delivery, text rendition, page inspection, documentary correspondence and canonical acceptance. A successful HTTP status, matching heading, supplied document metadata or request draft cannot close an evidence gate. Historical registers retain their dated scope.

## Public source routes checked (2026-10-19 UTC)

Read `docs/DAMOS-PUBLIC-ROUTES-2026-10-19.md` and `research/damos-public-routes-2026-10-19.json`; query `damos-public-routes` for exact receipt/scope. Public access, a successful HTTP response, a field name, a drawing label or physical line number does not establish linked linguistic analyses or an edition clause. Preserve source dependence, method limits and component-specific reuse terms. No raw source payload is redistributed by this register.
