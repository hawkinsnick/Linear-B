#!/usr/bin/env python3
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[1]
policy=json.loads((root/"research"/"blind-field-policy.json").read_text())
def forbidden(k):
 key=k.lower(); allowed={x.lower() for x in policy["allowed_observation_fields"]}
 if key in allowed:return False
 return any(key==p.lower() or p.lower() in re.split(r"[_\\-]+",key) for p in policy["forbidden_gold_field_patterns"])
assert not forbidden("inventory_number")
assert forbidden("number") and forbidden("grammatical_number") and forbidden("normalized_reading")
for s in ("build_observation_corpus.py","audit_gold_leakage.py"):
 t=(root/"scripts"/s).read_text(); assert 'policy["forbidden_gold_field_patterns"]' in t and 'policy["allowed_observation_fields"]' in t
print(json.dumps({"status":"PASS","policy_version":policy["version"],"regressions":4,"scripts_checked":2}))
