"""Shared field-name policy for builder and leakage auditor."""
import json,pathlib,re
R=pathlib.Path(__file__).resolve().parents[1]
def load_policy():return json.loads((R/'research/blind-field-policy.json').read_text())
def is_forbidden_field(k,policy):
    key=str(k).lower()
    if key in {str(x).lower() for x in policy['allowed_observation_fields']}:return False
    return any(key==str(p).lower() or str(p).lower() in re.split(r'[_\-]+',key) for p in policy['forbidden_gold_field_patterns'])
