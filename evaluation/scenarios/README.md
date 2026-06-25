# PMo benchmark scenarios

Each of the 55 input scenarios from the PMo dataset, one per file
(`scenario_01.md` … `scenario_55.md`). Every file carries:

- The natural-language process description (the user prompt content)
- The reported complexity level
- The ground-truth structural metrics (lanes, elements, gateways, flows,
  data objects, data associations)

## Regenerating

These files are derived from the JSONL records (any of the six raw files
contains the same 55 `input` fields). The extraction snippet is in the
header of [`scenario_01.md`](scenario_01.md) and is also part of
[`../../tools/extract_runs_from_jsonl.py`](../../tools/extract_runs_from_jsonl.py).
