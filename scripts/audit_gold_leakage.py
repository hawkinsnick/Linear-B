#!/usr/bin/env python3
import json,pathlib,re,sys
p=pathlib.Path(sys.argv[1]); rows=json.loads(p.read_text())
bad=re.compile(r"(lemma|morph|syntax|translation|meaning|semantic|gloss|case|gender|person|tense|mood|voice|lexeme)",re.I)
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
print(json.dumps({"status":"PASS","records":len(rows),"gold_like_field_hits":0}))
