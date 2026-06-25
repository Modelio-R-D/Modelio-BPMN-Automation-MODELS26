# Dataset — PMo

This folder contains the subset of the **PMo Dataset** used as the controlled
benchmark in our evaluation.

**Citation:**
Brissard, A., Cuppens, F., & Zouaq, A. (2025).
*PMo Dataset* (v1.0.0) [Data set]. Zenodo.
[doi:10.5281/zenodo.15857589](https://doi.org/10.5281/zenodo.15857589)

---

## What we extracted

From the full PMo Dataset we retained two fields per scenario:

| Field | PMo source | Role in our experiment |
|---|---|---|
| Textual description | natural-language process description | **LLM input**  to the model |
| BPMN XML | standardised BPMN 2.0 representation | **Ground truth** (reference diagram for evaluation) |

These 55 records are stored in [`PMo_input.jsonl`](PMo_input.jsonl) (one JSON
object per line).

---

## Ground-truth complexity metrics

Because the evaluation requires objective, structural metrics for each
reference diagram, we added a parser —
[`tools/bpmn_to_complexity.py`](../../tools/bpmn_to_complexity.py) — that
reads the BPMN XML in each record and enriches it with two new fields:

```jsonc
{
  // ... existing fields ...
  "complexity": "Simple",          // "Simple" | "Medium" | "Complex"
  "complexity_metrics": {
    "lanes":        1,             // swimlane count (1 when no pools)
    "elements":    6,             // tasks + gateways + events
    "gateways":     2,             // gateway nodes only
    "flows":       10,             // sequence flows
    "data_objects": 1,             // dataObject / dataObjectReference
    "data_assoc":   1              // dataInputAssociation + dataOutputAssociation
  }
}
```

The enriched file is [`PMo_input_processed.jsonl`](PMo_input_processed.jsonl)
and serves as the source of truth for all ground-truth values reported in the
paper.

To regenerate it from scratch:

```bash
python tools/bpmn_to_complexity.py Evaluation/dataset/PMo_input.jsonl \
       -o Evaluation/dataset/PMo_input_processed.jsonl
```

---

## Human-readable scenario descriptions

For a more convenient, browsable view of the 55 scenarios (one Markdown file
each), see [`Evaluation/scenarios/`](../scenarios/).