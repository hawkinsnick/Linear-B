# Attribution review

Two documentary controls: the published DAMOS example is not the live observation snapshot, and the Cambridge cast is not a second ancient witness. No native alternative apparatus is supplied by these packets.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| No complete record collection claimed; selected documentary packets only | — |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'LB-PUBLISHED-EXAMPLE'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| LB-PUBLISHED-EXAMPLE | SOURCE_ROLE | Aurora et al.2025 pp.10–11 identify one published document and seven XML units: five lexical words, a logogram and a numeral. This is not a live export or same-version word crosswalk. | Current snapshot export/ID lineage and linked linguistic annotation are still unacquired; no encoded alternatives follow from a published example. |
| LB-FP13-REPLICA-AND-DATE | COUNT_OR_IDENTITY | The museum-reported Cambridge cast is a modern replica of the BM tablet, not another ancient witness. BM and frozen DAMOS chronology assertions remain separately attributed. | No photographic/graphical certification or independent chronology adjudication follows from catalogue concordance. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
