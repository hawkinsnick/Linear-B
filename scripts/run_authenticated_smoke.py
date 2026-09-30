#!/usr/bin/env python3
"""Reproduce a non-gold, document-count-only smoke run from pinned DAMOS bytes.
Keep the work directory outside the repository: upstream data retains its rights.
"""
import argparse,hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--workdir',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    source=pathlib.Path(a.source);work=pathlib.Path(a.workdir).resolve()
    if work==R or R in work.parents:raise SystemExit('REFUSING: workdir must be outside the repository')
    work.mkdir(parents=True,exist_ok=True);observations=work/'observations.json'
    expected='eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2'
    if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:raise SystemExit('REFUSING: source digest mismatch')
    def run(script,*args):subprocess.run([sys.executable,str(R/'scripts'/script),*map(str,args)],check=True)
    run('build_observation_corpus.py',source,observations);run('audit_gold_leakage.py',observations);run('preflight_representation_condition.py',observations,'LB-PHONETIC')
    target=R/'research/targets/linear-a-coarse-v0.1.json';outputs=[]
    for suffix in ('a','b'):
        manifest=work/f'manifest-{suffix}.json';data=work/f'retained-{suffix}.json'
        run('run_matched_degradation.py',observations,target,'--seed',20260930,'--out',manifest,'--data-out',data)
        outputs.append(json.loads(manifest.read_text()))
    if outputs[0]['retained_dataset_sha256']!=outputs[1]['retained_dataset_sha256']:raise SystemExit('FAIL: repeat output mismatch')
    result=outputs[0];result.pop('retained_dataset');result.pop('retained_document_ids')
    result.update({'version':(R/'VERSION').read_text().strip(),'run_kind':'AUTHENTICATED_REAL_INPUT_SOFTWARE_SMOKE_TEST','raw_input_sha256':expected,'repeat_run_identical':True,'upstream_rights':'CC BY-NC-SA 4.0; retained dataset stays local and is not redistributed','gold_revealed':False,'calibration_executed':False,'scientific_matched_environment_claim_allowed':False,'note':'Document-count-only engine smoke run on the authenticated DAMOS observation export. It tests reproducibility and output integrity, not detector performance or cross-script equivalence.'})
    pathlib.Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
