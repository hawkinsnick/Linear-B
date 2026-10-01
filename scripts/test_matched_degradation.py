#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1];engine=root/"scripts"/"run_matched_degradation.py"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);rows=[{"document_id":"A","x":1},{"document_id":"A","x":2},{"document_id":"B","x":3},{"document_id":"C","x":4}]
 target=d/"t.json";target.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2}}}))
 outs=[]
 for i,data in enumerate((rows,list(reversed(rows)))):
  obs=d/f"o{i}.json";m=d/f"m{i}.json";dat=d/f"d{i}.json";obs.write_text(json.dumps(data))
  subprocess.run([sys.executable,str(engine),str(obs),str(target),"--seed","17","--out",str(m),"--data-out",str(dat)],check=True,capture_output=True,text=True);outs.append((json.loads(m.read_text()),dat.read_bytes()))
 A,B=outs;assert A[0]["retained_document_ids"]==B[0]["retained_document_ids"];assert A[1]==B[1];assert A[0]["retained_dataset_sha256"]==B[0]["retained_dataset_sha256"];assert A[0]["realized"]["document_count"]==2
 bad=d/"bad.json";bad.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"unknown","value":2}}}))
 p=subprocess.run([sys.executable,str(engine),str(d/"o0.json"),str(bad),"--seed","1","--out",str(d/"x"),"--data-out",str(d/"xd")],capture_output=True,text=True);assert p.returncode!=0 and "unknown/unmeasured" in p.stderr
 uns=d/"uns.json";uns.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2},"site_concentration":{"use":True,"status":"measured","value":0.5}}}))
 p=subprocess.run([sys.executable,str(engine),str(d/"o0.json"),str(uns),"--seed","1","--out",str(d/"y"),"--data-out",str(d/"yd")],capture_output=True,text=True);assert p.returncode!=0 and "not executable" in p.stderr
 for value in (True,2.5,"2",0,99):
  uns.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":value}}}))
  p=subprocess.run([sys.executable,str(engine),str(d/"o0.json"),str(uns),"--seed","1","--out",str(d/"z"),"--data-out",str(d/"zd")],capture_output=True,text=True);assert p.returncode!=0
print(json.dumps({"status":"PASS","engine":"matched-degradation-v0.4","checks":["cross-runtime hash ranking","input-order-independent selection","canonical dataset emission","dataset hashing","input hashing","unique-document sampling","all rows retained","unknown refusal","unsupported refusal","invalid/impossible count refusal"]}))
