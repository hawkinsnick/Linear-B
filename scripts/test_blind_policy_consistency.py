#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
from blind_field_policy import load_policy,is_forbidden_field
from build_observation_corpus import is_forbidden_field as builder_forbidden
R=pathlib.Path(__file__).resolve().parents[1];policy=load_policy()
assert builder_forbidden is is_forbidden_field
for key,expected in [('inventory_number',False),('number',True),('grammatical_number',True),('normalized_reading',True)]:assert is_forbidden_field(key,policy)==expected
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td)/'obs.json'
 def check(obs):
  p.write_text(json.dumps([{'document_id':'A','observable':obs}]))
  return subprocess.run([sys.executable,str(R/'scripts/audit_gold_leakage.py'),str(p)],capture_output=True,text=True)
 assert check({'inventory_number':'INV1'}).returncode==0
 assert check({'number':'plural'}).returncode!=0
 assert check({'grammatical_number':'plural'}).returncode!=0
 assert check({'normalized_reading':'secret'}).returncode!=0
 assert check({'undeclared_field':'secret'}).returncode!=0
print('PASS: shared policy, allowed inventory field, gold leakage and undeclared field refusal')
