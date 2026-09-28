#!/usr/bin/env python3
import hashlib,json,pathlib,sys,urllib.request
EXPECTED="eab9ccdfc4324b62f015bccd5e3f917f256cab8c058840842127eadecfbca2d2"
URL="https://github.com/ryanpavlicek/pyaegean/releases/download/damos-corpus-v2/damos-corpus.json"
out=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "data/raw/damos-corpus-v2.json")
out.parent.mkdir(parents=True,exist_ok=True)
with urllib.request.urlopen(URL) as r: data=r.read()
got=hashlib.sha256(data).hexdigest()
if got!=EXPECTED: raise SystemExit(f"SHA256 mismatch: {got}")
out.write_bytes(data)
print(json.dumps({"path":str(out),"bytes":len(data),"sha256":got,"verified":True}))
