#!/usr/bin/env python3
"""Audit every exported field against the authenticated source bytes."""
import argparse,hashlib,json,pathlib
from jsonschema import Draft202012Validator
R=pathlib.Path(__file__).resolve().parents[1]
def audit(source,export):
    raw=source.read_bytes();contract=json.loads((R/'research/damos-observation-field-map-v1.json').read_text())
    if hashlib.sha256(raw).hexdigest()!=contract['source_sha256']:raise ValueError('source digest mismatch')
    docs=json.loads(raw)['documents'];rows=json.loads(export.read_bytes());source_ids=[d['id'] for d in docs]
    if not isinstance(rows,list) or len(rows)!=len(docs) or len(set(source_ids))!=len(docs):raise ValueError('source/export count or IDs invalid')
    if [r['document_id'] for r in rows]!=source_ids:raise ValueError('source/export identity order drift')
    schema=json.loads((R/'schemas/observation-record-v1.schema.json').read_text());validator=Draft202012Validator(schema)
    mapping=contract['mapping']
    for d,r in zip(docs,rows):
        validator.validate(r)
        if set(r['observable'])!=set(mapping):raise ValueError('unknown/invented or missing observable fields')
        for target,field in mapping.items():
            if r['observable'][target]!=d.get(field):raise ValueError('field mapping mismatch: '+target)
        if r['provenance']['input_sha256']!=contract['source_sha256']:raise ValueError('provenance input mismatch')
    return {'status':'PASS','source_sha256':contract['source_sha256'],'observation_export_sha256':hashlib.sha256(export.read_bytes()).hexdigest(),'records':len(rows),'nonempty_transcription_surfaces':sum(bool(r['observable']['transliteration_surface']) for r in rows),'null_or_empty_surfaces':sum(not bool(r['observable']['transliteration_surface']) for r in rows),'mapped_scribe_labels':sum(bool(r['observable']['hand_label']) for r in rows),'mapped_inventory_numbers':sum(bool(r['observable']['inventory_number']) for r in rows),'all_source_field_values_preserved':True,'graphical_sign_identity_available':False,'linguistic_gold_available':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('export',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path);a=p.parse_args();result=audit(a.source,a.export);text=json.dumps(result,indent=2)+'\n'
    if a.out:a.out.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
