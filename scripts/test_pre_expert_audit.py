#!/usr/bin/env python3
"""Guard source mappings, unknown values, identity boundaries and determinism."""
import copy,json,pathlib,sys,unittest
from build_pre_expert_audit import build,validate_source,ROOT,PINS
class AuditTests(unittest.TestCase):
 def la(self):return {'_meta':{'license':'CC BY-NC-SA 4.0'},'documents':[{'id':'TEST a','site':'X','typology':'Tablet','period':None,'dimensions_cm':None,'reference_url':None,'attestations':[{'sign':'DA','kind':'syllable','word':0,'series':'AB','number':1,'raw_flags':[1,0,0,0]},{'sign':'','kind':'blank','word':None,'series':'','number':None,'raw_flags':[0,2,0,0]}]}],'signs':[{'series':'AB','number':1,'display':'DA','value':'da','ref':'fixture'}]}
 def lb(self):return {'_meta':{'license':'CC BY-NC-SA 4.0'},'documents':[{'id':'0','content':'a-[b','site':'X','heading':'same','heading_short':'same','joins':None},{'id':'1','content':None,'site':'X','heading':'different','heading_short':'same','joins':'+ 0'}]}
 def test_source_fields_unchanged(self):
  d=self.la();before=copy.deepcopy(d);a,l=build(d,'Linear-A','fixture');self.assertEqual(d,before);self.assertEqual(l['occurrences.json'][0]['source_fields'],d['documents'][0]['attestations'][0]);self.assertEqual(l['source-words.json'][0]['source_word_index'],0);self.assertIsNone(l['occurrences.json'][0]['phonetic_value']);self.assertEqual(a['occurrences_without_sign_key'],1)
 def test_duplicate_ids_rejected(self):
  for project,d in [('Linear-A',self.la()),('Linear-B',self.lb())]:
   d['documents'].append(copy.deepcopy(d['documents'][0]))
   with self.assertRaises(AssertionError):validate_source(d,project)
 def test_rights_rejected(self):
  d=self.la();d['_meta']['license']='MIT'
  with self.assertRaises(AssertionError):validate_source(d,'Linear-A')
 def test_no_join_or_object_inference(self):
  a,l=build(self.lb(),'Linear-B','fixture');self.assertEqual(a['identity_collisions']['heading_short']['records_in_collision_groups'],2);self.assertEqual(a['field_coverage']['content']['missing_or_empty'],1);self.assertTrue(all(x['physical_object_id'] is None for x in l['identity-register.json']));self.assertEqual(l['records.json'][0]['source_fields']['content'],'a-[b')
 def test_invalid_word_index_rejected(self):
  d=self.la();d['documents'][0]['attestations'][0]['word']=True
  with self.assertRaises(AssertionError):validate_source(d,'Linear-A')
 def test_deterministic(self):self.assertEqual(build(self.la(),'Linear-A','fixture'),build(self.la(),'Linear-A','fixture'))
if __name__=='__main__':unittest.main()
