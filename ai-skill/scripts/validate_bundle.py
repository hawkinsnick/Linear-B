#!/usr/bin/env python3
import json,sys
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"generated"/"research-bundle-index.json"
d=json.loads(p.read_text(encoding="utf-8"))
errors=[]
for k in ("schema_version","skill_version","source_commit","contract","artifacts"):
 if k not in d: errors.append("missing "+k)
seen=set()
for a in d.get("artifacts",[]):
 if a.get("path") in seen: errors.append("duplicate artifact "+str(a.get("path")))
 seen.add(a.get("path"))
 if not a.get("sha256") or len(a["sha256"])!=64: errors.append("bad sha256 "+str(a.get("path")))
if errors:
 print("\n".join(errors)); sys.exit(1)
print(f"AI bundle valid: {len(d['artifacts'])} indexed canonical artifacts")
