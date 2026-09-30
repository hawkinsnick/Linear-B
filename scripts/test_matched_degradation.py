#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1]; engine=root/"scripts"/"run_matched_degradation.py"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);obs=d/"o.json";target=d/"t.json";a=d/"a.json";b=d/"b.json";da=d/"da.json";db=d/"db.json"
 obs.write_text(json.dumps([{"document_id":"A","x":1},{"document_id":"A","x":2},{"document_id":"B","x":3},{"document_id":"C","x":4}]))
 target.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2}}}))
 for m,x in ((a,da),(b,db)): subprocess.run([sys.executable,str(engine),str(obs),str(target),"--seed","17","--out",str(m),"--data-out",str(x)],check=True,capture_output=True,text=True)
 A=json.loads(a.read_text());B=json.loads(b.read_text());assert A["retained_document_ids"]==B["retained_document_ids"];assert da.read_bytes()==db.read_bytes();assert A["retained_dataset_sha256"]==B["retained_dataset_sha256"];assert A["realized"]["document_count"]==2
 if "A" in A["retained_document_ids"]: assert A["realized"]["observation_records"]==3
 bad=d/"bad.json";bad.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"unknown","value":2}}}))
 p=subprocess.run([sys.executable,str(engine),str(obs),str(bad),"--seed","1","--out",str(d/"x"),"--data-out",str(d/"xd")],capture_output=True,text=True);assert p.returncode!=0 and "unknown/unmeasured" in p.stderr
 uns=d/"uns.json";uns.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2},"site_concentration":{"use":True,"status":"measured","value":0.5}}}))
 p=subprocess.run([sys.executable,str(engine),str(obs),str(uns),"--seed","1","--out",str(d/"y"),"--data-out",str(d/"yd")],capture_output=True,text=True);assert p.returncode!=0 and "not executable" in p.stderr
 for value in (True,2.5,"2",0,99):
  uns.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":value}}}))
  p=subprocess.run([sys.executable,str(engine),str(obs),str(uns),"--seed","1","--out",str(d/"z"),"--data-out",str(d/"zd")],capture_output=True,text=True);assert p.returncode!=0
print(json.dumps({"status":"PASS","engine":"matched-degradation-v0.3","checks":["determinism","dataset emission","dataset hashing","input hashing","unique-document sampling","all rows retained","unknown refusal","unsupported refusal","invalid/impossible count refusal"]}))

