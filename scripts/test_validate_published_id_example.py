import json,tempfile,unittest
from pathlib import Path
from validate_published_id_example import ROOT,REGISTER,validate
class SourceBoundary(unittest.TestCase):
 def test_native(self):validate()
 def reject(self,fn):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for p in ['research/damos-published-id-example-2026-10-14.json', 'research/gold-acquisition-gate.json']:
    f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/p).read_bytes())
   f=root/REGISTER;x=json.loads(f.read_text());fn(x);f.write_text(json.dumps(x))
   with self.assertRaises(ValueError):validate(root)
 def test_false_authority(self):self.reject(lambda x:x.update(current_snapshot_word_crosswalk_acquired=True))
 def test_false_semantics(self):self.reject(lambda x:x['units'][-1].update(category='lexical_word'))
 def test_scope_drift(self):self.reject(lambda x:x['source'].update(snapshot='LIVE_EXPORT'))
if __name__=='__main__':unittest.main()
