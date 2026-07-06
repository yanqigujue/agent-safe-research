# 鐢靛姏杩愮淮 AFW 鍥涚被浜や粯绱㈠紩

鏃ユ湡锛?026-07-01

杩欎唤鏂囨。鏄綋鍓?AFW / CapGuard 浜х墿鐨勫叆鍙ｉ〉锛岀敤鏉ュ洖绛旓細

```text
褰㈠紡鍖栧缓妯″湪鍝噷锛?娴嬭瘯妗嗘灦鍦ㄥ摢閲岋紵
娴嬭瘯鏍锋湰鍦ㄥ摢閲岋紵
瀹炴柦鏂规鍦ㄥ摢閲岋紵
鐜板湪瀹為檯璺戝嚭浜嗕粈涔堬紵
```

## 1. 褰㈠紡鍖栧缓妯?
涓绘枃妗ｏ細

```text
docs/power_ops_afw_formal_model_2026-07-01.md
docs/action_field_authority_warrant_calculus_2026-07-01.md
docs/power_ops_afw_trace_adapter_formal_mapping_2026-07-01.md
```

鏍稿績瀵硅薄锛?
```text
Cap(x)       source x 鎼哄甫鐨勫瓧娈垫巿鏉冭兘鍔?Need(s, f)   step s 涓瓧娈?f 闇€瑕佺殑鎺堟潈
Consume(x -> f, s)  鍔ㄤ綔瀛楁娑堣垂鏉ユ簮鎺堟潈
```

鏍稿績鍒ゅ畾锛?
```text
allow    Cap(x) 瑕嗙洊 Need(s, f)锛屼笖娌℃湁鏈В闄?obligation / counter-authority
block    缂?role銆乫ield銆乷peration銆乨ata/effect/delegation/time scope 鎴?obligation 鏈弧瓒?abstain  trace 涓嶅彲淇°€佺己灏戝彲鍒ゅ畾杈撳叆锛屾垨姝ｅ悜鎺堟潈鍜?counter-authority 鍐茬獊
```

褰撳墠宸茬粡瑕嗙洊鐨勭淮搴︼細

```text
semantic role
field
operation
data scope
effect scope
delegation scope
time scope
obligation
counter-authority
minimal authority witness
```

## 2. 娴嬭瘯妗嗘灦

涓绘枃妗ｏ細

```text
docs/power_ops_afw_test_framework_2026-07-01.md
```

鏍稿績浠ｇ爜锛?
```text
formaltrust_platform/experiments/afw_bench.py
formaltrust_platform/nodes/afw.py
formaltrust_platform/experiments/afw_runtime_report.py
formaltrust_platform/experiments/afw_runtime_suite.py
formaltrust_platform/experiments/afw_requirement_coverage.py
formaltrust_platform/experiments/afw_dataset_audit.py
formaltrust_platform/experiments/afw_annotation_agreement.py
formaltrust_platform/experiments/afw_defense_loop.py
tests/test_afw_bench.py
tests/test_interfaces.py
```

宸茬粡钀藉湴鐨勬祴璇曞眰锛?
```text
绂荤嚎 paired-row evaluator
trace-to-row adapter
trace-derived authority-confusion generator
FormalTrust guardrail node: guardrail.afw_capguard
FormalTrust runtime evaluator: evaluate.afw_runtime
raw trace adapter: custom.afw_trace_adapter
runtime report aggregator
runtime suite report aggregator
dataset annotation audit
annotation packet and kappa agreement workflow
defense-loop and K2/K3/K4 proxy report
```

## 3. 娴嬭瘯鏍锋湰

涓绘枃妗ｏ細

```text
docs/power_ops_afw_test_samples_2026-07-01.md
```

绂荤嚎鏍锋湰锛?
```text
examples/afw_same_source_paired_rows.json
examples/afw_composite_authority_rows.json
examples/afw_counter_authority_rows.json
examples/afw_attenuation_rows.json
examples/afw_boundary_role_rows.json
examples/afw_obligation_rows.json
examples/afw_temporal_rows.json
examples/afw_power_ops_rag_rows.json
examples/afw_power_ops_trace_scenarios.json
```

杩愯鏃舵牱鏈細

```text
examples/afw_runtime_validation.yaml
examples/afw_trace_adapter_runtime_validation.yaml
examples/afw_trace_adapter_multisource_runtime_validation.yaml
examples/afw_trace_adapter_malformed_runtime_validation.yaml
examples/afw_trace_adapter_span_log_runtime_validation.yaml
examples/afw_trace_adapter_otlp_runtime_validation.yaml
examples/afw_trace_adapter_otlp_envelope_runtime_validation.yaml
examples/afw_trace_adapter_obligation_runtime_validation.yaml
examples/afw_trace_adapter_temporal_runtime_validation.yaml
examples/afw_trace_adapter_counter_authority_runtime_validation.yaml
```

褰撳墠鏍锋湰瑙勬ā锛?
```text
power-ops paired rows = 32
power-ops trace scenarios = 20
generated authority-confusion rows = 40
runtime suite runs = 3
runtime suite cases = 12
dataset annotation audited items = 40
dataset fully labeled items = 40
annotation packet items = 40
kappa smoke min_kappa = 1.0
defense loop rows = 32
defense loop passes proxy gates = True
```

## 4. 瀹炴柦鏂规

涓绘枃妗ｏ細

```text
docs/power_ops_afw_implementation_scheme_2026-07-01.md
```

褰撳墠宸ョ▼鎺ュ叆鐐癸細

```text
guardrail.afw_capguard
evaluate.afw_runtime
custom.afw_trace_adapter
build_afw_runtime_run_summary
build_afw_runtime_suite_summary
render_afw_runtime_suite_markdown
run_afw_runtime_config_suite
```

鍜?FormalTrust 鐨勬帴鍙ｅ叧绯伙細

```text
node 璇诲彇 FormalTrustState + config
node 鍙繑鍥?FormalTrustState 椤跺眰瀛楁 patch
缁撴瀯鍖栦腑闂寸粨鏋滃啓鍏?metrics
澶т骇鐗╄矾寰勫啓鍏?artifacts
瀹夊叏鎷︽埅杩斿洖 gate_decision/final_action锛岃€屼笉鏄潬寮傚父琛ㄨ揪
```

## 5. 褰撳墠鍙鐜扮粨鏋?
Runtime suite 浜х墿锛?
```text
docs/power_ops_afw_runtime_suite_report_2026-07-01.md
docs/power_ops_afw_runtime_suite_report_2026-07-01.json
docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md
docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json
```

闇€姹傝鐩栫煩闃碉細

```text
docs/power_ops_afw_requirement_coverage_2026-07-01.md
docs/power_ops_afw_requirement_coverage_2026-07-01.json
```

Dataset annotation audit assets:

```text
docs/power_ops_afw_dataset_annotation_audit_2026-07-01.md
docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json
```

Annotation packet and agreement assets:

```text
docs/power_ops_afw_annotation_packet_2026-07-01.json
docs/power_ops_afw_annotation_packet_2026-07-01.jsonl
docs/power_ops_afw_annotation_smoke_annotator_a_2026-07-01.jsonl
docs/power_ops_afw_annotation_smoke_annotator_b_2026-07-01.jsonl
docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.md
docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.json
```

Defense loop assets:

```text
docs/power_ops_afw_defense_loop_report_2026-07-01.md
docs/power_ops_afw_defense_loop_report_2026-07-01.json
```

Suite 鎸囨爣锛?
```text
total_runs = 3
total_cases = 12
passed_cases = 12
mean_afw_behmatch = 1.0
total_runtime_fields = 10
prevented_fields = 8
false_allow_fields = 0
false_block_fields = 0
allow_cases = 2
block_cases = 7
abstain_cases = 3
counter_authority_events = 1
invalid_events = 5
unknown_events = 2
mean_compression_ratio = 0.7
```

All-config runtime suite 鎸囨爣锛?
```text
total_runs = 10
total_cases = 27
passed_cases = 27
mean_afw_behmatch = 1.0
total_runtime_fields = 25
prevented_fields = 21
false_allow_fields = 0
false_block_fields = 0
allow_cases = 4
block_cases = 20
abstain_cases = 3
counter_authority_events = 1
invalid_events = 5
unknown_events = 2
mean_compression_ratio = 0.76
```

Requirement coverage 鎸囨爣锛?
```text
total_requirements = 10
supported = 4
partial = 6
missing = 0
```

Dataset annotation audit metrics:
```text
paired_rows = 32
runtime_cases = 8
total_audited_items = 40
fully_labeled_items = 40
kappa_status = pending_human_double_annotation
dataset_scale_status = afw_specialized_subset_not_full_pdf_scale
```

Annotation agreement metrics:
```text
annotation_packet_items = 40
agreement_source = machine_prefill_smoke_not_human
agreement_smoke_min_kappa = 1.0
agreement_smoke_mean_kappa = 1.0
human_kappa_status = not_human_double_annotation
```

Defense loop proxy metrics:
```text
k2_min_risk_discovery_lift = 0.125
k3_min_safety_issue_reduction = 1.0
k4_utility_preservation = 1.0
general_ability_drop = 0.0
claim_scope = afw_power_ops_subset_proxy_not_project_level
```

Production chain manifest assets:
```text
examples/afw_power_ops_production_chain.yaml
formaltrust_platform/experiments/afw_production_chain.py
docs/power_ops_afw_production_chain_report_2026-07-01.md
docs/power_ops_afw_production_chain_report_2026-07-01.json
```

Production chain manifest metrics:
```text
model_roles_present = embedding, generation, rerank
required_model_roles_covered = True
rag_flow_contains_guardrail = True
estimated_model_memory_gb = 20.0
max_total_model_memory_gb = 22.0
gpu_memory_gb = 24.0
memory_budget_passes = True
api_compatibility_passes = True
production_readiness_status = manifest_validated_not_live_deployment
```

鍥炲綊楠岃瘉锛?
```powershell
pytest tests\test_afw_bench.py -q
# 57 passed

pytest tests\test_interfaces.py tests\test_afw_bench.py -q
# 81 passed

pytest tests\test_interfaces.py tests\test_afw_bench.py tests\test_mvp.py -q
# 146 passed

python -m compileall formaltrust_platform\experiments\afw_runtime_report.py formaltrust_platform\experiments\afw_runtime_suite.py formaltrust_platform\experiments\afw_requirement_coverage.py formaltrust_platform\experiments\afw_dataset_audit.py formaltrust_platform\experiments\afw_annotation_agreement.py formaltrust_platform\experiments\afw_defense_loop.py formaltrust_platform\experiments\afw_production_chain.py formaltrust_platform\nodes\afw.py
# passed
```

## 6. 鐩墠杩樹笉鑳借繃搴﹀绉扮殑鍦版柟

```text
褰撳墠 suite 鏄?curated validation runs锛屼笉鏄畬鏁?benchmark銆?褰撳墠 raw trace / span-log / OTLP 閮芥槸 curated 鎴?semi-real cases锛屼笉鏄敓浜ф棩蹇楀叏瑕嗙洊銆?褰撳墠 witness compression 鏄?artifact-level proxy锛屼笉鏄汉宸ュ璁℃椂闂寸殑鐪熷疄娴嬮噺銆?褰撳墠 counter-authority 鍙瘉鏄庡瓧娈?鏁堟灉鑼冨洿鍐呯殑 policy-hold abstain锛屼笉鏄畬鏁村啿绐佺敓鍛藉懆鏈熺郴缁熴€?```

## 7. 涓嬩竴姝ユ渶鍊煎緱鍋?
```text
1. 缁?40 鏉?generated authority-confusion rows 濉汉宸?plausibility label銆?2. 鎶?runtime source events 浠?curated JSONL 鎹㈡垚鍗婄湡瀹?RAG/agent trace parser 杈撳嚭銆?3. 鎶?all-config suite report 鍥哄寲鎴愬懆鏈熸€у洖褰掍骇鐗┿€?4. 鎶?witness compression 浠庤鏁版寚鏍囨帹杩涘埌浜哄伐瀹¤宸ヤ綔閲忓疄楠屻€?```

