# Per-run artifacts

330 folders — one per (approach, LLM, scenario) cell — making every
benchmark run individually inspectable without parsing JSONL.

```
config-helpers/                          no-helper/
├── claude_opus_4_5/                     ├── claude_opus_4_5/
│   ├── scenario_01/                     │   ├── scenario_01/
│   │   ├── input_scenario.md            │   │   ├── input_scenario.md
│   │   ├── ground_truth.bpmn            │   │   ├── ground_truth.bpmn
│   │   ├── ground_truth.py              │   │   ├── ground_truth.py
│   │   ├── ground_truth.png             │   │   ├── ground_truth.png
│   │   ├── generated.py                 │   │   ├── generated.py
│   │   ├── execution_output.txt         │   │   ├── execution_output.txt
│   │   ├── metrics.json                 │   │   ├── metrics.json
│   │   ├── diagram_generated.png        │   │   ├── diagram_generated.png
│   │   └── diagram_render.log           │   │   └── diagram_render.log
│   …                                    │   …
├── gpt_5_2/                             ├── gpt_5_2/
└── glm5/                                └── glm5/
```

## What each file is and where it comes from

| File                       | What it is                                                                                              | How it was produced                                                                                |
|----------------------------|---------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `input_scenario.md`        | The natural-language process description fed to the LLM for this run.                                   | Captured verbatim from the PMo dataset (Brissard et al. 2025).                                     |
| `ground_truth.bpmn`        | The reference BPMN 2.0 XML for the scenario.                                                            | Captured verbatim from the PMo dataset.                                                            |
| `ground_truth.py`          | A Modelio Jython script that *reconstructs* the ground-truth BPMN inside Modelio so the helper can count its lanes, elements, gateways, flows, data objects and data associations. **This is how we compute the ground-truth structural metrics** that the paper's MAE table compares against. | Auto-generated once from `ground_truth.bpmn` (the `# Auto-generated from BPMN XML:` header marks it). |
| `ground_truth.png`         | Modelio render of `ground_truth.py` — the reference BPMN diagram for visual comparison against `diagram_generated.png`. | Rendered once per scenario in the `config-helpers/claude_opus_4_5` cell and copied to the other 5 cells (the underlying `ground_truth.py` is the same across cells for a given scenario). |
| `generated.py`             | The LLM's output for this run — either a `CONFIG = {…}` config (Config+Helpers) or a full Modelio script (No-Helper). | Sent to the LLM in the original experiment; recorded in the JSONL.                                 |
| `execution_output.txt`     | stdout/stderr captured when `generated.py` was run in Modelio during the original experiment.           | Recorded in the JSONL at experiment time.                                                          |
| `metrics.json`             | Ground-truth metrics, generated metrics, token counts, generation time, execution success flag.         | Projection over the JSONL record.                                                                  |
| `diagram_generated.png`    | A re-rendered Modelio screenshot of `generated.py` (the LLM's BPMN diagram).                            | Produced by [`tools/render_diagrams.py`](../../tools/render_diagrams.py) running each `generated.py` in a fresh Modelio session. |
| `diagram_render.log`       | The Modelio execution transcript from rendering `generated.py` (used to debug PNG failures).            | Written by the render driver / macro.                                                              |
| `diagram_render_error.txt` *(only on failures)* | Exception text + truncated traceback when the LLM-generated script could not be re-rendered.  | Written by `tools/render_diagrams.py` when no `diagram_generated.png` was produced.                |

> **Ground-truth vs. generated, in one line.** `ground_truth.py` /
> `ground_truth.png` are *our* Modelio reconstruction of what the BPMN
> should look like (used purely to recount elements and for visual
> comparison). `generated.py` / `diagram_generated.png` are the *LLM's*
> attempt for this run. The point of the comparison is to compare
> structural metrics — and now, side-by-side diagrams — between them.

## Why ground-truth PNGs are rendered once and copied

For each of the 55 scenarios, the `ground_truth.py` content is the same
across all 6 (approach, LLM) cells — modulo a single `execfile()` path
line that the render wrapper rewrites in memory anyway. So we render
once per scenario in the `config-helpers/claude_opus_4_5` cell and copy
the resulting PNG to the matching scenario folder in the other 5 cells.
This produces 54 unique × 6 cells = **324 ground-truth PNG files**.

`scenario_23` is the one exception: its `ground_truth.py` is empty in
the original JSONL (`modelio_config: None`), so no ground-truth PNG is
produced for it in any cell.

## Regenerating

The JSONL is the source of truth; everything except the `.png` files is
derived from it.

```bash
# Refresh all .md / .py / .bpmn / .json files from the JSONL
python tools/extract_runs_from_jsonl.py --clean

# Re-render the PNGs from inside a stock Modelio installation.
# Reviewer path:  tools/macros/render_all.py (Modelio macro)
# Authors' path:  tools/render_diagrams.py (internal driver)
python tools/render_diagrams.py                # generated.py for every cell
python tools/render_diagrams.py --ground-truth --approach config-helpers --llm claude_opus_4_5
# then copy ground_truth.png across the other 5 cells (one-liner; see tools/README.md)
```

Both render paths are idempotent: re-running overwrites existing PNGs
and re-uses per-run sub-packages inside MODELS26.

## About the 18 failed `diagram_generated.png` renders

Of the 330 runs, 312 produced a `diagram_generated.png` and 18 did not.
The failures cluster on the LLMs the paper already identifies as weaker
— most are GLM5 producing syntactically broken Python or hallucinated
Modelio class names, and a handful are Claude/GPT scripts that hit BPMN
well-formedness rules Modelio enforces. The exact failure mode for each
is captured in `diagram_render_error.txt`.

## About ground-truth diagram quality

Modelio's BPMN auto-unmask behavior is non-deterministic (the README
calls this out explicitly): for processes with many elements packed into
a single lane, only a subset may render on a given execution. The
helper retries, but a few ground-truth scenarios needed 2–3 attempts to
converge on a fully-populated diagram. All 54 ground-truth PNGs
committed here passed a final post-render audit confirming zero
`SKIP (no graphics)` lines in their render log.
