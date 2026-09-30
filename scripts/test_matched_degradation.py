#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1]; engine=root/"scripts"/"run_matched_degradation.py"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td); obs=d/"o.json"; target=d/"t.json"; a=d/"a.json"; b=d/"b.json"
 obs.write_text(json.dumps([{"document_id":"A","x":1},{"document_id":"A","x":2},{"document_id":"B","x":3},{"document_id":"C","x":4}]))
 target.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2}}}))
 for out in (a,b): subprocess.run([sys.executable,str(engine),str(obs),str(target),"--seed","17","--out",str(out)],check=True,capture_output=True,text=True)
 A=json.loads(a.read_text());B=json.loads(b.read_text());assert A==B;assert A["realized"]["document_count"]==2
 if "A" in A["retained_document_ids"]: assert A["realized"]["observation_records"]==3
 bad=d/"bad.json";bad.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"unknown","value":2}}}))
 p=subprocess.run([sys.executable,str(engine),str(obs),str(bad),"--seed","1","--out",str(d/"x")],capture_output=True,text=True);assert p.returncode!=0 and "unknown/unmeasured" in p.stderr
 uns=d/"uns.json";uns.write_text(json.dumps({"dimensions":{"document_count":{"use":True,"status":"measured","value":2},"site_concentration":{"use":True,"status":"measured","value":0.5}}}))
 p=subprocess.run([sys.executable,str(engine),str(obs),str(uns),"--seed","1","--out",str(d/"y")],capture_output=True,text=True);assert p.returncode!=0 and "not executable" in p.stderr
print(json.dumps({"status":"PASS","engine":"matched-degradation-v0.2","checks":["determinism","unique-document sampling","all rows retained","unknown refusal","unsupported refusal"]}))
