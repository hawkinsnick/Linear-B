"""Replay attributed source metadata; reject silent promotion to scholarly acceptance."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/damos-published-id-example-2026-10-14.json'
PIN='901c0ba6354191b921cdeddf53c18f21155d420ace4ed3d5cc2f2977ba459490'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(root=ROOT):
 x=json.loads((root/REGISTER).read_text())
 if digest(x)!=PIN:raise ValueError('inspected source identity, categories or acceptance boundary changed')
 if len(x['units'])!=7 or len({u['published_xml_id'] for u in x['units']})!=7:raise ValueError('published unit ID drift')
 from collections import Counter
 if Counter(u['category'] for u in x['units'])!={'lexical_word':5,'logogram':1,'numeral':1}:raise ValueError('word denominator conflation')
 gates=json.loads((root/'research/gold-acquisition-gate.json').read_text())
 if gates['release_5_0_allowed'] is not False or not gates['state'].startswith('BLOCKED'):raise ValueError('example promoted to calibration gold')
 return {'status':'PASS_PUBLISHED_ID_EXAMPLE_ONLY','published_item_ids':1,'published_unit_ids':7,'lexical_words':5,'same_snapshot_crosswalk_acquired':False,'calibration_executed':False}
if __name__=='__main__':print(json.dumps(validate()))
