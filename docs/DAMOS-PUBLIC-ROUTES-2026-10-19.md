# Public DĀMOS route check, 19 October 2026 UTC

The official public application defines `ajaxitem/{id}/` for a document view and `ajaxitemcontent/{id}` for its content hint. Both complete responses were inspected for the existing documentary example4307 (PY Ae27); no additional pilot IDs or private routes were probed. The acquisition hashes, JSON field paths and scope are retained in `research/damos-public-routes-2026-10-19.json`.

Both endpoints returned HTTP200 with a text/html content-type, but their bodies decode as JSON. The content hint contains one content field. The document response contains item, bibliography, meta and legends; its content/richcontent are transliteration strings, not linked word-analysis records. Neither selected response supplied the requested physical-word/linguistic-word layer or same-snapshot crosswalk. This does not establish absence from all possible public routes or from the internal database.

No source text, app code or annotations are republished here. Data CC BY-NC-SA4.0 and application GPL3 terms remain distinct. The26-ID annotation request remains unsent and unresolved. HTTP success, JSON parsing, a richcontent field name and public word search are not annotation delivery or graphical gold.
