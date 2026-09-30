#!/usr/bin/env python3
"""Regression-test that builder/auditor policy coverage cannot silently diverge."""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[1]
policy=json.loads((root/"research"/"blind-field-policy.json").read_text(encoding="utf-8"))
forbidden=policy["forbidden_gold_field_patterns"]
assert "number" in forbidden and "normalized_reading" in forbidden
for script in ("build_observation_corpus.py","audit_gold_leakage.py"):
 text=(root/"scripts"/script).read_text(encoding="utf-8")
 assert 'policy["forbidden_gold_field_patterns"]' in text, f"{script} does not load forbidden patterns from policy"
print(json.dumps({"status":"PASS","policy_version":policy["version"],"patterns_checked":len(forbidden),"scripts_checked":2}))
