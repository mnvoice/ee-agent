# Electromagnetics Static / Dynamic Bridge v0.2 Learning Route Closeout - 2026-06-01

Scope: review-only closeout for the v0.2 electromagnetic static/dynamic bridge learning route.

This document closes the v0.2 review layer by turning the integrated map, candidate manifest, exam memory lines, and hold cleanup memo into one study route. It does not patch YAML, mutate source data, change answer keys, edit JSON, or create concept cards.

## Guardrails

- Keep PR #1 open, draft, and unmerged.
- Do not patch YAML.
- Do not create new concept-card YAML files.
- Do not promote `expansion_pilot` cards.
- Do not claim gold-set, benchmark, semantic-gain, or production readiness.
- Treat pressure flags as evidence signals only, not patch authorization.

## Supervisor Closeout Judgment

v0.2 is coherent as a learning route.

The route is not:

```text
More formulas to memorize.
```

The route is:

```text
A physical-quantity movement map that teaches how static electromagnetic quantities become circuit, machine, Maxwell, and wave quantities.
```

The most important rule remains:

```text
Usable review row and cleanup row must remain separate.
```

## Final Learning Route

Use this order.

| Order | Bundle | First question | Main movement | Resulting study value |
|---:|---|---|---|---|
| 0 | 정전계 / 정자계 앵커 | What creates the field? | `Q -> E -> D`, `I -> H -> B` | Gives the learner the field and medium vocabulary needed for every later row. |
| 1 | 유도기전력 | Is flux changing? | `Phi or N Phi -> d/dt -> e` | Bridges electromagnetics into machines through Faraday/Lenz. |
| 2 | 인덕턴스 / 결합 | Is it self-coupling or cross-coupling? | `i -> di/dt + L -> e`, `M -> e2` | Bridges fields into circuit inductance and machine winding coupling. |
| 3 | 맥스웰 / 변위전류 | Is D changing with time? | `D -> partial D / partial t -> displacement current -> H` | Bridges electrostatics into Maxwell and electromagnetic waves. |
| 4 | 전자파 속도 | Is the wave in vacuum or medium? | `epsilon, mu -> v` | Bridges medium constants into wave speed and power-engineering line intuition. |

## What To Do First

When a learner opens the integrated HTML, the recommended reading order is:

1. Read the five-bundle map once.
2. Read the physical quantity layer and the vacuum/medium split.
3. Read the bundle-specific solving order.
4. Read the row-level exam memory lines.
5. Ignore hold rows except as warnings.

Do not start from the row list. Start from the movement map.

## Bundle-Specific Study Instructions

### 0. 정전계 / 정자계 앵커

First see:

```text
source distribution -> field -> medium response -> flux/capacitance/energy
```

Use rows:

```text
p5 q3
p7 q8
p11 q3
p36 q1
p37 q3
p39 q7
```

Use with caution:

```text
p36 q1
```

Reason:

```text
p36 q1 has usable capacitance-unit value, but extracted choice text carries appended explanation.
```

### 1. 유도기전력

First see:

```text
Phi or N Phi -> time change -> induced emf
```

Use rows:

```text
p147 q1
p147 q2
```

Study split:

```text
Faraday gives size.
Lenz gives direction.
```

### 2. 인덕턴스 / 결합

First see:

```text
self-coupling L versus cross-coupling M
```

Use rows:

```text
p154 q2
p166 q50
p166 q52
p168 q59
p168 q60
```

Use with caution:

```text
p154 q2
p166 q50
p166 q52
```

Reason:

```text
p154 q2 has cleanup residue in extracted choice text.
p166 q50 and p166 q52 carry figure/OCR caveats.
```

### 3. 맥스웰 / 변위전류

First see:

```text
D(t) -> displacement current -> H
```

Use rows:

```text
p170 q3
p170 q4
p174 q14
```

Study split:

```text
Conduction current is charge flow.
Displacement current is a time-changing electric flux density term.
```

### 4. 전자파 속도

First see:

```text
vacuum constants versus medium constants
```

Use rows:

```text
p180 q43
p180 q47
```

Study split:

```text
Vacuum gives c.
Medium gives v = 1/sqrt(epsilon mu).
```

## Candidate / Caveat / Hold Boundary

| Class | Rows | Treatment |
|---|---|---|
| Usable-review | `p5 q3`, `p7 q8`, `p11 q3`, `p37 q3`, `p39 q7`, `p147 q1`, `p147 q2`, `p168 q59`, `p168 q60`, `p170 q3`, `p170 q4`, `p174 q14`, `p180 q43`, `p180 q47` | Study-facing review rows. |
| Caveated-review | `p36 q1`, `p154 q2`, `p166 q50`, `p166 q52` | Study-facing only with visible caveat. |
| Hold / cleanup-only | `p4 q1`, `p154 q1`, `p158 q9`, `p57 q7`, `p130 q3` | Do not use as study-facing material. |

This boundary is the v0.2 safety layer.

## Cross-Subject Result

The route creates these bridge points:

| Bridge | Target subject | Meaning |
|---|---|---|
| `Phi(t) -> e` | 전기기기 | Generator and transformer induction become field movement, not isolated formula. |
| `L/M coupling -> induced voltage` | 회로이론 / 전기기기 | Inductors and machine windings become two views of flux linkage. |
| `D(t) -> displacement current` | Maxwell / 전자파 | Electrostatics becomes dynamic field theory. |
| `epsilon, mu -> v` | 전력공학 / 전자파 | Medium constants become transmission-line and wave-speed intuition. |

## v0.3 Entry Questions

v0.3 should not start by increasing row count blindly.

It should answer one of these questions:

1. Can the static anchor set be expanded without introducing source conflicts?
2. Can the caveated mutual-inductance rows be paired with figure-aware review notes?
3. Can the Maxwell/displacement-current bridge be connected to wave equations without overclaiming?
4. Can power-engineering transmission-line rows be linked back to `epsilon`, `mu`, `v`, and characteristic impedance?
5. Can a cross-subject learning route be created for another subject using the same physical-quantity movement method?

## Storage Closeout

Canonical local archive:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-06-01/repo-mnvoice-ee-agent-pr-1
```

Main HTML surface:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-06-01/repo-mnvoice-ee-agent-pr-1/electromagnetics_static_dynamic_bridge_v0_1_review_html/electromagnetics_static_dynamic_bridge_v0_2_exam_memory_review.html
```

Related safety memo:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-06-01/repo-mnvoice-ee-agent-pr-1/electromagnetics_v0_2_hold_cleanup_memo_2026-06-01.md
```

## Non-Authorization Closeout

This closeout does not authorize:

- PR merge;
- PR ready-for-review transition;
- YAML mutation;
- source-data mutation;
- answer-key mutation;
- JSON mutation;
- tag/steps mutation;
- concept-card creation;
- concept-card promotion;
- `expansion_pilot` promotion;
- gold-set, benchmark, semantic-gain, or production readiness claims.
