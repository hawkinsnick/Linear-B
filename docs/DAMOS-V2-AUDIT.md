# DĀMOS-derived v2 corpus audit — 4.9.2

The exact user-supplied `damos-corpus.json` was independently re-hashed locally:

- bytes: **3,104,186**
- SHA-256: `eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2`
- parsed documents: **5,932**
- unique document IDs: **5,932**
- unique Trismegistos IDs: **5,932**
- documents with nonempty transliteration: **5,890**
- scribe: **3,945**
- find area: **3,262**
- find spot: **732**
- museum: **5,358**
- inventory: **1,305**

A 5,932-record observation export was generated locally and recursively audited for forbidden gold-like field names. Zero such field-name hits were found. The export SHA-256 is `2659e15884d3a36af8df3b98080e18941c2bd6cde48270cabe473c9be1027eaf`.

The full upstream or derived corpus is **not committed**. DĀMOS-derived content remains CC BY-NC-SA 4.0.

## Important limitation

This asset contains Linear B transliterations and contextual metadata. Transliteration already embodies deciphered sign readings; it is therefore not equivalent to a raw visual-sign corpus. The asset also does not provide the lemma/morphology/syntax/semantic gold layer required for the project's intended linguistic known-answer scoring.

Consequently, local-byte integrity and observation population are now satisfied, while linguistic-gold population, blind scoring and degradation-against-gold remain blocked.
