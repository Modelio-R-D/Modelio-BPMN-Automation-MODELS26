# Evaluation procedure

This document explains *who* ran the controlled benchmark, *when*, with *which
tooling and settings*, and *how* the resulting BPMN models were assessed. It
addresses Reviewer 2 Q2 ("could you specify more details about the
evaluation?") and the meta-review request to make the procedure explicit.

The MATISSE industrial validation followed a different protocol — see
[`matisse/procedure.md`](matisse/procedure.md).

> **TODO (authors):** several fields below are placeholders and need to be
> filled in before the camera-ready / artifact submission. They are marked
> `<<…>>`.

---

## 1. Scope

The controlled benchmark covers **55 BPMN scenarios** from the PMo dataset
(Brissard et al. 2025, arXiv:2507.11356), combining sources from
Mangler/Klievtsova, the PMo benchmark itself, Camunda BPMN-for-Research,
CCC19, and PET. The 55 input scenarios are reproduced under
[`scenarios/`](scenarios/).

Each scenario is evaluated under **2 approaches × 3 LLMs = 6 cells**,
giving **330 runs total**, all stored under [`runs/`](runs/) and
[`results/raw_jsonl/`](results/raw_jsonl/).

## 2. LLM settings

| Model           | Provider             | API endpoint           | Temperature | Top-p     | Max tokens |
|-----------------|----------------------|------------------------|-------------|-----------|------------|
| Claude Opus 4.5 | Anthropic            | `claude-opus-4-5`      | `<<TODO>>`  | `<<TODO>>`| `<<TODO>>` |
| GPT-5.2         | OpenAI / OpenRouter  | `gpt-5-2`              | `<<TODO>>`  | `<<TODO>>`| `<<TODO>>` |
| GLM5            | zai-org / OpenRouter | `glm-5`                | `<<TODO>>`  | `<<TODO>>`| `<<TODO>>` |

**Single run per (scenario, approach, LLM) cell.** The choice of single-run
was made because of the cost envelope and is acknowledged as a threat to
validity (see Reviewer 1 Q2 in the rebuttal).

**Retry policy.** GLM5 occasionally produced syntactically broken output. When
the generated script raised an exception inside Modelio, the **error message
was resubmitted to the same LLM** (1–3 retries). All other generations were
single-shot. The 5 GLM5 failures reported in `tables.md` Table 1 are the
scenarios where the retry budget was exhausted.

## 3. Prompts

Two system prompts, one per approach. They are versioned in this repository:

- Config+Helpers: [`prompts/system_prompt_config_helpers.md`](prompts/system_prompt_config_helpers.md)
- No-Helper:      [`prompts/system_prompt_no_helper.md`](prompts/system_prompt_no_helper.md)

Per-scenario user prompts are formed by wrapping the natural-language
description from [`scenarios/scenario_NN.md`](scenarios/) with the template in
[`prompts/user_prompt_template.md`](prompts/user_prompt_template.md). The
exact text submitted to the LLM for each of the 330 runs is captured in the
`generated.py` file's leading comment and reproducible from the raw JSONL.

## 4. Execution in Modelio

Each generated script was executed inside **Modelio 5.4** with the BPMN
helper library (Config+Helpers approach) or directly against the Modelio
Jython API (No-Helper approach). The execution log per run is stored as
`execution_output.txt` next to the script.

## 5. Measured outcomes

For each run we record:

- `execution_success` — did the generated script complete without exception
- `lanes`, `elements`, `flows`, `gateways`, `data_objects`, `data_assoc` —
  structural metrics extracted from the resulting Modelio model
- `*_generation_time` — wall-clock seconds for the LLM response
- `*_input_tokens`, `*_output_tokens`, `*_total_tokens` — provider-reported
  token counts (used to compute cost in Table 3)

### 5.1 How ground-truth metrics are obtained

Ground-truth metrics (`complexity_metrics` in the JSONL) are **not** parsed
out of the BPMN 2.0 XML directly. Instead, for each scenario we use a
small Jython script — `ground_truth.py`, auto-generated once from
`ground_truth.bpmn` and committed alongside it under
[`runs/<approach>/<llm>/scenario_<NN>/`](runs/) — that *reconstructs the
ground-truth BPMN inside Modelio* using the same
[`BPMN_Helpers.py`](../approaches/config-helpers/BPMN_Helpers.py) library
the experiment uses for the LLM-generated scripts. The structural counts
(lanes, elements, gateways, flows, data objects, data associations) are
then read from the resulting Modelio model.

Using the same helper to count both the ground-truth and the generated
output keeps the two metric vectors **directly comparable**: any
counting convention (e.g., how lanes are counted when nested, how a
gateway with one outgoing flow is treated) applies identically to both
sides, so the MAE reflects model differences, not measurement differences.

Each generated script's structural metrics are likewise read from the
Modelio model it produces — the JSONL fields `lanes`, `elements`,
`flows`, `gateways`, `data`, `data_assoc` are the after-execution counts.

### 5.2 Diagram renders for inspection

After the metric-collection phase, every `generated.py` is re-executed
inside a clean Modelio session — each in its own sub-package under the
`MODELS26` UML package — and the resulting BPMN diagram is exported as
`diagram_generated.png` next to the script. The ground-truth side is
also rendered: each `ground_truth.py` produces a `ground_truth.png`
that lets reviewers compare the reference BPMN diagram against the LLM
output side-by-side. Because every scenario's `ground_truth.py` is the
same across all 6 cells, the ground-truth PNG is rendered once and
copied to the other five.

Both render passes are **for reviewer inspection only** — they do not
feed back into any number in the paper. 312/330 `diagram_generated.png`
renders succeed (the 18 failures are mostly GLM5 syntactic and
hallucinated-import issues, documented per-cell in
`diagram_render_error.txt`); 54/55 unique `ground_truth.png` renders
succeed (`scenario_23`'s `ground_truth.py` is empty in the source JSONL
— `modelio_config: None` — so no ground-truth PNG is produced for it).

The reproducible path for reviewers is the Modelio macro
[`tools/macros/render_all.py`](../tools/macros/render_all.py), which
runs inside a stock Modelio installation and uses only standard Modelio
APIs (`saveInFile("PNG", …)`). The committed PNGs were produced with the
authors' equivalent automation driver
[`tools/render_diagrams.py`](../tools/render_diagrams.py); see
[`tools/README.md`](../tools/README.md) for the relationship between the
two.

## 6. Who ran it, when

- **Generation runs:** executed by `<<author name>>` during
  `<<YYYY-MM-DD .. YYYY-MM-DD>>`.
- **Execution / metric collection:** executed by `<<author name>>` during
  `<<YYYY-MM-DD .. YYYY-MM-DD>>` on `<<machine spec>>`.
- **Analysis:** the [`results/Evals.ipynb`](results/Evals.ipynb) notebook
  produces the paper tables deterministically from the JSONL inputs.

## 7. Threats to validity (procedure-related)

- **Structural-only validation.** Metrics count elements; they do not assess
  *process logic*. Two models with identical counts may still differ in
  semantics.
- **Single-run.** LLMs are non-deterministic; reported differences in
  Tables 5–8 of the paper reflect single executions per cell.
- **Self-evaluation.** The authors implemented both approaches; the choice of
  prompts and helper API surface may favor Config+Helpers.
- **Model-version drift.** LLM endpoints evolve. Token-count and timing
  figures are pinned to model versions as listed in §2.
- **Shared counter for both sides.** Ground-truth and generated metrics
  are produced by the same `BPMN_Helpers.py` counting code (see §5.1).
  Any bias in how the helper counts a particular construct affects both
  sides equally — keeping MAE comparable — but the absolute counts are
  helper-defined rather than abstract BPMN-XML-defined.
