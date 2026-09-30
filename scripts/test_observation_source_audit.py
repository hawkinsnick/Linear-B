#!/usr/bin/env python3
"""Real-input negative controls for the separate source-to-export auditor."""
import json,pathlib,tempfile,sys
from validate_observation_export import audit
source=pathlib.Path(sys.argv[1]);export=pathlib.Path(sys.argv[2]);rows=json.loads(export.read_text())
assert audit(source,export)['nonempty_transcription_surfaces']==5890
with tempfile.TemporaryDirectory() as td:
    p=pathlib.Path(td)/'bad.json'
    for corruption in ('empty_surface','wrong_scribe','wrong_id','invented_layout'):
        x=json.loads(export.read_text())
        if corruption=='empty_surface':x[0]['observable']['transliteration_surface']=None
        elif corruption=='wrong_scribe':x[0]['observable']['hand_label']='wrong'
        elif corruption=='wrong_id':x[0]['document_id']='wrong'
        else:x[0]['observable']['layout']={}
        p.write_text(json.dumps(x))
        try:audit(source,p)
        except ValueError:pass
        else:raise AssertionError('source mapping corruption accepted: '+corruption)
print('PASS: real-source surface, scribe, identifier and invented-field corruption refusal')
