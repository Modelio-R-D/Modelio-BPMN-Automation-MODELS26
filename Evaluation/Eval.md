# Evaluation Results

This file covers two complementary evaluations reported in the paper:

1. **MATISSE Industrial Validation** — practical validation with 7 industrial partners on 24 real-world scenarios using the Config+Helpers solution.
2. **Controlled Benchmark (PMo dataset)** — systematic comparison of Config+Helpers vs. No-Helper across 3 LLMs on 55 BPMN scenarios.

**Tool:** Modelio (Jython scripting API)

---

## Part 1 — MATISSE Industrial Validation

Initial validation of the Config+Helpers approach within the [MATISSE](https://matisse-kdt.eu/) European project (Nov 2025 – Feb 2026).  
**24 scenarios · 7 industrial partners · Config+Helpers only**

### Generation-Review Pipeline

A 6-stage pipeline was applied to each scenario:
1. **Partner inputs collection** — informal workflow descriptions (draw.io, MS Word, or both)
2. **LLM-assisted review** — systematic issue detection before generation
3. **LLM generation** — Config+Helpers solution used for all scenarios
4. **Recommendation** — corrected BPMN + structured description shared with partners
5. **Partner review** — accuracy validation, naming alignment, scope decisions
6. **Deliverable** — final BPMN models consolidated into project deliverable

### Table M1 — Detected Issues in Partner-provided Workflows

> 97 issues found across 12 scenarios with quantified reviews (avg 8.1 per scenario).

| Category | Count | % | Examples |
|----------|------:|--:|---------|
| Structural | 34 | 35% | Missing actor lanes, unclear start/end events |
| Data flow | 24 | 25% | Undefined data objects, missing associations |
| Process logic | 22 | 23% | Missing decision gateways, absent feedback loops |
| Traceability | 17 | 17% | Requirement ID mismatches, coverage gaps |
| **Total** | **97** | | avg 8.1 per scenario |

### Table M2 — Partner Retention of Generated BPMN Models

> 22 LLM-generated corrected BPMN models compared against final Modelio models.

| Category | Count | % | Description |
|----------|------:|--:|-------------|
| Adopted as-is | 14 | 64% | Model accepted in Modelio without modification |
| Minor changes | 3 | 14% | Task or lane name adjustments only |
| Major refactor | 5 | 22% | Partners change structure or naming conventions |

### Table M3 — Structural Metrics by Partner (final BPMN models)

| Partner | Domain | Scenarios | Avg Lanes | Avg Tasks | Avg Gateways | Avg Data Obj. | Avg Data Assoc. |
|---------|--------|----------:|----------:|----------:|-------------:|--------------:|----------------:|
| P1 | Railway | 2 | 3.0 | 13.0 | 6.0 | 10.0 | 17.5 |
| P2 | Energy/microgrid | 3 | 4.3 | 11.0 | 1.3 | 4.0 | 8.7 |
| P3 | Smart grid | 4 | 5.0 | 15.8 | 3.3 | 9.0 | 15.5 |
| P4 | Infrastructure | 4 | 4.5 | 11.8 | 4.0 | 6.5 | 11.0 |
| P5 | Manufacturing | 5 | 5.0 | 15.8 | 3.6 | 6.2 | 12.4 |
| P6 | Automotive | 4 | 3.75 | 17.3 | 3.5 | 11.8 | 23.8 |
| P7 | Defense | 2 | 4.0 | 14.0 | 2.5 | 13.0 | 26.0 |
| **All** | | **24** | **4.3** | **14.5** | **3.3** | **8.2** | **14.6** |

### Table M4 — MATISSE vs. PMo Dataset Comparison

| Metric | MATISSE (24 scenarios) | PMo (55 scenarios) | Ratio |
|--------|----------------------:|-------------------:|------:|
| Avg lanes | 4.3 | 1.1 | 3.9× |
| Avg tasks/elements | 14.5 | 22.6 | 0.6× |
| Avg gateways | 3.3 | 8.3 | 0.4× |
| Avg data objects | 8.2 | 0 | — |
| Scenarios with data objects | 23/24 (96%) | 0/55 (0%) | — |
| Avg data associations | 14.6 | 0 | — |
| Avg lines in output | 232 (range 116–549) | 137 (range 53–328) | 1.7× |

> MATISSE scenarios represent collaborative multi-actor workflows (4.3 lanes avg), while PMo scenarios are predominantly single-lane (1.1 lanes avg) with more complex decision logic (8.3 gateways avg). MATISSE outputs are also significantly richer in data objects and associations, highlighting dimensions that controlled benchmarks may underestimate.

---

## Part 2 — Controlled Benchmark (PMo Dataset)

Systematic comparison of **Config+Helpers** vs. **No-Helper** across 3 LLMs on 55 BPMN scenarios from the PMo dataset.

**LLMs evaluated:** Claude Opus 4.5 · GPT-5.2 · GLM5  
**Dataset:** 55 process descriptions from the PMo dataset

---

## Data Files

| File | Experiment | LLM | Description |
|------|-----------|-----|-------------|
| `output/exp_config_helper/generated_configs_modelio_claude_opus_4_5.jsonl` | Config+Helpers | Claude Opus 4.5 | 55 runs — LLM generates intermediate JSON config, executed via BPMN_Helpers.py in Modelio |
| `output/exp_config_helper/generated_configs_helper_GPT_5_2_modelio.jsonl` | Config+Helpers | GPT-5.2 | 55 runs — LLM generates intermediate JSON config, executed via BPMN_Helpers.py in Modelio |
| `output/exp_config_helper/generated_configs_helper_GLM5_modelio.jsonl` | Config+Helpers | GLM5 | 55 runs — LLM generates intermediate JSON config, executed via BPMN_Helpers.py in Modelio |
| `output/exp_no_helper/generated_configs_no_helper_claude_opus_4_5_modelio.jsonl` | No-Helper | Claude Opus 4.5 | 55 runs — LLM generates full Jython script calling Modelio API directly |
| `output/exp_no_helper/generated_configs_no_helper_gpt_5_2_modelio.jsonl` | No-Helper | GPT-5.2 | 55 runs — LLM generates full Jython script calling Modelio API directly |
| `output/exp_no_helper/generated_configs_no_helper_GLM5_modelio.jsonl` | No-Helper | GLM5 | 55 runs — LLM generates full Jython script calling Modelio API directly |

Each JSONL record contains: `execution_success`, `execution_error`, `complexity_metrics` (ground truth), `generated_metrics`, generation time, and token counts (input/output/total).

---

## Table 1 — Execution Success Rates

| Solution | Claude Opus 4.5 | GPT-5.2 | GLM5 |
|----------|-----------------|---------|------|
| Config+Helpers | 55/55 (100%) | 55/55 (100%) | 50/55 (90.9%) |
| No-Helper | 55/55 (100%) | 55/55 (100%) | 48/55 (87.3%) |

> GLM5 failures corrected by resubmitting with the execution error (1–3 retries).

---

## Table 2 — Generation Time (seconds)

| Solution | LLM | Avg | Std | Min | Max |
|----------|-----|----:|----:|----:|----:|
| Config+Helpers | Claude Opus 4.5 | 22.35 | 7.35 | 9.89 | 44.91 |
| Config+Helpers | GPT-5.2 | 49.45 | 28.65 | 10.33 | 132.17 |
| Config+Helpers | GLM5 | 201.13 | 154.63 | 14.88 | 834.52 |
| No-Helper | Claude Opus 4.5 | 68.59 | 5.39 | 54.51 | 81.86 |
| No-Helper | GPT-5.2 | 83.62 | 20.88 | 50.23 | 141.68 |
| No-Helper | GLM5 | 241.43 | 272.93 | 77.73 | 1153.25 |

> Config+Helpers is consistently faster: **3.07×** for Claude, **1.69×** for GPT-5.2, **1.20×** for GLM5.

---

## Table 3 — Token Usage and Average Cost per Run

| Solution | LLM | Input Avg | Output Avg | Total Avg | Total Std | Cost / Run ($) |
|----------|-----|----------:|-----------:|----------:|----------:|---------------:|
| Config+Helpers | Claude Opus 4.5 | 3,638 | 1,796 | 5,433 | 724 | 0.06 |
| Config+Helpers | GPT-5.2 | 3,136 | 3,467 | 6,603 | 2,144 | 0.05 |
| Config+Helpers | GLM5 | 3,118 | 8,567 | 11,685 | 4,695 | 0.02 |
| No-Helper | Claude Opus 4.5 | 12,514 | 7,059 | 19,573 | 573 | 0.24 |
| No-Helper | GPT-5.2 | 10,236 | 7,381 | 17,616 | 1,652 | 0.12 |
| No-Helper | GLM5 | 10,187 | 9,252 | 19,439 | 2,708 | 0.03 |

> Costs based on OpenRouter API pricing (March 2026): Claude $5/$25 per input/output token; GPT-5.2 $1.75/$14; GLM5 $0.72/$2.30.  
> Config+Helpers reduces total token consumption: **3.60×** for Claude, **2.67×** for GPT-5.2, **1.66×** for GLM5.  
> Input reduction is consistent across models (~3.3×). GLM5 output tokens remain nearly unchanged due to verbose chain-of-thought.

---

## Table 4 — Mean Absolute Error (MAE) by Structural Dimension

| Solution | LLM | Overall | Lanes | Elements | Gateways | Flows | Data Obj. | Data Assoc. |
|----------|-----|--------:|------:|---------:|---------:|------:|----------:|------------:|
| Config+Helpers | Claude Opus 4.5 | 4.030 | 2.182 | 4.145 | 4.618 | 6.109 | 2.545 | 4.582 |
| Config+Helpers | GPT-5.2 | 3.782 | 2.182 | 4.364 | 4.727 | 6.418 | 1.564 | 3.236 |
| Config+Helpers | GLM5 | 4.213 | 1.740 | 6.720 | 5.280 | 9.700 | 0.680 | 1.160 |
| No-Helper | Claude Opus 4.5 | 2.794 | 2.273 | 3.855 | 4.745 | 5.891 | 0.000 | 0.000 |
| No-Helper | GPT-5.2 | 2.948 | 2.691 | 4.364 | 4.255 | 6.382 | 0.000 | 0.000 |
| No-Helper | GLM5 | 3.698 | 1.854 | 6.292 | 5.188 | 8.854 | 0.000 | 0.000 |

> MAE = mean absolute difference between generated and ground-truth element counts across 6 structural dimensions. Lower is better.  
> No-Helper records **zero MAE on data objects and associations** because the few-shot examples provided to the LLM do not include them, the LLM simply never generates them.  
> Flows consistently show the highest MAE (5.891–9.700); lanes the lowest (1.740–2.691).

---

## Table 5 — Generated Output Size (lines of code)

| Solution | LLM | Avg Lines | Min | Max |
|----------|-----|----------:|----:|----:|
| Config+Helpers | Claude Opus 4.5 | 143 | 54 | 328 |
| Config+Helpers | GPT-5.2 | 134 | 63 | 253 |
| Config+Helpers | GLM5 | 112 | 53 | 219 |
| No-Helper | Claude Opus 4.5 | 667 | 577 | 765 |
| No-Helper | GPT-5.2 | 634 | 515 | 733 |
| No-Helper | GLM5 | 652 | 502 | 820 |

> Config+Helpers produces ~**5× fewer lines** on average (~130 vs. ~650).

---

## Summary

| Metric | Winner | Notes |
|--------|--------|-------|
| Success rate | Tied (Claude & GPT) | GLM5 slightly lower in both conditions |
| Generation time | Config+Helpers | 1.2–3.1× faster depending on LLM |
| Token consumption | Config+Helpers | 1.7–3.6× fewer tokens |
| Cost | Config+Helpers | Up to 4× cheaper (Claude) |
| Structural accuracy (MAE) | No-Helper | But only because data objects/assoc. are excluded from No-Helper output |
| Output size | Config+Helpers | ~5× fewer lines |

**Best accuracy per dollar:** GPT-5.2 with Config+Helpers  
**Most consistent output:** Claude Opus 4.5 with Config+Helpers  
**Budget option:** GLM5 with Config+Helpers (open-weight, hostable on-premise)
