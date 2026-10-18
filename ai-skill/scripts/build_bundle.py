#!/usr/bin/env python3
"""Build a vendor-neutral, provenance-aware AI research bundle from canonical repo artifacts."""
import csv, hashlib, json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"ai-skill"/"generated"; OUT.mkdir(parents=True,exist_ok=True)
sha=os.environ.get("SOURCE_COMMIT") or subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
CANDIDATES=[('attribution_review', 'research/attribution-review.json'), ('attribution_review', 'analysis/attribution-review-audit.json'), ('attribution_review', 'docs/ATTRIBUTION-REVIEW.md'), ('attribution_review', 'scripts/attribution_review.py'), ('attribution_review', 'scripts/test_attribution_review.py')]+[('native_evidence_profile', 'research/evidence-query-profile.json'), ('native_evidence_coverage', 'analysis/evidence-query-coverage.json'), ('native_evidence_query', 'scripts/evidence_query.py'), ('native_evidence_query_tests', 'scripts/test_native_evidence_query.py'), ('native_evidence_guide', 'docs/EVIDENCE-AND-ALTERNATIVES.md')]+[('published_id_example', 'research/damos-published-id-example-2026-10-14.json'), ('published_id_example', 'docs/DAMOS-PUBLISHED-ID-EXAMPLE.md'), ('published_id_example', 'scripts/validate_published_id_example.py')]+[('calibration_freeze', 'scripts/freeze_calibration_run.py'), ('calibration_freeze', 'docs/CALIBRATION-FREEZE-2026-10-14.md'), ('calibration_freeze', 'research/calibration-recheck-2026-10-14.json')]+[("object_concordance_checker", "scripts/check_kn_fp13_concordance.py")]+[["available_evidence_growth", "research/kn-fp13-object-concordance.json"], ["available_evidence_growth", "docs/KN-FP13-CONCORDANCE.md"]]+[("source_access_and_delivery", "research/source-access-delivery-2026-10-12.json"), ("source_delivery_requests", "docs/SOURCE-DELIVERY-REQUESTS.md")]+ [('prepared_field_coverage', 'research/corpus-coverage-register.json')]+[('prepared_calibration_inputs', 'analysis/calibration-prepared-inputs-2026-10-12.json'), ('calibration_preparation', 'scripts/prepare_calibration_inputs.py'), ('calibration_preparation_guide', 'docs/CALIBRATION-PREPARED-INPUTS.md'), ('calibration_acquisition_recheck', 'research/calibration-acquisition-2026-10-12.json')]+[
 ("cross_corpus_dependencies","research/cross-corpus-dependencies.json"),("sync_publication_guard","ai-skill/scripts/publish_sync.py"),("ai_integrity_guide","docs/AI-INTEGRITY.md"),("calibration_intake","docs/CALIBRATION-INTAKE.md"),("calibration_intake_checker","scripts/check_calibration_intake.py"),("source_route_check","research/source-route-check-2026-10-11.json")]+[("source_action_plan","research/source-action-plan.json"),("source_action_guide","docs/SOURCE-ACTION-PLAN.md")]+[
 ("generated_current_summary","README.md"),("current_summary_builder","scripts/build_current_summary.py"),
 ("calibration_source_recheck","research/calibration-source-recheck-2026-10-11.json"),("calibration_acquisition","docs/CALIBRATION-INPUTS.md"),
 ("collection_work_ledger","research/collection-work-ledger.json"),
 ("collection_review_packet","review/collection-packet.json"),
 ("pre_expert_contract","research/pre-expert-maximum.json"),
 ("pre_expert_source_audit","analysis/pre-expert-source-audit.json"),
 ("review_handoff","docs/PRE-EXPERT-HANDOFF.md"),
 ("comparison_contract","research/linear-a-b-control-interface.json"),
 ("current_status","analysis/current-status.json"),("audit","exports/audit.json"),
 ("coverage","data/coverage.json"),("claims","release/CLAIM-REGISTRY.csv"),
 ("corpus_json","exports/corpus.json"),("corpus_jsonl","exports/corpus.jsonl"),
 ("greek_subset","exports/greek-subset.json"),("eteocypriot_components","exports/eteocypriot-components.json"),
 ("rights_matrix","DATA-LICENSE-MATRIX.md"),("rights","docs/RIGHTS.md"),
 ("rights_and_licensing","docs/RIGHTS-AND-LICENSING.md"),("notice","NOTICE"),("third_party","THIRD-PARTY-NOTICES.md")
]
CANDIDATES += [("research_delivery", p) for p in ['scripts/research_delivery.py','scripts/test_research_delivery.py','docs/RESEARCH-DELIVERY.md','analysis/research-delivery.json']]
CANDIDATES += [("specialist_task_pilot", p) for p in ['scripts/task_pilot.py', 'scripts/test_task_pilot.py', 'docs/RESEARCH-TASK-PILOT.md', 'analysis/task-pilot-example.json', 'research/task-pilot.json', 'ai-skill/SKILL.md', 'research/blind-field-policy.json', 'scripts/blind_field_policy.py', 'scripts/build_observation_corpus.py', 'sources/damos-v2.json']]
CANDIDATES += [("bounded_source_study", p) for p in ['research/source-study-2026-10-17.json', 'scripts/source_study.py', 'scripts/test_source_study.py', 'docs/SOURCE-STUDY-2026-10-17.md', 'review/source-study-packet.json', 'review/source-study-response.json', 'analysis/source-study-audit.json', 'research/damos-live-pilot-2026-10-17.json']]
CANDIDATES += [("source_followup_and_review_teaching", p) for p in ['research/review-exercise-2026-10-18.json', 'scripts/review_walkthrough.py', 'scripts/test_review_walkthrough.py', 'docs/REVIEWER-WALKTHROUGH.md', 'review/teaching-example.json', 'review/followup-packet.json', 'review/followup-response.json', 'analysis/review-walkthrough-audit.json']]
artifacts=[]
for role,rel in CANDIDATES:
 p=ROOT/rel
 if p.is_file():
  b=p.read_bytes(); artifacts.append({"role":role,"path":rel,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
bundle={"schema_version":"0.3.1","skill_version":"0.3.1","source_commit":sha,
 "generated_at_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
 "canonical_repository":True,
 "contract":{"corpus_is_authoritative":True,"missing_means_unknown":True,"cross_corpus_equivalence_requires_explicit_evidence":True,
 "preserve_uncertainty":True,"preserve_source_independence":True,"preserve_rights":True},
 "artifacts":artifacts}
(OUT/"research-bundle-index.json").write_text(json.dumps(bundle,indent=2)+"\n",encoding="utf-8")
(OUT/"source-state.json").write_text(json.dumps({"schema_version":"1.0","source_commit":sha,"skill_version":"0.3.1","bundle_index":"ai-skill/generated/research-bundle-index.json"},indent=2)+"\n",encoding="utf-8")
print(f"Indexed {len(artifacts)} canonical artifacts at {sha}")
