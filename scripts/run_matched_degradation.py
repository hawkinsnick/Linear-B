#!/usr/bin/env python3
"""Deterministic document-level degradation for measured corpus-equivalence targets."""
import argparse,hashlib,json,random
from pathlib import Path
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("target");ap.add_argument("--seed",type=int,required=True);ap.add_argument("--out",required=True);ap.add_argument("--data-out",required=True);a=ap.parse_args()
 ob=Path(a.observations).read_bytes(); tb=Path(a.target).read_bytes(); rows=json.loads(ob); target=json.loads(tb)
 if not isinstance(rows,list) or any(not isinstance(r,dict) or not r.get("document_id") for r in rows): raise SystemExit("REFUSING: observations must be records with document_id")
 allowed={"document_count"}; dims=target.get("dimensions",{})
 unknown=[k for k,v in dims.items() if v.get("use",False) and v.get("status")!="measured"]; unsupported=[k for k,v in dims.items() if v.get("use",False) and k not in allowed]
 if unknown: raise SystemExit("REFUSING: requested unknown/unmeasured dimensions: "+",".join(sorted(unknown)))
 if unsupported: raise SystemExit("REFUSING: requested dimensions not executable in v0.3: "+",".join(sorted(unsupported)))
 dc=dims.get("document_count",{})
 if not dc.get("use") or dc.get("status")!="measured": raise SystemExit("REFUSING: v0.3 requires measured document_count")
 doc_ids=sorted({str(r["document_id"]) for r in rows}); n=int(dc["value"])
 if n<1 or n>len(doc_ids): raise SystemExit("REFUSING: impossible document_count target")
 rng=random.Random(a.seed); selected=sorted(rng.sample(doc_ids,n)); keep=set(selected); kept=[r for r in rows if str(r["document_id"]) in keep]
 data=(json.dumps(kept,ensure_ascii=False,separators=(",",":"))+"\n").encode(); Path(a.data_out).write_bytes(data)
 manifest={"engine":"matched-degradation-v0.3","seed":a.seed,"input_observation_sha256":sha(ob),"target_spec_sha256":sha(tb),"input_observation_records":len(rows),"input_unique_documents":len(doc_ids),"target":{"document_count":n},"realized":{"document_count":len(selected),"observation_records":len(kept)},"retained_document_ids":selected,"retained_document_ids_sha256":sha(("\n".join(selected)+"\n").encode()),"retained_dataset_sha256":sha(data),"retained_dataset":a.data_out,"note":"Samples unique document IDs and retains all observation rows for selected documents. Unknown dimensions are refused, never zero-imputed. Document-count degradation only; no historical/sign equivalence implied."}
 Path(a.out).write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");print(json.dumps({"retained_documents":len(selected),"retained_observations":len(kept),"dataset_sha256":sha(data),"manifest":a.out}))
if __name__=="__main__": main()
