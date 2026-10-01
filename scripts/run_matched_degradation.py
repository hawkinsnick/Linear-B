#!/usr/bin/env python3
"""Cross-runtime deterministic document-level degradation for measured targets."""
import argparse,hashlib,json
from pathlib import Path
def sha(b): return hashlib.sha256(b).hexdigest()
def rank(seed,doc_id):
    return hashlib.sha256((str(seed)+"\0"+doc_id).encode("utf-8")).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("observations");ap.add_argument("target");ap.add_argument("--seed",type=int,required=True);ap.add_argument("--out",required=True);ap.add_argument("--data-out",required=True);a=ap.parse_args()
 ob=Path(a.observations).read_bytes();tb=Path(a.target).read_bytes();rows=json.loads(ob);target=json.loads(tb)
 if not isinstance(rows,list) or any(not isinstance(r,dict) or not r.get("document_id") for r in rows): raise SystemExit("REFUSING: observations must be records with document_id")
 allowed={"document_count"};dims=target.get("dimensions",{})
 unknown=[k for k,v in dims.items() if v.get("use",False) and v.get("status")!="measured"];unsupported=[k for k,v in dims.items() if v.get("use",False) and k not in allowed]
 if unknown: raise SystemExit("REFUSING: requested unknown/unmeasured dimensions: "+",".join(sorted(unknown)))
 if unsupported: raise SystemExit("REFUSING: requested dimensions not executable in v0.4: "+",".join(sorted(unsupported)))
 dc=dims.get("document_count",{})
 if not dc.get("use") or dc.get("status")!="measured": raise SystemExit("REFUSING: v0.4 requires measured document_count")
 doc_ids=sorted({str(r["document_id"]) for r in rows});n=dc.get("value")
 if type(n) is not int: raise SystemExit("REFUSING: document_count must be an integer")
 if n<1 or n>len(doc_ids): raise SystemExit("REFUSING: impossible document_count target")
 ranked=sorted(doc_ids,key=lambda d:(rank(a.seed,d),d));selected=sorted(ranked[:n]);keep=set(selected)
 kept=sorted((r for r in rows if str(r["document_id"]) in keep),key=lambda r:(str(r["document_id"]),json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":"))))
 data=(json.dumps(kept,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode();Path(a.data_out).write_bytes(data)
 manifest={"engine":"matched-degradation-v0.4","selection_algorithm":"sha256(seed + NUL + document_id), ascending rank; document_id tie-break","seed":a.seed,"input_observation_sha256":sha(ob),"target_spec_sha256":sha(tb),"input_observation_records":len(rows),"input_unique_documents":len(doc_ids),"target":{"document_count":n},"realized":{"document_count":len(selected),"observation_records":len(kept)},"retained_document_ids":selected,"retained_document_ids_sha256":sha(("\n".join(selected)+"\n").encode()),"retained_dataset_sha256":sha(data),"retained_dataset":a.data_out,"note":"Cross-runtime hash-ranked unique-document selection; all rows for selected documents retained. Canonical output is input-order independent. Unknown dimensions are refused, never zero-imputed. No historical/sign equivalence implied."}
 Path(a.out).write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps({"retained_documents":len(selected),"retained_observations":len(kept),"dataset_sha256":sha(data),"manifest":a.out}))
if __name__=="__main__":main()
