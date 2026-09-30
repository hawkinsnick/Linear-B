#!/usr/bin/env python3
import json,pathlib
from build_observation_corpus import build_records,FIELD_MAP,is_forbidden_field
R=pathlib.Path(__file__).resolve().parents[1];policy=json.loads((R/'research/blind-field-policy.json').read_text())
d={'id':'A','content':'a-ko','scribe':'42','inventory':'INV1','site':'Pylos','translation':'secret','lemma':'secret'}
r=build_records([d],policy)[0]
assert r['observable']['transliteration_surface']=='a-ko'
assert r['observable']['hand_label']=='42' and r['observable']['inventory_number']=='INV1'
assert 'layout' not in r['observable'] and 'sign_sequence' not in r['observable']
assert 'secret' not in json.dumps(r)
assert build_records([{'id':'B','content':None}],policy)[0]['observable']['transliteration_surface'] is None
assert FIELD_MAP==json.loads((R/'research/damos-observation-field-map-v1.json').read_text())['mapping']
for docs in [[d,d],[{'id':''}],[{'id':'A','content':42}]]:
    try:build_records(docs,policy)
    except ValueError:pass
    else:raise AssertionError('invalid source accepted')
print('PASS: content/scribe/inventory mapping, unknown preservation, excluded gold and malformed source refusal')
