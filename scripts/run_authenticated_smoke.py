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
    run('build_observation_corpus.py',source,observations);run('audit_gold_leakage.py',observations)
    from validate_observation_export import audit
    mapping_audit=audit(source,observations)
    all_rows=json.loads(observations.read_text());eligible=[r for r in all_rows if isinstance(r['observable']['transliteration_surface'],str) and r['observable']['transliteration_surface'].strip()]
    eligible_ids={r['document_id'] for r in eligible};excluded=[r['document_id'] for r in all_rows if r['document_id'] not in eligible_ids]
    phonetic=work/'phonetic-eligible.json';phonetic.write_text(json.dumps(eligible,ensure_ascii=False,separators=(',',':')))
    run('preflight_representation_condition.py',phonetic,'LB-PHONETIC')
    target=R/'research/targets/linear-a-coarse-v0.1.json';outputs=[]
    for suffix in ('a','b'):
        manifest=work/f'manifest-{suffix}.json';data=work/f'retained-{suffix}.json'
        run('run_matched_degradation.py',phonetic,target,'--seed',20260930,'--out',manifest,'--data-out',data)
        outputs.append(json.loads(manifest.read_text()))
    if outputs[0]['retained_dataset_sha256']!=outputs[1]['retained_dataset_sha256']:raise SystemExit('FAIL: repeat output mismatch')
    result=outputs[0];result['mapping_audit']=mapping_audit;result['phonetic_eligibility']={'eligible':len(eligible),'excluded_missing_transcription':len(excluded),'excluded_document_ids_sha256':hashlib.sha256(('\n'.join(excluded)+'\n').encode()).hexdigest(),'rule':'Require nonempty source content before phonetic preflight and sampling; exclusions are completeness-based, never outcome-based.'};result.pop('retained_dataset');result.pop('retained_document_ids')
    result.update({'version':(R/'VERSION').read_text().strip(),'run_kind':'AUTHENTICATED_REAL_INPUT_SOFTWARE_SMOKE_TEST','raw_input_sha256':expected,'repeat_run_identical':True,'upstream_rights':'CC BY-NC-SA 4.0; retained dataset stays local and is not redistributed','gold_revealed':False,'calibration_executed':False,'scientific_matched_environment_claim_allowed':False,'note':'Document-count-only engine smoke run on authenticated DAMOS records with nonempty source transcription; 42 missing-surface records are explicitly excluded. It tests reproducibility and output integrity, not detector performance or cross-script equivalence.'})
    pathlib.Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
