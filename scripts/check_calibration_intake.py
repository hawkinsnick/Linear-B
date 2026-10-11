#!/usr/bin/env python3
"""Check private acquisition metadata and exact source IDs without loading answers.

This produces an alignment receipt, never a calibration result or gate change.
The annotation payload is hashed as bytes only. Keep manifest and output private.
"""
import argparse
import hashlib
import json
from pathlib import Path

FORMAT = 'linear-b-calibration-intake-v1'


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ' must be explicit')
    return value


def digest_file(base, entry):
    if not isinstance(entry, dict):
        raise ValueError('payload descriptor must be an object')
    relative = Path(nonempty(entry.get('path'), 'payload path'))
    if relative.is_absolute():
        raise ValueError('payload path must be relative to package')
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError('payload must be a regular file inside the private package')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    if path.stat().st_size == 0 or digest.hexdigest() != entry.get('sha256'):
        raise ValueError('empty payload or SHA-256 mismatch')
    return digest.hexdigest()


def key(row):
    # No text, normalization or fuzzy identity join.
    if not isinstance(row, dict):
        raise ValueError('identity row must be an object')
    return tuple(nonempty(row.get(k), k) for k in ('document_id', 'source_unit_id'))


def check(manifest, base):
    if not isinstance(manifest, dict):
        raise ValueError('manifest must be an object')
    if manifest.get('format') != FORMAT:
        raise ValueError('unsupported intake format')
    source = manifest.get('source', {})
    if not isinstance(source, dict):
        raise ValueError('source descriptor must be an object')
    for field in ('authority', 'locator', 'snapshot', 'rights_basis', 'lineage'):
        nonempty(source.get(field), 'source.' + field)
    if manifest.get('scope') not in ('pilot', 'corpus'):
        raise ValueError('explicit pilot/corpus scope required')
    observation = manifest.get('observation_units')
    gold = manifest.get('gold_unit_index')
    if not isinstance(observation, list) or not observation or not isinstance(gold, list) or not gold:
        raise ValueError('nonempty observation and answer-free gold ID indices required')
    obs = {}
    for row in observation:
        if set(row) != {'document_id', 'source_unit_id', 'source_locator'}:
            raise ValueError('observation index must contain source identity metadata only')
        ident = key(row)
        if ident in obs:
            raise ValueError('duplicate observation identity')
        nonempty(row.get('source_locator'), 'observation source locator')
        obs[ident] = row
    groups = {}
    analyses = set()
    for row in gold:
        # Reject answer values in the intake sidecar; answers belong in private payload.
        if set(row) != {'document_id', 'source_unit_id', 'analysis_group_id', 'analysis_id', 'source_locator'}:
            raise ValueError('gold index contains unexpected fields or lacks required metadata')
        ident = key(row)
        group = nonempty(row.get('analysis_group_id'), 'analysis group')
        aid = nonempty(row.get('analysis_id'), 'analysis id')
        nonempty(row.get('source_locator'), 'gold source locator')
        if (ident, group, aid) in analyses:
            raise ValueError('duplicate analysis identity')
        analyses.add((ident, group, aid))
        groups.setdefault(ident, set()).add(group)
    annotation = digest_file(base, manifest.get('annotation_payload', {}))
    observation_digest = digest_file(base, manifest.get('observation_payload', {}))
    # Multiple analyses in ONE source group are alternatives, not join ambiguity.
    exact = set(obs) & set(groups)
    ambiguous = {ident for ident in exact if len(groups[ident]) != 1}
    graphical = manifest.get('graphical_baseline')
    graphical_count = 0
    graphical_digest = None
    if graphical is not None:
        if not isinstance(graphical, dict):
            raise ValueError('graphical descriptor must be an object')
        for field in ('authority', 'snapshot', 'locator', 'data_rights_basis', 'image_rights_basis'):
            nonempty(graphical.get(field), 'graphical.' + field)
        rows = graphical.get('occurrences')
        if not isinstance(rows, list) or not rows:
            raise ValueError('graphical baseline needs occurrence-level source index')
        seen = set()
        for row in rows:
            ident = key(row)
            if ident not in obs:
                raise ValueError('graphical occurrence absent from observation index')
            oid = nonempty(row.get('occurrence_id'), 'occurrence ID')
            if (ident[0], oid) in seen:
                raise ValueError('duplicate graphical occurrence')
            seen.add((ident[0], oid))
            for field in ('face', 'line', 'position', 'source_locator', 'damage', 'uncertainty'):
                nonempty(row.get(field), 'graphical occurrence ' + field)
        graphical_count = len(rows)
        graphical_digest = digest_file(base, graphical.get('payload', {}))
    report = {
        'format': 'linear-b-calibration-alignment-receipt-v1',
        'scope': manifest['scope'], 'source_snapshot': source['snapshot'],
        'observation_tokens': len(obs), 'gold_units': len(groups),
        'gold_analysis_rows': len(analyses),
        'exact_matches': len(exact - ambiguous), 'ambiguous_matches': len(ambiguous),
        'unmatched_observation': len(set(obs) - set(groups)),
        'unmatched_gold': len(set(groups) - set(obs)), 'manual_overrides': 0,
        'annotation_payload_sha256': annotation,
        'observation_payload_sha256': observation_digest,
        'graphical_occurrences': graphical_count, 'graphical_payload_sha256': graphical_digest,
        'answers_loaded': False, 'source_authority_verified': False,
        'rights_review_complete': False, 'graphical_certification_verified': False,
        'experiment_gates_changed': False, 'calibration_executed': False,
        'next_gate': 'SOURCE_AND_RIGHTS_REVIEW_THEN_FROZEN_PROTOCOL; receipt alone does not authorize reveal',
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    # A private file cannot accidentally replace a tracked gate/status or source.
    repo = Path(__file__).resolve().parents[1]
    if args.out.resolve().is_relative_to(repo) or args.out.resolve() == args.manifest.resolve():
        parser.error('receipt output must be outside the repository and distinct from the manifest')
    try:
        result = check(json.loads(args.manifest.read_text()), args.manifest.parent)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, str(error) + '\n')
    try:
        # Never overwrite an observation, answer package or previous receipt.
        with args.out.open('x') as stream:
            stream.write(json.dumps(result, indent=2) + '\n')
    except OSError as error:
        parser.exit(2, str(error) + '\n')
    print('Private alignment receipt written; no answers loaded and no experiment gates changed.')


if __name__ == '__main__':
    main()
