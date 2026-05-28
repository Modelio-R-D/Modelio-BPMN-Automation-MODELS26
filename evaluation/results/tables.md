# PMo controlled benchmark — paper Tables 1–5

Systematic comparison of **Config+Helpers** vs. **No-Helper** across 3 LLMs
on 55 BPMN scenarios from the PMo dataset.

**LLMs:** Claude Opus 4.5 · GPT-5.2 · GLM5  
**Tool:** Modelio (Jython scripting API)  
**Source data:** [`raw_jsonl/`](raw_jsonl/) · reproduced in
[`Evals.ipynb`](Evals.ipynb).

For the MATISSE industrial validation tables (M1–M4), see
[`../matisse/partner_metrics.md`](../matisse/partner_metrics.md).

## Data files

| File                                                                  | Experiment      | LLM             |
|-----------------------------------------------------------------------|-----------------|-----------------|
| `raw_jsonl/exp_config_helper/generated_configs_modelio_claude_opus_4_5.jsonl` | Config+Helpers  | Claude Opus 4.5 |
| `raw_jsonl/exp_config_helper/generated_configs_helper_GPT_5_2_modelio.jsonl`  | Config+Helpers  | GPT-5.2         |
| `raw_jsonl/exp_config_helper/generated_configs_helper_GLM5_modelio.jsonl`     | Config+Helpers  | GLM5            |
| `raw_jsonl/exp_no_helper/generated_configs_no_helper_claude_opus_4_5_modelio.jsonl` | No-Helper | Claude Opus 4.5 |
| `raw_jsonl/exp_no_helper/generated_configs_no_helper_gpt_5_2_modelio.jsonl`         | No-Helper | GPT-5.2         |
| `raw_jsonl/exp_no_helper/generated_configs_no_helper_GLM5_modelio.jsonl`            | No-Helper | GLM5            |

Each JSONL record holds one run of one scenario; fields include
`execution_success`, `execution_error`, `complexity_metrics` (ground truth),
generated structural metrics, generation time, and token counts. The
per-run artifacts (prompt, generated script, execution log) are also
unpacked under [`../runs/`](../runs/).

---

## Table 1 — Execution success rates

| Solution        | Claude Opus 4.5 | GPT-5.2      | GLM5         |
|-----------------|-----------------|--------------|--------------|
| Config+Helpers  | 55/55 (100%)    | 55/55 (100%) | 50/55 (90.9%)|
| No-Helper       | 55/55 (100%)    | 55/55 (100%) | 48/55 (87.3%)|

> GLM5 failures corrected by resubmitting with the execution error
> (1–3 retries).

## Table 2 — Generation time (seconds)

| Solution        | LLM             |   Avg |   Std |  Min |    Max |
|-----------------|-----------------|------:|------:|-----:|-------:|
| Config+Helpers  | Claude Opus 4.5 | 22.35 |  7.35 |  9.89|  44.91 |
| Config+Helpers  | GPT-5.2         | 49.45 | 28.65 | 10.33| 132.17 |
| Config+Helpers  | GLM5            |201.13 |154.63 | 14.88| 834.52 |
| No-Helper       | Claude Opus 4.5 | 68.59 |  5.39 | 54.51|  81.86 |
| No-Helper       | GPT-5.2         | 83.62 | 20.88 | 50.23| 141.68 |
| No-Helper       | GLM5            |241.43 |272.93 | 77.73|1153.25 |

> Config+Helpers is consistently faster: **3.07×** for Claude,
> **1.69×** for GPT-5.2, **1.20×** for GLM5.

## Table 3 — Token usage and average cost per run

| Solution        | LLM             | Input Avg | Output Avg | Total Avg | Total Std | Cost/Run ($) |
|-----------------|-----------------|----------:|-----------:|----------:|----------:|-------------:|
| Config+Helpers  | Claude Opus 4.5 |     3,638 |      1,796 |     5,433 |       724 |         0.06 |
| Config+Helpers  | GPT-5.2         |     3,136 |      3,467 |     6,603 |     2,144 |         0.05 |
| Config+Helpers  | GLM5            |     3,118 |      8,567 |    11,685 |     4,695 |         0.02 |
| No-Helper       | Claude Opus 4.5 |    12,514 |      7,059 |    19,573 |       573 |         0.24 |
| No-Helper       | GPT-5.2         |    10,236 |      7,381 |    17,616 |     1,652 |         0.12 |
| No-Helper       | GLM5            |    10,187 |      9,252 |    19,439 |     2,708 |         0.03 |

> Costs based on OpenRouter API pricing (March 2026): Claude $5/$25 per
> input/output token; GPT-5.2 $1.75/$14; GLM5 $0.72/$2.30.  
> Config+Helpers reduces total token consumption: **3.60×** for Claude,
> **2.67×** for GPT-5.2, **1.66×** for GLM5. Input reduction is consistent
> across models (~3.3×). GLM5 output tokens remain nearly unchanged due to
> verbose chain-of-thought.

## Table 4 — Mean Absolute Error (MAE) by structural dimension

| Solution        | LLM             | Overall | Lanes | Elements | Gateways | Flows | Data Obj. | Data Assoc. |
|-----------------|-----------------|--------:|------:|---------:|---------:|------:|----------:|------------:|
| Config+Helpers  | Claude Opus 4.5 |   4.030 | 2.182 |    4.145 |    4.618 | 6.109 |     2.545 |       4.582 |
| Config+Helpers  | GPT-5.2         |   3.782 | 2.182 |    4.364 |    4.727 | 6.418 |     1.564 |       3.236 |
| Config+Helpers  | GLM5            |   4.213 | 1.740 |    6.720 |    5.280 | 9.700 |     0.680 |       1.160 |
| No-Helper       | Claude Opus 4.5 |   2.794 | 2.273 |    3.855 |    4.745 | 5.891 |     0.000 |       0.000 |
| No-Helper       | GPT-5.2         |   2.948 | 2.691 |    4.364 |    4.255 | 6.382 |     0.000 |       0.000 |
| No-Helper       | GLM5            |   3.698 | 1.854 |    6.292 |    5.188 | 8.854 |     0.000 |       0.000 |

> MAE = mean absolute difference between generated and ground-truth
> element counts across 6 structural dimensions. Lower is better.  
> No-Helper records **zero MAE on data objects and associations** because
> the few-shot examples provided to the LLM do not include them; the LLM
> simply never generates them.  
> Flows consistently show the highest MAE (5.891–9.700); lanes the lowest
> (1.740–2.691).

## Table 5 — Generated output size (lines of code)

| Solution        | LLM             | Avg Lines | Min | Max |
|-----------------|-----------------|----------:|----:|----:|
| Config+Helpers  | Claude Opus 4.5 |       143 |  54 | 328 |
| Config+Helpers  | GPT-5.2         |       134 |  63 | 253 |
| Config+Helpers  | GLM5            |       112 |  53 | 219 |
| No-Helper       | Claude Opus 4.5 |       667 | 577 | 765 |
| No-Helper       | GPT-5.2         |       634 | 515 | 733 |
| No-Helper       | GLM5            |       652 | 502 | 820 |

> Config+Helpers produces ~**5× fewer lines** on average (~130 vs. ~650).

---

## Summary

| Metric                  | Winner             | Notes                                              |
|-------------------------|--------------------|----------------------------------------------------|
| Success rate            | Tied (Claude, GPT) | GLM5 slightly lower in both conditions             |
| Generation time         | Config+Helpers     | 1.2–3.1× faster depending on LLM                   |
| Token consumption       | Config+Helpers     | 1.7–3.6× fewer tokens                              |
| Cost                    | Config+Helpers     | Up to 4× cheaper (Claude)                          |
| Structural accuracy MAE | No-Helper          | But only because data objects/assoc. are excluded  |
| Output size             | Config+Helpers     | ~5× fewer lines                                    |

**Best accuracy per dollar:** GPT-5.2 with Config+Helpers  
**Most consistent output:** Claude Opus 4.5 with Config+Helpers  
**Budget option:** GLM5 with Config+Helpers (open-weight, hostable on-premise)
