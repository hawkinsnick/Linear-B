# Linear B research pilot: trace a form through source records

This working pilot supports the first step of an administrative or prosopographical study: finding a literal form and inspecting its source context. It does not identify a person, classify a name, translate a word or establish that repeated names refer to one individual. No named scholar has requested, reviewed or endorsed this pilot.

## Read the executed example without installing anything

1. Open [the saved aggregate result](../analysis/task-pilot-example.json).
2. Find `query`: the search is the exact, case-sensitive literal `ko-wa`. No meaning is assigned to it by this demonstration.
3. Read `selection`: 25 explicitly frozen DĀMOS-derived source records report Pylos and `PY, Room 8`. These are the first matching records in the pinned source-array order, a convenience sample rather than a tablet series or representative archaeological sample.
4. Compare the two scenarios:

| Measurement | Executed result |
|---|---:|
| Selected source records | 25 |
| Literal matches | 23 |
| Source records containing those matches | 23 |
| Matches after the whole-record marker screen | 12 |
| Selected records flagged by that screen | 13 |

5. Read `marker_policy`. The screen flags surfaces containing `[`, `]`, `?`, combining underdot U+0323, `⟦` or `⟧`, then excludes the entire flagged record. An unmarked match may be excluded because a different part of its record is marked. Absence of these characters does not establish a secure reading; other conventions may remain unscreened. This is a sensitivity demonstration, not an estimate of reading reliability.
6. `persons_identified` and `validated_name_occurrences` are null: they are unavailable, not zero. Literal matches may be parts of longer strings and are not automatically lexical occurrences.
7. The public receipt excludes transcription payloads. `result_sha256` binds the complete local result; `reproduction` binds the source, selection specification, code, mapper and blind-field policy. Inspect source attribution and retained CC BY-NC-SA 4.0 terms in [the source registry](../sources/damos-v2.json) and [NOTICE](../NOTICE). No new primary edition has been inspected here.

## Reproduce and inspect full evidence locally

Download the repository using GitHub **Code → Download ZIP**, extract it and open a terminal in the extracted folder. Use Python 3.12, substituting `python3` or `py` if appropriate. The first command downloads the already registered public derivative and refuses a checksum mismatch. It is not a new linguistic-gold acquisition.

```sh
python scripts/acquire_damos_v2.py
python scripts/task_pilot.py --source data/raw/damos-corpus-v2.json --literal ko-wa --out output/task-pilot/ko-wa.json --html output/task-pilot/ko-wa.html
python scripts/task_pilot.py --source data/raw/damos-corpus-v2.json --literal ko-wa --verify-receipt analysis/task-pilot-example.json
python scripts/test_task_pilot.py
```

Open `output/task-pilot/ko-wa.html` in your browser. Each hit preserves the complete allowlisted observation context, its numeric source document ID, source JSON pointers, input hash and a zero-based Unicode-code-point span. These are not physical sign coordinates or edition page/line numbers. ID `4165` is a source identifier; do not invent a PY tablet designation from it. Museum and hand labels remain source assertions, not independent object or palaeographic certification.

Optionally append `--hand 4` to the query to select the exact source hand label. This selects an upstream attribution, not a newly validated scribal classification. Do not compare that filtered result to the unfiltered example receipt as though they were the same query.

Raw inputs and record-level outputs remain ignored local files. Do not add them to the public AI bundle or publish them merely because the script generated them. Each component retains its own rights. Project software/content licenses do not replace upstream terms.

## Use with an AI assistant

Provide the individual skill and, where permitted for the intended service, your local query result. The public aggregate receipt alone cannot support discussion of full transcription context. Ask:

> Using only the supplied query result, list matching source IDs and literal spans, report both marker-screen scenarios, and explain what the source context establishes. Preserve original strings and citations. Do not identify people, supply word meanings, infer source word IDs or convert JSON pointers into edition lines. State which evidence files you can actually read.

An acceptable answer reports 23 versus 12 for the unfiltered example and the limits above. This is an acceptance criterion, not an empirical LLM evaluation.

## Next scholarly step and review

The useful next question is whether a linguistically classified occurrence can be linked to an exact source locus. That requires an admissible same-snapshot annotation package, authoritative identifier/edition crosswalk and attributed linguistic analyses. Person equivalence then needs separate, source-supported identity claims. Keep those interpretation layers outside the blinded calibration inputs.

For review, supply the exact result, source/version, code/spec hashes and this question: “Are the selected source occurrences and their context faithfully represented, and which additional evidence is needed before a name or person claim?” Preserve the response, consulted sources, reviewer expertise/conflicts, dissent and maintainer disposition. Review state is PREPARED_NOT_REVIEWED; no acceptance is granted by generating this example. Existing [research-delivery controls](RESEARCH-DELIVERY.md) remain available for their registered public collections.

## Validation scope

Eight adversarial software tests cover offsets/overlaps, field whitelisting, marker scope, exact Unicode, missing data, source/identity/scope rejection and HTML escaping. The real source example was executed and replayed byte-for-byte. Neither checks a primary edition nor supplies linguistic calibration or expert validation. Native scientific gates remain unchanged.


Subsequent bounded source work: [Source study and specialist handoff](SOURCE-STUDY-2026-10-17.md). Its scope and evidence are separate from this historical pilot.
