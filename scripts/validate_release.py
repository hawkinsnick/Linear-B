#!/usr/bin/env python3
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];L=lambda p:json.loads((R/p).read_text())
def D(m):print("FAIL:",m);raise SystemExit(1)
v=(R/"VERSION").read_text().strip()
if v!="4.9.0":D("VERSION")
for p in ["analysis/4.9.0_status.json","analysis/hostile-audit-4.9.0.json","research/experiment-gates.json"]:
 if L(p).get("version")!=v:D("version drift "+p)
s=L("analysis/4.9.0_status.json")
if s["release_5_0_allowed"]:D("5.0 gate improperly open")
if any(s["executed"].values()):D("unsubstantiated execution claim")
for p in ["research/blind-calibration-spec-v1.json","research/scoring-spec-v1.json","research/degradation-spec-v1.json"]:
 if L(p)["result"] is not None:D("unsubstantiated result")
print(json.dumps({"version":v,"status":"PASS","protocols":"FROZEN","execution":"BLOCKED","release_5_0_allowed":False}))
