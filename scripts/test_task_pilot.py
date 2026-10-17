"""Adversarial retrieval tests; fixtures are synthetic, never scholarly gold."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import task_pilot as t
from blind_field_policy import load_policy


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(t.SPEC.read_bytes())
        self.spec['source_records'] = 25
        self.docs = [{'id': i, 'site': 'Pylos', 'find_area': 'PY, Room 8',
                      'content': 'a-a-a', 'scribe': '4',
                      'translation': 'FORBIDDEN_SENTINEL', 'lemma': 'FORBIDDEN_SENTINEL'}
                     for i in self.spec['document_ids']]

    def selected(self):
        return t.select(self.docs, self.spec, load_policy())

    def test_literal_overlaps_offsets_and_no_gold(self):
        result = t.query(self.selected(), self.spec, 'a-a')
        self.assertEqual(result['summary']['all_surface_matches'], 50)
        self.assertEqual([h['surface_span_codepoints'] for h in result['hits'][:2]], [[0, 3], [2, 5]])
        self.assertNotIn('FORBIDDEN_SENTINEL', json.dumps(result))
        self.assertIsNone(result['summary']['persons_identified'])
        self.assertEqual(result['hits'][0]['source_citation']['field_pointers']['hand_label'], '/documents/0/scribe')

    def test_whole_record_marker_screen_and_preserved_source(self):
        self.docs[0]['content'] = '[x] ko-wa'
        r = t.query(self.selected(), self.spec, 'ko-wa')
        self.assertEqual(r['summary']['all_surface_matches'], 1)
        self.assertEqual(r['summary']['matches_after_whole_record_marker_screen'], 0)
        self.assertEqual(r['hits'][0]['observation']['transliteration_surface'], '[x] ko-wa')

    def test_unicode_is_not_normalized(self):
        self.docs[0]['content'] = 'a\u0323'
        r = t.query(self.selected(), self.spec, '\u1ea1')
        self.assertEqual(r['summary']['all_surface_matches'], 0)
        self.assertIn(self.docs[0]['id'], r['summary']['marker_screened_record_ids'])

    def test_missing_hand_and_surface_remain_missing(self):
        self.docs[0]['content'] = None
        self.docs[1]['scribe'] = None
        r = t.query(self.selected(), self.spec, 'a-a', hand='4')
        self.assertEqual(r['summary']['records_after_hand_filter'], 24)
        self.assertEqual(r['summary']['missing_surface_record_ids'], [self.docs[0]['id']])

    def test_no_match_is_scoped(self):
        r = t.query(self.selected(), self.spec, 'absent')
        self.assertEqual(r['summary']['all_surface_matches'], 0)
        self.assertEqual(r['summary']['selected_source_records'], 25)

    def test_invalid_identity_scope_and_source_rejected(self):
        for mutation in ('duplicate', 'missing', 'context', 'order'):
            docs = copy.deepcopy(self.docs)
            if mutation == 'duplicate': docs[0]['id'] = docs[1]['id']
            if mutation == 'missing': docs[0]['id'] = 'missing'
            if mutation == 'context': docs[0]['site'] = 'Knossos'
            if mutation == 'order': docs.reverse()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                t.select(docs, self.spec, load_policy())
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'wrong.json'
            path.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                t.run(path, 'a')

    def test_empty_query_refused(self):
        for literal in ('', '   '):
            with self.assertRaises(ValueError): t.query(self.selected(), self.spec, literal)

    def test_receipt_has_no_payload_and_html_escapes(self):
        self.docs[0]['content'] = '<script>alert(1)</script>'
        r = t.query(self.selected(), self.spec, '<script>')
        self.assertNotIn('hits', t.receipt(r))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'view.html'
            t.write_html(r, path)
            self.assertNotIn('<script>', path.read_text())
            self.assertIn('&lt;script&gt;', path.read_text())


if __name__ == '__main__':
    unittest.main()
