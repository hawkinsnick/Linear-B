#!/usr/bin/env python3
"""Deterministic document-level degradation for measured corpus-equivalence targets."""
import argparse,hashlib,json,random
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("target");ap.add_argument("--seed",type=int,required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
 rows=json.loads(Path(a.observations).read_text(encoding="utf-8")); target=json.loads(Path(a.target).read_text(encoding="utf-8"))
 if not isinstance(rows,list) or any(not isinstance(r,dict) or not r.get("document_id") for r in rows): raise SystemExit("REFUSING: observations must be records with document_id")
 allowed={"document_count"}; dims=target.get("dimensions",{})
 unknown=[k for k,v in dims.items() if v.get("use",False) and v.get("status")!="measured"]
 unsupported=[k for k,v in dims.items() if v.get("use",False) and k not in allowed]
 if unknown: raise SystemExit("REFUSING: requested unknown/unmeasured dimensions: "+",".join(sorted(unknown)))
 if unsupported: raise SystemExit("REFUSING: requested dimensions not executable in v0.2: "+",".join(sorted(unsupported)))
 dc=dims.get("document_count",{})
 if not dc.get("use") or dc.get("status")!="measured": raise SystemExit("REFUSING: v0.2 requires measured document_count")
 doc_ids=sorted({str(r["document_id"]) for r in rows}); n=int(dc["value"])
 if n<1 or n>len(doc_ids): raise SystemExit("REFUSING: impossible document_count target")
 rng=random.Random(a.seed); selected=sorted(rng.sample(doc_ids,n)); keep=set(selected); kept=[r for r in rows if str(r["document_id"]) in keep]
 obs_keys=[f'{r["document_id"]}:{i}' for i,r in enumerate(kept)]
 manifest={"engine":"matched-degradation-v0.2","seed":a.seed,"input_observation_records":len(rows),"input_unique_documents":len(doc_ids),"target":{"document_count":n},"realized":{"document_count":len(selected),"observation_records":len(kept)},"retained_document_ids":selected,"retained_document_ids_sha256":hashlib.sha256(("\n".join(selected)+"\n").encode()).hexdigest(),"retained_observation_manifest_sha256":hashlib.sha256(("\n".join(obs_keys)+"\n").encode()).hexdigest(),"note":"Samples unique document IDs and retains all observation rows for selected documents. Document-count degradation only; no historical/sign equivalence implied."}
 Path(a.out).write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");print(json.dumps({"retained_documents":len(selected),"retained_observations":len(kept),"manifest":a.out}))
if __name__=="__main__": main()
