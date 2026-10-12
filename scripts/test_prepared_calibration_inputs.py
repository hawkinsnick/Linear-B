"""Hostile packaging controls; synthetic fixtures never become linguistic gold."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import prepare_calibration_inputs as module


class PreparedInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.json'
        self.source.write_text(json.dumps({'_meta': {'license': 'CC BY-NC-SA 4.0'},
            'documents': [{'id': 'SYNTHETIC-D1', 'content': 'SYNTHETIC-NOT-MYCENAEAN'},
                          {'id': 'SYNTHETIC-D2', 'content': None}]}))
        self.digest = hashlib.sha256(self.source.read_bytes()).hexdigest()

    def fake_audit(self, source, export):
        return {'records': 2, 'nonempty_transcription_surfaces': 1, 'null_or_empty_surfaces': 1,
                'observation_export_sha256': hashlib.sha256(export.read_bytes()).hexdigest()}

    def run_fixture(self, output):
        with patch.object(module, 'EXPECTED', self.digest), patch.object(module, 'audit', self.fake_audit), patch.object(module.subprocess, 'run'):
            return module.prepare(self.source, output)

    def test_index_never_fabricates_word_ids_or_answers(self):
        output = self.root / 'package'
        result = self.run_fixture(output)
        rows = json.loads((output / 'document-identities.json').read_text())
        self.assertEqual([row['source_word_ids'] for row in rows], [None, None])
        self.assertEqual(result['missing_transcription_surfaces'], 1)
        for field in ['aligned_linguistic_gold_available', 'certified_graphical_occurrences_available', 'gold_revealed', 'calibration_executed']:
            self.assertFalse(result[field])

    def test_unverified_bytes_rejected(self):
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            module.prepare(self.source, self.root / 'package')
        self.assertFalse((self.root / 'package').exists())

    def test_existing_package_is_never_overwritten(self):
        output = self.root / 'package'
        self.run_fixture(output)
        original = (output / 'observations.json').read_bytes()
        with self.assertRaises(FileExistsError):
            self.run_fixture(output)
        self.assertEqual((output / 'observations.json').read_bytes(), original)

    def test_failed_validation_does_not_leave_a_package(self):
        with patch.object(module, 'EXPECTED', self.digest), patch.object(module, 'audit', side_effect=ValueError('source mapping mismatch')):
            with self.assertRaises(ValueError):
                module.prepare(self.source, self.root / 'package')
        self.assertFalse((self.root / 'package').exists())

    def test_repository_output_rejected(self):
        with self.assertRaisesRegex(ValueError, 'outside the repository'):
            module.prepare(self.source, module.ROOT / 'private-package')


if __name__ == '__main__':
    unittest.main()
