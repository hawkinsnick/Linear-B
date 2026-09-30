#!/usr/bin/env python3
"""Regression tests: release drift, malformed schemas, gate leakage, count drift."""
import json,pathlib,shutil,subprocess,sys,tempfile,re,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
def run(root):return subprocess.run([sys.executable,str(root/"scripts/validate_current_state.py")],capture_output=True,text=True)
assert run(R).returncode==0
with tempfile.TemporaryDirectory() as td:
    root=pathlib.Path(td)/"repo";shutil.copytree(R,root,ignore=shutil.ignore_patterns(".git","__pycache__"))
    paths=["CITATION.cff","schemas/aegean-interop-v0.1.schema.json","analysis/current-status.json"]
    originals={p:(root/p).read_bytes() for p in paths}
    def check(path,content):
        (root/path).write_text(content);q=run(root)
        assert q.returncode!=0,(path,q.stdout,q.stderr)
        (root/path).write_bytes(originals[path])
    check(paths[0],re.sub(r'^version:.*$', 'version: 0.0.0', (root/paths[0]).read_text(), flags=re.M))
    check(paths[1],'{')
    s=json.loads(originals[paths[2]]);s["repository_version"]="0.0.0";check(paths[2],json.dumps(s))
    contract=root/"research/family-compatibility-v1.json";raw=contract.read_bytes();s=json.loads(raw);s["member_version"]="0.0.0";contract.write_text(json.dumps(s));assert run(root).returncode!=0;contract.write_bytes(raw)
    gates=root/"research/experiment-gates.json"
    if gates.exists():
        raw=gates.read_bytes();s=json.loads(raw)
        blocked=next(g for g in s["experiments"] if g["state"]=="BLOCKED");blocked["claim_allowed"]=True
        gates.write_text(json.dumps(s))
        current=json.loads(originals[paths[2]])
        for e in current["evidence"]:
            if e["path"]=="research/experiment-gates.json":e["sha256"]=hashlib.sha256(gates.read_bytes()).hexdigest()
        (root/paths[2]).write_text(json.dumps(current));assert run(root).returncode!=0;gates.write_bytes(raw);(root/paths[2]).write_bytes(originals[paths[2]])
    current=json.loads(originals[paths[2]])
    if "calibration_executed" in current["scientific_results"]:
        current["scientific_results"]["calibration_executed"]=True;check(paths[2],json.dumps(current))
    current=json.loads(originals[paths[2]])
    if current["committed_evidence_counts"]:
        key=next(iter(current["committed_evidence_counts"]));current["committed_evidence_counts"][key]+=1
        check(paths[2],json.dumps(current))
    assert run(root).returncode==0
print(json.dumps({"status":"PASS","checks":["positive","citation drift","malformed schema","current version drift","family version drift","blocked-claim tamper when applicable","restored positive"]}))
