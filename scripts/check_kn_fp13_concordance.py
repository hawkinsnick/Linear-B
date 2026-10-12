"""Check exact, attributed inventory concordance without certifying glyphs."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = 'eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2'
FILE = 'research/kn-fp13-object-concordance.json'


def validate(report, source=None):
    rows = {r['id']: r for r in report['records']}
    if len(rows) != len(report['records']) or set(rows) != {'BM-1910-0423-1', 'MAA-Z46404B'}:
        raise ValueError('museum record coverage or identity drift')
    if rows['BM-1910-0423-1']['registration'] != '1910,0423.1' or rows['BM-1910-0423-1']['source_reported_edition_id'] != 'CoMIK I, Fp(1) 13':
        raise ValueError('original inventory/edition assertion drift')
    cast = rows['MAA-Z46404B']
    if cast['object_type'] != 'modern plaster cast' or cast['source_reported_original_registration'] != 'British Museum 1910,0423.1' or cast['source_reported_document_id'] != 'KN Fp 13':
        raise ValueError('replica relationship drift')
    for row in rows.values():
        if row['physical_identity_independently_verified'] is not False or row['image_rights'] != 'NOT_ACQUIRED':
            raise ValueError('unsupported identity/image admission')
    join = report['frozen_damos_join']
    if join['source_record_id'] != '13' or join['heading_short'] != 'KN Fp(1) 13' or join['inventory_as_supplied'] != 'BM (GR1910.4-23.1)' or join['source_file_sha256'] != PIN or join['frozen_fields_overwritten'] is not False:
        raise ValueError('frozen source identity drift')
    if report['relations'] != [dict(from_id='MAA-Z46404B', to_id='BM-1910-0423-1', relation='SOURCE_REPORTED_REPLICA_OF', source_url='https://collections.maa.cam.ac.uk/objects/600876/', independent_ancient_witness=False)]:
        raise ValueError('replica promoted to independent witness')
    if source is not None:
        raw = Path(source).read_bytes()
        if hashlib.sha256(raw).hexdigest() != PIN:
            raise ValueError('unapproved observation snapshot')
        candidates = [r for r in json.loads(raw)['documents'] if r['id'] == join['source_record_id']]
        if len(candidates) != 1:
            raise ValueError('source record collision or absence')
        row = candidates[0]
        if row['heading_short'] != join['heading_short'] or row['inventory'] != join['inventory_as_supplied'] or row['museum'] != 'BM':
            raise ValueError('numeric-ID-only or inventory-conflicting join')
        if row['chronology'] != report['chronology_assertions'][1]['value']:
            raise ValueError('source chronology dropped or overwritten')
    return {'status': 'PASS_ONE_DOCUMENT_SOURCE_CONCORDANCE',
            'museum_assertions': 2, 'ancient_witness_count_certified': False,
            'actual_frozen_source_replayed': source is not None,
            'graphical_gold_acquired': False, 'calibration_executed': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path)
    a = p.parse_args()
    print(json.dumps(validate(json.loads((ROOT/FILE).read_text()), a.source), indent=2))
