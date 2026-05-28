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
Jython API (No-Helper approach). Execution was orchestrated via Modelio
ScriptServer (socket port 9999). The execution log per run is stored as
`execution_output.txt` next to the script.

## 5. Measured outcomes

For each run we record:

- `execution_success` — did the generated script complete without exception
- `lanes`, `elements`, `flows`, `gateways`, `data_objects`, `data_assoc` —
  structural metrics extracted from the resulting Modelio model
- `*_generation_time` — wall-clock seconds for the LLM response
- `*_input_tokens`, `*_output_tokens`, `*_total_tokens` — provider-reported
  token counts (used to compute cost in Table 3)

Ground-truth metrics (`complexity_metrics` in the JSONL) are computed from
the original PMo ground-truth BPMN XML using `tools/compute_metrics.py`
(TODO: add to the repo).

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
