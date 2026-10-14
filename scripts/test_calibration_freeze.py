"""Synthetic engineering controls only; these fixtures are not linguistic gold."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from freeze_calibration_run import freeze
class FreezeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  for p,b in [('observations.dat',b'observation fixture'),('answers.dat',b'NOT JSON: never parsed'),('predictions.dat',b'prediction fixture'),('protocol.dat',b'protocol fixture'),('implementation.dat',b'implementation fixture')]: (self.root/p).write_bytes(b)
  def entry(p):return {'path':p,'sha256':hashlib.sha256((self.root/p).read_bytes()).hexdigest()}
  self.intake={'format':'linear-b-calibration-intake-v1','scope':'pilot','source':dict(authority='synthetic-test-only',locator='fixture',snapshot='fixture-v1',rights_basis='test-only',lineage='synthetic'), 'observation_units':[dict(document_id='d1',source_unit_id='w1',source_locator='fixture')],'gold_unit_index':[dict(document_id='d1',source_unit_id='w1',analysis_group_id='g1',analysis_id='a1',source_locator='fixture')],'observation_payload':entry('observations.dat'),'annotation_payload':entry('answers.dat')}
  self.manifest={'format':'linear-b-pre-reveal-freeze-v1','intake_manifest':'intake.json','prediction_payload':entry('predictions.dat'),'scoring_protocol':entry('protocol.dat'),'predictor_implementation':entry('implementation.dat'),'observation_sha256':self.intake['observation_payload']['sha256'],'annotation_sha256':self.intake['annotation_payload']['sha256'],'source_snapshot':'fixture-v1','task':'known_answer_linguistic','experiment_id':'SYNTHETIC-NOT-CALIBRATION'}
 def tearDown(self):self.tmp.cleanup()
 def run_freeze(self):
  (self.root/'intake.json').write_text(json.dumps(self.intake));return freeze(self.manifest,self.root)
 def test_no_reveal_or_acceptance(self):
  r=self.run_freeze()
  for k in ['answers_loaded','gold_reveal_authorized','calibration_executed','prediction_semantics_validated','scoring_semantics_validated']:self.assertIs(r[k],False)
 def test_mutated_predictions_rejected(self):
  (self.root/'predictions.dat').write_bytes(b'changed')
  with self.assertRaises(ValueError):self.run_freeze()
 def test_intake_bindings(self):
  for k in ['source_snapshot','observation_sha256','annotation_sha256']:
   old=self.manifest[k];self.manifest[k]='mismatch'
   with self.assertRaises(ValueError):self.run_freeze()
   self.manifest[k]=old
 def test_alternatives_are_not_ambiguity(self):
  r=copy.deepcopy(self.intake['gold_unit_index'][0]);r['analysis_id']='a2';self.intake['gold_unit_index'].append(r);self.assertEqual(self.run_freeze()['exact_matches'],1)
 def test_ambiguous_groups_rejected(self):
  r=copy.deepcopy(self.intake['gold_unit_index'][0]);r['analysis_group_id']='g2';self.intake['gold_unit_index'].append(r)
  with self.assertRaises(ValueError):self.run_freeze()
 def test_unmatched_rejected(self):
  self.intake['observation_units'].append(dict(document_id='d1',source_unit_id='w2',source_locator='fixture'))
  with self.assertRaises(ValueError):self.run_freeze()
 def test_alias_rejected(self):
  self.manifest['prediction_payload']=self.intake['annotation_payload']
  with self.assertRaises(ValueError):self.run_freeze()
 def test_graphical_requires_component(self):
  self.manifest['task']='degraded_graphical'
  with self.assertRaises(ValueError):self.run_freeze()
 def test_path_escape_rejected(self):
  self.manifest['scoring_protocol']['path']='../protocol.dat'
  with self.assertRaises(ValueError):self.run_freeze()
if __name__=='__main__':unittest.main()
