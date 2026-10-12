# Linear B source delivery requests

Both requests below are drafted and unsent. Contacts are verified from current primary project pages on 2026-10-12. The [DAMOS documentation](https://damos.hf.uio.no/howto) lists Federico Aurora and `federico.aurora@ub.uio.no`; the linked personal profile currently returns 404. [LiBER](https://liber.cnr.it/) lists editor Maurizio Del Freo and `maurizio.delfreo@cnr.it`. A project contact can route permission questions; that does not establish ownership of every contributed text or photograph.

## DĀMOS linked linguistic data

Subject: Request for a linked DĀMOS observation and annotation export

Dear Federico,

I’m building a free, noncommercial research corpus of ancient scripts, including Linear B. We have prepared a private observation package from an attributed DĀMOS-derived snapshot, but it lacks source-issued word IDs and linked linguistic annotations. Your 2025 EpiDoc export paper explains that epigraphic exports and linguistic analyses are separate, linked through `item.id` and `phys_word.id`.

Would it be possible to obtain an observation export and its linked linguistic annotation layer from the same source version? The useful fields would be document and physical-word IDs, face/line/token locators, actual and normalized forms, lemma, morphology and syntax where available, and each competing analysis with its uncertainty and bibliographic provenance. Unannotated and uncertain units should remain visible rather than being omitted.

A small, source-defined alignment pilot would be helpful if a full export is not yet ready. Please specify its selection, coverage, version and limitations. We would first validate the join keys and provenance; receiving data would not be treated as successful calibration or scholarly approval.

Could you also confirm the terms for private automated analysis and, separately, public redistribution of each supplied component? We would retain your attribution, license and any restrictions. We do not need photographs for this linguistic request, and we are not asking you to create new annotations or review our project.

Thank you for any export, documentation or appropriate access route you can offer.

## LiBER graphical and layout evidence

Subject: Research access to source-defined Linear B occurrence and layout data

Dear Maurizio,

I’m building a free, noncommercial ancient-script research corpus. For Linear B, we need to distinguish deciphered transcriptions from the graphical evidence that supports them. LiBER’s layout, apparatus and photograph references look like a useful route.

Is there an existing, published or source-defined export linking document/object IDs to sign occurrences, faces, lines and positions, with damage, uncertain identifications, alternatives, joins and edition provenance retained? A bounded sample with a documented selection and version would let us establish the alignment before considering wider coverage. We are asking for existing evidence, not new annotations or expert review of our project.

For any photograph, drawing or RTI references, could you identify the relevant owners, credit lines and permissions? Your site's personal non-profit image terms and limited scholarly text reuse are helpful, but we would appreciate explicit scope for private automated analysis, storage, and any public release of derived data or images. These permissions can be decided separately; a metadata/occurrence-only export would still be useful if images cannot be licensed.

We will retain the supplied attribution, uncertainty and restrictions and will not publish restricted components. Please let us know whether you can provide this or direct us to the appropriate data or rights contact.

Thank you.

## On delivery

Keep source answers private. Use `scripts/check_calibration_intake.py` under the existing [intake contract](CALIBRATION-INTAKE.md), preserving exact source-issued IDs rather than inventing token ordinals. Freeze the observation/version scope and experiment protocol before authorized answer reveal. Neither photographs nor deciphered transcriptions alone certify a graphical baseline. Source delivery, alignment, rights review and calibrated performance remain separate gates. CaLiBRA remains an alternative with an ordinary HTTP 502 route failure at this checkpoint; it has not delivered a photograph or annotation package.
