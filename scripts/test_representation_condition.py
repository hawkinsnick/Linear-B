#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1];p=root/"scripts"/"project_representation_condition.py"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);src=d/"o.json";out=d/"x.json"
 src.write_text(json.dumps([{"document_id":"PY 1","observable":{"transliteration_surface":"a-ko","site":"Pylos","layout":{}}}]))
 q=subprocess.run([sys.executable,str(p),str(src),"LB-PHONETIC","--out",str(out)],capture_output=True,text=True);assert q.returncode==0
 z=json.loads(out.read_text());assert z==[{"document_id":"PY 1","transliteration_surface":"a-ko"}]
 for c in ("LB-RAW","LB-STRUCTURAL","LB-CONTEXT"):
  q=subprocess.run([sys.executable,str(p),str(src),c,"--out",str(out)],capture_output=True,text=True);assert q.returncode!=0 and "transliteration must not substitute" in q.stderr
print(json.dumps({"status":"PASS","checks":["phonetic projection","raw refusal","structural refusal","context refusal"]}))
