# Scenario 01 — config-helpers / GLM5

**Status:** ❌ execution failed

Side-by-side comparison with the reference BPMN and the other 5 (approach × LLM) cells: [scenario_01.md](../../../../comparisons/scenario_01.md)

## Reference (ground truth) vs. this run

**Reference BPMN**

![ground truth](ground_truth.png)

**Generated BPMN**

_Render failed: `ERROR: IndentationError: unindent does not match any outer indentation level in <script> at line number 124 at column number 4`_  ([log](diagram_render_error.txt))

## This run at a glance

| metric | ground truth | generated | Δ |
|---|---:|---:|---:|
| Lanes | 1 | — |  |
| Elements | 16 | — |  |
| Gateways | 6 | — |  |
| Flows | 18 | — |  |
| Data obj. | 0 | — |  |
| Data assoc. | 0 | — |  |

**Generation:** 6,309 tokens · 163.9s · $0.010

## Files in this folder

- [`input_scenario.md`](input_scenario.md) — natural-language prompt
- [`ground_truth.bpmn`](ground_truth.bpmn) — reference BPMN XML
- [`ground_truth.py`](ground_truth.py) — reference Modelio script
- [`ground_truth.png`](ground_truth.png) — rendered reference diagram
- [`generated.py`](generated.py) — LLM output
- [`metrics.json`](metrics.json) — full metric record
- [`execution_output.txt`](execution_output.txt) — Modelio execution log (from the original experiment)
- [`diagram_render_error.txt`](diagram_render_error.txt) — render failure detail
