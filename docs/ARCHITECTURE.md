# Architecture — 0.1.0

## Evidence layer
Documents/objects, identifiers, sign occurrences, physical loci, source-defined structural units, damage/uncertainty and context.

## Gold layer
Deciphered readings, normalized forms, lemmas, morphology, syntax and other linguistic analyses. Gold assertions require scholarly provenance and may disagree.

## Experiment boundary
A blind detector receives only an explicitly exported observation view. Predictions are frozen before a gold join. The gold layer is never silently available through an observation adapter.

## Research layer
Experiment gates, frozen predictions, scoring specifications, results, claims and errata.

## Interchange
Aegean Epigraphy Interchange v0.1. Linear-B-specific linguistic categories live under extensions and are not requirements imposed on Linear A or Cypro-Minoan.

## Clients
Future Python/CLI/API/export clients consume the interchange layer and cannot redefine evidence.
