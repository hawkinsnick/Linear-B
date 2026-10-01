"""Synthetic encoding tests only; these are not ancient data or linguistic gold."""
import unittest
import xml.etree.ElementTree as ET
from import_epidoc import import_bytes, TEI

def wrap(body, annotations=''):
    return (f'<TEI xmlns="{TEI}"><text><body><div type="edition"><ab>{body}</ab></div></body></text>{annotations}</TEI>').encode()

def run(data):
    return import_bytes(data, source_id='SYNTHETIC-NOT-GOLD', rights='CC0 synthetic fixture', locator='test fixture')

class ImportTests(unittest.TestCase):
    def test_plain_and_nonphonetic(self):
        r=run(wrap('<w xml:id="w1">da-mo-de</w><w xml:id="w2" type="logogram">OLE</w><num xml:id="n1">1</num><pc xml:id="p1"><g ref="#word-divider"/></pc>'))
        self.assertEqual([u['source_unit_id'] for u in r['units']], ['w1','w2','n1','p1'])
        self.assertEqual([u['complete_plain_syllabic_text'] for u in r['units']], ['da-mo-de',None,None,None])
        self.assertFalse(r['linguistic_gold'])
    def test_editorial_and_alternatives_preserved(self):
        r=run(wrap('<w xml:id="w1"><choice><orig>pa</orig><reg>ro</reg></choice><supplied reason="lost" cert="low">ka</supplied><g ref="#s47"/><m type="specifier">f</m></w><gap reason="lost" extent="unknown" unit="character"/><w xml:id="w2" part="F">-pa</w>', '<standOff><list type="analyses"><item corresp="#w1">A</item><item corresp="#w1">B</item></list></standOff>'))
        self.assertTrue(all(u['complete_plain_syllabic_text'] is None for u in r['units']))
        e=ET.fromstring(r['edition_xml'])
        self.assertEqual(e.find('.//{'+TEI+'}g').get('ref'), '#s47')
        self.assertEqual(e.find('.//{'+TEI+'}supplied').get('cert'), 'low')
        self.assertIsNotNone(e.find('.//{'+TEI+'}gap'))
        self.assertEqual(len(ET.fromstring(r['annotation_groups_xml'][0]).findall('.//{'+TEI+'}item')),2)
    def test_rejected_alignment_and_entities(self):
        bad=[wrap('<w>pa</w>'),wrap('<w xml:id="a">pa</w><num xml:id="a">1</num>'),wrap('<w xml:id="a"><w xml:id="b">pa</w></w>'),b'<!DOCTYPE TEI [<!ENTITY x "pa">]>'+wrap('<w xml:id="a">&x;</w>'),b'<TEI/>',wrap('')]
        for data in bad:
            with self.subTest(data=data), self.assertRaises(ValueError):run(data)
    def test_provenance_required(self):
        with self.assertRaises(ValueError):import_bytes(wrap('<w xml:id="a">pa</w>'),source_id='',rights='NOASSERTION',locator='1')

if __name__=='__main__':unittest.main()
