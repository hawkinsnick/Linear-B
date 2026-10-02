---
name: linear-b-research
description: Evidence-first AI research skill for the Linear B corpus.
version: 0.3.1
---

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
