#!/usr/bin/env python3
"""Replay documentary appendix bindings; visual review and scholarly acceptance are separate."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def verify(receipt,raw):
    if hashlib.sha256(raw).hexdigest()!=receipt['native_sha256']:raise ValueError('native appendix example changed')
    data=json.loads(raw);seen=set()
    if len(receipt['assertions'])!=10:raise ValueError('fixed appendix scope changed')
    for a in receipt['assertions']:
        p=a['native_pointer']
        if p in seen:raise ValueError('duplicate appendix claim')
        seen.add(p)
        bits=p.split('/')[1:]
        if bits[0]=='document' and len(bits)==2:actual=data['document'][bits[1]]
        elif bits[0]=='units' and len(bits)==2 and bits[1] in [str(i) for i in range(7)]:
            unit=data['units'][int(bits[1])];actual={k:unit[k] for k in ['published_xml_id','element','source_line','published_xml_line','category']}
        else:raise ValueError('unregistered appendix claim pointer')
        if actual!=a['expected'] or a['comparison']!='MATCH':raise ValueError('documentary claim differs from native attribution')
    expected={'/document/'+k for k in ['published_xml_id','published_damos_item_id','standard_label']}|{'/units/'+str(i) for i in range(7)}
    if seen!=expected:raise ValueError('appendix assertion membership changed')
    for k in ['current_damos_export_delivered','same_version_word_crosswalk_verified','linguistic_gold_acquired','calibration_executed','external_specialist_review','source_pdf_or_images_redistributed']:
        if receipt[k] is not False:raise ValueError('unsupported evidence upgrade')
    if receipt['reading_changes']!=0:raise ValueError('no reading change authorized')
    return len(seen)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--native-root',type=Path,default=ROOT);p.add_argument('--receipt',type=Path,default=ROOT/'research/published-appendix-recheck-2026-10-25.json');p.add_argument('--pdf',type=Path);a=p.parse_args();r=json.loads(a.receipt.read_text());path=Path(r['native_path'])
    if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe appendix input path')
    count=verify(r,(a.native_root/path).read_bytes())
    if a.pdf:
        raw=a.pdf.read_bytes()
        if not raw.startswith(b'%PDF') or len(raw)!=r['publication']['bytes'] or hashlib.sha256(raw).hexdigest()!=r['publication']['sha256']:raise ValueError('wrong appendix publication copy')
    print(json.dumps({'status':'PASS_RECORDED_APPENDIX_ATTRIBUTIONS','claim_bundles':count,'pdf_hash_checked':bool(a.pdf),'visual_review_automatically_proven':False,'scholarly_acceptance_granted':False}))
if __name__=='__main__':main()
