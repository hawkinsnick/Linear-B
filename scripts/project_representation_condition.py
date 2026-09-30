#!/usr/bin/env python3
"""Project authenticated observation records into frozen detector-visible conditions."""
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("condition");ap.add_argument("--out",required=True);a=ap.parse_args()
 rows=json.loads(Path(a.observations).read_text(encoding="utf-8"))
 if not isinstance(rows,list): raise SystemExit("REFUSING: observations must be a list")
 cid=a.condition.upper()
 if cid not in {"LB-RAW","LB-STRUCTURAL","LB-CONTEXT","LB-PHONETIC"}: raise SystemExit("REFUSING: unknown or gold condition")
 out=[]
 for r in rows:
  o=r.get("observable",{})
  did=r.get("document_id")
  if not did or not isinstance(o,dict): raise SystemExit("REFUSING: malformed observation record")
  graphical=o.get("graphical_sign_identity")
  if cid in {"LB-RAW","LB-STRUCTURAL","LB-CONTEXT"} and not graphical:
   raise SystemExit(cid+" UNAVAILABLE: source lacks graphical_sign_identity; transliteration must not substitute for raw sign identity")
  x={"document_id":did}
  if cid=="LB-RAW": x["graphical_sign_identity"]=graphical
  elif cid=="LB-STRUCTURAL":
   x.update({"graphical_sign_identity":graphical,"layout":o.get("layout")})
  elif cid=="LB-CONTEXT":
   x.update({"graphical_sign_identity":graphical,"layout":o.get("layout"),"site":o.get("site"),"hand_label":o.get("hand_label"),"support":o.get("support"),"find_area":o.get("find_area"),"find_spot":o.get("find_spot")})
  else:
   if not isinstance(o.get("transliteration_surface"),str) or not o["transliteration_surface"].strip(): raise SystemExit("LB-PHONETIC UNAVAILABLE: missing transliteration_surface")
   x["transliteration_surface"]=o["transliteration_surface"]
  out.append(x)
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 print(json.dumps({"condition":cid,"records":len(out),"output":a.out}))
if __name__=="__main__": main()
