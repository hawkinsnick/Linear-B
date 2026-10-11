"""Synthetic hostile intake checks; fixtures are not Mycenaean data or gold."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from check_calibration_intake import check, FORMAT


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        # Intentionally invalid JSON: the checker must never parse answer values.
        (self.base / 'answers.bin').write_bytes(b'PRIVATE SYNTHETIC PAYLOAD {INVALID JSON')
        self.payload = {'path': 'answers.bin', 'sha256': hashlib.sha256((self.base / 'answers.bin').read_bytes()).hexdigest()}
        self.manifest = {'format': FORMAT, 'scope': 'pilot',
            'source': {k: 'synthetic-not-gold' for k in ('authority','locator','snapshot','rights_basis','lineage')},
            'observation_units': [{'document_id':'D1','source_unit_id':'W1','source_locator':'synthetic'}],
            'gold_unit_index': [{'document_id':'D1','source_unit_id':'W1','analysis_group_id':'G1','analysis_id':'A1','source_locator':'synthetic'}],
            'annotation_payload': self.payload, 'observation_payload': self.payload}

    def test_alternatives_and_blind_boundary(self):
        self.manifest['gold_unit_index'].append(dict(self.manifest['gold_unit_index'][0], analysis_id='A2'))
        report = check(self.manifest, self.base)
        self.assertEqual((report['exact_matches'],report['ambiguous_matches'],report['gold_analysis_rows']), (1,0,2))
        for name in ('answers_loaded','experiment_gates_changed','calibration_executed','source_authority_verified'):
            self.assertFalse(report[name])

    def test_ambiguous_and_unmatched_ids(self):
        self.manifest['gold_unit_index'].append(dict(self.manifest['gold_unit_index'][0],analysis_group_id='G2'))
        self.manifest['gold_unit_index'].append(dict(self.manifest['gold_unit_index'][0],document_id='D2'))
        self.manifest['observation_units'].append(dict(self.manifest['observation_units'][0],source_unit_id='W2'))
        report = check(self.manifest, self.base)
        self.assertEqual((report['exact_matches'],report['ambiguous_matches'],report['unmatched_observation'],report['unmatched_gold']), (0,1,1,1))

    def test_rejects_collision_answers_missing_keys_and_bad_digest(self):
        mutations = [
            lambda m: m['observation_units'].append(m['observation_units'][0]),
            lambda m: m['gold_unit_index'].append(m['gold_unit_index'][0]),
            lambda m: m['gold_unit_index'][0].update(lemma='answer'),
            lambda m: m['observation_units'][0].update(lemma='answer'),
            lambda m: m['gold_unit_index'][0].update(source_unit_id=''),
            lambda m: m['annotation_payload'].update(sha256='0'*64),
            lambda m: m['annotation_payload'].update(path='../answers.bin'),
            lambda m: m.update(scope='unspecified'),
            lambda m: m['source'].update(rights_basis=''),
        ]
        for mutate in mutations:
            m = copy.deepcopy(self.manifest); mutate(m)
            with self.subTest(manifest=m), self.assertRaises(ValueError): check(m, self.base)

    def test_graphical_not_inferred_from_words(self):
        report = check(self.manifest,self.base)
        self.assertEqual(report['graphical_occurrences'],0)
        g = {k: 'synthetic' for k in ('authority','snapshot','locator','data_rights_basis','image_rights_basis')}
        g.update(payload=self.payload, occurrences=[dict(document_id='D1',source_unit_id='W1',occurrence_id='S1', **{k:'synthetic' for k in ('face','line','position','source_locator','damage','uncertainty')})])
        self.manifest['graphical_baseline'] = g
        self.assertEqual(check(self.manifest,self.base)['graphical_occurrences'],1)
        self.assertFalse(check(self.manifest,self.base)['graphical_certification_verified'])
        g['occurrences'][0]['source_unit_id'] = 'missing'
        with self.assertRaises(ValueError):check(self.manifest,self.base)

    def test_cli_private_receipt_and_no_overwrite(self):
        manifest = self.base / 'manifest.json'
        manifest.write_text(json.dumps(self.manifest))
        output = self.base / 'receipt.json'
        command = [sys.executable,str(Path(__file__).with_name('check_calibration_intake.py')),str(manifest),'--out',str(output)]
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)
        before = output.read_bytes()
        self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)
        self.assertEqual(output.read_bytes(),before)
        for invalid in (None, [], {'format':FORMAT,'source':None}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):check(invalid,self.base)


if __name__ == '__main__':
    unittest.main()
