# PMo benchmark scenarios

Each of the 55 input scenarios from the PMo dataset, one per file
(`scenario_01.md` … `scenario_55.md`). Every file carries:

- The natural-language process description (the user prompt content)
- The reported complexity level
- The ground-truth structural metrics (lanes, elements, gateways, flows,
  data objects, data associations)

These are the inputs fed to the LLMs in the controlled benchmark.

## Sources

The PMo dataset (Brissard et al. 2025, arXiv:2507.11356) consolidates 55
scenarios from five upstream sources. Per-scenario attribution is recorded
in the upstream dataset; this folder preserves only the natural-language
text and ground-truth metrics.

## Regenerating

These files are derived from the JSONL records (any of the six raw files
contains the same 55 `input` fields). The extraction snippet is in the
header of [`scenario_01.md`](scenario_01.md) and is also part of
[`../../tools/extract_runs_from_jsonl.py`](../../tools/extract_runs_from_jsonl.py).
