#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("condition",choices=["LB-RAW","LB-STRUCTURAL","LB-CONTEXT","LB-PHONETIC","LB-GOLD"]);a=ap.parse_args()
rows=json.loads(Path(a.observations).read_text(encoding="utf-8"))
if not isinstance(rows,list) or not rows: raise SystemExit("REFUSING: observations must be a nonempty JSON list")
keys=set().union(*(r.keys() for r in rows if isinstance(r,dict)))
req={"LB-RAW":{"graphical_sign_identity"},"LB-STRUCTURAL":{"graphical_sign_identity","document_id"},"LB-CONTEXT":{"graphical_sign_identity","document_id","site"},"LB-PHONETIC":{"transliteration_surface","document_id"},"LB-GOLD":{"lemma"}}[a.condition]
missing=sorted(req-keys)
if missing: raise SystemExit("REFUSING "+a.condition+": missing required fields: "+",".join(missing))
if a.condition!="LB-PHONETIC":
 print(json.dumps({"condition":a.condition,"field_preflight":"PASS","note":"Field presence only; scientific execution may have additional gates."}))
else:
 print(json.dumps({"condition":a.condition,"field_preflight":"PASS","warning":"Uses deciphered conventional transliteration; not a graphical-sign baseline."}))
