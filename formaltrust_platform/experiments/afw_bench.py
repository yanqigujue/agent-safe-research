from __future__ import annotations

import copy
import json
from itertools import combinations
from pathlib import Path
from typing import Any, Literal


Decision = Literal["allow", "block", "abstain"]
BaselineName = Literal[
    "capguard",
    "permission_only",
    "attribution_only",
    "field_attribution_only",
    "strict_block",
    "boundary_scope_only",
    "authgraph_style_parameter_provenance",
    "skill_permission_style",
]


def load_paired_rows(path: str | Path) -> list[dict[str, Any]]:
    """Load deterministic action-field authority warrant paired rows."""

    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("AFW row file must contain a list under 'rows'")
    return rows


def load_many_paired_rows(paths: list[str | Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(load_paired_rows(path))
    return rows


def load_trace_scenarios_as_rows(path: str | Path) -> list[dict[str, Any]]:
    return [_trace_scenario_to_row(scenario) for scenario in _load_trace_scenarios(path)]


def generate_authority_confusion_rows(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in _load_trace_scenarios(path):
        for confusion in scenario.get("role_confusions", []):
            rows.append(_trace_confusion_to_row(scenario, confusion))
    return rows


def infer_capability_from_trace_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    source_event = scenario.get("source_event", {})
    authority_manifest = scenario.get("authority_manifest")
    if isinstance(authority_manifest, dict):
        return _capability_from_authority_manifest(
            source_event, authority_manifest, inferred_from="authority_manifest"
        )

    manifest = scenario.get("skill_manifest")
    if source_event.get("source_type") != "skill" or not isinstance(manifest, dict):
        raise ValueError("Trace scenarios need either authority_manifest or skill_manifest for inference")

    semantic_roles = manifest.get("output_semantic_roles", [])
    if not semantic_roles:
        raise ValueError("skill_manifest must declare output_semantic_roles for capability inference")

    return _capability_from_authority_manifest(
        source_event,
        {
            "semantic_roles": semantic_roles,
            "fields": manifest.get("allowed_fields", []),
            "operations": manifest.get("allowed_operations", []),
            "data_scope": manifest.get("allowed_data_scope", []),
            "effect_scope": manifest.get("allowed_effect_scope", []),
            "delegation_scope": manifest.get("allowed_delegation_scope", []),
            "obligations": manifest.get("output_obligations", []),
        },
        inferred_from="skill_manifest",
    )


def _capability_from_authority_manifest(
    source_event: dict[str, Any], manifest: dict[str, Any], *, inferred_from: str
) -> dict[str, Any]:
    semantic_roles = manifest.get("semantic_roles", [])
    if not semantic_roles:
        raise ValueError("authority manifest must declare semantic_roles")

    return {
        "source_id": source_event["source_id"],
        "semantic_roles": semantic_roles,
        "fields": manifest.get("fields", []),
        "operations": manifest.get("operations", []),
        "data_scope": manifest.get("data_scope", []),
        "effect_scope": manifest.get("effect_scope", []),
        "delegation_scope": manifest.get("delegation_scope", []),
        "obligations": manifest.get("obligations", []),
        "inferred_from": inferred_from,
    }


def find_minimal_authority_witness(row: dict[str, Any], consumption: dict[str, Any]) -> dict[str, Any]:
    capabilities = _row_capabilities(row)
    required_roles = _required_roles(consumption.get("need", {}))
    role_candidates = {
        role: [
            index
            for index, capability in enumerate(capabilities)
            if _capability_covers_role(capability, role, consumption)
        ]
        for role in required_roles
    }
    missing_roles = [role for role, candidate_indexes in role_candidates.items() if not candidate_indexes]
    if missing_roles:
        return {
            "covers_need": False,
            "capability_indexes": [],
            "covered_roles": {},
            "missing_roles": missing_roles,
            "obligations": [],
            "undischarged_obligations": [],
        }

    for size in range(1, len(capabilities) + 1):
        for candidate_set in combinations(range(len(capabilities)), size):
            if _candidate_set_covers_roles(candidate_set, role_candidates):
                covered_roles = {
                    role: next(index for index in candidate_set if index in candidate_indexes)
                    for role, candidate_indexes in role_candidates.items()
                }
                obligation_specs = _witness_obligation_specs(capabilities, candidate_set)
                return {
                    "covers_need": bool(required_roles),
                    "capability_indexes": list(candidate_set),
                    "covered_roles": covered_roles,
                    "missing_roles": [],
                    "obligations": sorted(obligation_specs),
                    "undischarged_obligations": _undischarged_obligations(obligation_specs, consumption),
                }

    return {
        "covers_need": False,
        "capability_indexes": [],
        "covered_roles": {},
        "missing_roles": required_roles,
        "obligations": [],
        "undischarged_obligations": [],
    }


def authority_witness_audit_summary(row: dict[str, Any], consumption: dict[str, Any]) -> dict[str, Any]:
    witness = find_minimal_authority_witness(row, consumption)
    full_count = len(_row_capabilities(row))
    witness_count = len(witness["capability_indexes"])
    irrelevant_count = full_count - witness_count if witness["covers_need"] else full_count
    return {
        "covers_need": witness["covers_need"],
        "full_context_capability_count": full_count,
        "witness_capability_count": witness_count,
        "irrelevant_capability_count": irrelevant_count,
        "compression_ratio": _ratio(irrelevant_count, full_count),
        "missing_roles": witness["missing_roles"],
        "undischarged_obligations": witness["undischarged_obligations"]
        if row.get("enforce_obligations")
        else [],
    }


def evaluate_authority_consumptions(
    capabilities: list[dict[str, Any]],
    consumptions: list[dict[str, Any]],
    *,
    enforce_obligations: bool = False,
    counter_authority: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate runtime action-field consumptions against available capabilities."""

    row = {
        "row_id": "runtime_authority_check",
        "source": {"source_type": "runtime"},
        "capabilities": capabilities,
        "counter_authority": counter_authority or [],
        "enforce_obligations": enforce_obligations,
    }
    field_results = [
        _evaluate_authority_consumption(row, capabilities, consumption, index)
        for index, consumption in enumerate(consumptions)
    ]
    decision_counts = {
        decision: sum(1 for result in field_results if result["decision"] == decision)
        for decision in ("allow", "block", "abstain")
    }
    total = len(field_results)
    witness_compression_rate = _ratio(
        sum(result["witness_audit"]["compression_ratio"] for result in field_results),
        total,
    )

    return {
        "mode": "runtime_authority_consumptions",
        "total_fields": total,
        "gate_decision": _authority_consumption_gate_decision(decision_counts, total),
        "decision_counts": decision_counts,
        "allow_rate": _ratio(decision_counts["allow"], total),
        "block_rate": _ratio(decision_counts["block"], total),
        "abstain_rate": _ratio(decision_counts["abstain"], total),
        "witness_compression_rate": witness_compression_rate,
        "allowed_fields": [
            result["field"] for result in field_results if result["decision"] == "allow"
        ],
        "blocked_fields": [
            result["field"] for result in field_results if result["decision"] == "block"
        ],
        "abstained_fields": [
            result["field"] for result in field_results if result["decision"] == "abstain"
        ],
        "field_results": field_results,
    }


def evaluate_paired_rows(rows: list[dict[str, Any]], *, baseline: BaselineName) -> dict[str, Any]:
    row_results = [_evaluate_row(row, baseline=baseline) for row in rows]
    total = len(row_results)
    legal_allowed = sum(1 for result in row_results if result["legal_decision"] == "allow")
    laundered_blocked = sum(1 for result in row_results if result["laundered_decision"] == "block")
    laundered_rejected = sum(1 for result in row_results if result["laundered_decision"] in {"block", "abstain"})
    laundered_allowed = sum(1 for result in row_results if result["laundered_decision"] == "allow")
    abstained = sum(
        1
        for result in row_results
        for decision_key in ("legal_decision", "laundered_decision")
        if result[decision_key] == "abstain"
    )

    legal_preservation_rate = _ratio(legal_allowed, total)
    false_allow_rate = _ratio(laundered_allowed, total)
    laundering_block_rate = _ratio(laundered_blocked, total)
    legal_witness_compression_rate = _ratio(
        sum(result["legal_witness_audit"]["compression_ratio"] for result in row_results),
        total,
    )

    return {
        "baseline": baseline,
        "total_rows": total,
        "legal_preservation_rate": legal_preservation_rate,
        "laundering_block_rate": laundering_block_rate,
        "laundering_reject_rate": _ratio(laundered_rejected, total),
        "false_allow_rate": false_allow_rate,
        "false_block_rate": _ratio(total - legal_allowed, total),
        "abstain_rate": _ratio(abstained, total * 2),
        "same_source_contrast_gap": legal_preservation_rate - false_allow_rate,
        "legal_witness_compression_rate": legal_witness_compression_rate,
        "field_family_results": _field_family_results(row_results),
        "row_results": row_results,
    }


def _evaluate_row(row: dict[str, Any], *, baseline: BaselineName) -> dict[str, Any]:
    if baseline in {"permission_only", "attribution_only"}:
        legal_decision: Decision = "allow"
        laundered_decision: Decision = "allow"
    elif baseline == "strict_block":
        legal_decision = "block"
        laundered_decision = "block"
    elif baseline == "capguard":
        capabilities = _row_capabilities(row)
        legal_decision = _capguard_decision(row, capabilities, row["legal_consumption"])
        laundered_decision = _capguard_decision(row, capabilities, row["laundered_consumption"])
    elif baseline == "boundary_scope_only":
        capabilities = _row_capabilities(row)
        legal_decision = "allow" if _boundary_scope_covers(capabilities, row["legal_consumption"]) else "block"
        laundered_decision = "allow" if _boundary_scope_covers(capabilities, row["laundered_consumption"]) else "block"
    elif baseline == "field_attribution_only":
        legal_decision = "allow" if _has_field_attribution(row, row["legal_consumption"]) else "block"
        laundered_decision = "allow" if _has_field_attribution(row, row["laundered_consumption"]) else "block"
    elif baseline == "authgraph_style_parameter_provenance":
        legal_decision = _authgraph_style_decision(row, row["legal_consumption"])
        laundered_decision = _authgraph_style_decision(row, row["laundered_consumption"])
    elif baseline == "skill_permission_style":
        legal_decision = _skill_permission_decision(row, row["legal_consumption"])
        laundered_decision = _skill_permission_decision(row, row["laundered_consumption"])
    else:
        raise ValueError(f"Unsupported AFW baseline: {baseline}")

    return {
        "row_id": row["row_id"],
        "source_type": row["source"]["source_type"],
        "legal_field": row["legal_consumption"]["field"],
        "laundered_field": row["laundered_consumption"]["field"],
        "laundered_field_family": _field_family(row["laundered_consumption"]["field"]),
        "legal_decision": legal_decision,
        "laundered_decision": laundered_decision,
        "legal_witness": find_minimal_authority_witness(row, row["legal_consumption"]),
        "laundered_witness": find_minimal_authority_witness(row, row["laundered_consumption"]),
        "legal_witness_audit": authority_witness_audit_summary(row, row["legal_consumption"]),
        "laundered_witness_audit": authority_witness_audit_summary(row, row["laundered_consumption"]),
        "expected_legal": row["expected"]["legal"],
        "expected_laundered": row["expected"]["laundered"],
        "nearest_neighbor_objection": row.get("nearest_neighbor_objection", []),
    }


def _evaluate_authority_consumption(
    row: dict[str, Any],
    capabilities: list[dict[str, Any]],
    consumption: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    decision = _capguard_decision(row, capabilities, consumption)
    witness = find_minimal_authority_witness(row, consumption)
    witness_audit = authority_witness_audit_summary(row, consumption)
    field = consumption.get("field")
    field_name = field if isinstance(field, str) else "<missing>"

    return {
        "index": index,
        "field": field_name,
        "field_family": _field_family(field_name),
        "operation": consumption.get("operation"),
        "decision": decision,
        "attributed_source_id": consumption.get("attributed_source_id"),
        "required_roles": _required_roles(consumption.get("need", {})),
        "witness": witness,
        "witness_audit": witness_audit,
    }


def _authority_consumption_gate_decision(
    decision_counts: dict[str, int], total: int
) -> Decision:
    if total == 0:
        return "abstain"
    if decision_counts["block"]:
        return "block"
    if decision_counts["abstain"]:
        return "abstain"
    return "allow"


def _row_capabilities(row: dict[str, Any]) -> list[dict[str, Any]]:
    if "capabilities" in row:
        return row["capabilities"]
    return [row["capability"]]


def _capguard_decision(
    row: dict[str, Any], capabilities: list[dict[str, Any]], consumption: dict[str, Any]
) -> Decision:
    if not _capabilities_cover(capabilities, consumption):
        return "block"
    if row.get("enforce_obligations") and _obligations_missing(row, consumption):
        return "block"
    if _counter_authority_applies(row, consumption):
        return "abstain"
    return "allow"


def _capabilities_cover(capabilities: list[dict[str, Any]], consumption: dict[str, Any]) -> bool:
    need = consumption.get("need", {})
    required_roles = _required_roles(need)

    return bool(required_roles) and all(
        any(_capability_covers_role(capability, role, consumption) for capability in capabilities)
        for role in required_roles
    )


def _boundary_scope_covers(capabilities: list[dict[str, Any]], consumption: dict[str, Any]) -> bool:
    need = consumption.get("need", {})
    data_scope = need.get("data_scope")
    delegation_scope = need.get("delegation_scope")
    effect_scope = need.get("effect_scope")
    time_scope = need.get("time_scope")

    return any(
        _field_is_covered(consumption.get("field"), capability.get("fields", []))
        and _operation_is_covered(consumption.get("operation"), capability.get("operations", []))
        and _data_scope_is_covered(data_scope, capability.get("data_scope", []))
        and _delegation_scope_is_covered(delegation_scope, capability.get("delegation_scope", []))
        and _effect_scope_is_covered(effect_scope, capability.get("effect_scope", []))
        and _time_scope_is_covered(time_scope, capability.get("time_scope", []))
        for capability in capabilities
    )


def _has_field_attribution(row: dict[str, Any], consumption: dict[str, Any]) -> bool:
    attributed_source_id = consumption.get("attributed_source_id")
    if attributed_source_id is None:
        return False

    source_ids = {row.get("source", {}).get("source_id")}
    for capability in _row_capabilities(row):
        if capability.get("source_id") is not None:
            source_ids.add(capability["source_id"])
    return attributed_source_id in source_ids


def _trace_scenario_to_row(scenario: dict[str, Any]) -> dict[str, Any]:
    row = {
        "row_id": scenario["scenario_id"],
        "source": scenario["source_event"],
        "capability": _trace_scenario_capability(scenario),
        "legal_consumption": scenario["legal_event"],
        "laundered_consumption": scenario["laundering_event"],
        "nearest_neighbor_objection": scenario.get("nearest_neighbor_objection", []),
        "expected": scenario["expected"],
    }
    _copy_optional_row_metadata(row, scenario)
    return row


def _trace_confusion_to_row(scenario: dict[str, Any], confusion: dict[str, Any]) -> dict[str, Any]:
    legal = copy.deepcopy(scenario["legal_event"])
    laundered = copy.deepcopy(scenario["legal_event"])
    laundered["value"] = confusion.get("target_value", laundered.get("value"))

    laundered_need = copy.deepcopy(legal.get("need", {}))
    laundered_need.pop("required_roles", None)
    laundered_need["required_role"] = confusion["target_required_role"]
    laundered["need"] = laundered_need

    row = {
        "row_id": f"{scenario['scenario_id']}::{confusion['confusion_id']}",
        "source": copy.deepcopy(scenario["source_event"]),
        "capability": copy.deepcopy(scenario["capability"]),
        "legal_consumption": legal,
        "laundered_consumption": laundered,
        "nearest_neighbor_objection": confusion.get(
            "nearest_neighbor_objection", scenario.get("nearest_neighbor_objection", [])
        ),
        "expected": {"legal": "allow", "laundered": "block"},
        "generated_from": scenario["scenario_id"],
        "confusion_type": "boundary_preserving_semantic_role_mutation",
    }
    _copy_optional_row_metadata(row, scenario)
    return row


def _trace_scenario_capability(scenario: dict[str, Any]) -> dict[str, Any]:
    if "capability" in scenario:
        return scenario["capability"]
    return infer_capability_from_trace_scenario(scenario)


def _load_trace_scenarios(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    scenarios = payload.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise ValueError("AFW trace scenario file must contain a list under 'scenarios'")
    return scenarios


def _copy_optional_row_metadata(row: dict[str, Any], scenario: dict[str, Any]) -> None:
    for key in ("skill_manifest", "authgraph", "counter_authority"):
        if key in scenario:
            row[key] = copy.deepcopy(scenario[key])


def _authgraph_style_decision(row: dict[str, Any], consumption: dict[str, Any]) -> Decision:
    field = consumption.get("field")
    if not isinstance(field, str) or not field.startswith("parameters"):
        return "allow"

    authgraph = row.get("authgraph", {})
    source_id = consumption.get("attributed_source_id")
    authorized_sources = authgraph.get("authorized_parameter_sources", [])
    authorized_fields = authgraph.get("authorized_parameter_fields", [])
    if source_id not in authorized_sources:
        return "block"
    if not _field_is_covered(field, authorized_fields):
        return "block"
    return "allow"


def _skill_permission_decision(row: dict[str, Any], consumption: dict[str, Any]) -> Decision:
    if row.get("source", {}).get("source_type") != "skill":
        return "allow"

    manifest = row.get("skill_manifest")
    if not isinstance(manifest, dict):
        return "block"

    need = consumption.get("need", {})
    data_scope = need.get("data_scope")
    delegation_scope = need.get("delegation_scope")
    effect_scope = need.get("effect_scope")

    allowed_delegation_scope = manifest.get("allowed_delegation_scope", [])
    delegation_ok = True if delegation_scope is None else delegation_scope in allowed_delegation_scope

    return (
        "allow"
        if _field_is_covered(consumption.get("field"), manifest.get("allowed_fields", []))
        and _operation_is_covered(consumption.get("operation"), manifest.get("allowed_operations", []))
        and _data_scope_is_covered(data_scope, manifest.get("allowed_data_scope", []))
        and _effect_scope_is_covered(effect_scope, manifest.get("allowed_effect_scope", []))
        and delegation_ok
        else "block"
    )


def _required_roles(need: dict[str, Any]) -> list[str]:
    if "required_roles" in need:
        return need["required_roles"]
    required_role = need.get("required_role")
    if required_role is None:
        return []
    return [required_role]


def _counter_authority_applies(row: dict[str, Any], consumption: dict[str, Any]) -> bool:
    need = consumption.get("need", {})
    for counter in row.get("counter_authority", []):
        field_matches = counter.get("field") == consumption.get("field")
        effect_matches = counter.get("effect_scope") in {None, need.get("effect_scope")}
        if field_matches and effect_matches:
            return True
    return False


def _capability_covers_role(capability: dict[str, Any], role: str, consumption: dict[str, Any]) -> bool:
    need = consumption.get("need", {})
    return (
        role in capability.get("semantic_roles", [])
        and _field_is_covered(consumption.get("field"), capability.get("fields", []))
        and _operation_is_covered(consumption.get("operation"), capability.get("operations", []))
        and _data_scope_is_covered(need.get("data_scope"), capability.get("data_scope", []))
        and _delegation_scope_is_covered(need.get("delegation_scope"), capability.get("delegation_scope", []))
        and _effect_scope_is_covered(need.get("effect_scope"), capability.get("effect_scope", []))
        and _time_scope_is_covered(need.get("time_scope"), capability.get("time_scope", []))
    )


def _candidate_set_covers_roles(
    candidate_set: tuple[int, ...], role_candidates: dict[str, list[int]]
) -> bool:
    return all(any(index in candidate_set for index in indexes) for indexes in role_candidates.values())


def _witness_obligations(capabilities: list[dict[str, Any]], candidate_set: tuple[int, ...]) -> list[str]:
    return sorted(_witness_obligation_specs(capabilities, candidate_set))


def _witness_obligation_specs(
    capabilities: list[dict[str, Any]], candidate_set: tuple[int, ...]
) -> dict[str, str]:
    obligations: dict[str, str] = {}
    for index in candidate_set:
        for obligation in capabilities[index].get("obligations", []):
            name = _obligation_name(obligation)
            mode = _obligation_mode(obligation)
            if mode == "must_discharge" or name not in obligations:
                obligations[name] = mode
    return obligations


def _obligations_missing(row: dict[str, Any], consumption: dict[str, Any]) -> bool:
    witness = find_minimal_authority_witness(row, consumption)
    return bool(witness["undischarged_obligations"])


def _undischarged_obligations(
    obligation_specs: dict[str, str], consumption: dict[str, Any]
) -> list[str]:
    carried = set(consumption.get("carried_obligations", []))
    discharged = set(consumption.get("discharged_obligations", []))
    return [
        name
        for name, mode in sorted(obligation_specs.items())
        if (name not in discharged if mode == "must_discharge" else name not in discharged and name not in carried)
    ]


def _obligation_name(obligation: Any) -> str:
    if isinstance(obligation, dict):
        return str(obligation["name"])
    return str(obligation)


def _obligation_mode(obligation: Any) -> str:
    if isinstance(obligation, dict):
        return str(obligation.get("mode", "may_carry_forward"))
    return "may_carry_forward"


def _field_is_covered(field: str | None, covered_fields: list[str]) -> bool:
    if field is None:
        return False
    return any(field == covered or field.startswith(f"{covered}.") for covered in covered_fields)


def _operation_is_covered(operation: str | None, covered_operations: list[str]) -> bool:
    if operation is None:
        return False
    return operation in covered_operations


def _data_scope_is_covered(data_scope: str | None, covered_scopes: list[str]) -> bool:
    if data_scope is None:
        return True
    return data_scope in covered_scopes


def _delegation_scope_is_covered(delegation_scope: str | None, covered_scopes: list[str]) -> bool:
    if delegation_scope is None:
        return True
    return delegation_scope in covered_scopes


def _effect_scope_is_covered(effect_scope: str | None, covered_scopes: list[str]) -> bool:
    if effect_scope is None:
        return False
    return effect_scope in covered_scopes


def _time_scope_is_covered(time_scope: str | None, covered_scopes: list[str]) -> bool:
    if time_scope is None:
        return True
    return time_scope in covered_scopes


def _field_family_results(row_results: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    families = sorted({result["laundered_field_family"] for result in row_results})
    output: dict[str, dict[str, float | int]] = {}
    for family in families:
        family_rows = [result for result in row_results if result["laundered_field_family"] == family]
        blocked = sum(1 for result in family_rows if result["laundered_decision"] == "block")
        output[family] = {
            "count": len(family_rows),
            "laundering_block_rate": _ratio(blocked, len(family_rows)),
        }
    return output


def _field_family(field: str) -> str:
    if field == "requires_human_approval":
        return "approval"
    if field in {"risk_level", "risk_report"}:
        return "risk_report"
    if field in {"data_read_scope", "data_write_scope"}:
        return "data_scope"
    return field


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator
