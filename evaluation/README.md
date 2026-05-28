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
    input_scenario.md       # natural-language process description
    ground_truth.bpmn       # ground-truth BPMN XML from the PMo dataset
    ground_truth.py         # Modelio script that reconstructs the ground-truth
                            # BPMN so the helper can count its elements
                            # (this is how we obtain the *ground-truth* metrics)
    ground_truth.png        # Modelio render of ground_truth.py (54 unique x 6 cells)
    generated.py            # the LLM-generated script for this run
    execution_output.txt    # Modelio execution log captured at experiment time
    metrics.json            # ground-truth & generated metrics, tokens, timing
    diagram_generated.png   # Modelio render of generated.py (312/330 succeeded)
    diagram_render.log      # transcript of that render
```

See [`runs/README.md`](runs/README.md) for a per-file explanation of
*what* each artifact is and *where it came from*. The entire tree is
regenerable from [`results/raw_jsonl/`](results/raw_jsonl/) plus a
running Modelio — see [`../REPRODUCE.md`](../REPRODUCE.md).
