#!/usr/bin/env python3
"""Validate source-specific action plans; never certify scientific completion."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'research/source-action-plan.json').read_text())
assert p['format']=='corpus-source-action-plan-v1'
assert p['claim_scope']=='BOUNDED_SOURCE_AUDIT_NOT_GLOBAL_EXHAUSTION'
seen=set()
for task in p['tasks']:
    assert task['id'] not in seen;seen.add(task['id'])
    assert task['dependency'] in {'ACCESS','PERMISSION','SOURCE_DELIVERY','RECONCILIATION','HUMAN_REVIEW'}
    assert task['status'] in {'OPEN','BLOCKED','WAITING_FOR_EVIDENCE','COMPLETE'}
    for field in ('source','next_action','acceptance'):
        assert isinstance(task[field],str) and task[field].strip(),(task['id'],field)
    assert task['evidence']
    for rel in task['evidence']:
        file=(R/rel).resolve()
        assert file.is_relative_to(R) and file.is_file(),(task['id'],rel)
assert p['rights_only_ready'] is False
assert any(t['dependency']!='PERMISSION' and t['status']!='COMPLETE' for t in p['tasks'])
print(p['corpus']+': source-action plan valid; rights-only readiness remains false')
