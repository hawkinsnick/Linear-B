import copy
import json
from pathlib import Path
import unittest
from check_kn_fp13_concordance import validate


class ConcordanceTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((Path(__file__).resolve().parents[1]/'research/kn-fp13-object-concordance.json').read_text())

    def test_native(self):
        self.assertFalse(validate(self.report)['graphical_gold_acquired'])

    def test_cast_not_ancient_witness(self):
        self.report['relations'][0]['independent_ancient_witness'] = True
        with self.assertRaises(ValueError):
            validate(self.report)

    def test_identity_and_permission_rejected(self):
        self.report['records'][0]['image_rights'] = 'GRANTED'
        with self.assertRaises(ValueError):
            validate(self.report)

    def test_numeric_id_is_insufficient(self):
        self.report['frozen_damos_join']['inventory_as_supplied'] = 'BM ANOTHER'
        with self.assertRaises(ValueError):
            validate(self.report)

    def test_duplicate_source_id(self):
        self.report['records'].append(copy.deepcopy(self.report['records'][0]))
        with self.assertRaises(ValueError):
            validate(self.report)


if __name__ == '__main__':
    unittest.main()
