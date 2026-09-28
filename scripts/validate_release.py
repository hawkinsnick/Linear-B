#!/usr/bin/env python3
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]; L=lambda p:json.loads((R/p).read_text())
def die(m): print("FAIL:",m);raise SystemExit(1)
v=(R/"VERSION").read_text().strip()
if v!="4.9.1":die("VERSION")
x=L("analysis/4.9.1_transport-fix.json")
if x["version"]!=v or x["scientific_gate_change"]:die("transport correction contract")
g=L("research/experiment-gates.json")
if g["version"]!="4.9.0":die("4.9.0 scientific gates must remain unchanged pending CI evidence")
print(json.dumps({"version":v,"status":"PASS","purpose":"transport verification","scientific_gates":"UNCHANGED"}))
