#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("condition",choices=["LB-RAW","LB-STRUCTURAL","LB-CONTEXT","LB-PHONETIC","LB-GOLD"]);a=ap.parse_args()
rows=json.loads(Path(a.observations).read_text(encoding="utf-8"))
if not isinstance(rows,list) or not rows: raise SystemExit("REFUSING: observations must be a nonempty JSON list")
if any(not isinstance(r,dict) or not isinstance(r.get("observable",{}),dict) for r in rows): raise SystemExit("REFUSING: malformed observation envelope")
req={"LB-RAW":({"document_id"},{"graphical_sign_identity"}),"LB-STRUCTURAL":({"document_id"},{"graphical_sign_identity","layout"}),"LB-CONTEXT":({"document_id"},{"graphical_sign_identity","layout","site"}),"LB-PHONETIC":({"document_id"},{"transliteration_surface"}),"LB-GOLD":({"document_id"},{"lemma"})}[a.condition]
for index,row in enumerate(rows):
 missing=sorted((req[0]-set(row))|(req[1]-set(row.get("observable",{}))))
 if missing: raise SystemExit("REFUSING "+a.condition+": record "+str(index)+" missing required fields: "+",".join(missing))
 if not isinstance(row.get("document_id"),str) or not row["document_id"].strip(): raise SystemExit("REFUSING: empty/malformed document_id at record "+str(index))
msg={"condition":a.condition,"field_preflight":"PASS","envelope":"document_id + observable"}
if a.condition=="LB-PHONETIC": msg["warning"]="Uses deciphered conventional transliteration; not a graphical-sign baseline."
if a.condition=="LB-GOLD": msg["note"]="Field presence only; gold access/alignment/scoring gates still apply."
print(json.dumps(msg))

