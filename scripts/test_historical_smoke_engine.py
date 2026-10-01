"""Historical smoke replay must retain its frozen engine, not the current sampler."""
import pathlib,shutil,tempfile,unittest
from run_authenticated_smoke import historical_engine,R
class HistoricalEngineTests(unittest.TestCase):
 def test_frozen_bytes_and_tamper_refusal(self):
  source=historical_engine();self.assertNotEqual(source,R/'scripts/run_matched_degradation.py')
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);target=root/'scripts/history'/source.name;target.parent.mkdir(parents=True);shutil.copyfile(source,target);self.assertEqual(historical_engine(root),target);target.write_text(target.read_text()+'\n# tampered\n')
   with self.assertRaisesRegex(SystemExit,'historical sampling implementation digest mismatch'):historical_engine(root)
if __name__=='__main__':unittest.main()
