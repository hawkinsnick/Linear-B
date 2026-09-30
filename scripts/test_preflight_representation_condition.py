#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1];p=root/"scripts"/"preflight_representation_condition.py"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td); src=d/"o.json";src.write_text(json.dumps([{"document_id":"PY 1","observable":{"transliteration_surface":"a-ko","site":"Pylos","layout":{}}}]))
 q=subprocess.run([sys.executable,str(p),str(src),"LB-PHONETIC"],capture_output=True,text=True);assert q.returncode==0 and "PASS" in q.stdout
 q=subprocess.run([sys.executable,str(p),str(src),"LB-RAW"],capture_output=True,text=True);assert q.returncode!=0 and "graphical_sign_identity" in q.stderr
 src.write_text(json.dumps([{"document_id":"PY 1","observable":{"transliteration_surface":"a-ko"}},{"document_id":"PY 2","observable":{}}]))
 q=subprocess.run([sys.executable,str(p),str(src),"LB-PHONETIC"],capture_output=True,text=True);assert q.returncode!=0 and "record 1" in q.stderr
 src.write_text(json.dumps([{"document_id":"","observable":{"transliteration_surface":"a-ko"}}]))
 q=subprocess.run([sys.executable,str(p),str(src),"LB-PHONETIC"],capture_output=True,text=True);assert q.returncode!=0 and "document_id" in q.stderr
 for surface in (None,"", "   "):
  src.write_text(json.dumps([{"document_id":"A","observable":{"transliteration_surface":surface}}]))
  q=subprocess.run([sys.executable,str(p),str(src),"LB-PHONETIC"],capture_output=True,text=True);assert q.returncode!=0 and "transliteration_surface" in q.stderr
print(json.dumps({"status":"PASS","checks":["nested observation envelope","phonetic pass","raw refusal","per-record field completeness","empty identifier refusal"]}))

