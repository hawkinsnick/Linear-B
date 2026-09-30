#!/usr/bin/env python3
"""Export explicit permitted fields from checksum-pinned DAMOS v2 bytes."""
import hashlib,json,pathlib,sys
from blind_field_policy import load_policy,is_forbidden_field
R=pathlib.Path(__file__).resolve().parents[1]
EXPECTED='eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2'
FIELD_MAP={'transliteration_surface':'content','support':'support','site':'site','find_area':'find_area','find_spot':'find_spot','hand_label':'scribe','museum':'museum','inventory_number':'inventory'}
def build_records(documents,policy):
    if not isinstance(documents,list) or not documents:raise ValueError('expected nonempty documents list')
    rows=[];seen=set()
    for d in documents:
        if not isinstance(d,dict) or not isinstance(d.get('id'),str) or not d['id'].strip() or d['id'] in seen:raise ValueError('missing/duplicate document id')
        seen.add(d['id'])
        obs={name:d.get(source) for name,source in FIELD_MAP.items()}
        if any(v is not None and not isinstance(v,str) for v in obs.values()):raise ValueError('unexpected source field type')
        # Absent source information stays absent/unknown, never an invented empty observation.
        rows.append({'document_id':d['id'],'source_id':'DAMOS-DERIVATIVE-V2','observable':obs,'provenance':{'input_sha256':EXPECTED,'derivation':'build_observation_corpus.py','blind_field_policy_version':policy['version'],'field_mapping':'research/damos-observation-field-map-v1.json'}})
    return rows
def main():
    src=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else 'data/derived/linear-b-observation-v1.json')
    raw=src.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise SystemExit('Refusing unverified input')
    data=json.loads(raw);policy=load_policy()
    rows=build_records(data['documents'],policy)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')))
    print(json.dumps({'records':len(rows),'nonempty_transcription_surfaces':sum(bool(x['observable']['transliteration_surface']) for x in rows),'mapped_scribe_labels':sum(bool(x['observable']['hand_label']) for x in rows),'mapped_inventory_numbers':sum(bool(x['observable']['inventory_number']) for x in rows),'output':str(out)}))
if __name__=='__main__':main()
