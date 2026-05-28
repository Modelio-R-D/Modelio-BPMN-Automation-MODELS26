# Per-run artifacts

330 folders — one per (approach, LLM, scenario) cell — making every
benchmark run individually inspectable without parsing JSONL.

```
config-helpers/                       no-helper/
├── claude_opus_4_5/                  ├── claude_opus_4_5/
│   ├── scenario_01/                  │   ├── scenario_01/
│   │   ├── input_scenario.md         │   │   ├── input_scenario.md
│   │   ├── ground_truth.bpmn         │   │   ├── ground_truth.bpmn
│   │   ├── ground_truth.py           │   │   ├── ground_truth.py
│   │   ├── generated.py              │   │   ├── generated.py
│   │   ├── execution_output.txt      │   │   ├── execution_output.txt
│   │   ├── metrics.json              │   │   ├── metrics.json
│   │   ├── diagram_generated.png               │   │   ├── diagram_generated.png
│   │   └── diagram_render.log        │   │   └── diagram_render.log
│   …                                 │   …
├── gpt_5_2/                          ├── gpt_5_2/
└── glm5/                             └── glm5/
```

## What each file is and where it comes from

| File                       | What it is                                                                                              | How it was produced                                                                                |
|----------------------------|---------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `input_scenario.md`        | The natural-language process description fed to the LLM for this run.                                   | Captured verbatim from the PMo dataset (Brissard et al. 2025).                                     |
| `ground_truth.bpmn`        | The reference BPMN 2.0 XML for the scenario.                                                            | Captured verbatim from the PMo dataset.                                                            |
| `ground_truth.py`          | A Modelio Jython script that *reconstructs* the ground-truth BPMN inside Modelio so the helper can count its lanes, elements, gateways, flows, data objects and data associations. **This is how we compute the ground-truth structural metrics** that the paper's MAE table compares against. | Auto-generated once from `ground_truth.bpmn` (the `# Auto-generated from BPMN XML:` header marks it). |
| `generated.py`             | The LLM's output for this run — either a `CONFIG = {…}` config (Config+Helpers) or a full Modelio script (No-Helper). | Sent to the LLM in the original experiment; recorded in the JSONL.                                 |
| `execution_output.txt`     | stdout/stderr captured when `generated.py` was run in Modelio during the original experiment.           | Recorded in the JSONL at experiment time.                                                          |
| `metrics.json`             | Ground-truth metrics, generated metrics, token counts, generation time, execution success flag.         | Projection over the JSONL record.                                                                  |
| `diagram_generated.png`              | A re-rendered Modelio screenshot of `generated.py` (the diagram a reviewer would actually want to look at). | Produced by [`tools/render_diagrams.py`](../../tools/render_diagrams.py) running each `generated.py` in a fresh Modelio session. |
| `diagram_render.log`       | The Modelio execution transcript from rendering `generated.py` (used to debug PNG failures).            | Written by the render driver / macro.                                                              |
| `diagram_render_error.txt` *(only on failures)* | Exception text + truncated traceback when the LLM-generated script could not be re-rendered.  | Written by `tools/render_diagrams.py` when no `diagram_generated.png` was produced.                          |

> **Ground-truth vs. generated, in one line.** `ground_truth.py` is *our*
> Modelio reconstruction of what the BPMN should look like (used purely to
> recount elements). `generated.py` is the *LLM's* attempt for this run.
> The point of the comparison is to compare structural metrics between them.

## Regenerating

The JSONL is the source of truth; everything except `diagram_generated.png` is
derived from it.

```bash
# Refresh all .md / .py / .bpmn / .json files from the JSONL
python tools/extract_runs_from_jsonl.py --clean

# Re-render the PNGs from inside a stock Modelio installation.
# See tools/README.md for the macro path; the snippet below is the
# authors' internal automation driver and not the reviewer path.
python tools/render_diagrams.py
```

The render driver is idempotent: re-running it overwrites existing PNGs
and re-uses per-run sub-packages inside MODELS26.

## About the 18 failed renders

Of the 330 runs, 312 produced a PNG and 18 did not. The failures cluster
on the LLMs the paper already identifies as weaker — most are GLM5
producing syntactically broken Python or hallucinated Modelio class
names, and a handful are Claude/GPT scripts that hit BPMN well-formedness
rules Modelio enforces. The exact failure mode for each is captured in
`diagram_render_error.txt`.
