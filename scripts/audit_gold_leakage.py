#!/usr/bin/env python3
import json,pathlib,sys
from blind_field_policy import is_forbidden_field as policy_forbidden
p=pathlib.Path(sys.argv[1])
policy_path=pathlib.Path(__file__).resolve().parents[1]/"research"/"blind-field-policy.json"
policy=json.loads(policy_path.read_text(encoding="utf-8"))
rows=json.loads(p.read_text(encoding="utf-8"))
hits=[]
if not isinstance(rows,list):raise SystemExit("REFUSING: observation export must be a list")
for r in rows:
 if not isinstance(r,dict) or not isinstance(r.get("observable"),dict):raise SystemExit("REFUSING: malformed observation envelope")
 unknown=set(r["observable"])-set(policy["allowed_observation_fields"])
 if unknown:raise SystemExit("REFUSING: undeclared detector-visible fields: "+", ".join(sorted(unknown)))
def walk(x,path=""):
 if isinstance(x,dict):
  for k,v in x.items():
   q=f"{path}.{k}" if path else k
   if policy_forbidden(k,policy): hits.append(q)
   walk(v,q)
 elif isinstance(x,list):
  for i,v in enumerate(x): walk(v,f"{path}[{i}]")
walk(rows)
if hits: raise SystemExit("GOLD LEAKAGE: "+", ".join(hits[:20]))
print(json.dumps({"status":"PASS","records":len(rows),"gold_like_field_hits":0,"policy_version":policy["version"],"policy_path":str(policy_path)}))
