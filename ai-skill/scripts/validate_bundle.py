#!/usr/bin/env python3
import hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/"ai-skill";errors=[]
bundle=json.loads((A/"generated"/"research-bundle-index.json").read_text())
manifest=json.loads((A/"manifest.json").read_text())
profile=json.loads((A/"references"/"authority-profile.json").read_text())
skill=(A/"SKILL.md").read_text()
match=re.search(r"^version:\s*([^\s]+)",skill,re.M)
declared=match.group(1) if match else None
expected=str(manifest.get("skill_version"))
if declared!=expected: errors.append("skill and manifest version differ")
if bundle.get("skill_version")!=expected: errors.append("bundle and manifest version differ")
if bundle.get("schema_version")!=manifest.get("bundle_schema"): errors.append("bundle schema differs")
indexed={x.get("path"):x for x in bundle.get("artifacts",[])}
for req in profile.get("required_authorities",[]):
 p=R/req["path"]
 if req.get("required") and not p.is_file(): errors.append("missing authority "+req["path"]);continue
 if p.is_file():
  item=indexed.get(req["path"])
  digest=hashlib.sha256(p.read_bytes()).hexdigest()
  if not item: errors.append("authority not indexed "+req["path"])
  elif item.get("sha256")!=digest: errors.append("authority hash differs "+req["path"])
if not bundle.get("source_commit"): errors.append("missing source commit")
if errors: print("\n".join(errors));sys.exit(1)
print("Linear B AI integration validation PASS")
