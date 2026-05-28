# Evaluation

This folder contains everything that supports the paper's quantitative
claims and the qualitative MATISSE validation.

## How to find what you need

| If you want…                                | Look at                                                  |
|---------------------------------------------|----------------------------------------------------------|
| The paper tables (PMo benchmark)            | [`results/tables.md`](results/tables.md)                 |
| The paper tables (MATISSE)                  | [`matisse/partner_metrics.md`](matisse/partner_metrics.md)|
| The 55 PMo input scenarios                  | [`scenarios/`](scenarios/)                               |
| The prompts sent to the LLMs                | [`prompts/`](prompts/)                                   |
| The 330 individual run artifacts            | [`runs/`](runs/)                                         |
| How to reproduce the tables                 | [`../REPRODUCE.md`](../REPRODUCE.md)                     |
| Who ran the benchmark, when, with what LLM settings | [`PROCEDURE.md`](PROCEDURE.md)                   |
| The 6-stage MATISSE pipeline                | [`matisse/procedure.md`](matisse/procedure.md)           |
| The raw JSONL experiment data               | [`results/raw_jsonl/`](results/raw_jsonl/)               |
| The reproducibility notebook                | [`results/Evals.ipynb`](results/Evals.ipynb)             |
| Preliminary baseline experiments (motivation for Config+Helpers) | [`prompts/preliminary_tests/`](prompts/preliminary_tests/) |

## The two evaluations

The paper reports two complementary studies:

1. **MATISSE industrial validation** — 24 scenarios from 7 partners,
   Config+Helpers only, qualitative partner-driven acceptance. Materials are
   confidential; metrics are in [`matisse/`](matisse/).
2. **Controlled PMo benchmark** — 55 scenarios × 2 approaches × 3 LLMs =
   330 runs, structural-metric driven. Materials are fully public; raw data
   in [`results/raw_jsonl/`](results/raw_jsonl/), per-run unpacks in
   [`runs/`](runs/).

## Per-run artifact layout

For every (approach, LLM, scenario) cell, [`runs/`](runs/) contains:

```
runs/<approach>/<llm>/scenario_<NN>/
    input_scenario.md      # natural-language process description
    ground_truth.bpmn      # ground-truth BPMN XML from the PMo dataset
    ground_truth.py        # ground-truth Modelio config
    generated.py           # the LLM-generated script
    execution_output.txt   # Modelio execution log
    metrics.json           # ground-truth and generated metrics + tokens + timing
```

The entire `runs/` tree is regenerated from
[`results/raw_jsonl/`](results/raw_jsonl/) by
[`../tools/extract_runs_from_jsonl.py`](../tools/extract_runs_from_jsonl.py).
