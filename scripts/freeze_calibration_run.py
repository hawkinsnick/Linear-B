"""Bind answer-free alignment, observations, predictions and scoring before gold reveal.

This hashes sealed answers without parsing them and grants no authority, rights or
scientific acceptance. All private output must remain outside the repository.
"""
import argparse,hashlib,json
from pathlib import Path
from check_calibration_intake import check,digest_file,nonempty
ROOT=Path(__file__).resolve().parents[1]
def freeze(manifest,base):
 if manifest.get('format')!='linear-b-pre-reveal-freeze-v1':raise ValueError('unsupported freeze format')
 if set(manifest)!={'format','intake_manifest','prediction_payload','scoring_protocol','predictor_implementation','observation_sha256','annotation_sha256','source_snapshot','task','experiment_id'}:raise ValueError('unexpected or missing freeze fields')
 p=Path(nonempty(manifest['intake_manifest'],'intake manifest'))
 if p.is_absolute() or not (base/p).resolve().is_relative_to(base.resolve()):raise ValueError('intake outside package')
 intake=json.loads((base/p).read_text());report=check(intake,(base/p).parent)
 for key,value in [('observation_sha256',report['observation_payload_sha256']),('annotation_sha256',report['annotation_payload_sha256']),('source_snapshot',report['source_snapshot'])]:
  if manifest[key]!=value:raise ValueError('freeze/intake binding mismatch: '+key)
 if report['exact_matches']==0 or report['ambiguous_matches'] or report['unmatched_observation'] or report['unmatched_gold']:raise ValueError('scope must be exactly aligned; unresolved units require a separately declared pilot')
 task=manifest['task']
 if task not in {'known_answer_linguistic','degraded_graphical'}:raise ValueError('undeclared calibration task')
 if task=='degraded_graphical' and report['graphical_occurrences']==0:raise ValueError('graphical component absent')
 files={key:digest_file(base,manifest[key]) for key in ['prediction_payload','scoring_protocol','predictor_implementation']}
 paths=[(base/manifest[k]['path']).resolve() for k in files]
 paths += [((base/p).parent/intake[k]['path']).resolve() for k in ['observation_payload','annotation_payload']]
 if len(set(map(str,paths)))!=len(paths):raise ValueError('predictions/protocol/implementation/answers/observations must be distinct files')
 nonempty(manifest['experiment_id'],'experiment identifier')
 return {'format':'linear-b-pre-reveal-freeze-receipt-v1','experiment_id':manifest['experiment_id'],'task':task,'source_snapshot':report['source_snapshot'],'scope':report['scope'],'exact_matches':report['exact_matches'],'observation_sha256':manifest['observation_sha256'],'sealed_annotation_sha256':manifest['annotation_sha256'],'frozen_file_sha256':files,'intake_manifest_sha256':hashlib.sha256((base/p).read_bytes()).hexdigest(),'freeze_manifest_sha256':hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'answers_loaded':False,'prediction_semantics_validated':False,'scoring_semantics_validated':False,'source_authority_verified':False,'rights_review_complete':False,'gold_reveal_authorized':False,'experiment_gates_changed':False,'calibration_executed':False,'boundary':'A byte binding is not proof of preregistration chronology, correct predictions, authoritative gold or valid scoring. Independent source/rights review and the native gate authority remain required.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.resolve().is_relative_to(ROOT) or a.out.exists():p.error('new private output outside the repository required')
 try:
  result=freeze(json.loads(a.manifest.read_text()),a.manifest.parent)
  with a.out.open('x') as out:out.write(json.dumps(result,indent=2)+'\n')
 except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,str(e)+'\n')
 print('Private pre-reveal byte binding written; no answers loaded or calibration authorized.')
if __name__=='__main__':main()
