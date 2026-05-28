# Scenario 29 — config-helpers / GLM5

**Status:** ❌ execution failed

Side-by-side comparison with the reference BPMN and the other 5 (approach × LLM) cells: [scenario_29.md](../../../../comparisons/scenario_29.md)

## Reference (ground truth) vs. this run

**Reference BPMN**

![ground truth](ground_truth.png)

**Generated BPMN**

![generated](diagram_generated.png)

## This run at a glance

| metric | ground truth | generated | Δ |
|---|---:|---:|---:|
| Lanes | 1 | 4 | +3 |
| Elements | 35 | 32 | -3 |
| Gateways | 12 | 4 | -8 |
| Flows | 50 | 25 | -25 |
| Data obj. | 0 | 9 | +9 |
| Data assoc. | 0 | 13 | +13 |

**Generation:** 14,314 tokens · 200.4s · $0.027

## Files in this folder

- [`input_scenario.md`](input_scenario.md) — natural-language prompt
- [`ground_truth.bpmn`](ground_truth.bpmn) — reference BPMN XML
- [`ground_truth.py`](ground_truth.py) — reference Modelio script
- [`ground_truth.png`](ground_truth.png) — rendered reference diagram
- [`generated.py`](generated.py) — LLM output
- [`diagram_generated.png`](diagram_generated.png) — rendered LLM diagram
- [`metrics.json`](metrics.json) — full metric record
- [`execution_output.txt`](execution_output.txt) — Modelio execution log (from the original experiment)
