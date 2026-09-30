#!/usr/bin/env python3
import json,pathlib,re,sys
p=pathlib.Path(sys.argv[1])
policy_path=pathlib.Path(__file__).resolve().parents[1]/"research"/"blind-field-policy.json"
policy=json.loads(policy_path.read_text(encoding="utf-8"))
rows=json.loads(p.read_text(encoding="utf-8"))
patterns=policy["forbidden_gold_field_patterns"]
bad=re.compile("("+"|".join(re.escape(x) for x in patterns)+")",re.I)
hits=[]
def walk(x,path=""):
 if isinstance(x,dict):
  for k,v in x.items():
   q=f"{path}.{k}" if path else k
   if bad.search(k): hits.append(q)
   walk(v,q)
 elif isinstance(x,list):
  for i,v in enumerate(x): walk(v,f"{path}[{i}]")
walk(rows)
if hits: raise SystemExit("GOLD LEAKAGE: "+", ".join(hits[:20]))
print(json.dumps({"status":"PASS","records":len(rows),"gold_like_field_hits":0,"policy_version":policy["version"],"policy_path":str(policy_path)}))
