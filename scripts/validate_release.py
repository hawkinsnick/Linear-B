#!/usr/bin/env python3
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];L=lambda p:json.loads((R/p).read_text())
def die(m): print("FAIL:",m);raise SystemExit(1)
v=(R/"VERSION").read_text().strip()
if v!="4.2.0":die("VERSION")
for p in ["analysis/4.2.0_observation_status.json","research/experiment-gates.json","research/blind-field-policy.json"]:
 if L(p).get("version")!=v:die("version drift "+p)
s=L("analysis/4.2.0_observation_status.json")
if s["observation_records_materialized"]!=0 or s["leakage_audit_result"] is not None:die("unsupported populated-corpus claim")
g=L("research/experiment-gates.json")["experiments"]
if any(x["claim_allowed"] for x in g):die("blocked experiment permits claim")
pol=L("research/blind-field-policy.json")
if pol["policy"]!="deny_by_default":die("blind policy")
print(json.dumps({"version":v,"status":"PASS","observation_contract":"READY","population":"BLOCKED"}))
