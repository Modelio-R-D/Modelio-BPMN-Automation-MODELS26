# Tools

Utilities used during artifact preparation and reproduction.

| Path                              | Purpose                                                                 |
|-----------------------------------|-------------------------------------------------------------------------|
| `run_pipeline.py`                 | **LLM generation pipeline.** Calls OpenRouter for a given `--approach` (`config-helpers` \| `no-helper`) and `--model`, appends generated scripts + token/timing metrics to a JSONL file. Supports `--resume` for interrupted runs. |
| `bpmn_to_complexity.py`           | Parses BPMN XML and extracts structural complexity metrics; enriches the input JSONL with `complexity` and `complexity_metrics` fields. |
| `get_bpmn_metrics.py`             | Modelio macro: inspect complexity metrics of an open diagram interactively from the Script console. |
| `extract_runs_from_jsonl.py`      | Regenerates [`Evaluation/runs/`](../Evaluation/runs/) from [`Evaluation/results/raw_jsonl/`](../Evaluation/results/raw_jsonl/). |

The paper's analysis notebook lives with the data, not here:
[`evaluation/results/Evals.ipynb`](../evaluation/results/Evals.ipynb).
