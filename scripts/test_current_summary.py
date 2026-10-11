#!/usr/bin/env python3
"""Ensure current summaries fail closed on prose or native-source drift."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(root,*args):return subprocess.run([sys.executable,str(root/'scripts/build_current_summary.py'),*args],capture_output=True,text=True)
assert run(R,'--check').returncode==0
with tempfile.TemporaryDirectory() as td:
    root=Path(td)/'repo'
    for rel in ['README.md','VERSION','scripts/build_current_summary.py','analysis/current-status.json','analysis/pre-expert-source-audit.json','analysis/observation-source-mapping-audit.json','research/calibration-source-recheck-2026-10-11.json','research/residual-blocker-ledger-3.0.21.json','research/reference-manifest.json','research/pre-expert-maximum.json']:
        p=R/rel
        if p.is_file():q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    assert run(root,'--check').returncode==0
    readme=root/'README.md';old=readme.read_text();readme.write_text(old.replace('## Current evidence status','## Fake current status'));assert run(root,'--check').returncode!=0;readme.write_text(old)
    if (root/'research/reference-manifest.json').exists():
        p=root/'research/reference-manifest.json';d=json.loads(p.read_text());d['coverage']['source_text_rows']+=1
    else:
        p=root/'analysis/current-status.json';d=json.loads(p.read_text());d['scientific_results']['calibration_executed']=True
    p.write_text(json.dumps(d));assert run(root,'--check').returncode!=0
    assert run(root,'--write').returncode==0;assert run(root,'--check').returncode==0
    # The summary reports authority state; native scientific validators remain responsible for admission.
    readme.write_text(readme.read_text()+'\n<!-- CURRENT-STATUS:START -->');assert run(root,'--check').returncode!=0
print('PASS: current summary, prose drift, authority drift, replay, duplicate markers')
