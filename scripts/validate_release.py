#!/usr/bin/env python3
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def L(p): return json.loads((R/p).read_text())
def die(m): print("FAIL:",m); raise SystemExit(1)
v=(R/"VERSION").read_text().strip()
if v!="4.0.0": die("VERSION")
for p in ["analysis/4.0.0_status.json","analysis/release-gates-4.0.0.json","research/experiment-gates.json"]:
 if L(p).get("version")!=v: die("version drift "+p)
src={x["source_id"] for x in L("sources/registry.json")}
for x in L("provenance/source-lineage.json"):
 if x["source_id"] not in src: die("orphan lineage source")
status=L("analysis/4.0.0_status.json")
if status["damos_bytes_materialized"]: die("unexpected materialized-byte claim")
if status["known_answer_calibration_result"] is not None: die("unexpected calibration result")
gates=L("research/experiment-gates.json")["experiments"]
if any(x["claim_allowed"] for x in gates): die("blocked experiment permits claim")
props=L("schemas/linear-b-record.schema.json")["properties"]
if "observation" not in props or "gold" not in props: die("missing observation/gold separation")
print(json.dumps({"version":v,"status":"PASS","research_gates":[x["state"] for x in gates]}))
