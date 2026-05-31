# Broad-Scope Patch Gate Precheck

작성일: 2026-06-01 KST
작성자: Codex supervisor

## 1. Purpose

이 문서는 `concept_card_broad_scope_action_plan_2026-06-01.md`의 다음 단계 precheck다.

대상은 broad-scope action plan에서 지정한:

- `patch_candidate` 6건
- 이번 precheck 지시에서 열거된 `optional_note` 15건

이다.

이 문서는 YAML patch가 아니다. 새 concept-card YAML을 만들지 않는다. `expansion_pilot` 카드를 승격하지 않는다. pressure flag는 증거 신호로만 사용한다.

## 2. Source Boundary

사용한 근거:

- `docs/audit/concept_cards/concept_card_100_problem_full_classification_2026-05-31.md`
- `docs/audit/concept_cards/concept_card_64_percent_strategy_decision_memo_2026-06-01.md`
- `docs/audit/concept_cards/concept_card_broad_scope_action_plan_2026-06-01.md`
- `docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md`
- `app/data/questions.json`

주의:

- `app/data/questions.json`의 `solution`과 `steps`는 보조 근거다. 원문/그림/선택지가 충돌할 때는 hard evidence로 쓰지 않는다.
- 출판사 cross-reference row는 usable stem이 없으면 concept-card 실패로 세지 않는다.
- figure-dependent row는 원문 그림 확인 전까지 card patch authorization으로 승격하지 않는다.

## 3. Patch Candidate Row-By-Row Precheck

| priority | problem_id | source condition from classification | source evidence | figure/source dependency | current mapping | patchable as circuit card? | better disposition before gate | precheck decision |
|---:|---|---|---|---|---|---|---|---|
| 1 | `2003_1회_66` | `figure_missing`; `pure_circuit_theory`; `patch_candidate` | Stem asks antiresonance angular frequency of a shown 2-terminal circuit. Choices are `100`, `200`, `400`, `800`; recorded answer is `2`. `solution` says LC resonance/antiresonance, but `steps` calculation reaches `400`, conflicting with recorded answer. | High. The stem explicitly says "그림과 같은"; the actual topology and values decide whether the row is simple LC resonance, antiresonance, or a broader 2-terminal network condition. There is also answer/step inconsistency. | `rlc_resonance`, `q_bandwidth` | Conditionally patchable only after source figure and answer reconciliation. Do not patch from this row alone. | Figure check plus answer-key/data cleanup first; then decide whether the change is a bounded `rlc_resonance` note or a separate antiresonance treatment. | **Gate hold.** Strong pressure signal, but no YAML mutation until figure and answer conflict are resolved. |
| 2 | `2001_3회_71` | `usable`; `broad_scope_exam_circuit`; `patch_candidate` | Stem asks the third-harmonic resonance frequency of an RLC series resonant circuit. Choices are formula variants. Recorded answer is `3`. `solution` incorrectly says the problem is incomplete despite usable stem/choices. | Medium. No explicit figure dependency in the stem. The data issue is in generated solution quality, not necessarily the source stem. | `rlc_resonance`, `harmonics` | Patchable in principle as a narrow bridge between harmonic order and RLC resonance, but the row is better treated as a small optional note unless repeated source evidence appears. | Optional note candidate or narrow patch only after human confirms that third-harmonic resonance belongs in existing `rlc_resonance` rather than a broader harmonics card. | **Human gate required.** Most patchable of the six, but one row should not create a global card change by itself. |
| 3 | `2000_4회_61` | `figure_missing`; `pure_circuit_theory`; `patch_candidate` | Stem asks the condition for the shown circuit impedance to become `R`. Choices include `Z_1 Z_2 = R`, `Z_1 Z_2 = R^2`, and ratio forms. Recorded answer is `1`, but generated solution derives `Z_1 Z_2 = R^2` and marks choice 3. | High. The actual shown circuit is essential. There is a recorded-answer vs solution conflict. | `impedance`, `two_port_network` | Not safely patchable before figure and answer reconciliation. It may be a constant-resistance/image-impedance condition, but the exact circuit determines the formula. | Data cleanup plus figure check; then possibly a bounded two-port/image-impedance caution. | **Gate hold.** Treat as pressure evidence, not patch authorization. |
| 4 | `2002_3회_63` | `figure_missing`; `pure_circuit_theory`; `patch_candidate` | Stem says `Z_01 = 6 ohm` and asks for `R`; inventory calls it image-impedance calculation. Choices in `questions.json` are Laplace-expression options, which do not match the stem. Generated solution assumes a two-port made from series `R` and shunt `1/5 S`. | Very high. Figure is needed, and choices appear cross-contaminated from another row. | `impedance`, `two_port_network` | Not patchable as-is. The topic is plausible, but the row has source/choice damage. | Data cleanup first. Keep as image-impedance pressure signal only after the usable stem/figure/options are restored. | **Data cleanup before gate.** No card evidence until source conflict is repaired. |
| 5 | `2003_3회_75` | `tag_text_mismatch`; `pure_circuit_theory`; `patch_candidate` | Tag says symmetrical components, but stem asks when two image impedances `Z_01` and `Z_02` of a 4-terminal network are equal. Choices include `AD=BC`, `AB=CD`, `A=D`, `B=C`; recorded answer is `3`. No generated solution. | Low to medium. No explicit figure dependency in stem; formula convention still needs human verification. Main issue is wrong tag and missing explanation. | `two_port_network`, `impedance` | Patchable in principle as a two-port convention/formula boundary, but should be checked against accepted image-impedance definitions before patching. | Tag cleanup note plus human formula check. Likely optional/two-port note rather than broad new card. | **Conditional gate candidate.** Can enter human patch gate, but not direct YAML mutation. |
| 6 | `2004_1회_79` | `tag_text_mismatch`; `pure_circuit_theory`; `patch_candidate` | Tag says Laplace inverse, but stem gives four-terminal constants `A=5/3`, `B=800`, `C=1/450 mho`, `D=5/3` and asks transfer constant `theta`. Choices are complex values. Generated solution says information is incomplete. | Medium. Stem has constants and choices, but transfer-constant convention and generated-solution failure require verification. | `two_port_network` | Patchable only after formula/convention verification. This is two-port/transfer-constant detail, not Laplace. | Human formula check; likely two-port convention note or separate image/transfer-constant mini-card candidate if repeated. | **Human gate required.** Keep as pressure signal; do not patch automatically. |

## 4. Patch Candidate Split

| bucket | rows | reading | gate posture |
|---|---|---|---|
| RLC resonance / antiresonance | `2003_1회_66`, `2001_3회_71` | Real circuit-card pressure exists, but one row is figure/answer-conflicted and the other is a single harmonic-order bridge row. | Human review before any `rlc_resonance` change. `2001_3회_71` may be optional-note sufficient. |
| Two-port / image impedance / transfer constants | `2000_4회_61`, `2002_3회_63`, `2003_3회_75`, `2004_1회_79` | The repeated topic is real, but two of four are figure/answer/choice damaged. Two are cleaner tag-mismatch rows. | Do not patch from damaged rows. A human gate can consider a bounded `two_port_network` convention note using the cleaner rows plus restored source evidence. |

## 5. Optional Note Group Precheck

| group | rows | source dependency | disposition | reason |
|---|---|---|---|---|
| Bode / bandwidth / stability | `1999_3회_65`, `2000_4회_66`, `2003_1회_67` | Mixed. `1999_3회_65` is tag/text mismatch with no generated solution; `2000_4회_66` is a control stability pole-location row; `2003_1회_67` is usable first-order closed-loop bandwidth. | Group but do not patch. Split into `bode_plot` optional note for frequency-response bandwidth and control-card backlog for stability criteria. | Do not stretch `bode_plot` into full control stability. Bandwidth may be a bounded frequency-response note; Routh/pole-location stability belongs to control/signal. |
| Non-sinusoidal power | `1998_6회_70`, `1999_6회_66`, `2000_4회_67`, `2004_1회_78` | Mixed. Two rows have usable formulas; `1998_6회_70` has generated-solution failure; `2004_1회_78` lacks the actual waveform/equations in text. | Group as optional note/new-card pressure, not patch. | Harmonic RMS/distortion/average-power details are useful, but current source quality is uneven and may need a non-sinusoidal power mini-track rather than scattered card edits. |
| Waveform to Laplace | `1998_4회_65`, `2001_3회_72`, `2003_1회_70` | `1998_4회_65` is usable impulse-response wording. `2001_3회_72` and `2003_1회_70` are square-wave Laplace rows with corrupted choices and figure dependence. | Optional note/data cleanup split. | Impulse response can support a small `laplace_transform` bridge. Square-wave rows need figure/choice repair before card evidence. |
| RLC transient details | `2001_1회_69`, `2001_1회_70` | `2001_1회_69` is figure-dependent and has a corrupted choice; `2001_1회_70` is usable RLC transient calculation. | Optional note only. | These rows indicate calculation-detail pressure but do not justify broad core changes without a human decision on `second_order_response` vs `rlc_resonance` boundaries. |
| Measurement / scaling | `1999_6회_62` | Usable source; choices have minor OCR oddity but stem/solution are clear enough for evidence. | Optional note candidate. | Meter-range scaling is a worked example of Ohm's law and series resistance, not a new concept-card scope. |
| Frequency locus | `2002_3회_69` | Usable topic but choices are OCR/table-contaminated. | Optional note/data cleanup. | RL admittance/current locus is relevant to impedance/phasor, but choice cleanup and human confirmation are needed before using it as hard evidence. |
| Control-response bridge | `2002_3회_70` | Usable transfer-function step-response row with graph-choice dependency. | Hold for control/signal card planning. | This is closer to control response than circuit-card patching. Do not stretch `laplace_transform` or `second_order_response` to absorb it. |

## 6. What Is Truly Circuit-Card Patchable Now?

Strict reading:

| disposition | rows |
|---|---|
| Can enter human patch gate after source check | `2001_3회_71`, `2003_3회_75`, `2004_1회_79` |
| Must be figure/data cleanup before patch gate | `2003_1회_66`, `2000_4회_61`, `2002_3회_63` |
| Better as optional note, not immediate patch | `1998_4회_65`, `1999_6회_62`, `1999_6회_66`, `2000_4회_67`, `2001_1회_70`, `2003_1회_67` |
| Better held for control/signal planning | `2000_4회_66`, `2002_3회_70` |
| Data cleanup before concept evidence | `1998_6회_70`, `2001_1회_69`, `2001_3회_72`, `2002_3회_69`, `2003_1회_70`, `2004_1회_78` |

This split is intentionally conservative. It prevents the 6 `patch_candidate` rows from being read as six authorized card patches.

## 7. Claim Boundary

This precheck does not claim:

- YAML patch authorization
- new concept-card creation authorization
- `expansion_pilot` promotion
- gold-set completion
- benchmark status
- semantic-gain proof
- production readiness
- PR #1 ready-for-review approval
- PR #1 merge approval

It only says:

```text
The broad-scope pressure signals are real, but several require source repair or human formula review before they can become card changes.
```

## 8. Human Gate Required Before YAML Mutation

Before any YAML mutation, a human supervisor must decide:

1. Whether `2001_3회_71` is enough to add a harmonic-resonance note, or whether it stays optional.
2. Whether `2003_1회_66` has a verified antiresonance topology and a reconciled answer.
3. Whether `2000_4회_61` and `2002_3회_63` can be repaired from the source figure/options.
4. Whether `2003_3회_75` and `2004_1회_79` should become a bounded `two_port_network` note or a separate future image-impedance/transfer-constant card.
5. Whether Bode/stability rows are split between circuit frequency response and control/signal stability.
6. Whether non-sinusoidal power deserves a mini-track rather than scattered optional notes.

## 9. Recommended Next Step

Prepare a source-check packet for the three damaged high-pressure rows:

- `2003_1회_66`
- `2000_4회_61`
- `2002_3회_63`

Then prepare a human-review packet for the two cleaner two-port convention rows:

- `2003_3회_75`
- `2004_1회_79`

No YAML mutation should occur until those gate decisions are recorded.
