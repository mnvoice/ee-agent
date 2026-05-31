# Source YAML Examples Preservation Constraint

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Constraint

The five user-provided YAML examples in `concept_card_yaml_examples.md` are the source seed examples for the concept-card workflow.

They must be preserved as original source examples.

Allowed handling:

- preserve the original wording and field values
- apply Markdown/code-block formatting for readability
- reference them as seed examples in later records

Disallowed handling:

- silently rewriting the five examples to match later reviewed cards
- treating later Codex patches as retroactive edits to the original examples
- changing risk levels, formulas, trigger words, or memory logic in the source examples without an explicit source-example revision gate
- claiming the five examples are gold set or corpus-grounded final artifacts

## 2. Current Source File

Current preserved source file:

```text
docs/audit/concept_cards/concept_card_yaml_examples.md
```

The five preserved examples are:

1. `RLC resonance`
2. `Laplace transform`
3. `Thevenin equivalent`
4. `symmetrical components`
5. `z-transform`

## 3. Relationship To Reviewed Cards

Reviewed YAML cards under `concept_cards/*.yaml` may differ from the original five source examples because the reviewed card set went through later authoring, review, patch, and risk-boundary gates.

That difference is allowed only if it is represented as later reviewed work.

It must not be described as if the original five source examples themselves were changed.

## 4. Supervisor Rule

Future gates should treat `concept_card_yaml_examples.md` as a preserved source snapshot unless the user explicitly authorizes a source-example revision gate.

