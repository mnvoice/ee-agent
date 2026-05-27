#!/usr/bin/env python3
"""schema_validator.py - Rule Schema v0.1-draft validator.

Read-only validator for the rule schema and ee-agent profile produced by the
Rule Schema Artifact Revision Gate. Performs minimum structural checks and
optional rules-instance cross-checks (L1-L6). L7/L8 are reported as
unresolved_policy_questions; v0.1 never hard-fails on them.

References:
- docs/.../v_next_results_d3_split/schema_validator_design_v0.1.md
- docs/.../v_next_results_d3_split/schema_validator_implementation_decisions_v0.1.md
- docs/.../v_next_results_d3_split/rule_schema_v0.1_draft.schema.json
- docs/.../v_next_results_d3_split/ee_agent_rule_profile_v0.1_draft.json

Scope (decision D-13 included):
  (a) schema JSON parse
  (b) profile JSON parse
  (c) required root presence (schema 5 + profile 6)
  (d) profile.compatible_schema_version == schema SchemaMetadata.schema_version const
  (e) profile.threshold_proposals.*.status == "proposal"
  (f) if --rules provided: L1-L6 checks
  (g) if --rules provided: L7-L8 report_only + unresolved_policy_questions

Scope (decision D-13 excluded, NOT implemented in v0.1):
  (h) rules migration
  (i) threshold confirmation
  (j) governance verdict application
  (k) schema/profile/rules file modification
  (l) D-4 automation
  (m) JSON Schema draft-07 full validation
  (n) P1-P6 catalog self-check (full)
  (o) warning grade generation

Dependencies: Python standard library only (decision D-12).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Exit codes (decision D-7)
# ---------------------------------------------------------------------------
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_TOOL = 2

# ---------------------------------------------------------------------------
# Schema/profile expected constants (decision D-13 c/d)
# ---------------------------------------------------------------------------
SCHEMA_REQUIRED_ROOTS = (
    "schema_metadata",
    "core",
    "profile_contract",
    "rule_contract",
    "change_report_contract",
)
PROFILE_REQUIRED_ROOTS = (
    "profile_metadata",
    "domain_taxonomy",
    "predicate_library",
    "check_library",
    "threshold_proposals",
    "aggregation_policy",
)
ALL_CHECK_IDS = (
    "schema_root_required",
    "profile_root_required",
    "version_alignment",
    "threshold_status",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
    "L8",
)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only validator for Rule Schema v0.1-draft.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--schema",
        required=True,
        type=Path,
        help="Path to rule_schema_v0.1_draft.schema.json (required).",
    )
    parser.add_argument(
        "--profile",
        required=True,
        type=Path,
        help="Path to ee_agent_rule_profile_v0.1_draft.json (required).",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=None,
        help="Optional rules instance JSON file. If absent, L1-L8 are skipped.",
    )
    parser.add_argument(
        "--change-report",
        type=Path,
        default=None,
        dest="change_report",
        help="Optional ChangeReport JSON file. Reserved for future use; presence "
        "only is recorded in v0.1.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        dest="report_json",
        help="Optional output path for the full JSON report. If absent, only "
        "stdout summary is produced.",
    )
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------
def file_record(path: Path | None) -> dict[str, Any]:
    """Return a metadata record (path, sha256, exists) for an input file."""
    if path is None:
        return {"path": None, "sha256": None, "exists": False}
    if not path.exists():
        return {"path": str(path), "sha256": None, "exists": False}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path), "sha256": digest, "exists": True}


def load_json_or_tool_error(path: Path, label: str) -> Any:
    """Load JSON. On failure raise SystemExit with EXIT_TOOL."""
    if not path.exists():
        print(f"[tool-error] {label} file not found: {path}", file=sys.stderr)
        raise SystemExit(EXIT_TOOL)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[tool-error] {label} JSON parse failed: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_TOOL)
    except OSError as exc:
        print(f"[tool-error] {label} read failed: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_TOOL)


# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------
_JSON_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def _json_type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "null"
    return "unknown"


def _type_matches(value: Any, expected_type: str) -> bool:
    """Minimum type match. Unknown expected_type passes through."""
    py_type = _JSON_TYPE_MAP.get(expected_type)
    if py_type is None:
        return True
    # bool must not satisfy "integer" or "number"
    if expected_type in ("integer", "number") and isinstance(value, bool):
        return False
    return isinstance(value, py_type)


# ---------------------------------------------------------------------------
# Structural checks (D-13 c/d/e)
# ---------------------------------------------------------------------------
def check_schema_root(schema: dict) -> list[dict]:
    """schema JSON Schema document must declare the 5 required root keys
    inside its `properties` block AND list them in `required`."""
    errors: list[dict] = []
    properties = schema.get("properties", {})
    declared_required = schema.get("required", [])
    for key in SCHEMA_REQUIRED_ROOTS:
        if key not in properties:
            errors.append(
                {
                    "check_id": "schema_root_required",
                    "input_locator": f"schema.properties.{key}",
                    "expected": f"property '{key}' declared",
                    "actual": "missing",
                    "severity": "error",
                }
            )
        if key not in declared_required:
            errors.append(
                {
                    "check_id": "schema_root_required",
                    "input_locator": f"schema.required[{key}]",
                    "expected": f"'{key}' listed in schema.required",
                    "actual": "missing",
                    "severity": "error",
                }
            )
    return errors


def check_profile_root(profile: dict) -> list[dict]:
    """profile must contain the 6 required root keys (ProfileContract)."""
    errors: list[dict] = []
    for key in PROFILE_REQUIRED_ROOTS:
        if key not in profile:
            errors.append(
                {
                    "check_id": "profile_root_required",
                    "input_locator": f"profile.{key}",
                    "expected": f"root key '{key}' present",
                    "actual": "missing",
                    "severity": "error",
                }
            )
    return errors


def check_version_alignment(schema: dict, profile: dict) -> list[dict]:
    """profile.compatible_schema_version == schema SchemaMetadata.schema_version const."""
    errors: list[dict] = []
    schema_version_const = (
        schema.get("definitions", {})
        .get("SchemaMetadata", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )
    profile_meta = profile.get("profile_metadata", {})
    profile_compat = profile_meta.get("compatible_schema_version") if isinstance(profile_meta, dict) else None
    profile_version = profile_meta.get("profile_version") if isinstance(profile_meta, dict) else None

    if schema_version_const is None:
        errors.append(
            {
                "check_id": "version_alignment",
                "input_locator": "schema.definitions.SchemaMetadata.properties.schema_version.const",
                "expected": "string const value",
                "actual": "missing",
                "severity": "error",
            }
        )
    if profile_version is None:
        errors.append(
            {
                "check_id": "version_alignment",
                "input_locator": "profile.profile_metadata.profile_version",
                "expected": "string",
                "actual": "missing",
                "severity": "error",
            }
        )
    if profile_compat is None:
        errors.append(
            {
                "check_id": "version_alignment",
                "input_locator": "profile.profile_metadata.compatible_schema_version",
                "expected": "string",
                "actual": "missing",
                "severity": "error",
            }
        )
    if schema_version_const is not None and profile_compat is not None:
        if schema_version_const != profile_compat:
            errors.append(
                {
                    "check_id": "version_alignment",
                    "input_locator": "profile.profile_metadata.compatible_schema_version",
                    "expected": schema_version_const,
                    "actual": profile_compat,
                    "severity": "error",
                }
            )
    return errors


def check_threshold_status(profile: dict) -> list[dict]:
    """profile.threshold_proposals.*.status must equal "proposal"."""
    errors: list[dict] = []
    thresholds = profile.get("threshold_proposals", {})
    if not isinstance(thresholds, dict):
        errors.append(
            {
                "check_id": "threshold_status",
                "input_locator": "profile.threshold_proposals",
                "expected": "object",
                "actual": _json_type_name(thresholds),
                "severity": "error",
            }
        )
        return errors
    for name, body in thresholds.items():
        status = body.get("status") if isinstance(body, dict) else None
        if status != "proposal":
            errors.append(
                {
                    "check_id": "threshold_status",
                    "input_locator": f"profile.threshold_proposals.{name}.status",
                    "expected": "proposal",
                    "actual": status,
                    "severity": "error",
                }
            )
    return errors


# ---------------------------------------------------------------------------
# Rules-based checks (D-13 f, L1-L6)
# ---------------------------------------------------------------------------
def check_L1_id_uniqueness(rules: list) -> list[dict]:
    errors: list[dict] = []
    seen: dict[str, list[int]] = {}
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        rid = rule.get("id")
        if rid is None:
            continue
        seen.setdefault(rid, []).append(idx)
    for rid, occurrences in seen.items():
        if len(occurrences) > 1:
            errors.append(
                {
                    "check_id": "L1",
                    "duplicate_id": rid,
                    "occurrences": [{"rule_index": i} for i in occurrences],
                    "severity": "error",
                }
            )
    return errors


def _predicate_catalog(profile: dict) -> dict[str, dict]:
    lib = profile.get("predicate_library", [])
    if not isinstance(lib, list):
        return {}
    out: dict[str, dict] = {}
    for item in lib:
        if isinstance(item, dict) and isinstance(item.get("predicate_id"), str):
            out[item["predicate_id"]] = item
    return out


def _check_catalog(profile: dict) -> dict[str, dict]:
    lib = profile.get("check_library", [])
    if not isinstance(lib, list):
        return {}
    out: dict[str, dict] = {}
    for item in lib:
        if isinstance(item, dict) and isinstance(item.get("function_id"), str):
            out[item["function_id"]] = item
    return out


def _category_set(profile: dict) -> set[str]:
    cats = profile.get("domain_taxonomy", {}).get("category_enum", [])
    if not isinstance(cats, list):
        return set()
    return {c for c in cats if isinstance(c, str)}


def check_L2_predicate_id(rules: list, predicate_lib: dict[str, dict]) -> list[dict]:
    errors: list[dict] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        criteria = rule.get("criteria", {})
        preds = criteria.get("predicates", []) if isinstance(criteria, dict) else []
        if not isinstance(preds, list):
            continue
        for c_idx, pred in enumerate(preds):
            if not isinstance(pred, dict):
                continue
            pid = pred.get("predicate_id")
            if pid is None:
                continue
            if pid not in predicate_lib:
                errors.append(
                    {
                        "check_id": "L2",
                        "unknown_predicate_id": pid,
                        "rule_id": rule.get("id"),
                        "rule_index": idx,
                        "criteria_index": c_idx,
                        "severity": "error",
                    }
                )
    return errors


def _check_minimum_object_schema(
    instance: dict,
    schema: dict,
    check_id: str,
    locator_base: dict[str, Any],
) -> list[dict]:
    """Minimum check: required fields present + top-level property type match.
    Does NOT perform JSON Schema draft-07 full validation (decision D-12)."""
    errors: list[dict] = []
    if not isinstance(schema, dict):
        return errors
    required = schema.get("required", [])
    if isinstance(required, list):
        for k in required:
            if k not in instance:
                err = {
                    "check_id": check_id,
                    "missing_required": k,
                    "severity": "error",
                }
                err.update(locator_base)
                errors.append(err)
    props = schema.get("properties", {})
    if isinstance(props, dict):
        for k, v in instance.items():
            prop_schema = props.get(k)
            if not isinstance(prop_schema, dict):
                continue
            expected_type = prop_schema.get("type")
            if isinstance(expected_type, str) and not _type_matches(v, expected_type):
                err = {
                    "check_id": check_id,
                    "field": k,
                    "expected_type": expected_type,
                    "actual_type": _json_type_name(v),
                    "severity": "error",
                }
                err.update(locator_base)
                errors.append(err)
    return errors


def check_L3_predicate_args(rules: list, predicate_lib: dict[str, dict]) -> list[dict]:
    errors: list[dict] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        criteria = rule.get("criteria", {})
        preds = criteria.get("predicates", []) if isinstance(criteria, dict) else []
        if not isinstance(preds, list):
            continue
        for c_idx, pred in enumerate(preds):
            if not isinstance(pred, dict):
                continue
            pid = pred.get("predicate_id")
            args = pred.get("args", {})
            cat = predicate_lib.get(pid)
            if cat is None:
                continue
            if not isinstance(args, dict):
                errors.append(
                    {
                        "check_id": "L3",
                        "predicate_id": pid,
                        "rule_id": rule.get("id"),
                        "rule_index": idx,
                        "criteria_index": c_idx,
                        "expected_type": "object",
                        "actual_type": _json_type_name(args),
                        "severity": "error",
                    }
                )
                continue
            arg_schema = cat.get("args_schema", {})
            locator = {
                "predicate_id": pid,
                "rule_id": rule.get("id"),
                "rule_index": idx,
                "criteria_index": c_idx,
            }
            errors.extend(_check_minimum_object_schema(args, arg_schema, "L3", locator))
    return errors


def check_L4_verdict_category(rules: list, category_enum: set[str]) -> list[dict]:
    errors: list[dict] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        verdict = rule.get("verdict", {})
        if not isinstance(verdict, dict):
            continue
        cat = verdict.get("category")
        if cat is None:
            continue
        if cat not in category_enum:
            errors.append(
                {
                    "check_id": "L4",
                    "unknown_category": cat,
                    "rule_id": rule.get("id"),
                    "rule_index": idx,
                    "severity": "error",
                }
            )
    return errors


def check_L5_function_id(rules: list, check_lib: dict[str, dict]) -> list[dict]:
    errors: list[dict] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        ac = rule.get("automated_check", {})
        if not isinstance(ac, dict):
            continue
        fid = ac.get("function_id")
        if fid is None:
            continue
        if fid not in check_lib:
            errors.append(
                {
                    "check_id": "L5",
                    "unknown_function_id": fid,
                    "rule_id": rule.get("id"),
                    "rule_index": idx,
                    "severity": "error",
                }
            )
    return errors


def check_L6_check_parameters(rules: list, check_lib: dict[str, dict]) -> list[dict]:
    errors: list[dict] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        ac = rule.get("automated_check", {})
        if not isinstance(ac, dict):
            continue
        fid = ac.get("function_id")
        params = ac.get("parameters", {})
        cat = check_lib.get(fid)
        if cat is None:
            continue
        if not isinstance(params, dict):
            errors.append(
                {
                    "check_id": "L6",
                    "function_id": fid,
                    "rule_id": rule.get("id"),
                    "rule_index": idx,
                    "expected_type": "object",
                    "actual_type": _json_type_name(params),
                    "severity": "error",
                }
            )
            continue
        param_schema = cat.get("parameters_schema", {})
        locator = {
            "function_id": fid,
            "rule_id": rule.get("id"),
            "rule_index": idx,
        }
        errors.extend(
            _check_minimum_object_schema(params, param_schema, "L6", locator)
        )
    return errors


# ---------------------------------------------------------------------------
# L7/L8 report-only (D-13 g)
# ---------------------------------------------------------------------------
def check_L7_L8(rules: list) -> tuple[list[dict], list[dict]]:
    """Generate report_only items and unresolved_policy_questions for L7/L8.

    v0.1 NEVER hard-fails on L7/L8. Items below are recorded only when the
    relevant fields are present in the rule.
    """
    report_only: list[dict] = []
    saw_L7 = False
    saw_L8 = False

    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        pg = rule.get("priority_group")
        verdict = rule.get("verdict", {}) if isinstance(rule.get("verdict"), dict) else {}
        sev = verdict.get("severity")
        meta = rule.get("metadata", {}) if isinstance(rule.get("metadata"), dict) else {}
        v_status = meta.get("verification_status")
        deprecation_signal = meta.get("deprecation_signal")

        # L7: every (priority_group, severity) combination is policy-undefined in v0.1
        if isinstance(pg, str) and isinstance(sev, str):
            saw_L7 = True
            report_only.append(
                {
                    "check_id": "L7",
                    "rule_id": rule.get("id"),
                    "rule_index": idx,
                    "priority_group": pg,
                    "severity": sev,
                    "combination_observed": f"{pg}+{sev}",
                    "policy_decision_status": "undefined",
                    "severity_grade": "report_only",
                }
            )

        # L8: well_tested rule missing deprecation_signal
        if v_status == "well_tested" and not (
            isinstance(deprecation_signal, str) and deprecation_signal.strip()
        ):
            saw_L8 = True
            report_only.append(
                {
                    "check_id": "L8",
                    "rule_id": rule.get("id"),
                    "rule_index": idx,
                    "verification_status": v_status,
                    "deprecation_signal_present": False,
                    "observation": "well_tested rule without deprecation_signal",
                    "policy_decision_status": "undefined",
                    "severity_grade": "report_only",
                }
            )

    unresolved: list[dict] = []
    if saw_L7:
        unresolved.append(
            {
                "check_id": "L7",
                "decision_needed": (
                    "Rule.priority_group / Verdict.severity combination policy "
                    "is undefined for v0.1."
                ),
                "suggested_options": [
                    "allow-all: accept every combination",
                    "matrix-deny: define per priority_group an allowed severity set",
                    "per-domain: store the matrix in the profile",
                ],
                "context": (
                    "design schema_validator_design_v0.1.md section 3.7. "
                    "v0.1 must not hard-fail."
                ),
            }
        )
    if saw_L8:
        unresolved.append(
            {
                "check_id": "L8",
                "decision_needed": (
                    "RuleMetadata.deprecation_signal vs verification_status "
                    "consistency policy is undefined for v0.1."
                ),
                "suggested_options": [
                    "required-for-well-tested: well_tested rules must declare deprecation_signal",
                    "free-text: deprecation_signal stays free-form",
                    "per-domain: profile lists required metadata fields per verification_status",
                ],
                "context": (
                    "design schema_validator_design_v0.1.md section 3.8. "
                    "v0.1 must not hard-fail."
                ),
            }
        )
    return report_only, unresolved


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def _classify_check_outcome(
    errors: list[dict],
    report_only: list[dict],
    skipped: list[str],
) -> dict[str, str]:
    """Map check_id to 'pass' | 'fail' | 'skip' | 'report_only'."""
    outcome: dict[str, str] = {cid: "pass" for cid in ALL_CHECK_IDS}
    for cid in skipped:
        if cid in outcome:
            outcome[cid] = "skip"
    for err in errors:
        cid = err.get("check_id")
        if cid in outcome and outcome[cid] != "skip":
            outcome[cid] = "fail"
    for item in report_only:
        cid = item.get("check_id")
        if cid in outcome and outcome[cid] not in ("fail", "skip"):
            outcome[cid] = "report_only"
    return outcome


def _decide_exit(errors: list[dict], warnings: list[dict], report_only: list[dict]) -> str:
    if errors:
        return "fail"
    if warnings:
        return "pass_with_warnings"
    if report_only:
        return "pass_with_report_only"
    return "pass"


def _exit_code_for(decision: str) -> int:
    if decision == "fail":
        return EXIT_FAIL
    return EXIT_PASS


def run_validation(args: argparse.Namespace) -> dict[str, Any]:
    """Execute all checks and return the report object."""
    schema_path = args.schema
    profile_path = args.profile
    rules_path = args.rules
    change_report_path = args.change_report

    schema = load_json_or_tool_error(schema_path, "schema")
    profile = load_json_or_tool_error(profile_path, "profile")

    errors: list[dict] = []
    report_only: list[dict] = []
    warnings: list[dict] = []  # v0.1: always empty (decision D-8)
    unresolved: list[dict] = []
    skipped: list[str] = []

    if not isinstance(schema, dict):
        errors.append(
            {
                "check_id": "schema_root_required",
                "input_locator": "schema",
                "expected": "object",
                "actual": _json_type_name(schema),
                "severity": "error",
            }
        )
    else:
        errors.extend(check_schema_root(schema))

    if not isinstance(profile, dict):
        errors.append(
            {
                "check_id": "profile_root_required",
                "input_locator": "profile",
                "expected": "object",
                "actual": _json_type_name(profile),
                "severity": "error",
            }
        )
    else:
        errors.extend(check_profile_root(profile))

    if isinstance(schema, dict) and isinstance(profile, dict):
        errors.extend(check_version_alignment(schema, profile))
        errors.extend(check_threshold_status(profile))

    rules: list | None = None
    if rules_path is not None:
        rules_raw = load_json_or_tool_error(rules_path, "rules")
        # Accept either a bare list or {"rules": [...]} shape (schema allows both at root)
        if isinstance(rules_raw, dict) and isinstance(rules_raw.get("rules"), list):
            rules = rules_raw["rules"]
        elif isinstance(rules_raw, list):
            rules = rules_raw
        else:
            errors.append(
                {
                    "check_id": "L1",
                    "input_locator": "rules",
                    "expected": "array of rules or object with .rules array",
                    "actual": _json_type_name(rules_raw),
                    "severity": "error",
                }
            )
            rules = None

    if rules is not None and isinstance(profile, dict):
        pred_lib = _predicate_catalog(profile)
        check_lib = _check_catalog(profile)
        cat_enum = _category_set(profile)

        errors.extend(check_L1_id_uniqueness(rules))
        errors.extend(check_L2_predicate_id(rules, pred_lib))
        errors.extend(check_L3_predicate_args(rules, pred_lib))
        errors.extend(check_L4_verdict_category(rules, cat_enum))
        errors.extend(check_L5_function_id(rules, check_lib))
        errors.extend(check_L6_check_parameters(rules, check_lib))

        ro, ur = check_L7_L8(rules)
        report_only.extend(ro)
        unresolved.extend(ur)
    else:
        skipped.extend(["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"])

    # change_report is only recorded by presence in v0.1 (no shape checks yet)
    change_report_skipped = change_report_path is None

    outcome = _classify_check_outcome(errors, report_only, skipped)
    passed = sum(1 for v in outcome.values() if v == "pass")
    failed = sum(1 for v in outcome.values() if v == "fail")
    skipped_count = sum(1 for v in outcome.values() if v == "skip")
    report_only_count = sum(1 for v in outcome.values() if v == "report_only")

    exit_decision = _decide_exit(errors, warnings, report_only)

    report = {
        "summary": {
            "total_checks": len(ALL_CHECK_IDS),
            "passed": passed,
            "failed": failed,
            "warned": 0,
            "report_only": report_only_count,
            "skipped": skipped_count,
            "exit_decision": exit_decision,
            "errors_count": len(errors),
            "report_only_items_count": len(report_only),
            "unresolved_policy_questions_count": len(unresolved),
        },
        "errors": errors,
        "warnings": warnings,
        "report_only": report_only,
        "unresolved_policy_questions": unresolved,
        "skipped_checks": skipped,
        "input_files": {
            "schema": file_record(schema_path),
            "profile": file_record(profile_path),
            "rules": file_record(rules_path),
            "change_report": file_record(change_report_path),
        },
        "metadata": {
            "validator_version": "0.1.0",
            "schema_version_const": (
                schema.get("definitions", {})
                .get("SchemaMetadata", {})
                .get("properties", {})
                .get("schema_version", {})
                .get("const")
                if isinstance(schema, dict)
                else None
            ),
            "profile_version": (
                profile.get("profile_metadata", {}).get("profile_version")
                if isinstance(profile, dict)
                else None
            ),
            "change_report_skipped": change_report_skipped,
            "check_outcomes": outcome,
        },
    }
    return report


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def print_stdout_summary(report: dict, args: argparse.Namespace) -> None:
    summary = report["summary"]
    inputs = report["input_files"]
    print("schema_validator v0.1")
    print("=====================")
    print(f"schema:         {inputs['schema']['path']}")
    print(f"profile:        {inputs['profile']['path']}")
    rules_path = inputs["rules"]["path"]
    print(f"rules:          {rules_path if rules_path else '(not provided)'}")
    cr_path = inputs["change_report"]["path"]
    print(f"change_report:  {cr_path if cr_path else '(not provided)'}")
    print()
    print(f"errors:                          {summary['errors_count']}")
    print(f"warnings:                        {summary['warned']}")
    print(f"report_only items:               {summary['report_only_items_count']}")
    print(f"unresolved_policy_questions:     {summary['unresolved_policy_questions_count']}")
    print(f"skipped checks:                  {summary['skipped']}")
    print(f"exit_decision:                   {summary['exit_decision']}")
    if args.report_json:
        print(f"report_json:                     {args.report_json}")


def write_json_report(report: dict, path: Path) -> None:
    """Write the full report JSON. Does NOT modify any input file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = run_validation(args)
    except SystemExit as exc:
        # tool-level error already reported to stderr
        return int(exc.code) if isinstance(exc.code, int) else EXIT_TOOL

    print_stdout_summary(report, args)
    if args.report_json:
        try:
            write_json_report(report, args.report_json)
        except OSError as exc:
            print(f"[tool-error] failed to write report: {exc}", file=sys.stderr)
            return EXIT_TOOL

    return _exit_code_for(report["summary"]["exit_decision"])


if __name__ == "__main__":
    sys.exit(main())
