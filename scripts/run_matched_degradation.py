#!/usr/bin/env python3
"""Deterministic document-level degradation for measured corpus-equivalence targets."""
import argparse,hashlib,json,random
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("target");ap.add_argument("--seed",type=int,required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
rows=json.loads(Path(a.observations).read_text(encoding="utf-8")); target=json.loads(Path(a.target).read_text(encoding="utf-8"))
allowed={"document_count"}
unknown=[k for k,v in target.get("dimensions",{}).items() if v.get("status")!="measured" and v.get("use",False)]
unsupported=[k for k,v in target.get("dimensions",{}).items() if v.get("use",False) and k not in allowed]
if unknown: raise SystemExit("REFUSING: requested unknown/unmeasured dimensions: "+",".join(unknown))
if unsupported: raise SystemExit("REFUSING: requested dimensions not executable in v0.1: "+",".join(unsupported))
dc=target["dimensions"].get("document_count",{})
if not dc.get("use") or dc.get("status")!="measured": raise SystemExit("REFUSING: v0.1 requires measured document_count")
n=int(dc["value"])
if n<1 or n>len(rows): raise SystemExit("REFUSING: impossible document_count target")
rng=random.Random(a.seed); idx=sorted(rng.sample(range(len(rows)),n)); kept=[rows[i] for i in idx]
ids=[r["document_id"] for r in kept]
manifest={"engine":"matched-degradation-v0.1","seed":a.seed,"input_records":len(rows),"target":{"document_count":n},"realized":{"document_count":len(kept)},"retained_document_ids":ids,"retained_ids_sha256":hashlib.sha256(("\n".join(ids)+"\n").encode()).hexdigest(),"note":"Document-count degradation only. No claim of LA/CM/CH historical or sign equivalence."}
Path(a.out).write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");print(json.dumps({"retained":len(ids),"manifest":a.out}))
