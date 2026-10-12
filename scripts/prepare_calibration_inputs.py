"""Materialize real, answer-free Linear B inputs in a private research directory."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from build_observation_corpus import EXPECTED, FIELD_MAP, build_records
from blind_field_policy import load_policy
from validate_observation_export import audit

ROOT = Path(__file__).resolve().parents[1]


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def prepare(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('private input package must be outside the repository')
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError('source digest mismatch')
    data = json.loads(raw)
    if data.get('_meta', {}).get('license') != 'CC BY-NC-SA 4.0':
        raise ValueError('source license mismatch')
    rows = build_records(data['documents'], load_policy())
    # Document IDs are supplied; no token ordinal is promoted to a source word ID.
    identities = [{'document_id': row['document_id'], 'source_locator': '/documents/' + str(index),
                   'has_transliteration': bool(row['observable']['transliteration_surface']),
                   'source_word_ids': None, 'source_word_alignment_status': 'NOT_SUPPLIED_IN_DERIVATIVE'}
                  for index, row in enumerate(rows)]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(exist_ok=False)
    try:
        export = output / 'observations.json'
        export.write_text(json.dumps(rows, ensure_ascii=False, separators=(',', ':')))
        verified = audit(source, export)
        subprocess.run([sys.executable, str(ROOT / 'scripts/audit_gold_leakage.py'), str(export)], check=True, capture_output=True)
        (output / 'document-identities.json').write_bytes(encode(identities))
        files = {name: {'sha256': hashlib.sha256((output / name).read_bytes()).hexdigest(),
                        'bytes': (output / name).stat().st_size}
                 for name in ['observations.json', 'document-identities.json']}
        report = {'format': 'linear-b-prepared-inputs-v1', 'source_sha256': EXPECTED,
                  'source_license': data['_meta']['license'], 'attribution': data['_meta'].get('attribution'),
                  'records': verified['records'], 'nonempty_transcription_surfaces': verified['nonempty_transcription_surfaces'],
                  'missing_transcription_surfaces': verified['null_or_empty_surfaces'],
                  'observation_export_sha256': verified['observation_export_sha256'],
                  'mapped_field_coverage': {name: {'present': sum(bool(row['observable'][name]) for row in rows),
                                                'missing': sum(not bool(row['observable'][name]) for row in rows)} for name in FIELD_MAP},
                  'files': files, 'source_word_ids_available': False,
                  'aligned_linguistic_gold_available': False, 'certified_graphical_occurrences_available': False,
                  'observations_are_deciphered_transliterations': True,
                  'gold_revealed': False, 'predictions_frozen': False, 'calibration_executed': False,
                  'redistribution_authorized_by_this_package': False,
                  'next_inputs': ['source-issued word-ID crosswalk', 'linked annotation payload preserving alternatives',
                                  'source-certified graphical occurrences and component permissions'],
                  'growth_policy': 'Build corpus coverage independently of calibration; source claims stay unreviewed until accepted.'}
        (output / 'input-readiness.json').write_bytes(encode(report))
        (output / 'README.md').write_text('# Private Linear B observation inputs\n\n'
            'These are real, checksum-pinned DAMOS derivative observations, with upstream CC BY-NC-SA 4.0 attribution. '
            'Keep this package outside public repository uploads. It contains deciphered transliterations, not raw graphical signs. '
            'The document index does not supply source word IDs or annotated answers. '
            'Use the native calibration intake checker after a linked source package arrives. '
            'No predictions, gold reveal, scholarly acceptance or calibration results are generated.\n')
        return report
    except Exception:
        shutil.rmtree(output)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output), indent=2))
