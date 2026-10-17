#!/usr/bin/env python3
"""Source-bound literal retrieval, without linguistic inference or gold inspection."""
import argparse
import hashlib
import html
import json
from pathlib import Path

from blind_field_policy import load_policy
from build_observation_corpus import FIELD_MAP, build_records

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'research/task-pilot.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def validate_spec(spec):
    ids = spec['document_ids']
    if len(ids) != 25 or len(set(ids)) != 25 or any(not isinstance(i, str) or not i for i in ids):
        raise ValueError('pilot requires 25 unique explicit source IDs')
    if not spec.get('marker_characters') or any(len(c) != 1 for c in spec['marker_characters']):
        raise ValueError('marker screen must declare single Unicode characters')
    if not spec.get('example_literal'):
        raise ValueError('empty example query')


def select(documents, spec, policy):
    validate_spec(spec)
    # Use the existing observation whitelist. Extra source fields never enter results.
    observations = build_records(documents, policy)
    if len(observations) != spec['source_records']:
        raise ValueError('source record count differs')
    indices = {row['document_id']: i for i, row in enumerate(observations)}
    if any(i not in indices for i in spec['document_ids']):
        raise ValueError('selected source ID missing')
    selected = [(indices[i], observations[indices[i]]) for i in spec['document_ids']]
    for _, row in selected:
        if any(row['observable'][k] != spec['selection'][k] for k in ('site', 'find_area')):
            raise ValueError('selected source context differs')
    matching = [row['document_id'] for row in observations if all(
        row['observable'][k] == spec['selection'][k] for k in ('site', 'find_area'))]
    if matching[:25] != spec['document_ids']:
        raise ValueError('frozen IDs differ from declared selection rule')
    return selected


def query(selected, spec, literal, hand=None):
    if not literal or not literal.strip():
        raise ValueError('a nonempty literal is required')
    hits = []
    missing, screened = [], []
    eligible = 0
    for index, row in selected:
        obs = row['observable']
        if hand is not None and obs['hand_label'] != hand:
            continue
        eligible += 1
        surface = obs['transliteration_surface']
        if not surface:
            missing.append(row['document_id'])
            continue
        markers = [c for c in spec['marker_characters'] if c in surface]
        if markers:
            screened.append(row['document_id'])
        # Include overlapping matches. Offsets count Python Unicode code points in
        # the unchanged source string, never signs, words or physical line positions.
        for start in range(len(surface)):
            if surface.startswith(literal, start):
                hits.append({
                    'document_id': row['document_id'],
                    'surface_span_codepoints': [start, start + len(literal)],
                    'matched_literal': surface[start:start + len(literal)],
                    'marker_characters_present': markers,
                    'observation': obs,
                    'source_citation': {
                        'source_id': row['source_id'],
                        'input_sha256': spec['input_sha256'],
                        'record_pointer': f'/documents/{index}',
                        'field_pointers': {k: f'/documents/{index}/{v}' for k, v in FIELD_MAP.items()},
                        'edition_locator': None,
                        'locator_limit': 'Source JSON pointers, not primary-edition page/line or physical sign locators.'
                    },
                    'person_identity': None,
                    'linguistic_classification': None,
                })
    unmarked_hits = [h for h in hits if not h['marker_characters_present']]
    summary = {
        'selected_source_records': len(selected),
        'records_after_hand_filter': eligible,
        'missing_surface_record_ids': missing,
        'marker_screened_record_ids': screened,
        'all_surface_matches': len(hits),
        'all_matching_record_ids': sorted({h['document_id'] for h in hits}),
        'matches_after_whole_record_marker_screen': len(unmarked_hits),
        'matching_record_ids_after_marker_screen': sorted({h['document_id'] for h in unmarked_hits}),
        'persons_identified': None,
        'validated_name_occurrences': None,
    }
    return {
        'format': 'linear-b-task-query-v1',
        'pilot_id': spec['pilot_id'],
        'query': {'literal': literal, 'source_hand_label': hand, 'method': spec['query_method']},
        'selection': spec['selection'],
        'marker_policy': spec['marker_policy'],
        'summary': summary, 'hits': hits,
        'unsupported': spec['unsupported'], 'rights': spec['rights'],
        'scientific_status': spec['scientific_status'],
    }


def run(source, literal, hand=None):
    spec_raw = SPEC.read_bytes()
    spec = json.loads(spec_raw)
    raw = Path(source).read_bytes()
    if digest(raw) != spec['input_sha256']:
        raise ValueError('source checksum differs; no result produced')
    selected = select(json.loads(raw)['documents'], spec, load_policy())
    result = query(selected, spec, literal, hand)
    result['reproduction'] = {
        'source_sha256': digest(raw), 'spec_sha256': digest(spec_raw),
        'code_sha256': digest(Path(__file__).read_bytes()),
        'observation_mapper_sha256': digest((ROOT / 'scripts/build_observation_corpus.py').read_bytes()),
        'blind_policy_sha256': digest((ROOT / 'research/blind-field-policy.json').read_bytes()),
        'field_policy_code_sha256': digest((ROOT / 'scripts/blind_field_policy.py').read_bytes()),
        'offset_unit': 'zero-based Unicode code point; half-open interval',
        'raw_document_count': spec['source_records'],
    }
    return result


def receipt(result):
    """Public aggregate receipt excludes transcription surfaces and record payloads."""
    return {k: v for k, v in result.items() if k != 'hits'} | {
        'result_sha256': digest(encoded(result)),
        'result_payload_published': False,
        'aggregate_terms': 'DAMOS-derived aggregate context retains CC BY-NC-SA 4.0; see NOTICE.',
    }


def write_html(result, path):
    # Escaping the complete payload also protects source strings containing markup.
    body = html.escape(encoded(result).decode('utf-8'))
    Path(path).write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Linear B bounded research pilot</title>'
        '<style>body{max-width:1100px;margin:2rem auto;padding:0 1rem;font:17px system-ui;'
        'line-height:1.5}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f4f6;'
        'padding:1rem;font-size:14px}</style><h1>Linear B: source-bound retrieval</h1>'
        '<p>Use your browser’s Find to locate a document ID. These are literal matches in '
        '25 selected source records, not identified people or validated linguistic words. '
        'The marker screen is a character heuristic, not a secure-reading judgment.</p>'
        '<p>Source pointers and code-point spans are digital locators, not edition lines. '
        'Upstream component rights apply. This local report grants no publication rights.</p>'
        '<pre>' + body + '</pre></html>', encoding='utf-8')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', required=True)
    p.add_argument('--literal', required=True)
    p.add_argument('--hand')
    p.add_argument('--out', help='Local JSON result; default prints to stdout')
    p.add_argument('--html', help='Optional local readable HTML result')
    p.add_argument('--receipt', help='Write aggregate receipt without source text')
    p.add_argument('--verify-receipt', help='Compare exact aggregate receipt to saved version')
    a = p.parse_args()
    try:
        result = run(a.source, a.literal, a.hand)
        if a.verify_receipt and json.loads(Path(a.verify_receipt).read_bytes()) != receipt(result):
            raise ValueError('receipt or result differs')
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_bytes(encoded(result))
        elif not a.verify_receipt:
            print(encoded(result).decode('utf-8'), end='')
        if a.html:
            write_html(result, a.html)
        if a.receipt:
            Path(a.receipt).write_bytes(encoded(receipt(result)))
        print(json.dumps(result['summary']), file=__import__('sys').stderr)
    except (ValueError, KeyError, TypeError, OSError) as error:
        p.exit(2, f'Refused: {error}\n')


if __name__ == '__main__':
    main()
