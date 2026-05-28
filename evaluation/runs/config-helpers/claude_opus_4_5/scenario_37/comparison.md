# Scenario 37 — config-helpers / Claude Opus 4.5

**Status:** ⚠️ executed at experiment time, render failed today

Side-by-side comparison with the reference BPMN and the other 5 (approach × LLM) cells: [scenario_37.md](../../../../comparisons/scenario_37.md)

## Reference (ground truth) vs. this run

**Reference BPMN**

![ground truth](ground_truth.png)

**Generated BPMN**

_Render failed: `ERROR: org.modelio.vcore.smkernel.IllegalModelManipulationException: IllegalModelManipulationException [Error: -1, object=null, closure=org.`_  ([log](diagram_render_error.txt))

## This run at a glance

| metric | ground truth | generated | Δ |
|---|---:|---:|---:|
| Lanes | 1 | 4 | +3 |
| Elements | 23 | 21 | -2 |
| Gateways | 11 | 4 | -7 |
| Flows | 30 | 26 | -4 |
| Data obj. | 0 | 5 | +5 |
| Data assoc. | 0 | 7 | +7 |

**Generation:** 5,754 tokens · 29.5s · $0.071

## Files in this folder

- [`input_scenario.md`](input_scenario.md) — natural-language prompt
- [`ground_truth.bpmn`](ground_truth.bpmn) — reference BPMN XML
- [`ground_truth.py`](ground_truth.py) — reference Modelio script
- [`ground_truth.png`](ground_truth.png) — rendered reference diagram
- [`generated.py`](generated.py) — LLM output
- [`metrics.json`](metrics.json) — full metric record
- [`execution_output.txt`](execution_output.txt) — Modelio execution log (from the original experiment)
- [`diagram_render_error.txt`](diagram_render_error.txt) — render failure detail
