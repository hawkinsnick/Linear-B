#!/usr/bin/env python3
"""Audit pinned sources; emit record-level derivatives only in ignored directories.
No prospective cohort, predictions, experiment outcomes or linguistic gold is read.
"""
import argparse, collections, csv, hashlib, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
PINS={'Linear-A':'9a5e4783146144fc5ac54c5dc2b372b39cc0e0ea40ca15207243f8c539f03dd8','Linear-B':'eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2'}
def dump(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def present(value):
 return value is not None and (not isinstance(value,str) or bool(value.strip())) and value!=[]
def coverage(docs,fields):
 return {f:{'present':sum(present(d.get(f)) for d in docs),'missing_or_empty':sum(not present(d.get(f)) for d in docs),'denominator':len(docs)} for f in fields}
def groups(docs,fields):
 return {f:dict(sorted(collections.Counter(str(d.get(f)) if present(d.get(f)) else '<UNKNOWN>' for d in docs).items())) for f in fields}
def pointer(source_hash,index,field=None):
 return {'input_sha256':source_hash,'json_pointer':f'/documents/{index}'+('/'+field if field else ''),'license':'CC BY-NC-SA 4.0','status':'SOURCE_REPORTED_NOT_INDEPENDENTLY_VERIFIED'}
def validate_source(data,project):
 docs=data['documents'];assert isinstance(docs,list) and docs,'empty documents'
 ids=[d['id'] for d in docs];assert all(isinstance(x,str) and x.strip() for x in ids),'missing id'
 assert len(ids)==len(set(ids)),'duplicate source id'
 assert data['_meta']['license']=='CC BY-NC-SA 4.0','source rights drift'
 if project=='Linear-A':
  for d in docs:
   assert isinstance(d['attestations'],list),'bad attestations'
   for a in d['attestations']:
    assert isinstance(a,dict) and {'sign','kind','word','series','number','raw_flags'}<=a.keys(),'incomplete attestation'
    assert a['word'] is None or type(a['word']) is int and a['word']>=0,'invalid source word index'
    assert a['number'] is None or type(a['number']) is int,'invalid sign number'
 else:
  for d in docs:
   for f in ['content','site','support','scribe','inventory','find_area','find_spot','museum','joins']:
    assert d.get(f) is None or isinstance(d[f],str),'invalid field type: '+f
 return docs
def write_csv(path,rows,fields):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def build(data,project,source_hash):
 docs=validate_source(data,project);local={};audit={'schema_version':'1.0','project':project,'source_sha256':source_hash,'source_license':'CC BY-NC-SA 4.0','documents':len(docs),'unique_source_ids':len(docs),'scope':'Exact authenticated derivative snapshot only; not all surviving inscriptions or physical objects.','source_independence':'ONE_DERIVATIVE_SOURCE_NOT_INDEPENDENT_VALIDATION','prospective_outcomes_inspected':False,'calibration_executed':False,'redistributes_source_records':False}
 fields=['site','typology','period','dimensions_cm','reference_url'] if project=='Linear-A' else ['content','site','support','scribe','inventory','find_area','find_spot','museum','joins','heading','heading_short','chronology','permalink']
 audit['field_coverage']=coverage(docs,fields);audit['group_counts']=groups(docs,['site','typology','period'] if project=='Linear-A' else ['site','support'])
 audit['source_attribution']=data['_meta'].get('attribution')
 local['source-metadata.json']=[{k:data['_meta'].get(k) for k in ['license','attribution','cite','version','generated','source_sha256']}]
 records=[{'record_id':project+':'+d['id'],'source_record_id':d['id'],'source_fields':{f:d.get(f) for f in fields},'provenance':pointer(source_hash,i)} for i,d in enumerate(docs)]
 local['records.json']=records
 if project=='Linear-A':
  occ=[];words=[]
  for i,d in enumerate(docs):
   wg=collections.defaultdict(list)
   for j,a in enumerate(d['attestations']):
    sign_id=f"{a['series']}:{a['number']}" if a['series'] and a['number'] is not None else None
    occ.append({'occurrence_id':f"Linear-A:{d['id']}:{j}",'document_id':d['id'],'sequence_index':j,'source_fields':a,'sign_id':sign_id,'phonetic_value':None,'provenance':pointer(source_hash,i,f'attestations/{j}')})
    if a['word'] is not None:wg[a['word']].append(j)
   for word,indices in sorted(wg.items()):words.append({'word_id':f"Linear-A:{d['id']}:word:{word}",'document_id':d['id'],'source_word_index':word,'occurrence_indices':indices,'definition':'SigLA source grouping; not a confirmed linguistic word','provenance':pointer(source_hash,i,'attestations')})
  local['occurrences.json']=occ;local['source-words.json']=words
  concordance=[]
  for i,s in enumerate(data['signs']):
   concordance.append({'source_sign_key':f"{s['series']}:{s['number']}",'source_fields':s,'linear_a_phonetic_value':None,'linear_b_equivalence_status':'NOT_ESTABLISHED_BY_THIS_SOURCE','provenance':{'input_sha256':source_hash,'json_pointer':f'/signs/{i}','license':'CC BY-NC-SA 4.0'}})
  local['sign-concordance.json']=concordance
  sign_counts=collections.Counter(s['source_sign_key'] for s in concordance);known=set(sign_counts)
  audit.update({'occurrences':len(occ),'source_word_groups':len(words),'source_sign_entries':len(concordance),'unique_source_sign_keys':len(known),'duplicate_sign_keys':sum(v-1 for v in sign_counts.values()),'occurrences_without_sign_key':sum(x['sign_id'] is None for x in occ),'occurrences_with_sign_key_absent_from_sign_table':sum(x['sign_id'] is not None and x['sign_id'] not in known for x in occ),'occurrence_kinds':dict(sorted(collections.Counter(x['source_fields']['kind'] for x in occ).items())),'numeral_quantities':'NOT_PROVIDED_BY_SOURCE','raw_flags':'PRESERVED_UNDECODED_NO_CERTAINTY_OR_DAMAGE_INFERENCE','source_word_boundary':'SOURCE_EDITORIAL_GROUPING_NOT_GORILA_EQUIVALENCE'})
 else:
  local['identity-register.json']=[{'document_id':d['id'],'heading':d.get('heading'),'heading_short':d.get('heading_short'),'joins_source_text':d.get('joins'),'permalink':d.get('permalink'),'physical_object_id':None,'join_resolution':'SOURCE_TEXT_PRESERVED_NOT_ADJUDICATED','provenance':pointer(source_hash,i)} for i,d in enumerate(docs)]
  collisions={}
  for f in ['heading','heading_short','inventory']:
   c=collections.Counter(d[f] for d in docs if present(d.get(f)));collisions[f]={'duplicated_values':sum(n>1 for n in c.values()),'records_in_collision_groups':sum(n for n in c.values() if n>1)}
  audit['identity_collisions']=collisions
  for f in ['graphical_sign_identity','layout_coordinates','damage_annotation','linguistic_annotation']:
   audit['field_coverage'][f]={'present':0,'missing_or_empty':len(docs),'denominator':len(docs),'boundary':'NOT_EXPORTED_IN_AUTHENTICATED_DERIVATIVE'}
  audit['transliteration_boundary']='Editorial transliteration preserves markup; does not supply graphical sign occurrence identity, geometry, or aligned linguistic gold.'
 return audit,local
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source',type=pathlib.Path);ap.add_argument('--local-output',type=pathlib.Path,default=ROOT/'data/generated/pre-expert');ap.add_argument('--report',type=pathlib.Path,default=ROOT/'analysis/pre-expert-source-audit.json');args=ap.parse_args()
 project='Linear-A' if (ROOT/'data/unresolved_cases.csv').exists() else 'Linear-B'
 raw=args.source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
 if digest!=PINS[project]:raise SystemExit('Refusing unverified source bytes')
 target=args.local_output.resolve();allowed=[(ROOT/'data/generated').resolve(),(ROOT/'data/private').resolve()]
 if not any(target==p or p in target.parents for p in allowed):raise SystemExit('Record-level exports must stay in ignored data/generated or data/private')
 audit,local=build(json.loads(raw),project,digest);target.mkdir(parents=True,exist_ok=True)
 for name,rows in local.items():dump(target/name,rows)
 if project=='Linear-A':
  docs=json.loads(raw)['documents'];ins=[];oc=[];prov=[]
  for i,d in enumerate(docs):
   pid=f'SIGLA-V2:{i}';ins.append({'document_id':d['id'],'source_id':'SIGLA-DECODED-V2','site_name':d.get('site'),'document_type':d.get('typology'),'period':d.get('period'),'dimensions':json.dumps(d.get('dimensions_cm')),'source_url':d.get('reference_url'),'source_license':'CC BY-NC-SA 4.0','provenance_id':pid})
   prov.append({'provenance_id':pid,'source_id':'SIGLA-DECODED-V2','source_record':d['id'],'input_sha256':digest,'json_pointer':f'/documents/{i}','license':'CC BY-NC-SA 4.0'})
  for x in local['occurrences.json']:oc.append({'occurrence_id':x['occurrence_id'],'document_id':x['document_id'],'sequence_index':x['sequence_index'],'word_index':x['source_fields']['word'],'sign_id':x['sign_id'],'source_display':x['source_fields']['sign'],'source_license':'CC BY-NC-SA 4.0'})
  for name,rows in [('inscriptions',ins),('sign_occurrences',oc),('provenance',prov)]:write_csv(target/(name+'.csv'),rows,list(rows[0]))
  sites=[{'site_name':k,'source_record_count':v,'source_id':'SIGLA-DECODED-V2','source_license':'CC BY-NC-SA 4.0'} for k,v in audit['group_counts']['site'].items()];write_csv(target/'sites.csv',sites,list(sites[0]))
  cases=list(csv.DictReader((ROOT/'data/unresolved_cases.csv').open()));lookup=collections.defaultdict(list)
  for i,d in enumerate(docs):lookup[re.sub(r'\s+','',d['id'])].append((i,d))
  queue=[]
  for c in cases:
   matches=lookup.get(re.sub(r'\s+','',c['document_id']),[])
   queue.append({**c,'source_candidates':[{'source_id':d['id'],'reference_url':d.get('reference_url'),'provenance':pointer(digest,i)} for i,d in matches],'status':'UNRESOLVED_REQUIRES_PRIMARY_COLLATION_OR_EXPERT','identity_match_rule':'Whitespace removal only; no fuzzy or join inference','source_match_count':len(matches)})
  dump(target/'unresolved-source-locators.json',queue);audit['unresolved_cases']={'total':len(queue),'with_exact_whitespace_only_source_match':sum(bool(x['source_candidates']) for x in queue),'without_match':sum(not x['source_candidates'] for x in queue),'adjudicated':0}
 audit['local_export_manifest']=[{'file':name,'records':len(rows),'sha256':hashlib.sha256((target/name).read_bytes()).hexdigest()} for name,rows in sorted(local.items())]
 audit['implementation_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest();dump(args.report,audit);print(json.dumps({k:audit[k] for k in ['project','documents','unique_source_ids','prospective_outcomes_inspected','calibration_executed']}))
if __name__=='__main__':main()
