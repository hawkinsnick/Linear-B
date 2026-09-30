#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else "data/derived/linear-b-observation-v1.json")
policy_path=pathlib.Path(__file__).resolve().parents[1]/"research"/"blind-field-policy.json"
policy=json.loads(policy_path.read_text(encoding="utf-8"))
EXPECTED="eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2"
raw=src.read_bytes()
if hashlib.sha256(raw).hexdigest()!=EXPECTED: raise SystemExit("Refusing unverified input")
data=json.loads(raw)
patterns=policy["forbidden_gold_field_patterns"]
FORBIDDEN=re.compile("("+"|".join(re.escape(x) for x in patterns)+")",re.I)
def docs(x):
 if isinstance(x,list): return x
 if isinstance(x,dict):
  for k in ("documents","records","data","items"):
   if isinstance(x.get(k),list): return x[k]
 raise SystemExit("Unrecognized corpus envelope; inspect before adapting")
rows=[]; quarantine=set()
for d in docs(data):
 if not isinstance(d,dict): continue
 for k in d:
  if FORBIDDEN.search(k): quarantine.add(k)
 did=str(d.get("document_id",d.get("id","")))
 if not did: continue
 obs={"transliteration_surface":d.get("transliteration",d.get("text")),"sign_sequence":d.get("signs",[]) if isinstance(d.get("signs",[]),list) else [],"layout":d.get("layout",{}) if isinstance(d.get("layout",{}),dict) else {},"damage":d.get("damage",[]) if isinstance(d.get("damage",[]),list) else [],"support":d.get("support"),"site":d.get("site"),"find_area":d.get("find_area"),"find_spot":d.get("find_spot"),"object_class":d.get("object_class"),"hand_label":d.get("hand"),"museum":d.get("museum"),"inventory_number":d.get("inventory_number")}
 rows.append({"document_id":did,"source_id":"DAMOS-DERIVATIVE-V2","observable":obs,"provenance":{"input_sha256":EXPECTED,"derivation":"build_observation_corpus.py","blind_field_policy_version":policy["version"]}})
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,ensure_ascii=False,separators=(",",":")))
print(json.dumps({"records":len(rows),"quarantined_gold_like_upstream_keys":sorted(quarantine),"policy":str(policy_path),"output":str(out)}))
