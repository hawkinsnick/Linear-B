#!/usr/bin/env python3
"""Render the current README summary from native authorities; --check rejects drift."""
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
START="<!-- CURRENT-STATUS:START -->"
END="<!-- CURRENT-STATUS:END -->"
def load(path):return json.loads((ROOT/path).read_text())
def render():
    name=ROOT.name
    if (ROOT/'research/reference-manifest.json').exists():
        c=load('research/reference-manifest.json')['coverage']; s=load('research/pre-expert-maximum.json')
        return f"## Current evidence status\n\nPopulated, frozen eDiAna reference layer; structural fleet admission is distinct from scholarly acceptance. {c['digital_catalogue_records']} digital catalogue records provide {c['source_text_rows']} source text rows across {s['record_count']} provisional segments on {s['physical_monuments']} reported monuments. Canonical verified readings: {c['canonical_verified_readings']}; independent reviews: {c['independent_reviews']}. Primary-edition collation and the TL 55 segmentation discrepancy remain open.\n\nAuthorities: [reference manifest](research/reference-manifest.json) and [remaining gates](research/pre-expert-maximum.json). Reference rows are not independently certified physical lines."
    s=load('analysis/current-status.json'); version=(ROOT/'VERSION').read_text().strip()
    if s['repository_version']!=version:raise ValueError('status/version mismatch')
    if (ROOT/'research/calibration-source-recheck-2026-10-11.json').exists():
        a=load('analysis/pre-expert-source-audit.json')
        # Frozen source counts remain those of the authenticated mapping audit.
        m=load('analysis/observation-source-mapping-audit.json')
        q=load('research/calibration-source-recheck-2026-10-11.json')
        return f"## Current evidence status\n\nNative release version: **{version}**. Authenticated source mapping: {m['records']:,} records, {m['nonempty_transcription_surfaces']:,} nonempty transcription surfaces, and {m['null_or_empty_surfaces']} missing/empty surfaces. Calibration executed: **{str(s['scientific_results']['calibration_executed']).lower()}**. The acquisition recheck ({q['checked']}) acquired neither linguistic gold nor an authoritative graphical baseline. The described DĀMOS EpiDoc export omits linguistic annotations; a separately linked annotation package is required.\n\nAuthorities: [current state](analysis/current-status.json), [experiment gates](research/experiment-gates.json), and [calibration inputs](docs/CALIBRATION-INPUTS.md). Software smoke checks do not establish linguistic calibration."
    r=load('research/residual-blocker-ledger-3.0.21.json')
    return f"## Current evidence status\n\nNative release version: **{version}**; researcher-tooling checkpoint: **{r['version']}** (a separate capability milestone). Known-answer calibration executed: **{str(s['scientific_results']['calibration_executed']).lower()}**. Prospective evidence remains sealed; historical 2.5 analyses remain quarantined. Source permissions/access and admissible independent evidence govern further evidence growth.\n\nAuthorities: [current state](analysis/current-status.json) and [residual evidence gates](research/residual-blocker-ledger-3.0.21.json). Historical release reports retain their original scope and dates."
def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    path=ROOT/'README.md';text=path.read_text();expected=START+'\n'+render()+'\n'+END
    if text.count(START)!=1 or text.count(END)!=1:raise ValueError('exactly one current-status block required')
    before,tail=text.split(START);old,after=tail.split(END)
    if a.write:path.write_text(before+expected+after)
    elif START+old+END!=expected:raise SystemExit('stale README current summary; run with --write')
    print('PASS: README current summary matches native authorities')
if __name__=='__main__':main()
