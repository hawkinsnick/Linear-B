#!/usr/bin/env python3
"""Validate audit accounting and fail closed on unsupported readiness claims."""
import hashlib,json,pathlib
from build_pre_expert_audit import ROOT,PINS
report=json.loads((ROOT/'analysis/pre-expert-source-audit.json').read_text());project=report['project'];n=report['documents']
assert report['source_sha256']==PINS[project]
assert n==report['unique_source_ids']==({'Linear-A':802,'Linear-B':5932}[project])
assert not report['prospective_outcomes_inspected'] and not report['calibration_executed'] and not report['redistributes_source_records']
assert report['implementation_sha256']==hashlib.sha256((ROOT/'scripts/build_pre_expert_audit.py').read_bytes()).hexdigest()
for c in report['field_coverage'].values():assert c['present']+c['missing_or_empty']==c['denominator']==n
for counts in report['group_counts'].values():assert sum(counts.values())==n
assert report['source_license']=='CC BY-NC-SA 4.0'
if project=='Linear-A':
 assert report['occurrences']==sum(report['occurrence_kinds'].values())==5144
 assert report['source_word_groups']==1401 and report['source_sign_entries']==376
 assert report['unresolved_cases']['adjudicated']==0
else:assert report['field_coverage']['content']['present']==5890
contract=json.loads((ROOT/'research/pre-expert-maximum.json').read_text())
if contract['state']=='PRE_EXPERT_MAXIMUM':
 assert all(x['status'] in ['COMPLETE','SOURCE_BLOCKED'] for x in contract['machine_resolvable'])
 for x in contract['machine_resolvable']:
  if x['status']=='SOURCE_BLOCKED':assert x.get('blocker') and x.get('evidence')
assert all(x['status'] in ['COMPLETE','SOURCE_BLOCKED'] for x in contract['machine_resolvable']), 'Undispositioned machine task'
for m in contract['machine_resolvable']:
 if m['status']=='SOURCE_BLOCKED':assert m.get('blocker'), 'No concrete blocker'
 for path in m.get('evidence',[]):assert (ROOT/path).is_file(),path
print('Pre-expert source accounting PASS; no scientific gate opened')
