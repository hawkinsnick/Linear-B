#!/usr/bin/env python3
"""Validate current release metadata, schemas, evidence counts and sealed gates.
Historical artifact content versions are independent of the release version.
"""
import csv, hashlib, json, pathlib, re, sys
from jsonschema import Draft202012Validator, validators
R=pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
def require(ok,msg):
    if not ok: raise ValueError(msg)
def validate():
    version=(R/"VERSION").read_text().strip()
    require(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+",version),"invalid release version")
    citation=(R/"CITATION.cff").read_text()
    match=re.search(r'^version:\s*["\']?([^"\'\s]+)',citation,re.M)
    require(match and match.group(1)==version,"citation version drift")
    files=list(R.rglob("*.json"))
    for p in files: json.loads(p.read_text(encoding="utf-8"))
    for p in (R/"schemas").glob("*.json"):
        schema=json.loads(p.read_text());validators.validator_for(schema).check_schema(schema)
    state=load("analysis/current-status.json")
    require(state["repository_version"]==version,"current status version drift")
    family=load("research/family-compatibility-v1.json")
    require(family["member_version"]==version,"family member version drift")
    suite=load("research/family-compatibility-suite-v1.json")
    require(family["contract_version"]==suite["required_contract_version"]==suite["suite_version"]=="1.1.0","family contract")
    require(set(family["members"])==set(suite["required_members"])=={"linear-a","linear-b","cypro-minoan","cretan-hieroglyphic","phaistos-disc"} and len(family["members"])==5,"family membership")
    require(family["membership_boundary"]=="Native evidence only; membership implies no linguistic affinity, shared sign identities, or pooled analysis.","family claim boundary")
    for p in suite["required_artifacts"]:require((R/p).is_file(),"missing family artifact: "+p)
    for evidence in state["evidence"]:
        require(hashlib.sha256((R/evidence["path"]).read_bytes()).hexdigest()==evidence["sha256"],"evidence digest drift: "+evidence["path"])
    gates=load("research/experiment-gates.json")["experiments"] if (R/"research/experiment-gates.json").exists() else []
    for g in gates:
        if g["state"]=="BLOCKED":
            require(g["claim_allowed"] is False,"blocked gate permits claim")
            require(g.get("result_ref") is None,"blocked gate has result")
    schema=load("schemas/aegean-interop-v0.1.schema.json")
    # Exercise actual contract semantics, including rights, unknown fields and provenance.
    v=Draft202012Validator(schema)
    good={"project":family["members"][0],"record_id":"fixture","assertions":[{"assertion_type":"metadata","value":None,"status":"published","provenance":[{"source_id":"fixture"}]}],"rights":{"record_license":"NOASSERTION"}}
    require(v.is_valid(good),"interchange positive fixture rejected")
    for member in family["members"]:
        fixture=json.loads(json.dumps(good));fixture["project"]=member
        require(v.is_valid(fixture),"interchange member rejected: "+member)
    for mutation in ("rights","provenance","unknown"):
        bad=json.loads(json.dumps(good))
        if mutation=="rights":del bad["rights"]
        elif mutation=="provenance":bad["assertions"][0]["provenance"]=[]
        else:bad["unexpected"]=True
        require(not v.is_valid(bad),"interchange negative fixture accepted: "+mutation)
    if "calibration_executed" in state["scientific_results"]:
        require(state["scientific_results"]["calibration_executed"] is False,"unsupported current calibration claim")
    if "prospective_outcomes_inspected" in state["scientific_results"]:
        require(state["scientific_results"]["prospective_outcomes_inspected"] is False,"prospective seal unexpectedly opened")
    if (R/"analysis/observation-source-mapping-audit.json").exists():
        mapping=load("analysis/observation-source-mapping-audit.json")
        require(mapping["records"]==5932 and mapping["nonempty_transcription_surfaces"]==5890 and mapping["null_or_empty_surfaces"]==42 and mapping["all_source_field_values_preserved"] is True,"corrected DAMOS surface coverage drift")
        smoke=load("analysis/authenticated-document-count-smoke.json")
        require(smoke["mapping_audit"]==mapping,"smoke/source mapping mismatch")
        require(smoke["phonetic_eligibility"]["eligible"]==5890 and smoke["phonetic_eligibility"]["excluded_missing_transcription"]==42,"phonetic completeness exclusions drift")
        require(smoke["input_unique_documents"]==5890 and smoke["realized"]["document_count"]==802 and smoke["repeat_run_identical"] is True,"corrected smoke counts/repeatability")
        require(smoke["gold_revealed"] is False and smoke["calibration_executed"] is False and smoke["scientific_matched_environment_claim_allowed"] is False,"software smoke promoted to scientific result")
    counts=state["committed_evidence_counts"]
    if (R/"corpus/index.json").exists():
        idx=load("corpus/index.json");require(idx["version"]==version,"index version drift")
        ids=idx["records"];require(len(ids)==len(set(ids))==idx["record_count"],"duplicate/index count")
        require(set(ids)=={p.stem for p in (R/"corpus/inscriptions").glob("*.json") if p.stem!="TEMPLATE"},"index membership")
        require(counts["rich_records"]==len(ids),"rich record count drift")
        occ=load("occurrences/occurrences.json")["occurrences"]
        require(len({o["occurrence_id"] for o in occ})==len(occ),"duplicate occurrence")
        sources={s["source_id"] for s in load("bibliography/sources.json")}
        for o in occ:require(o["record_id"] in ids and o["source_id"] in sources and o.get("locator"),"occurrence provenance/reference")
        require(counts["source_checked_occurrences"]==len(occ),"occurrence count drift")
    if (R/"corpus/chic-catalogue-spine.json").exists():
        cat=load("corpus/chic-catalogue-spine.json");signs=load("signs/chic-core-sign-registry.json")
        require([x["id"] for x in cat]==[f"CHIC-{i:03d}" for i in range(1,332)],"CH catalogue identity/order")
        require({k:sum(x["series"]==k for x in cat) for k in "HISY"}=={"H":122,"I":57,"S":136,"Y":16},"CH series")
        require(len(signs)==len({s["id"] for s in signs})==96,"CH sign registry")
        require(all(s.get("phonetic_value") is None for s in signs),"CH phonetic leakage")
        sources={s["id"] for s in load("bibliography/sources.json")}
        for x in cat+signs:require(set(x.get("source_ids",[]))<=sources,"CH orphan source")
        manifest=load("corpus/manifest.json");require(manifest["version"]==version,"manifest version drift")
        require(counts["catalogue_identities"]==len(cat),"CH catalogue count drift")
        require(counts["critical_readings"]==len(load("corpus/critical-readings.json")),"CH reading count drift")
    if (R/"research/gold-acquisition-gate.json").exists():
        gold=load("research/gold-acquisition-gate.json")
        require(gold["release_5_0_allowed"] is False,"gold gate unexpectedly opened")
        require(not state["scientific_results"]["calibration_executed"],"unsupported calibration claim")
    print(json.dumps({"status":"PASS","version":version,"json_files":len(files),"schemas":len(list((R/"schemas").glob("*.json"))),"evidence_counts":counts,"scientific_gate_claim":"UNCHANGED"}))
if __name__=="__main__":
    try:validate()
    except Exception as e:print("FAIL:",str(e),file=sys.stderr);sys.exit(1)
